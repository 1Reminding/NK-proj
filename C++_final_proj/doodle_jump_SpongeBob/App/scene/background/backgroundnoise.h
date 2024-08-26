#ifndef BACKGROUNDNOISE_H
#define BACKGROUNDNOISE_H

#include <QSGGeometryNode>
#include <QQuickWindow>

class BackgroundNoise : public QSGGeometryNode
{
public:
    BackgroundNoise(QQuickWindow *window);

    void setRect(const QRectF &bounds);
private:
    QQuickWindow *window = nullptr;
};

#endif // BACKGROUNDNOISE_H
