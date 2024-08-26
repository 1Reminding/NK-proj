#include "button.h"
#include <QDebug>

Button::Button(const char * img1, const char * img2, QGraphicsItem *)
{
    imgs[0].load(img1);
    imgs[1].load(img2);

    setPixmap(imgs[0]);

    // allow to detect mouse hover
    setAcceptHoverEvents(true);
}

void Button::mousePressEvent(QGraphicsSceneMouseEvent *)
{
    emit clicked();
    setPixmap(imgs[0]);
}

void Button::hoverEnterEvent(QGraphicsSceneHoverEvent *)
{
    setPixmap(imgs[1]);
}

void Button::hoverLeaveEvent(QGraphicsSceneHoverEvent *)
{
    setPixmap(imgs[0]);
}

Option::Option(const char * img1, const char * img2, QGraphicsItem *)
{
    isOn = false;
    imgs[0].load(img1);
    imgs[1].load(img2);
    setPixmap(imgs[0]);
}

void Option::mousePressEvent(QGraphicsSceneMouseEvent *)
{
    emit clicked();
    isOn = !isOn;
    setPixmap(imgs[isOn]);
}
