#ifndef CONTROLLERFACTORY_H
#define CONTROLLERFACTORY_H

#include <QObject>
#include <pluginsbase_global.h>
#include <abstractobjectcontroller.h>

class PLUGINSBASE_EXPORT ControllerFactory : public QObject
{
    Q_OBJECT
public:
    ControllerFactory(QString type, std::function<AbstractObjectController*()> cr): m_creator(cr), m_type(type) {}
    AbstractObjectController *create(){ return m_creator();  }
    QString type() const { return m_type; }
private:
    std::function<AbstractObjectController*()> m_creator = nullptr;
    QString m_type;
};

#endif // CONTROLLERFACTORY_H
