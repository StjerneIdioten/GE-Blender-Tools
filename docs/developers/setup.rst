.. _developers_setup:

Setup Development Environment
=============================

To work on the Blender addon you will need to clone the source repo to your PC and then somehow make Blender aware
of the *addon* folder. The preferred way is to create a symbolic link in your Blender versions *scripts/addons* folder
with the name "GETools", since this is the name that the addon is distributed under. Although it is advised to keep
the code agnostic to the folder name by using :code:`__package__` to refer to the addon in code and
:code:`from . import submodule` when doing imports.

The way to create this symlink in an elevated powershell would be:

.. code-block:: powershell

  New-Item -ItemType SymbolicLink -Path "%APPDATA%\Roaming\Blender Foundation\Blender\3.0\scripts\addons\GETools" -Target "GE-Blender-Tools\addon"

Where you of course replace *-Path* and *-Target* with path that fit your setup.

.. Note::
    Default Blender addon location in Windows is
    *"%APPDATA%\\Roaming\\Blender Foundation\\Blender\\3.0\\scripts\\addons"*, where the version number is whatever you
    are developing against currently.

Upgrading Blender Version
-------------------------
When you upgrade Blender to a new version so e.g. going from *2.91 → 2.92* Blender will always ask you whether or
not you are interested in bringing over your settings, which you usually are. But if you have done this symlinking and
you just open Blender normally, then it will fail on moving the symlink. To avoid this you need to open Blender with
administrative rights the first time you open a new installation, to allow it to create a new symlink for your new
Blender installation.

Codeveloping with GE-Core
-------------------------
This addon uses underlying functionality of the GE-Core library to interact with all the Giants Engine specific files,
thus most of the development should really be on the Blender specific side of things. But it might be that certain
features need to be developed/changed in GE-Core or that you just want to work directly with the bleeding edge source
instead of only the released builds on PyPi. In any case, to do this you should clone the GE-Core repository and
install it into your Blender Python as a development package. To do this in Windows it requires you to do the following
in powershell:

.. code-block:: powershell

  C:\Program Files\Blender Foundation\Blender 3.0\3.0\python\bin\python.exe -m pip install -e "path\to\GE-Core"

Of course with the path to your own Blender installation and location of the cloned GE-Core source.

In doing this pip will call distutils and generate all the information it needs from GE-Core and create the relevant
files in your Blender's python's site-packages (amongst that it tells python where GE-Core is actually located).
You can then develop away on GE-Core as well and all your imports in GETools will work out as they should as well as
the dependency checking that the addon does upon startup.
