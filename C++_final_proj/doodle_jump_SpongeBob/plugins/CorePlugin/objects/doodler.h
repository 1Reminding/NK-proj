#ifndef DOODLER_H
#define DOODLER_H

#include <base/sceneitem.h>

class Doodler : public SceneItem
{
public:
    explicit Doodler(QObject *parent = nullptr, double width = 100, double height = 100);
};

#endif // DOODLER_H
