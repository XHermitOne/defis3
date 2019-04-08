#usr/bin/env python
# -*- coding: utf-8 -*-

import wx
#import sqlobject

import ic.components.icResourceParser as prs
import ic.components.icEvents as icEvents
import ic.utils.util as util
import matplotlib
import matplotlib.numerix as numerix
import datetime
import time
import ic.dlg.msgbox as msgbox
#import ic.db.tabclass as tabclass
#import NSI.spravfunc as spravfunc
#from NSI import spravctrl

from matplotlib.dates import DayLocator, HourLocator, MinuteLocator,\
     drange, date2num, timezone, num2date

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': wx.Size(722, 591), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'6745983d6fd2147038ba0dc016df8907', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(198, 86), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'13fe8b62916040404c16dae48292fe49', 'proportion': 0, 'name': u'DefaultName_1054', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'refresh': None, 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Trend', 'onDrawCursor': None, 'description': None, '_uuid': u'1fb40484f9500d18ee7bcdafaae2c411', 'style': 0, 'wxAgg': 0, 'flag': 8192, 'recount': None, 'onMouseLeftDown': None, 'name': u'Graph', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(33, 39), 'onInit': None}, {'activate': 1, 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (5, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 0, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'1c45c52fd3a101ba5189f62a3b4ba18d', 'flag': 0, 'child': [{'activate': 1, 'show': 1, 'refresh': None, 'border': 0, 'size': wx.Size(210, 124), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (6, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'CheckListBox', 'description': None, '_uuid': u'e02b424e4e6f37091a367f4f44198c76', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'objectsList', 'items': u"['\u0414\u043e\u043a\u0442\u043e\u0440\u0441\u043a\u0430\u044f', '\u041f\u0440\u0438\u043c\u0430']", 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': 1, 'show': 1, 'refresh': None, 'font': {}, 'border': 0, 'size': wx.Size(111, 81), 'style': 0, 'foregroundColor': (0, 0, 0), 'layout': u'vertical', 'component_module': None, 'selected': 0, 'proportion': 0, 'label': u'\u0412\u0438\u0434 \u0433\u0438\u0441\u0442\u043e\u0433\u0440\u0430\u043c\u043c\u044b', 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'RadioGroup', 'description': None, 'max': 0, '_uuid': u'9f01c8cd736beba32cba9500610a8653', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'span': (5, 1), 'name': u'typeHistGrp', 'items': [u'\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435', u'\u0414\u043e\u043b\u044f \u0432 \u0441\u0443\u043c\u043c\u0435'], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 7), 'onInit': None}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': wx.Size(80, 21), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', '_uuid': u'0321f5577e652858055d184ff33b07cf', 'style': 2, 'flag': 0, 'recount': None, 'name': u'date1', 'value': u'', 'alias': None, 'init_expr': None, 'position': (1, 3), 'refresh': None}, {'activate': 1, 'show': 1, 'keyDown': None, 'border': 0, 'size': wx.Size(80, 21), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'DatePickerCtrl', '_uuid': u'0d86b22a3a1382be1a6a37da7dcdd35d', 'style': 2, 'flag': 0, 'recount': None, 'name': u'date2', 'value': u'', 'alias': None, 'init_expr': None, 'position': (3, 3), 'refresh': None}, {'activate': 1, 'show': 1, 'text': u'\u0412\u0438\u0434\u044b \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438', 'refresh': None, 'font': {'style': u'bold', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'MS Sans Serif', 'type': u'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(69, 15), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'6d77ae3d7d5cbb2d78f0f0c869a2dcaf', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': None, 'name': u'default_1111', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 1)}, {'activate': 1, 'show': 1, 'text': u'\u041f\u0435\u0440\u0438\u043e\u0434', 'refresh': None, 'font': {'style': u'bold', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'MS Sans Serif', 'type': u'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(70, 15), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'86f91e497b36d704b47a92d13c1ef267', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': None, 'name': u'default_1122', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 3)}, {'activate': 1, 'ctrl': u"if value:\r\n    _resultEval = spravctrl.CtrlSprav('Menager', value, field='cod')", 'pic': u'S', 'hlp': u"spravctrl.HlpSprav('Menager', parentForm=self)", 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(70, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'ee98153c32f12497770633ce300ceccc', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'agentEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (1, 5), 'onInit': None, 'refresh': []}, {'activate': 1, 'ctrl': u"spravctrl.CtrlSprav('Contragent', value, field='cod')", 'pic': u'S', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(70, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'30d083c06939995ea6bc95f02e3e748b', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': u"spravctrl.HlpSprav('Contragent', parentForm=self)", 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'contragentEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': u'self.Enable(False)', 'position': (3, 5), 'onInit': None, 'refresh': []}, {'activate': 1, 'show': 1, 'text': u'\u0410\u0433\u0435\u043d\u0442', 'refresh': None, 'font': {'style': u'bold', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'MS Sans Serif', 'type': u'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': wx.Size(70, 15), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'07396ae5be8d3f45b358890744beac63', 'moveAfterInTabOrder': u'', 'flag': 2048, 'recount': None, 'name': u'default_1172', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 5)}, {'activate': 1, 'show': 1, 'text': u'\u041a\u043e\u043d\u0442\u0440\u0430\u0433\u0435\u043d\u0442', 'refresh': None, 'font': {'style': u'bold', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'MS Sans Serif', 'type': u'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'9cb7e1693d1953657e9fb39048a926ec', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1187', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (2, 5)}, {'activate': 1, 'show': 1, 'text': u'\u0420\u0435\u0433\u0438\u043e\u043d', 'refresh': None, 'font': {'style': u'bold', 'name': u'defaultFont', 'family': u'sansSerif', 'faceName': u'MS Sans Serif', 'type': u'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', '_uuid': u'bc86b1923558257c8c834bed75b913b0', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'default_1203', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (4, 5)}, {'activate': 1, 'ctrl': u"if value:\r\n    _resultEval = spravctrl.CtrlSprav('Region', value, field='cod')", 'pic': u'S', 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': wx.Size(70, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', 'description': None, '_uuid': u'c061aae3515ddf79c9db7ac8788e6083', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'hlp': u"spravctrl.HlpSprav('Region', parentForm=self)", 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'regionEdt', 'changed': None, 'value': u'', 'alias': None, 'init_expr': u'', 'position': (5, 5), 'onInit': None, 'refresh': []}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1289', 'border': 0, '_uuid': u'66d2f46b59622a5fcf3a4377e8c7fea8', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (0, 0), 'type': u'SizerSpace', 'size': wx.Size(11, 27)}, {'activate': 1, 'show': 1, 'refresh': None, 'font': {}, 'border': 0, 'size': wx.Size(105, 64), 'style': 0, 'foregroundColor': (0, 0, 0), 'layout': u'vertical', 'component_module': None, 'selected': 0, 'proportion': 0, 'label': u'\u0415\u0434. \u0438\u0437\u043c.', 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'RadioGroup', 'description': None, 'max': 0, '_uuid': u'c6becec4ee2d44ce82a7f620094352f1', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': None, 'span': (3, 1), 'name': u'meraGrp', 'items': [u'\u0421\u0443\u043c\u043c\u0430 (\u0440\u0443\u0431.)', u'\u041c\u0430\u0441\u0441\u0430 (\u043a\u0433.)'], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 7), 'onInit': None}, {'activate': 1, 'show': 1, 'refresh': None, 'font': {}, 'border': 0, 'size': wx.Size(118, 151), 'style': 0, 'foregroundColor': (0, 0, 0), 'layout': u'vertical', 'component_module': None, 'selected': 0, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0438\u043e\u0434', 'source': None, 'backgroundColor': (255, 255, 255), 'type': u'RadioGroup', 'description': None, 'max': 0, '_uuid': u'6e918e138b37a11be169b4585074726c', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'span': (7, 1), 'name': u'periodGrp', 'items': [u'\u041f\u0435\u0440\u0438\u043e\u0434', u'\u041c\u0435\u0441\u044f\u0446', u'\u041a\u0432\u0430\u0440\u0442\u0430\u043b', u'\u0413\u043e\u0434'], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 9), 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.OnButtonRefresh(evt)', 'font': {}, 'border': 0, 'size': wx.Size(119, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'2de1bb542da94a005d607b0cd0630baf', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'refreshBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (8, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.ClearObjList()', 'font': {}, 'border': 0, 'size': (119, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u0427\u0438\u0441\u0442\u0438\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'8e63210112bbefd3173bc493332825e4', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'clearBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': u'1', 'borderRightColor': (128, 0, 64), 'child': [], 'refresh': None, 'borderTopColor': (128, 0, 64), 'font': {'style': u'regular', 'size': 8, 'underline': False, 'family': u'sansSerif', 'faceName': u'MS Sans Serif'}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(143, 20), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 7), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': (255, 196, 225), 'isSort': False, 'type': u'HeadCell', 'borderWidth': 1, 'description': None, 'shortHelpString': u'', 'backgroundColor2': None, '_uuid': u'bf37ac1728b94c5062b13bd71f325ddf', 'style': 0, 'bgrImage': None, 'flag': 8192, 'recount': None, 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': (128, 0, 64), 'name': u'QueryIndicator', 'borderBottomColor': (128, 0, 64), 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (8, 3), 'borderStyle': None, 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.OnButtonReport(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u0447\u0435\u0442', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'702b2a3196faa98b3a5839a24bbb7d70', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'reportBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 3), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'name': u'GBSizerParam', 'alias': None, 'init_expr': None, 'position': wx.Point(38, 348), 'vgap': 0}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'MonitorPanel', 'keyDown': None, 'alias': None, 'init_expr': u'from NSI import spravctrl', 'position': wx.Point(0, 0), 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 5, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IMonitorPanel'

#   Словарь едениц измерения
graph_type_mera = {0:'РУБ', 1:'КГ'}

#   Словарь типов гистограмм
graph_type_hist = {0:'Сумма',1:'Сравнение',2:'Доля'}

#   Словарь типов периодов наблюдения
ic_period_date = 0
ic_period_month = 1
ic_period_qwart = 2
ic_period_year = 3

#   Словарь соответствий месяцов определенному кварталу
ic_month_qwart_indx = { 1:1, 2:1, 3:1,
                        4:2, 5:2, 6:2,
                        7:3, 8:3, 9:3,
                        10:4, 11:4, 12:4}

graph_type_period = {ic_period_date:'Заданый период',
                    ic_period_month:'Месяц',
                    ic_period_qwart:'Квартал',
                    ic_period_year:'Год'}

#   Цвета в зависимости от индекса
graph_color = ['b','g','r', 'c', 'm', 'y', 'k', 'w',
                (0.8, 0.8, 0.8),
                (1,0.5,0.25),
                (0, 0.5, 1),
                (0, 0.8, 0.7),
                (1, 0, 0.5),
                (0.5, 0.5, 0.8),
                (1, 0.5, 0.8),
                (0.5, 0.5, 0.5)]

class IMonitorPanel:
    def __init__(self, parent):
        self.evalSpace=util.InitEvalSpace()
        
        #   Список сравниваемых позиций
        self._objList = []
        self._objDict = {}

        #   Указатель на класс данных
        self._dataclass = None
        #   Буфер данных, отфильтрованных по дате, региону и агенту
        self._data = None
        #   Буфер обработанных данных, которые отображаются на графике. Является
        #   списком. Элемнты имеют следующую структуру:
        #  (cod, <список коордитат X>, <список коордитат Y>)
        self._report_data = None
        
        #   Список дат периода наблюдения
        self._dtrange = None
        #   Картеж старых параметров запроса (дата1, дата2, менеджер, регион,
        #   список продукции)
        self._oldPar = (None, None, None, None, None)
        
        #   Период наблюдения (data1, data2)
        self.date1 = None
        self.date2 = None
        
        self.evalSpace['WrapperObj'] = self
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=True)
        self.object = self.evalSpace['_root_obj']
        self.init_graph()
        self.GetNameObj('QueryIndicator').Show(False)
        
        btn = self.GetNameObj('refreshBtn')
        btn.Bind(icEvents.EVT_GRID_POST_SELECT, self.RefreshMonitor)
        
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
            
    def AppendObjList(self, cod, name):
        """
        Добавляет в список сравниваемых позиций.
        """
        ctrl = self.GetNameObj('objectsList')
        
        if ctrl:
            #print 'cod=', cod
            nm = name.strip()
            s = '<%s> %s' % (cod, nm)
            #print 'name=', s
            codlst = map(lambda x: x[0], self._objList)
            
            if not cod in codlst:
                ctrl.Append(s)
                self._objList.append((cod, nm))
                self._objDict[cod] = nm
        
    def BarChart(self, title, period=0):
        """
        Гистограмма сравнения.
        """
        if self.date1 >= self.date2:
            print '#### Warnint date2 < date1 !!!!!'
            return False
            
        print '>>> Period=', period, ic_period_month
        # Подготавливаем данные
        data = self.GetDataBuff()
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')

        # Чистим график
        if data:
            #self.GetNameObj('Graph').fig.clear()
            self.GetNameObj('Graph').subplot.cla()
            subplot = self.GetNameObj('Graph').subplot
            xlt = None
            mera_i = self.GetMeraIndx()
            ih = self.GetHistIndx()
            self._report_data = []
            
            #   В зависимости от типа периода формирум разметку оси х
            if period == ic_period_date:
                _xlt = self._dtrange
                xlt = map(lambda x: x[:5], self._dtrange)
                lxlt = len(xlt)
                
                if lxlt > 30:
                    for i in range(lxlt):
                        if i % 3 <> 0:
                            xlt[i] = ''
                            
                elif lxlt > 15:
                    for i in range(lxlt):
                        if i % 2:
                            xlt[i] = ''
                
            elif period == ic_period_month:
                xlt = ('Янв','Фвр','Мрт','Апр','Май','Июн','Июл','Авг','Снт','Окт','Нбр','Дкб')
                _xlt = xlt
            elif period == ic_period_qwart:
                xlt = ('I','II','III','IV')
                _xlt = xlt
            elif period == ic_period_year:
                y1 = self.date1.GetYear()
                y2 = self.date2.GetYear()
                xlt = range(y1, y2+1)
                xlt = map(lambda x: str(x), xlt)
                _xlt = xlt
            #   Формируем гистограмму
            if xlt and subplot:
            
                # Нормализуем данные
                if period == ic_period_date:
                    N = min(len(xlt), len(data[0][1]))
                else:
                    N = len(xlt)
                    
                ind = numerix.arange(N)    # the x locations for the groups
                
                checkLst = self.GetCheckedObjList()
                nh = len(data)
                width = 1.0/float(nh+1)
                
                lineLst = []
                legendLst = []
                maxLst = [0 for x in range(N)]
                
                for indx, obj in enumerate(data):
                    cod, summa, kol, cena, ei = obj
                    _buff = [0 for x in range(N)]
                    print '  >>> CREATING BAR for:', cod
                    
                    if cod in checkLst:
                        clr = graph_color[indx]
                        
                        # Сумма
                        if mera_i == 0:
                            if period == ic_period_date:
                                _buff = summa[:N]

                            elif period == ic_period_month:
                                for i, val in enumerate(summa):
                                    mnth = int(self._dtrange[i][3:5])
                                    _buff[mnth-1] += val
                                    
                            elif period == ic_period_qwart:
                                for i, val in enumerate(summa):
                                    mnth = int(self._dtrange[i][3:5])
                                    qw = ic_month_qwart_indx[mnth]
                                    _buff[qw-1] += val
                                    
                            elif period == ic_period_year:
                                for i, val in enumerate(summa):
                                    year = self._dtrange[i][6:]
                                    ny = xlt.index(year)
                                    _buff[ny] += val
                        # Масса
                        else:
                            if period == ic_period_date:
                                _buff = kol[:N]
                                
                            elif period == ic_period_month:
                                for i, val in enumerate(kol):
                                    mnth = int(self._dtrange[i][3:5])
                                    _buff[mnth-1] += val
                                    
                            elif period == ic_period_qwart:
                                for i, val in enumerate(kol):
                                    mnth = int(self._dtrange[i][3:5])
                                    qw = ic_month_qwart_indx[mnth]
                                    _buff[qw-1] += val

                            elif period == ic_period_year:
                                for i, val in enumerate(kol):
                                    year = self._dtrange[i][6:]
                                    ny = xlt.index(year)
                                    _buff[ny] += val
                            
                        if ih > 0:
                            p = subplot.bar(ind, _buff, width, bottom=maxLst, color=clr)

                            for n, s in enumerate(_buff):
                                maxLst[n] += s
                        else:
                            p = subplot.bar(ind+indx*width, _buff, width, color=clr)

                        #print '>>> <%s> Buff=%s' % (cod, str(_buff))
                        self._report_data.append((cod, _xlt, _buff))
                        lineLst.append(p[0])
                        legendLst.append(self.GetCodName(cod))
                        
                if mera_i == 0:
                    subplot.set_ylabel('Сумма (тыс. руб.)\n')
                else:
                    subplot.set_ylabel('Масса (кг.)\n')
                
                if lineLst:
                    subplot.legend(lineLst, legendLst, 'upper right', shadow=True)
                    
                subplot.set_xticks(ind+0.5)
                subplot.set_xticklabels(xlt[:N])

                cod_reg = self.GetRegionCod()
                cod_agent = self.GetAgentCod()
                reg, agent = (None, None)
                
                if cod_reg:
                    reg = spravctrl.FSprav('Region',cod_reg).strip()
                    
                if cod_agent:
                    agent = spravctrl.FSprav('Menager',cod_agent).strip()
                
                if reg and agent:
                    subplot.set_title('Реализация, %s, %s' % (agent, reg))
                elif reg:
                    subplot.set_title('Реализация, %s' % reg)
                elif agent:
                    subplot.set_title('Реализация, %s' % agent)
                else:
                    subplot.set_title('Реализация продукции')
                    
    def BarPart(self):
        """
        Гистограмма, отражающая долю в сумме.
        """
        pass
        
    def ClearObjList(self):
        """
        Чистим список сравниваемых позиций.
        """
        ctrl = self.GetNameObj('objectsList')
        
        if ctrl:
            ctrl.Clear()
        
        self._objList = []
        
    def GetCheckedObjList(self):
        """
        Возвращает список отмеченных для отображения на графике позиций.
        """
        ctrl = self.GetNameObj('objectsList')
        lst = self.GetObjList()
        check_lst = []
        
        for indx, ob in enumerate(lst):
            if ctrl.IsChecked(indx):
                check_lst.append(ob[0])

        return check_lst
        
    def GetAgentCod(self):
        """
        Возвращает код агента (менеджера).
        """
        obj = self.GetNameObj('agentEdt')
        
        if obj:
            return obj.GetValue()

        return None
        
    def GetCodName(self, cod):
        """
        По коду возвращает наименование продукции.
        """
        if self._objDict.has_key(cod):
            return self._objDict[cod]
            
    def GetContragentCod(self):
        """
        Возвращает код контрагента.
        """
        obj = self.GetNameObj('contragentEdt')
        
        if obj:
            return obj.GetValue()

        return None

    def GetDataclass(self):
        """
        Возвращает указатель на интерфейс работы с источником данных.
        """
        if not self._dataclass:
            self._dataclass = tabclass.CreateTabClass('analitic')
            
        return self._dataclass

    def GetDataBuff(self):
        """
        Возвращает буфер данных, по которому строится гистограмма.
        """
        return self._data

    def GetDateRangeLst(self):
        """
        Возвращает список дат между максимальной и минммальной датой.
        """
        matplotlib.rcParams['timezone'] = 'US/Pacific'
        tz = timezone('US/Pacific')

        dt = datetime.timedelta(days=1)
        
        y1 = self.date1.GetYear()
        m1 = self.date1.GetMonth()+1
        d1 = self.date1.GetDay()
        tt1 = datetime.datetime(int(y1), int(m1), int(d1), tzinfo=tz)
        
        y2 = self.date2.GetYear()
        m2 = self.date2.GetMonth()+1
        d2 = self.date2.GetDay()
        print '>>> date2=', y2, m2, d2
        tt2 = datetime.datetime(int(y2), int(m2), int(d2), tzinfo=tz)
        
        dates = drange(tt1, tt2, dt)
        
        lst = []
        for d in dates:
            dt1 = num2date(d)
            y1 = str(dt1.year)
            m1 = ('00'+ str(dt1.month))[-2:]
            d1 = ('00'+ str(dt1.day))[-2:]
            
            lst.append('%s.%s.%s' % (d1, m1, y1))
            
        return lst

    def GetGraphDataBuff(self):
        """
        Возвращает буфер данных, по которому строится гистограмма.
        """
        return self._report_data
        
    def GetHistIndx(self):
        """
        Возвращает индекс выбанного пункта из списка типов гистограмм.
        """
        obj = self.GetNameObj('typeHistGrp')
        
        if obj:
            return obj.GetSelection()

        return None
        
    def GetMeraIndx(self):
        """
        Возвращает индекс выбанного пункта из списка едениц измерений.
        """
        obj = self.GetNameObj('meraGrp')
        
        if obj:
            return obj.GetSelection()

        return None

    def GetPeriodIndx(self):
        """
        Возвращает индекс выбанного пункта из списка периодов наблюдения.
        """
        obj = self.GetNameObj('periodGrp')
        
        if obj:
            return obj.GetSelection()

        return None
    
    def GetObjList(self):
        """
        Возвращает список сравниваемых позиций.
        """
        return self._objList
    
    def GetRegionCod(self):
        """
        Возвращает код контрагента.
        """
        obj = self.GetNameObj('regionEdt')
        
        if obj:
            return obj.GetValue()

        return None

    def init_graph(self):
        """
        Инициализация графика.
        """
        N = 5
        menMeans   = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd     = (2, 3, 4, 1, 2)
        womenStd   = (3, 5, 2, 3, 3)
        ind = numerix.arange(N)    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence
        obj = self.GetNameObj('Graph')
        
        self.ClearObjList()

    def OnButtonRefresh(self, evt):
        """
        Обрабатываем нажатие копки <Обновить>.
        """
        self.SetIndicatorText('Подождите обрабатывается запрос ...')
        self.RefreshMonitor(None)
        
#        btn = self.GetNameObj('refreshBtn')
#        event = icEvents.icGridPostSelectEvent(icEvents.icEVT_GRID_POST_SELECT, btn.GetId())
#        btn.GetEventHandler().AddPendingEvent(event)
        
    def OnButtonReport(self, evt):
        """
        Обрабатываем нажатие кнопки <Отчет>
        """
        # Создаем отчет
        self.RefreshMonitor(None)
        
        msg = ''
        buffLst = self.GetGraphDataBuff()
        indx = self.GetMeraIndx()
        
        for obj in buffLst:
            cod, xLst, yLst = obj
            name = self.GetCodName(cod)
            
            if indx == 0:
                msg = '%s---- <%s>:  %s ----- Сумма в руб.\n' % (msg, cod, name)
                f = 1000
            else:
                msg = '%s---- <%s>:  %s ----- Вес в кг.\n' % (msg, cod, name)
                f = 1
                
            for i, xx in enumerate(xLst):
                yy = yLst[i]
                msg = '%s%s:    %s\n' % (msg, xx, str(yy*f))
            
        prnt = self.GetNameObj('MonitorPanel')
        dlg = wx.lib.dialogs.ScrolledMessageDialog(prnt, msg, 'Отчет по реализации продукции')
        dlg.ShowModal()
        dlg.Destroy()

    def PrepareBuff(self):
        """
        Подготавливается буфер за период.
        """
        #   Получаем спискок отмеченных позиций
        obj_lst = self.GetObjList()
        prnt = self.GetNameObj('MonitorPanel')
        
        if not obj_lst:
            msgbox.MsgBox(prnt, "Выберите список позиций")
            return False
            
        #   Код региона
        reg = self.GetRegionCod()
        
        #   Код менеджера
        agent = self.GetAgentCod()
        if agent:
            agent = '0'+self.GetAgentCod()

#        if not agent:
#            msgbox.MsgBox(prnt, "Выберите менеджера")
#            return False
        
        #   Пока не используется
        contragent = self.GetContragentCod()

        dt1 = self.GetNameObj('date1').GetValue()
        y1 = str(dt1.GetYear())
        m1 = ('00'+ str(dt1.GetMonth()+1))[-2:]
        d1 = ('00'+ str(dt1.GetDay()))[-2:]
        t1 = '%s.%s.%s' % (y1, m1, d1)

        dt2 = self.GetNameObj('date2').GetValue()
        y2 = str(dt2.GetYear())
        m2 = ('00'+ str(dt2.GetMonth()+1))[-2:]
        d2 = ('00'+ str(dt2.GetDay()))[-2:]
        t2 = '%s.%s.%s' % (y2, m2, d2)

        tb = time.clock()
        
        #--- Создаем буфер
        cl = self.GetDataclass()
        _buff = []
#        indxCtrl = self.GetNameObj('QueryIndicator')
#        indxCtrl.Show(True)
#        indxCtrl.GetParent().Refresh()
        
        for obj in obj_lst:
            cod, name = obj
            print '>>>> Prepare buff t1,t2, cod, reg, agent = ', t1,t2, cod, reg, agent
            self.SetIndicatorText('Обр. запроса по: <%s> %s' % obj)
            
            if agent == '999' or not agent and reg:
                rs = cl.select(sqlobject.AND(cl.q.codt.startswith(cod),
                                cl.q.dtoper >= t1,
                                cl.q.dtoper <= t2,
                                cl.q.reg == reg))
            elif agent == '999' or not agent and not reg:
                rs = cl.select(sqlobject.AND(cl.q.codt.startswith(cod),
                                cl.q.dtoper >= t1,
                                cl.q.dtoper <= t2))
            elif agent and not reg:
                rs = cl.select(sqlobject.AND(cl.q.codt.startswith(cod),
                                cl.q.dtoper >= t1,
                                cl.q.dtoper <= t2,
                                cl.q.mens == agent))
            else:
                rs = cl.select(sqlobject.AND(cl.q.codt.startswith(cod),
                                cl.q.dtoper >= t1,
                                cl.q.dtoper <= t2,
                                cl.q.mens == agent,
                                cl.q.reg == reg))
            lrs = rs.count()
            dtrange = self.GetDateRangeLst()
            summaBuff = [0 for x in range(len(dtrange))]
            kolfBuff = [0 for x in range(len(dtrange))]
            
            if lrs > 0:
                for i, r in enumerate(rs):
                    dtoper, kolf, summa, cena, ei = (r.dtoper, r.kolf, r.summa, r.cena, r.ei)
                
                    l = dtoper.split('.')
                    dtoper = '%s.%s.%s' % (l[2], l[1], l[0])
                    
                    if dtoper in dtrange:
                        indx = dtrange.index(dtoper)
                        
                        if indx >= 0:
                            summaBuff[indx] += summa/1000.
                            kolfBuff[indx] += kolf
                    
            _buff.append((cod, summaBuff, kolfBuff, (), ()))
                
        self._data = _buff
        self._dtrange = dtrange
        #print '>>> PREPARE DATA:', self._data
        return True
    
    def RefreshMonitor(self, evt):
        """
        Обновляет информацию, отображаемую на мониторе.
        """
        print '>>> RefreshMonitor'
        d1, d2, oag, oreg, olstLen = self._oldPar
        
        self.date1 = self.GetNameObj('date1').GetValue()
        self.date2 = self.GetNameObj('date2').GetValue()
        reg = self.GetRegionCod()
        agent = self.GetAgentCod()
        obj_lst = self.GetObjList()
    
        if (d1 <> self.date1 or d2 <> self.date2 or oag  <> agent or
            oreg <> reg or len(obj_lst) <> olstLen):
            self.PrepareBuff()
            self._oldPar = self.date1, self.date2, agent, reg, len(obj_lst)
            
        self.BarChart('Title', self.GetPeriodIndx())
        self.GetNameObj('Graph').canvas.draw()

        indxCtrl = self.GetNameObj('QueryIndicator')
        indxCtrl.Show(False)
        indxCtrl.Refresh()
        
    def SetIndicatorText(self, text = ''):
        """
        Устанавливает текст в окне индикатора запроса.
        """
        indxCtrl = self.GetNameObj('QueryIndicator')
        indxCtrl.Show(True)
        indxCtrl.SetLabel(text)
        evt = wx.PaintEvent(indxCtrl.GetId())
        return indxCtrl.GetEventHandler().ProcessEvent(evt)
        
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
    
