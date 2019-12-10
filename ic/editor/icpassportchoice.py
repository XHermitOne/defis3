#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль диалогового окна выбора паспорта объекта.
"""

# --- Подключение библиотек ---
import os
import os.path
import wx

from ic.log import log

from ic.bitmap import bmpfunc
from ic.utils import toolfunc

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation


# --- Функции ---
def open_passport_choice_dlg(parent=None, prj=None):
    """
    Выбор паспорта объекта.

    :param parent: Ссылка на окно.
    :param prj: Объект проекта.
    :return: Возвращает список паспорта выбранного объекта или None  в случае ошибки.
    """
    if prj is None:
        from ic.engine import glob_functions
        prj = glob_functions.getPrjRoot()

    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPassportChoiceDialog(parent, prj)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getPassport()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                parent.Destroy()
            log.debug(u'Выбор паспорта %s' % result)
            return result
    except:
        log.fatal(u'Ошибка выбора паспорта объекта')
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()

    return None


def open_passport_list_dlg(parent=None, prj=None, default=None):
    """
    Выбор списка паспортов выбранных объектов.

    :param parent: Ссылка на окно.
    :param prj: Объект проекта.
    :return: Возвращает список паспортов выбранных объектов или None в случае ошибки.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPassportListDialog(parent, prj, default)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getPassports()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                parent.Destroy()
            log.debug(u'Выбор паспорта %s' % result)
            return result
    except:
        log.fatal(u'Ошибка выбора списка паспортов объекта')
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           parent.Destroy()

    return None


class icPassportChoicePanel(wx.Panel):
    """
    Класс панели выбора паспорта объекта.
    """

    def __init__(self, parent_, prj=None):
        """
        Конструктор.

        :param parent_: Окно.
        :param prj: Объект проекта.
        """
        from ic.prj import icPrjTree
        
        try:
            if prj is None:
                from ic.engine import glob_functions
                prj = glob_functions.getPrjRoot()

            wx.Panel.__init__(self, parent_, wx.NewId())

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            # Текущий выбранный паспорт
            id_ = wx.NewId()
            self._psp_label = wx.StaticText(self, id_, u'Паспорт: ')
            cursor = wx.StockCursor(wx.CURSOR_QUESTION_ARROW)
            self._psp_label.SetCursor(cursor)
            self._psp_label.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)

            self._splitter = wx.SplitterWindow(self, wx.NewId())
            self._prj_viewer = icPrjTree.icPrjTreeViewer(self._splitter, None)

            if prj:
                self._prj_viewer.setRoot(prj)

            self._splitter.SplitVertically(self._prj_viewer,
                                           self._prj_viewer.getNonePanel(), 400)
            
            self._boxsizer.Add(self._psp_label, 0, wx.ALL, 10)
            self._boxsizer.Add(self._splitter, 1, wx.EXPAND | wx.GROW, 10)
            
            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)

            self._passport = None
        except:
            log.fatal(u'Ошибка создания объекта панели выбора паспорта объекта')

    def onMouseLeftDown(self, event):
        """
        Обработчик отображения паспорта.
        """
        try:
            self.setPassportLabel()
        except:
            self._psp_label.SetLabel(u'Паспорт: ')
        event.Skip()
        
    def setPassportLabel(self, psp=None):
        """
        Установить текущий выбранный паспорт к окне.
        """
        if psp is None:
            self._selectedPassport()
            psp = self._passport
        self._psp_label.SetLabel(u'Паспорт: %s' % psp)

    def _selectedPassport(self):
        """
        Определить какой паспорт выбран.
        """
        type_name = None
        obj_name = None
        interface = None
        res_name = None
        subsys_name = None
        
        prj_node = self._prj_viewer.getSelectionNode()
        res_viewer = self._splitter.GetWindow2()
        if res_viewer is None:
            res_object = None
        else:
            res_object = res_viewer.getSelectedObject()
           
        res_file_name = None
        if res_object:
            type_name = res_object['type']
            obj_name = res_object['name']
            res_file_name = res_viewer.getNodeResFileName()
        else:
            res_file_name = prj_node.getFullResFileName()
        if res_file_name:
            # Это нужно чтобы мы точно были уверены что выбираем рут
            prj = prj_node.getRoot()
            if prj.isPrjRoot():
                prj_path = prj.getPath()
            else:
                prj_path = prj.getParentRoot().getPath()
            root_prj_path = os.path.dirname(prj_path)
            res_dirname = os.path.dirname(res_file_name)

            # Заменить в пути файла ресурса путь до проекта
            if prj_path in res_file_name:
                # Ресурс находиться в этом же проекте
                res_name = res_file_name.replace(prj_path, '')
                subsys_name = os.path.basename(prj_path)
            elif root_prj_path in res_dirname:
                # Ресурс находиться в подсистеме
                res_name = res_file_name.replace(res_dirname, '')
                subsys_name = os.path.basename(res_dirname)
            if res_name[0] == '/':
                res_name = res_name[1:]

        unicode_psp = ((type_name, obj_name, interface, res_name, subsys_name),)
        # self._passport = ic_util.encode_unicode_struct(unicode_psp)
        self._passport = unicode_psp


class icPassportChoiceDialog(wx.Dialog):
    """
    Класс диалогового окна выбора паспорта объекта.
    """

    def __init__(self, parent_, prj=None):
        """
        Конструктор.

        :param parent_: Окно.
        :param prj: Объект проекта.
        """
        try:
            _title = u'Определение паспорта объекта'
            
            wx.Dialog.__init__(self, parent_, -1, title=_title,
                               pos=wx.DefaultPosition, size=wx.Size(800, 400))

            icon_img = bmpfunc.getSysImg('imgEdtPassport')
            if icon_img:
                icon = wx.Icon(icon_img)
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

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._psp_panel = icPassportChoicePanel(self, prj)
            
            self._boxsizer.Add(self._psp_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора паспорта объекта')

    def onOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self._psp_panel._selectedPassport()
        self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self._psp_panel._passport = None
        self.EndModal(wx.ID_CANCEL)

    def getPassport(self):
        """
        Паспорт выбранного объекта.
        """
        return self._psp_panel._passport


class icPassportListPanel(wx.Panel):
    """
    Класс панели выбора списка паспортов объектов.
    """

    def __init__(self, parent_, prj=None):
        """
        Конструктор.

        :param parent_: Окно.
        :param prj: Объект проекта.
        """
        try:
            # Сохранить объект проекта, для последующего использования
            self._Prj = prj
            
            wx.Panel.__init__(self, parent_, wx.NewId())

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)
            
            # Панель инструментов управления
            self._toolbar = wx.ToolBar(self, wx.NewId(), style=wx.TB_HORIZONTAL | wx.NO_BORDER)
            self._toolbar.SetToolBitmapSize(wx.Size(16, 16))

            id_ = wx.NewId()
            bmp = bmpfunc.getSysImg('imgPlus')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id_, 'Add', bmp, shortHelp=_('Add'))
            self.Bind(wx.EVT_TOOL, self.onAddPassport, id=id_)

            id_ = wx.NewId()
            bmp = bmpfunc.getSysImg('imgMinus')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id_, 'Delete', bmp, shortHelp=_('Delete'))
            self.Bind(wx.EVT_TOOL, self.onDelPassport, id=id_)

            self._toolbar.AddSeparator()

            id_ = wx.NewId()
            bmp = bmpfunc.getSysImg('imgEdit')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id_, 'edit', bmp, shortHelp=_('edit'))
            self.Bind(wx.EVT_TOOL, self.onEditPassport, id=id_)
            
            self._toolbar.AddSeparator()

            id_ = wx.NewId()
            bmp = bmpfunc.getSysImg('imgUp')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id_, 'MoveUp', bmp, shortHelp=_('Move up'))
            self.Bind(wx.EVT_TOOL, self.onMoveUpPassport, id=id_)
            
            id_ = wx.NewId()
            bmp = bmpfunc.getSysImg('imgDown')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id_, 'MoveDown', bmp, shortHelp=_('Move down'))
            self.Bind(wx.EVT_TOOL, self.onMoveDownPassport, id=id_)
            
            self._toolbar.Realize()

            self._list_box = wx.ListBox(self, wx.NewId())
            
            self._boxsizer.Add(self._toolbar, 0, wx.EXPAND | wx.GROW, 10)
            self._boxsizer.Add(self._list_box, 1, wx.EXPAND | wx.GROW, 10)
            
            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)

            self._passports = []
        except:
            log.fatal(u'Ошибка создания объекта панели выбора списка паспортов объектов')

    def setPassportList(self, passport_list=None):
        """
        Установить список паспортов.

        :param passport_list: Список паспортов.
        """
        if passport_list is None:
            passport_list = []
        
        self._passports = passport_list
        self._list_box.Clear()
        
        for cur_psp in self._passports:
            self._list_box.Append(str(cur_psp))
            
    def onAddPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент добавления паспорта в список паспортов.
        """
        psp = open_passport_choice_dlg(self, self._Prj)
        if psp:
            self._list_box.Append(str(psp))
            self._passports.append(psp)
        event.Skip()
        
    def onDelPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент удаления паспорта из списка паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            self._list_box.Delete(selected)
            del self._passports[selected]
        
        event.Skip()
        
    def onEditPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент изменения паспорта в списке паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            psp = open_passport_choice_dlg(self, self._Prj)
            if psp:
                self._list_box.SetString(selected, str(psp))
                self._passports[selected] = psp
        
        event.Skip()
        
    def onMoveUpPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент перемещения вверх паспорта в списке паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            new_pos = selected - 1
            if new_pos >= 0:
                selected_str = self._list_box.GetString(selected)
                pop_str = self._list_box.GetString(new_pos)
                self._list_box.SetString(selected, pop_str)
                self._list_box.SetString(new_pos, selected_str)
                self._list_box.Select(new_pos)
                
                selected_psp = self._passports[selected]
                self._passports[selected] = self._passports[new_pos]
                self._passports[new_pos] = selected_psp
                
        event.Skip()
        
    def onMoveDownPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент перемещения вниз паспорта в списке паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            new_pos = selected+1
            if new_pos < self._list_box.GetCount():
                selected_str = self._list_box.GetString(selected)
                pop_str = self._list_box.GetString(new_pos)
                self._list_box.SetString(selected, pop_str)
                self._list_box.SetString(new_pos, selected_str)
                self._list_box.Select(new_pos)
                
                selected_psp = self._passports[selected]
                self._passports[selected] = self._passports[new_pos]
                self._passports[new_pos] = selected_psp
                
        event.Skip()
        

class icPassportListDialog(wx.Dialog):
    """
    Класс диалогового окна выбора списков паспортов объектов.
    """

    def __init__(self, parent_, prj=None, default=None):
        """
        Конструктор.

        :param parent_: Родительское окно.
        :param prj: Объект проекта.
        :param default: Список паспортов по умолчанию.
        """
        try:
            _title = u'Определение паспортов объектов'
            
            wx.Dialog.__init__(self, parent_, -1, title=_title,
                               pos=wx.DefaultPosition, size=wx.Size(800, 400))

            icon_img = bmpfunc.getSysImg('imgEdtPassport')
            if icon_img:
                icon = wx.Icon(icon_img)
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

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._psp_list_panel = icPassportListPanel(self, prj)
            # Если надо то установить редатируемый список паспортов
            if default:
                self._psp_list_panel.setPassportList(default)
            
            self._boxsizer.Add(self._psp_list_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора списка паспортов объектов')
        
    def onOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        """
        Обработчик нажатия кнопки -Отмена-.
        """
        self._psp_list_panel._passports = []
        self.EndModal(wx.ID_CANCEL)

    def getPassports(self):
        """
        Паспорта выбранных объектов.
        """
        return self._psp_list_panel._passports


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp(0)
    main_frm = open_passport_list_dlg(None, None)

    main_frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
