# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['collectmeterdigits/__main__.py','collectmeterdigits/glob.py','collectmeterdigits/hash_manual.py','collectmeterdigits/labeling.py','collectmeterdigits/predict.py', ],
    pathex=['collectmeterdigits/'],
    binaries=[],
    datas=[('collectmeterdigits/models/*.tflite', 'collectmeterdigits/models')],
    hiddenimports=['requests'],
    hookspath=[],
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
    name='collectmeterdigits',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
