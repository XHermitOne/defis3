#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль диалогового окна выбора паспорта объекта.
"""

# --- Подключение библиотек ---
import wx

from ic.log import log

from ic.bitmap import ic_bmp
from ic.utils import ic_file
from ic.utils import ic_util

__version__ = (0, 0, 2, 1)

_ = wx.GetTranslation


# --- Функции ---
def icPassportChoiceDlg(Win_=None, Prj_=None):
    """
    Выбор паспорта объекта.
    @param Win_: Ссылка на окно.
    @param Prj_: Объект проекта.
    @return: Возвращает список паспорта выбранного объекта или None  в случае ошибки.
    """
    if Prj_ is None:
        from ic.engine import ic_user
        Prj_ = ic_user.getPrjRoot()

    dlg = None
    win_clear = False
    try:
        if Win_ is None:
            id_ = wx.NewId()
            Win_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPassportChoiceDialog(Win_, Prj_)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getPassport()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                Win_.Destroy()
            log.info(u'<<<PASSPORT>> <%s> type <%s>' % (result, type(result)))
            return result
    
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()

    return None


def icPassportListDlg(Win_=None, Prj_=None, Default_=None):
    """
    Выбор списка паспортов выбранных объектов.
    @param Win_: Ссылка на окно.
    @param Prj_: Объект проекта.
    @return: Возвращает список паспортов выбранных объектов или None в случае ошибки.
    """
    dlg = None
    win_clear = False
    try:
        if Win_ is None:
            id_ = wx.NewId()
            Win_ = wx.Frame(None, id_, '')
            win_clear = True

        dlg = icPassportListDialog(Win_, Prj_, Default_)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getPassports()
            dlg.Destroy()
            # Удаляем созданное родительское окно
            if win_clear:
                Win_.Destroy()
            log.info(u'<<<PASSPORTS>> <%s> type <%s>' % (result, type(result)))
            return result
    
    finally:
        if dlg:
            dlg.Destroy()

        # Удаляем созданное родительское окно
        if win_clear:
           Win_.Destroy()

    return None


class icPassportChoicePanel(wx.Panel):
    """
    Класс панели выбора паспорта объекта.
    """

    def __init__(self, parent_, Prj_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Prj_: Объект проекта.
        """
        from ic.prj import PrjTree
        
        try:
            if Prj_ is None:
                from ic.engine import ic_user
                Prj_ = ic_user.getPrjRoot()

            wx.Panel.__init__(self, parent_, wx.NewId())

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            # Текущий выбранный паспорт
            id_ = wx.NewId()
            self._psp_label = wx.StaticText(self, id_, u'Паспорт: ')
            cursor = wx.StockCursor(wx.CURSOR_QUESTION_ARROW)
            self._psp_label.SetCursor(cursor)
            self._psp_label.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)

            self._splitter = wx.SplitterWindow(self, wx.NewId())
            self._prj_viewer = PrjTree.icPrjTreeViewer(self._splitter, None)

            if Prj_:
                self._prj_viewer.setRoot(Prj_)

            self._splitter.SplitVertically(self._prj_viewer,
                                           self._prj_viewer.getNonePanel(), 400)
            
            self._boxsizer.Add(self._psp_label, 0, wx.ALL, 10)
            self._boxsizer.Add(self._splitter, 1, wx.EXPAND | wx.GROW, 10)
            
            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)

            self._passport = None
        except:
            log.fatal(u'Ошибка создания объекта панели выбора паспорта объекта')

    def OnMouseLeftDown(self, event):
        """
        Обработчик отображения паспорта.
        """
        try:
            self.setPassportLabel()
        except:
            self._psp_label.SetLabel(u'Паспорт: ')
        event.Skip()
        
    def setPassportLabel(self, Psp_=None):
        """
        Установить текущий выбранный паспорт к окне.
        """
        if Psp_ is None:
            self._selectedPassport()
            Psp_ = self._passport
        self._psp_label.SetLabel(u'Паспорт: %s' % Psp_)

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
            root_prj_path = ic_file.DirName(prj_path)
            res_dirname = ic_file.DirName(res_file_name)

            # Заменить в пути файла ресурса путь до проекта
            if prj_path in res_file_name:
                # Ресурс находиться в этом же проекте
                res_name = res_file_name.replace(prj_path, '')
                subsys_name = ic_file.BaseName(prj_path)
            elif root_prj_path in res_dirname:
                # Ресурс находиться в подсистеме
                res_name = res_file_name.replace(res_dirname, '')
                subsys_name = ic_file.BaseName(res_dirname)
            if res_name[0] == '/':
                res_name = res_name[1:]

        unicode_psp = ((type_name, obj_name, interface, res_name, subsys_name),)
        self._passport = ic_util.encode_unicode_struct(unicode_psp)


class icPassportChoiceDialog(wx.Dialog):
    """
    Класс диалогового окна выбора паспорта объекта.
    """

    def __init__(self, parent_, Prj_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Prj_: Объект проекта.
        """
        try:
            _title = u'Определение паспорта объекта'
            
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent_, -1, title=_title,
                       pos=wx.DefaultPosition, size=wx.Size(800, 400))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            icon_img = ic_bmp.getSysImg('imgEdtPassport')
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
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

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._psp_panel = icPassportChoicePanel(self, Prj_)
            
            self._boxsizer.Add(self._psp_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора паспорта объекта')

    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self._psp_panel._selectedPassport()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
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

    def __init__(self, parent_, Prj_=None):
        """
        Конструктор.
        @param parent_: Окно.
        @param Prj_: Объект проекта.
        """
        try:
            # Сохранить объект проекта, для последующего использования
            self._Prj = Prj_
            
            wx.Panel.__init__(self, parent_, wx.NewId())

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)
            
            # Панель инструментов управления
            self._toolbar = wx.ToolBar(self, wx.NewId(), style=wx.TB_HORIZONTAL | wx.NO_BORDER)
            self._toolbar.SetToolBitmapSize(wx.Size(16, 16))

            id_ = wx.NewId()
            bmp = ic_bmp.getSysImg('imgPlus')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id=id_, bitmap=bmp, shortHelpString=_('Add'))
            self.Bind(wx.EVT_TOOL, self.OnAddPassport, id=id_)

            id_ = wx.NewId()
            bmp = ic_bmp.getSysImg('imgMinus')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id=id_, bitmap=bmp, shortHelpString=_('Delete'))
            self.Bind(wx.EVT_TOOL, self.OnDelPassport, id=id_)

            self._toolbar.AddSeparator()

            id_ = wx.NewId()
            bmp = ic_bmp.getSysImg('imgEdit')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id=id_, bitmap=bmp, shortHelpString=_('Edit'))
            self.Bind(wx.EVT_TOOL, self.OnEditPassport, id=id_)
            
            self._toolbar.AddSeparator()

            id_ = wx.NewId()
            bmp = ic_bmp.getSysImg('imgUp')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id=id_, bitmap=bmp, shortHelpString=_('Move up'))
            self.Bind(wx.EVT_TOOL, self.OnMoveUpPassport, id=id_)
            
            id_ = wx.NewId()
            bmp = ic_bmp.getSysImg('imgDown')
            if bmp is None:
                bmp = wx.NullBitmap
            self._toolbar.AddTool(id=id_, bitmap=bmp, shortHelpString=_('Move down'))
            self.Bind(wx.EVT_TOOL, self.OnMoveDownPassport, id=id_)
            
            self._toolbar.Realize()

            self._list_box = wx.ListBox(self, wx.NewId())
            
            self._boxsizer.Add(self._toolbar, 0, wx.EXPAND | wx.GROW, 10)
            self._boxsizer.Add(self._list_box, 1, wx.EXPAND | wx.GROW, 10)
            
            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)

            self._passports = []
        except:
            log.fatal(u'Ошибка создания объекта панели выбора списка паспортов объектов')

    def SetPassportList(self, PassportList_=None):
        """
        Установить список паспортов.
        @param PassportList_: Список паспортов.
        """
        if PassportList_ is None:
            PassportList_ = []
        
        self._passports = PassportList_
        self._list_box.Clear()
        
        for cur_psp in self._passports:
            self._list_box.Append(str(cur_psp))
            
    def OnAddPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент добавления паспорта в список паспортов.
        """
        psp = icPassportChoiceDlg(self, self._Prj)
        if psp:
            self._list_box.Append(str(psp))
            self._passports.append(psp)
        event.Skip()
        
    def OnDelPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент удаления паспорта из списка паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            self._list_box.Delete(selected)
            del self._passports[selected]
        
        event.Skip()
        
    def OnEditPassport(self, event):
        """
        Обработчик нажатия на кнопку-инструмент изменения паспорта в списке паспортов.
        """
        selected = self._list_box.GetSelection()
        if 0 <= selected < self._list_box.GetCount() and selected != wx.NOT_FOUND:
            psp = icPassportChoiceDlg(self, self._Prj)
            if psp:
                self._list_box.SetString(selected, str(psp))
                self._passports[selected] = psp
        
        event.Skip()
        
    def OnMoveUpPassport(self, event):
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
        
    def OnMoveDownPassport(self, event):
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

    def __init__(self, parent_, Prj_=None, Default_=None):
        """
        Конструктор.
        @param parent_: Родительское окно.
        @param Prj_: Объект проекта.
        @param Default_: Список паспортов по умолчанию.
        """
        try:
            _title = u'Определение паспортов объектов'
            
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
            pre.Create(parent_, -1, title=_title,
                       pos=wx.DefaultPosition, size=wx.Size(800, 400))

            # This next step is the most important, it turns this Python
            # object into the real wrapper of the dialog (instead of pre)
            # as far as the wxPython extension is concerned.
            self.PostCreate(pre)

            icon_img = ic_bmp.getSysImg('imgEdtPassport')
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
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

            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._psp_list_panel = icPassportListPanel(self, Prj_)
            # Если надо то установить редатируемый список паспортов
            if Default_:
                self._psp_list_panel.SetPassportList(Default_)
            
            self._boxsizer.Add(self._psp_list_panel, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log.fatal(u'Ошибка создания объекта диалогового окна выбора списка паспортов объектов')
        
    def OnOK(self, event):
        """
        Обработчик нажатия кнопки -OK-.
        """
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
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
    main_frm = icPassportListDlg(None, None)

    main_frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
