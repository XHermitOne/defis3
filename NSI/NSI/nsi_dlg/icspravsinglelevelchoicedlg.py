#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог выбора кода из одного уровня справочника.
"""

import wx

from ic.log import log
from ic.dlg import dlgfunc
from ic.utils import ic_util
from ic.engine import glob_functions

__version__ = (0, 1, 1, 1)


def select_single_level_choice_dlg(parent=None, sprav=None, n_level=0, parent_code=None):
    """
    Вызвать диалог выбора кода из одного уровня справочника.
    @param parent: Родительское окно диалогового окна.
        Если не определено, то берется главное окно приложения.
    @param sprav: Объект справочника, из которого производится выбор.
        Может задаваться паспортом объекта или непосредственно объектом.
    @param n_level: Индекс уровня с которого производится выбор.
        Задается начиная с 0.
    @param parent_code: Родительский код для детализации значений уровня.
        Если не определен, то считается что это самый первый уровень.
    @return: Выбранный код или None, если нажата <Отмена>.
    """
    if ic_util.is_pasport(sprav):
        # Справочник задается паспортом. Необходимо создать объект
        sprav = glob_functions.getKernel().Create(sprav)

    if sprav is None:
        log.warning(u'Не определен объект справочника для выбора')
        return None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    selected_code = None
    try:
        sprav_storage = sprav.getStorage()
        level_table = sprav_storage.getLevelTable(parent_code) if sprav_storage else list()
        level = sprav.getLevelByIdx(n_level)
        records = [sprav_storage.record_tuple2record_dict(rec) for rec in level_table]
        choices = [rec.get('name', u'-')for rec in records]

        select_idx = dlgfunc.getSingleChoiceIdxDlg(parent, sprav.getDescription(), level.getDescription(), choices)
        if select_idx >= 0:
            selected_code = records[select_idx].get(sprav_storage.getCodeFieldName(), None)
        return selected_code
    except:
        log.fatal(u'Ошибка выбора кода из одного уровня справочника.')
    return None
