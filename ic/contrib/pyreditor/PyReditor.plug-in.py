# PyReditor - Advanced Python Regular Expresion Editor
#
# Copyright (c) 2008, 2009
# Primoz Cermelj <primoz.cermelj@gmail.com>
#
# This program is based on RegexEditor.plug-in.py plugin originated from
# Boa Constructor and is licensed under GPL.
# 
# See LICENSE.TXT for license terms.
#----------------------------------------------------------------------------
"""
This is a Boa Constructor-based plugin interface to PyReditor. This will
be displayed under the menu "Tools" in Boa Constructor.

See plugin-install.txt too.
"""

from .pyreditor.pyreditor import PyReditorFrm
import Preferences, Utils, Plugins
from Utils import _
import os, sys

_NAME = 'PyReditor'
_IMG = 'pyreditor/Images/pyreditor.png'
_RELPATH = 'pyreditor'


class ToolFrame(PyReditorFrm, Utils.FrameRestorerMixin):
    def __init__(self, parent, relpath=_RELPATH):
        path = os.path.join(os.path.split(sys.argv[0])[0], relpath)
        PyReditorFrm.__init__(self, parent, path=path)
        self.loadDims()


def openFrame(editor):
    frame = ToolFrame(editor)
    frame.Show()
    
    
def getImgData():
    res = '\x89PNG\r\n'
    try:
        fh = open(_IMG, 'rb')
        res = fh.read()
        fh.close()
    except:
        pass
    return res
    

Plugins.registerTool(_(_NAME), openFrame, _IMG)
Preferences.IS.registerImage(_IMG, getImgData())



