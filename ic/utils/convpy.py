#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

__version__ = (0, 1, 1, 1)


def DoPyEndLine(dir_path):
    """
    Функция во всех модулях пакета приводит разделители линий к питоновскому виду.
    """

    if os.path.isdir(dir_path):
        #   Определяем список файлов
        dir_list = os.listdir(dir_path)

        for indx, fl in enumerate(dir_list):
            path, fileName = os.path.split(fl)
            try:
                ext = fileName.split('.')[1]
            except:
                ext = None
            
            fn = os.path.join(dir_path, fl)
            
            #   Если очередное имя является именем директории то рекурсивно 
            #   вызываем функцию конвертации файлов директории
            if os.path.isdir(fn):
                print('dir:', fn, '.......')
                DoPyEndLine(fn)
                
            elif ext in ['py', 'PY']:
                f = None
                try:
                    f = open(fn, 'rt')
                    txt = f.read(-1)
                    txt = txt.replace('\r\n', '\n').replace('\n\r', '\n').replace('\r', '\n')
                    f.close()
                    
                    f = open(fn, 'wt')
                    f.write(txt)
                    f.close()

                    print('>> Success convert file:', fn)
                except:
                    if f:
                        f.close()
                    print('convert Error file:', fn)


if __name__ == '__main__':
    DoPyEndLine('C:/Python23/Lib/site-packages/ic')
