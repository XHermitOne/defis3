#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса HtmlWindow.
Модуль содержит класс icHtmlPanel, который по ресурсному описанию создает компонент для отображения html-текста.
Для корректной работы класса html.HtmlWindow с русскими буквами требуется запись в реестре.
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage 1252=c_1251.nls

@type SPC_IC_HTML_PANEL: C{dictionary}
@var SPC_IC_HTML_PANEL: Спецификация на ресурсное описание компонента. Ключи SPC_IC_HTML_PANEL:

    - B{name = 'default'}: Имя окна.
    - B{type = 'HtmlPanel'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}:Цвет фона.
    - B{style=wx.HW_SCROLLBAR_AUTO}:Стиль окна. Используются все стили класса wxWindow.
    - B{file=None}:Html файл, который будет отображаться в окне.

@type ICHtmlPanelStyle: C{dictionary}
@var ICHtmlPanelStyle: Словарь стилей компонента. Описпание ключей ICHtmlPanelStyle:

    - C{wx.html.HW_SCROLLBAR_NEVER}: Окно без вертикального скролирования.
    - C{wx.html.HW_SCROLLBAR_AUTO}: C вертикальным скролированием.
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.utils.util import icSpcDefStruct
from ic.utils.util import ic_eval
from wx import html
from .icwidget import icWidget, SPC_IC_WIDGET

_ = wx.GetTranslation

SPC_IC_HTML_PANEL = {'type':'Panel',
                     'name':'defaultWindow',

                     'position':(-1,-1),
                     'size':(-1,-1),
                     'foregroundColor':None,
                     'backgroundColor':None,
                     'file': None,
                     'style': html.HW_SCROLLBAR_AUTO,

                     '__parent__': SPC_IC_WIDGET,
                     }

__version__ = (0, 0, 0, 2)


class icHtmlPanel(icWidget, wx.Panel):
    """
    Интерфейс для создания окна класса wxPanel
    через ресурсное описание.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icHtmlPanel.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        #   Атрибуты сайзера
        self.sizer = None
        self.bSizerAdd = False
        icSpcDefStruct(SPC_IC_HTML_PANEL, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        pos = component['position']
        size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        self.source = component['file']

        wx.Panel.__init__(self, parent, id, pos, size,
                          style=style, name=self.name)
        hwin = html.HtmlWindow(self, -1)
        
        if self.source not in [None, '', 'None']:
            hwin.LoadPage(self.source)
        
        if fgr is not None:
            hwin.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            hwin.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hwin, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.BindICEvt()

    def DestroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except:
                    pass
        except:
            pass


def test(par=0):
    """
    Тестируем класс icHtmlPanel.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icHtmlPanel Test')
    win = icHtmlPanel(frame, -1, {'file': 'C:\Python22\epydoc\html\ic.components.icgrid.html',
                                   'keyDown': 'print(\'keyDown in icHtmlPanel\')'})
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test()
