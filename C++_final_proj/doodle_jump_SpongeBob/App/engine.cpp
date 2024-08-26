#include "engine.h"
#include <QtConcurrent>
#include <chrono>
#include <ctime>
#include <engineinterface.h>

using namespace std::chrono_literals;

Engine::Engine(QObject *parent) : QObject(parent), EngineBase()
{
    m_lastCreatedPIID = 0;
    messageNegotiator->registerMsgHandler(&Engine::proceedSetEngineModeMsg, this);
    messageNegotiator->registerMsgHandler(&Engine::proceedChangeViewRectMsg, this);

    m_levelGenerator->setCreateHandler([this](QString name, QPointF pos){
       return createObject(name, pos);
    });

    m_levelGenerator->setDeleteHandler([this](uint32_t id){
        return deleteObject(id);
    });
    m_generator.setSeed(0137);
}

Engine::~Engine()
{
    m_engineThread.cancel();
    m_interfaceProceeder.cancel();
    m_interfaceProceeder.waitForFinished();
    m_engineThread.waitForFinished();
}

void Engine::start()
{
    m_engineThread = QtConcurrent::run([this](){
        const int delay = 1000; // microsec
        auto start = std::chrono::system_clock::now();
        auto last = std::chrono::system_clock::now();
        while (this->working)
        {
            auto now = std::chrono::system_clock::now();
            auto dt = std::chrono::duration_cast<std::chrono::microseconds>(now - last).count();
            if (dt > delay)
            {
                auto t1 = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::system_clock::now() - start).count();
                proceed(t1, dt);
                last = now;
            }
        }
    });
    //
    m_interfaceProceeder = QtConcurrent::run([this](){
        while (this->working)
        {
            m_interface->proceed();
            for (const auto &proceeder : qAsConst(m_proceeders))
            {
                proceeder();
            }
        }
    });
}

void Engine::stop()
{
    working = false;
    m_interfaceProceeder.cancel();
    m_engineThread.cancel();
    m_engineThread.waitForFinished();
    m_interfaceProceeder.waitForFinished();
}

void Engine::addControllerFactories(const QList<ControllerFactory *> *value)
{
    for (auto* controller : *value)
    {
        m_objectControllerFactories.insert(controller->type(), controller);
        //getting controller baunding rect
        auto instance = controller->create();
        m_controllersBoundingRect.insert(controller->type(), instance->getBoundingRect());
        delete instance;
    }
}

void Engine::addCollideControllerFactories(const QList<ControllerFactory *> *value)
{
    for (auto* controller : *value)
    {
        m_collideControllerFactories.insert(controller->type(), controller);
        //getting controller baunding rect
        auto instance = controller->create();
        m_controllersBoundingRect.insert(controller->type(), instance->getBoundingRect());
        delete instance;
    }
}

void Engine::addProceeder(std::function<void ()> proceeder)
{
    m_proceeders.push_back(proceeder);
}

SetModeEngineMsgAns Engine::proceedSetEngineModeMsg(SetModeEngineMsg msg)
{
    if(msg.mode == START)
    {
        this->doMath = true;
    }

    if(msg.mode == PAUSE || msg.mode == STOP)
    {
        this->doMath = false;
    }

    if(msg.mode == STOP)
    {
        for (auto p : m_objectControllers)
        {
            delete p;
        }
        m_objectControllers.clear();
        m_lastCreatedPIID = -1;
    }

    SetModeEngineMsgAns msgAnswer;
    msgAnswer.modeChangedSuccess = true;
    msgAnswer.mode = msg.mode;
    return msgAnswer;
}

ChangeViewRectMsgAns Engine::proceedChangeViewRectMsg(ChangeViewRectMsg msg)
{
    setViewRect(msg.viewRect);
    ChangeViewRectMsgAns ans;
    ans.success = true;
    return ans;
}

uint32_t Engine::createObject(QString type, QPointF pos)
{
    ControllerFactory* factory = nullptr;
    auto it = m_objectControllerFactories.find(QString(type + QString("Controller")));
    if (it == m_objectControllerFactories.end())
    {
        it = m_collideControllerFactories.find(QString(type + QString("Controller")));
        if (it == m_collideControllerFactories.end())
        {
            qDebug() << "error, controller" << type << "doesn't exist";
            return -1;
        }
    }
    factory = it.value();

    AbstractObjectController *controller = factory->create();
    m_lastCreatedPIID++;
    controller->setPiId(m_lastCreatedPIID);
    controller->setEngineBase(this);
    controller->setViewRect(m_viewRect);

    while(controller->needInitWithRandomValue())
    {
        double topValue = controller->getRangeTo();
        double bottomValue = controller->getRangeFrom();

        controller->setRandomValue(m_generator.generate()%static_cast<int>(topValue-bottomValue)+bottomValue);
    }

    controller->init(pos);

    insertController(m_lastCreatedPIID, controller);

    CreateItemMsg msg;
    msg.x = pos.x();
    msg.y = pos.y();
    msg.width = controller->getBoundingRect().width();
    msg.height = controller->getBoundingRect().height();
    msg.objectType = type;
    msg.id = m_lastCreatedPIID;
    m_interface->sendFromEngine(msg, m_lastCreatedPIID);

    //qDebug() << "Engine create" << msg.id;

    return m_lastCreatedPIID;
}

bool Engine::deleteObject(uint32_t id)
{
    RemoveItemMessage msg;
    msg.ids = {id};
    if (m_collideObjectControllers.contains(id))
    {
        delete m_collideObjectControllers[id];
        m_collideObjectControllers.remove(id);
    }
    else if (m_objectControllers.contains(id))
    {
        delete m_objectControllers[id];
        m_objectControllers.remove(id);
    }
    else
    {
        return false;
    }
    //qDebug() << "Engine delete" << id;
    m_interface->sendFromEngine(msg, id);
    return true;
}

