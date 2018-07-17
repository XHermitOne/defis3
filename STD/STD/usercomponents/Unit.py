#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Универсальный блок описания.
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.PropertyEditor.icDefInf as icDefInf
import ic.components.icwidget as icwidget
import STD.reestr_img as reestr_img
import ic.components.icResourceParser as prs

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CUnit')

ic_class_spc = {'name':'defaultUnit',
                'type':'Unit',
                'unit_id':None,
                'value':None,
                'default':None,
                'child':[],
                '__brief_attrs__': ['name', 'value'],
                '__parent__':icwidget.SPC_IC_SIMPLE}

ic_class_pic = reestr_img.Item
ic_class_pic2 = reestr_img.Item
#ic_can_contain = ['Unit']

class CUnit(icwidget.icSimple):
    """
    Описание пользовательского компонента.

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
        self.value = component['value']
        self.unit_id = component['unit_id']
        self.default = component['default']
        self.child = component['child']
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """

        #print '>>> Begin parse:', self.evalSpace.keys()
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace,
                                bCounter = bCounter, progressDlg = progressDlg)

    def getChildValue(self,ChildName_):
        """
        Получить значение дочернего юнита по его имени.
        @param ChildName_: Имя дочернего юнита.
        """
        child=None
        if ChildName_ in self.components:
            child=self.components[ChildName_]
        #print 'DBG UNIT',ChildName_,child,type(ChildName_),self.components.keys()
        if child is not None:
            return child.value
        return None
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

def test(par=0):
    """
    Тестируем класс CUnit.
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