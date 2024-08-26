#ifndef BUTTON_H
#define BUTTON_H

#include <QGraphicsPixmapItem>
#include <QGraphicsSceneMouseEvent>
#include <QGraphicsTextItem>
#include <QPixmap>

class Button: public QObject, public QGraphicsPixmapItem
{
    Q_OBJECT;
public:
    Button(const char * = "", const char * = "", QGraphicsItem * parent = NULL);

    void mousePressEvent(QGraphicsSceneMouseEvent *);
    void hoverEnterEvent(QGraphicsSceneHoverEvent *);
    void hoverLeaveEvent(QGraphicsSceneHoverEvent *);

    QPixmap imgs[2];

signals:
    void clicked();
};

class Option: public QObject, public QGraphicsPixmapItem
{
    Q_OBJECT;
public:
    Option(const char * = "", const char * = "", QGraphicsItem * parent = NULL);

    void mousePressEvent(QGraphicsSceneMouseEvent *);

    QPixmap imgs[2];

signals:
    void clicked();

private:
    bool isOn;
};

#endif // BUTTON_H
