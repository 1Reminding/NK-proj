#ifndef SCENE_H
#define SCENE_H

#include <QMutex>
#include <QTimer>
#include <engineinterface.h>
#include <base/scenebase.h>
#include "keynegotiator.h"

class Scene : public SceneBase
{
    Q_OBJECT
    friend class SceneView;
    Q_PROPERTY(QRectF resolution READ resolution WRITE setResolution NOTIFY resolutionChanged)
    Q_PROPERTY(QRectF viewRect READ viewRect WRITE setViewRect NOTIFY viewRectChanged)
    Q_PROPERTY(int objectsCount READ objectsCount WRITE setObjectsCount NOTIFY objectsCountChanged)
public:
    explicit Scene(QObject *parent = nullptr);
    ~Scene();
    void addFactory(const QList<SceneItemFactory *> *factories) override;
    void setEngineInterface(EngineInterface * ei) override;
    void setKeyNegotiator(KeyNegotiator* keyNegotiator);
    void startTest();
    uint32_t getDoodlerId();

    const QRectF &resolution();
    void setResolution(const QRectF &newResolution);

    const QRectF &viewRect() const;
    void setViewRect(const QRectF &newViewRect);

    void updateItems();

    int objectsCount() const;
    void setObjectsCount(int newObjectsCount);

signals:
    void resolutionChanged(QRectF);
    void viewRectChanged(QRectF);

    void objectsCountChanged();

protected:
    SceneItem *addItem(QPoint pos, QString objectName, uint32_t id, QVariantMap initialParams = {}) override;
    SceneItem *addItem(double x, double y, QString type, uint32_t id) override;
    void removeItem(SceneItem *item) override;

private:
    QMutex m_mutex;
    QTimer* m_timer = nullptr;
    EngineInterface* m_engineInterface = nullptr;
    KeyNegotiator* m_keyNegotiator = nullptr;
    QList<SceneItem*> m_sceneItems;
    QMap<uint32_t, SceneItem*> m_sceneItemsRegistry;
    uint32_t m_doodlerId = -1;
    QRectF m_resolution;
    QRectF m_viewRect;
    int m_objectsCount;
};

#endif // SCENE_H
