#ifndef RANDOMGENERATOR_H
#define RANDOMGENERATOR_H

#include "core_global.h"
#include <QString>

class CORE_EXPORT RandomGenerator
{
public:
    void setSeed(uint32_t seed) { m_seed = QString::number(seed); }
    quint32 generate()
    {
        m_seed = QString::number(std::hash<std::string>{}(m_seed.toStdString()));
        return m_seed.midRef(0,m_seed.length()/2).toUInt();
    }
private:
    QString m_seed;
};

#endif // RANDOMGENERATOR_H
