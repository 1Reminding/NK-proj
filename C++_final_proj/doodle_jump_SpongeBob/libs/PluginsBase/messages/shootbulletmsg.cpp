#include "shootbulletmsg.h"

void ShootBulletMsg::serialize(QDataStream *s) const
{
    *s << x << y;
}

void ShootBulletMsg::deserialize(QDataStream * s)
{
    *s >> x >> y;
}

void ShootBulletMsgAns::serialize(QDataStream * s) const
{;
    *s << success;
}

void ShootBulletMsgAns::deserialize(QDataStream * s)
{
    *s >> success;
}
