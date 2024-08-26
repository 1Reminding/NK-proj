#ifndef SLABVMOVINGCONTROLLER_H
#define SLABVMOVINGCONTROLLER_H

#include "slabcontroller.h"

class SlabVMovingController : public SlabController
{
public:
    SlabVMovingController();
    void proceed(double dt, QRectF & visualRect) override;
    void init(QPointF startPoint) override;

    bool needInitWithRandomValue() override;
    double getRangeFrom() override;
    double getRangeTo() override;
    void setRandomValue(double value) override;
    void setViewRect(QRectF &viewRect) override;

private:
    bool m_inited = false;
    qreal top = 0;
    qreal bottom = 0;
    qreal speed = 1.5;
    qreal velocity = 45;
    qreal m_internalVelocity = 0;
    enum MovingMode{
        NONE = 0x00,
        UP = 0x01,
        DOWN = 0x02,
        VELOCITY_DOWN = 0x04,
        VELOCITY_UP = 0x08
    };
    Q_DECLARE_FLAGS(MovingModes, MovingMode)
    MovingModes mode;

    QRectF m_viewRect;
};

#endif // SLABVMOVINGCONTROLLER_H
