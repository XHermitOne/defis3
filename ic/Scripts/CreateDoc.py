#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import epydoc.cli as cli


def GetPackageModuleList(package_name, ignore_lst,  moduleList=None):
    """
    Функция возвращает список модулей пакета со всеми вложениями.

    @type package_name: C{string}
    @param package_name: Полный путь до питоновского пакета.
    """
    if not moduleList:
        moduleList = []
        
    if os.path.isdir(package_name):
        #   Определяем список файлов
        dir_list = os.listdir(package_name)

        #   Если это не питоновский пакет, то выходим из функции
        if '__init__.py' not in dir_list:
            print('Dir %s isn\'t package' % package_name)
            return moduleList

        for indx, fl in enumerate(dir_list):
            path, fileName = os.path.split(fl)

            #   Определяем расширение            
            try:
                ext = fileName.split('.')[1]
            except:
                ext = None
            
            fn = package_name+'/'+fl
            
            #   Если очередное имя является именем директории то рекурсивно 
            #   вызываем функцию создания списка модулей.
            if os.path.isdir(fn) and fn not in ignore_lst:
                print('Dir:', fn, '.......')
                GetPackageModuleList(fn, ignore_lst, moduleList)
                
            elif ext in ['py', 'PY']:
                print('append: ', fn) 
                moduleList.append(fn)
    else:
        print('Package <%> didn\'t find') 

    return moduleList


def main(package_name,  ignore_lst):
    lst = GetPackageModuleList(package_name,  ignore_lst)
    
    ArgV = ['--debug'] + lst
    cli.cli(ArgV)


if __name__ == '__main__':
    main('C:/Python23/Lib/site-packages/ic',  ['C:/Python23/Lib/site-packages/ic/icEditor'])
