#include "abstractobjectcontroller.h"

AbstractObjectController::AbstractObjectController()
{
    m_negotiator = new MessageNegotiator;
}

AbstractObjectController::~AbstractObjectController()
{
    delete m_negotiator;
}

QRectF AbstractObjectController::getBoundingRect()
{
    return m_boundingRect;
}

ControllerType AbstractObjectController::getControllerType()
{
    return m_controllerType;
}

int AbstractObjectController::getCollidableTypes()
{
    return m_collidableTypes;
}

double AbstractObjectController::getVelocityX()
{
    return m_velocityX;
}

double AbstractObjectController::getVelocityY()
{
    return m_velocityY;
}

void AbstractObjectController::setPiId(int value)
{
    m_id = value;
}

void AbstractObjectController::setEngineBase(EngineBase *value)
{
    m_engine = value;
}

CollisionType AbstractObjectController::getCollisionType()
{
    return m_collisionType;
}

QByteArray AbstractObjectController::proceedMsg(MessageHeader* header, QDataStream &stream)
{
    return m_negotiator->proceedMsg(header, stream);
}

void AbstractObjectController::changePos(QPointF point)
{
    changeX(point.x());
    changeY(point.y());
}

void AbstractObjectController::changeX(double x)
{
    m_boundingRect = {x, m_boundingRect.y(), m_boundingRect.width(), m_boundingRect.height()};
}

void AbstractObjectController::changeY(double y)
{
    m_boundingRect = {m_boundingRect.x(), y, m_boundingRect.width(), m_boundingRect.height()};
}
