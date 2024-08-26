#ifndef SCENEITEMFACTORY_H
#define SCENEITEMFACTORY_H

#include <QObject>
#include <QVariantMap>
#include <pluginsbase_global.h>
#include "base/sceneitem.h"

class PLUGINSBASE_EXPORT SceneItemFactory : public QObject
{
    Q_OBJECT
public:
    SceneItemFactory(QString type, std::function<SceneItem*()> creator) : m_creator(creator), m_type(type) {}
    QString type() { return m_type;}
    SceneItem *create(QVariantMap params){ auto item = m_creator(); setParams(item, params); return item; }
private:
    void setParams(QObject *obj, QVariantMap params)
    {
        QMapIterator<QString, QVariant> iter(params);
        QMap<QString, int> properties;

        for (int i = 0, size = obj->metaObject()->propertyCount(); i < size; i++)
        {
            auto p = obj->metaObject()->property(i);
            properties.insert(p.name(), i);
        }

        while (iter.hasNext())
        {
            auto p = iter.next();
            if (properties.contains(p.key()))
            {
                obj->metaObject()->property(properties[p.key()]).write(obj, p.value());
            }
        }
    }

private:
    std::function<SceneItem*()> m_creator = nullptr;
    QString m_type;
};

#endif // SCENEITEMFACTORY_H
