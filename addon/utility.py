import os
import ctypes
import importlib
from importlib import metadata
import logging

logger = logging.getLogger(__name__)

addon_name = __package__.partition('.')[0]


def is_admin() -> bool:
    """Checks if user has administrative rights, regardless of OS used"""
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1


def compare_versions(version1, version2):
    return True if version1 == version2 or version1 == '0.0.0' else False


def package_installed(package_name):
    installed = False
    # Try if module version can be found through dist-info or egg-info
    try:
        if metadata.version(package_name):
            installed = True
    except metadata.PackageNotFoundError:
        pass
    return installed


def import_module(module_name, global_name=None):
    if global_name is None:
        global_name = module_name
    logger.debug(f"Importing module: {global_name}")
    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        globals()[global_name] = importlib.import_module(module_name)
