#include "slabvmovingcontroller.h"
#include <messages/changecoordsmsg.h>
#include <enginebase.h>
#include <engineinterface.h>

SlabVMovingController::SlabVMovingController() : SlabController()
{

}

void SlabVMovingController::proceed(double dt, QRectF &visualRect)
{
    if (m_inited)
    {
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

        if (mode.testFlag(DOWN))
        {
            auto step = (m_internalVelocity * dt/100000) * speed;
            changeY(m_boundingRect.y() - step);
            if (bottom > m_boundingRect.y() - step)
            {
                mode = VELOCITY_DOWN;
                mode.setFlag(DOWN);
            }
            if (m_internalVelocity <= 0)
            {
                m_internalVelocity = 0;
                mode = VELOCITY_UP;
                mode.setFlag(UP, true);
            }
        }
        else if (mode.testFlag(UP))
        {
            auto step = (m_internalVelocity * dt/100000) * speed;
            changeY(m_boundingRect.y() + step);
            if (top < m_boundingRect.y() + step)
            {
                mode = VELOCITY_DOWN;
                mode.setFlag(UP);
            }

            if (m_internalVelocity <= 0)
            {
                m_internalVelocity = 0;
                mode = VELOCITY_UP;
                mode.setFlag(DOWN, true);
            }
        }

        ChangeCoordsMsg msg;
        msg.x = m_boundingRect.x();
        msg.y = m_boundingRect.y();

        m_engine->getInterface()->sendFromEngine(msg, m_id);
    }
}

void SlabVMovingController::init(QPointF startPoint)
{
    m_boundingRect = QRectF(startPoint.x(), startPoint.y(), m_boundingRect.width(), m_boundingRect.height());
    mode = UP;
    mode.setFlag(VELOCITY_UP);

    bottom = startPoint.y() - m_viewRect.height() / 5;
    top += startPoint.y();

    m_internalVelocity = velocity;
    m_inited = true;
}

bool SlabVMovingController::needInitWithRandomValue()
{
    return top == 0;
}

double SlabVMovingController::getRangeFrom()
{
    if (top == 0)
    {
        return 0;
    }
    return 0;
}

double SlabVMovingController::getRangeTo()
{
    if (bottom == 0)
    {
        return m_viewRect.height();
    }
    return 0;
}

void SlabVMovingController::setRandomValue(double value)
{
    if (top == 0)
    {
        top = value;
    }
}

void SlabVMovingController::setViewRect(QRectF &viewRect)
{
    m_viewRect = viewRect;
}
