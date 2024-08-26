QT += core
QT += gui
QT += quickwidgets
QT += quick
QT += concurrent
QT += gui-private
CONFIG += c++17

SOURCES += \
    appcore.cpp \
    engine.cpp \
    imageprovider.cpp \
    keynegotiator.cpp \
    main.cpp \
    scene/background/backgroundgrid.cpp \
    scene/background/backgroundnoise.cpp \
    scene/fpsmonitor.cpp \
    scene/scene.cpp \
    scene/sceneview.cpp

RESOURCES += resources/qml.qrc

QML_IMPORT_PATH =

HEADERS += \
    appcore.h \
    engine.h \
    imageprovider.h \
    keynegotiator.h \
    scene/background/backgroundgrid.h \
    scene/background/backgroundnoise.h \
    scene/fpsmonitor.h \
    scene/scene.h \
    scene/sceneview.h

CONFIG(release, debug|release){
DEFINES += QT_NO_DEBUG_OUTPUT
LIBS += -L$$PWD/../../bin/libs -lcore
LIBS += -L$$PWD/../../bin/libs -lpluginsbase
} else {
win32: LIBS += -L$$OUT_PWD/../libs/PluginsBase/debug -lpluginsbase
else:unix: LIBS += -L$$OUT_PWD/../libs/PluginsBase/ -lpluginsbase

win32: LIBS += -L$$OUT_PWD/../libs/Core/debug -lCore
else:unix: LIBS += -L$$OUT_PWD/../libs/Core/ -lCore
}

INCLUDEPATH += $$PWD/../libs/PluginsBase
DEPENDPATH += $$PWD/../libs/PluginsBase

INCLUDEPATH += $$PWD/../libs/Core
DEPENDPATH += $$PWD/../libs/Core
