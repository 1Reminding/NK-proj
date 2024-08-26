#ifndef COLLISIONDETECTOR_H
#define COLLISIONDETECTOR_H

#include <cstdint>
class DoodlerController;
class AbstractObjectController;

enum class CollisionType : uint8_t
{
    NONE = 0x00,
    TOP = 0x01,
    BOTTOM = 0x02,
    LEFT = 0x04,
    RIGHT = 0x08
};

class CollisionDetector
{
public:
    CollisionDetector();
    void proceed(AbstractObjectController* doodlerController, AbstractObjectController *object);
};

#endif // COLLISIONDETECTOR_H
