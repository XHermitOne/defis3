#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
from matplotlib import pylab
import ic.interfaces.icBrPnlInterface as icBrPnlInterface

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'77c9cd9ff305d753b720d6ae76e4dfb4', 'proportion': 0, 'name': u'DefaultName_1435', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': None, 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, 44), 'moveAfterInTabOrder': u'', 'foregroundColor': (10, 83, 220), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u043f\u043b\u0430\u043d\u0430 \u043d\u0430 31.12.2005', 'source': None, 'backgroundColor': (245, 245, 245), 'isSort': False, 'type': u'HeadCell', 'init_expr': None, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'284790d1482053c5459b450cc9cc6e97', 'style': 0, 'flag': 8192, 'child': [], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'HeadCell_1528', 'borderBottomColor': (10, 83, 220), 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(7, 11), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Trend', '_uuid': u'59215845986b3029b17696b39cc662ef', 'description': None, 'onDrawCursor': None, 'moveAfterInTabOrder': u'', 'wxAgg': 0, 'flag': 8192, 'recount': None, 'onMouseLeftDown': None, 'name': u'trend', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'89bcc300db9243966667d69c39834a9c', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'MainPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 0, 5)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IYearIndicatorPanel'

class IYearIndicatorPanel(icobjectinterface.icObjectInterface,
                        icBrPnlInterface.icBrowsPanelInterface):
    def __init__(self, parent, metaObj=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type metaObj: C{icMetaItem}
        @param metaObj: Указатель на дерево планов.
        """
        #
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        icBrPnlInterface.icBrowsPanelInterface.__init__(self, metaObj)
        
        trend = self.GetNameObj('trend')
        labels = trend.subplot.get_xticklabels()
        pylab.set(labels, size=10, color='#0a53e0')
        labels = trend.subplot.get_yticklabels()
        pylab.set(labels, size=10, color='#0a53e0')
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    def LoadData(self):
        """
        Подготавливаем данные для графика.
        """
        pass
        
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