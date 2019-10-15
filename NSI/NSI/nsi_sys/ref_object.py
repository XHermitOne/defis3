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
        if parent is None:
            parent = glob_functions.getMainWin()

        try:
            return icspraveditdlg.edit_sprav_dlg(parent=parent, nsi_sprav=self)
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка редактирования' % self.name)
            return False
