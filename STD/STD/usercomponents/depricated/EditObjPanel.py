#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Базовая панель для редактирования объектов реестра.
Все остальные панели редактирования и просмотра
наследуются от этой панели.
"""

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import STD.interfaces.reestr.browsPanelInterface as pnlIfs

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CEditObjPanel')

ic_class_spc = {'name':'defaultPanel',
                'type':'EditObjPanel',
                'load_data':None,
                'save_data':None,
                'nest':'Panel:ObjPanel',
                '__lists__':{'nest':['Panel:ObjPanel']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'44070354b12ab942f290c2061b1f63d0', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [], 'name': u'ObjPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 1, 7)
###END SPECIAL BLOCK

class CEditObjPanel(ictemplate.icTemplateInterface, pnlIfs.icBrowsPanelReestrInterface):
    """
    Описание пользовательского компонента.
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
        - B{load_data=None}: Выражение загрузка данных в панель
        - B{save_data=None}: Выражение выгрузки данных из панели
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        
        pnlIfs.icBrowsPanelReestrInterface.__init__(self)
        self.resource['load_data'] = component['load_data']
        self.resource['save_data'] = component['save_data']
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource
    
    def LoadData(self):
        """
        """
        self.eval_attr('load_data')
        
    def SaveData(self):
        """
        """
        self.eval_attr('save_data')
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CEditObjPanel.
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