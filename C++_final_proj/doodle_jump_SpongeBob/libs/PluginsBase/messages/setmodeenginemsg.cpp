#include "setmodeenginemsg.h"

void SetModeEngineMsgAns::serialize(QDataStream *s) const
{
    *s << modeChangedSuccess << mode;
}

void SetModeEngineMsgAns::deserialize(QDataStream *s)
{
    *s >> modeChangedSuccess;
    int m;
    *s >> m;
    mode = static_cast<EngineMode>(m);
}

void SetModeEngineMsg::serialize(QDataStream *s) const
{
    *s << mode;
}

void SetModeEngineMsg::deserialize(QDataStream *s)
{
    int mode;
    *s >> mode;
    this->mode = static_cast<EngineMode>(mode);
}
