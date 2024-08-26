#ifndef SCORE_H
#define SCORE_H

#include <QString>
#include <QVector>
#include <QGraphicsScene>
#include <QGraphicsTextItem>
#include <QGraphicsPixmapItem>
#include <QGraphicsItemGroup>
#include <QKeyEvent>

class NameScore
{
public:
    NameScore(){}
    NameScore(QString);

    QString name;
    int score;
    QGraphicsTextItem * nameGraphics, * scoreGraphics, * rank;
};

class Rank: public QGraphicsItemGroup
{
public:
    Rank(){}
    ~Rank(){}

    void keyPressEvent(QKeyEvent * event);
};

class Score
{
public:
    Score();

    void read();
    void save();
    void add(QString, int);
    int findHighScore(QString);
    void addToScene(QGraphicsScene *);
    void clean(QGraphicsScene *);
    void addRankToScene(QGraphicsScene *);

private:
    QVector<NameScore> data;
    QVector<QGraphicsItem *> graphics;
    Rank * rank;
};

#endif // SCORE_H
