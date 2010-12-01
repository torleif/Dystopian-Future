"""
Script for building the example.

Usage:
    python setup.py py2app
"""
from distutils.core import setup
import py2app

NAME = 'Black and White'
VERSION = '0.1'

plist = dict(
    CFBundleIconFile=NAME,
    CFBundleName=NAME,
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
    CFBundleIdentifier='org.pygame.examples.bw',
)

setup(
    data_files=['English.lproj', 'textures', 'ambient', 'icon.png', 'levels', 'textures', 'seven.ttf'],
    app=[
        #dict(script="aliens_bootstrap.py", plist=plist),
        dict(script="game.py", plist=plist),
    ],
)
