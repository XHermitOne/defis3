#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Стандартная панель (Тестовая).
"""

import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy

### Общий интерфэйс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdGridPanel')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdGridPanel',
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'9d500b71224b00a2f1e3705ed64b5124', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(143, 94), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'247aa75b2a77e80f4736bed773c65bb9', 'proportion': 1, 'name': u'panelSizer', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': wx.Size(385, 34), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'd8065dc48b38f5443d4e936261b5ae57', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'cc91832ed124f328de9fff27f1af569d', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'default_1173', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(86, 15), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'StaticText', 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'a07f224a236e35f11f1ba2a0ac9cbc92', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1181', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(18, 17), 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u"print '### interface:', _interfaces\r\nprint '### interface name:', self.GetInterfaceName()\r\nprint '### interface:', self.GetComponentInterface()\r\nself.GetComponentInterface().OnClientClick()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'button', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'0d6c038a57bb382bcb581fe8fcc14341', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1130', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(213, 14), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'name': u'TopPanel', 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((150,150,150), 2)', 'position': wx.Point(0, 0), 'onInit': None}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (217, 217, 179), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'b24176dc53cf1c0380cc3470adf9b1e9', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': u'0', 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'a344355cd371b1aa7cdca8253f081a1f', 'flag': 0, 'child': [], 'name': u'panelGrid', 'alias': None, 'init_expr': None, 'position': wx.Point(160, 107), 'vgap': 0}], 'name': u'clientPanel', 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((150,150,150), 2)', 'position': wx.Point(0, 0), 'onInit': None}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': wx.Size(385, 34), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'b7b36726711d02187ec9ee084f810bec', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [], 'name': u'BottomPanel', 'keyDown': None, 'alias': None, 'init_expr': u'self.SetRoundBoundMode((150,150,150), 2)', 'position': wx.Point(0, 406), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'StdGridPanel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 3, 1)
###END SPECIAL BLOCK

class CStdGridPanel(ictemplate.icTemplateInterface):
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def _build_resource(self):
        """
        Собирает ресурс из ресурса компонента и ресурса шаблона.
        """
        if self._templRes and 'child' in self._templRes:
            chld = self.resource['child']
            self.resource = copy.deepcopy(self._templRes)
            
            res = self.GetObjectResource('clientPanel', 'Panel', self.resource)
            
            if res and 'child' in res:
                res['child'] = chld

        return self.resource
    def OnClientClick(self):
        """
        """
        print('!!!! OnClientClick')
    ###BEGIN EVENT BLOCK
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