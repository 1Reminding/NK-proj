#include "setvelocitymsg.h"

void SetVelocityMsg::serialize(QDataStream *s) const
{
    *s << velocity;
}

void SetVelocityMsg::deserialize(QDataStream * s)
{
    *s >> velocity;
}

void SetVelocityMsgAns::serialize(QDataStream * s) const
{;
    *s << success;
}

void SetVelocityMsgAns::deserialize(QDataStream * s)
{
    *s >> success;
}
