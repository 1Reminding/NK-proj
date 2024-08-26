#ifndef ENGINE_H
#define ENGINE_H

#include <QFuture>
#include <QObject>
#include <QTimer>
#include <enginebase.h>
#include <messages/changeviewrect.h>
#include <messages/createitemmessage.h>
#include <messages/removeitemmessage.h>
#include <messages/setmodeenginemsg.h>
#include <messages/setvelocitymsg.h>
#include <factories/controllerfactory.h>

class Engine : public QObject, public EngineBase
{
public:
    Engine(QObject *parent = nullptr);
    ~Engine();

    void start();
    void stop();

    void addControllerFactories(const QList<ControllerFactory *> *value);
    void addCollideControllerFactories(const QList<ControllerFactory *> *value);
    void addProceeder(std::function<void()> proceeder);

private:
    SetModeEngineMsgAns proceedSetEngineModeMsg(SetModeEngineMsg msg);
    ChangeViewRectMsgAns proceedChangeViewRectMsg(ChangeViewRectMsg msg);

    uint32_t createObject(QString type, QPointF pos);
    bool deleteObject(uint32_t id);

private:
    QHash<QString, ControllerFactory*> m_objectControllerFactories;
    QHash<QString, ControllerFactory*> m_collideControllerFactories;
    QList<std::function<void()>> m_proceeders;
    QFuture<void> m_engineThread;
    QFuture<void> m_interfaceProceeder;
    RandomGenerator m_generator;
    bool working = true;
};

#endif // ENGINE_H
