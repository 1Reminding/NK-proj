#ifndef ABSTRACTOBJECTCONTROLLER_H
#define ABSTRACTOBJECTCONTROLLER_H

#include "messageheader.h"
#include "messagenegotiator.h"
#include "core_global.h"
#include "collisiondetector.h"

#include <QRectF>

enum class ControllerType : uint8_t
{
    SLAB = 1,
    MONSTER = 2,
    DOODLER = 4,
    GHOST = 8,      //multiplayer doodler
    BULLET = 16,
    POWERUP = 32,
    TRAP = 64
};

class EngineBase;

class CORE_EXPORT AbstractObjectController
{
public:
    AbstractObjectController();
    virtual ~AbstractObjectController();

    virtual void proceedCollision(ControllerType controllerType, CollisionType collisionType) = 0;
    virtual void proceed(double dt, QRectF &visualRect) = 0;
    virtual void init(QPointF startPoint) = 0;

    //random initialization
    virtual bool needInitWithRandomValue() { return false; }
    virtual double getRangeFrom() { return 0; }
    virtual double getRangeTo() { return 0; }
    virtual void setRandomValue(double value) { Q_UNUSED(value) }
    virtual void setViewRect(QRectF &viewRect) {  Q_UNUSED(viewRect) }

    QByteArray proceedMsg(MessageHeader *header, QDataStream &stream);

    QRectF getBoundingRect();
    ControllerType getControllerType();
    int getCollidableTypes();
    double getVelocityX();
    double getVelocityY();

    void setPiId(int value);
    int getPiId() const { return m_id; }
    void setEngineBase(EngineBase *e);
    CollisionType getCollisionType();

protected:
    void changePos(QPointF point);
    void changeX(double x);
    void changeY(double y);

protected:
    EngineBase *m_engine = nullptr;
    uint32_t m_id;
    MessageNegotiator *m_negotiator ;

    QRectF m_boundingRect;
    CollisionType m_collisionType = CollisionType::NONE;
    ControllerType m_controllerType = ControllerType::SLAB;
    int m_collidableTypes = 0;
    double m_velocityX = 0;
    double m_velocityY = 0;
};

#endif // ABSTRACTCONTROLLER_H
