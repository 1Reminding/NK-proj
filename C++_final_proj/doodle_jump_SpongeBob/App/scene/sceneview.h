#ifndef SCENEVIEW_H
#define SCENEVIEW_H

#include <QQuickItem>
#include "fpsmonitor.h"
#include "keynegotiator.h"
#include "scene.h"

class SceneView : public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QRectF visualRect READ visualRect WRITE setVisualRect NOTIFY visualRectChanged)
    Q_PROPERTY(Scene* scene READ scene WRITE setScene NOTIFY sceneChanged)
    Q_PROPERTY(KeyNegotiator* keyNegotiator READ keyNegotiator WRITE setKeyNegotiator NOTIFY keyNegotiatorChanged)
    Q_PROPERTY(double currentFPS READ currentFPS WRITE setCurrentFPS NOTIFY currentFPSChanged)
public:
    SceneView();

    Scene *scene() const;
    void setScene(Scene *newScene);

    double currentFPS() const;
    void setCurrentFPS(double newCurrentFPS);

    KeyNegotiator *keyNegotiator() const;
    void setKeyNegotiator(KeyNegotiator *newKeyNegotiator);

    const QRectF &visualRect();

signals:
    void sceneChanged();
    void currentFPSChanged();
    void keyNegotiatorChanged();
    void visualRectChanged();

protected:
    QSGNode *updatePaintNode(QSGNode *, UpdatePaintNodeData *) override;
    void geometryChanged(const QRectF &newGeometry, const QRectF &oldGeometry) override;
    void mousePressEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
    void keyReleaseEvent(QKeyEvent *event) override;

private slots:
    void setVisualRect(const QRectF &newVisualRect);
    void moveToPos(double x, double y);

private:
    Scene* m_scene = nullptr;
    bool m_geometryChanged = true;
    double m_currentFPS;
    FpsMonitor m_fpsMonitor;
    KeyNegotiator *m_keyNegotiator = nullptr;
    qreal m_offset = 0;

    QRectF m_visualRect;

    enum UpdateReason{
        DEFAULT = 0x00,
        SHIFT_Y = 0x01,
        RIGHT = 0x02,
        VELOCITY_DOWN = 0x04,
        VELOCITY_UP = 0x08
    };
    Q_DECLARE_FLAGS(MovingModes, UpdateReason)
    MovingModes mode;
};

#endif // SCENEVIEW_H
