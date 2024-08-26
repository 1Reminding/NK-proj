#ifndef KEYNEGOTIATOR_H
#define KEYNEGOTIATOR_H

#include <QObject>
#include <QPointF>

class KeyNegotiator : public QObject
{
    Q_OBJECT
public:
    explicit KeyNegotiator(QObject *parent = nullptr);

public slots:
    void pressLeft();
    void pressRight();
    void pressPause();
    void pressFire(QPointF pos);

    void releaseLeft();
    void releaseRight();
    void releasePause();
signals:
    void leftPressed();
    void rightPressed();
    void pausePressed();
    void firePressed(QPointF pos);

    void leftReleased();
    void rightReleased();
    void pauseReleased();
};

#endif // KEYNEGOTIATOR_H
