# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interfaces\\windows\\windows_interface_exe.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src'), ('data', 'data'), ('models', 'models')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox', 'tkinter.filedialog', 'flask', 'transformers', 'torch', 'tensorflow', 'numpy', 'pandas', 'sklearn', 'matplotlib', 'seaborn', 'requests', 'beautifulsoup4', 'lxml', 'tqdm', 'jupyter', 'ipykernel'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI_History',
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
