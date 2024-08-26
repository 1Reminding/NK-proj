#include "globalconfig.h"

GlobalConfig::GlobalConfig(QObject *parent) : QObject(parent)
{

}

GlobalConfig *GlobalConfig::instance(){
    static GlobalConfig *m_instance;
    if (m_instance == nullptr) {
        m_instance = new GlobalConfig();
    }
    return m_instance;
}

QObject *GlobalConfig::qmlInstance(QQmlEngine *engine, QJSEngine *scriptEngineBase)
{
    Q_UNUSED(engine)
    Q_UNUSED(scriptEngineBase)
    return instance();
}
