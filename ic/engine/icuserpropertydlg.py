#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5

import wx
import ic
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.kernel import io_prnt
from ic.engine import icUser
from ic.dlg import ic_dlg
from ic.utils import ic_str
from ic.utils import coderror

### !!!! NO CHANGE !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'keyDown': None, 'border': 5, 'size': (-1, -1), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': True, 'title': u'\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': '2ce0e36abab12d27b0a60a834e74c64b', 'moveAfterInTabOrder': '', 'killFocus': None, 'flag': 240, 'recount': None, 'setFocus': None, 'child': [{'activate': 1, 'obj_module': None, 'minCellWidth': 10, 'data_name': None, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 1, 'type': 'GridBagSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': '405fbc37b8a845f62e99d4a28db8a481', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c:', 'data_name': None, 'refresh': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': '56108ca31e8c4347296aa0e2fa6a6c25', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'nameLabel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'ctrl': u'GetInterface().onNameEditCtrl()', 'data_name': None, 'hlp': None, 'value': '', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'alias': None, 'component_module': None, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'show': 1, 'type': 'TextField', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'ef0efbfc30be215378df5102f9917177', 'pic': 'S', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'nameEdit', 'changed': u'None', 'keyDown': None, 'init_expr': None, 'position': (1, 2), 'use_fdict': False, 'onInit': None, 'refresh': []}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041f\u043e\u043b\u043d\u043e\u0435 \u0438\u043c\u044f:', 'data_name': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': 'cc3163b58137a6ac7369dd23bda0c4d2', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'descriptionLabel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (3, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'data_name': None, 'getvalue': None, 'value': '', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': 'TextField', 'res_module': None, 'pic': 'S', 'description': None, '_uuid': 'b8019e859275170e00eabc96992c9cdf', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'descriptionEdit', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (3, 2), 'onInit': None, 'refresh': []}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041f\u0430\u043f\u043a\u0430 \u043d\u0430\u0441\u0442\u0440\u043e\u0435\u043a:', 'data_name': None, 'refresh': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': 'f41488adaddc09747b92c691aa1c65cc', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'localDirLabel', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (5, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'data_name': None, 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': 'TextField', 'res_module': None, 'pic': 'S', 'description': None, '_uuid': '47ae4547a8a724ab1eff54321ea7f934', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'localDirEdit', 'changed': None, 'value': '', 'alias': None, 'init_expr': None, 'position': (5, 2), 'onInit': None, 'refresh': []}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u0420\u043e\u043b\u044c:', 'data_name': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': '40b5a52285e7ebc635b593ae532490c3', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'roleLabel', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (7, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'refresh': [], 'border': 0, 'size': (-1, -1), 'style': 33555520, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': (255, 255, 255), 'type': 'Choice', 'res_module': None, 'loseFocus': None, 'description': None, '_uuid': '2a251bc9a142d9c269c4fcde002a6f14', 'moveAfterInTabOrder': '', 'choice': None, 'flag': 8192, 'recount': [], 'field_name': None, 'setFocus': None, 'name': u'roleChoice', 'items': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (7, 2), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041f\u0430\u0440\u043e\u043b\u044c:', 'data_name': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': 'b26b4d814f5e5b53f4fd99cf5cdab119', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'passwordLabel1', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (9, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'data_name': None, 'getvalue': None, 'value': '', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 2048, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': 'TextField', 'res_module': None, 'pic': 'S', 'description': None, '_uuid': '8a47685e1b2229aff19ae3f0ee4712a6', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'passwordEdit1', 'changed': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (9, 2), 'onInit': None, 'refresh': []}, {'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u043f\u0430\u0440\u043e\u043b\u044f:', 'data_name': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': (50, 50, 50), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'StaticText', 'res_module': None, 'description': None, '_uuid': '7619c2477d0a65a15357dde960d34687', 'moveAfterInTabOrder': '', 'flag': 2048, 'recount': None, 'name': u'passwordLabel2', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (11, 1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'data_name': None, 'getvalue': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 2048, 'foregroundColor': (0, 0, 0), 'span': (1, 3), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': 'TextField', 'res_module': None, 'pic': 'S', 'description': None, '_uuid': '32c994951c6953c977ab812e6f932fc6', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': [], 'hlp': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'passwordEdit2', 'changed': None, 'value': '', 'alias': None, 'init_expr': None, 'position': (11, 2), 'onInit': None, 'refresh': []}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'GetInterface().onOKButtonMouseClick(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u041a', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': 'b3df6bdb645320b270f374f1be58821f', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': u'ok_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (14, 2), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u'GetInterface().onCancelButtonMouseClick(event)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041e\u0442\u043c\u0435\u043d\u0430', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', 'res_module': None, 'description': None, '_uuid': '0298ea5e1f2ea90b466ddf3d3307833a', 'userAttr': None, 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': u'cancel_button', 'mouseUp': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (14, 4), 'onInit': None, 'refresh': None, 'mouseContextDown': None}, {'size': (5, 5), 'style': 0, 'activate': 1, 'obj_module': None, 'description': None, '_uuid': 'db071935c20b52a3a5c3ae961daef762', 'border': 0, 'span': (1, 1), 'data_name': None, 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'component_module': None, 'position': (15, 5), 'res_module': None, 'type': 'SizerSpace', 'name': 'DefaultName_1205'}], 'name': u'userPropertySizer', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'name': u'userPropertyDlg', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 2)
###END SPECIAL BLOCK

#   Class name
ic_class_name = 'icUserPropertyDialog'


class icUserPropertyDialog(icobjectinterface.icObjectInterface):
    def __init__(self, parent):
        """
        Constructor.
        """
        #   Base class constructor
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)

        # Редактируемые данные
        self._data = None
        # менеджер управления файлами ресурса пользователя.
        self._manager = None

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

    def setManager(self, Manager_=None):
        """
        Установить менеджер управления файлами ресурса пользователя.
        """
        self._manager = Manager_
        
        # Вместе менеджером устаонвить список ролей
        if self._manager:
            roles = self._manager.getRoles()
            role_choice = self.GetNameObj('roleChoice')
            if role_choice:
                for name, description in roles:
                    if description:
                        role_choice.Append(description)
                    else:
                        role_choice.Append(name)

    def getData(self):
        """
        Редактиуемые данные.
        """
        return self._data

    def setData(self, Data_=None):
        """
        Установить данные.
        """
        self._data = Data_
        if self._data is not None:
            self._refreshControls(self._data)

    def _refreshControls(self, Data_):
        """
        Обновление значений контролов по редактируемым данным.
        """
        dlg = self.getDialog()
        user_name = ''
        if 'name' in Data_:
            user_name = Data_['name']
        dlg.SetTitle(u'Пользователь: ' + user_name)
        
        name_edit = self.GetNameObj('nameEdit')
        if name_edit:
            name_edit.SetValue(user_name, False)
            
        description_edit = self.GetNameObj('descriptionEdit')
        if description_edit:
            if 'description' in Data_:
                description_edit.SetValue(Data_['description'], False)
            
        local_dir_edit = self.GetNameObj('localDirEdit')
        if local_dir_edit:
            local_dir_edit.SetValue(Data_['local_dir'], False)
            
        role_choice = self.GetNameObj('roleChoice')
        if role_choice:
            roles = self._manager.getRoles()
            roles_name = [role[0] for role in roles]
            roles_description = [role[1] for role in roles]
            try:
                selection = roles_name.index(Data_['roles'][0])
            except IndexError:
                selection = 0
            role_choice.SetSelection(selection)            
                
    def _refreshData(self):
        """
        Обновить данные по контролам редактирования.
        """
        # Главное окно и горизонтальное меню наследуются у текущего пользователя
        default_main_win = ic.getKernel().GetAuthUser().resource['main_win']
        default_main_menubars = ic.getKernel().GetAuthUser().resource['menubars']
        
        data = util.icSpcDefStruct(icUser.SPC_IC_USER, {'main_win': default_main_win,
                                                        'menubars': default_main_menubars})
        
        name_edit = self.GetNameObj('nameEdit')
        if name_edit:
            data['name'] = name_edit.GetValue()
            
        description_edit = self.GetNameObj('descriptionEdit')
        if description_edit:
            data['description'] = description_edit.GetValue()
            
        local_dir_edit = self.GetNameObj('localDirEdit')
        if local_dir_edit:
            data['local_dir'] = local_dir_edit.GetValue()
            
        role_choice = self.GetNameObj('roleChoice')
        if role_choice:
            roles = self._manager.getRoles()
            selection = role_choice.GetSelection()
            try:
                data['roles'] = [roles[selection][0]]
            except:
                data['roles'] = []
            
        password_edit1 = self.GetNameObj('passwordEdit1')
        password_edit2 = self.GetNameObj('passwordEdit2')
        if password_edit1 and password_edit2:
            password1_txt = password_edit1.GetValue()
            password2_txt = password_edit2.GetValue()
            password1_md5 = md5.new(password1_txt).hexdigest()
            password2_md5 = md5.new(password2_txt).hexdigest()
            if password1_md5 == password2_md5:
                if not password1_txt.strip():
                    # Выбрана пустая строка
                    data['password'] = md5.new('').hexdigest()
                else:
                    data['password'] = password1_md5
            else:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ!',
                                    u'Введенный пароль и подтверждение на совпадают. Введите еще раз.',
                    ParentWin_ = self.getDialog())
                return None
        
        self._data = data
        return self._data
        
    def getDialog(self):
        """
        Объект диалога.
        """
        return self.getObject()
    
    def onOKButtonMouseClick(self, event):
        """
        Обработчик нажатия на кнопку <OK>.
        """
        dlg = self.getDialog()
        result = self._refreshData()
        if result:
            dlg.EndModal(wx.ID_OK)
        
    def onCancelButtonMouseClick(self, event):
        """
        Обработчик нажатия на кнопку <Отмена>.
        """
        dlg = self.getDialog()
        self.setData(None)
        dlg.EndModal(wx.ID_CANCEL)
        
    def onNameEditChanged(self, event):
        """
        Изменение значения имени полььзователя в редакторе.
        """
        name = event.GetString()
        if not ic_str.isLATText(name):
            name = ic_str.rus2lat_keyboard(name)
            name_edit = self.GetNameObj('nameEdit')
            name_edit.SetValue(name)
        dlg = self.getDialog()
        dlg.SetTitle(u'Пользователь: '+str(name))
        
        local_dir_edit = self.GetNameObj('localDirEdit')
        if local_dir_edit:
            local_dir = local_dir_edit.GetValue()
            if local_dir:
                new_local_dir = 'C:\\#WRK\\'+str(name)
                local_dir_edit.SetValue(new_local_dir)
            
        event.Skip()
        
    def onNameEditCtrl(self):
        """
        Изменение значения имени полььзователя в редакторе.
        """
        name_edit = self.GetNameObj('nameEdit')
        isChanged = name_edit.IsModified()
        old = name = name_edit.GetValue()
        if not ic_str.isLATText(name):
            name = ic_str.rus2lat_keyboard(name)
            name_edit.SetValue(name)
        dlg = self.getDialog()
        dlg.SetTitle(u'Пользователь: '+str(name))
        
        local_dir_edit = self.GetNameObj('localDirEdit')
        if local_dir_edit:
            local_dir = local_dir_edit.GetValue()
            if local_dir:
                new_local_dir = 'C:\\#WRK\\'+str(name)
                local_dir_edit.SetValue(new_local_dir)
            
        if isChanged or name != old:
            return coderror.IC_CTRL_REPL
        
        return coderror.IC_CTRL_OK


def icUserPropertyDlg(ParentForm_, DefaultRes_, UserManager_=None):
    """
    Функция вызова диалогового окна редактирования
    свойств пользователя.
    @param ParentForm_: Родительское окно.
    @param DefaultRes_: Структура для редактирования
    по умолчанию.
    @param UserManager_: Менеджер пользователей.
    """
    dlg = None
    result = None
    clear = False
    try:
        if ParentForm_ is None:
            id_ = wx.NewId()
            ParentForm_ = wx.Frame(None, id_, '')
            clear = True

        dlg_iface = icUserPropertyDialog(ParentForm_)
        dlg_iface.setManager(UserManager_)  # Установить менеджера у всех контролов редактирования
        dlg_iface.setData(DefaultRes_)
        dlg = dlg_iface.getDialog()
        
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg_iface.getData()
            dlg.Destroy()
            if clear:
                ParentForm_.Destroy()
            return result
    except:
        io_prnt.outErr(u'Ошибка редактирования пользователя.')

    finally:
        if dlg:
            dlg.Destroy()

        if clear:
            ParentForm_.Destroy()

    return None


def test(par=0):
    """
    Test icUserPropertyDialog class.
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
