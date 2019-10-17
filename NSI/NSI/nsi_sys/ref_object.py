#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс объекта-ссылки/справочника.

Объект-ссылка отличается от справочника тем что
организует свое хранение в виде каскада таблиц уровней.

На каждом уровне таблица содержит поля code и status.
code - код объекта-ссылки/справочника.
status - вкл./выкл. объекта.
"""

from ic.components import icwidget

from ic.log import log
from ic.utils import system_cache
from ic.engine import glob_functions
from ic.dlg import dlgfunc
from ic.utils import coderror

from . import icsprav
from ..nsi_dlg import icspraveditdlg
from ..nsi_dlg import icspravchoicetreedlg

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_REFOBJECT = {'type': 'RefObject',
                    'name': 'default',
                    'description': '',      # Описание справочника

                    'db': None,             # Паспорт БД хранения данных
                    'cache': True,          # Автоматически кэшировать?
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    '__attr_hlp__': {'db': u'Паспорт БД хранения данных',
                                     'cache': u'Автоматически кэшировать?',
                                     },
                    }


class icRefObjectProto(icsprav.icSpravInterface):
    """
    Класс объекта-ссылки/справочника.
    """

    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.
        @param sprav_manager: Объект менеджера справочника.
        @param name: Имя справочника в списке менеджера справочников.
        """
        icsprav.icSpravInterface.__init__(self, sprav_manager, name)

        # Кэш
        self._cache = system_cache.icCache()

    def Edit(self, parent_code=(None,), parent=None):
        """
        Запуск окна редактирования объекта-ссылки/справочника.
        @param parent_code: Код более верхнего уровня.
        @param parent: Родительская форма.
            Если не определена, то берется главная форма.
        @return: Возвращает результат выполнения опереции True/False.
        """
        # Перед редактированием необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self.createLevelTabRes()

        if parent is None:
            parent = glob_functions.getMainWin()

        try:
            return icspraveditdlg.edit_sprav_dlg(parent=parent, nsi_sprav=self)
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка редактирования' % self.name)
            return False

    def getLevels(self):
        """
        Список уровней объекта-ссылки/справочника.
        """
        log.warning(u'Не определен метод получения списка уровней объекта-ссылки/справочника в <%s>' % self.__class__.__name__)
        return list()

    def getLevel(self, level_id=0):
        """
        Получить уровень объекта-ссылки/справочника.
        @param level_id: Идентификатор уровня.
            Может быть как индексом так и наменованием уровня.
        @return: Объект уровня или None если уровень не найден.
        """
        levels = self.getLevels()
        if isinstance(level_id, int):
            # Идентификатор уровня задается индексом
            if 0 <= level_id < len(levels):
                return levels[level_id]
        elif isinstance(level_id, str):
            # Идентификатор уровня задается как имя
            level_names = [level.getName() for level in levels]
            if level_id in level_names:
                level_idx = level_names.index(level_id)
                return levels[level_idx]
        return None

    def createLevelTabRes(self):
        """
        Создать все ресурсы таблиц всех уровней объекта-ссылки/справочника.
        @return: True/False.
        """
        levels = self.getLevels()
        if levels:
            for level in levels:
                level.genTableRes()
            return True
        return False

    def getTable(self, index=0):
        """
        Таблица объекта-ссылки.
        Считаем что это таблица уровня.
        @param index: Индекс уровня объекта-ссылки.
            Если не определен, то берется первый уровень.
        """
        levels = self.getLevels()
        if levels:
            try:
                return levels[index].getTable()
            except IndexError:
                log.fatal(u'Ошибка получения таблицы объекта-ссылки/справочника <%s>' % self.getName())
        return None

    def Hlp(self, parent_code=(None,), field=None, form=None, parent=None, dt=None,
            default_selected_code=None, view_fields=None, search_fields=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного объекта-ссылки/справочника.
        @type parent_code: C{...}
        @param parent_code: Код более верхнего уровня.
        @param field: Задает поле или группу полей, которые надо вернуть.
            Полу задается строкой. Поля задаются словарем.
        @param form: имя формы визуального интерфейса работы со справочником.
        @param parent: Родительская форма.
        @type dt: C{string}
        @param dt: Время актуальности кода.
        @param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        @param view_fields: Список имен полей для просмотра.
            Если не определено то отображаются <Код> и <Наименование>.
        @param search_fields: Список имен полей для поиска.
            Если не определено то поиск только по <Код> и <Наименование>.
        @return: Код ошибки, Результат выбора
        """
        result = coderror.IC_HLP_OK
        res_val = None

        try:
            if parent_code is None:
                parent_code = (None,)

            # Для обработки необходимо преобразовать в список
            parent_code = list(parent_code)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике
            if self.getLevelCount() <= x_level:
                log.warning(u'Не корректный номер уровня %d' % x_level)
                return coderror.IC_HLP_FAILED_LEVEL, res_val

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
                return coderror.IC_HLP_FAILED_LEVEL, res_val

            # Обработка штатной функцией
            code = icspravchoicetreedlg.choice_sprav_dlg(parent=parent,
                                                         nsi_sprav=self,
                                                         fields=view_fields,
                                                         default_selected_code=default_selected_code,
                                                         search_fields=search_fields)
            if code:
                return coderror.IC_HLP_OK, code, self.getFields(field, code)
            return coderror.IC_HLP_FAILED_IGNORE, code, None
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка в методе Hlp/Choice' % self._name)
            result = coderror.IC_HLP_FAILED_TYPE_SPRAV

        return result, res_val, self.getFields(field, res_val)

    # Другое название метода (я считаю что более правильное)
    Choice = Hlp

