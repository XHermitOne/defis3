#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Окно редактирования окружения проекта.
"""

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.log import log
from ic.engine import ic_user

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource={'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (700, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u0430:', 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '0ad15ccc4d095715387d2eccb12a879a', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': u'1b8806cf6c2d638c25d3c59ff3c112d6', 'flag': 8192, 'child': [{'image_size': (16, 16), 'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': 'eae7af89a80b33eb5c47f3cf5f2e3f40', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'hgap': 0, 'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'description': None, '_uuid': '95ec394e93a7cc8e1bde36e56394cd5f', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'labels': [u'\u0418\u043c\u044f', u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', u'\u041f\u0440\u0430\u0432\u0430 \u0434\u043e\u0441\u0442\u0443\u043f\u0430', u'\u041a\u043b\u044e\u0447 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438'], 'refresh': None, 'selectChanged': None, 'border': 0, 'size': (-1, -1), 'treeDict': {}, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 1, 'itemCollapsed': None, 'source': u'', 'itemActivated': None, 'itemExpanded': None, 'titleRoot': u'\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435', 'type': u'SimpleTreeListCtrl', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'dc623b2f9a824d2061e54390de26b8df', 'style': 0, 'flag': 8192, 'recount': None, 'hideHeader': False, 'backgroundColor': None, 'child': [], 'name': u'view_treectrl', 'wcols': [100, 300, 100, 100], 'data_name': None, 'keyDown': None, 'itemChecked': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'layout': 'vertical', 'name': 'DefaultName_1955', 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'name': u'page1', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'res_module': None, 'enable': True, 'description': None, 'onClose': None, '_uuid': '19125fb18a8a3637d184598750760926', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': 'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': 'e106970beeb7230acec78432913f9f36', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'child': [{'activate': 1, 'disabledBitmap': None, 'name': u'add_tool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c', 'longHelpString': '', '_uuid': '15ba70c1d4ab2f7373b333186092acd6', 'pushedBitmap': None, 'label': '', 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgPlus', 'dis_img_indx': -1, 'push_img_indx': -1, 'type': 'ToolBarTool', 'onTool': u'GetInterface().onAddTool(event)'}, {'activate': 1, 'name': u'del_tool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c', 'longHelpString': '', '_uuid': '62644b048005a3e4cb84cb11d21c0b3f', 'push_img_indx': -1, 'pushedBitmap': None, 'label': '', 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgMinus', 'dis_img_indx': -1, 'disabledBitmap': None, 'type': 'ToolBarTool', 'onTool': u'GetInterface().onDelTool(event)'}, {'activate': 1, 'name': '_1462', '_uuid': 'a5ecd8ea547b9fb515748947c3b54002', 'init_expr': None, 'type': 'Separator', 'size': 5}, {'activate': 1, 'name': u'set_tool', 'toolType': 0, 'shortHelpString': u'\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c', 'longHelpString': '', '_uuid': '4d27e4d06fd31e08caa8c9b28fb3cf68', 'push_img_indx': -1, 'pushedBitmap': None, 'label': '', 'img_indx': -1, 'isToggle': 0, 'init_expr': None, 'bitmap': u'@common.imgCheck', 'dis_img_indx': -1, 'disabledBitmap': None, 'type': 'ToolBarTool', 'onTool': u'GetInterface().onSetTool(event)'}], 'image_list': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097668, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'ToolBar', 'res_module': None, 'enable': True, 'description': None, '_uuid': 'aa4c26aab338b277f543442a7ecc3488', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'env_grid_toolbar', 'data_name': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'bitmap_size': (16, 15)}, {'labelClick': None, 'activate': 1, 'obj_module': None, 'show': 1, 'col_count': 2, 'refresh': None, 'hrows': [], 'border': 0, 'size': (-1, -1), 'row_labels': ['1'], 'col_label_height': -1, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'row_label_width': -1, 'cellSelect': None, 'source': None, 'component_module': None, 'proportion': 1, 'readonly': False, 'row_count': 1, 'backgroundColor': None, 'cellDClick': None, 'type': 'SimpleGrid', 'res_module': None, 'enable': True, 'description': None, 'selection_mode': 'cells', '_uuid': '5408ba83e9411fc1e1f40b68ea4812d3', 'style': 0, 'col_labels': [u'\u0418\u043c\u044f', u'\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435'], 'flag': 8192, 'alias': None, 'recount': None, 'child': [], 'name': u'env_grid', 'wcols': [70, 200], 'default_col_width': -1, 'default_row_height': -1, 'data_name': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'cellChange': None}], 'layout': 'vertical', 'name': 'DefaultName_3200', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'name': u'page2', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}], 'titles': [u'\u041e\u0441\u043d\u043e\u0432\u043d\u044b\u0435', u'\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435'], 'keyDown': None, 'images': [], 'border': 0, 'select': u'0', 'size': (-1, -1), 'onRightMouseClick': None, 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 1, 'pageChanged': None, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Notebook', 'res_module': None, 'enable': True, 'description': None, '_uuid': '39f073d92ed3a646411304aef2aa3390', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': u'env_notebook', 'data_name': None, 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'attach_focus': False, 'data_name': None, 'mouseClick': u"GetObject('envEditDialog').Close()", 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, 'proportion': 0, 'label': u'\u0417\u0430\u043a\u0440\u044b\u0442\u044c', 'source': None, 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', 'res_module': None, 'enable': True, 'description': None, '_uuid': '715871895a45fd4b4eaa61a34d44c178', 'userAttr': None, 'moveAfterInTabOrder': u'', 'flag': 2304, 'recount': None, 'name': u'close_button', 'mouseUp': None, 'keyDown': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': None, 'mouseContextDown': None}], 'layout': u'vertical', 'name': u'DefaultName_1481', 'alias': None, 'init_expr': None, 'position': (0, 0), 'vgap': 0}], 'icon': None, 'setFocus': None, 'name': u'envEditDialog', 'data_name': None, 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 1)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icEnvironmentEditDlg'


class icEnvironmentEditDlg(icobjectinterface.icObjectInterface):

    def __init__(self, parent, Context_=None, ProjectRoot_=None):
        """
        Конструктор интерфейса.
        """
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        
        try:
            viewer = self.GetNameObj('view_treectrl')
            if Context_ is None:
                Context_ = ic_user.getKernel().GetContext()
            variables = self._contextConvert(Context_)
            viewer.LoadTree(variables)
        except:
            log.error(u'Ошибка инициализации дерева просмотра хранилища переменных.')
        
        self._project_root = ProjectRoot_
        if self._project_root:
            try:
                env_grid = self.GetNameObj('env_grid')
                env_dict = self._project_root.prj_res_manager.getPrjEnv()
                env_list = env_dict.items()
                env_list.sort()
                log.debug('Environment list: <%s>' % env_list)
                env_grid.setTable(env_list)
            except:
                log.error(u'Ошибка инициализации грида редактирования дополнительных атрибутов проекта.')

    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
    def _contextConvert(self, Context_):
        """
        Переконвертировать контекст в формат дерева.
        """
        result = []
        for name in Context_.keys():
            tree_item = {}
            context_item = Context_[name]
            tree_item['name'] = name
            tree_item['__record__'] = [name, str(context_item), '', '']
            result.append(tree_item)
        return result

    def design(self):
        """
        """
        self.getObject().ShowModal()
        
    def onAddTool(self, event=None):
        """
        Обработчик добавления новой записи в гриде дополнительных атрибутов проекта.
        """
        env_grid = self.GetNameObj('env_grid')
        env_grid.appendRow()
        
    def onDelTool(self, event=None):
        """
        Обработчик удаления выбранной записи в гриде дополнительных атрибутов проекта.
        """
        env_grid = self.GetNameObj('env_grid')
        env_grid.deleteCurRow()
        
    def onSetTool(self, event=None):
        """
        Обработчик сохранения отредактированных значений.
        """
        env_grid = self.GetNameObj('env_grid')
        env_list = env_grid.getTable()
        env_dict = None
        if env_list:
            env_dict = dict([(str(name), val) for name, val in env_list if name])
        if self._project_root and env_dict:
            self._project_root.prj_res_manager.setPrjEnv(env_dict)
            self._project_root.save()


def test(par=0):
    """
    Тестируем класс.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #
    # Тестовый код
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
