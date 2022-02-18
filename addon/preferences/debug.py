import logging

import bpy
from bpy.props import *

from ..utility import (addon_name, import_module, package_installed)

logger = logging.getLogger(__name__)


class Properties(bpy.types.PropertyGroup):

    def debug_level_set(self, value):
        self['debug_level'] = value
        for handler in logging.getLogger(addon_name).handlers:
            if handler.name == 'Blender Console':
                handler.setLevel(self.debug_level)

    def debug_level_get(self):
        return self.get('debug_level')

    def console_colour_set(self, value):
        handler = next((x for x in logging.getLogger(addon_name).handlers if x.name == 'Blender Console'), None)
        colour_output = False
        if value:
            try:
                import colorama
            except ModuleNotFoundError:
                pass
            else:
                class ColouredFormatter(logging.Formatter):
                    def format(self, record):
                        s = super().format(record)
                        color = colorama.Fore.WHITE
                        if record.levelname == 'DEBUG':
                            color = colorama.Fore.GREEN
                        elif record.levelname == 'INFO':
                            color = colorama.Fore.BLACK + colorama.Style.BRIGHT
                        elif record.levelname == 'WARNING':
                            color = colorama.Fore.YELLOW
                        elif record.levelname == 'ERROR':
                            color = colorama.Fore.RED
                        elif record.levelname == 'CRITICAL':
                            color = colorama.Fore.BLACK + colorama.Back.RED
                        # Colorama autoreset doesn't seem to be working as well as just adding resets at message end
                        return f"{color}{s}{colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL}"
                colorama.init(autoreset=True)
                handler.setFormatter(ColouredFormatter('%(name)s:%(funcName)s:%(levelname)s: %(message)s'))
                self['console_colour'] = True
                colour_output = True
        if not colour_output:
            handler.setFormatter(logging.Formatter('%(name)s:%(funcName)s:%(levelname)s: %(message)s'))
            self['console_colour'] = False

    def console_colour_get(self):
        return self.get('console_colour')

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

    # This needs the library "colorama" to be installed!
    console_colour: BoolProperty(
        name='Colour Code Console Output',
        description='If enabled the output to the console will be color formatted depending on logging level',
        default=False,
        get=console_colour_get,
        set=console_colour_set
    )


def draw(preferences, context, layout):
    row = layout.row()
    row.prop(preferences.debug, 'debug_level')
    row = layout.row()
    row.label(text='Clear Console On Load')
    row.prop(preferences.debug, 'clear_console_on_load', text='')
    row = layout.row()
    row.label(text='Colour Console Output')
    row.prop(preferences.debug, 'console_colour', text='')
    if not package_installed("colorama"):
        row.enabled = False


def register():
    bpy.utils.register_class(Properties)


def unregister():
    bpy.utils.unregister_class(Properties)
