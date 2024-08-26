#=============EDITED_BY_PLUGINHELPER=============#
TEMPLATE = lib
TARGET = CorePlugin
QT += qml
QT += quick
CONFIG += qt
CONFIG += plugin
CONFIG += c++17
CONFIG += qmltypes
CONFIG += shared dll

QML_IMPORT_NAME = CorePlugin
QML_IMPORT_MAJOR_VERSION = 1.0

DESTDIR = $$PWD/../../bin/plugins/$$QML_IMPORT_NAME
QMLTYPES_FILENAME = $$DESTDIR/CorePlugin.qmltypes
uri = CorePlugin

#Inputs
DEFINES += COREPLUGIN_LIBRARY
SOURCES += \
        controllers/doodlercontroller.cpp \
        controllers/slabcontroller.cpp \
        controllers/slabhmovingcontroller.cpp \
        controllers/slabvmovingcontroller.cpp \
        coreplugin_plugin.cpp \
        objects/doodler.cpp \
        objects/slab.cpp \
        objects/slabhmoving.cpp \
        objects/slabvmoving.cpp


HEADERS += \
        controllers/doodlercontroller.h \
        controllers/slabcontroller.h \
        controllers/slabhmovingcontroller.h \
        controllers/slabvmovingcontroller.h \
        coreplugin_plugin.h \
        objects/doodler.h \
        objects/slab.h \
        objects/slabhmoving.h \
        objects/slabvmoving.h


DISTFILES = \
    qmldir


#=============QMLDIR_COPY=============#
!equals(_PRO_FILE_PWD_, $$OUT_PWD) {
    copy_qmldir.target = $$DESTDIR/qmldir
    copy_qmldir.depends = $$_PRO_FILE_PWD_/qmldir
    copy_qmldir.commands = $(COPY_FILE) "$$replace(copy_qmldir.depends, /, $$QMAKE_DIR_SEP)" "$$replace(copy_qmldir.target, /, $$QMAKE_DIR_SEP)"
    QMAKE_EXTRA_TARGETS += copy_qmldir
    PRE_TARGETDEPS += $$copy_qmldir.target
}

#====================SPECIAL_PROPERTIES_STARTS====================
CONFIG(release, debug|release){
LIBS += -L$$PWD/../../../bin/libs -lpluginsbase
LIBS += -L$$PWD/../../../bin/libs -lCore
}else{
win32: LIBS += -L$$OUT_PWD/../../libs/PluginsBase/debug -lpluginsbase
else:unix: LIBS += -L$$OUT_PWD/../../libs/PluginsBase/ -lpluginsbase
win32: LIBS += -L$$OUT_PWD/../../libs/Core/debug -lCore
else:unix: LIBS += -L$$OUT_PWD/../../libs/Core/ -lCore
}
INCLUDEPATH += $$PWD/../../libs/PluginsBase
DEPENDPATH += $$PWD/../../libs/PluginsBase
INCLUDEPATH += $$PWD/../../libs/Core
DEPENDPATH += $$PWD/../../libs/Core
INCLUDEPATH += $$PWD/../../
#====================SPECIAL_PROPERTIES_ENDS====================

