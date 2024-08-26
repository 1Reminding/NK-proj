#ifndef SLABDEFAULT_H
#define SLABDEFAULT_H

#include <base/sceneitem.h>
#include <messagenegotiator.h>
#include <QObject>
#include <messages/changecoordsmsg.h>

class Slab : public SceneItem
{
public:
    explicit Slab(QObject *parent = nullptr, double width = 100, double height = 100);
};

#endif // SLABDEFAULT_H
