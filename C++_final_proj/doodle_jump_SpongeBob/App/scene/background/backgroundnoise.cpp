#include "backgroundnoise.h"

#include <QRandomGenerator>
#include <QSGSimpleMaterialShader>
#include <QSGTexture>
#include <QQuickWindow>

#define NOISE_SIZE 32

struct NoisyMaterial
{
    ~NoisyMaterial() {
        delete texture;
    }

    QColor color;
    QSGTexture *texture;
};

class NoisyShader : public QSGSimpleMaterialShader<NoisyMaterial>
{
    QSG_DECLARE_SIMPLE_SHADER(NoisyShader, NoisyMaterial)
public:
    NoisyShader()
    {
        setShaderSourceFile(QOpenGLShader::Vertex, ":/shaders/noisy.vsh");
        setShaderSourceFile(QOpenGLShader::Fragment, ":/shaders/noisy.fsh");
    }

    QList<QByteArray> attributes() const override {  return QList<QByteArray>() << "aVertex" << "aTexCoord"; }

    void updateState(const NoisyMaterial *m, const NoisyMaterial *) override
    {
        program()->setUniformValue(id_color, m->color);
        m->texture->bind();

        QSize s = m->texture->textureSize();
        program()->setUniformValue(id_textureSize, QSizeF(1.0 / s.width(), 1.0 / s.height()));
    }

    void resolveUniforms() override {
        id_texture = program()->uniformLocation("texture");
        id_textureSize = program()->uniformLocation("textureSize");
        id_color = program()->uniformLocation("color");
        program()->setUniformValue(id_texture, 0);
    }

private:
    int id_color = -1;
    int id_texture = -1;
    int id_textureSize = -1;
};

BackgroundNoise::BackgroundNoise(QQuickWindow *window)
{
    // Make some noise...
    QImage image(NOISE_SIZE, NOISE_SIZE, QImage::Format_RGB32);
    uint *data = (uint *) image.bits();
    for (int i=0; i<NOISE_SIZE * NOISE_SIZE; ++i) {
        uint g = QRandomGenerator::global()->bounded(0xff);
        data[i] = 0xff000000 | (g << 16) | (g << 8) | g;
    }

    QSGTexture *t = window->createTextureFromImage(image);
    t->setFiltering(QSGTexture::Nearest);
    t->setHorizontalWrapMode(QSGTexture::Repeat);
    t->setVerticalWrapMode(QSGTexture::Repeat);

    QSGSimpleMaterial<NoisyMaterial> *m = NoisyShader::createMaterial();
    m->state()->texture = t;
    m->state()->color = QColor::fromRgb(249, 247, 206);
    m->setFlag(QSGMaterial::Blending);

    setMaterial(m);
    setFlag(OwnsMaterial, true);

    QSGGeometry *g = new QSGGeometry(QSGGeometry::defaultAttributes_TexturedPoint2D(), 4);
    QSGGeometry::updateTexturedRectGeometry(g, QRectF(), QRectF());
    setGeometry(g);
    setFlag(OwnsGeometry, true);
}

void BackgroundNoise::setRect(const QRectF &bounds)
{
    QSGGeometry::updateTexturedRectGeometry(geometry(), bounds, QRectF(0, 0, 1, 1));
    markDirty(QSGNode::DirtyGeometry);
}
