# Internal version number, which doesn't stricly have to be a three number tuple, like the bl_info one
__version__ = "0.0.0"  # This number will be updated by CI

import importlib

# Version number should only be 0.0.0 when developing, which is the only time where we also want to reload gecore
if __version__ == "0.0.0":
    if "gecore" in locals():
        print("Reloading gecore")
        importlib.reload(gecore)

import gecore

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
    print(f"Registering {__name__}")
    pass


def unregister():
    print(f"Unregistering {__name__}")
    pass
