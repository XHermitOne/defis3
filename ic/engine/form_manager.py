#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного WX окна.
"""

# Подключение библиотек
import os
import os.path

from ic import config
from ic.engine import ic_user
from ic.utils import resfunc
from ic.utils import formdatamanager

from . import panel_manager
from . import stored_ctrl_manager


__version__ = (1, 1, 2, 1)


class icFormManager(formdatamanager.icFormDataManager,
                    panel_manager.icPanelManager,
                    stored_ctrl_manager.icStoredCtrlManager):
    """
    Менеджер WX окна.
    ВНИМАНИЕ! Для того чтобы пользоваться менеджером
    имена контролов должны совпадат с именами словаря заполнения.
    Т.е. если в словаре заполнения используются имена реквизитов
    объекта, то имена контролов их обрабатывающих должны быть такими
    же как имена реквизитов объекта.
    Основные методы:
        set_form_data|set_ctrl_data - расстановка значений в контролы диалогового окна.
        get_form_data|get_ctrl_data - получение значений из контролов диалогового окна.
        save_dlg|save_ctrl - сохранение позиций и размеров динамических контролов диалогового окна.
        load_dlg|load_ctrl - загрузка позиций и размеров динамических контролов диалогового окна.
    """
    # Другое наименование метода
    get_form_data = panel_manager.icPanelManager.get_ctrl_data
    # Другое наименование метода
    set_form_data = panel_manager.icPanelManager.set_ctrl_data

    def save_dlg(self):
        """
        Сохранить позиции и размеры динамических контролов для
        последующего их востановления.
        Принцип такой: Пользователь может менять размеры окон,
        положение и размер сплиттеров и т.п.
        Этой функцией по закрытию происходит сохранение
        в локальную папку профиля.
        При открытии окна с помощью метода <load_dlg>
        происходит восстановление сохраненных параметров.
        @return: True/False.
        """
        # Определить имя файла для хранения данных
        res_filename = os.path.join(config.PROFILE_DIRNAME,
                                    ic_user.getPrjName(),
                                    self.__class__.__name__)
        data = self._getCtrlData()
        return resfunc.SaveResourcePickle(res_filename, data)

    # Другое наименование метода
    save_ctrl = save_dlg

    def load_dlg(self):
        """
        Загрузить позиции и размеры динамических контролов окна.
        @return: True/False.
        """
        res_filename = os.path.join(config.PROFILE_DIRNAME,
                                    ic_user.getPrjName(),
                                    self.__class__.__name__)
        data = resfunc.LoadResourcePickle(res_filename)
        return self._setCtrlData(data)

    # Другое наименование метода
    load_ctrl = load_dlg
