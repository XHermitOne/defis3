#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет содержит пользовательские компоненты.
"""

import os.path
import ic.dlg.ic_logo_dlg as ic_logo_dlg
# import ic.kernel.io_prnt as io_prnt
from ic.log import log

#
__version__ = (1, 0, 1, 1)


#   Словарь пользовательских модулей
icUserModulesDict = {}

# Имя пакета, где находятся пользовательские компоненты в подсистемах
DEFAULT_SUBSYS_PACKAGE = 'usercomponents'


def icClearUserModulDict():
    """
    Очистка словаря пользовательских модулей.
    """
    globals()['icUserModulesDict'] = dict()

    
def icGetUserModulDict(not_load_lst=None, bRefresh = False):
    """
    Импортирует пользовательские модули и заполняет словрь, у которого ключи названия
    пользовательских типов, значения соответствующие модули.
    
    @type not_load_lst: C{list}
    @param not_load_lst: Список ползовательских типов, которые подгружать не надо.
    @rtype: C{dictionary}
    @return: Возвращает словрь, у которого ключи - названия пользовательских типов, значения -
        соответствующие модули.
    """
    user_modules_dict = globals()['icUserModulesDict']

    if not not_load_lst:
        not_load_lst = []
        
    if not user_modules_dict:

        import ic.utils.resource as resource

        #   Ищем системные пользовательские компоненты
        lst_dir = [resource.icGetUserClassesPath()]
        prefix = '%s.' % DEFAULT_SUBSYS_PACKAGE 
        
        #   Ищем прикладные пользовательские компоненты
        if resource.icGetSubsysResPaths() and resource.icGetSubsysResPaths()[0] <> None:
            lst_dir += resource.icGetSubsysResPaths()
        
        for i, user_dir in enumerate(lst_dir):
            subsys = ''
            if i > 0:
                p, subsys = os.path.split(user_dir)
                user_dir += '/%s' % DEFAULT_SUBSYS_PACKAGE
                
            log.info('>>> user_dir %s' % user_dir)
            if user_dir and os.path.isdir(user_dir):
                dir_list = os.listdir(user_dir)
                
                for j, file in enumerate(dir_list):
                    if not '__init__.py' in file and not '.bak' in file:
                        path, fileName = os.path.split(file)
        
                        #   Определяем расширение
                        try:
                            ext = fileName.split('.')[1]
                        except:
                            ext = None
        
                        #   Импортируем пользовательский модуль
                        if i > 0:
                            md = subsys+'.'+prefix+fileName.split('.')[0]
                        else:
                            md = fileName.split('.')[0]

                        if ext == 'py' and md not in not_load_lst:
                            try:
                                log.info('>>> user component import %s' % md)
                                ic_logo_dlg.SetLoadProccessBoxLabel(u'>>> Имп. компонент: %s' % md, 100*j/len(dir_list))

                                class_mod = __import__(md, globals(), locals(), [], -1)
                                # Поскольку __import__ возвращает родительский модуль
                                # получаем доступ до нужного нам модуля через 
                                # рекурсивный getattr
                                if i > 0:
                                    c = md.split('.')
                                    for x in c[1:]:
                                        class_mod = getattr(class_mod, x)

                                #   Определяем атрибут подсистемы
                                class_mod.user_subsys = subsys
                                try:
                                    typ = class_mod.ic_class_spc['type']
                                    user_modules_dict[typ] = class_mod
                                except AttributeError, msg:
                                    typ = None
                                    log.warning(u'### module <%s> has invalid component interface (absent variable <ic_class_spc>)' % md)
                            except:
                                try:
                                    log.fatal(u'###! import error module: %s' % md)
                                except:
                                    print(u'###! import error module: %s' % md)

    return user_modules_dict

