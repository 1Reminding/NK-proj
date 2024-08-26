#ifndef SLABVMOVING_H
#define SLABVMOVING_H

#include <base/sceneitem.h>

class SlabVMoving : public SceneItem
{
public:
    explicit SlabVMoving(QObject *parent = nullptr, double width = 100, double height = 100);
};

#endif // SLABVMOVING_H
