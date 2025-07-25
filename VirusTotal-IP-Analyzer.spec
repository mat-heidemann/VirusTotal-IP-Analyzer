# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the directory where this spec file is located
try:
    spec_root = Path(__file__).parent
except NameError:
    # Fallback when __file__ is not defined (e.g., when testing)
    spec_root = Path.cwd()

block_cipher = None

# Define the main script
main_script = spec_root / 'main.py'

# Define data files to include
datas = [
    (str(spec_root / 'src'), 'src'),
    (str(spec_root / 'assets' / 'icon.png'), 'assets'),
]

# Define hidden imports
hiddenimports = [
    'customtkinter',
    'requests',
    'cryptography',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'PIL',
    'PIL._tkinter_finder',
]

# Analysis
a = Analysis(
    [str(main_script)],
    pathex=[str(spec_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate entries
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Determine platform and set appropriate executable name and settings
import platform
current_platform = platform.system().lower()

if current_platform == 'windows':
    exe_name = 'VirusTotal-IP-Analyzer-Windows'
    console_mode = False
    icon_path = str(spec_root / 'assets' / 'icon.ico') if (spec_root / 'assets' / 'icon.ico').exists() else None
else:
    exe_name = 'virustotal-ip-analyzer-linux'
    console_mode = True
    icon_path = None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=console_mode,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
