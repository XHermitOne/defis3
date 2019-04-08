#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.db.icdataset as icdataset
import copy
#import NSI.spravfunc as spravfunc

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'keyDown': u'WrapperObj.keyDownFuncDialog_1147(evt)', 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u041f\u0435\u0440\u0432\u0438\u0447\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': None, '_uuid': u'6e67d28c91102efaf30df26d63d7af79', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0445', '_uuid': u'b709d8cbda0deacddd41ab70ae83150c', 'alias': None, 'init_expr': None, 'child': [{'activate': 1, 'name': u'Table', '_uuid': u'bf67589b5f27d9c1f047c8695328a547', 'docstr': u'ic.db.icdataset-module.html', 'filter': u"select id from analitic where reg='0241'", 'alias': None, 'res_query': u'analitic', 'init_expr': None, 'file': u'analitic.tab', 'type': u'DataLink', 'link_expr': u''}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1149', 'position': wx.Point(196, 48), 'type': u'BoxSizer', '_uuid': u'923aba6ea21aab1aac1fcc2bf04392c4', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'activated': None, 'cols': [{'activate': u'0', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'label': u'\u0420\u0435\u0433\u0438\u043e\u043d', 'width': 50, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'ebbf666c0b87b4a46976e061334dbb2e', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'0918794bbff18e2983568764aacb0c48', 'recount': None, 'hlp': None, 'name': u'reg', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'label': u'\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'd4fcd7abd9c384e9e586a6e6937d8b58', 'recount': None, 'hlp': None, 'name': u'mens', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'WrapperObj.getvalueFunccodt(evt, value)', 'style': 0, 'label': u'\u041a\u043e\u0434 \u0442\u043e\u0432\u0430\u0440\u0430', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'74929ddff78420fb240fec41a66ff10e', 'recount': None, 'hlp': u'', 'name': u'codt', 'setvalue': u'', 'attr': u'C', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'getvalue': u'WrapperObj.getvalueFuncProduct(evt)', 'style': 0, 'label': u'\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', 'width': 200, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'74929ddff78420fb240fec41a66ff10e', 'recount': None, 'hlp': None, 'attr': u'C', 'setvalue': u'', 'name': u'Product', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'label': u'\u0421\u0443\u043c\u043c\u0430', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'5809f6e6182da4e31fd2b2122e2dff87', 'recount': None, 'hlp': None, 'attr': u'W', 'setvalue': u'', 'name': u'summa', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'label': u'\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'69169ba353ce7cee40643845064946e8', 'recount': None, 'getvalue': u'', 'attr': u'W', 'setvalue': u'', 'name': u'kolf', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'border': 0, 'size': (-1, -1), 'style': 33554979, 'foregroundColor': None, 'span': (1, 1), 'selected': None, 'proportion': 1, 'source': u'Table', 'getattr': None, 'backgroundColor': None, 'type': u'ListDataset', '_uuid': u'4acfa404169e2d383ed72a6a52d52fb0', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': [], 'name': u'TableListDataset', 'refresh': None, 'alias': None, 'init_expr': None, 'indxFldFind': 0, 'position': wx.Point(10, -6), 'onInit': u'WrapperObj.OnInitFuncTableListDataset(evt)'}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'Dialog_1147', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 0)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IAnaliticTable'

ProductSpravBuff = {}

def SetProductSpravBuff(buff):
    """
    """
    global ProductSpravBuff
    ProductSpravBuff = buff
    
def ClearProductSpravBuff():
    """
    """
    global ProductSpravBuff
    ProductSpravBuff = {}
    
class IAnaliticTable:
    def __init__(self, parent, tableName=None, filter=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @param tableName: Имя таблицы.
        @param filter: структурный фильтр или SQL выражения для фильтрации выборки.
            Пример 1: {'codt':'0010001','reg':'0241'}
            Пример 2: select id from analitic where codt='0010001' and reg='0241'
        """
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        self._res = copy.deepcopy(resource)
        
        res = self.GetNameRes('Table')
        self.spravDict=None
        # Переопределяем источник данных
        if tableName:
            res['file']=tableName + '.tab'
            res['res_query']=tableName
        # Переопределяем фильтр
        if filter:
            res['filter']=filter
            
        self.__obj = prs.icBuildObject(parent, self._res, evalSpace=self.evalSpace, bIndicator=True)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object

    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if self.evalSpace['_dict_obj'].has_key(name):
            return self.evalSpace['_dict_obj'][name]
        else:
            return None
            
    def GetNameRes(self, name):
        """
        Возвращает ресурс по имени компонента.
        """
        return icdataset.findResName(self._res, name)
    ###BEGIN EVENT BLOCK
    
    def getvalueFunccodt(self, evt, value):
        """
        Функция обрабатывает событие <?>.
        """
        if ProductSpravBuff and ProductSpravBuff.has_key(value):
            value = ProductSpravBuff[value].strip()
            
        return value
    
    def OnInitFuncTableListDataset(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        global ProductSpravBuff
        ProductSpravBuff = spravfunc.getReplDict('Product','cod', 'name')

    
    def keyDownFuncDialog_1147(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        cod = evt.GetKeyCode()
        
        if cod==wx.WXK_ESCAPE:
            self.getObject().EndModal(wx.ID_CANCEL)
            
        return None
    ###END EVENT BLOCK
    
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