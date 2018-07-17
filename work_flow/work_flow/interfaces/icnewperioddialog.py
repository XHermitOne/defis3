#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
from ic.utils import ic_res

### !!!! NO CHANGE !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource={'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': 'e505e146fbb908d94af06de53acfe260', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'minCellWidth': 10, 'data_name': None, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 5, 'proportion': 0, 'type': 'GridBagSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': 'f3f41845404caba3fd7ac1772d7e1844', 'flag': 8192, 'child': [{'activate': u'1', 'obj_module': None, 'show': 1, 'text': u'\u0421\u0443\u0431\u044a\u0435\u043a\u0442:', 'data_name': None, 'keyDown': None, 'font': {'faceName': u'Tahoma', 'style': 'regular', 'underline': False, 'family': 'sansSerif', 'size': 8}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'faafeaa1728d592fae1b19ac847dcb6a', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'subject_label', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'recount': None, 'is_choice_list': False, 'set_selected_code': None, 'keyDown': None, 'border': 0, 'size': (350, -1), 'level_enable': -1, 'moveAfterInTabOrder': '', 'view_all': False, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'SpravTreeComboCtrl', 'popup_type': 0, 'get_label': None, 'enable': True, 'description': None, '_uuid': '374f58c620024d1f54d1c0714fad40ec', 'style': 0, 'flag': 8192, 'foregroundColor': None, 'root_code': None, 'child': [], 'sprav': None, 'res_module': None, 'name': u'subject_choice', 'find_item': None, 'data_name': u'subj_cod', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (1, 2), 'onInit': u'None', 'get_selected_code': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'text': u'\u041d\u0430\u0447\u0430\u043b\u043e:', 'data_name': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'enable': True, 'description': None, '_uuid': '04ecf4b801565e79f0dc0d6146c350f7', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'begin_date_label', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (3, 1), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'data_name': u'begin_date', 'keyDown': None, 'border': 0, 'size': (350, -1), 'style': 2, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': 'DatePickerCtrl', 'res_module': None, 'enable': True, 'onDateChanged': None, 'description': None, '_uuid': 'cf26cac994236e76ae47ef86092c3d4b', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'begin_date_edit', 'value': '', 'alias': None, 'init_expr': None, 'position': (3, 2), 'onInit': None, 'refresh': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': u'end_period', 'keyDown': None, 'border': 0, 'check': u'GetInterface().onEndPeriodCheck(event)', 'size': (-1, -1), 'uncheck': u'GetInterface().onEndPeriodUncheck(event)', 'style': 33554432, 'foregroundColor': None, 'checked': 0, 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u043a\u0440\u044b\u0442\u044c \u043f\u0435\u0440\u0438\u043e\u0434', 'source': None, 'backgroundColor': None, 'type': 'CheckBox', 'res_module': None, 'enable': True, 'loseFocus': None, 'description': None, '_uuid': '461bd655c15e757b30f824e932ec39ab', 'moveAfterInTabOrder': '', 'flag': 0, 'recount': [], 'span': (1, 2), 'field_name': None, 'attr': None, 'setFocus': None, 'name': u'end_period_check', 'refresh': [], 'init_expr': None, 'position': (5, 1), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'text': u'\u041e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u0435:', 'data_name': None, 'refresh': None, 'font': {}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'enable': True, 'description': None, '_uuid': '94c6acc08efc1f460446beedb50e1444', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'end_date_label', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 1), 'onInit': None}, {'activate': u'1', 'obj_module': None, 'show': 1, 'data_name': u'end_date', 'value': '', 'border': 0, 'size': (350, -1), 'style': 2, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'DatePickerCtrl', 'res_module': None, 'enable': False, 'onDateChanged': None, 'description': None, '_uuid': 'b1eadbb62e32669c3ff537f8d87698e4', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'end_date_edit', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 2), 'onInit': None, 'refresh': None}], 'name': 'DefaultName_3078', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (100, 100), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '494452535fe5205fc07490658c6bd3ed', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'recount': None, 'name': 'defaultWindow_2132', 'data_name': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'data_name': None, 'border': 5, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '9638ebe00759e9b79b60acd56e21cddd', 'flag': 2560, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'GetInterface().onCancelButton(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': '22a56885338309e7748af6309582ea5c', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': u'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'GetInterface().onOkButton(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u041a', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'f5f85d2ea87c026d3e8a4f54b0d6d996', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': u'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'layout': u'horizontal', 'name': 'DefaultName_2290', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'layout': 'vertical', 'name': 'DefaultName_1974', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'keyDown': None, 'border': 0, 'size': (450, 200), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0433\u043e \u043f\u0435\u0440\u0438\u043e\u0434\u0430', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Dialog', 'res_module': u'new_period_dlg_frm.py', 'enable': True, 'description': None, 'onClose': u'None', '_uuid': 'ad448a27bcca9a1b2b31dcd5f07997d0', 'moveAfterInTabOrder': '', 'killFocus': None, 'flag': 0, 'recount': None, 'icon': None, 'setFocus': None, 'name': u'new_period_dlg', 'data_name': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 3)
###END SPECIAL BLOCK

#   Class name
ic_class_name = 'icNewPeriodDialog'

def icNewPeriodDlg(ParentWin_=None,OBJ_=None):
    """
    Функция вызова диалогового окна создания нового 
    периода истории изменения состояния объекта.
    @param ParentWin_: Родительское окно диалогового окна.
    @param OBJ_: Редактируемый объект предметной области.
    """
    try:
        dlg_interface=icNewPeriodDialog(ParentWin_,OBJ_)
        dlg=dlg_interface.getObject()
        dlg.ShowModal()
        return dlg_interface.getResult()
    except:
        ic.io_prnt.outErr(u'Ошибка при вызове диалогового окна создания нового периода объекта %s.'%OBJ_)
        return None
        
class icNewPeriodDialog(icobjectinterface.icObjectInterface):
    def __init__(self, parent=None,OBJ=None):
        """
        Constructor.
        @param parent: Рродительское окно.
        @param OBJ: Объект редактирования.
        """
        #
        try:
            ic_res.findSpcInResource('subject_choice',resource)['sprav']=OBJ.getHistory().getSubjectPsp()
        except:
            ic.io_prnt.outErr(u'Ошибка инициализации справочника субъектов контрола \'subject_choice\' в форме %s'%resource['name'])
            
        #   Base class constructor
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        
        #Результат выбора в диалоговом окне
        self.result=None
        

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

    def onCancelButton(self,event):
        """
        Обработчик нажатия на кнопке <Отмена>.
        """
        dlg=self.getObject()
        if dlg:
            dlg.EndModal(wx.ID_CANCEL)
        
    def onOkButton(self,event):
        """
        Обработчик нажатия на кнопке <ОК>.
        """
        dlg=self.getObject()
        if dlg:
            self.result=self._getEditResult()
            if self._validEditResult(self.result):
                dlg.EndModal(wx.ID_OK)                
        
    def _getEditResult(self):
        """
        Получить результат редактирования.
        """
        dlg=self.getObject()
        if dlg:
            return dlg.GetContext().getValueInCtrl(dlg)
        return None
    
    def _validEditResult(self,Result_):
        """
        Проверка/контроль на правильность заполнения результатов редактирования.
        @return: True-все ок, False-данные не корректны, None - ошибка.
        """
        try:
            if not Result_['subj_cod']:
                ic.ic_dlg.icMsgBox(u'Внимание!',
                    u'Требуется выбор субъекта',ParentWin_=self.getObject())
                return False
            return True
        except:
            ic.io_prnt.outErr(u'Ошибка проверки результирующих данных')
        return None
        
    def getResult(self):
        """
        Результат.
        """
        return self.result
    
    def onEndPeriodCheck(self,event):
        """
        Обработчик изменения признака закрытия периода.
        """
        checked=self.getObject().GetObject('end_period_check').IsChecked()
        self.getObject().GetObject('end_date_edit').Enable(checked)

    def onEndPeriodUncheck(self,event):
        """
        Обработчик изменения признака закрытия периода.
        """
        checked=self.getObject().GetObject('end_period_check').IsChecked()
        self.getObject().GetObject('end_date_edit').Enable(checked)
        
def test(par=0):
    """
    Test NewPeriodDialog class.
    """

    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Test code #
    ################

    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test()

    