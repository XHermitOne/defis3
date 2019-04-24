#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговая форма тестирования OLAP сервера Cubes.
"""

import keyword

import wx
import wx.stc
from . import cubes_olap_srv_test_dlg

from ic.log import log
from ic.utils import ic_util

__version__ = (0, 1, 1, 1)

FUNCTIONS = ('aggregate', )


class icCubesOLAPSrvTestDialog(cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto):
    """
    Диалоговая форма тестирования OLAP сервера Cubes.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        cubes_olap_srv_test_dlg.icCubesOLAPSrvTestDialogProto.__init__(self, *args, **kwargs)

        # Настройка обозревателя кода
        self.json_scintilla.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.json_scintilla.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.json_scintilla.SetProperty('fold', '1')
        self.json_scintilla.SetProperty('tab.timmy.whinge.level', '1')
        self.json_scintilla.SetMargins(0, 0)

        # Не видеть пустые пробелы в виде точек
        self.json_scintilla.SetViewWhiteSpace(False)

        # Установить ширину 'таба'
        # Indentation and tab stuff
        self.json_scintilla.SetIndent(4)                 # Proscribed indent size for wx
        self.json_scintilla.SetIndentationGuides(True)   # Show indent guides
        self.json_scintilla.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.json_scintilla.SetTabIndents(True)          # Tab key indents
        self.json_scintilla.SetTabWidth(4)               # Proscribed tab size for wx
        self.json_scintilla.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Установка поле для захвата маркеров папки
        self.json_scintilla.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.json_scintilla.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.json_scintilla.SetMarginSensitive(1, True)
        self.json_scintilla.SetMarginSensitive(2, True)
        self.json_scintilla.SetMarginWidth(1, 25)
        self.json_scintilla.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,    'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Маркеры режима отладки
        # self.json_scintilla.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        # self.json_scintilla.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')

        self.func_choice.AppendItems(FUNCTIONS)
        self.func_choice.SetSelection(0)

        # Тестируемый OLAP сервер
        self._OLAP_server = None

    def setOLAPServer(self, olap_server):
        """
        Установить тестируемый OLAP сервер.
        @param olap_server: OLAP сервер
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            # Настраиваем контрол выбора кубов
            choices = [cube.description if cube.description else cube.name for cube in self._OLAP_server.getCubes()]
            self.cube_choice.Clear()
            self.cube_choice.AppendItems(choices)
            if choices:
                self.cube_choice.SetSelection(0)

    def onCloseButtonClick(self, event):
        """
        Обработчик кнопки ЗАКРЫТЬ.
        """
        self.EndModal(wx.ID_CLOSE)
        event.Skip()

    def onRefreshButtonClick(self, event):
        """
        Обработчик кнопки ОБНОВИТЬ.
        """
        if self._OLAP_server:
            i_cube = self.cube_choice.GetSelection()
            cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
            i_func = self.func_choice.GetSelection()
            func_name = FUNCTIONS[i_func] if i_func >= 0 else None
            result = None
            if cube and func_name:
                result = self._OLAP_server.get_response(cube_name=cube.getName(), func_name=func_name)
            else:
                if not cube:
                    log.warning(u'Не определен куб для отображения')
                if not func_name:
                    log.warning(u'Не определена функция для отображения')

            # self.json_scintilla.SetText(str(result))
            self.json_scintilla.ClearAll()
            self.json_scintilla.AddText(ic_util.StructToTxt(result))

        event.Skip()


def show_cubes_olap_srv_test_dlg(parent=None, olap_srv=None):
    """
    Отобразить окно тестирования OLAP сервера Cubes.
    @param parent: Родительское окно.
        Если не определено, то берется самое главное окно.
    @param olap_srv: Тестируемый OLAP сервер.
    @return: True/False.
    """
    if olap_srv is None:
        log.warning(u'Не определен объект OLAP сервера для тестирования')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Запускаем OLAP сервер
        olap_srv.run()

        dlg = icCubesOLAPSrvTestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)

        dlg.ShowModal()
        return True
    except:
        log.fatal(u'Ошибка отображения окна тестирования OLAP сервера Cubes.')
    return False