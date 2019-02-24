#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import locale
import gettext


def is_package():
    return __file__.find('src') < 0

######################################


APP = 'xpander'
APPNAME = 'xpander'

# check if running from source
if is_package():
    ROOTDIR = '/opt/extras.ubuntu.com/xpander/share'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    ICONDIR = os.path.join(ROOTDIR, 'icons')
    EXAMPLESDIR = '/opt/extras.ubuntu.com/xpander/etc/xpander'
else:
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons/'))
    EXAMPLESDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/Examples/'))

ICON = os.path.join(ICONDIR, 'xpander.svg')
ICON_ACTIVED_LIGHT = os.path.join(ICONDIR, 'xpander-active.svg')
ICON_PAUSED_LIGHT = os.path.join(ICONDIR, 'xpander-paused.svg')
ICON_ACTIVED_DARK = os.path.join(ICONDIR, 'xpander-active-dark.svg')
ICON_PAUSED_DARK = os.path.join(ICONDIR, 'xpander-paused-dark.svg')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'

####
try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    print(language)
    if sys.version_info[0] == 3:
        _ = language.gettext
    else:
        _ = language.ugettext
except Exception as e:
    print(e)
    _ = str
APPNAME = _(APPNAME)
