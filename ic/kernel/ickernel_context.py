#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Описание контекств ядра системы.
"""

import os
import os.path
import sys

from ic.utils import filefunc
from ic.utils import ic_mode
from ic.utils import impfunc
from . import icContext
from ic.log import log

__version__ = (0, 1, 1, 1)


GET_KERNEL_FUNC = compile(u'''
def get_kernel():
    return globals().kernel
''', '<string>', 'exec')


class icKernelContext(icContext.BaseContext):
    """
    Контекст ЯДРА объектов системы.
    """

    def init_context(self, *arg, **kwarg):
        """
        Инициализируем контекст.
        """
        from . import ic_dot_use
        from . import icscheme
        from . import icsettings
        self['metadata'] = ic_dot_use.icMetaDataDotUse()
        self['schemas'] = icscheme.icDBSchemasDotUse()
        self['settings'] = icsettings.icSettingsDotUse()
        
    def Get(self, name):
        """
        Получить копию объекта.
        @param name: Имя объекта.
        @return: Возвращает копию объекта не связанную с оригиналом
            или None, если нет такого объекта.
        """
        return self.get(name, None)

    def Set(self, name, data):
        """
        Сохранить объект.
        @param name: Имя объекта.
        @param data: Данные.
        @return: Возвращает результат выполнения операции (False или True).
        """
        return self.__setitem__(name, data)

    def Del(self, name):
        """
        Удалить объект.
        @param name: Имя объекта.
        @return: Возвращает удаленный из хранилища объект.
        """
        return self.__delitem__(name)
        
    def Clear(self):
        """
        Очистить контекст.
        """
        return self.clear()

    def Is(self, Name_):
        """
        Функция проверяет усть ли объект в хранилище.
        @param Name_: Имя объекта.
        @return: Результат поиска (0/1).
        """
        return Name_ in self
    
    def Print(self):
        """
        Вывести на консоль содержимое ХРАНИЛИЩА.
        """
        try:
            log.info('-------------------------------------------------------------------------------')
            log.info('- Name          --- Value                                                     -')
            log.info('-------------------------------------------------------------------------------')
            for name, value in self.items():
                log.info('%-20s %-50s' % (str(name)[:20], str(value)[:50]))
            log.info('-------------------------------------------------------------------------------')
        except:
            log.fatal(u'Ошибка метода icKernelContext.Print')

    # ФУНКЦИИ ДВИЖКА
    def saveImports(self):
        """
        Сохранение имен импортированных модулей.
        """
        imported_modules = sys.modules.keys()
        self.Set('ImportedPy', imported_modules)
   
    def clearImports(self):
        """
        Удалить импортируемые во время работы модули из пространства имен.
        """
        imported_modules = self.Get('ImportedPy')
        if imported_modules:
            for import_module in sys.modules.keys():
                if not (import_module in imported_modules):
                    try:
                        del sys.modules[import_module]
                    except:
                        log.error(u'Ошибка удаления импортированного модуля %s из пространства имен(sys.modules).' % import_module)

    def refreshImports(self):
        """
        Обновить импортируемы модули.
        """
        self.clearImports()
        self.saveImports()

    def initEnv(self, prj_dir, **environ):
        """
        Инициализация окружения по папке проекта.
        @param prj_dir: Папке проекта.
        """
        if isinstance(prj_dir, str):
            # prj_dirname = prj_dirname.encode(sys.getfilesystemencoding())
            pass
            
        if prj_dir and os.path.isdir(prj_dir):
            # !!!Обязательно нормировать для использования!!!
            prj_dir = os.path.normpath(prj_dir)
        
            # Прописать для импорта родительскую папку проекта
            parent_prj_dir = os.path.dirname(prj_dir)
            if parent_prj_dir not in sys.path:
                # sys.path.append(parent_prj_dir)
                sys.path = impfunc.addImportPath(parent_prj_dir)
            # Прописать папку проекта для импорта
            if prj_dir not in sys.path:
                # sys.path.append(prj_dirname)
                sys.path = impfunc.addImportPath(prj_dir)

            log.info(u'vvvvvvvvvvvvvvvvvvvvvvvv')
            log.info(u'Окружение системы. Пути:')
            log.info(impfunc.getSysPathStr())
            log.info(u'^^^^^^^^^^^^^^^^^^^^^^^^')

            prj_name = os.path.basename(prj_dir)
            # Папка ресурсов проекта
            self.Set('SYS_RES', prj_dir)
            self.Set('PRJ_DIR', prj_dir)
            self.Set('LOG_DIR', os.path.join(os.path.dirname(prj_dir), 'log'))
            self.Set('LOCK_DIR', os.path.join(os.path.dirname(prj_dir), 'lock'))
        
            # Список папок подсистем
            self.Set('SUBSYS_RES', self._getSubSysRes(prj_dir))

        # Дополнительные параметры окружения
        if environ:
            for env in environ:
                self.Set(env, environ[env])

        # Запомнить все импортированные модули/системные модули
        self.clearImports()
        self.saveImports()
  
    def _destroyEnv(self):
        """
        Сброс/разрушение окружения системы.
        """
        prj_dir = self.Get('PRJ_DIR')
        if prj_dir:
            if prj_dir in sys.path:
                i = sys.path.index(prj_dir)
                del sys.path[i]

        self.Clear()
        
        self.clearImports()
        
    def _getSubSysRes(self, prj_dir):
        """
        Получить список директорий подсистем вместе с проектом.
        """
        subsys_res = [prj_dir]
        root_prj_dir = os.path.dirname(os.path.normpath(prj_dir))
        sub_dirs = filefunc.getSubDirs(root_prj_dir)
        # log.debug(u'Проверка списка директорий проектов %s' % str(sub_dirs))
        subsys_dirs = [dir_path for dir_path in sub_dirs if self._isSubSysDir(dir_path) and \
                       not filefunc.isSamePathWin(dir_path, prj_dir)]
        subsys_res.extend(subsys_dirs)
        return subsys_res

    def _isSubSysDir(self, dir_path):
        """
        Проверить, является ли папка папкой подсистемы.
        @param dir_path: Исследуемая папка.
        """
        is_dir = os.path.isdir(dir_path)
        is_init_file = os.path.exists(os.path.join(dir_path, '__init__.py'))
        is_pro_file = bool(filefunc.getFilenamesByExt(dir_path, '.pro'))
        # log.debug(u'Проверка PRO файла %s в директории <%s>' % (is_pro_file, dir_path))
        return is_dir and is_init_file and is_pro_file
    
    def getMainWin(self):
        """
        Определить главное окно системы.
        """
        if ic_mode.isRuntimeMode():
            return self.kernel.getMainWin()
        return None

    def getMainOrg(self):
        """
        Определить главный органайзер.
        """
        try:
            return self.getMainWin().GetMainNotebook()
        except:
            return None

    def getKernel(self):
        """
        Ядро системы. Он же движок.
        """
        return self.kernel

    def getPrjRoot(self):
        """
        Корневой объект дерева проекта.
        """
        if self.Is('PRJ_ROOT'):
            return self.Get('PRJ_ROOT')
        return None
    
    def getCurUserName(self):
        """
        Имя текущего зарегистрированного пользователя в системе.
        """
        return self.Get('UserName')
