#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import shutil

    
def is_windows():
    """
    ОС windows?
    """
    return sys.platform[:3].lower() == 'win'


def is_linux():
    """
    ОС linux?
    """
    return sys.platform[:3].lower() == 'lin'

if is_windows():
    PATH_DELIMETER = '\\'
elif is_linux():
    PATH_DELIMETER = '/'


def _delWalk(args, CurDir_, CurNames_):
    """
    """
    _dir = args[0]
    del_filter = args[1]
    
    if del_filter[0] in CurNames_:
        pth = CurDir_+PATH_DELIMETER+del_filter[0]
        if os.path.exists(pth):
            try:
                shutil.rmtree(pth, True)
                print('Deleted', pth)
            except:
                raise


def del_x(Dir_, DelFilter_=('.svn', '.SVN', '.Svn')):
    """
    """
    try:
        os.path.walk(Dir_, _delWalk, (Dir_, DelFilter_))
        return True
    except:
        raise

print('START')
del_x(os.getcwd())
