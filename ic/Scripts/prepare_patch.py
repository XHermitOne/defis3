#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, os.path
import sys
import datetime
import time
import shutil
__doc__ = """ Create patch folder with changed files.
prepare_patch path [lt [path_to [ignor_list] ]]
path    - files projects path
lt      - compare time - files changed after this time will copy to patch folder
path_to - patch folder. Old files will deleted
ignor_lst - ignor list files. For example: '*.doc', 'first.bat'

Example: prepare_patch c:\defis 2009.09.04 c:\defis_patch *.pyc *.pyo
"""
IGNOR_PATCH_FILE_EXT = [
    '*.pyc',
    '*.~py',
    '*.edbkup',
    '*.backup',
    '*.pyo',
    '*.log',
    '*.lck',
    '*.bak',
    '*_pkl.*',
    '*.rar',
    #'*.html',
    '*.zip',
    '.svn',
    '*.mdb',
    'Thumbs.db',
    '*.tmp',
    '*.chm',
    #'*.doc',
    '.pdbrc',
]

IGNOR_PATCH_FOLDER_PRZ = ['.svn',
    '.git',
    '/lock',
    '/log',
    '/tmp',
    'Registr/admin',
    #'Registr/NSI',
    'Registr/STD',
    'media/npa',
    ]

IGNOR_RELEASE_FOLDER_PRZ = ['.svn',
    '.git',
    '/lock',
    '/log',
    '/tmp',
    'Registr/admin',
    ]

#IGNOR_PATCH_FOLDER_PRZ = IGNOR_RELEASE_FOLDER_PRZ

def parse_folder(args, dirname, names):
    """ """
    dirname = dirname.replace('\\','/')
    for ign in IGNOR_PATCH_FOLDER_PRZ:
        if ign in dirname:
           return

    path = args[0].replace('\\', '/')
    path_to = args[1].replace('\\', '/')
    lt = args[2]
    il = args[3]
    f = args[4]
    bp = False
    todir = dirname.replace(path, path_to)
    if not os.path.isdir(todir) and names:
#        os.makedirs(todir)
#        print 'make dirs:', todir, len(names)
#        f.write('make dirs:%s\n' % todir)
#        bp = True
        pass
#    elif names:
#        print 'dir:', todir

    for fn in names:
        ignor = False
        for ign in il:
            ign=ign.replace('*','')
            if ign in fn:
                ignor = True
                break
        src = '%s/%s' % (dirname, fn)
        if not ignor and not os.path.isdir(src):
            tm = os.path.getmtime(src)
            st = list(time.gmtime(tm))
            #st[3] += 8
            #print st
            tt = '%04d.%02d.%02d %02d:%02d' % (st[0], st[1], st[2], st[3], st[4])
            if tt >= lt:
                dst =  '%s/%s' % (todir, fn)
                if not bp and not os.path.isdir(todir):
                    os.makedirs(todir)
                    print('make dirs:', todir)
                    f.write('make dirs:%s\n' % todir)
                    bp = True

                shutil.copyfile(src, dst)

                if not bp:
                    bp = True
                    print('dir:', todir)
                    f.write('dir:%s\n'% todir)

                s = '    %s ./%s -> %s' % (tt, fn, dst)
                print(s)
                f.write(s+'\n')

def prepare_patch_tree(path, path_to, lt, ignor_list=IGNOR_PATCH_FILE_EXT):
    """ Создает папку с файлами которые изменились с определенного времени.
    @param path: Путь до папки с проектом.
    @param path_to: Путь куда положить патч.
    @param lt: Время актуальных изменений. Если не указано, то изменения беруться за текущий день.
    @param ignor_list: Список игнорируемых файлов.
    """
    ignor_list = ignor_list or IGNOR_PATCH_FILE_EXT
    #print (path, path_to, lt, ignor_list)
    f = open('patch.log', 'w')
    os.path.walk(path, parse_folder, (path, path_to, lt, ignor_list, f))
    f.close()

def main():
    pars = sys.argv[1:]
    if len(pars) > 0:
        path = pars[0]
    else:
        print('Not define path to project folder.')
        print(__doc__)
        return

    if path.endswith('/'):
        path = path[:-1]

    now = datetime.datetime.now()

    if len(pars) > 1:
        lt = pars[1].replace('-','.').replace('&',' ')
    else:
        lt = '%04d.%02d.%02d' % (now.year, now.month, now.day)

    if len(pars) > 2:
        path_to = pars[2]
    else:
        path_to = '%s_patch_%04d_%02d_%02d' % (path, now.year, now.month, now.day)

    if len(pars) > 3:
        ignor_list = pars[3:]
    else:
        ignor_list = None

    prepare_patch_tree(path, path_to, lt, ignor_list)

if __name__ == '__main__':
    main()