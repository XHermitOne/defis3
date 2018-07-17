#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит описание класса IEHtmlPanel, который отображае HTML текст в окне.

@type SPC_IC_IE_HTML: C{dictionary}
@var SPC_IC_IE_HTML: Спецификация на ресурсное описание :

    - B{type='IEHtmlWindow'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{file='about:blank'}: Адресс html файла для отображения.

"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.utils.util import icSpcDefStruct
from ic.utils.util import ic_eval
from ic.imglib import common
from .icwidget import icWidget,  SPC_IC_WIDGET

_ = wx.GetTranslation

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin

SPC_IC_IE_HTML = {'type': 'IEHtmlWindow',
                  'name': 'default',
                  'file': 'about:blank',

                  '__parent__': SPC_IC_WIDGET,
                  }

__version__ = (0, 0, 0, 2)


class icIEHtmlPanel(icWidget, wx.Window):
    """
    Html браузер.
    """
    def __init__(self, parent, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        icSpcDefStruct(SPC_IC_IE_HTML, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        wx.Window.__init__(self, parent, -1, size=(400, -1),
                           style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.current = component['file']
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ie = iewin.IEHtmlWindow(self, -1)
        
        self.toolbar = wx.ToolBar(self, wx.NewId(), size=(-1, 27))
        self.toolbar.SetToolBitmapSize(wx.Size(16, 16))
        
        id_prev = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgGoPrevPage, id=id_prev, shortHelpString=_('Prev page'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnPrevPageButton, id=id_prev)

        id_next = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgGoNextPage, id=id_next, shortHelpString=_('Next page'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnNextPageButton, id=id_next)
        
        id_next = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgGoHomePage, id=id_next, shortHelpString=_('Home page'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnHomeButton, id=id_next)

        id_next = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgRefreshPage, id=id_next, shortHelpString=_('Refresh'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnRefreshPageButton, id=id_next)

        id_next = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgStopPage, id=id_next, shortHelpString=_('Stop'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnStopButton, id=id_next)

        id_next = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgSearchPage, id=id_next, shortHelpString=_('Search'))
        self.toolbar.Bind(wx.EVT_TOOL, self.OnSearchPageButton, id=id_next)

        self.toolbar.AddSeparator()
        txt = wx.StaticText(self.toolbar, -1, _('Place:'))
        self.toolbar.AddControl(txt)
        
        self.location = wx.ComboBox(self.toolbar, wx.NewId(), '', size=(300, -1), style=wx.CB_DROPDOWN | wx.PROCESS_ENTER)
        self.toolbar.AddControl(self.location)
        
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, id=self.location.GetId())
        self.Bind(wx.EVT_KEY_UP, self.OnLocationKey, self.location)
        self.Bind(wx.EVT_CHAR, self.IgnoreReturn, self.location)

        self.toolbar.Realize()

        sizer.Add(self.toolbar, 0, wx.ALIGN_TOP | wx.ALIGN_LEFT | wx.EXPAND)
        sizer.Add(self.ie, 1, wx.GROW | wx.EXPAND)

        self.ie.Navigate(self.current)
        self.location.Append(self.current)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(iewin.EVT_BeforeNavigate2, self.OnBeforeNavigate2, self.ie)
        self.Bind(iewin.EVT_NewWindow2, self.OnNewWindow2, self.ie)
        self.Bind(iewin.EVT_DocumentComplete, self.OnDocumentComplete, self.ie)
        self.Bind(iewin.EVT_StatusTextChange, self.OnStatusTextChange, self.ie)
        self.Bind(iewin.EVT_TitleChange, self.OnTitleChange, self.ie)
        self.BindICEvt()

    def ShutdownDemo(self):
        pass

    def OnSize(self, evt):
        self.Layout()

    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.ie.Navigate(url)

    def OnLocationKey(self, evt):
        if evt.KeyCode() == wx.WXK_RETURN:
            URL = self.location.GetValue()
            self.location.Append(URL)
            self.ie.Navigate(URL)
        else:
            evt.Skip()

    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, 'Open Location',
                                 'Enter a full URL or local path',
                                 self.current, wx.OK | wx.CANCEL)
        dlg.CentreOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.ie.Navigate(self.current)
        dlg.Destroy()

    def OnHomeButton(self, event):
        self.ie.GoHome()    # ET Phone Home!

    def OnPrevPageButton(self, event):
        self.ie.GoBack()

    def OnNextPageButton(self, event):
        self.ie.GoForward()

    def OnStopButton(self, evt):
        self.ie.Stop()

    def OnSearchPageButton(self, evt):
        self.ie.GoSearch()

    def OnRefreshPageButton(self, evt):
        self.ie.Refresh(iewin.IEHTML_REFRESH_COMPLETELY)

    def logEvt(self, name, event):
        pass

    def OnBeforeNavigate2(self, evt):
        self.logEvt('OnBeforeNavigate2', evt)
        
    def OnNewWindow2(self, evt):
        self.logEvt('OnNewWindow2', evt)
        evt.Veto()  # don't allow it

    def OnDocumentComplete(self, evt):
        self.logEvt('OnDocumentComplete', evt)
        self.current = evt.URL
        try:
            self.location.SetValue(self.current)
        except:
            pass

    def OnTitleChange(self, evt):
        self.logEvt('OnTitleChange', evt)

    def OnStatusTextChange(self, evt):
        self.logEvt('OnStatusTextChange', evt)


def startMiniHtmlBrows(fileDoc=None):
    frame = wx.MiniFrame(None, -1, _('Help'), size=(520, 600),
                         style=wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ)
    if fileDoc:
        win = icIEHtmlPanel(frame, {'file': fileDoc})
    else:
        win = icIEHtmlPanel(frame, {})
    frame.SetSize((535, 600))
    frame.CentreOnScreen(wx.BOTH)
    frame.Show(True)
    return win


def test(par=0):
    """
    Тестируем класс icIEHtmlPanel.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    common.img_init()
    frame = wx.Frame(None, -1, 'HTML Window', pos=(300, 50),
                     size=(500, 500), style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN)

    if wx.Platform == '__WXMSW__':
        startMiniHtmlBrows('')
    else:
        dlg = wx.MessageDialog(frame, 'This only works on MSW.',
                               'Sorry', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
