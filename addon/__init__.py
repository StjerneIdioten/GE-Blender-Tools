# This fixes reloading, by deleting the module references and thus forcing a reload
if "bpy" in locals():
    import sys
    for module in list(sys.modules):
        if __name__ in module:
            del sys.modules[module]

import bpy

# Internal version number, which doesn't stricly have to be a three number tuple, like the bl_info one
__version__ = "0.0.0"

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


def register():
    pass


def unregister():
    pass
