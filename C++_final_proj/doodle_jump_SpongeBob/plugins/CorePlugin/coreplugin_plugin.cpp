#include "coreplugin_plugin.h"
#include <QDir>
#include <qqml.h>

#include "controllers/doodlercontroller.h"
#include "controllers/slabcontroller.h"
#include "objects/slab.h"
#include "objects/doodler.h"
#include <controllers/slabhmovingcontroller.h>
#include <controllers/slabvmovingcontroller.h>
#include <objects/slabhmoving.h>
#include <objects/slabvmoving.h>


void CorePlugin::registerTypes(const char *)
{
    // @uri SaveProvider
}

void CorePlugin::init(QString appPath)
{
    m_appPath = appPath;

    createControllerFactory<SlabController>();
    createObjectFactory<Slab>();

    createControllerFactory<SlabVMovingController>();
    createObjectFactory<SlabVMoving>();

    createControllerFactory<SlabHMovingController>();
    createObjectFactory<SlabHMoving>();

    createCollideControllerFactory<DoodlerController>();
    createObjectFactory<Doodler>();

    m_resources.insert("SlabDefault", "Slabdefault");
}
