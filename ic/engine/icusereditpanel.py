#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.kernel import io_prnt
from ic.engine import icUser
from ic.dlg import ic_dlg
from ic.engine import ic_user
from ic.engine import icuserpropertydlg

### !!!! NO CHANGE !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'keyDown': None, 'border': 0, 'size': (700, 300), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '1a8480f28485c4f33b879aadc62eeb06', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'child': [{'hgap': 0, 'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'description': None, '_uuid': '90e6c9850d880937d96eddb9b1a3774c', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'image_list': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'ToolBar', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'd9a3725015eca79e98770741cae22e94', 'moveAfterInTabOrder': '', 'flag': 10752, 'recount': None, 'child': [{'activate': 1, 'name': u'addTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', 'longHelpString': '', '_uuid': '456e9c36f3c3e3312864facdb97f08d1', 'label': '', 'pushedBitmap': None, 'disabledBitmap': None, 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@GetInterface().addTool_bitmap(evt)', 'dis_img_indx': -1, 'push_img_indx': -1, 'type': 'ToolBarTool', 'onTool': u'GetInterface().onAddButtonMouseClick(event)'}, {'activate': 1, 'name': u'editTool', 'toolType': 0, 'shortHelpString': u'\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', 'longHelpString': '', '_uuid': '9a836fef266bd792723b050015175436', 'pushedBitmap': None, 'label': '', 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@GetInterface().editTool_bitmap(evt)', 'type': 'ToolBarTool', 'onTool': u'GetInterface().onEditButtonMouseClick(event,values)'}, {'activate': 1, 'disabledBitmap': u'@GetInterface().disDelTool_bitmap(evt)', 'name': u'delTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', 'longHelpString': '', '_uuid': '0d474b257540d2908ca03622f3af1082', 'pushedBitmap': None, 'label': '', 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@GetInterface().delTool_bitmap(evt)', 'dis_img_indx': -1, 'push_img_indx': -1, 'type': 'ToolBarTool', 'onTool': u'GetInterface().onDelButtonMouseClick(event,values)'}], 'name': u'userEditToolbar', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': wx.Point(631, 0), 'onInit': None, 'bitmap_size': (16, 15)}, {'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'activated': None, 'selected': u'GetInterface().onUserGridItemSelected(event,values)', 'border': 0, 'size': (-1, -1), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': 'SimpleObjectListView', 'res_module': None, 'enable': True, 'description': None, '_uuid': '6994dd47a0493c7a448970f882fc31e9', 'style': 0, 'oddRowsBackColor': (255, 255, 255), 'flag': 8192, 'recount': None, 'evenRowsBackColor': (225, 235, 250), 'keyDown': None, 'child': [{'activate': 1, 'obj_module': None, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'component_module': None, 'label': u'\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', 'width': 200, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': u'\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', 'shortHelpString': '', '_uuid': 'c8719fca0eec43781a13b53d0a8f7fd4', 'recount': None, 'hlp': None, 'name': u'user', 'setvalue': '', 'attr': 'W', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'component_module': None, 'label': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'width': 250, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'shortHelpString': '', '_uuid': '4dcd9b8a49d028ba99d34afcada16814', 'recount': None, 'hlp': None, 'name': u'description', 'setvalue': '', 'attr': 'W', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None}, {'activate': 1, 'obj_module': None, 'ctrl': None, 'pic': 'S', 'getvalue': '', 'style': 0, 'component_module': None, 'label': u'\u0420\u043e\u043b\u044c', 'width': 250, 'init': None, 'valid': None, 'type': 'GridCell', 'res_module': None, 'sort': None, 'cell_attr': {'foregroundColor': (0, 0, 0), 'name': '', '_uuid': None, 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': u'\u0420\u043e\u043b\u044c', 'shortHelpString': '', '_uuid': 'd6e062095e1cdf036e2170e189893a50', 'recount': None, 'hlp': None, 'name': u'role_description', 'setvalue': '', 'attr': 'W', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None}], 'name': u'userGrid', 'refresh': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'layout': 'vertical', 'name': u'userEditBoxsizer', 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'name': u'userEditPanel', 'refresh': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 6)
###END SPECIAL BLOCK

#   Class name
ic_class_name = 'icUserEditPanel'


class icUserEditPanel(icobjectinterface.icObjectInterface):
    """
    Панель редактирования пользователей.
    """
    def __init__(self, parent):
        """
        Constructor.
        """
        from ic.imglib import newstyle_img
        self.imglib = newstyle_img
        #   Base class constructor
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)

        # Редактируемые данные
        self._data = None
        # менеджер управления файлами ресурса пользователя.
        self._manager = None

    ###BEGIN EVENT BLOCK
    
    def addTool_bitmap(self, evt):
        return self.imglib.getadd_rowBitmap()
    
    def editTool_bitmap(self, evt):
        return self.imglib.getedit_rowBitmap()
    
    def delTool_bitmap(self, evt):
        return self.imglib.getdel_rowBitmap()

    def disDelTool_bitmap(self, evt):
        return self.imglib.getdis_del_rowBitmap()
        
    ###END EVENT BLOCK

    def setManager(self, Manager_):
        """
        Установить менеджер управления файлами ресурса пользователя.
        @param Manager_: Объект менеджера пользователей.
        """
        self._manager = Manager_

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
        if Data_ is not None:
            self._init_data(self._data)

    def _init_data(self, Data_):
        """
        Инициализация данных в панели редактора.
        """
        dataset = self._data2obj_grid_dataset(Data_)
        grid = self.GetNameObj('userGrid')
        grid.context['values'] = None
        if grid:
            grid.setDataset(dataset)

    def _roles2role_description_str(self, RolesList_):
        """
        Функция преобразования списка ролей в список описаний ролей.
        """
        roles = self._manager.getRoles()
        roles_description = [role[1] for role in roles if role[0] in RolesList_]
        return ', '.join(roles_description)

    def _data2obj_grid_dataset(self, Data_):
        """
        Фукция преобразования данных о пользователях в набор данных
        для грида объектов.
        """
        result = []
        for user_name in Data_.keys():
            user_spc = Data_[user_name]
            name = user_spc['name']
            description = user_spc['description']
            roles = user_spc['roles']
            if self._manager:
                roles_description = self._roles2role_description_str(roles)
            else:
                roles_description = ''
            rec = dict()
            rec['user'] = name
            rec['description'] = description
            rec['roles'] = roles
            rec['role_description'] = roles_description or ', '.join(roles)
            result.append(rec)
        return result

    def _obj_grid_dataset2data(self, ObjGridDataset_):
        """
        Фукция преобразования набора данных
        для грида объектов в данные о пользователях.
        """
        result = {}
        for rec in ObjGridDataset_:
            name = rec['user']
            description = rec['description']
            roles = rec['roles']
            new_user = util.icSpcDefStruct(icUser.SPC_IC_USER,
                                           {'name': name,
                                            'description': description,
                                            'roles': roles})
            result[name] = new_user
        return result

    def refreshData(self):
        """
        Обновить внутреннее представление данных из контролов редактирования.
        """
        pass

    def getPanel(self):
        """
        Объект панели редактора пользователей.
        """
        return self.getObject()

    def updateData(self, UserData_):
        """
        Обновить ресурс данными о пользователе.
        """
        self._data[UserData_['name']] = UserData_
        self._init_data(self._data)
        
    def onAddButtonMouseClick(self, event):
        """
        Обработчик нажатия на кнопку создания нового пользователя.
        """
        try:
            # Главное окно и горизонтальное меню наследуются у текущего пользователя
            default_main_win = ic_user.getKernel().GetAuthUser().resource['main_win']
            default_main_menubars = ic_user.getKernel().GetAuthUser().resource['menubars']
            default_res = util.icSpcDefStruct(icUser.SPC_IC_USER,
                                              {'main_win': default_main_win,
                                               'name': 'new_user',
                                               'local_dir': 'C:\\#WRK\\new_user',
                                               'menubars': default_main_menubars})
            user_res = icuserpropertydlg.icUserPropertyDlg(self.getPanel(),
                                                           default_res, self._manager)
            if user_res:
                self.updateData(user_res)
            
            if event:    
                event.Skip()
        except:
            io_prnt.outErr(u'Ошибка добавления нового пользователя.')
        
    def onEditButtonMouseClick(self, event, values=None):
        """
        Обработчик нажатия на кнопку редактирования пользователя.
        """
        try:
            if values:
                user_name = values['user']
                default_res = self._data[user_name]
                user_res = icuserpropertydlg.icUserPropertyDlg(self.getPanel(),
                                                               default_res, self._manager)
                if user_res:
                    self.updateData(user_res)
            else:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Выберите пользователя для редактирования.')

            if event:    
                event.Skip()
        except:
            io_prnt.outErr(u'Ошибка редактирования пользователя.')
        
    def onDelButtonMouseClick(self, event, values=None):
        """
        Обработчик нажатия на кнопку удаления пользователя.
        """
        try:
            if values:
                user_name = values['user']
                if ic_dlg.icAskBox(u'УДАЛЕНИЕ',
                                   u'Удалить пользователя %s?' % user_name):
                    del self._data[user_name]
                    self._init_data(self._data)
            else:
                ic_dlg.icWarningBox(u'ВНИМАНИЕ', u'Выберите пользователя, которого надо удалить.')
                    
            if event:
                event.Skip()
        except:
            io_prnt.outErr(u'Ошибка удаления пользователя.')
            
    def onUserGridItemSelected(self, event, values=None):
        """
        Выбор пользователя в гриде пользователей.
        """
        tb = self.GetNameObj('userEditToolbar')
        if values is None:
            tb.enableTool('addTool', True)
            tb.enableTool('editTool', False)
            tb.enableTool('delTool', False)
        elif values['user'] == 'admin':
            # Админа нельзя удалить
            tb.enableTool('addTool', True)
            tb.enableTool('editTool', True)
            tb.enableTool('delTool', False)
        else:
            tb.enableTool('addTool', True)
            tb.enableTool('editTool', True)
            tb.enableTool('delTool', True)
        event.Skip()


def test(par=0):
    """
    Test icUserEditPanel class.
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
