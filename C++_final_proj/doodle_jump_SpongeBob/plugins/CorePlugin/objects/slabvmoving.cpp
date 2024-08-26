#include "slabvmoving.h"

SlabVMoving::SlabVMoving(QObject *parent, double width, double height)
    : SceneItem(parent, width, height)
{
    m_type = "SlabVMoving";
}
