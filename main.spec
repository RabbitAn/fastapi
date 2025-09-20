# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata, collect_all
import os

binaries = []
hiddenimports = []

base_path = os.path.dirname(os.path.abspath(SPEC))
datas = [
    (os.path.join(base_path, 'templates'), 'templates')
]

# 收集依赖包的所有资源
for pkg in ('aerich', 'tortoise-orm', 'asyncpg', 'fastapi'):
    datas_pkg, binaries_pkg, hiddenimports_pkg = collect_all(pkg)
    datas += datas_pkg
    binaries += binaries_pkg
    hiddenimports += hiddenimports_pkg

# 添加元数据
for meta_pkg in ('aerich', 'tortoise-orm', 'fastapi'):
    datas += copy_metadata(meta_pkg)

# 确保 asyncpg backend 被包含
hiddenimports += ['tortoise.backends.asyncpg']

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)
