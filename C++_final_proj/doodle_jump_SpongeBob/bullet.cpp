#include "bullet.h"
#include "hazard.h"
#include <QGraphicsScene>
#include <QDebug>

Bullet::Bullet(QTimer * t, int h, int x, int y)
{
    limit = h;
    vx = x;
    vy = y;
    timer = t;

    setPixmap(QPixmap(":/bullet/images/bullet.png"));
    setZValue(2);


    connect(timer, SIGNAL(timeout()), this, SLOT(move()));
}

Bullet::~Bullet()
{
    if(scene() != NULL){
        scene()->removeItem(this);
    }
}

void Bullet::move()
{
    QList<QGraphicsItem*> colliding_items = collidingItems();
    for(int i = 0, n = colliding_items.size();i<n; ++i){
        Monster * monster = dynamic_cast<Monster *>(colliding_items[i]);
        if(monster){
            monster->hit();
        } else {
            continue;
        }
    }

    setPos(x() + vx, y() + vy);

    if(x() < 0 || x() > 640 || y() < limit){
        scene()->removeItem(this);
        delete this;
    }
}

