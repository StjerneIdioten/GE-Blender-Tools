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

# Setup logging for the addon
import logging
logger = logging.getLogger(__package__)
# The logger module isn't cleared on a reload of the addon, so we need to delete the handlers manually
logger.handlers.clear()
# Set the top level logger to always log everything, control the actual log level on the handlers
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler_formatter = logging.Formatter('%(name)s:%(funcName)s:%(levelname)s: %(message)s')
console_handler.setFormatter(console_handler_formatter)
# This is only for showing initial logging before the AddonPreferences have been loaded. After they've been set, then
# the log level is determined by the debug_level preference
if __version__ == 'develop':
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.WARNING)
console_handler.set_name('Blender Console')
logger.addHandler(console_handler)

import bpy
from . import preferences

dependencies_fulfilled = False


def register():
    logger.info(f"Registering Addon")
    preferences.register()
    if preferences.dependencies.dependencies_fulfilled():
        logger.info("Python module dependencies fulfilled")
        preferences.dependencies.register_addon()
        global dependencies_fulfilled
        dependencies_fulfilled = True
    else:
        logger.warning("Python module dependencies not fulfilled!")
    if bpy.context.preferences.addons[__package__].preferences.debug.clear_console_on_load:
        import os
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    logger.debug("This is a DEBUG message!")
    logger.info("This is an INFO message!")
    logger.warning("This is a WARNING!")
    logger.error("This is an ERROR!")
    logger.critical("This is CRITICAL!")


def unregister():
    logger.info(f"Unregistering Addon")
    if dependencies_fulfilled:
        preferences.dependencies.unregister_addon()
    preferences.unregister()
    if __version__ == "develop":
        import sys
        logger.info("Deleting addon modules from sys.modules")
        # Nuke all references to imported submodules when developing, otherwise reloading doesn't update submodules...
        for module_name in sorted(sys.modules.keys()):
            if module_name.startswith(__package__):
                logger.debug(f"Deleting module: {module_name}")
                del sys.modules[module_name]
