#include "slab.h"

Slab::Slab(QObject *parent, double width, double height)
    : SceneItem(parent, width, height)
{
    m_type = "Slab";
}


