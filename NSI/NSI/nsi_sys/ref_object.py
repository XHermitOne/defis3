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
