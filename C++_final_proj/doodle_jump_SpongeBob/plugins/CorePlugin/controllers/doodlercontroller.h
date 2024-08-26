#ifndef DOODLERCONTROLLER_H
#define DOODLERCONTROLLER_H

#include "abstractobjectcontroller.h"
#include <messages/setvelocitymsg.h>

class DoodlerController : public AbstractObjectController
{
public:
    DoodlerController();

    virtual void proceedCollision(ControllerType controllerType, CollisionType collisionType) override;
    virtual void proceed(double dt, QRectF &visualRect) override;
    virtual void init(QPointF pos) override;

private:
    SetVelocityMsgAns proceedSetVelocity(SetVelocityMsg msg);
    double getVelocityByHeight(double height, double delta = 0);

private:
    double m_delta = 0.000009;
    double m_velocityMult = 1;
    bool m_moving = false;
    double m_jumpHeight = 505;
    double m_easingProgress = 0;
    double m_yBeforeJump = 0;
};

#endif // DOODLERCONTROLLER_H
