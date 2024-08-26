#include "sceneview.h"
#include "scene/background/backgroundnoise.h"
#include <cmath>
#include <scene/background/backgroundgrid.h>
#include <QPainter>
#include <QSGSimpleTextureNode>
#include <QSGTransformNode>

class BackgroundNode : public QSGNode
{
public:
    BackgroundGrid *grid = nullptr;
    BackgroundNoise *background = nullptr;
};

class ChildNode : public QSGGeometryNode
{
public:
    QSGSimpleTextureNode *texture = nullptr;
    uint32_t id;
};

class MainNode : public QSGNode
{
public:
    //!subchilds
    QMap<uint32_t, ChildNode*> childs;
    //! childs
    BackgroundNode *backgroundNode = nullptr;
    QSGTransformNode *shiftYTransformNode = nullptr;

};

SceneView::SceneView()
{
    setFlag(ItemHasContents, true);
    setFlag(QQuickItem::ItemAcceptsInputMethod, true);
    setFlag(QQuickItem::ItemIsFocusScope, true);
    setAcceptedMouseButtons(Qt::LeftButton);
    setClip(true);
    setSmooth(true);
    setAntialiasing(true);
    setAcceptHoverEvents(true);
    forceActiveFocus();
}

QSGNode* SceneView::updatePaintNode(QSGNode *node, UpdatePaintNodeData *)
{
    MainNode* mainNode = static_cast<MainNode*>(node);

    QRectF rect = boundingRect();

    if (!mainNode)
    {
        mainNode = new MainNode();
        mainNode->shiftYTransformNode = new QSGTransformNode();
        mainNode->backgroundNode = new BackgroundNode();

        mainNode->appendChildNode(mainNode->backgroundNode);
        mainNode->appendChildNode(mainNode->shiftYTransformNode);

        mainNode->backgroundNode->grid = new BackgroundGrid();
        mainNode->backgroundNode->background = new BackgroundNoise(window());

        mainNode->backgroundNode->appendChildNode(mainNode->backgroundNode->background);
        mainNode->backgroundNode->appendChildNode(mainNode->backgroundNode->grid);
        m_geometryChanged = true;

        m_offset = rect.height();
        mainNode->shiftYTransformNode->setMatrix(QTransform().translate(0, m_offset));
        mainNode->shiftYTransformNode->markDirty(QSGNode::DirtyMatrix);
    }

    if (rect.isEmpty())
    {
        delete mainNode;
        return nullptr;
    }

    if (m_geometryChanged)
    {
        mainNode->backgroundNode->background->setRect(rect);
        mainNode->backgroundNode->grid->setRect(rect);
    }

    for (auto* item : qAsConst(m_scene->m_sceneItems))
    {
        if (item->removingState() == SceneItem::RemovingState::PREPARE && mainNode->childs.contains(item->id()))
        {
            mainNode->removeChildNode(mainNode->childs[item->id()]);
            mainNode->childs.remove(item->id());
            item->setRemovingState(SceneItem::RemovingState::READY);
        }
        else if (item->needUpdate())
        {
            auto child = mainNode->childs[item->id()];
            if (!child)
            {
                child = new ChildNode();
                child->id = item->id();

                child->setGeometry(new QSGGeometry(QSGGeometry::defaultAttributes_Point2D(), 4));
                child->geometry()->setDrawingMode(QSGGeometry::DrawTriangleFan);

                auto m = new QSGFlatColorMaterial();
                m->setColor("green");
                child->setMaterial(m);
                child->setFlags(QSGNode::OwnsGeometry | QSGNode::OwnsMaterial);

                //child->texture = new QSGSimpleTextureNode();
                //child->texture->setOwnsTexture(true);
                //child->appendChildNode(child->texture);
                //QImage img(item->width(), item->height(), QImage::Format_ARGB32);
                //img.fill(Qt::red);
                //auto t = window()->createTextureFromImage(img, QQuickWindow::TextureHasAlphaChannel);
                //child->texture->setTexture(t);
                //child->texture->setRect(QRectF(item->x(), -item->y(), img.width(), img.height()));
                mainNode->shiftYTransformNode->appendChildNode(child);
                mainNode->childs[item->id()] = child;
            }

            if (item->needUpdate())
            {
                auto g = child->geometry();
                g->vertexDataAsPoint2D()[0].set(item->x(), -item->y());
                g->vertexDataAsPoint2D()[1].set(item->x() + item->width(), -item->y());
                g->vertexDataAsPoint2D()[2].set(item->x() + item->width(), -(item->y() - item->height()));
                g->vertexDataAsPoint2D()[3].set(item->x(), -(item->y() - item->height()));
                //child->texture->setRect(QRectF(item->x(), -item->y(), item->width(), item->height()));
                child->setGeometry(g);
                child->markDirty(QSGNode::DirtyGeometry | QSGNode::DirtyMaterial);
                item->setNeedUpdate(false);
            }
        }

        if (item->id() == m_scene->getDoodlerId())
        {
            double limit = m_visualRect.y() - m_visualRect.height() * 0.3;
            double currDoodleY = item->boundingRect().y();
            if (limit <= currDoodleY)
            {
                m_offset += std::floor(currDoodleY - limit);
            }
            //qDebug() << limit << currDoodleY << m_visualRect << m_visualRect.y() - (limit - currDoodleY);
        }

    }

    if (m_fpsMonitor.isWorking())
    {
        setCurrentFPS(m_fpsMonitor.recalculateFPS());
    }

    m_geometryChanged = false;
    setVisualRect({rect.x(), m_offset, rect.width(), rect.height()});
    mainNode->shiftYTransformNode->setMatrix(QTransform().translate(0, m_visualRect.y()));
    mainNode->shiftYTransformNode->markDirty(QSGNode::DirtyMatrix);

    update();
    return mainNode;
}

void SceneView::geometryChanged(const QRectF &newGeometry, const QRectF &oldGeometry)
{
    m_geometryChanged = true;
    update();
    QQuickItem::geometryChanged(newGeometry, oldGeometry);
}

void SceneView::mousePressEvent(QMouseEvent *event)
{
    forceActiveFocus();
    if (event->button() == Qt::MouseButton::LeftButton)
    {
        auto pos = event->localPos();
        m_keyNegotiator->pressFire(pos);
        event->setAccepted(true);
    }
    QQuickItem::mousePressEvent(event);
}

void SceneView::keyPressEvent(QKeyEvent *event)
{
    if (event->isAutoRepeat()) return;
    if (event->key() == Qt::Key_A || event->key() == Qt::Key_Left)
    {
        qDebug() << "Left";
        m_keyNegotiator->pressLeft();
        event->ignore();
    }
    else if (event->key() == Qt::Key_D || event->key() == Qt::Key_Right)
    {
        qDebug() << "Right";
        m_keyNegotiator->pressRight();
        event->ignore();
    }
    else if (event->key() == Qt::Key_Escape || event->key() == Qt::Key_P)
    {
        m_keyNegotiator->pressPause();
    }
    QQuickItem::keyPressEvent(event);
}

void SceneView::keyReleaseEvent(QKeyEvent *event)
{
    if (event->isAutoRepeat()) return;
    if (event->key() == Qt::Key_A || event->key() == Qt::Key_Left)
    {
        qDebug() << "Left stop";
        m_keyNegotiator->releaseLeft();
    }
    else if (event->key() == Qt::Key_D || event->key() == Qt::Key_Right)
    {
        qDebug() << "Right stop";
        m_keyNegotiator->releaseRight();
    }
    else if (event->key() == Qt::Key_Escape || event->key() == Qt::Key_P)
    {
        m_keyNegotiator->releasePause();
    }
    QQuickItem::keyReleaseEvent(event);
}

Scene *SceneView::scene() const
{
    return m_scene;
}

void SceneView::setScene(Scene *newScene)
{
    if (m_scene == newScene)
        return;
    m_scene = newScene;
    emit sceneChanged();
}

double SceneView::currentFPS() const
{
    return m_currentFPS;
}

void SceneView::setCurrentFPS(double newCurrentFPS)
{
    if (qFuzzyCompare(m_currentFPS, newCurrentFPS))
        return;
    m_currentFPS = newCurrentFPS;
    emit currentFPSChanged();
}

KeyNegotiator *SceneView::keyNegotiator() const
{
    return m_keyNegotiator;
}

void SceneView::setKeyNegotiator(KeyNegotiator *newKeyNegotiator)
{
    if (m_keyNegotiator == newKeyNegotiator)
        return;
    m_keyNegotiator = newKeyNegotiator;
    emit keyNegotiatorChanged();
}

const QRectF &SceneView::visualRect()
{
    return m_visualRect;
}

void SceneView::setVisualRect(const QRectF &newVisualRect)
{
    if (m_visualRect == newVisualRect)
        return;
    m_visualRect = newVisualRect;
    m_scene->setViewRect(m_visualRect);
    emit visualRectChanged();
}

void SceneView::moveToPos(double x, double y)
{
    setVisualRect({x, y, m_visualRect.width(), m_visualRect.height()});
    update();
}
