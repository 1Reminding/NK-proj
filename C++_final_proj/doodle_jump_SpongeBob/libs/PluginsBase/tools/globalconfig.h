#ifndef GLOBALCONFIG_H
#define GLOBALCONFIG_H

#include <QObject>
#include <qqml.h>

class GlobalConfig : public QObject
{
    Q_OBJECT
public:
    explicit GlobalConfig(QObject *parent = nullptr);
    static GlobalConfig *instance();
    static QObject *qmlInstance(QQmlEngine *engine, QJSEngine *scriptEngineBase);
    static inline const int GlobalStyleQMLRegistration = qmlRegisterSingletonType<GlobalConfig>("PluginsBase", 1, 0, "GlobalConfig", &GlobalConfig::qmlInstance);

    enum SettingsWindowMode{
        NOMOD = 0x00,
        SCENE = 0x01,
        WINDOW = 0x02
    };

signals:

};

#endif // GLOBALSTYLE_H
