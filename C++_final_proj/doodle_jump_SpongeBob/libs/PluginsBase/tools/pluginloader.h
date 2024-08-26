#ifndef PLUGINLOADER_H
#define PLUGINLOADER_H

#include <QDir>
#include <QObject>
#include <QPluginLoader>
#include <QString>
#include <QUrl>
#include <pluginsbase_global.h>

class AbstractPluginInterface;

class PLUGINSBASE_EXPORT PluginLoader : public QObject
{
    Q_OBJECT
public:
    PluginLoader(const QString &appPath, QObject *parent = nullptr);
    ~PluginLoader();
    AbstractPluginInterface* load(QString libname);
    bool unload(const QString &name);
private:
    QString m_appPath;
    QHash<QString, QPluginLoader*> m_instancesRegistry;
};


#endif // PLUGINLOADER_H
