#!/usr/bin/env python
# code: utf-8

'''
A wrapper script to generate zip files for GitHub releases.

This script tends to be compatible with both Python 2 and Python 3.
'''

from __future__ import print_function

import os
import shutil
import subprocess


DEDRM_SRC_DIR = 'dedrm_src'
OBOK_SRC_DIR = 'obok_src'
SHELLS_BASE = 'contrib'

def make_calibre_plugin():
    calibre_plugin_dir = os.path.join(SHELLS_BASE, 'DeDRM_calibre_plugin')
    core_dir = os.path.join(calibre_plugin_dir, 'DeDRM_plugin')

    shutil.copytree(DEDRM_SRC_DIR, core_dir)
    shutil.make_archive(core_dir, 'zip', core_dir)
    shutil.rmtree(core_dir)


def make_obok_plugin():
    obok_plugin_dir = os.path.join(SHELLS_BASE, 'Obok_calibre_plugin')
    core_dir = os.path.join(obok_plugin_dir, 'obok_plugin')

    shutil.copytree(OBOK_SRC_DIR, core_dir)
    shutil.make_archive(core_dir, 'zip', core_dir)
    shutil.rmtree(core_dir)


def make_windows_app():
    windows_app_dir = os.path.join(SHELLS_BASE, 'DeDRM_Windows_Application')
    core_dir = os.path.join(windows_app_dir, 'DeDRM_App', 'DeDRM_lib', 'lib')

    # delete any existing core_dir
    try:
        shutil.rmtree(core_dir)
    except OSError:
        pass

    shutil.copytree(DEDRM_SRC_DIR, core_dir)


def make_standalone_windows_app():
    contrib_dir = os.path.join(CONTRIB_BASE, 'windows_standalone')

    build_dir = os.path.join(BUILD_BASE, 'DeDRM_Standalone_Windows_Application')

    cmd = ("pyinstaller "
           "-y "
           "--workpath=pyi_build "
           "--distpath=" + build_dir + " "
           + contrib_dir + "\DeDRM_App.spec").split()

    # STDERR is redirected to STDOUT. Printing any STDERR in Appveyor results in an error during build.
    subprocess.call(cmd, stderr=subprocess.STDOUT)

    # Some distributions of Python "read-only"-erize their files. (e.g. ActiveState)
    # Decontaminate the build of them if this is built using those distributions.
    subprocess.call(('attrib -R ' + build_dir + '\\* /S').split(), stderr=subprocess.STDOUT)
    shutil.copy(os.path.join(contrib_dir, 'DeDRM_Standalone_App_ReadMe.txt'), build_dir)


def make_macos_app():
    macos_app_dir = os.path.join(SHELLS_BASE, 'DeDRM_Macintosh_Application')
    core_dir = os.path.join(macos_app_dir, 'DeDRM.app', 'Contents', 'Resources')

    # Resources already exists - copy contents to contents.
    _, dirs, files = next(os.walk(DEDRM_SRC_DIR))
    for name in dirs:
        shutil.copyfile(
            os.path.join(DEDRM_SRC_DIR, name),
            os.path.join(core_dir, name)
        )
    for name in files:
        shutil.copy2(
            os.path.join(DEDRM_SRC_DIR, name),
            os.path.join(core_dir, name)
        )


def make_release(version):
    make_calibre_plugin()
    make_windows_app()
    # PyInstaller only supports building on the target platform for the target platform.
    if sys.platform == "win32":
        make_standalone_windows_app()
    make_macos_app()
    make_obok_plugin()

    release_name = 'DeDRM_tools_{}'.format(version)
    return shutil.make_archive(release_name, 'zip', SHELLS_BASE)


if __name__ == '__main__':
    import sys
    try:
        version = sys.argv[1]
    except IndexError:
        raise SystemExit('Usage: {} version'.format(__file__))

    print(make_release(version))
