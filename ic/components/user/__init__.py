#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Пакет содержит пользовательские компоненты.
"""

import os.path

from ic.dlg import ic_logo_dlg
from ic.log import log

#
__version__ = (1, 1, 1, 1)


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
        if resource.icGetSubsysResPaths() and resource.icGetSubsysResPaths()[0] is not None:
            lst_dir += resource.icGetSubsysResPaths()
        
        for i, user_dir in enumerate(lst_dir):
            subsys = ''
            if i > 0:
                p, subsys = os.path.split(user_dir)
                user_dir += '/%s' % DEFAULT_SUBSYS_PACKAGE

            level_import = 1 if i == 0 else 0
            log.info(u'>>> Папка пользовательских компонентов %s. Уровень импорта [%d]' % (user_dir, level_import))
            if user_dir and os.path.isdir(user_dir):
                dir_list = os.listdir(user_dir)
                
                for j, file in enumerate(dir_list):
                    if '__init__.py' not in file and '.bak' not in file:
                        path, fileName = os.path.split(file)
        
                        #   Определяем расширение
                        try:
                            ext = fileName.split('.')[1]
                        except:
                            ext = None
        
                        #   Импортируем пользовательский модуль
                        if i > 0:
                            # Модуль их папки компонентов подсистемы
                            md = subsys + '.' + prefix + fileName.split('.')[0]
                        else:
                            # Модуль из папки системных компонентов
                            md = fileName.split('.')[0]

                        if ext == 'py' and md not in not_load_lst:
                            try:
                                log.info(u'>>> Импорт пользовательского компонента %s' % md)
                                ic_logo_dlg.setLoadProccessBoxLabel(u'>>> Импортируемый компонент: %s' % md,
                                                                    100 * j / len(dir_list))

                                # ВНИМАНИЕ! Аргумент level определяет уровень с которого
                                # происходит импортирование.
                                # Если level=0, то импорт происходит с глобального уровня
                                # Если level=1, то импорт происходит с текущего пакета
                                # Если level=2, то импорт происходит с родительского пакета и т.п.
                                class_mod = __import__(md, globals(), locals(),
                                                       # fromlist=sys.path,
                                                       level=level_import)

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
                                except AttributeError as msg:
                                    typ = None
                                    log.warning(u'### В модуле <%s> не корректный интерфейс компонента (Проверте переменную <ic_class_spc>)' % md)
                            except:
                                log.fatal(u'###! Ошибка импорта модуля: %s' % md, bForcePrint=True)
                                log.warning(u'ВНИМАНИЕ! Возможно в корневой папке подсистемы находится __init__.py.')

    return user_modules_dict

