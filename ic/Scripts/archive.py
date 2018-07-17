#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import time

# Не акхивируемые файлы
_not_archived_file_ext = ['.dia~', '.pyc', '.PYC', '.bak', '.BAK', '.lck', '.LCK',
                          '.~py', '.~PY', '.dbg', '.DBG',
                          '_pkl.frm', '_pkl.tab', '_pkl.src', '_pkl.mnu',
                          '_pkl.acc', '_pkl.mtd', '_pkl.win', '_pkl.rol', '_pkl.odb']


def _del_not_archived_walk(args, cur_dir, cur_names):
    """
    Фнукция удаления ненужных файлов.
    """
    for cur_name in cur_names:
        _find_ = False
        for ext in args:
            if cur_name[-len(ext):] in args:
                _find_ = True
                break
        if _find_:
            full_name = cur_dir+'/'+cur_name
            if os.path.isfile(full_name):
                print('DELETE:', full_name)
                os.remove(full_name)


def del_all_not_archived():
    return os.path.walk(os.getcwd(), _del_not_archived_walk, tuple(_not_archived_file_ext))


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


time_start = time.time()


print('DELETE NOT ARCHIVED FILES:')
del_all_not_archived()
print('...OK')

if is_linux():
    # Перед архивированием удаляем оставшиеся архивы
    DEL_CMD = 'rm -f -v py_prj_svn_linux*.zip'
    print('DELETE FILE:', DEL_CMD)
    os.system(DEL_CMD)
    
    CUR_DATE_STR = time.strftime('_%Y_%m_%d', time.localtime(time.time()))
    ARCHIVE_CMD = 'zip -r py_prj_svn_linux%s.zip *' % CUR_DATE_STR
    print('RUN COMMAND:', ARCHIVE_CMD)
    os.system(ARCHIVE_CMD)
    print('...OK')

    COPY_PATH = '/media/KINGSTON/'
    if os.path.exists(COPY_PATH):
        DEL_CMD = 'rm -f -v %spy_prj_svn_linux*.zip' % COPY_PATH
        print('DELETE FILE:', DEL_CMD)
        os.system(DEL_CMD)

        MOVE_CMD = 'mv py_prj_svn%s.zip %s' % (CUR_DATE_STR, COPY_PATH)
        print('MOVE:', MOVE_CMD)
        os.system(MOVE_CMD)

elif is_windows():
    CUR_DATE_STR = time.strftime('_%Y_%m_%d', time.localtime(time.time()))
    ARCHIVE_CMD = '"C:\Program Files\WinRAR\WinRar.exe" a -r -s py_prj_svn_win32%s.zip *' % CUR_DATE_STR
    print('RUN COMMAND:', ARCHIVE_CMD)
    os.system(ARCHIVE_CMD)
    print('...OK')

stop_time = time.time() - time_start
print('Time:', stop_time, ' sec.', stop_time/60, 'min.')
