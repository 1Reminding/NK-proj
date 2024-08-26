#include "levelgenerator.h"
#include "engineinterface.h"
#include "qrandom.h"
#include <QDateTime>

LevelGenerator::LevelGenerator()
{
    m_randomX.setSeed(0137);
    m_randomY.setSeed(0137);
    m_randomType.setSeed(0137);
}

LevelGenerator::~LevelGenerator()
{
    m_file->close();
}

void LevelGenerator::proceed(const QRectF &visualRect)
{
    if (!m_inited)
    {
        createObject("Doodler", {424, 337});
        m_inited = true;
        for (int i = 0; i < 7; i++)
        {
            createObject("Slab", {i * 100 + 8.3 * i, 30});
        }
        m_maxY = 30;
    }
    uint64_t gap = 120;
    if (m_offset + gap < visualRect.y())
    {
        m_offset += gap;
        //! TODO generation without viewRect width (width might be around 8 platforms + 7 spices = 835
        //! if real width would be bigger -> scale all objects
        int x = m_randomX.generate()%(static_cast<int>(visualRect.width()) - 100);
        int y = 0;
        int r = 0;
        bool intersects = false;
        do
        {
            y = m_randomY.generate()%static_cast<int>(visualRect.height()) + m_offset;
            r = sqrt(pow(m_maxY - y,2) + pow(x - x, 2));
            if (r <= 490 || y <= m_maxY)
            {
                intersects = false;
                QRect createdObjectRect(x + 5, y + 5, m_boundingRectGetter("Slab").width() + 10, m_boundingRectGetter("Slab").height() + 10);
                for (const auto &obj : qAsConst(m_objects))
                {
                    QRect objRect(obj.xPos + 5, obj.yPos + 5, obj.boundingRect.width() + 10, obj.boundingRect.height() + 10);
                    if (createdObjectRect.intersects(objRect) || objRect.intersects(createdObjectRect))
                    {
                        intersects = true;
                        //y += 40;
                        qDebug() << "intersects" << createdObjectRect << QRect(obj.xPos, obj.yPos, obj.boundingRect.width(), obj.boundingRect.height());
                        break;
                    }
                }
            }
        }while ((r > 490 && y > m_maxY) || intersects);

        if (y > m_maxY)
        {
            m_maxY = y;
        }
        qDebug() << QPointF(x, y);
        //TODO different objects spawn due to percentage
        if (m_randomType.generate()%23==0)
        {
            createObject("SlabVMoving", QPointF(x, y));
        }
        else if (m_randomType.generate()%23==0)
        {
            createObject("SlabHMoving", QPointF(x, y));
        }
        else
        {
            createObject("Slab", QPointF(x, y));
        }
    }

    for (const auto &key : m_objects.keys())
    {
        if (m_objects[key].yPos < m_offset - visualRect.height() * 2)
        {
            m_deleteHandler(key);
        }
    }
}

void LevelGenerator::addGenerateableObjectsTypes(AbstractObjectController *objectTypes, ControllerType controllerType)
{
    switch(controllerType)
    {
    case ControllerType::SLAB:
    {
        m_creatableSlabObjects.append(objectTypes);
        break;
    }
    case ControllerType::MONSTER:
    {
        m_creatableMonsterObjects.append(objectTypes);
        break;
    }
    case ControllerType::DOODLER:
    {
        qDebug() << "Cannot add Doodler to levelGenerator";
        return;
    }
    case ControllerType::GHOST:
    {
        qDebug() << "Cannot add GHOST to levelGenerator";
        return;
    }
    case ControllerType::BULLET:
    {
        qDebug() << "Cannot add BULLET to levelGenerator";
        return;
    }
    case ControllerType::POWERUP:
    {
        m_creatablePowerUPObjects.append(objectTypes);
        break;
    }
    }
}

void LevelGenerator::setCreateHandler(const std::function<uint32_t (QString, QPointF)> &createHandler)
{
    m_createHandler = createHandler;
}

void LevelGenerator::setDeleteHandler(const std::function<bool(uint32_t)> &deleteHandler)
{
    m_deleteHandler = deleteHandler;
}

void LevelGenerator::setBoundingRectGetter(const std::function<QRectF (QString)> &boundingRectGetter)
{
    m_boundingRectGetter = boundingRectGetter;
}

void LevelGenerator::createObject(QString type, QPointF pos)
{
    uint32_t id = m_createHandler(type, pos);
    if (m_inited)
    {
        m_objects[id] = {pos.x(), pos.y(), m_boundingRectGetter(type)};
    }
}
