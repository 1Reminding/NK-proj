#include "imageprovider.h"
#include <QDebug>

ImageProvider::ImageProvider(QObject *parent)
    : QObject(parent)
{

}

ImageProvider::~ImageProvider()
{
    QStringList keys = m_imagesId.keys();

    for (const auto &key : keys)
    {
        auto image = m_imagesId[key];
        m_imagesId.remove(key);
        delete image;
    }
    m_imagesPath.clear();
}

void ImageProvider::registerImage(QString id, QString path, double imageWidth, double imageHeight)
{
    if (m_imagesId.contains(id))
    {
        qDebug() << "Cannot register image: id already exist!";
        return;
    }

    auto image = new QImage(path);
    if (image->isNull())
    {
        qDebug() << "Cannot register image: undefined path!";
        delete image;
        return;
    }

    if (imageWidth != 0 && imageHeight != 0)
    {
        image->scaledToHeight(imageHeight, Qt::SmoothTransformation);
        image->scaledToWidth(imageWidth, Qt::SmoothTransformation);
    }

    m_imagesPath.insert(path, image);
    m_imagesId.insert(id, image);
}

QImage *ImageProvider::getImage(QString id)
{
    if (m_imagesId.keys().contains(id))
    {
        return m_imagesId[id];
    }
    return nullptr;
}
