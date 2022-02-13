import os
from sys import executable as blender_python_bin
import subprocess
from importlib import metadata
from collections import namedtuple
import logging

import bpy
from bpy.props import *

from ..utility import (addon_name, is_admin, compare_versions, import_module)

logger = logging.getLogger(__name__)

Dependency = namedtuple('Dependency', ['module', 'package', 'name', 'version'])
dependencies = (Dependency(module='gecore', package='ge-core', name=None, version='0.1.0'),
                Dependency(module='colorama', package='colorama', name=None, version='0.4.4'))


class Properties(bpy.types.PropertyGroup):
    package_backup_file: bpy.props.StringProperty(
        default=os.path.expanduser('~\\blender_python_packages_backup.txt'),
        description="Where to save/load a backup of the installed python packages",
        subtype="FILE_PATH"
    )


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
        except ImportError as err:
            self.report({"ERROR"}, str(err))
            logger.exception(err)
            return {"CANCELLED"}
        except subprocess.CalledProcessError as err:
            self.report({"ERROR"}, str(err))
            logger.exception(err)
            # TODO: Figure out a way to handle this more graciously [WinError 5], it happens despite of admin rights

        if dependencies_fulfilled():
            register_addon()

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
            path = bpy.context.preferences.addons[addon_name].preferences.dependencies.package_backup_file
            with open(path, 'w') as file_:
                subprocess.run([blender_python_bin, "-m", "pip", "freeze", "--exclude-editable"], stdout=file_,
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
            path = bpy.context.preferences.addons[addon_name].preferences.dependencies.package_backup_file
            subprocess.run([blender_python_bin, "-m", "pip", "install", "-r", path],
                           check=True, env=environ_copy)
        except (subprocess.CalledProcessError, ImportError) as err:
            # TODO: Check if the file is missing and give a warning about it
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        if not dependencies_fulfilled():
            unregister_addon()

        return {"FINISHED"}


def draw(preferences, context, layout):
    row = layout.row()
    row.alignment = "LEFT"
    has_admin_rights = is_admin()
    if not has_admin_rights:
        row = layout.row()
        row.label(text="Launch Blender as administrator to install/upgrade packages!", icon="ERROR")
    else:
        split = layout.split(factor=0.5)
        split.prop(preferences.dependencies, 'package_backup_file', text='')
        split.operator(GE_TOOLS_OT_backup_packages.bl_idname, text='Backup Package List',
                       icon="FILE_NEW")
        split.operator(GE_TOOLS_OT_restore_packages.bl_idname, text='Restore Packages',
                       icon="FILE_REFRESH")

    deps = dependencies
    dep_box = layout.box()
    row = dep_box.row()
    row.label(text="Package")
    row.label(text="Required Version")
    row.label(text='Installed Version')
    row.label(text='')

    for idx, dep in enumerate(deps):
        version_installed = dependency_installed_version(dep)
        if version_installed == "None":
            op_text = 'Install'
        elif version_installed != '0.0.0' and version_installed != dep.version:
            op_text = 'Upgrade'
        else:
            op_text = 'Installed'
        row = dep_box.row()
        row.label(text=dep.package)
        row.label(text=dep.version)
        if op_text != 'Installed':
            row.alert = True
        row.label(text=version_installed)
        row.alert = False
        op_icon = "ERROR"
        if op_text == 'Installed' or not is_admin:
            row.enabled = False
        if op_text == 'Installed':
            op_icon = "CHECKMARK"
        op = row.operator(GE_TOOLS_OT_install_dependency.bl_idname, text=op_text, icon=op_icon)
        op.dependency_index = idx


classes = (
    GE_TOOLS_OT_install_dependency,
    GE_TOOLS_OT_backup_packages,
    GE_TOOLS_OT_restore_packages,
    Properties
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


def register_addon():
    """Registers the rest of the addon once dependencies are fulfilled"""
    logger.info("Registering Dependent Parts of Addon")


def unregister_addon():
    logger.info("Unregistering Dependent Parts of Addon")


def dependency_installed_version(dependency):
    version = "None"
    # Try if module version can be found through dist-info or egg-info
    try:
        version = metadata.version(dependency.package)
    except metadata.PackageNotFoundError:
        pass
    return version


def install_dependency(dependency, upgrade=False):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([blender_python_bin, "-m", "pip", "install", f"{dependency.package}=={dependency.version}"],
                   check=True, env=environ_copy)


def dependencies_fulfilled():
    for dependency in dependencies:
        installed_version = dependency_installed_version(dependency)
        if not compare_versions(installed_version, dependency.version):
            return False
    return True
