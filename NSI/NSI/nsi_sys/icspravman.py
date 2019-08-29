#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер справочной системы.
    Справочная система представляет собой ресурс метаданных с
    определенными в нем компонентами справочников.
    В общем менеджер справочников нужен для доступа
    к объектам справочников/перечислений через точке(__getattr__).
"""

# Подключение библиотек
import wx

import ic
from ic.log import log
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.kernel import icexceptions
from ic.engine import glob_functions

# Версия
__version__ = (0, 1, 1, 2)


# Константы
# Имя справочной системы по умолчанию
DEFAULT_NSI_SPRAV_NAME = 'nsi_sprav'


class icSpravManagerContainer(object):
    """
    Контейнер справочников.
        Контейнер справочников необходим для организации доступа к
        справочникам ч/з точку из менеджера справочников.
    """

    def __init__(self, parent_sprav_manager):
        """
        Конструктор.

        """
        self._parent = parent_sprav_manager
        # Справочники и перечисления вместе
        self.__dict__['_all'] = {}
        # Справочники, разложенные по именам
        self.__dict__['_spravDict'] = {}
        # Перечисления, разложенные по именам
        self.__dict__['_enumDict'] = {}

    def getAll(self):
        """
        Все справочники и перечисления.
        """
        return self._all

    all = property(getAll)

    def getSpravDict(self):
        """
        Словарь справочников.
        """
        return self._spravDict

    spravDict = property(getSpravDict)

    def getEnumDict(self):
        """
        Словарь перечислений.
        """
        return self._enumDict

    enumDict = property(getEnumDict)

    def hasName(self, name):
        """
        Зарегистрирован справочник с таким именем?
        """
        return name in self._all

    def setSprav(self, sprav=None):
        """
        Установить справочник/перечисление.
        """
        if sprav:
            self._all[sprav.name] = sprav
            self._all[sprav.name]._sprav_manager = self._parent

    def getSpravByName(self, SpravName_):
        """
        Справочник по имени.
        """
        if self.hasName(SpravName_):
            return self._all[SpravName_]
        return None


class icSpravManagerInterface(object):
    """
    Класс абстрактного менеджера справочной системы.
        Реализует только интерфейс.
    """
    def __init__(self):
        """
        Конструктор.
        """
        pass


class icSpravManagerPrototype(icSpravManagerInterface):
    """
    Менеджер справочной системы.
    """

    def __init__(self):
        """
        Конструктор.
        """
        icSpravManagerInterface.__init__(self)
        # Контейнер справочников
        self._container = icSpravManagerContainer(self)

    def getContainer(self):
        """
        Контейнер справочников.
        """
        return self._container

    container = property(getContainer)

    def getSpravByName(self, sprav_name):
        """
        Получить справочник по имени.
        @param sprav_name: Имя справочника.
        """
        return self._container.getSpravByName(sprav_name)

    def __nonzero__(self):
        """
        Провера на не 0.
        """
        return self is not None

    def __getattr__(self, name):
        """
        Доступ к справочникам и перечислениям через точку.
        """
        container = self.__dict__['_container']
        if container.hasName(name):
            return container.all[name]
        else:
            # По умолчанию
            try:
                return self.__dict__[name]
            except KeyError:
                return None

    def admin(self, parent=None,
              title=u'Администрирование справочников',
              prompt_text=u'Выберите справочник для редактирования:'):
        """
        Администрирование справочной системы, описываемой данным менеджером.
        @param parent: Родительское окно для формы редактирования справочника.
        """
        if parent is None:
            parent = glob_functions.getMainWin()
        spravs = self.getContainer().getAll().values()
        choice_str = [sprav.name+u' - '+sprav.description if sprav.description else u'' for sprav in spravs]
        idx = dlgfunc.getSingleChoiceIdxDlg(parent, title, prompt_text, choice_str)
        if idx >= 0:
            edit_sprav = spravs[idx]
            log.info(u'Редактирование справочника: %d %s' % (idx, edit_sprav.name))
            try:
                edit_sprav.edit(parent=parent)
            except icexceptions.MethodAccessDeniedException:
                wx.MessageBox(u'У пользователя [%s] нет прав на редактирвоние справочников.' % ic.getCurUserName())

    def editSprav(self, sprav_name, parent=None):
        """
        Вызов редактирования справочника по имени.
        @param sprav_name: Имя справочника.
        @param parent: Родительское окно для формы редактирования справочника.
        """
        if parent is None:
            parent = glob_functions.getMainWin()

        edit_sprav = self.getSpravByName(sprav_name)
        if edit_sprav:
            return edit_sprav.Edit(ParentForm_=parent)
        else:
            log.warning(u'Справочник <%s> не найден в менеджере <%s>' % (sprav_name, self.name))
        return None

    def choiceSprav(self, sprav_name, parent=None, default_selected_code=None):
        """
        Вызов выбора значения справочника по имени.
        @param sprav_name: Имя справочника.
        @param parent: Родительское окно для формы редактирования справочника.
        @param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        @return: Функция возвращает выбранный код справочника
            или None в случае ошибки или если нажата кнопка <Отмена>.
        """
        if parent is None:
            parent = glob_functions.getMainWin()

        choice_sprav = self.getSpravByName(sprav_name)
        if choice_sprav:
            result = choice_sprav.Choice(parentForm=parent,
                                         default_selected_code=default_selected_code)
            if result[0] == coderror.IC_CTRL_OK:
                return result[1]
        else:
            log.warning(u'Справочник <%s> не найден в менеджере <%s>' % (sprav_name, self.name))
        return None


def test():
    """
    Тестовая функция.
    """
    sprav_manager = icSpravManagerPrototype()
    sprav_manager.Months.Hlp()


if __name__ == '__main__':
    test()
