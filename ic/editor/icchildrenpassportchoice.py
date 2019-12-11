#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалогового окна выбора паспорта дочернего объекта.
"""

from ic.log import log
from ic.dlg import dlgfunc


__version__ = (0, 1, 1, 1)


def open_children_passport_choice_dlg(parent=None, parent_obj=None, include=None, exclude=None):
    """
    Выбор паспорта дочернего объекта.

    :param parent: Ссылка на окно.
    :param parent_obj: Компонент родительского объекта.
    :param include: Список имен включенных в список выбора дочерних компонентов.
        Если не определен, то беруться все доверние компоненты.
    :param exclude: Список имен исключенных из списка выбора дочерних компонентов.
        Если не определен, то беруться все доверние компоненты.
    :return: Возвращает список паспорта выбранного объекта или None в случае ошибки.
    """
    if parent_obj is None:
        msg = u'Не определен компонент родительского объекта для выбора паспорта дочернего объекта'
        log.warning(msg)
        dlgfunc.openWarningBox(u'ОШИБКА', msg)
        return None

    # Получить список имен дочерних объектов
    children = parent_obj.get_children_lst()
    children_names = [child.getName() for child in children]
    # Дополнительная фильтрация
    if include:
        # Отфильтровываем включенные в список дочерние компоненты
        children_names = [child_name for child_name in children_names if child_name in include]
    if exclude:
        # Отфильтровываем исключенные из списка дочерние компоненты
        children_names = [child_name for child_name in children_names if child_name not in exclude]

    # Вызов диалогового окна выбора
    selected_idx = dlgfunc.getSingleChoiceIdxDlg(parent=parent,
                                                 title=u'ПАСПОРТ ОБЪЕКТА',
                                                 prompt_text=u'Выберите компонент:',
                                                 choices=children_names)
    if selected_idx >= 0:
        # Получаем список дочерних объектов по списку имен
        selected_name = children_names[selected_idx]
        selected_child = parent_obj.GetChildByName(selected_name)
        selected_passport = selected_child.GetPassport()
        return selected_passport
    return None
