#ifndef KGRIDNode_H
#define KGRIDNode_H

#include <QtQuick/QSGGeometryNode>
#include <QtQuick/QSGFlatColorMaterial>

class BackgroundGrid : public QSGGeometryNode
{
public:
    BackgroundGrid();

    void setRect(const QRectF &rect);

private:
    QSGFlatColorMaterial m_material;
    QSGGeometry m_geometry;
};

#endif // BackgroundGrid_H
