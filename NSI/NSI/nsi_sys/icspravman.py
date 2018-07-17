#!/usr/bin/env python
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
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.kernel import icexceptions
from ic.engine import ic_user

# Версия
__version__ = (0, 0, 1, 1)


# Константы
# Имя справочной системы по умолчанию
DEFAULT_NSI_SPRAV_NAME = 'nsi_sprav'


class icSpravManagerContainer(object):
    """
    Контейнер справочников.
        Контейнер справочников необходим для организации доступа к
        справочникам ч/з точку из менеджера справочников.
    """

    def __init__(self, ParentSpravManager_):
        """
        Конструктор.

        """
        self._parent = ParentSpravManager_
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

    def setSprav(self, Sprav_=None):
        """
        Установить справочник/перечисление.
        """
        if Sprav_:
            self._all[Sprav_.name] = Sprav_
            self._all[Sprav_.name]._sprav_manager = self._parent

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

    def getSpravByName(self, SpravName_):
        """
        Получить справочник по имени.
        @param SpravName_: Имя справочника.
        """
        return self._container.getSpravByName(SpravName_)

    def __nonzero__(self):
        """
        Провера на не 0.
        """
        return type(self) != type(None)

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

    def Admin(self, ParentForm_=None,
              Title_=u'Администрирование справочников',
              MsgTxt_=u'Выберите справочник для редактирования:'):
        """
        Администрирование справочной системы, описываемой данным менеджером.
        @param ParentForm_: Родительское окно для формы редактирования справочника.
        """
        if ParentForm_ is None:
            ParentForm_ = ic_user.icGetMainWin()
        spravs = self.getContainer().getAll().values()
        choice_str = [sprav.name+u' - '+sprav.description if sprav.description else u'' for sprav in spravs]
        idx = ic_dlg.icSingleChoiceIdxDlg(ParentForm_, Title_, MsgTxt_, choice_str)
        if idx >= 0:
            edit_sprav = spravs[idx]
            log.info(u'Редактирование справочника: %d %s' % (idx, edit_sprav.name))
            try:
                edit_sprav.Edit(ParentForm_=ParentForm_)
            except icexceptions.MethodAccessDeniedException:
                wx.MessageBox(u'У пользователя [%s] нет прав на редактирвоние справочников.' % ic.getCurUserName())

    def EditSprav(self, SpravName_, ParentForm_=None):
        """
        Вызов редактирования справочника по имени.
        @param SpravName_: Имя справочника.
        @param ParentForm_: Родительское окно для формы редактирования справочника.
        """
        if ParentForm_ is None:
            ParentForm_ = ic_user.icGetMainWin()

        edit_sprav = self.getSpravByName(SpravName_)
        if edit_sprav:
            return edit_sprav.Edit(ParentForm_=ParentForm_)
        else:
            log.warning(u'Справочник <%s> не найден в менеджере <%s>' % (SpravName_, self.name))
        return None

    def ChoiceSprav(self, SpravName_, ParentForm_=None, default_selected_code=None):
        """
        Вызов выбора значения справочника по имени.
        @param SpravName_: Имя справочника.
        @param ParentForm_: Родительское окно для формы редактирования справочника.
        @param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        @return: Функция возвращает выбранный код справочника
            или None в случае ошибки или если нажата кнопка <Отмена>.
        """
        if ParentForm_ is None:
            ParentForm_ = ic_user.icGetMainWin()

        choice_sprav = self.getSpravByName(SpravName_)
        if choice_sprav:
            result = choice_sprav.Choice(parentForm=ParentForm_,
                                         default_selected_code=default_selected_code)
            if result[0] == coderror.IC_CTRL_OK:
                return result[1]
        else:
            log.warning(u'Справочник <%s> не найден в менеджере <%s>' % (SpravName_, self.name))
        return None


def test():
    """
    Тестовая функция.
    """
    sprav_manager = icSpravManagerPrototype()
    sprav_manager.Months.Hlp()


if __name__ == '__main__':
    test()
