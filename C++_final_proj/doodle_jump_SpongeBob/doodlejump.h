#ifndef DOODLEJUMP_H
#define DOODLEJUMP_H

#include "mainwindow.h"
#include "player.h"
#include "platform.h"
#include "button.h"
#include "hazard.h"
#include "score.h"
#include <QObject>
#include <QTimer>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QGraphicsPixmapItem>
#include <QGraphicsTextItem>
#include <QVector>
#include <QString>

class Player;
class Platform;
class Hazard;
class Score;

class DoodleJump:public QObject
{
    Q_OBJECT;

    friend class MainWindow; // not sure it is necessary

public:
    DoodleJump(QGraphicsView * = NULL);

    void spawnPlaform(int);
    void cleanPlatform();
    void end();
    void cleanScene();
    bool getTurnOnSound();

    bool isEnd;
    QTimer * timer;

public slots:
    void play();
    void pause();
    void resume();
    void menu();
    void option();
    void scores();
    void switchSound();
    void setBackGround();

private:
    bool isOverlapping(QGraphicsPixmapItem *);
    bool possiability(float);

    int score, highestScore, last;
    bool turnOnSound;
    QString name;
    Player * player;
    Score * scoreData;
    QGraphicsScene * scene;
    QGraphicsView * view;
    QGraphicsPixmapItem background[2];
    QVector<Platform *> platforms;
    QVector<Hazard *> hazards;
    QMediaPlayer * endSound;
    QGraphicsPixmapItem * welcomeBackground, * pauseBackground, * scoreBackground, * optionBar, * toolBar, * endBar, * gameOver, * tapToChange, * soundText;
    QGraphicsTextItem * scoreText, * endText, * nameText;
    Button * playButton, * pauseButton, * resumeButton, * playAgainButton, * menuButton, *optionButton, *scoreButton;
    Option * OnOffButton, * localButton;
};

#endif // DOODLEJUMP_H
