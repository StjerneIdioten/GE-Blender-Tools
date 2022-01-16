import os
import bpy
from . import dependency_handling


class GE_TOOLS_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    package_backup_file: bpy.props.StringProperty(
        default=os.path.expanduser('~\\blender_python_packages_backup.txt'),
        description="Where to save/load a backup of the installed python packages",
        subtype="FILE_PATH"
    )

    def draw(self, context):
        layout = self.layout

        dep_layout = layout.box()
        row = dep_layout.row()
        row.alignment = "LEFT"
        row.label(text="Dependencies:")
        is_admin = dependency_handling.is_admin()
        if not is_admin:
            row = dep_layout.row()
            row.label(text="Launch Blender as administrator to install/upgrade packages!", icon="ERROR")
        else:
            split = dep_layout.split(factor=0.5)
            split.prop(self, 'package_backup_file', text='')
            split.operator(dependency_handling.GE_TOOLS_OT_backup_packages.bl_idname, text='Backup Package List', icon="FILE_NEW")
            split.operator(dependency_handling.GE_TOOLS_OT_restore_packages.bl_idname, text='Restore Packages', icon="FILE_REFRESH")

        deps = dependency_handling.dependencies
        dep_box = dep_layout.box()
        row = dep_box.row()
        row.label(text="Package")
        row.label(text="Required Version")
        row.label(text='Installed Version')
        row.label(text='')

        for idx, dep in enumerate(deps):
            version_installed = dependency_handling.dependency_installed_version(dep)
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
            op = row.operator(dependency_handling.GE_TOOLS_OT_install_dependency.bl_idname, text=op_text, icon=op_icon)
            op.dependency_index = idx


class GE_TOOLS_PT_test_panel(bpy.types.Panel):
    bl_idname = f"{__package__}.test_panel"
    bl_label = "Test Panel"
    bl_region_type = 'WINDOW'
    bl_space_type = "PREFERENCES"
    bl_parent_id = __package__

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello there")


def register():
    bpy.utils.register_class(GE_TOOLS_preferences)
    #bpy.utils.register_class(GE_TOOLS_PT_test_panel)


def unregister():
    #bpy.utils.unregister_class(GE_TOOLS_PT_test_panel)
    bpy.utils.unregister_class(GE_TOOLS_preferences)
