#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно конструктора фильтров.
"""

# Version
__version__ = (0, 0, 0, 1)

# Imports
import wx
from ic.kernel import io_prnt
from ic.bitmap import ic_bmp
try:
    from . import filter_constructor
except:
    filter_constructor = None

try:
    from . import filter_builder_env
except:
    filter_builder_env = None

def icFilterConstructorDlg(ParentWin_=None, DefaultFilterData_=None, Env_=None):
    """
    Функция вызова диалогового окна конструктора фильтров.
    @param ParentWin_: Родительское окно диалога конструктора фильтров.
    @param DefaultFilterData_: Фильтр по умолчанию.
    @param Env_: Окружение работы конструктора фильтров.
    """
    if Env_ is None:
        io_prnt.outWarning(u'Не определено окружение для конструктора фильтров')

        # Окружение должно быть обязательно
        try:
            Env_ = filter_builder_env.FILTER_ENVIRONMENT
        except:
            from . import filter_builder_env
            Env_ = filter_builder_env.FILTER_ENVIRONMENT

    dlg = None
    try:
        win_clear = False
        if ParentWin_ is None:
            id_ = wx.NewId()
            ParentWin_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icFilterConstructorDialog(ParentWin_, DefaultFilterData_, Env_)
        if dlg.ShowModal() in (wx.ID_OK,):
            result = dlg.getFilterData()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                ParentWin_.Destroy()
            return result

    except:
        io_prnt.outLastErr(u'Ошибка конструктора фильтра')

    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           ParentWin_.Destroy()

    return None


class icFilterConstructorDialog(wx.Dialog):
    """
    Диалоговое окно конструктора фильтров.
    """

    def __init__(self, parent, DefaultFilterData_=None, Env_=None):
        """
        Конструктор.
        """
        try:
            _title = u'Конструктор фильтров'
            
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent, -1, title=_title,
                       style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                       pos=wx.DefaultPosition, size=wx.Size(900, 400))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            # Определение иконки диалогового окна
            icon = None
            try:
                from ic.imglib import newstyle_img
                icon_img = newstyle_img.data_filter
            except:
                icon_img = ic_bmp.getSysImg('imgFilter')
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
            if icon:
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)
            
            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
            
            # Кнопка -OK-
            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.OnOK, id=id_)
            # Кнопка -Отмена-
            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Отмена', size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id=id_)

            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            global filter_constructor
            if filter_constructor is None:
                from . import filter_constructor

            self._filter_constructor_ctrl = filter_constructor.icFilterConstructorTreeList(self)

            if Env_:
                # Устанивить окружение работы конструктора фильтров
                self._filter_constructor_ctrl.setEnvironment(Env_)
                
            # Если надо то установить редатируемый список паспортов
            if DefaultFilterData_:
                self._filter_constructor_ctrl.setFilterData(DefaultFilterData_)
            else:
                self._filter_constructor_ctrl.setDefault()
            
            self._boxsizer.Add(self._filter_constructor_ctrl, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            io_prnt.outErr(u'Ошибка создания объекта диалогового окна конструктора фильтров')
        
    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
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
    
    result = icFilterConstructorDlg(parent, DefaultFilterData_=default_filter, Env_=env)
    print('TEST ... RESULT:', result)
    app.MainLoop()
    print('TEST ... STOP')

if __name__ == '__main__':
    test()
