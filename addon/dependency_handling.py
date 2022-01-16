import bpy
import os
import ctypes
import sys
import subprocess
import importlib
from importlib import metadata
from collections import namedtuple
from bpy.props import (IntProperty, BoolProperty)

Dependency = namedtuple('Dependency', ['module', 'package', 'name', 'version'])
dependencies = (Dependency(module='gecore', package='ge-core', name=None, version='0.1.0'),)


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1


def dependency_installed_version(dependency):
    version = "None"
    # Try if module version can be found through dist-info or egg-info
    try:
        version = metadata.version(dependency.package)
    except metadata.PackageNotFoundError:
        pass

    return version


def compare_versions(version1, version2):
    return True if version1 == version2 or version1 == '0.0.0' else False


def import_module(module_name, global_name=None):
    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        globals()[global_name] = importlib.import_module(module_name)


def install_dependency(dependency, upgrade=False):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", f"{dependency.package}=={dependency.version}"],
                   check=True, env=environ_copy)


def dependencies_fulfilled():
    for dependency in dependencies:
        installed_version = dependency_installed_version(dependency)
        if not compare_versions(installed_version, dependency.version):
            return False
    return True


class GE_TOOLS_OT_install_dependency(bpy.types.Operator):
    bl_idname = "getools.install_dependency"
    bl_label = "Install dependency"
    bl_description = "Download and install/upgrade package. It is advisable to save a backup of the currently " \
                     "installed packages beforehand, in case this operation breaks something in other addons!"
    bl_options = {"REGISTER", "INTERNAL"}

    dependency_index: IntProperty(default=0)
    upgrade: BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return not dependencies_fulfilled()

    def execute(self, context):
        dependency = dependencies[self.dependency_index]
        try:
            install_dependency(dependency, self.upgrade)
            import_module(module_name=dependency.module,
                          global_name=dependency.name)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        #bpy.ops.script.reload()
        # Register the panels, operators, etc. since dependencies are installed
        #for cls in classes:
        #    bpy.utils.register_class(cls)

        return {"FINISHED"}


class GE_TOOLS_OT_backup_packages(bpy.types.Operator):
    bl_idname = "getools.backup_packages"
    bl_label = "Backup Packages"
    bl_description = "Backup list of python packages and versions to the file specified"
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return is_admin()

    def execute(self, context):
        try:
            environ_copy = dict(os.environ)
            environ_copy["PYTHONNOUSERSITE"] = "1"
            path = bpy.context.preferences.addons[__package__].preferences.package_backup_file
            with open(path, 'w') as file_:
                subprocess.run([sys.executable, "-m", "pip", "freeze", "--exclude-editable"], stdout=file_,
                               check=True, env=environ_copy)
        except subprocess.CalledProcessError as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        return {"FINISHED"}


class GE_TOOLS_OT_restore_packages(bpy.types.Operator):
    bl_idname = "getools.restore_packages"
    bl_label = "Restore Packages"
    bl_description = "Restore packages to saved versions, if file exists"
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return is_admin()

    def execute(self, context):
        try:
            environ_copy = dict(os.environ)
            environ_copy["PYTHONNOUSERSITE"] = "1"
            path = bpy.context.preferences.addons[__package__].preferences.package_backup_file
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", path],
                           check=True, env=environ_copy)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        return {"FINISHED"}


def register():
    bpy.utils.register_class(GE_TOOLS_OT_install_dependency)
    bpy.utils.register_class(GE_TOOLS_OT_backup_packages)
    bpy.utils.register_class(GE_TOOLS_OT_restore_packages)


def unregister():
    bpy.utils.unregister_class(GE_TOOLS_OT_restore_packages)
    bpy.utils.unregister_class(GE_TOOLS_OT_backup_packages)
    bpy.utils.unregister_class(GE_TOOLS_OT_install_dependency)

