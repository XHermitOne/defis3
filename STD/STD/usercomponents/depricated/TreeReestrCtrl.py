#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Компонент, представляющий реестр в виде дерева.
д Наследует интерфейс <reestr.icTreeReestrInterface>
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import STD.interfaces.reestr.treeReestrInterface as reestr
import ic.utils.uuid as uuid
import ic.PropertyEditor.icDefInf as icDefInf

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CTreeReestrCtrl')

ic_class_spc = {'name':'defaultReestrTreeCtrl',
                'type':'TreeReestrCtrl',
                'selected':None,
                'titleRoot':'Реестр',
                'activated':None,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'titleRoot']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['StdReestr']
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'child': [{'activate': 1, 'minCellWidth': 3, 'minCellHeight': 3, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [1], 'component_module': None, 'flexCols': [1], 'proportion': 1, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'1d8a7432211831b3c4c699dcce5ef3eb', 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'activated': None, 'keyDown': u'', 'onExpand': None, 'border': 0, 'titleRoot': u'\u0420\u0435\u0435\u0441\u0442\u0440', 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'onRightClick': u'GetInterface().OnRightClickFuncreestrTree(evt)', 'component_module': None, 'selected': u'GetInterface().selectedFuncreestrTree(evt)', 'proportion': 1, 'source': None, 'backgroundColor': None, 'size': (-1, -1), 'type': u'TreeCtrl', 'description': None, '_uuid': u'20cde7e30955394581dc0fd15dc74ff2', 'style': 25, 'flag': 8192, 'recount': None, 'name': u'reestrTree', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'0760fd967e4ab31fccc2d3fdeb997c60', 'proportion': 0, 'name': u'DefaultName_2240', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (0, 2), 'border': 0, 'size': (0, 0)}, {'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'299dfd7b7ab7d78f45d831748eb877fa', 'proportion': 0, 'name': u'DefaultName_2345', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (2, 0), 'border': 0, 'size': (0, 0)}, {'style': 0, 'activate': 1, 'prim': u'', 'name': u'reestrList', 'component_module': None, '_uuid': u'36eaf918b251e5934aa1be126c4705ee', 'alias': None, 'init_expr': None, 'child': [], 'type': u'Group', 'description': u'\u0421\u043f\u0438\u0441\u043e\u043a \u0440\u0435\u0435\u0441\u0442\u0440\u043e\u0432, \u043c\u0435\u0436\u0434\u0443 \u043a\u043e\u0442\u043e\u0440\u044b\u043c\u0438\r\n\u043c\u043e\u0436\u043d\u043e \u043f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0430\u0442\u044c\u0441\u044f'}], 'name': u'panelSZR', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': wx.Size(231, 440), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'cb8a14d7667394b9c0943c58aae27b96', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'TopPanel', 'refresh': None, 'alias': None, 'init_expr': u'#self.SetRoundBoundMode((100, 128, 192), 1)', 'position': wx.Point(123, 103), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 3, 5)
###END SPECIAL BLOCK

class CTreeReestrCtrl(ictemplate.icTemplateInterface, reestr.icTreeReestrInterface):
    """
    Древовидное представление реестра.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.reestrObj = None
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
                                                
        reestr.icTreeReestrInterface.__init__(self, context=evalSpace)
        self.resource['name'] = component['name']
        #   Изменение вычисляемых атрибутов должно соправождаться изменением
        # uuid, т.к. в буфере может остаться компилированное выражение от
        # другого объекта собранного по данному шаблону
        res = self.GetObjectResource('reestrTree', 'TreeCtrl')
        res['selected'] = component['selected']
        res['activated'] = component['activated']
        res['titleRoot'] = component['titleRoot']
        res['_uuid'] = uuid.get_uuid()
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def _init_nest(self, nest=None):
        """
        Определяет гнездо компонента.
        """
        if nest:
            self._nest = nest
        else:
            self._nest = ('Group','reestrList')
        
    def SetReestr(self, reestr):
        """
        Устанавливаем текущий реестр.
        """
        if reestr:
            self.reestrObj = reestr
            tree = self.getRegObj('reestrTree')
            print('---> tree=', tree)
            tree.max_level = -1 if reestr.GetComponentInterface() == None else reestr.GetComponentInterface().max_level
            tree.LoadTree(self.reestrObj)
            
    ###BEGIN EVENT BLOCK
    
    def OnRightClickFuncreestrTree(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        print('<< OnRightClickFuncreestrTree >>')
        return None
    
    def selectedFuncreestrTree(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        print('<< selectedFuncreestrTree >>')
        return None
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CTreeReestrCtrl.
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