#ifndef SCENEBASE_H
#define SCENEBASE_H

#include <QObject>
#include <QQmlComponent>
#include "base/sceneitem.h"
#include "factories/controllerfactory.h"
#include "factories/sceneitemfactory.h"
#include <engineinterface.h>

class PLUGINSBASE_EXPORT SceneBase : public QObject
{
    Q_OBJECT
public:
    explicit SceneBase(QObject *parent = nullptr) : QObject(parent) {}
    virtual void addFactory(const QList<SceneItemFactory*> *factories) = 0;
    virtual void setEngineInterface(EngineInterface * ei) = 0;

protected:
    SceneItem* getItem(uint32_t id);
    virtual SceneItem *addItem(QPoint pos, QString objectType, uint32_t id, QVariantMap initialParams = {}) = 0;
    virtual SceneItem *addItem(double x, double y, QString objectType, uint32_t id) = 0;
    virtual void removeItem(SceneItem* item) = 0;

protected:
    QHash<QString, SceneItemFactory*> m_factoriesHash;
};

#endif // SCENEBASE_H
