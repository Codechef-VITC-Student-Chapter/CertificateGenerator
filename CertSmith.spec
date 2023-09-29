# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['cer.py'],
    pathex=[],
    binaries=[],
    datas=[('./codechefXvitcc.png', '.'), ('./email.csv', '.'), ('./Roboto.woff', '.'), ('./user_credentials.json', '.'), ('./macOS-Sonoma-light.jpg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CertSmith',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['examples/CertSmith icon type 2 iter 4.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CertSmith',
)
app = BUNDLE(
    coll,
    name='CertSmith.app',
    icon='./examples/CertSmith icon type 2 iter 4.png',
    bundle_identifier=None,
)
