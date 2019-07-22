#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx

import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import plan.interfaces.IODBSprav as IODBSprav
import ic.utils.coderror as coderror
import ic.dlg.msgbox as msgbox
import ic.utils.system_cache as ic_cache

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043b\u0430\u043d\u0430\u043c\u0438', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'description': None, 'onClose': u'WrapperObj.OnCloseFuncMainPanel(evt)', '_uuid': u'5f370f0ca6ec800ea503368fd26e87ad', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'1f616cefe3430ad89360748ce453c49c', 'proportion': 0, 'name': u'DefaultName_1881_2163', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'line_color': (200, 200, 200), 'activate': 1, 'show': 1, 'cols': [{'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncCod(self.GetView(), value, row, evt)', 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u041a\u043e\u0434', 'width': 70, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'e460e88b88b1011ff07ffb4f6bac3c0c', 'recount': None, 'getvalue': u'', 'name': u'cod', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'05baa37b6a260390c1c221eab2e5191b', 'recount': None, 'hlp': None, 'name': u'description', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': None, 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', 'width': 100, 'init': None, 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'544e7b46067f8bd0fb1bf7b0e4b1df52', 'recount': None, 'getvalue': u'', 'name': u'source', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'ctrl': u'WrapperObj.ctrlFuncStruct(self.GetView(), value,evt)', 'pic': u'S', 'hlp': None, 'style': 0, 'component_module': None, 'label': u'\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430', 'width': 100, 'init': u'@WrapperObj.initFuncStruct(evt)', 'valid': None, 'type': u'GridCell', 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'shortHelpString': u'', '_uuid': u'6912182bb0115da1ca814fcec2ffba90', 'recount': None, 'getvalue': u'', 'name': u'struct', 'setvalue': u'', 'attr': u'W', 'keyDown': None, 'alias': None, 'init_expr': None}], 'keyDown': None, 'border': 0, 'post_select': None, 'size': (-1, -1), 'moveAfterInTabOrder': u'', 'dclickEditor': None, 'span': (1, 1), 'delRec': None, 'component_module': None, 'row_height': 20, 'selected': None, 'proportion': 1, 'init': None, 'label': u'Grid', 'source': None, 'getattr': None, 'backgroundColor': None, 'fixRowSize': 0, 'type': u'GridDataset', '_uuid': u'4307aebec9938818118ee03a839d97e8', 'fixColSize': 0, 'description': None, 'post_del': None, 'post_init': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'cell_attr', 'alignment': (u'left', u'middle')}, 'style': 0, 'docstr': u'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': None, 'label_attr': {'foregroundColor': (0, 0, 0), 'name': u'', '_uuid': u'fc33020efab49628ee1db46207ea5d88', 'backgroundColor': None, 'font': {'style': None, 'name': u'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': u'', 'type': u'Font', 'underline': 0, 'size': 8}, 'type': u'label_attr', 'alignment': (u'left', u'middle')}, 'name': u'modPlanGrid', 'label_height': 20, 'changed': None, 'onSize': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'', 'refresh': None}, {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, 55), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': None, '_uuid': u'6de57653ac102a5570e6662d5a2acb80', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'text': u'\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u0431\u0430\u0437\u043e\u0432\u043e\u0433\u043e \u043f\u043b\u0430\u043d\u0430: []', 'refresh': None, 'font': {'faceName': u'Tahoma', 'style': u'bold', 'underline': False, 'family': u'sansSerif', 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'description': None, '_uuid': u'0ed6a16e6e92e1621166109fe5f67a32', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'basePlanStruct', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(11, 7), 'onInit': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncReCountBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u043c\u043e\u0434\u0438\u0444. \u0437\u0430 \u043c\u0435\u0441\u044f\u0446', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'adb266de4aef409dad7019f0f68c2c86', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'ReCountBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(8, 32), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncReCountYearBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(157, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u043c\u043e\u0434\u0438\u0444. \u0437\u0430 \u0433\u043e\u0434', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'description': None, '_uuid': u'3173aa94a99f059912e42561b5c9d60e', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'ReCountYearBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(164, 32), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncReCountAllMnthBtn(evt)', 'font': {}, 'border': 0, 'size': wx.Size(182, 23), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u0435\u0440\u0435\u0441\u0447\u0435\u0442 \u0432\u0441\u0435\u0445 \u043c\u043e\u0434\u0438\u0444. \u0437\u0430 \u043c\u0435\u0441\u044f\u0446', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'9b09e3af00056babe16b962374e5b7b7', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'ReCountAllMnthBtn', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(325, 32), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'name': u'defaultWindow_2066', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(0, 371), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': None, 'name': u'ManageDialog', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u'WrapperObj.OnInitFuncMainPanel(evt)'}

#   Версия объекта
__version__ = (1, 1, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IManagePlans'


class IManagePlans(icobjectinterface.icObjectInterface):
    """
    Интерфейс к форме управления планов.
    """
    def __init__(self, parent, modifyPlanDict=None, metaplan_lst=None, 
                 browser=None, plan_sys='Modif3'):
        """
        Конструктор интерфейса.
        
        @type modifyPlanDict: C{dictionary}
        @param modifyPlanDict: Словарь описаний модификаций.
        @type metaplan_lst: C{list}
        @param metaplan: Описание структуры базового плана.
        @type browser: C{icobjectinterface.icObjectInterface}
        @param browser: Интерфейс к браузеру системы планирования.
        @param plan_sys: Имя системы планирования, определяет имя хранилища, где
            будут храниться описания модификаций планов.
        """
        #
        self.plan_sys = plan_sys
        self.data = modifyPlanDict
        self.metaObj = None
        self.metaplan_lst = metaplan_lst
        
        #   Указатель на интерфейс браузера системы планирования
        self._brows = browser
        
        #   Чистим буфер класса
        ic_cache.systemCache.clear(ic_class_name)
        
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
            
        # print ' ............ metaplan list:', metaplan_lst
        if self.metaplan_lst:
            
            ctrl = self.GetNameObj('basePlanStruct')
            ctrl.SetLabel('Структура базового плана: %s' % str(self.metaplan_lst))
            
    def getBrowserInterface(self):
        """
        Возвращяет указатель на интерфейс к браузеру системы планирования.
        """
        return self._brows
        
    ###BEGIN EVENT BLOCK
    def OnInitFuncMainPanel(self, evt):
        """
        Функция обрабатывает событие <onInit на диалоговом окне>.
        """
        cls = IODBSprav.IODBSprav(None)
        sprav = cls.getObject()
        # print '****** self.plan_sys=', self.plan_sys
        if self.plan_sys in sprav:
            self.metaObj = sprav[self.plan_sys]
            # print '>>>> ..... Find plan modifications File'
        else:
            self.metaObj = sprav.Add(self.plan_sys, 'planModif')
            # print '>>>> ..... Create File for plan modifications'
            self.metaObj.value.modifications = [['', '', '', '']]
            
        # print '-------- sprav:', self.metaObj.value.modifications
        self.LoadData(self.metaObj.value.modifications)
            
        return None
    
    def OnCloseFuncMainPanel(self, evt):
        """
        Функция обрабатывает событие <OnClose>.
        """
        #   Сохраняем изменения
        self.SaveData()
        return None
    
    def ctrlFuncCod(self, grid, value, row, evt):
        """
        Функция обрабатывает событие <ctrl> на поле cod.
        """
        lst = [r[0] for r in grid.dataset.data ]
        
        if value in lst and row != lst.index(value):
            msgbox.MsgBox(grid, u'Идентификатор плана %s уже существует' % value)
            return coderror.IC_CTRL_FAILED_IGNORE
            
        return None
    
    def ctrlFuncStruct(self, grid, value, evt):
        """
        Функция обрабатывает событие <ctrl> на поле struct.
        """
        try:
            lst = eval(value)
            
            if len(lst) < 3 or lst[1] != 'mYear' or lst[2] != 'mMonth':
                msgbox.MsgBox(grid,
                              u'Ошибка в описании структуры плана; 2-ым и 3-им элементом должны быть \'mYear\' и \'mMonth\'')
                return coderror.IC_CTRL_FAILED_IGNORE
                
            if self.metaplan_lst is not None:
                for x in lst:
                    if x not in self.metaplan_lst:
                        msgbox.MsgBox(grid,
                                      u'Тип узла <%s>. не определен в базовом плане' % x)
                        return coderror.IC_CTRL_FAILED_IGNORE

        except:
            msgbox.MsgBox(grid,
                          u'Ошибка в описании структуры модификации плана%s.' % value)
            return coderror.IC_CTRL_FAILED_IGNORE
            
        return None
    
    def mouseClickFuncReCountBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на компоненте ReCountBtn.
        """
        #   Получаем указатель на интерфейс браузера
        ibrows = self.getBrowserInterface()
        
        if ibrows and ibrows.recountFunc:
            #   Сохраняем таблицу в хранилище
            self.SaveData()
            #   Получаем указатель на базовый план
            # metaplan = ibrows.setMetaplanById()
            
            #   Вызываем функцию пересчета
            grid = self.GetNameObj('modPlanGrid')
            row = grid.GetGridCursorRow()
            id_modif_plan = grid.GetTable().GetValue(row, 0)
            
            if id_modif_plan:
                ibrows.recountFunc(self.GetNameObj('ManageDialog'), ibrows, id_modif_plan)
            
        return None
            
    def initFuncStruct(self, evt):
        """
        Функция обрабатывает событие <init> на поле <struct>.
        """
        return str(self.metaplan_lst[:3])
    
    def mouseClickFuncReCountYearBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на кнопке ReCountYearBtn.
        Производится пересчет модификаций плана за год.
        """
        #   Получаем указатель на интерфейс браузера
        ibrows = self.getBrowserInterface()
        
        if ibrows and ibrows.recountModifPlanYear:
            #   Сохраняем таблицу в хранилище
            self.SaveData()
        
            #   Вызываем функцию пересчета
            grid = self.GetNameObj('modPlanGrid')
            row = grid.GetGridCursorRow()
            id_modif_plan = grid.GetTable().GetValue(row, 0)
            
            if id_modif_plan:
                ibrows.recountModifPlanYear(self.GetNameObj('ManageDialog'), ibrows, id_modif_plan)
    
    def mouseClickFuncReCountAllMnthBtn(self, evt):
        """
        Функция обрабатывает событие <mouseClick> на кнопке ReCountAllMnthBtn.
        Производится пересчет всех модификаций плана за месяц.
        """
        #   Получаем указатель на интерфейс браузера
        ibrows = self.getBrowserInterface()
        
        if ibrows and ibrows.recountAllModifPlanMnth:
            #   Сохраняем таблицу в хранилище
            self.SaveData()
        
            #   Вызываем функцию пересчета
            grid = self.GetNameObj('modPlanGrid')
            modif_lst = [r[0] for r in grid.dataset.data]
            
            if modif_lst:
                ibrows.recountAllModifPlanMnth(self.GetNameObj('ManageDialog'), ibrows, modif_lst)

    ###END EVENT BLOCK
    def LoadData(self, data=None):
        """
        Функция читает таблицу из хранилища.
        """
        if not data:
            data = self.data
            
        grid = self.GetNameObj('modPlanGrid')
        grid.dataset.SetDataBuff(data)
        grid.RefreshGrid()

    def SaveData(self):
        """
        Функция сохраняет таблицу в хранилище.
        """
        #   Сохраняем изменения
        if self.metaObj:
            self.metaObj.value.modifications = self.GetNameObj('modPlanGrid').dataset.data

            # print '------ SaveAllChildren()', self.metaObj.value.modifications
            # self.metaObj.setValueChanged(True)
            self.metaObj.SaveAllChildren()
            self.metaObj.Close()
        return None


def test(par=0):
    """
    Тестируем класс new_form.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
#    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
    cls = IManagePlans(frame)
    
    data = [('p1', 'plan1', 'p1', "['a1','a2', 'a3']"),
            ('p2', 'plan2', 'p2', "['a1','a3', 'a2']")]
    cls.LoadData(data)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
