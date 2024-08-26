#include "fpsmonitor.h"
#include <QDateTime>

double FpsMonitor::recalculateFPS()
{
    qint64 currentTime = QDateTime::currentDateTime().toMSecsSinceEpoch();
    m_times.push_back(currentTime);

    while (m_times[0] < currentTime - 1000)
    {
       m_times.pop_front();
    }

    int currentCount = m_times.length();
    m_currentFPS = (currentCount + m_cacheCount) / 2;

    if (currentCount != m_cacheCount)
    {
        m_history.push_back(m_currentFPS);
        while(m_history.count() > 200)
        {
            m_history.pop_front();
        }
    }

    m_cacheCount = currentCount;
    return m_currentFPS;
}

bool FpsMonitor::isWorking()
{
    return m_isWorking;
}
