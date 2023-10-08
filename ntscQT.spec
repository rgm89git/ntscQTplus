# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ntscQT.py'],
    pathex=['C:/hostedtoolcache/windows/python/3.10.11/x64/lib/site-packages'],
    binaries=[('C:/hostedtoolcache/windows/python/3.10.11/x64/lib/site-packages/cv2/opencv_videoio_ffmpeg*.dll', '.'), ('./ffmpeg-2023-10-04-git-9078dc0c52-essentials_build/bin/ffmpeg.exe', '.')],
    datas=[('./app/ringPattern.npy', './app'), ('translate/*.qm', 'translate/'), ('./icon.png', '.'), ('./ui/img/logo32px.png', './ui/img')],
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
    name='ntscQTplus',
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
    icon=['icon.ico'],
)
