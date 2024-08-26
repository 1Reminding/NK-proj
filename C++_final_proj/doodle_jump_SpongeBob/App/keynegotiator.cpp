#include "keynegotiator.h"

KeyNegotiator::KeyNegotiator(QObject *parent)
    : QObject(parent)
{

}

void KeyNegotiator::pressLeft()
{
    emit leftPressed();
}

void KeyNegotiator::pressRight()
{
    emit rightPressed();
}

void KeyNegotiator::pressPause()
{
    emit pausePressed();
}

void KeyNegotiator::pressFire(QPointF pos)
{
    emit firePressed(pos);
}

void KeyNegotiator::releaseLeft()
{
    emit leftReleased();
}

void KeyNegotiator::releaseRight()
{
    emit rightReleased();
}

void KeyNegotiator::releasePause()
{
    emit pauseReleased();
}
