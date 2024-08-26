#include "doodler.h"

Doodler::Doodler(QObject *parent, double width, double height)
    : SceneItem(parent, width, height)
{
    m_type = "Doodler";
    m_movable = true;
}
