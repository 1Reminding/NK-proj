#include "slabhmoving.h"

SlabHMoving::SlabHMoving(QObject *parent, double width, double height)
    : SceneItem(parent, width, height)
{
    m_type = "SlabHMoving";
}
