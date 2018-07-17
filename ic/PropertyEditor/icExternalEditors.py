#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Внешние редакторы свойств.
"""

import wx
import string
import wx.grid as Grid
from . import icDefInf
import ic.components.icfont as icfont
import wx.lib.dialogs
from . import ic_pyed
from ic.utils import ic_uuid


class icBaseEdt:
    """
    Базовый класс внешнего редактора редактора.
    """
    def __init__(self, parent, value, pos, size, style):
        """
        """
        
    def HlpDlg(self, parent, value, pos, size, style):
        """
        Функция запускает внешний редактор.
        """
        
    def Ctrl(self, value):
        """
        Функция контроля значения.
        """
    
    def Draw(self, dc):
        """
        Функция отрисовки значения данного типа в режиме просмотра. 
        """
    
    def strToVal(self, text):
        """
        Функция преобразования строки в значение ресурса.
        """


def ColorEdtDlg(parent, value):
    """
    Диалог выбора цвета.
    
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type value: C{string}
    @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
    @return: Возвращет выбранный цвет в виде строки 'wx.Colour(r,g,b)'.
    """
    dlg = wx.ColourDialog(parent)
    dlg.GetColourData().SetChooseFull(True)

    if value:
        clr = eval(value)
    else:
        clr = None

    if clr is not None:
        dlg.GetColourData().SetColour(clr)
    else:
        dlg.GetColourData().SetColour(wx.Colour(0, 0, 0))
            
    if dlg.ShowModal() == wx.ID_OK:
        data = dlg.GetColourData()
        clr = data.GetColour()
        ret = 'wx.Colour(%d, %d, %d)' % (clr.Red(), clr.Green(), clr.Blue())
    else:
        ret = None
        
    dlg.Destroy()
    return ret


def FontEdtDlg(parent, value):
    """
    Диалоговое окно для определения шрифта.

    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type value: C{string}
    @param value: Текущее значение шрифта в виде словаря.
    """
    data = wx.FontData()
    data.EnableEffects(True)
    
    if value:
        fnt = eval(value)
    else:
        fnt = {}

    curFont = icfont.icFont(fnt)
    data.SetInitialFont(curFont)

    dlg = wx.FontDialog(parent, data)

    if dlg.ShowModal() == wx.ID_OK:
        data = dlg.GetFontData()
        font = data.GetChosenFont()
        
        fnt = {}
        fnt['size'] = font.GetPointSize()
        fnt['family'] = icfont.getICFamily(font)
        fnt['style'] = icfont.getICFontStyle(font)
        fnt['faceName'] = font.GetFaceName()
        fnt['underline'] = font.GetUnderlined()
        
    dlg.Destroy()
    return str(fnt)


def StyleEdtDlg(parent, style, styles,
                position=wx.DefaultPosition, size=wx.DefaultSize, dlgStyle=0):
    """
    Диалоговое окно для определяения комбинировнного стиля.
    
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type style: C{int}
    @param style: Стиль компонента в виде числа. Пример: wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB.
    @type styles: C{dictionary}
    @param styles: Словарь соответствий между названием стиля и идентификатором стиля.
        Пример: ICButtonStyle = {'BU_LEFT':wx.BU_LEFT,'BU_TOP':wx.BU_TOP}
    @type position: C{wx.Point}
    @param position: Позиция диалога.
    @type size: C{wx.Size}
    @param size: Размер диалогового окна.
    @type dlgStyle: C{int}
    @param dlgStyle: Стиль диалога.
    @rtype: C{string}
    @return: Возвращает значение выбранного стиля в текстовом виде.
    """
    ist = int(style)
    dict = icDefInf.getStyleDict(ist, styles)
    lst = dict.keys()
    
    dlg = wx.lib.dialogs.MultipleChoiceDialog(parent, u'', u'Выбери стиль', lst, style=dlgStyle)

    if position != wx.DefaultPosition:
        if parent:
            x, y = position
            position = parent.ClientToScreenXY(x, y) 
            
        dlg.SetPosition(position)
    
    if size != wx.DefaultSize:
        dlg.SetSize(size)
        
    # Определяем стиль компонента
    
    for indx, key in enumerate(lst):
        if dict[key] == 1:
            dlg.lbox.SetSelection(indx)
        
    if dlg.ShowModal() == wx.ID_OK:
        tst = dlg.GetValue()
        style = 0
        
        for indx in tst:
            key = lst[indx]
            style = style | styles[key]

    dlg.Destroy()
    return style


def ChoiceEdtDlg(parent, value, lst, position=wx.DefaultPosition, size=wx.DefaultSize, style=wx.CHOICEDLG_STYLE):
    """
    Диалоговое окно для выбора значения из списка.
    
    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type value: C{string}
    @param value: Текущее значение.
    @type lst: C{list}
    @param lst: Список выбора.
    @type position: C{wx.Point}
    @param position: Позиция окна.
    @type size: C{wx.Size}
    @param size: Размер диалогового окна.
    @type style: C{int}
    @param style: Стиль диалога.
    @rtype: C{string}
    @return: Возвращает выбранное значение.
    """
    dlg = wx.SingleChoiceDialog(parent, '', '', lst, style)

    if position != wx.DefaultPosition:
        if parent:
            x, y = position
            position = parent.ClientToScreenXY(x, y) 
            
        dlg.SetPosition(position)

    if size != wx.DefaultSize:
        dlg.SetSize(size)
    
    if value in lst:
        dlg.SetSelection(lst.index(value))
        
    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.GetStringSelection()

    dlg.Destroy()
    return value


def PyScriptEdtDlg(parent, attr, text, pos, size, uuid_attr, bEnable=True):
    """
    Диалоговое окно для редактирования скриптов.

    @type parent: C{wx.Window}
    @param parent: Указатель на родительское окно.
    @type attr: C{string}
    @param attr: Имя атрибута.
    @type text: C{string}
    @param text: Текст скрипта.
    @type pos: C{wx.Point}
    @param pos: Позиция.
    @type size: C{wx.Size}
    @param size: Размер редактора.
    @rtype: C{tuplpe}
    @return: Первый элемент признак редактирования, второй текст, третий новый uuid.
    """
    # Определяем смещение видимой части окна
    old = text
    x, y = pos
    pos = parent.ClientToScreenXY(x, y) 
    dlg = ic_pyed.icPyEditorDlg(parent, text, pos, size)

    if not bEnable:
        self.dlg.editor.SetReadOnlyMode()
        
    ret = dlg.ShowModal()
    prz = False
        
    if ret == wx.ID_OK:

        # Генерируем новый UUID
        old_uuid = uuid_attr
        
        if bEnable:
            text = dlg.editor.GetText()

            # Если текст изменился генерируем новый uuid
            if old != text:
                prz = True
                uuid_attr = ic_uuid.get_uuid()
                            
        # запомнинаем точки останова
        dlg.editor.GetBreakpoints()
        SysProc.SetPointList(old_uuid, uuid_attr, attr, dlg.editor._Breakpoints, 
                             dlg.editor.GetText(),
                             (dlg.editor.GetLineCount(), dlg.editor.GetIndent(),
                             dlg.editor.GetEOLMode()))
    if dlg:
        dlg.Destroy()
    
    return prz, text, uuid_attr


def test(par=0):
    """
    Тестируем класс icButton
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'icButton Test')
    win = wx.Panel(frame, -1)
    frame.Show(True)

    sts = {'BU_LEFT': wx.BU_LEFT,
           'BU_TOP': wx.BU_TOP,
           'BU_RIGHT': wx.BU_RIGHT,
           'BU_BOTTOM': wx.BU_BOTTOM,
           'BU_EXACTFIT': wx.BU_EXACTFIT}

    st = StyleEdtDlg(win, str(257), sts, size=(-1, 150))

    app.MainLoop()


if __name__ == '__main__':
    """
    Тестируем.
    """
    test()
