#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Описание контекств ядра системы.
"""

import os
import os.path
import sys
from ic.kernel import io_prnt

from ic.utils import ic_file
from ic.utils import ic_mode
from . import icContext
from ic.log import log


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
        
    def Get(self, Name_):
        """
        Получить копию объекта.
        @param Name_: Имя объекта.
        @return: Возвращает копию объекта не связанную с оригиналом
            или None, если нет такого объекта.
        """
        return self.get(Name_, None)

    def Set(self, Name_, Data_):
        """
        Сохранить объект.
        @param Name_: Имя объекта.
        @param Data_: Данные.
        @return: Возвращает результат выполнения операции (False или True).
        """
        return self.__setitem__(Name_, Data_)

    def Del(self, Name_):
        """
        Удалить объект.
        @param Name_: Имя объекта.
        @return: Возвращает удаленный из хранилища объект.
        """
        return self.__delitem__(Name_)
        
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
            io_prnt.outErr(u'Ошибка метода icKernelContext.Print')

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
                        io_prnt.outErr(u'Ошибка удаления импортированного модуля %s из пространства имен(sys.modules).' % import_module)

    def refreshImports(self):
        """
        Обновить импортируемы модули.
        """
        self.clearImports()
        self.saveImports()

    def initEnv(self, PrjDir_, **environ):
        """
        Инициализация окружения по папке проекта.
        @param PrjDir_: Папке проекта.
        """
        if isinstance(PrjDir_, unicode):
            PrjDir_ = PrjDir_.encode(sys.getfilesystemencoding())
            
        if PrjDir_ and os.path.isdir(PrjDir_):
            # !!!Обязательно нормировать для использования!!!
            PrjDir_ = os.path.normpath(PrjDir_)
        
            # Прописать для импорта родительскую папку проекта
            if PrjDir_ not in sys.path:
                sys.path.append(PrjDir_)
            parent_prj_dir = os.path.dirname(PrjDir_)
            if parent_prj_dir not in sys.path:
                sys.path.append(parent_prj_dir)

            io_prnt.outLog(u'vvvvvvvvvvvvvvvvvvvvvvvv')
            io_prnt.outLog(u'Окружение системы. Пути:')
            for pth in sys.path:
                io_prnt.outLog(u'\t%s' % pth)
            io_prnt.outLog(u'^^^^^^^^^^^^^^^^^^^^^^^^')

            prj_name = os.path.basename(PrjDir_)
            # Папка ресурсов проекта
            self.Set('SYS_RES', PrjDir_)
            self.Set('PRJ_DIR', PrjDir_)
            self.Set('LOG_DIR', os.path.dirname(PrjDir_)+'/log/')
            self.Set('LOCK_DIR', os.path.dirname(PrjDir_)+'/lock')
        
            # Список папок подсистем
            self.Set('SUBSYS_RES', self._getSubSysRes(PrjDir_))

        # Дополнительные параметры окружения
        if environ:
            for env in environ:
                self.Set(env, environ[env])

        # Запомнить все импортированные модули/системные модули
        self.clearImports()
        self.saveImports()
  
    def _DestroyEnv(self):
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
        
    def _getSubSysRes(self, PrjDir_):
        """
        Получить список директорий подсистем вместе с проектом.
        """
        subsys_res = [PrjDir_]
        root_prj_dir = os.path.dirname(os.path.normpath(PrjDir_))
        sub_dirs = ic_file.GetSubDirs(root_prj_dir)
        subsys_dirs = [dir_path for dir_path in sub_dirs if self._IsSubSysDir(dir_path) and \
                             not ic_file.SamePathWin(dir_path, PrjDir_)]
        subsys_res.extend(subsys_dirs)
        return subsys_res

    def _IsSubSysDir(self, Dir_):
        """
        Проверить, является ли папка папкой подсистемы.
        @param Dir_: Исследуемая папка.
        """
        is_dir = os.path.isdir(Dir_)
        is_init_file = os.path.exists(Dir_+'/__init__.py')
        is_pro_file = bool(ic_file.GetFilesByExt(Dir_, '.pro'))
        return is_dir and is_init_file and is_pro_file
    
    def getMainWin(self):
        """
        Определить главное окно системы.
        """
        if ic_mode.isRuntimeMode():
            return self.kernel.GetMainWin()
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
