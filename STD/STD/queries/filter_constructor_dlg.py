#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно конструктора фильтров.
"""

import wx

from ic.bitmap import bmpfunc
from ic.log import log

try:
    from . import filter_constructor
except:
    filter_constructor = None

try:
    from . import filter_builder_env
except:
    filter_builder_env = None

__version__ = (0, 1, 1, 2)


def get_filter_constructor_dlg(parent=None, default_filter_data=None, env=None):
    """
    Функция вызова диалогового окна конструктора фильтров.
    @param parent: Родительское окно диалога конструктора фильтров.
    @param default_filter_data: Фильтр по умолчанию.
    @param env: Окружение работы конструктора фильтров.
    """
    if env is None:
        log.warning(u'Не определено окружение для конструктора фильтров')

        # Окружение должно быть обязательно
        try:
            env = filter_builder_env.FILTER_ENVIRONMENT
        except:
            from . import filter_builder_env
            env = filter_builder_env.FILTER_ENVIRONMENT

    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icFilterConstructorDialog(parent, default_filter_data, env)
        if dlg.ShowModal() in (wx.ID_OK,):
            result = dlg.getFilterData()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                parent.Destroy()
            return result
    except:
        log.fatal(u'Ошибка конструктора фильтра')

    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()

    return None


class icFilterConstructorDialog(wx.Dialog):
    """
    Диалоговое окно конструктора фильтров.
    """

    def __init__(self, parent, default_filter_data=None, env=None):
        """
        Конструктор.
        """
        try:
            _title = u'Конструктор фильтров'

            wx.Dialog.__init__(self, parent, -1, title=_title,
                               style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                               pos=wx.DefaultPosition, size=wx.Size(900, 400))

            # Определение иконки диалогового окна
            icon = None
            try:
                icon_img = bmpfunc.createLibraryBitmap('filter_advanced.png')
            except:
                icon_img = bmpfunc.getSysImg('imgFilter')
            if icon_img:
                icon = wx.Icon(icon_img)
            if icon:
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)

            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.onOK, id=id_)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.onCancel, id=id_)

            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            global filter_constructor
            if filter_constructor is None:
                from . import filter_constructor

            self._filter_constructor_ctrl = filter_constructor.icFilterConstructorTreeList(self)

            if env:
                # Устанивить окружение работы конструктора фильтров
                self._filter_constructor_ctrl.setEnvironment(env)

            # Если надо то установить редатируемый список паспортов
            if default_filter_data:
                self._filter_constructor_ctrl.setFilterData(default_filter_data)
            else:
                self._filter_constructor_ctrl.setDefault()

            self._boxsizer.Add(self._filter_constructor_ctrl, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна конструктора фильтров')

    def onOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self.EndModal(wx.ID_CANCEL)

    def getFilterData(self):
        """
        Данные фильтра.
        """
        if self._filter_constructor_ctrl:
            return self._filter_constructor_ctrl.getFilterData()
        return None


def test(parent=None):
    """
    Функция тестирования.
    """
    print('TEST ... START')
    app = wx.PySimpleApp()

    import copy
    from ic.log import log
    import ic.config
    from . import filter_builder_env

    log.init(ic.config)

    env = filter_builder_env.FILTER_ENVIRONMENT
    env['requisites'] = []

    requisite1 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite1['name'] = 'Name'
    requisite1['description'] = u'Название'
    requisite1['type'] = filter_builder_env.REQUISITE_TYPE_STR
    requisite1['funcs'] = list(filter_builder_env.DEFAULT_STRING_FUNCS)
    env['requisites'].append(requisite1)

    requisite2 = copy.deepcopy(filter_builder_env.FILTER_REQUISITE)
    requisite2['name'] = 'Cost'
    requisite2['description'] = u'Цена'
    requisite1['type'] = filter_builder_env.REQUISITE_TYPE_FLOAT
    requisite2['funcs'] = list(filter_builder_env.DEFAULT_NUMBER_FUNCS)
    env['requisites'].append(requisite2)

    default_filter = {'name': 'AND', 'type': 'group', 'children': [{'requisite': 'Name',
                                                                    'type': 'compare', 'arg_1': u'qweer',
                                                                    'func': 'equal',
                                                                    '__sql__': ('name', '=', 'qweer')},
                                                                   {'requisite': 'Cost', 'type': 'compare',
                                                                    'arg_1': u'1000', 'func': 'lesser',
                                                                    '__sql__': ('cost', '<', '1000')}], 'logic': 'AND'}

    result = get_filter_constructor_dlg(parent, default_filter_data=default_filter, env=env)
    print('TEST ... RESULT:', result)
    app.MainLoop()
    print('TEST ... STOP')


if __name__ == '__main__':
    test()
