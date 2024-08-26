#include "changecoordsmsg.h"
#include <QDataStream>

void ChangeCoordsMsg::serialize(QDataStream *s) const
{
    *s << x << y;
}

void ChangeCoordsMsg::deserialize(QDataStream * s)
{
    *s >> x >> y;
}

void ChangeCoordsMsgAns::serialize(QDataStream * s) const
{;
    *s << success;
}

void ChangeCoordsMsgAns::deserialize(QDataStream * s)
{
    *s >> success;
}
