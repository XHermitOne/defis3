#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс для импортируемых подсистем.
"""

# --- Подключение библиотек ---
# --- Константы ---

__version__ = (0, 0, 0, 3)


# --- Описание классов ---
class ImportSubSysInterface:
    """
    Интерфейс для импортируемых подсистем.
    """

    def __init__(self):
        """
        Конструктор.
        """
        # Имя импортируемой подсистемы
        self.name = None
        # Указание приложения/движка,  под которой запущена подсистема.
        self.app_parent = None
        # Путь к подсистеме, во время выполнения
        self.runtime_path = None
        # Путь к подсистеме для редактирования
        self.edit_path = None

        # Иконка подсистемы.
        self.icon = None
        
        # Пакет импортируемой подсистемы
        self.package = None

    def _import_package(self):
        """
        Инициализация пакета импортируемой подсистемы.
        """
        if not self.package:
            # Если имя определено, то импортировать
            # пакет импортируемой подсистемы
            if self.name:
                exec 'import '+self.name
            self.package = eval(self.name)
        return self.package

    def initialize(self, AppRunTime_=None):
        """
        Инициализация подсистемы в режиме выполнения.
        @param AppRunTime_: Указание приложения/движка,  
            под которым запущена подсистема.
        """
        self.app_parent = AppRunTime_

        package = self._import_package()
        if package:
            try:
                idx = dir(self.package).index('initialize')
                self.package.getattr('initialize')(self.app_parent)
            except ValueError:
                # Если такой функции в пакете нет, то ничего не делать
                pass
            
    def deinitialize(self, AppRunTime_=None):
        """
        Деинициализация подсистемы в режиме выполнения.
        @param AppRunTime_: Указание приложения/движка,  
            под которым запущена подсистема.
        """
        if AppRunTime_: 
            self.app_parent = AppRunTime_
            
        package = self._import_package()
        if package:
            try:
                idx = dir(self.package).index('deinitialize')
                self.package.getattr('deinitialize')(self.app_parent)
            except ValueError:
                # Если такой функции в пакете нет, то ничего не делать
                pass
   
    def install(self, RootPrjTree_=None):
        """
        Функция вызываема при инсталляции подсистемы в редакторе.
        Дополнительное определение подсистемы и ее компонентов 
        во внутренних регистрационных реестрах и таблицах.
        @param RootPrjTree_: Корневой узел дерева проектов.
        """
        package = self._import_package()

        # При инсталяции по умолчанию определить
        # иконку импортируемой подсистемы
        self.getIcon()
        
        if package:
            try:
                idx = dir(self.package).index('install')
                self.package.getattr('install')(RootPrjTree_)
            except ValueError:
                # Если такой функции в пакете нет, то ничего не делать
                pass
        
    def deinstall(self, RootPrjTree_=None):
        """
        Функция,  вызываемая при деинсталяции подсистемы из редактора.
        @param RootPrjTree_: Корневой узел дерева проектов.
        """
        package = self._import_package()
        if package:
            try:
                idx = dir(self.package).index('deinstall')
                self.package.getattr('deinstall')(RootPrjTree_)
            except ValueError:
                # Если такой функции в пакете нет, то ничего не делать
                pass

    def getIcon(self):
        """
        Определений иконки подсистемы.
        Иконка в основном необходима для образного представления 
        подсистемы во время редактирования.
        """
        if not self.icon:
            package = self._import_package()
            if package:
                try:
                    idx = dir(self.package).index('get_icon')
                    self.icon = self.package.getattr('get_icon')()
                except ValueError:
                    # Если такой функции в пакете нет, то ничего не делать
                    self.icon = None
        return self.icon
