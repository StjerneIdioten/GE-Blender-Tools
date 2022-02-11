import logging
import bpy
from bpy.props import *
from . import (dependencies, debug)
from ..utility import addon_name

logger = logging.getLogger(__package__)


class GE_TOOLS_preferences(bpy.types.AddonPreferences):
    bl_idname = addon_name

    settings: EnumProperty(
        name='Settings',
        description='Settings to display',
        items=[
            ('DEPENDENCIES', 'Dependencies', ''),
            ('DEBUG', 'Debug', '')],
        default='DEPENDENCIES'
    )

    dependencies: PointerProperty(type=dependencies.Properties)
    debug: PointerProperty(type=debug.Properties)

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        row = column.row(align=True)
        row.prop(self, 'settings', expand=True)

        box = column.box()
        globals()[self.settings.lower()].draw(self, context, box)


def register():
    logger.info("Registering Preferences")
    debug.register()
    dependencies.register()
    bpy.utils.register_class(GE_TOOLS_preferences)
    # The setter for debug_level updates the log level in the logging module, but when Blender loads the setter isn't
    # called. So we have to set the level ourselves the first time.

    for handler in logging.getLogger(addon_name).handlers:
        if handler.name == 'Blender Console':
            handler.setLevel(bpy.context.preferences.addons[addon_name].preferences.debug.debug_level)


def unregister():
    logger.info("Unregistering Preferences")
    bpy.utils.unregister_class(GE_TOOLS_preferences)
    dependencies.unregister()
    debug.unregister()

