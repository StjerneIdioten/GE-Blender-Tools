# Internal version number, which doesn't strictly have to be a three number tuple, like the bl_info one
__version__ = "develop"  # This number will be updated by CI

bl_info = {
    "name": "Giants Engine Tools",
    "author": "Stjerneidioten",
    "description": "A set of tools for developing mods for Giants Engine based games such as Farming Simulator",
    "version": (0, 0, 0),  # Get's updated by CI
    "blender": (3, 0, 0),
    "location": "",  # The addon adds multiple things in multiple places
    "warning": "This is still in early development!",
    "support": "COMMUNITY",
    "category": "Game Engine",
    "tracker_url": "https://github.com/StjerneIdioten/GE-Blender-Tools/issues",
    "doc_url": "https://github.com/StjerneIdioten/GE-Blender-Tools"
}

import sys
from . import addon_preferences
from . import dependency_handling


def register():
    print(f"Registering {__package__}")
    addon_preferences.register()
    dependency_handling.register()
    if dependency_handling.dependencies_fulfilled:
        print(f"Dependencies fulfilled for {__package__}")
        # Register other classes
        #for cls in classes:
        #    bpy.utils.register_class(cls)


def unregister():
    print(f"Unregistering {__package__}")
    if dependency_handling.dependencies_fulfilled:
        print(f"Dependencies fulfilled for {__package__}")
        #for cls in classes:
        #    bpy.utils.unregister_class(cls)
    dependency_handling.unregister()
    addon_preferences.unregister()
    if __version__ == "develop":
        # Nuke all references to imported submodules when developing, otherwise reloading doesn't update submodules...
        for module_name in sorted(sys.modules.keys()):
            if module_name.startswith(__package__):
                del sys.modules[module_name]