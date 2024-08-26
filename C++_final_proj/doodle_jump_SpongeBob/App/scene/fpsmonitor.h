#ifndef FPSMONITOR_H
#define FPSMONITOR_H

#include <QVector>

class FpsMonitor
{
public:
    double recalculateFPS();
    bool isWorking();

private:
    double m_currentFPS;
    int m_cacheCount;
    QVector<qint64> m_times;
    QVector<double> m_history;
    bool m_isWorking = true;
};

#endif // FPSMONITOR_H
