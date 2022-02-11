import logging

import bpy
from bpy.props import *

from ..utility import addon_name

logger = logging.getLogger(__name__)


class Properties(bpy.types.PropertyGroup):

    def debug_level_set(self, value):
        self['debug_level'] = value
        for handler in logging.getLogger(addon_name).handlers:
            if handler.name == 'Blender Console':
                handler.setLevel(self.debug_level)

    def debug_level_get(self):
        return self.get('debug_level')

    debug_level: EnumProperty(
        name='Debug Level',
        description='What severity level to show debug info from',
        items=[
            ('ERROR', 'Error', ''),
            ('WARNING', 'Warning', ''),
            ('INFO', 'Info', ''),
            ('DEBUG', 'Debug', '')],
        set=debug_level_set,
        get=debug_level_get,
        default='WARNING'
    )

    clear_console_on_load: BoolProperty(
        name='Clear Console On Load',
        description='Whether to clear the console after the addon has loaded, very useful when developing and '
                    'reloading all the time. Keeps the log free of the registration debug messages as well',
        default=False
    )


def draw(preferences, context, layout):
    row = layout.row()
    row.prop(preferences.debug, 'debug_level')
    row = layout.row()
    row.label(text='Clear Console On Load')
    row.prop(preferences.debug, 'clear_console_on_load', text='')


def register():
    bpy.utils.register_class(Properties)


def unregister():
    bpy.utils.unregister_class(Properties)
