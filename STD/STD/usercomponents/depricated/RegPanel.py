#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Трехоконная стилизованная панель (состоит из шапки, клиентской часть, подвала).
Используется в браузере реестров документов (TreeReestrBrowser).
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.PropertyEditor.icDefInf as icDefInf
import ic.utils.util as util
import copy
import ic.components.icwxpanel as icwxpanel
import ic.kernel.icobject as icobject
import ic.kernel.ickernel as ickernel
import ic.utils.ic_cache as ic_cache
from ic.kernel import io_prnt
from ic.dlg import msgbox
import  wx.lib.anchors as anchors

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CRegPanel')

ic_class_spc = {'name':'defaultPanel',
                'type':'RegPanel',
                'backgroundColor': None,
                'nest':'Panel:clientRgPanel',
                'foregroundColor': (150, 150, 150),
                '__attr_types__': {0: ['name', 'type'],
                        icDefInf.EDT_COLOR: ['backgroundColor', 'foregroundColor']},
                '__lists__':{'nest':['Panel:topRgPanel',
                                    'Panel:clientRgPanel',
                                    #'GridBagSizer:clientRgSizer',
                                    'BoxSizer:clientRgSizer',
                                    'Panel:bottomRgPanel']},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}

#   Список компонентов, которые могут содержаться в компоненте
#   Вставлять объекты можно только через функцию
ic_can_contain = []
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'child': [{'hgap': u'5', 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': wx.Point(42, 49), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'92018da56175263d3b3fd74aba1670db', 'proportion': 1, 'name': u'TopBSZR', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'0bf85c48e32b316ff7b8b78588faef58', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'topRgPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}, {'activate': 1, 'show': 1, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'a0d3c183d30c823ecc5d3b9dcc4004ed', 'proportion': 1, 'name': u'clientRgSizer', 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'style': 0, 'activate': 1, 'span': (1, 1), 'description': None, 'component_module': None, 'type': u'SizerSpace', '_uuid': u'a58138733eaedfe090a740739f485385', 'proportion': 0, 'name': u'DefaultName_4519', 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 0)}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}, {'activate': u'0', 'minCellWidth': 5, 'minCellHeight': 5, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [0], 'component_module': None, 'flexCols': [0], 'proportion': 1, 'type': u'GridBagSizer', 'hgap': 0, 'description': None, '_uuid': u'5bf664afb79a5cee457bb63e0e022ca1', 'flag': 8192, 'child': [{'style': 0, 'activate': u'0', 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'909762d9efd6a1d7defa8fa9737c3edd', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (1, 2), 'size': (5, 5), 'type': u'SizerSpace', 'name': u'DefaultName_2281'}, {'style': 0, 'activate': u'0', 'span': (1, 1), 'description': None, 'component_module': None, 'border': 0, '_uuid': u'545158f7e7f681daf9ff9e70317527a6', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (2, 1), 'size': (5, 5), 'type': u'SizerSpace', 'name': u'DefaultName_2391'}], 'name': u'clientRgSizer2', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (223, 235, 242), 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'9faf1223d489eb4171d429b7eb7ec7e0', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'clientRgPanel', 'refresh': None, 'alias': None, 'init_expr': u'#self.SetRoundBoundMode((100, 128, 192), 2)', 'position': wx.Point(0, 20), 'onInit': None}, {'activate': 1, 'show': 1, 'child': [], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'a92e4bbcace16acba2e6c83f3494926d', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'bottomRgPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 40), 'onInit': None}, {'activate': 1, 'show': u'0', 'child': [], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'268554402b2db18de90f2e2db46dd588', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'unvisiblePanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(221, 327), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': u'5', 'size': (-1, -1)}], 'keyDown': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'description': None, 'onClose': None, '_uuid': u'd75d382ef1b5325357b620ec63cf52ce', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': u'RegPanel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'GetInterface().OnInit()'}

#   Версия объекта
__version__ = (1, 0, 6, 1)
###END SPECIAL BLOCK

class CRegPanel(ictemplate.icTemplateInterface):
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
        self.foregroundColor = component['foregroundColor']
        self.backgroundColor = component['backgroundColor']
        
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        self._init_color_style()
        self.last = None
    
        # Картеж: <имя формы>, <имя подсистемы>
        self._form = None
        # Указаткль на объект реестра
        self._obj = None
        
        #   Буфер панелей редактирования объектов
        self.objBuff = ic_cache.icCache(self.__class__.__name__)
        self.objBuff.clear(self.__class__.__name__)
        
    def _init_color_style(self):
        """
        Переопределяются цвета клиентской панели.
        """
        cl_res = self.GetObjectResource('clientRgPanel')
        
        cl_res['foregroundColor']  = self.foregroundColor
        cl_res['backgroundColor']  = self.backgroundColor

    def init_component(self, context=None):
        """
        Инициализация компонента. Вызывается парсером после создания компонента.
        """
        if context and self.foregroundColor:
            for obj in self._reg_objects.values():
                if obj.name == 'clientRgPanel':
                    #obj.SetRoundBoundMode(self.foregroundColor, 2)
                    obj.SetBorderMode(self.foregroundColor, 2)
                    break
                    
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def create_obj(self, name, subsys=None):
        """
        Создаем объект.
        
        @param name: Имя формы.
        @param subsys: Имя подсистемы.
        """
        
        # Взять из буфера
        hash_id = '%s:%s' % (name, subsys)
        if self.objBuff.hasObject(self.__class__.__name__, hash_id):
            print('>>> GET FROM BUFFER:', hash_id)
            return self.objBuff.get(self.__class__.__name__, hash_id)
        
        kernel = self.GetContext().get_kernel()
        
        if not kernel:
            kernel = ickernel.icKernel()

        if kernel:
            prnt = self.getRegObj('unvisiblePanel')
            pspf = icobject.getResPSP(name+'.frm', subsys, self.GetInterfaceName())
            obj = kernel.Create(pspf, parent=prnt)
            self.objBuff.add(self.__class__.__name__, hash_id, obj)
            return obj

    def OnInit(self):
        """
        Инициализация формы.
        """
        pass

    def init_panel(self):
        """
        Инициализация панели.
        """
        if self._form:
            #   Получаем указатель на ядро
            name, subsys = self._form
            win = self.create_obj(name, subsys)
            if win:
                self.SetPanel(win)

            # Вызываем у объекта функцию чтения данных на форму
            if self._obj:
                if hasattr(self._obj.metaitem.value, 'doc_uuid') and self._obj.metaitem.value.doc_uuid:
                    io_prnt.outLog(u'>>> Загружаем документ UUID=%s' % self._obj.metaitem.value.doc_uuid)
                    self._obj.load(self._obj.metaitem.value.doc_uuid)
                    self._obj.startEdit()

                    if not self._obj.isMyLock():
                        msgbox.MsgBox(win, u'Документ заблокирова пользователем %s' % self._obj.ownerLock())
                        
                ifs = win.GetComponentInterface()
                if ifs:
                    ifs.set_object(self._obj)
                    ifs.LoadData()
                
#                ifs = win.GetComponentInterface().GetComponentInterface()
#
#                # Если форма на базе шаблона
#                if ifs:
#                    ifs.set_object(self._obj)
#                    ifs.LoadData()
#                # Панель должна быть сделана на базе шаблона STD.EditObjPanel.py
#                elif win.GetComponentInterface():
#                    win.GetComponentInterface().set_object(self._obj)
#                    win.GetComponentInterface().LoadData()
                    
        
    def SetEditPanel(self, obj, subsys='STD'):
        """
        Создает панель редактирования.
        
        @param name: Имя формы.
        @type obj: C{icObject}
        @param obj: Указатель на объект реестра.
        @param subsys: Имя подсистемы.
        """
        if obj:
            print('========== SET EDIT PANEL ==============')
            # Сохраняем данные на текущей форме
            if self.last:
                ifs = self.last.GetComponentInterface()
                if ifs:
                    ifs.SaveData()
                    self._obj.stopEdit()
                    
            # Устанавливаем новую
            self._form = (obj.GetEditForm(), subsys)
            self._obj = obj
            wx.CallAfter(self.init_panel)

    def SetPanel3(self, obj):
        """
        Вставляет оконный объект на клиентскую панель.
        """
        # Получаем указатель на сайзер (GridBagSizer)
        pnl = self.getRegObj('clientRgPanel')
        bszr = self.getRegObj('clientRgSizer')
        clientPos = (1,1)
        clientSpan = (1,1)

        if self.last:
            # Сохраняем изменения
            
            # Удаляем старую форму
            self.last.Show(False)
            bszr.Remove(self.last)
            self.last = None
            
        obj.Reparent(pnl)
        bszr.Add(obj, clientPos, clientSpan, wx.EXPAND, 1)
        obj.Show()
        self.last = obj
        bszr.Layout()

    def SetPanel(self, obj):
        """
        Вставляет оконный объект на клиентскую панель.
        """
        # Получаем указатель на сайзер (GridBagSizer)
        pnl = self.getRegObj('clientRgPanel')
        bszr = self.getRegObj('clientRgSizer')
        #clientPos = (1,1)
        clientPos = (0,0)
        clientSpan = (1,1)

        if self.last:
            # Сохраняем изменения
            
            # Удаляем старую форму
            self.last.Show(False)
            bszr.Detach(self.last)
            self.last = None
            
        obj.Reparent(pnl)
        bszr.Add(obj, 1, wx.EXPAND | wx.ALL, 5)
        obj.Show()
        self.last = obj
        bszr.Layout()

    def SetPanel2(self, obj):
        """
        Вставляет оконный объект на клиентскую панель.
        """
        # Получаем указатель на сайзер (GridBagSizer)
        pnl = self.getRegObj('clientRgPanel')
        #bszr = self.getRegObj('clientRgSizer')
        pnl.SetAutoLayout(True)
        clientPos = (1,1)
        clientSpan = (1,1)

        if self.last:
            # Сохраняем изменения
            
            # Удаляем старую форму
            self.last.Show(False)
            #bszr.Remove(self.last)
            self.last = None
            
        obj.Reparent(pnl)
        #bszr.Add(obj, clientPos, clientSpan, wx.EXPAND, 1)
        obj.SetPosition((5,5))
        obj.SetConstraints(anchors.LayoutAnchors(obj, True, True, True, True))
        obj.Show()
        self.last = obj
        #bszr.Layout()
            
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CRegPanel.
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