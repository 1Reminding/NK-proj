#ifndef BULLET_H
#define BULLET_H

#include <QObject>
#include <QGraphicsPixmapItem>
#include <QTimer>

class Bullet:public QObject, public QGraphicsPixmapItem
{
    Q_OBJECT
public:
    Bullet(QTimer *, int, int = 0, int = -60);
    ~Bullet();

public slots:
    void move();

private:
    int vx, vy, limit;
    QTimer * timer;

};

#endif // BULLET_H
