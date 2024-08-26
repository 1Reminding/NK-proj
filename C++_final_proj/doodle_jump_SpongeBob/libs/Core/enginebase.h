 #ifndef ENGINEBASE_H
#define ENGINEBASE_H

#include <vector>
#include <map>
#include <functional>
#include "abstractobjectcontroller.h"
#include "levelgenerator.h"
#include <messagenegotiator.h>
#include <core_global.h>
#include <mutex>

class AbstractObjectController;
class EngineInterface;

class CORE_EXPORT EngineBase
{
public:
    EngineBase();
    ~EngineBase();

    EngineInterface *getInterface() const;
    LevelGenerator *getLevelGenerator() const;
    void setViewRect(QRectF rect);

    virtual void start() = 0;
    virtual void stop() = 0;

    unsigned long long engineTime() const;

protected:
    void proceed(int uSecond, int dt);
    bool removeController(uint32_t id);
    void insertController(uint32_t id, AbstractObjectController *c);
    QByteArray proceedItemMsg(MessageHeader header, QDataStream &s);

protected:
    uint32_t m_lastCreatedPIID = 0;
    QMap<uint32_t, AbstractObjectController*> m_objectControllers;
    QMap<uint32_t, AbstractObjectController*> m_collideObjectControllers;
    QMap<QString, QRectF> m_controllersBoundingRect;
    MessageNegotiator* messageNegotiator = nullptr;
    EngineInterface* m_interface = nullptr;
    LevelGenerator* m_levelGenerator = nullptr;
    CollisionDetector* m_collisionDetector = nullptr;
    bool doMath = false;
    QRectF m_viewRect;

private:
    int prevTime_us = 0;
    unsigned long long m_engineTime = 0;
};


#endif // ENGINEBASE_H
