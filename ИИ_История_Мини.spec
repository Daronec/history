# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interfaces\\windows\\windows_interface_universal.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('configs', 'configs')],
    hiddenimports=['tkinter', 'PIL', 'pdfplumber', 'PyPDF2', 'pymupdf', 'docx2txt', 'python-docx'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'transformers', 'tensorflow', 'numpy', 'pandas', 'matplotlib', 'seaborn', 'jupyter', 'flask', 'streamlit'],
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
    name='ИИ_История_Мини',
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
    icon=['icon.ico'],
)
