#include "scene.h"
#include "qthread.h"

#include <QThread>
#include <base/sceneitem.h>
#include <messages/changecoordsmsg.h>
#include <messages/changeviewrect.h>
#include <messages/createitemmessage.h>
#include <messages/removeitemmessage.h>
#include <messages/setmodeenginemsg.h>
#include <messages/setvelocitymsg.h>

Scene::Scene(QObject *parent)
    : SceneBase(parent)
{
    m_timer = new QTimer(this);

    connect(m_timer, &QTimer::timeout, this, [this](){
        updateItems();
    });
}

Scene::~Scene()
{
}

void Scene::addFactory(const QList<SceneItemFactory *> *factories)
{
    for (auto f : *factories)
    {
        qDebug() << f->type();
        if (!m_factoriesHash.keys().contains(f->type()))
            m_factoriesHash.insert(f->type(), f);
    }
}

void Scene::setEngineInterface(EngineInterface *ei)
{
    if(ei != nullptr)
    {
        m_engineInterface = ei;

        ei->installStreamMsg<CreateItemMsg>([this](CreateItemMsg msg, uint32_t itemId){
            QMutexLocker locker(&m_mutex);
            addItem(QPoint(msg.x, msg.y), msg.objectType, itemId, QVariantMap{{"width", msg.width}, {"height", msg.height}});
        });

        ei->installStreamMsg<RemoveItemMessage>([this](RemoveItemMessage , uint32_t itemId){
            QMutexLocker locker(&m_mutex);
            if (m_sceneItemsRegistry.contains(itemId))
            {
                auto object = m_sceneItemsRegistry[itemId];
                object->setRemovingState(SceneItem::PREPARE);
            }
        });

        ei->installStreamMsg<ChangeCoordsMsg>([this](ChangeCoordsMsg msg, uint32_t itemId){
            QMutexLocker locker(&m_mutex);
            if (m_sceneItemsRegistry.contains(itemId))
            {
                auto object = m_sceneItemsRegistry[itemId];
                object->setX(msg.x);
                object->setY(msg.y);
            }
        });
    }
}

void Scene::setKeyNegotiator(KeyNegotiator *keyNegotiator)
{
    if (keyNegotiator != nullptr)
    {
        m_keyNegotiator = keyNegotiator;

        connect(m_keyNegotiator, &KeyNegotiator::leftPressed, this, [this](){
            if (m_doodlerId < 0) return;
            SetVelocityMsg msg;
            msg.velocity = -1.;
            m_engineInterface->sendToEngine(msg, m_doodlerId);
        });

        connect(m_keyNegotiator, &KeyNegotiator::leftReleased, this, [this](){
            if (m_doodlerId < 0) return;
            SetVelocityMsg msg;
            msg.velocity = -2;
            m_engineInterface->sendToEngine(msg, m_doodlerId);
        });

        connect(m_keyNegotiator, &KeyNegotiator::rightPressed, this, [this](){
            if (m_doodlerId < 0) return;
            SetVelocityMsg msg;
            msg.velocity = 1.;
            m_engineInterface->sendToEngine(msg, m_doodlerId);
        });

        connect(m_keyNegotiator, &KeyNegotiator::rightReleased, this, [this](){
            if (m_doodlerId < 0) return;
            SetVelocityMsg msg;
            msg.velocity = 2;
            m_engineInterface->sendToEngine(msg, m_doodlerId);
        });

        connect(m_keyNegotiator, &KeyNegotiator::pausePressed, this, [](){
            //! TODO finish pause implementation
            //SetModeEngineMsg msg;
            //msg.mode = EngineMode::PAUSE;
            //m_engineInterface->sendToEngine(msg);
        });

        connect(m_keyNegotiator, &KeyNegotiator::pausePressed, this, [this](){
            //! TODO finish pause implementation
            SetModeEngineMsg msg;
            msg.mode = EngineMode::START;
            m_engineInterface->sendToEngine(msg);
        });

        connect(m_keyNegotiator, &KeyNegotiator::firePressed, this, [](QPointF pos){
            //! TODO finish fire implementation
             //qDebug() << pos;
        });
    }
}

void Scene::startTest()
{
    m_timer->start(100);
    SetModeEngineMsg startEngineMsg;
    startEngineMsg.mode = EngineMode::START;
    m_engineInterface->sendToEngine(startEngineMsg).onCompleted<SetModeEngineMsgAns>([](const SetModeEngineMsgAns & ans){
        qDebug() << ":start" << ans.modeChangedSuccess;
    });
}

uint32_t Scene::getDoodlerId()
{
    return m_doodlerId;
}

SceneItem *Scene::addItem(QPoint pos, QString objectType, uint32_t id, QVariantMap initialParams)
{
    SceneItem * item = nullptr;

    if (objectType.toUpper().contains("DOODLER"))
    {
        m_doodlerId = id;
    }

    if (m_factoriesHash.contains(objectType))
    {
        QVariantMap m{{"x", pos.x()}, {"y" , pos.y()}};
        for (const QString& str : initialParams.keys())
        {
            m[str] = initialParams[str];
        }
        item = m_factoriesHash[objectType]->create(m);
        item->setObjectName(objectType);
        //item->setParent(this);
        item->setId(id);

        m_sceneItemsRegistry[id] = item;
        qDebug() << "Scene create:" << item->id();
        m_sceneItems.push_back(item);
        setObjectsCount(m_sceneItems.count());
    }
    return item;
}

SceneItem *Scene::addItem(double x, double y, QString objectType, uint32_t id)
{
    return addItem(QPoint(x, y), objectType, id);
}

void Scene::removeItem(SceneItem *item)
{
    if (item != nullptr)
    {
        m_sceneItems.removeAll(item);
        qDebug() << "Scene remove:" << item->id();
        delete item;
        setObjectsCount(m_sceneItems.count());
    }
}

void Scene::updateItems()
{
    QMutexLocker locker(&m_mutex);
    for (int i = m_sceneItems.length() - 1; i >= 0  ; i--)
    {
        //! Cannot set parent for item from another thread
        //if (m_sceneItems[i]->parent() == nullptr)
        //{
        //    m_sceneItems[i]->moveToThread(QThread::currentThread());
        //    m_sceneItems[i]->setParent(this);
        //}

        if (m_sceneItems[i]->removingState() == SceneItem::READY)
        {
            removeItem(m_sceneItems[i]);
        }
    }
}

const QRectF &Scene::resolution()
{
    return m_resolution;
}

void Scene::setResolution(const QRectF &newResolution)
{
    if (m_resolution == newResolution)
        return;
    m_resolution = newResolution;
    emit resolutionChanged(m_resolution);
}

const QRectF &Scene::viewRect() const
{
    return m_viewRect;
}

void Scene::setViewRect(const QRectF &newViewRect)
{
    if (m_viewRect == newViewRect)
        return;
    m_viewRect = newViewRect;
    if (m_engineInterface)
    {
        ChangeViewRectMsg msg;
        msg.viewRect = m_viewRect;
        m_engineInterface->sendToEngine(msg);
    }
    emit viewRectChanged(m_viewRect);
}

int Scene::objectsCount() const
{
    return m_objectsCount;
}

void Scene::setObjectsCount(int newObjectsCount)
{
    if (m_objectsCount == newObjectsCount)
        return;
    m_objectsCount = newObjectsCount;
    emit objectsCountChanged();
}
