#ifndef SLABHMOVING_H
#define SLABHMOVING_H

#include <base/sceneitem.h>

class SlabHMoving : public SceneItem
{
    Q_OBJECT
public:
    explicit SlabHMoving(QObject *parent = nullptr, double width = 100, double height = 100);
};

#endif // SLABHMOVING_H
