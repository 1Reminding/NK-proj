attribute highp vec4 aVertex;
attribute highp vec2 aTexCoord;

uniform highp mat4 qt_Matrix;
uniform highp vec2 textureSize;

varying highp vec2 vTexCoord;
varying lowp vec2 vShadeCoord;

void main() {
    gl_Position = qt_Matrix * aVertex;
    vTexCoord = aVertex.xy * textureSize;
    vShadeCoord = aTexCoord;
}
