from distutils.spawn import find_executable
import os
import shutil
import pathlib
import subprocess


def is_tool(name):
    """Check whether `name` is on PATH."""
    return find_executable(name) is not None


if not is_tool('pyinstaller'):
    print("Installing pyinstaller")
    subprocess.run(['pip', 'install', 'pyinstaller'], capture_output=False)
    print("Done installing pyinstaller")


print("Creating spec file")

fileData = """
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ( 'assets', 'assets' )
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

"""

with open('main.spec', 'w') as f:
    f.write(fileData)


currentWdPath = str(pathlib.Path().resolve())

print("Building your shitty app")
output = subprocess.run(["pyinstaller", "--onefile", "--noconsole", "main.py"], capture_output=False)
print(output)
if output:
    executable_extension = ""
    if os.name == 'nt':
        executable_extension = '.exe'

    src_path = os.path.join(currentWdPath, 'dist', 'main'+executable_extension)
    shutil.move(src_path, currentWdPath)

    print("Done building your shitty app")
    print("ur gay btw")

