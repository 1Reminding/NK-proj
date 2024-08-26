#include "slabhmovingcontroller.h"
#include <messages/changecoordsmsg.h>
#include <enginebase.h>
#include <engineinterface.h>

SlabHMovingController::SlabHMovingController() : SlabController()
{

}

void SlabHMovingController::proceed(double dt, QRectF &visualRect)
{
    if (m_inited)
    {
        if (mode.testFlag(LEFT))
        {
            auto step = (m_internalVelocity * dt/100000) * speed;
            changeX(m_boundingRect.x() - step);
            if (left > m_boundingRect.x() - step)
            {
                mode.setFlag(VELOCITY_DOWN);
            }
            if (m_internalVelocity <= 0)
            {
                mode = VELOCITY_UP;
                mode.setFlag(RIGHT, true);
            }
        }
        else if (mode.testFlag(RIGHT))
        {
            auto step = (m_internalVelocity * dt/100000) * speed;
            changeX(m_boundingRect.x() + step);
            if (right < m_boundingRect.x() + step)
            {
                mode.setFlag(VELOCITY_DOWN);
            }

            if (m_internalVelocity <= 0)
            {
                mode = VELOCITY_UP;
                mode.setFlag(LEFT, true);
            }
        }

        if (mode.testFlag(VELOCITY_DOWN))
        {
            if (m_internalVelocity > 0)
            {
                m_internalVelocity -= dt/100000 * velocity;
            }
        }
        else if (mode.testFlag(VELOCITY_UP))
        {
            if (m_internalVelocity < velocity)
            {
                m_internalVelocity += dt/100000 * velocity;
            }
        }

        ChangeCoordsMsg msg;
        msg.x = m_boundingRect.x();
        msg.y = m_boundingRect.y();

        m_engine->getInterface()->sendFromEngine(msg, m_id);
    }
}

void SlabHMovingController::init(QPointF startPoint)
{
    changePos(startPoint);
    mode = LEFT;
    mode.setFlag(VELOCITY_UP);

    m_internalVelocity = velocity;
    m_inited = true;
}

void SlabHMovingController::setViewRect(QRectF &viewRect)
{
    m_viewRect = viewRect;
    left = 10;
    right = viewRect.width() - 110;
}
