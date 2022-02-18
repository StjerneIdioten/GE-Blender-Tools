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

    # TODO: Investigate if there is a way to call a method when a property is loaded
    # When a preference get's loaded it's setter is not called, meaning that the code which keeps it in sync with
    # external modules is not called. By setting it to the same value the code is called and the external module is
    # set with the proper value. There might be a better way to do this, but it works for now!
    bpy.context.preferences.addons[addon_name].preferences.debug.debug_level = \
        bpy.context.preferences.addons[addon_name].preferences.debug.debug_level
    bpy.context.preferences.addons[addon_name].preferences.debug.console_colour = \
        bpy.context.preferences.addons[addon_name].preferences.debug.console_colour


def unregister():
    logger.info("Unregistering Preferences")
    bpy.utils.unregister_class(GE_TOOLS_preferences)
    dependencies.unregister()
    debug.unregister()

