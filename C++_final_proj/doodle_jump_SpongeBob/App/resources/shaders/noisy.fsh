uniform sampler2D texture;
uniform lowp float qt_Opacity;
uniform lowp vec4 color;

varying highp vec2 vTexCoord;
varying lowp vec2 vShadeCoord;

#define PI 3.14159265358979323846

void main()
{
    lowp float shade = texture2D(texture, vTexCoord).r * 0.09 - length(vec2(0.5, 0.4) - vShadeCoord) * 0.3;
    lowp vec4 c = vec4(color.xyz + shade, color.w);
    gl_FragColor = c * qt_Opacity;
}
