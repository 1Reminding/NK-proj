#ifndef SAVEPROVIDER_PLUGIN_H
#define SAVEPROVIDER_PLUGIN_H

#include <QQmlExtensionPlugin>
#include <QQmlComponent>
#include <AbstractPluginInterface.h>

class CorePlugin : public QQmlExtensionPlugin, public AbstractPluginInterface
{
    Q_OBJECT
    Q_INTERFACES(AbstractPluginInterface)
    Q_PLUGIN_METADATA(IID QQmlExtensionInterface_iid)

public:
    virtual void registerTypes(const char *uri) override;
    virtual void init(QString appPath = "") override;
private:
    QString m_appPath = "";
};

#endif // SAVEPROVIDER_PLUGIN_H
