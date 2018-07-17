#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'hgap': 0, 'activate': 1, 'obj_module': None, 'child': [{'activate': 1, 'show': 1, 'activated': u'WrapperObj.activatedFuncHelpList(evt, row)', 'cols': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 70, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'd75246ae3b78c8a10b380741ad75533f', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'cod', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', 'width': 300, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'f69ca2a78c0f9e34becba016eb93920d', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'name', 'keyDown': None, 'alias': None, 'init_expr': None}], 'refresh': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 33554979, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'selected': None, 'proportion': 1, 'source': None, 'getattr': None, 'backgroundColor': None, 'type': u'ListDataset', '_uuid': u'e59d5d0e260eae1306ef55abf1b8fc30', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': [], 'name': u'HelpList', 'keyDown': None, 'alias': None, 'init_expr': None, 'indxFldFind': 0, 'position': (-1, -1), 'onInit': u'WrapperObj.OnInitFuncHelpList(evt)'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'horizontal', 'name': u'DefaultName_1048', 'alias': None, 'component_module': None, 'type': u'BoxSizer', '_uuid': u'ccf3e62915de3564a9994a141669e532', 'proportion': 0, 'flag': 256, 'position': wx.Point(41, 85), 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1170_1352', 'alias': None, 'type': u'SizerSpace', '_uuid': u'c32ef6c6189c8b124ed6a5e33b9eddb2', 'proportion': 0, 'component_module': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 30)}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncchoiceBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0412\u044b\u0431\u0440\u0430\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'1b72909cc6cdd22d339a1933acd70e4d', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': None, 'name': u'choiceBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(166, 318), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1170_1454', 'alias': None, 'type': u'SizerSpace', '_uuid': u'c32ef6c6189c8b124ed6a5e33b9eddb2', 'proportion': 0, 'component_module': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (10, 0)}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncCancelBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'9441f9342a988f87534dd22555955fb5', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': None, 'name': u'cancelBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(251, 318), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1170', 'alias': None, 'type': u'SizerSpace', '_uuid': u'c32ef6c6189c8b124ed6a5e33b9eddb2', 'proportion': 0, 'component_module': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'border': 0, 'size': (-1, -1), 'style': 0, 'layout': u'vertical', 'alias': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'description': None, '_uuid': u'f300f3cc6736da13a55d4ef590eae2f6', 'flag': 0, 'component_module': None, 'span': (1, 1), 'name': u'DefaultName_1568_1568', 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'keyDown': u'WrapperObj.keyDownFuncHlpListDlg(evt)', 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0412\u044b\u0431\u0435\u0440\u0438:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': '0fc957547fc80af2bf16bea6d10fbbf4', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'alias': None, 'recount': None, 'setFocus': None, 'name': u'HlpListDlg', 'refresh': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 0, 6)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IHlpSprav'

class IHlpSprav(icobjectinterface.icObjectInterface):
    def __init__(self, parent, metaObj=None, descrKey='description'):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на метаобъект справочника.
        """
        #   Указатель на дерево справочной системы
        self.metaObj = metaObj
        self.descrKey = descrKey
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
    def Choice(self, row=None):
        """
        """
        obj = self.GetNameObj('HelpList')
        
        if row==None:
            row = obj.currentItem
            
        name = obj.dataset.data[row][1]
        self.SetResult(name)
        dlg = self.getObject()
        dlg.EndModal(wx.ID_OK)

    ###BEGIN EVENT BLOCK
    
    def mouseClickFuncCancelBtn(self, evt):
        """
        Функция обрабатывает нажатие кнопки  <Cancel>.
        """
        self.SetResult(None)
        dlg = self.getObject()
        dlg.EndModal(wx.ID_CANCEL)
    
    def keyDownFuncHlpListDlg(self, evt):
        """
        Функция обрабатывает нажатие клавиш на клавиатуре.
        """
        keyCod = evt.GetKeyCode()
        
        if keyCod == wx.WXK_ESCAPE:
            self.SetResult(None)
            dlg = self.getObject()
            dlg.EndModal(wx.ID_CANCEL)
    
    def activatedFuncHelpList(self, evt, row):
        """
        Функция обрабатывает событие <activated>.
        """
        self.Choice(row)
    
    def mouseClickFuncchoiceBtn(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        self.Choice(None)

    
    def OnInitFuncHelpList(self, evt):
        """
        Функция обрабатывает событие <OnInit>.
        """
        buff = [(1,2),('a','b')]
        if self.metaObj:
            lst = self.metaObj.keys()
            print('@@@@@ lst=', lst)
            
            if 1:
                lst.sort()
                buff = [None for x in lst]
                for i, key in enumerate(lst):
                    obj = self.metaObj[key]
                    buff[i] = (key, getattr(obj.value, self.descrKey))
#        else:
#            buff = [(1,2),('a','b')]
        print(' @@@@ >>>>  buff:', buff)
        obj = self.GetNameObj('HelpList')
        obj.RefreshData(buff)
        obj.SetCursor(0)
    ###END EVENT BLOCK
    
    def SetResult(self, result):
        """
        Устанавливает возвращаемое формой значение.
        """
        print('>>> listdataset RESULT=', result)
        self.evalSpace['result'] = result
        
    def GetResult(self):
        """
        Возвращает возвращаемое формой значение.
        """
        return self.evalSpace['result']
        
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