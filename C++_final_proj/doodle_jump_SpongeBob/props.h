#ifndef PROPS_H
#define PROPS_H

#include "player.h"
#include "platform.h"
#include <QObject>
#include <QGraphicsPixmapItem>
#include <QPixmap>
#include <QTimer>
#include <QMediaPlayer>

class Player;
class Platform;

class Props: public QGraphicsPixmapItem
{
public:
    Props();
    virtual ~Props(){};

    virtual void collide(Player*){};
protected:
    Player * player;
    QMediaPlayer * sound;
};

class Spring: public Props
{
public:
    Spring();
    virtual ~Spring();

    virtual void collide(Player *);

    QPixmap imgs[2];
};

class PropellerHelmet: public QObject, public Props
{
    Q_OBJECT

public:
    PropellerHelmet(Platform *, QTimer *);
    virtual ~PropellerHelmet();

    void collide(Player *) override;

    int t, count, endPos;
    bool used;
    QPixmap imgs[3];
    Platform * platform;
    QTimer * timer;

public slots:
    void fly();
    void fall();
};

#endif // PROPS_H
