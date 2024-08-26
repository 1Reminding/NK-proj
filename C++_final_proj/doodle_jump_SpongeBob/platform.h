#ifndef PLATFORM_H
#define PLATFORM_H

#include "player.h"
#include "props.h"
#include <QObject>
#include <QGraphicsPixmapItem>
#include <QTimer>
#include <QMediaPlayer>
#include <QDebug>

class Player;
class Props;

class Platform: public QObject, public QGraphicsPixmapItem
{
    Q_OBJECT

public:
    Platform();
    virtual ~Platform(){};

    virtual void collide(Player*){};
    virtual void spawnProps(){};

    Props * props;

public slots:
    virtual void move(){};

protected:
    QMediaPlayer * sound;
    QTimer * timer;
    float VEL;
};

class NormalPlatform: public Platform
{
    Q_OBJECT

public:
    NormalPlatform(QTimer *);
    virtual ~NormalPlatform();

    virtual void collide(Player*);
    virtual void spawnProps();
};

class CrackedPlatform: public Platform
{
    Q_OBJECT

public:
    CrackedPlatform(QTimer *);
    virtual ~CrackedPlatform();

    virtual void collide(Player*);

public slots:
    void falling();

protected:
    QPixmap img[4];
    int count;
};

class HorizontalMovePlatform: public NormalPlatform
{
    Q_OBJECT

public:
    HorizontalMovePlatform(QTimer *);
    virtual ~HorizontalMovePlatform();

public slots: // or private?
    virtual void move();
};

class OneOffPlatform: public NormalPlatform
{
    Q_OBJECT

public:
    OneOffPlatform(QTimer *);
    virtual ~OneOffPlatform();

    virtual void collide(Player*);
};

#endif // PLATFORM_H
