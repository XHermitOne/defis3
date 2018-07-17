#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит базовый класс для внешних редакторов.
"""

import ic.utils.coderror as coderror
import wx.lib.dialogs
from ic.utils import ic_uuid
from . import basefuncs
from ic.kernel import io_prnt

_ = wx.GetTranslation


class icBaseEdt:
    """
    Базовый класс внешних редакторов.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = -1

    def __init__(self, grid, value, pos, size, style):
        """
        Конструктор.
        """

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition,
               size=wx.DefaultSize, style=0, *arg, **kwarg):
        """
        Функция запускает внешний редактор.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно (грид).
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Расположение диалога на гриде.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалогового окна.
        """
        return coderror.IC_HLP_OK, value

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        # Текст
        if type(value) in (str, unicode):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def Clear(dc, rect, bgr, *arg, **kwarg):
        """
        Чистим ячейку.
        @type rect: C{wx.Rect}
        @param rect: Координаты и размеры ячейки в гриде.
        @type bgr: C{wx.Colour}
        @param bgr: Цвет заливки.
        """
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBrush(wx.Brush(bgr, wx.SOLID))
        dc.SetPen(wx.Pen(bgr, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected, *arg, **kwarg):
        """
        Функция отрисовки значения данного типа в режиме просмотра в гриде.
        @type renderer: C{PropValueRenderer}
        @param renderer: Объект отрисовки ячейки грида.
        @type grid: C{wx.Grid}
        @param grid: Указатель на грид.
        @type cell_attr: C{wx.GridCellAttr}
        @param cell_attr: Атрибут текущей ячейки.
        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        @type rect: C{wx.Rect}
        @param rect: Координаты и размеры ячейки в гриде.
        @type row: C{int}
        @param row: Номер строки.
        @type col: C{int}
        @param col: Номер колонки.
        @type isSelected: C{bool}
        @param isSelected: Признак выбранной ячейки.
        """
        text = renderer.table.GetValue(row, col)
        bgr = renderer.backgroundColor
        icBaseEdt.Clear(dc, rect, bgr)
        icBaseEdt.DrawText(renderer, grid, text, dc, rect)

    @staticmethod
    def DrawText(renderer, grid, text, dc, rect, *arg, **kwarg):
        """
        Отрисовывает значение текстового атрибута.
        @type renderer: C{PropValueRenderer}
        @param renderer: Объект отрисовки ячейки грида.
        @type grid: C{wx.Grid}
        @param grid: Указатель на грид.
        @type text: C{string}
        @param text: Текст.
        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        @type rect: C{wx.Rect}
        @param rect: Координаты и размеры ячейки в гриде.
        """
        dc.SetBrush(renderer.normalBrush)
        dc.SetTextBackground(renderer.backgroundColor)
        dc.SetTextForeground(renderer.color)
        dc.SetFont(renderer.font)

        lx, ly = dc.GetTextExtent('H')
        width, height = (lx * len(text), ly)
        if rect.width - 2 < width:
            nd = width / lx - 3 - (width - rect.width) / lx
            if nd > 0:
                text = text[:nd] + '...'

        dc.DrawText(text, rect.x+1+4, rect.y+1)

    @staticmethod
    def strToVal(text, *arg, **kwarg):
        """
        Функция преобразования строки в значение ресурса.
        """
        try:
            value = eval(text)
        except:
            return None

        return value


#################################################
#   НАБОР СТАНДАРТНЫХ РЕДАКТОРОВ
#################################################


class icTextEdt(icBaseEdt):
    """
    Редактор текстового значения.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 0

    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    strToVal = staticmethod(strToVal)


class icROTextEdt(icBaseEdt):
    """
    Текстовое значения, которое предназначено только для чтения.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 17

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        return coderror.IC_CTRL_FAILED_IGNORE


class icImageEdt(icBaseEdt):
    """
    Редактор образа.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 18

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        """
        Функция отрисовки значения данного типа в режиме просмотра в гриде.
        """
        st = 2
        sx = 16
        bgr = renderer.backgroundColor
        icImageEdt.Clear(dc, rect, bgr)

        x, y = rect.GetPosition()
        dc.SetBrush(wx.Brush(bgr, wx.SOLID))

        dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))
        dc.DrawRectangle(x+st, y+st, sx, sx)
        dc.SetTextForeground(renderer.color)
        dc.SetTextBackground(bgr)
        dc.SetFont(renderer.font)
        dc.DrawText(u'[Image]', x+2*st+sx, y+1)

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        return coderror.IC_CTRL_FAILED_IGNORE


class icFileEdt(icBaseEdt):
    """
    Редактор выбора файла.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 51

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        if type(value) in (str, unicode):
            import os.path
            if os.path.isabs(value):
                return coderror.IC_CTRL_OK
        return coderror.IC_CTRL_FAILED_IGNORE


class icDirEdt(icBaseEdt):
    """
    Редактор выбора директории.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 52

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        if type(value) in (str, unicode):
            import os.path
            if os.path.isabs(value):
                return coderror.IC_CTRL_OK
        return coderror.IC_CTRL_FAILED_IGNORE


class icPyScriptEdt(icBaseEdt):
    """
    Редактор Python скриптов.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 12

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        """
        Функция отрисовки значения данного типа в режиме просмотра
        в гриде.
        """
        bgr = renderer.backgroundColor
        icPyScriptEdt.Clear(dc, rect, bgr)
        text = unicode(grid.GetTable().GetValue(row, col))
        nf = text.find('\n')
        if nf >= 0:
            text = '<Script> %s' % text[:nf-1]

        icPyScriptEdt.DrawText(renderer, grid, text, dc, rect)

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, *arg, **par):
        """
        Диалоговое окно для редактирования скриптов.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно (грид).
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Расположение диалога на гриде.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалогового окна.
        @type par: C{dictionary}
        @param par: Словарь дополнительных именованных параметров. <attr> - имя атрибута,
            <uuid_attr> - старый UUID атрибута, <bEnable=True> - признак режима редактирования.
        @rtype: C{tuplpe}
        @return: Первый элемент признак редактирования, второй текст, третий новый uuid.
        """
        from ic.PropertyEditor import ic_pyed
        text = value
        uuid_attr = par['uuid_attr']
        prz = False
        if 'bEnable' in par:
            bEnable = par['bEnable']
        else:
            bEnable = True

        try:
            # Определяем смещение видимой части окна
            old = text
            x, y = pos
            sx, sy = size
            if sx < 450:
                size = (450, sy)

            pos = parent.ClientToScreenXY(x, y)
            dlg = ic_pyed.icPyEditorDlg(parent, text, pos, size, style=style)

            if not bEnable:
                dlg.editor.SetReadOnlyMode()

            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                # Генерируем новый UUID
                old_uuid = uuid_attr
                if bEnable:
                    text = dlg.editor.GetText()
                    # Если текст изменился генерируем новый uuid
                    if old != text:
                        prz = True
                        uuid_attr = ic_uuid.get_uuid()
            if dlg:
                dlg.Destroy()
        except:
            io_prnt.outLastErr(u'PyScript HlpDlg ERROR')

        return prz, text, uuid_attr


class ChoiceMenu(wx.Menu):
    def __init__(self, parent, lst, style=0):
        """
        Конструктор меню для списка выбора.
        """
        wx.Menu.__init__(self, style=style)
        self._idLst = []
        self._lst = lst
        self._sel = None
        for el in lst:
            id = wx.NewId()
            self._idLst.append(id)
            self.Bind(wx.EVT_MENU, self.OnChoice, id=id)
            self.Append(id, el)

    def GetSelString(self):
        """
        Возвращает строку выбора.
        """
        if self.IsSelString() and self._lst:
            return self._lst[self._sel]

    def IsSelString(self):
        """
        Возвращает признак того, что один из элементов списка был
        выбран.
        """
        if self._sel is None:
            return False
        return True

    def OnChoice(self, evt):
        """
        Обработка выбора одного из пунктов меню.
        """
        id = evt.GetId()
        self._sel = self._idLst.index(id)


class icChoiceEdt(icBaseEdt):
    """
    Редактор значения из списка.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    @type AttrListDict: C{dictionary}
    @cvar AttrListDict: Словарь списков возможных значений для атрибутов данного типа.
    """
    ID_Editor = 1
    AttrListDict = {}
    CHOICE_ITEM = None

    def OnChoiceItem(self, evt):
        """
        Обработка выбора меню.
        """

    @staticmethod
    def SetAttrListDict(attr, lst):
        """
        Устанавливает список возможных значений заданного атрибута.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @type lst: C{list}
        @param lst: Cписок возможных значений заданного атрибута.
        """
        icChoiceEdt.AttrListDict[attr] = lst

    @staticmethod
    def GetAttrListDict(attr):
        """
        Возвращает список возможных значений заданного атрибута.
        @type attr: C{string}
        @param attr: Имя атрибута.
        """
        if attr in icChoiceEdt.AttrListDict:
            return icChoiceEdt.AttrListDict[attr]
        else:
            return None

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        return text

    @staticmethod
    def HlpDlgOld(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
                  style=wx.CHOICEDLG_STYLE, *arg, **kwarg):
        """
        Диалоговое окно для выбора значения из списка.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @rtype: C{string}
        @return: Возвращает выбранное значение.
        """
        lst = icChoiceEdt.GetAttrListDict(attr)
        if not lst:
            lst = []

        dlg = wx.SingleChoiceDialog(parent, '', '', lst, style)
        if pos != wx.DefaultPosition:
            if parent:
                x, y = pos
                pos = parent.ClientToScreenXY(x, y)

            dlg.SetPosition(pos)

        if size != wx.DefaultSize:
            dlg.SetSize(size)

        if value in lst:
            dlg.SetSelection(lst.index(value))

        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetStringSelection()

        dlg.Destroy()
        return value

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=wx.CHOICEDLG_STYLE, *arg, **kwarg):
        """
        Диалоговое окно для выбора значения из списка.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @rtype: C{string}
        @return: Возвращает выбранное значение.
        """
        lst = icChoiceEdt.GetAttrListDict(attr)
        if not lst:
            lst = []

        dlg = ChoiceMenu(parent, lst)
        parent.PopupMenu(dlg, pos)
        # Возвращаем выбранный элемент списка
        if lst and dlg.IsSelString():
            value = dlg.GetSelString()

        dlg.Destroy()
        return value

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Функция контроля значения.
        @param value: Контролируемое значение.
        """
        # Текст
        if type(value) in (str, unicode):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED


class icTextListEdt(icBaseEdt):
    """
    Редактор списка в текстовом виде.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 20

    @staticmethod
    def strToVal(text):
        """
        Функция преобразования строки в значение ресурса.
        """
        try:
            value = eval(text)
        except:
            log.error('eval(text): text=<%s>' % text)
            return None

        return value

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль значения.
        """
        # Преобразем строку к значению
        #value = icTextListEdt.strToVal(value)
        #if value is None:
        #    return value

        if type(value) in (list, tuple):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, *arg, **par):
        """
        Диалоговое окно для редактирования списка в текстовом редакторе.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно (грид).
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Расположение диалога на гриде.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалогового окна.
        @type par: C{dictionary}
        @param par: Словарь дополнительных именованных параметров. <attr> - имя атрибута,
            <uuid_attr> - старый UUID атрибута, <bEnable=True> - признак режима редактирования.
        @rtype: C{tuplpe}
        @return: Первый элемент признак редактирования, второй текст, третий новый uuid.
        """
        from ic.PropertyEditor import ic_pyed
        text = value
        uuid_attr = par['uuid_attr']
        if 'bEnable' in par:
            bEnable = par['bEnable']
        else:
            bEnable = True

        try:
            # Определяем смещение видимой части окна
            old = text
            x, y = pos
            sx, sy = size
            if sx < 450:
                size = (450, sy)

            pos = parent.ClientToScreenXY(x, y)
            dlg = ic_pyed.icPyEditorDlg(parent, text, pos, size, style=style)
            if not bEnable:
                dlg.editor.SetReadOnlyMode()

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
            if dlg:
                dlg.Destroy()
        except:
            io_prnt.outLastErr(u'icTextListEdt HlpDlg ERROR')

        return prz, text, uuid_attr


class icTextDictEdt(icBaseEdt):
    """
    Редактор словаря в питоновском синтаксисе.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 30

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль значения.
        """
        # Преобразем строку к значению
        #value = icTextDictEdt.strToVal(value)
        #if value is None:
        #    return value

        if isinstance(value, dict):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, *arg, **par):
        """
        Диалоговое окно для редактирования словаря в текстовом редакторе.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно (грид).
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение.
        @type pos: C{wx.Point}
        @param pos: Расположение диалога на гриде.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалогового окна.
        @type par: C{dictionary}
        @param par: Словарь дополнительных именованных параметров. <attr> - имя атрибута,
            <uuid_attr> - старый UUID атрибута, <bEnable=True> - признак режима редактирования.
        @rtype: C{tuplpe}
        @return: Первый элемент признак редактирования, второй текст, третий новый uuid.
        """
        from ic.PropertyEditor import ic_pyed
        text = value
        uuid_attr = par['uuid_attr']

        if 'bEnable' in par:
            bEnable = par['bEnable']
        else:
            bEnable = True

        try:
            # Определяем смещение видимой части окна
            old = text
            x, y = pos
            sx, sy = size
            if sx < 450:
                size = (450, sy)

            pos = parent.ClientToScreenXY(x, y)
            dlg = ic_pyed.icPyEditorDlg(parent, text, pos, size, style=style)
            if not bEnable:
                dlg.editor.SetReadOnlyMode()

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
            if dlg:
                dlg.Destroy()
        except:
            io_prnt.outLastErr(u'icTextDictEdt HlpDlg ERROR')

        return prz, text, uuid_attr


class icDictEdt(icBaseEdt):
    """
    Редактор словаря.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 35

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icDictEdt.strToVal(value)
        #if value is None:
        #    return value

        if isinstance(value, dict):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED


class icFontEdt(icBaseEdt):
    """
    Редактор шрифта.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 9

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icFontEdt.strToVal(value)
        #if value is None:
        #    return value

        if isinstance(value, dict):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, *arg, **kwarg):
        """
        Диалоговое окно для определения шрифта.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение шрифта в виде словаря.
        @type pos: C{wx.Point}
        @param pos: Позиция диалога.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        """
        from ic.components import icfont
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
            fnt = dict()
            fnt['size'] = font.GetPointSize()
            fnt['family'] = icfont.getICFamily(font)
            fnt['style'] = icfont.getICFontStyle(font)
            fnt['faceName'] = font.GetFaceName()
            fnt['underline'] = font.GetUnderlined()

        dlg.Destroy()
        return unicode(fnt)


class icNumberEdt(icBaseEdt):
    """
    Редактор числовых значений.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 40

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icNumberEdt.strToVal(value)
        #if value is None:
        #    return value

        if type(value) in (int, float, bool):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def strToVal(text, *arg, **kwarg):
        """
        Функция преобразования строки в значение ресурса.
        """
        try:
            value = eval(text.strip())
        except:
            log.error('eval(text): text=<%s>' % text)
            return None

        return value


class icCheckBoxEdt(icBaseEdt):
    """
    Редактор логических значений.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 2

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icCheckBoxEdt.strToVal(value)
        #if value is None:
        #   return value

        if type(value) in (int, float, bool):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=wx.CHOICEDLG_STYLE, *arg, **kwarg):
        """
        Диалоговое окно для выбора значения из списка.
        """
        lst = ['True', 'False']
        dlg = ChoiceMenu(parent, lst)
        parent.PopupMenu(dlg, pos)
        # Возвращаем выбранный элемент списка
        if lst and dlg.IsSelString():
            value = dlg.GetSelString()

        dlg.Destroy()
        return value

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        """
        Функция отрисовки значения данного типа в режиме просмотра в гриде.
        @type renderer: C{PropValueRenderer}
        @param renderer: Объект отрисовки ячейки грида.
        @type grid: C{wx.Grid}
        @param grid: Указатель на грид.
        @type cell_attr: C{wx.GridCellAttr}
        @param cell_attr: Атрибут текущей ячейки.
        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        @type rect: C{wx.Rect}
        @param rect: Координаты и размеры ячейки в гриде.
        @type row: C{int}
        @param row: Номер строки.
        @type col: C{int}
        @param col: Номер колонки.
        @type isSelected: C{bool}
        @param isSelected: Признак выбранной ячейки.
        """
        text = renderer.table.GetValue(row, col)
        value = icCheckBoxEdt.strToVal(text)
        if value:
            text = 'True'
        else:
            text = 'False'

        bgr = renderer.backgroundColor
        icBaseEdt.Clear(dc, rect, bgr)
        icBaseEdt.DrawText(renderer, grid, text, dc, rect)


class icCombineEdt(icBaseEdt):
    """
    Редактор комбинированных значений.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    @type AttrCombDict: C{dictionary}
    @cvar AttrCombDict: Словарь словарей комбинированных свойств.
    """

    ID_Editor = 7
    AttrCombDict = {}

    @staticmethod
    def SetAttrCombDict(attr, dict):
        """
        Устанавливает словарь комбинированных свойств заданного атрибута.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @type dict: C{dictionary}
        @param dict: Словарь комбинированных свойств.
        """
        icCombineEdt.AttrCombDict[attr] = dict

    @staticmethod
    def GetAttrCombDict(attr):
        """
        Возвращает словарь комбинированных свойств заданного атрибута.
        @type attr: C{string}
        @param attr: Имя атрибута.
        """
        if attr in icCombineEdt.AttrCombDict:
            return icCombineEdt.AttrCombDict[attr]
        else:
            return None

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        """
        Функция отрисовки значения данного типа в режиме просмотра в гриде.
        """
        bgr = renderer.backgroundColor
        icCombineEdt.Clear(dc, rect, bgr)
        style = grid.GetTable().GetValue(row, col)
        attr = grid.GetTable().GetValue(row, 0)
        attr = attr.strip()
        try:
            if attr in grid._styles_attr:
                styles = grid._styles_attr[attr]
                dict = basefuncs.getStyleDict(int(style), styles)
                text = ''
                for indx, key in enumerate(dict.keys()):
                    if dict[key] == 1:
                        text = text + ' | ' + key
                icCombineEdt.DrawText(renderer, grid, text[3:], dc, rect)
            else:
                icCombineEdt.DrawText(renderer, grid, style, dc, rect)
        except:
            io_prnt.outLastErr(u'ERROR')
            icCombineEdt.DrawText(renderer, grid, style, dc, rect)

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #val = icCombineEdt.strToVal(value)
        #if val is None:
        #    return val

        if type(value) in (int, float, bool):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, *arg, **kwarg):
        """
        Диалоговое окно для определяения комбинировнного стиля.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{int}
        @param value: Стиль компонента в виде числа. Пример: wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB.
        @type pos: C{wx.Point}
        @param pos: Позиция диалога.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @rtype: C{string}
        @return: Возвращает значение выбранного стиля в текстовом виде.
        """
        styles = icCombineEdt.GetAttrCombDict(attr)
        ist = int(value)
        dict = basefuncs.getStyleDict(ist, styles)
        lst = dict.keys()
        dlg = wx.lib.dialogs.MultipleChoiceDialog(parent, u'', u'Выбери стиль', lst, style=style)
        if pos != wx.DefaultPosition:
            if parent:
                x, y = pos
                pos = parent.ClientToScreenXY(x, y)

            dlg.SetPosition(pos)

        if size != wx.DefaultSize:
            dlg.SetSize(size)

        # Определяем стиль компонента
        for indx, key in enumerate(lst):
            if dict[key] == 1:
                dlg.lbox.SetSelection(indx)

        if dlg.ShowModal() == wx.ID_OK:
            tst = dlg.GetValue()
            st = 0
            for indx in tst:
                key = lst[indx]
                st = st | styles[key]
        else:
            st = value

        dlg.Destroy()
        return st


class icColorEdt(icBaseEdt):
    """
    Редактор значений цветов.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 8

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        """
        Функция отрисовки значения данного типа в режиме просмотра в гриде.
        """
        st = 4
        sx = 12
        bgr = renderer.backgroundColor
        icColorEdt.Clear(dc, rect, bgr)
        clr = text = grid.GetTable().GetValue(row, col)
        if type(clr) in (type(''),type(u'')):
            clr = eval(clr)

        x, y = rect.GetPosition()
        if clr:
            dc.SetBrush(wx.Brush(clr, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(bgr, wx.SOLID))

        dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))
        dc.DrawRectangle(x+st, y+st, sx, sx)
        dc.SetTextForeground(renderer.color)
        dc.SetTextBackground(bgr)
        dc.SetFont(renderer.font)
        dc.DrawText(unicode(text), x+2*st+sx, y+1)

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, *arg, **kwarg):
        """
        Диалог выбора цвета.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @return: Возвращет выбранный цвет в виде строки 'wx.Colour(r,g,b)'.
        """
        clrd = wx.ColourData()
        clrd.SetChooseFull(True)
        if value:
            clr = eval(value)
        else:
            clr = None

        if clr is not None:
            clrd.SetColour(clr)
        else:
            clrd.SetColour(wx.Colour(0,0,0))

        dlg = wx.ColourDialog(parent, clrd)

        cod = dlg.ShowModal()
        if cod == wx.ID_OK:
            data = dlg.GetColourData()
            clr = data.GetColour()
            ret = '(%d, %d, %d)' % (clr.Red(), clr.Green(), clr.Blue())
        else:
            ret = None

        dlg.Destroy()
        return ret

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        if value in (None, 'None'):
            return coderror.IC_CTRL_OK

        #value = icColorEdt.strToVal(value)
        #if value is None:
        #    return value

        if (type(value) == wx.Colour) or (isinstance(value, tuple) and len(value) == 3):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED


class icPointEdt(icBaseEdt):
    """
    Редактор значений wx.Point.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 10

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icPointEdt.strToVal(value)
        #if value is None:
        #    return value

        if type(value) in (tuple, type(wx.Point(0, 0))) and len(value) == 2:
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED


class icSizeEdt(icBaseEdt):
    """
    Редактор значений wx.Size.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 11

    @staticmethod
    def Ctrl(value, *arg, **kwarg):
        """
        Контроль.
        """
        # Преобразем строку к значению
        #value = icSizeEdt.strToVal(value)
        #if value is None:
        #    return value

        if type(value) in (tuple, type(wx.Size(0, 0))) and len(value) == 2:
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED


class icUserEdt(icBaseEdt):
    """
    Редактор текстового значения.
    @type ID_Edtitor: C{int}
    @cvar ID_Edtitor: Идентификатор внешнего редактора.
    """
    ID_Editor = 16

    @staticmethod
    def Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected):
        propEdt = renderer.kwarg.get('propEdt', None)
        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                edtFunc = getattr(modl, 'property_editor_draw', None)
                if edtFunc:
                    if edtFunc(dc, cell_attr, rect, row, col, isSelected, propEdt):
                        return
            except:
                io_prnt.outErr(_('User property eritor draw error.') + (' property: <%s>' % cell_attr))

        return icBaseEdt.Draw(renderer, grid, cell_attr, dc, rect, row, col, isSelected)

    @staticmethod
    def Ctrl(value, attr=None, propEdt=None, *arg, **kwarg):
        """
        Ф-ия контроля значения.
        @param value: Проверяемое значение.
        @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
        @param propEdt: Указатель на редактор свойств.
        """
        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                edtFunc = getattr(modl, 'property_editor_ctrl')
                return edtFunc(attr, value, propEdt, *arg, **kwarg)
            except:
                io_prnt.outErr(_('User property editor control error.') + (u' property: <%s>' % attr))

        return coderror.IC_CTRL_OK

    @staticmethod
    def HlpDlg(parent, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0, propEdt=None, *arg, **kwarg):
        """
        Диалог выбора цвета.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type attr: C{string}
        @param attr: Имя текущего атрибута.
        @type value: C{string}
        @param value: Текущее значение цвета в виде 'wx.Colour(r,g,b)'.
        @type pos: C{wx.Point}
        @param pos: Позиция окна.
        @type size: C{wx.Size}
        @param size: Размер диалогового окна.
        @type style: C{int}
        @param style: Стиль диалога.
        @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
        @param propEdt: Указатель на редактор свойств.
        @return: Возвращет выбранный цвет в виде строки 'wx.Colour(r,g,b)'.
        """
        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                edtFunc = getattr(modl, 'get_user_property_editor')
                return edtFunc(attr, value, pos, size,
                               style, propEdt, *arg, **kwarg)
            except:
                io_prnt.outErr(u'Ошибка вызова пользовательского редактора свойства <%s>' % attr)

    @staticmethod
    def strToVal(text, propEdt=None, *arg, **kwarg):
        """
        Функция преобразования строки в значение ресурса.
        @type propEdt: C{ic.components.user.objects.PropNotebookEdt}
        @param propEdt: Указатель на редактор свойств.
        """
        value = text
        if propEdt and propEdt.getResTree():
            typRes = propEdt.getResource()['type']
            modl = propEdt.getResTree().GetTypeModule(typRes)
            try:
                edtFunc = getattr(modl, 'str_to_val_user_property')
                return edtFunc(propEdt.GetAttr(), text, propEdt, *arg, **kwarg)
            except:
                io_prnt.outErr(u'Ошибка конвертации пользовательского свойства')
        else:
            try:
                value = eval(text)
            except:
                return None

        return value


if __name__ == '__main__':
    """
    """
    s = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
    s1 = 'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    lst = [x for x in s1]
    lst.sort()
    for x in lst:
        print(x)
