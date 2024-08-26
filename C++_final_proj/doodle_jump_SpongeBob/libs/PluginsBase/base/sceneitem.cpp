#include "sceneitem.h"

SceneItem::SceneItem(QObject *parent, double width, double height)
    : QObject(parent),
      m_width(width),
      m_height(height)
{

}

QString SceneItem::type() const
{
    return m_type;
}

void SceneItem::setType(const QString &newType)
{
    m_type = newType;
}

uint32_t SceneItem::id() const
{
    return m_id;
}

double SceneItem::x() const
{
    return m_x;
}

double SceneItem::y() const
{
    return m_y;
}

double SceneItem::width() const
{
    return m_width;
}

double SceneItem::height() const
{
    return m_height;
}

const QString &SceneItem::imagePath() const
{
    return m_imagePath;
}

void SceneItem::setRemovingState(RemovingState newState)
{
    m_removingState = newState;
}

QRectF SceneItem::boundingRect() const
{
    return QRectF(m_x, m_y, m_width, m_height);
}

SceneItem::RemovingState SceneItem::removingState()
{
    return m_removingState;
}

void SceneItem::setId(uint32_t newId)
{
    if (m_id == newId)
        return;
    m_id = newId;
    emit idChanged();
}

void SceneItem::setX(double newX)
{
    if (qFuzzyCompare(m_x, newX))
        return;
    m_x = newX;
    setNeedUpdate(true);
    emit xChanged();
}

void SceneItem::setY(double newY)
{
    if (qFuzzyCompare(m_y, newY))
        return;
    m_y = newY;
    setNeedUpdate(true);
    emit yChanged();
}

bool SceneItem::movable() const
{
    return m_movable;
}

void SceneItem::setMovable(bool newMovable)
{
    if (m_movable == newMovable)
        return;
    m_movable = newMovable;
    emit movableChanged();
}

bool SceneItem::needUpdate() const
{
    return m_needUpdate;
}

void SceneItem::setNeedUpdate(bool newNeedUpdate)
{
    if (m_needUpdate == newNeedUpdate)
        return;
    m_needUpdate = newNeedUpdate;
    emit needUpdateChanged();
}

void SceneItem::setWidth(double newWidth)
{
    if (qFuzzyCompare(m_width, newWidth))
        return;
    m_width = newWidth;
    emit widthChanged();
}

void SceneItem::setHeight(double newHeight)
{
    if (qFuzzyCompare(m_height, newHeight))
        return;
    m_height = newHeight;
    emit heightChanged();
}
