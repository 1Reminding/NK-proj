#include "enginebase.h"
#include "engineinterface.h"

#include <QRectF>
#include <QThread>

static inline bool containsType(int type, int sequance)
{
    return (type & sequance) == type;
}

EngineBase::EngineBase()
{
    m_interface = new EngineInterface;
    m_interface->m_engine = this;
    messageNegotiator = new MessageNegotiator;
    m_levelGenerator = new LevelGenerator();
    m_collisionDetector = new CollisionDetector();

    m_levelGenerator->setBoundingRectGetter([this](QString type) -> QRectF{
        if (m_controllersBoundingRect.contains(type + "Controller"))
        {
            return m_controllersBoundingRect[type + "Controller"];
        }
        return {};
    });

    doMath = false;
}

EngineBase::~EngineBase()
{
    delete m_interface;
    delete messageNegotiator;
}

EngineInterface *EngineBase::getInterface() const
{
    return m_interface;
}

LevelGenerator *EngineBase::getLevelGenerator() const
{
    return m_levelGenerator;
}

void EngineBase::setViewRect(QRectF rect)
{
    m_viewRect = rect;
}

void EngineBase::proceed(int uSecond, int dt)
{
    Q_UNUSED(dt)
    //take msgs from interface and proceed them
    while (true)
    {
        QByteArray serMsg = m_interface->toEngineBase.pop();
        if (serMsg.isEmpty()) break;
        QDataStream stream(&serMsg, QIODevice::ReadOnly);
        MessageHeader msgMessageHeader;
        stream >> msgMessageHeader;

        QByteArray answ;
        if (msgMessageHeader.itemId == -1)
        { //msg for controller
            answ = messageNegotiator->proceedMsg(&msgMessageHeader, stream);
        }
        else
        { //global msg
            answ = proceedItemMsg(msgMessageHeader, stream);
        }

        if (answ.size() > 0) {
            m_interface->_pushAnswerEngineSide(answ, &msgMessageHeader);
        }
    }

    if(doMath)
    {
        m_levelGenerator->proceed(m_viewRect);
        //proceed physical items
        for (auto c : m_objectControllers)
        {
            c->proceed(1000, m_viewRect);
        }

        for (auto d : m_collideObjectControllers)
        {
            for (auto c : qAsConst(m_objectControllers))
            {
                if (containsType(static_cast<int>(c->getControllerType()), d->getCollidableTypes()))
                {
                    m_collisionDetector->proceed(d, c);
                }
            }
            d->proceed(1000, m_viewRect);
        }

        m_engineTime += 1000; // uSecond
        prevTime_us = uSecond;
    }
}

void EngineBase::insertController(uint32_t id, AbstractObjectController* c)
{
    if (c->getControllerType() == ControllerType::BULLET || c->getControllerType() == ControllerType::DOODLER)
    {
        m_collideObjectControllers.insert(id, c);
    }
    else
    {
        m_objectControllers.insert(id, c);
    }
}

bool EngineBase::removeController(uint32_t id)
{
    auto iter = m_objectControllers.find(id);
    if (iter == m_objectControllers.end())
    {
        return false;
    }

    delete iter.value();
    m_objectControllers.erase(iter);

    return true;
}

QByteArray EngineBase::proceedItemMsg(MessageHeader header, QDataStream &s)
{
    for (const auto c : qAsConst(m_objectControllers))
    {
        if (c->getPiId() == header.itemId)
        {
            return c->proceedMsg(&header, s);
        }
    }

    for (const auto c : qAsConst(m_collideObjectControllers))
    {
        if (c->getPiId() == header.itemId)
        {
            return c->proceedMsg(&header, s);
        }
    }
    return nullptr;
}

unsigned long long EngineBase::engineTime() const
{
    return m_engineTime;
}
