import bpy
from bpy.props import *
from .. import __package__ as addon_name

from . import (dependencies, debug)


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
    debug.register()
    dependencies.register()
    bpy.utils.register_class(GE_TOOLS_preferences)


def unregister():
    bpy.utils.unregister_class(GE_TOOLS_preferences)
    dependencies.unregister()
    debug.unregister()

