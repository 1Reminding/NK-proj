#include "collisiondetector.h"
#include "abstractobjectcontroller.h"
#include <QDebug>

CollisionDetector::CollisionDetector()
{

}

void CollisionDetector::proceed(AbstractObjectController *targetController, AbstractObjectController *object)
{
    if (targetController->getVelocityY() < 0)
    {
        QRectF targetRect = targetController->getBoundingRect();
        QRectF objectRect = object->getBoundingRect();
        if (targetRect.y() - targetRect.height() <= objectRect.y() && targetRect.y() - targetRect.height() >= objectRect.y() - objectRect.height() * 0.3)
        {
            if (targetRect.x() <= objectRect.x() + objectRect.width() && targetRect.x() + targetRect.width() >= objectRect.x())
            {
                targetController->proceedCollision(object->getControllerType(), CollisionType::BOTTOM);
            }
        }
    }
    //else if
}
