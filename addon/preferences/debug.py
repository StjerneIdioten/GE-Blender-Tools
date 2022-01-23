import bpy
from bpy.props import *


class Properties(bpy.types.PropertyGroup):

    debug_level: EnumProperty(
        name='Debug Level',
        description='What severity level to show debug info from',
        items=[
            ('ERROR', 'Error', ''),
            ('WARNING', 'Warning', ''),
            ('INFO', 'Info', ''),
            ('DEBUG', 'Debug', '')],
        default='WARNING'
    )


def draw(preferences, context, layout):
    row = layout.row()
    row.prop(preferences.debug, 'debug_level')


def register():
    bpy.utils.register_class(Properties)


def unregister():
    bpy.utils.unregister_class(Properties)
