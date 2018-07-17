#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'child': [{'activate': 1, 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': u'1fcfd2bb8c764bc8daa391853606f292', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'activated': u'WrapperObj.activatedFuncbaseLst(evt)', 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(150, 298), 'style': 3, 'foregroundColor': (0, 0, 0), 'span': (3, 1), 'component_module': None, 'selected': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'MultiColumnList', 'res_module': None, 'col_width': [145], 'description': None, '_uuid': u'5117983a2ec89d1cccd2ed06eaa40edb', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'baseLst', 'fields': [u'\u0411\u0430\u0437\u043e\u0432\u044b\u0439 \u0441\u043f\u0438\u0441\u043e\u043a'], 'refresh': None, 'alias': None, 'init_expr': None, 'items': [], 'position': (1, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u'WrapperObj.mouseClickFuncToBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'->', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'22df85aa85dcc8d52514e58427ae1861', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'ToBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u'WrapperObj.mouseClickFuncFromBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, 20), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'<-', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'b681754338d605f8a334fb05382c4439', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'FromBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'activated': u'WrapperObj.activatedFuncchoiceLst(evt)', 'refresh': None, 'font': {}, 'border': 0, 'size': (150, -1), 'style': 3, 'foregroundColor': (0, 0, 0), 'span': (3, 1), 'component_module': None, 'selected': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'MultiColumnList', 'res_module': None, 'col_width': [145], 'description': None, '_uuid': u'41aef565906699a9bb3982c3b64846fc', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': None, 'name': u'choiceLst', 'fields': [u'\u041e\u0442\u043e\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0441\u043f\u0438\u0441\u043e\u043a'], 'keyDown': None, 'alias': None, 'init_expr': None, 'items': [], 'position': (1, 5), 'onInit': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u'WrapperObj.mouseClickFuncDelBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u0441\u0435', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'1d4552ba7d13893c408054c0c81164ef', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'DelBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 5), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'description': None, 'position': (7, 1), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'45dbbcd984e239f93158f379f1d12c43', 'proportion': 0, 'name': u'DefaultName_1118', 'alias': None, 'flag': 256, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u'WrapperObj.mouseClickFuncexitBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0412\u044b\u0445\u043e\u0434', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'03f3e8f85764aeabf70459367c1c9b83', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 256, 'recount': None, 'name': u'exitBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(10, 350), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'attach_focus': False, 'mouseClick': u'WrapperObj.mouseClickFuncchoiceBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'description': None, '_uuid': u'35a14ea32971426e1fd5b10f30364c3b', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 256, 'recount': None, 'name': u'choiceBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(85, 350), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'span': (1, 5), 'res_module': None, 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'DefaultName_1560', 'alias': None, 'init_expr': None, 'position': wx.Point(63, 54), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (460, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0412\u044b\u0431\u0435\u0440\u0438', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': u'GetListDlg_frm.py', 'description': None, 'onClose': None, '_uuid': u'6eb8a5e3706ab1349bdd2112564503f9', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'recount': None, 'setFocus': None, 'name': u'GetListDlg', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'WrapperObj.OnInitFuncGetListDlg(evt)'}

#   Версия объекта
__version__ = (1, 0, 0, 4)
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
    
    def OnInitFuncGetListDlg(self, evt):
        """
        Функция обрабатывает событие <onInit>.
        """
        #self.set_base_list(['one','два', 'три'])
        return None
    
    def mouseClickFuncToBtn(self, evt):
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
    
    def mouseClickFuncFromBtn(self, evt):
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
    
    def mouseClickFuncDelBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на 'DelBtn'.
        """
        obj = self.GetNameObj('choiceLst')
        base = self.GetNameObj('baseLst')
        obj.DeleteAllItems()
        #base.DeleteAllItems()
        self.set_base_list()

        return None
    
    def mouseClickFuncexitBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на 'exitBtn'.
        """
        dlg = self.GetNameObj('GetListDlg')
        dlg.EndModal(wx.ID_CANCEL)
        
    def mouseClickFuncchoiceBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на 'choiceBtn'.
        """
        dlg = self.GetNameObj('GetListDlg')
        obj = self.GetNameObj('choiceLst')
        self.set_result(obj.getStringsByCol(0))
        dlg.EndModal(wx.ID_OK)
        
    
    def activatedFuncbaseLst(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return self.mouseClickFuncToBtn(evt)
        
    
    def activatedFuncchoiceLst(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        return self.mouseClickFuncFromBtn(evt)
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