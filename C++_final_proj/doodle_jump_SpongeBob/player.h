#ifndef PLAYER_H
#define PLAYER_H

#include "doodlejump.h"
#include "props.h"
#include <QObject>
#include <QGraphicsPixmapItem>
#include <QKeyEvent>
#include <QTimer>
#include <QPixmap>
#include <QMediaPlayer>
#include <QDebug>

class DoodleJump;

class Player:public QObject, public QGraphicsPixmapItem
{
    Q_OBJECT

public:
    Player(int, int, QTimer *, DoodleJump * = NULL);

    void keyPressEvent(QKeyEvent * event);
    void keyReleaseEvent(QKeyEvent * event);
    void setVel(float = -30);
    void start();
    void stop();
    void shoot();
    void hitByMonster();
    void reset();
    int getStatus();
    int getVel();

    bool shield, isHit, inHole;
    bool left, right, space;
    Props * props;
    DoodleJump * doodlejump;

public slots:
    void move();
    void moveEvent();
    void hitByHole();

private:
    float vel;
    int status, count;
    QPixmap imgs[3][2], star_imgs[3];
    QTimer * timer;
    QGraphicsPixmapItem * mouth, * star;
    QMediaPlayer * bulletsound, * hitsound;
};

#endif // PLAYER_H
