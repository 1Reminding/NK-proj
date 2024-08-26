#include "changeviewrect.h"

void ChangeViewRectMsg::serialize(QDataStream *s) const
{
    *s << viewRect;
}

void ChangeViewRectMsg::deserialize(QDataStream * s)
{
    *s >> viewRect;
}

void ChangeViewRectMsgAns::serialize(QDataStream * s) const
{;
    *s << success;
}

void ChangeViewRectMsgAns::deserialize(QDataStream * s)
{
    *s >> success;
}
