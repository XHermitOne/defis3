#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
from ic.utils import util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'show': 1, 'child': [{'activate': 1, 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 0, 'type': 'GridBagSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '1fcfd2bb8c764bc8daa391853606f292', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'activated': 'WrapperObj.activatedFuncbaseLst(event)', 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(150, 298), 'style': 3, 'foregroundColor': (0, 0, 0), 'span': (3, 1), 'component_module': None, 'selected': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': 'MultiColumnList', 'res_module': None, 'col_width': [145], 'description': None, '_uuid': '5117983a2ec89d1cccd2ed06eaa40edb', 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'baseLst', 'fields': ['Базовый список'], 'refresh': None, 'alias': None, 'init_expr': None, 'items': [], 'position': (1, 1), 'onInit': None, '__item_id': 2}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': 'WrapperObj.mouseClickFuncToBtn(event)', 'font': {}, 'border': 0, 'size': (-1, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': '->', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '22df85aa85dcc8d52514e58427ae1861', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'ToBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None, '__item_id': 3}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': 'WrapperObj.mouseClickFuncFromBtn(event)', 'font': {}, 'border': 0, 'size': (-1, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': '<-', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': 'b681754338d605f8a334fb05382c4439', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'FromBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None, '__item_id': 4}, {'activate': 1, 'show': 1, 'activated': 'WrapperObj.activatedFuncchoiceLst(event)', 'refresh': None, 'font': {}, 'border': 0, 'size': (150, -1), 'style': 3, 'foregroundColor': (0, 0, 0), 'span': (3, 1), 'component_module': None, 'selected': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': 'MultiColumnList', 'res_module': None, 'col_width': [145], 'description': None, '_uuid': '41aef565906699a9bb3982c3b64846fc', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': 'choiceLst', 'fields': ['Отобранный список'], 'keyDown': None, 'alias': None, 'init_expr': None, 'items': [], 'position': (1, 5), 'onInit': None, '__item_id': 5}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': 'WrapperObj.mouseClickFuncDelBtn(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': 'Удалить все', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '1d4552ba7d13893c408054c0c81164ef', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'DelBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 5), 'onInit': None, 'refresh': None, 'mouseContextDown': None, '__item_id': 6}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': 'horizontal', 'description': None, 'position': (7, 1), 'component_module': None, 'type': 'BoxSizer', '_uuid': '45dbbcd984e239f93158f379f1d12c43', 'proportion': 0, 'name': 'DefaultName_1118', 'alias': None, 'flag': 256, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': 'WrapperObj.mouseClickFuncexitBtn(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': 'Выход', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '03f3e8f85764aeabf70459367c1c9b83', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 256, 'recount': None, 'name': 'exitBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 350), 'onInit': None, 'refresh': None, 'mouseContextDown': None, '__item_id': 8}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': 'WrapperObj.mouseClickFuncchoiceBtn(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': 'Запомнить', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '35a14ea32971426e1fd5b10f30364c3b', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 256, 'recount': None, 'name': 'choiceBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 350), 'onInit': None, 'refresh': None, 'mouseContextDown': None, '__item_id': 9}], 'span': (1, 5), 'res_module': None, 'border': 0, 'vgap': 0, 'size': (-1, -1), '__item_id': 7}], 'name': 'DefaultName_1560', 'alias': None, 'init_expr': None, 'position': wx.Point(63, 54), 'vgap': 0, '__item_id': 1}], 'keyDown': None, 'border': 0, 'size': (460, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': 'Выбери', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Dialog', 'res_module': 'GetListDlg_frm.py', 'description': None, 'onClose': None, '_uuid': '6eb8a5e3706ab1349bdd2112564503f9', 'moveAfterInTabOrder': '', 'killFocus': None, 'flag': 0, 'recount': None, 'setFocus': None, 'name': 'GetListDlg', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': 'WrapperObj.OnInitFuncGetListDlg(event)', '__item_id': 0}

#   Version
__version__ = (1, 0, 0, 5)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IGetListDlg'

class IGetListDlg(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        """
        Конструктор интерфейса.
        """
        # Список базовых элементов
        self._base_lst = None
        # Список выбранных элементов
        self._choice_lst = None
        # Результат
        self._result = None
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    def get_result(self):
        """
        Возвращает результат работы компонента.
        """
        return self._result
        
    ###BEGIN EVENT BLOCK
    
    def OnInitFuncGetListDlg(self, event):
        """
        Функция обрабатывает событие <onInit>.
        """
        #self.set_base_list(['one','два', 'три'])
        return None
    
    def mouseClickFuncToBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick> на 'ToBtn'.
        """
        base = self.GetNameObj('baseLst')
        obj = self.GetNameObj('choiceLst')
        item = base.currentItem
        if item >= 0:
            el = base.GetItemText(item)
            print('el=', el)
            obj.appendStringRec(el)
            base.DeleteItem(item)
        return None
    
    def mouseClickFuncFromBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick> на 'FromBtn'.
        """
        base = self.GetNameObj('baseLst')
        obj = self.GetNameObj('choiceLst')
        item = obj.currentItem
        if item >= 0:
            el = obj.GetItemText(item)
            print('el=', el)
            base.appendStringRec(el)
            obj.DeleteItem(item)
        
        return None
    
    def mouseClickFuncDelBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick> на 'DelBtn'.
        """
        obj = self.GetNameObj('choiceLst')
        base = self.GetNameObj('baseLst')
        obj.DeleteAllItems()
        #base.DeleteAllItems()
        self.set_base_list()

        return None
    
    def mouseClickFuncexitBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick> на 'exitBtn'.
        """
        dlg = self.GetNameObj('GetListDlg')
        dlg.EndModal(wx.ID_CANCEL)
        
    def mouseClickFuncchoiceBtn(self, event):
        """
        Функция обрабатывает событие <mouseClick> на 'choiceBtn'.
        """
        dlg = self.GetNameObj('GetListDlg')
        obj = self.GetNameObj('choiceLst')
        self.set_result(obj.getStringsByCol(0))
        dlg.EndModal(wx.ID_OK)
        
    
    def activatedFuncbaseLst(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        return self.mouseClickFuncToBtn(event)
        
    
    def activatedFuncchoiceLst(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        return self.mouseClickFuncFromBtn(event)
    ###END EVENT BLOCK

    def set_base_list(self, lst=None):
        """
        Устанавливает список возможных значений для списка выбора.
        """
        obj = self.GetNameObj('baseLst')
        obj.DeleteAllItems()

        if lst:
            self._base_lst = lst
        else:
            lst = self._base_lst
        
        if lst:
            for el in lst:
                obj.appendStringRec(el)

    def set_choice_list(self, lst):
        """
        Устанавливаем первоначальный список выбора.
        """
        obj = self.GetNameObj('choiceLst')
        obj.DeleteAllItems()

        if lst:
            for el in lst:
                obj.appendStringRec(el)
        
    def set_result(self, res):
        """
        Определяем результат.
        """
        self.GetContext()['result'] = res
        self._result = res
        
def test(par=0):
    """
    Тестируем класс new_form.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()