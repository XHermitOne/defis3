#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import copy
import os.path

import ic.components.icResourceParser as prs
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.utils.coderror as coderror
import ic.PropertyEditor.icDefInf as icDefInf
import wx.grid as Grid
import ic.PropertyEditor.icEditorGridRender as icrender
import ic.dlg.msgbox as msgbox
from ic.kernel import io_prnt
import ic.utils.resource as Resource
from ic.utils import ic_uuid

_ = wx.GetTranslation

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': u'1', 'obj_module': None, 'show': u'1', 'child': [{'size': (-1, -1), 'style': 0, 'activate': u'1', 'obj_module': None, 'description': None, 'alias': u'None', '__item_id': 1, 'modules': {}, 'border': 0, '_uuid': '61843d9340d13ce7c738f5fa1c3cc850', 'proportion': 0, 'data_name': None, 'object': u'None', 'component_module': None, 'flag': 0, 'init_expr': u'GetInterface().resource_init_expr()', 'span': (1, 1), 'position': (-1, -1), 'res_module': None, 'type': u'Import', 'name': u'resource'}, {'hgap': 0, 'activate': u'1', 'obj_module': None, '__default_page__': 0, '__attr_types__': {0: ['name', 'type', 'alias', 'data_name'], 1: ['layout', 'alignment'], 7: ['flag', 'style'], 40: ['proportion', 'border', 'vgap, hgap'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'init_expr', 'pre_init_expr', 'description', 'component_module', 'hgap', 'child', 'vgap'], 17: ['res_module', '_uuid', 'obj_module']}, 'data_name': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'layout': u'vertical', 'alias': u'', 'component_module': None, 'proportion': 0, '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, '__version__': '0.0.0.0', 'type': u'BoxSizer', '__doc__': None, 'res_module': None, '__styles__': {'DEFAULT': 0}, 'description': None, '__item_id': 2, '_uuid': u'4a4ca30ae69f315d5afcac400a4ee0f4', '__brief_attrs__': [], 'flag': 0, 'child': [{'activate': u'1', 'obj_module': None, 'show': u'1', '__attr_types__': {0: ['moveAfterInTabOrder', 'name', 'type', 'data_name', 'label', 'alias', 'field_name'], 1: ['layout', 'alignment'], 2: ['icDelButton', 'isLocaleTitles', 'enable'], 7: ['flag', 'style'], 8: ['selPageColor', 'foregroundColor', 'backgroundColor'], 9: ['font'], 10: ['position', 'span'], 11: ['size'], 12: ['recount', 'activate', 'description', 'show', 'component_module', 'pre_init_expr', 'refresh', 'source', 'onSelectTitle', 'keyDown', 'child', 'path', 'onInit', 'init_expr'], 17: ['obj_module', '_uuid', 'res_module'], 20: ['images', 'titles'], 40: ['border', 'proportion']}, 'selPageColor': (232, 232, 208), 'recount': u'WrapperObj.recountFuncNB(evt)', 'onSelectTitle': u'WrapperObj.OnSelectPage(self.GetSelected())', 'titles': ['Base', 'Visual', 'Special', 'Events', 'All'], 'keyDown': u'None', 'path': u"@# \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u044f\u0435\u043c \u043f\u0443\u0442\u044c \u0434\u043e \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438 \u043a\u0430\u0440\u0442\u0438\u043d\u043e\u043a\r\nimport ic.utils.resource as resource\r\n_resultEval = resource.icGetICPath()+'/PropertyEditor/images'\r\n", 'images': [u'cog.png', u'color_picker.png', u'', u'', u'page_white_stack.png'], 'font': {'style': 'regular', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'border': 0, 'size': (393, 27), 'style': 0, 'foregroundColor': (100, 100, 100), 'span': (1, 1), '__init_res_by_wizard__': None, 'component_module': None, '__default_page__': 0, 'proportion': 0, 'source': u'', '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, 'backgroundColor': (245, 245, 245), '__version__': '0.0.0.0', 'type': u'TitlesNotebook', '__doc__': None, 'res_module': None, '__styles__': {'DEFAULT': 0}, '__events__': {'onSelectTitle': ('wx.EVT_LEFT_UP', 'OnSelectTitle', False), 'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False), 'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False)}, 'enable': True, 'description': None, '__item_id': 3, '_uuid': '5c5fa1b4-05e9-44a1-a6ec-e670c36f4738', 'moveAfterInTabOrder': u'', '__brief_attrs__': [], 'flag': 8192, 'alias': u'None', 'child': [], 'isLocaleTitles': True, 'name': u'NB', 'icDelButton': False, 'data_name': None, 'refresh': u'None', '__version__icwidget': '0.0.0.0', '__version__base': '0.0.0.0', '__interface__': None, 'init_expr': u'GetInterface().OnInitExpr()', 'position': (0, 0), 'onInit': None}, {'line_color': (255, 255, 255), 'activate': u'1', 'obj_module': None, 'enable_freq_dict': False, '_uuid': '2e4a3d1619bdd6bce0d1d683109406f6', 'show': u'1', 'init_expr': u'GetWrapper().PropertyGrid_init_expr()', 'data_name': None, 'cols': [{'activate': u'1', 'ctrl': u'', 'pic': u'S', 'getvalue': u'', 'style': 0, 'show': u'1', 'label': u'', 'width': 120, 'init': u'', 'valid': u'None', 'type': u'GridCell', 'sort': u'None', 'cell_attr': {'activate': '1', 'name': '', '__item_id': 6, '_uuid': '23fd87416a6b09f3ca925a9314584fc5', 'foregroundColor': (0, 0, 0), 'init_expr': 'None', 'backgroundColor': (245, 245, 245), 'font': {'style': 'regular', 'name': 'defaultFont', 'family': 'sansSerif', 'faceName': 'Arial', 'type': 'Font', 'underline': False, 'size': 8}, 'type': 'cell_attr', 'alignment': "('left', 'middle')"}, 'shortHelpString': u'', '__item_id': 5, '_uuid': u'7ed8b82e86d35d9e1e0dee428a03f15b', 'recount': u'None', 'hlp': u'None', 'name': u'attributes', 'setvalue': u'', 'attr': u'R', 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None'}, {'activate': u'1', 'obj_module': None, 'ctrl': u'WrapperObj.Ctrl(self.GetView(), value, row, col)', 'pic': u'S', 'getvalue': u'', 'style': 0, 'component_module': None, 'show': u'1', 'label': u'col', 'width': 200, 'init': u'', 'valid': u'None', 'type': u'GridCell', 'res_module': None, 'sort': u'None', 'cell_attr': {'activate': '1', 'name': '', '__item_id': 8, '_uuid': '23fd87416a6b09f3ca925a9314584fc5', 'foregroundColor': (0, 0, 0), 'init_expr': 'None', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': ('left', 'middle')}, 'description': None, 'shortHelpString': u'', '__item_id': 7, '_uuid': u'fd27d78ef4194499c466535b7d69734a', 'recount': u'None', 'hlp': u'WrapperObj.OnHelpFuncValues(self.GetView(), row, col, evt)', 'name': u'values', 'setvalue': u'', 'attr': u'W', 'data_name': None, 'keyDown': u'', 'alias': u'None', 'init_expr': u'None'}], 'onSize': u'WrapperObj.OnSizeGrid(evt)', 'border': 0, 'post_select': u'GetWrapper().PropertyGrid_post_select(evt)', 'size': (220, 207), 'style': 0, 'dclickEditor': u'WrapperObj.OnDClickEditorFuncPropertyGrid(evt)', 'span': (1, 1), 'delRec': u'', 'row_height': 20, 'selected': u'WrapperObj.OnSelectGridCell(row, col)', 'proportion': 1, 'getattr': u'GetWrapper().PropertyGrid_getattr(col)', 'label': u'Grid', 'source': u'', 'init': u'@False', 'backgroundColor': (255, 255, 255), 'fixRowSize': 1, 'type': u'GridDataset', 'selection_mode': 'cells', 'res_module': None, 'enable': True, 'fixColSize': 0, 'description': None, 'post_del': u'None', 'post_init': u'None', 'cell_attr': {'activate': '1', 'name': '', '__item_id': 9, '_uuid': '6c62e5d9286f17d110c8db3613ae518b', 'foregroundColor': (0, 0, 0), 'init_expr': 'None', 'backgroundColor': (255, 255, 255), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'cell_attr', 'alignment': "('left', 'middle')"}, 'moveAfterInTabOrder': u'', 'docstr': 'ic.components.icgrid.html', 'flag': 8192, 'foregroundColor': None, 'recount': u'None', 'label_attr': {'activate': '1', 'name': '', '__item_id': 10, '_uuid': '6c62e5d9286f17d110c8db3613ae518b', 'foregroundColor': (255, 255, 255), 'init_expr': 'None', 'backgroundColor': (100, 100, 100), 'font': {'style': None, 'name': 'defaultFont', 'family': None, '__attr_types__': {}, 'faceName': '', 'type': 'Font', 'underline': 0, 'size': 8}, 'type': 'label_attr', 'alignment': ('left', 'middle')}, '__item_id': 4, 'keyDown': u'WrapperObj.GridKeyDown(evt)', 'name': u'PropertyGrid', 'label_height': 0, 'changed': u'None', 'refresh': u'None', 'alias': u'None', 'component_module': None, 'position': (2, 2), 'onInit': None}], 'span': (1, 1), 'name': u'DefaultName_1121', '__version__base': '0.0.0.0', '__init_res_by_wizard__': None, '__interface__': None, 'init_expr': u'None', 'position': (191, 25), 'vgap': 0}], 'moveAfterInTabOrder': u'', 'refresh': u'None', 'border': 0, 'size': (300, -1), 'onRightMouseClick': None, 'style': 524288, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': u'', 'onLeftMouseClick': None, 'backgroundColor': (255, 255, 255), 'type': u'Panel', 'res_module': None, 'enable': True, 'description': None, '__item_id': 0, 'onClose': u'None', '_uuid': u'0a7bc1e3ebd8b631b85cc406658ed078', 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': u'None', 'name': u'PropertyPanel', 'data_name': None, 'keyDown': u'None', 'alias': u'None', 'init_expr': u'None', 'position': wx.Point(5, 5), 'onInit': None}

#   Version
__version__ = (1, 1, 2, 3)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'PropNotebookEdt'

#   Список атрибутов отображаемых в графическом редакторе
icGraphEdtLstVar = ['font', 'size', 'position', 'backgroundColor', 'foregroundColor']


def GetExampleSpc():
    spc = {'__parent__': icwidget.SPC_IC_WIDGET}
    util.icSpcDefStruct(spc, spc, True)
    spc['spec_attr'] = '''for x in range(10):
    print(x)
    '''
    spc['cols'] = 1
    spc['type'] = 'FlexGridSizer'
    spc['font'] = {}
    spc['layout'] = 'verical'
    spc['alignment'] = ''

    spc['__attr_types__'][icDefInf.EDT_NUMBER].append('cols')
    spc['__attr_types__'][icDefInf.EDT_PY_SCRIPT].append('spec_attr')

    spc['__attr_types__'][icDefInf.EDT_FONT] = ['font']
    spc['__attr_types__'][icDefInf.EDT_CHOICE] = ['layout','alignment']
    
    spc['__styles__'] = {'BU_LEFT': wx.BU_LEFT,
                         'BU_TOP': wx.BU_TOP,
                         'BU_RIGHT': wx.BU_RIGHT,
                         'BU_BOTTOM': wx.BU_BOTTOM,
                         'BU_EXACTFIT': wx.BU_EXACTFIT}
    return spc


class PropNotebookEdt:
    """
    Редактор свойств.
    """

    def __init__(self, parent):
        """
        Конструктор.
        """
        #   Признак - 'только для чтения'
        self._readonly = False
        #   Словарь списков атрибутов каждой страницы
        self._pages_flt = {}
        #   Указатель на ресурс
        self._resource = None
        #   Указатель на спецификацию
        self._spc = None
        #   Указатель на родительский ресурс
        self._prnt_res = None
        #   Координаты выбранной ячейки
        self._last_sel = (-1, -1)
        #   Указатель на дерево ресурса
        self._resTree = None
        #   Признак включения контроля полей значений свойств.
        self._ctrl = True
        
        self.context = self.evalSpace = util.InitEvalSpace()
        #   Ссылка на обкладку
        self.evalSpace['WrapperObj'] = self

        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)

        self.object = self.evalSpace['_root_obj']

    def AddAttrPageLst(self, indx, attr):
        """
        Добавляет атрибут в список заданной страницы.
        @type indx: C{int}
        @param indx: Индекс страницы.
        @type attr: C{string}
        @param attr: Имя атрибута.
        """
        if indx in self._pages_flt:
            self._pages_flt[indx].append(attr)

    def AddProperty(self, attr, value, typeEdt=icDefInf.EDT_PY_SCRIPT):
        """
        Функция добавляет свойство в ресурс.
        @type attr: C{string}
        @param attr: Имя свойства.
        @type value: C{string}
        @param value: Значение свойства.
        @type typeEdt: C{int}
        @param typeEdt: Тип редактора.
        """
        self.SetProperty(attr, value)
        res = self.GetResource()
        if typeEdt in res['__attr_types__']:
            res['__attr_types__'][typeEdt].append(attr)
        else:
            res['__attr_types__'][typeEdt] = [attr]

        self.AddAttrPageLst(2, attr)
        self.SetRenderer()
        self.GetNB().SelectTitle(2)

    def Ctrl(self, grid, value, row, col):
        """
        Контроль значений свойств.
        @type grid: C{wx.Grid}
        @param grid: Указатель на грид, в котором редактируются свойста ресурса.
        @type value: C{string}
        @param value: Проверяемое значение.
        @type row: C{int}
        @param row: Номер строки.
        @type col: C{int}
        @param col: Номер колонки.
        @rtype: C{int}
        @return: Возвращает код проверки.
        """
        if not self.IsEnableCtrl():
            return coderror.IC_CTRL_OK
        ret = coderror.IC_CTRL_OK
        attr = grid.GetTable().GetValue(row, 0)
        attr = attr.strip()
        res = self.GetResource()
        tree = self.GetResTree()
        if row >= grid.GetTable().GetNumberRows()-1:
            ret = coderror.IC_CTRL_FAILED_IGNORE
            
        #   Проверяем на уникальность имени ресурса
        elif attr == 'name':
            lst = tree.GetChildNameList(tree.GetSelection())
            if value in lst:
                msgbox.MsgBox(grid.GetView(), _('Name <%s> exist. Enter another name.') % value)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            else:
                tree.SetItemText(tree.GetSelection(), res['type']+': '+value)
                self.SetProperty(attr, value)
        else:
            #   Контроль в соответствии с типом атрибута
            typ = self.GetPropertyType(attr)
            cls = icDefInf.GetEditorClass(typ)
            ret = cls.Ctrl(value, attr=attr, propEdt=self)
            if typ is None:
                msgbox.MsgBox(grid.GetView(), _('Unknown atribute type: <%s>') % value)
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret == coderror.IC_CTRL_FAILED:
                msgbox.MsgBox(grid.GetView(), _('Invalid value type: <%s> property <%s>') % (value, attr))
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret is None:
                msgbox.MsgBox(grid.GetView(), _('Write value error:%s property <%s>') % (value, attr))
                ret = coderror.IC_CTRL_FAILED_IGNORE
            elif ret == coderror.IC_CTRL_FAILED_IGNORE:
                pass
            #   Если контроль прошел успешно, то сохраняем значение в ресурсном
            #   описании
            else:
                if 'activate' in res:
                    old = str(res['activate'])

                self.SetProperty(attr, value)
                if self.GetResTree():
                    val = self.GetProperty(attr)
                    self.GetResTree().ChangeSelGraphProperty(attr, val)
                # -----------------------------------------------------------------------
                #   Раскрашиваем неактивные элементы серым цветом начиная со старого узла
                if attr == 'activate':
                    #   По состоянию родителя определяем изменять цвет текста
                    #   или нет
                    prnt = tree.GetItemParent(tree.GetSelection())
                    if old != value and tree.GetItemTextColour(prnt) != wx.Colour(*icDefInf.DEACTIVATE_COLOR):
                        tree.SetTextColor(tree.GetSelection())
        return ret

    def DelProperty(self, prop):
        """
        Удаляет свойство.
        """
        res = self.GetResource()
        if prop in res:
            res.pop(prop)
            #   Удаляем имя атрибута из списка свойств одной из страниц
            for indx in self._pages_flt.keys():
                if prop in self._pages_flt[indx]:
                    self._pages_flt[indx].remove(prop)
        else:
            return False
        
        return True
        
    def EnableCtrl(self, bEnable):
        """
        Включает/отключает контроль.
        @type bEnable: C{bool}
        @param bEnable: Признак включения контроля значения свойств.
        """
        self._ctrl = bEnable
        
    def getObject(self):
        """
        Возвращает объект, реализуемый интерфейсом.
        """
        return self.object

    def GetResource(self):
        """
        Возвращает редактируемый ресурс.
        """
        return self._resource
    
    def GetSpc(self):
        """
        Возвращает спецификацию.
        """
        return self._spc

    def GetResTree(self):
        """
        Возвращает ссылку на дерево ресурса.
        """
        return self._resTree

    def GetResEditor(self):
        """
        Возвращает указатель на редактор ресурса
        ic.PropertyEditor.icResTree.icResourceEditor.
        """
        return self.GetResTree().GetResEditor()
        
    def GetAttr(self, row=-1):
        """
        Возвращает имя атрибута по номеру сроки.
        @type row: C{int}
        @param row: Номер строки.
        """
        grid = self.GetPropertyGrid()
        if row < 0:
            row = grid.GetGridCursorRow()

        attr = grid.GetTable().GetValue(row, 0)
        attr = attr.strip()
        return attr
        
    def GridKeyDown(self, evt):
        """
        Обработка нажатия клавиши в гриде.
        """
        attr = self.GetAttr()
        if not self.GetSpc():
            evt.Skip()
            return
            
        spc = self.GetSpc().keys()
        #   Если атрибут не описан в спецификации, то его можно удалить
        if evt.GetKeyCode() == wx.WXK_DELETE and attr not in spc and not self.isReadOnly():
            grid = self.GetPropertyGrid()
            row = grid.GetGridCursorRow()
            retmsg = msgbox.MsgBox(grid.GetView(), u'Вы действительно хотите удалить атрибут <%s>?' % attr,
                                   style=wx.YES_NO | wx.ICON_QUESTION)
            if retmsg == wx.ID_YES:
                grid.GetTable().DeleteRows(row, bAsk=False)
                self.DelProperty(attr)

            evt.Skip()
            return False

        elif evt.GetKeyCode() == wx.WXK_DELETE:
            return False
            
        elif evt.GetKeyCode() == wx.WXK_RETURN:
            self.GetPropertyGrid().DisableCellEditControl()
            self.GetPropertyGrid().MoveCursorDown(False)
            return False
            
        elif evt.GetKeyCode() == wx.WXK_INSERT:
            res = self.GetResource()
            nb = self.GetNB()
            if res and 'type' in res and res['type'] == 'DataLink':
                from ic.components.user.objects import icreloadattrdlg
                info = self.GetResTree().GetObjectsInfo()
                cls = icreloadattrdlg.ReloadAttrDlg(self.evalSpace['_dict_obj']['PropertyGrid'], info)
                dlg = cls.getObject()
                ret = dlg.ShowModal()
                if ret == wx.ID_OK:
                    typeObj = dlg.evalSpace['_dict_obj']['typeChoice'].GetStringSelection()
                    attr = dlg.evalSpace['_dict_obj']['attrChoice'].GetStringSelection()
                    nameObj = dlg.evalSpace['_dict_obj']['nameText'].GetValue()
                    val = dlg.evalSpace['_dict_obj']['valText'].GetValue()
                    self.AddProperty('%s:%s:%s' % (typeObj, nameObj, attr), val)
                
                dlg.Destroy()
                
            elif res:
                msgbox.MsgBox(None, u'В ресурс типа <%s> добавить дополнительный параметр нельзя' % res['type'])
        
    def isReadOnly(self):
        """
        Возвращает признак редактирования. True - только для чтения,
        False - редактирование.
        """
        return self._readonly
        
    def IsEnableCtrl(self):
        """
        Возвращает признак разрешения контроля поля значений свойств
        ресурсного описания.
        """
        return self._ctrl
        
    def GetPageAttrLst(self, indx):
        """
        Возвращает список атрибутов заданной страницы.
        @type indx: C{int}
        @param indx: Индекс страницы.
        """
        if indx in self._pages_flt:
            return self._pages_flt[indx]
        else:
            return None

    def GetNB(self):
        """
        Возвращает указатель на панель закладок.
        """
        if 'NB' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['NB']
        else:
            return None

    def GetPageNumber(self):
        """
        Возвращает количество групп атрибутов.
        """
        return len(self._pages_flt.keys())
        
    def GetPrntResource(self):
        """
        Возвращает родительский ресурс.
        """
        return self._prnt_res
        
    def GetProperty(self, prop):
        """
        Возвращеет значение заданного свойства.
        """
        return self.GetResource()[prop]
        
    def GetPropertyType(self, prop):
        """
        Возвращает тип свойства.
        """
        #   Определяем тип свойства
        typ = None
        tps = self.GetResource()['__attr_types__']
        for id_edt in tps.keys():
            if prop in tps[id_edt]:
                typ = id_edt
                break
        return typ

    def GetPropertyGrid(self):
        """
        Возвращает указатель на грид.
        """
        if 'PropertyGrid' in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj']['PropertyGrid']
        else:
            return None
    
    # --- BEGIN EVENT BLOCK ---
    def OnDClickEditorFuncPropertyGrid(self, evt):
        """
        Функция обрабатывает событие <EVT_LEFT_DCLICK> на редакторе
        ячеки грида.
        """
        grid = self.GetPropertyGrid()
        if grid:
            try:
                row = grid.GetGridCursorRow()
                col = grid.GetGridCursorCol()
                # имя атрибута
                attr = grid.GetTable().GetValue(row, 0)
                attr = attr.strip()
                type = grid.render.GetColAttrType(attr)
                # значение атрибута
                _val = grid.GetTable().GetValue(row, 1)
                # Пытаемся найти обработчик в коде
                if col > 0 and 'WrapperObj.' in _val and '(' in _val:
                    n1 = _val.find('WrapperObj.')
                    n2 = _val.find('(', n1)
                    
                    if n2 > n1:
                        func = _val[n1+11: n2]
                        tree = self.GetResTree()
                        if tree:
                            ide = tree.GetResEditor().GetIDEInterface()
                            if ide and ide.SelectFile(tree.GetResEditor().file):
                                ide.GoToFunc(func)
                # Автоматически создаем заготовку функции и ссылку на неё
                elif col > 0 and _val in ('', None, 'None') and type == icDefInf.EDT_PY_SCRIPT:
                    tree = self.GetResTree()
                    fl = tree.GetResEditor().file.replace('\\', '/')
                    p, ext = os.path.os.path.splitext(fl)
                    if tree:
                        ide = tree.GetResEditor().GetIDEInterface()
                        if ext != '.py':
                            fl = tree.GetResEditor().get_res_module_name(fl)
                            
                        bSel = ide and ide.SelectFile(fl)
                        
                        # Если файл не открыт пытаемся его открыть
                        if not bSel:
                            tree.GetResEditor().OnPyScript(None)
                            bSel = ide and ide.SelectFile(fl)
                            
                        if bSel:
                            grid.DisableCellEditControl()
                            nm = self.GetResource()['name']
                            func = '%s_%s' % (nm, attr)
                            # По расширению файла ресурса определяем способ вызова:
                            # '.py' - вызываем метод интерфейса, в противном случае
                            # функцию модуля ресусра
                            if ext == '.py':
                                ptFunc = 'GetWrapper().%s(evt)' % func
                            else:
                                ptFunc = 'GetManager().%s(evt)' % func
                            
                            grid.setNameValue('values', ptFunc, row)
                            
                            #   Если функции нет, то добавляем заготовку в
                            #   текст модуля
                            ide.insertEvtFuncToInterface(fl, func)
                            grid.EnableCellEditControl()
            except:
                io_prnt.outLastErr('###')
        
        return None

    def OnSelectPage(self, indx):
        """
        Фильтрует список свойств в зависимости от закладки.
        """
        #   Отключаем контроль на значения свойств
        self.EnableCtrl(False)
        nb = self.GetNB()
        resource = self.GetResource()
        grid = self.GetPropertyGrid()
        if grid:
            lst = self.GetPageAttrLst(indx)
            grid.BeginBatch()
            old_init = grid.resource['init']
            grid.resource['init'] = None
        
            #   Чистим список атрибутов
            dn = len(lst) - (grid.GetTable().GetNumberRows()-1)
            num = (grid.GetTable().GetNumberRows()-1)
            if dn < 0:
                for i in range(-dn):
                    grid.GetTable().DeleteRows(0, bAsk=False)
            elif dn > 0:
                grid.AddRows(dn)
            
            #   Заполняем нужными свойства
            indx = 0
            for key in lst:
                if key in resource:
                    grid.setNameValue('attributes', '  '+key, indx)
                    if isinstance(resource[key], unicode):
                        val = resource[key]
                    else:
                        val = unicode(resource[key])

                    grid.setNameValue('values', val, indx)
                    grid.Update(indx)
                    indx += 1
            grid.EndBatch()
            grid.resource['init'] = '@False'
            grid.MakeCellVisible(0, 0)

        #   Включаем контроль на значения свойств
        self.EnableCtrl(True)

    def OnSizeGrid(self, evt):
        """
        Обработка изменения размера грида.
        """
        grid = self.GetPropertyGrid()
        if not grid:
            return
        sx, sy = grid.GetSize()
        w0 = grid.GetColSize(0)
        if (sx - w0) > 50:
            grid.SetColSize(1, int(sx - w0-5))
        else:
            grid.SetColSize(1, 50)
        
    def OnSelectGridCell(self, row, col):
        """
        Функция вызывается при выборе ячейки грида.
        @type row: C{int}
        @param row: Номер ряда.
        @type col: C{int}
        @param col: Номер колонки.
        """
        grid = self.GetPropertyGrid()
        if grid:
            grid.SetFocus()
            # имя атрибута
            attr = grid.GetTable().GetValue(row, 0)
            attr = attr.strip()
            try:
                type = grid.render.GetColAttrType(attr)
                # значение атрибута
                _val = grid.GetTable().GetValue(row, 1)
                if col == 0:
                    pass
                elif type != icDefInf.EDT_PY_SCRIPT and row < grid.GetTable().GetNumberRows():
                    select_evt = wx.grid.GridEvent(wx.NewId(), wx.grid.wxEVT_GRID_CELL_LEFT_DCLICK, grid, row, col)
                    grid.GetEventHandler().AddPendingEvent(select_evt)

                # Ищем функцию в тексте модуля
                # GetInterface и WrapperObj синонимы
                func = None
                fl = None
                tree = self.GetResTree()
                if _val:
                    _val = _val.replace('GetInterface().', 'WrapperObj.').replace('GetWrapper().', 'WrapperObj.')

                if _val and col > 0 and 'WrapperObj.' in _val and '(' in _val:
                    fl = tree.GetResEditor().file.replace('\\', '/')
                    n1 = _val.find('WrapperObj.')
                    n2 = _val.find('(', n1)
                    if n2 > n1:
                        func = _val[n1+11: n1+n2]
                    else:
                        func = _val[n1+11:]
                        
                prz_lst = ('GetResModule().', 'GetManager().')
                for prz in prz_lst:
                    if _val and col > 0 and prz in _val:
                        lp = len(prz)
                        fl = tree.GetResEditor().get_res_module_name()
                        n1 = _val.find(prz)
                        n2 = _val.find('(', n1+lp)
                        if n2 > n1:
                            func = _val[n1+lp: n1+n2]
                        else:
                            func = _val[n1+lp:]

                if func and fl:
                    if tree:
                        ide = tree.GetResEditor().GetIDEInterface()
                        if ide and ide.SelectFile(fl):
                            ide.GoToFunc(func)
            except:
                io_prnt.outLastErr('###')

    def OnPostSelectGridCell(self, row, col):
        """
        Функция вызывается после выбора ячейки грида.
        @type row: C{int}
        @param row: Номер ряда.
        @type col: C{int}
        @param col: Номер колонки.
        """
        _grid = self.GetPropertyGrid()
        try:
            attr = _grid.GetTable().GetValue(row, 0)
            attr = attr.strip()
            type = _grid.render.GetColAttrType(attr)
            _val = _grid.GetTable().GetValue(row, 1)
            if col == 1 and type == icDefInf.EDT_PY_SCRIPT and self._last_sel != (row, col):
                r = _grid.CellToRect(row, col)
                self._last_sel = (row, col)
                sx, sy = _grid.GetSize()
                res = self.GetResource()
                tree = self.GetResTree()
                if tree and tree.GetPanelGroup():
                    tx, ty = tree.GetPanelGroup().GetSize()
                    sy = 0
                    prnt = tree.GetPanelGroup()
                else:
                    tx, ty = 0, 0
                    prnt = _grid
        
                if '_uuid' in res:
                    _uuid = res['_uuid']
                else:
                    _uuid = ic_uuid.get_uuid()
            
                if _val and _val.find('\n') >= 0:
                    cls = icDefInf.GetEditorClass(type)
                    bEnable = not self.isReadOnly()
                    prz, val, _uuid = cls.HlpDlg(prnt, attr, _val, pos=(r.x+70, 0),
                                                 size=(sx-r.x-70, sy+ty), uuid_attr=_uuid, bEnable=bEnable)
                    #   Обновляем uuid
                    if prz:
                        Resource.RefreshResUUID(res, self.GetPrntResource(), _uuid)
                        ret = _grid.setNameValue('values', val)
                else:
                    Resource.RefreshResUUID(res, self.GetPrntResource(), ic_uuid.get_uuid())
                    _grid.EnableCellEditControl()

            self._last_sel = (row, col)
        except:
            io_prnt.outLastErr('###')
    
    def OnHelpFuncValues(self, grid, row, col, evt):
        """
        Функция помощи на поле значения <hlp>.
        """
        import ic.PropertyEditor.icExternalEditors as edt
        from ic.utils import ic_uuid
        import ic.utils.ic_util as ic_util
        attr = grid.GetTable().GetValue(row, 0)
        attr = attr.strip()
        type = grid.render.GetColAttrType(attr)
        _val = grid.GetTable().GetValue(row, 1)
        cls = icDefInf.GetEditorClass(type)
        
        # Определяем позицию и размер
        r = grid.CellToRect(row, col)
        dx, dy = grid.GetScrollPixelsPerUnit()
        vx, vy = grid.GetViewStart()
        scr_x = dx*vx
        scr_y = dy*vy
        screen_x, screen_y = wx.GetDisplaySize()
        sx, sy = (-1, 150)
        px, py = grid.ClientToScreenXY(0, r.y+20-scr_y)
        
        if py + sy + 20 > screen_y:
            pos = (r.x-scr_x, r.y-scr_y-sy)
        else:
            pos = (r.x-scr_x, r.y+20-scr_y)
        
        # Вызываем нужный редактор
        if type == icDefInf.EDT_COMBINE and attr in grid._styles_attr:
            styles = grid._styles_attr[attr]
            cls.SetAttrCombDict(attr, styles)
            return cls.HlpDlg(grid.GetView(), attr, _val, pos=pos, size=(sx, sy))
        
        elif type == icDefInf.EDT_CHOICE:
            _res = self._spc
            
            if '__lists__' in _res and attr in _res['__lists__']:
                lst = _res['__lists__'][attr]
                if py + sy + 20 > screen_y:
                    pos = (r.x-scr_x, r.y-scr_y)
                else:
                    pos = (r.x-scr_x, r.y+20-scr_y)
                    
                cls.SetAttrListDict(attr, lst)
                return cls.HlpDlg(grid.GetView(), attr, _val, pos=pos, size=(sx, sy), style=wx.CANCEL)
        
        elif type in (icDefInf.EDT_PY_SCRIPT, icDefInf.EDT_TEXTDICT, icDefInf.EDT_TEXTLIST):
            r = grid.CellToRect(row, col)
            sx, sy = grid.GetSize()
            res = self.GetResource()
            tree = self.GetResTree()
        
            if tree and tree.GetPanelGroup():
                tx, ty = tree.GetPanelGroup().GetSize()
                sy = 0
                prnt = tree.GetPanelGroup()
            else:
                tx, ty = 0, 0
                prnt = grid.GetView()
        
            if '_uuid' in res:
                _uuid = res['_uuid']
            else:
                _uuid = ic_uuid.get_uuid()
        
            if type in (icDefInf.EDT_TEXTDICT, icDefInf.EDT_TEXTLIST):
                _val = ic_util.StructToTxt(eval(_val))
        
            prz, val, _uuid = cls.HlpDlg(prnt, attr, _val, pos=(r.x+70, 0),
                                         size=(sx-r.x-70, sy+ty), uuid_attr=_uuid, bEnable=True)
            
            if type in (icDefInf.EDT_TEXTDICT, icDefInf.EDT_TEXTLIST):
                val = val.replace('\r\n', '').replace('\n', '')
                
            #   Обновляем uuid
            if prz:
                prnt_res = self.GetPrntResource()
                Resource.RefreshResUUID(res, prnt_res, _uuid)
                return val
        else:
            return cls.HlpDlg(grid.GetView(), attr, _val, pos, (sx, sy), propEdt=self)

        return None
        
    def OnInitExpr(self):
        nb = self.GetNB()
        nb.GetTitle(0).SetDescription(_('Base'))
        nb.GetTitle(1).SetDescription(_('Visual'))
        nb.GetTitle(2).SetDescription(_('Special attributes'))
        nb.GetTitle(3).SetDescription(_('Events'))
        nb.GetTitle(4).SetDescription(_('All'))

    def resource_init_expr(self):
        _dict_obj = self.context['_dict_obj']
        #   Ресурс родительского компонента
        if 'parent_resource' not in _dict_obj:
            _dict_obj['parent_resource'] = None

        #   Если не определен режим работы (просмотр, редактирование),
        #   то устанавливаем режим редактировния.
        if 'bEditMode' not in _dict_obj:
            _dict_obj['bEditMode'] = True

        #   Сервисные переменные
        _dict_obj['_last_select'] = (-1, -1)

        return None
    
    def PropertyGrid_getattr(self, col):
        grid = self.context['_dict_obj']['PropertyGrid']
        if col == 1:
            attr = grid.val_col_attr
            attr.IncRef()
            return attr
        else:
            return None
    
    def PropertyGrid_post_select(self, evt):
        _row, _col = evt.GetData()
        return self.OnPostSelectGridCell(_row, _col)

    def PropertyGrid_init_expr(self):
        grid = self.context['_dict_obj']['PropertyGrid']
        nb = self.context['_dict_obj']['NB']
        self.SetResource(None)
        #   Отключаем частотный словарь
        grid.EnableFreqDict(False)

    ###END EVENT BLOCK
    
    def RefreshView(self):
        """
        Обновляет представление грида.
        """
        nb = self.evalSpace['_dict_obj']['NB']
        indx = nb.GetSelected()
        if 'PropertyGrid' in self.evalSpace['_dict_obj']:
            grid = self.evalSpace['_dict_obj']['PropertyGrid']
            lst = self.GetPageAttrLst(indx)
            grid.BeginBatch()
            grid.resource['init'] = None
            #   Чистим список атрибутов
            dn = len(lst) - (grid.GetTable().GetNumberRows()-1)
            num = (grid.GetTable().GetNumberRows()-1)
            if dn < 0:
                for i in range(-dn):
                    grid.GetTable().DeleteRows(0, bAsk=False)
            elif dn > 0:
                grid.AddRows(dn)
            
            #   Заполняем нужными свойства
            for indx, key in enumerate(lst):
                grid.setNameValue('attributes', '  '+key, indx)
                grid.setNameValue('values', str(resource[key]), indx)
                grid.Update(indx)
        
            grid.EndBatch()
            grid.resource['init'] = '@False'
            return True
            
        return False

    def SetNameProperty(self, prop, value):
        """
        Устанавливает значение заданного свойства.
        @type prop: C{string}
        @param prop: Имя атрибута.
        @param value: Значение атрибута.
        """
        if prop in self.GetResource():
            self.GetResource()[prop] = value
            return True
            
        return False
   
    def SetProperty(self, prop, value):
        """
        Устанавливает значение заданного свойства. Предварительно,
        значение преобразуется к нужному типу.
        @type prop: C{string}
        @param prop: Имя атрибута.
        @type value: C{string}
        @param value: Значение атрибута.
        """
        #   Определяем тип свойства
        typ = self.GetPropertyType(prop)
        if typ is not None:
            if typ == icDefInf.EDT_USER_PROPERTY:
                cls = icDefInf.GetEditorClass(typ)
                self.GetResource()[prop] = cls.strToVal(value, self)
            else:
                #   Преобразуем к нужному типу
                self.GetResource()[prop] = icDefInf.strToVal(typ, value)
        else:
            self.GetResource()[prop] = unicode(value)

    def SetResTree(self, resTree):
        """
        Установить ссылку на дерево ресурса.
        @type resTree: C{icResTree.icResTree}
        @param resTree: Указатель на дерево ресурса.
        """
        self._resTree = resTree
        
    def SetSpc(self, spec):
        """
        Устанавливает спецификацию ресурса.
        """
        util.icSpcDefStruct(spec, spec, True)
        self._spc = spec

    def SetReadOnly(self, bReadOnly=True):
        """
        Устанавливает режим чтения.
        """
        self._readonly = bReadOnly

    def SelectPropertyEdt(self, prop):
        """
        Устанавливает заданное свойство на редактирование.
        @type prop: C{string}
        @param prop: Свойство ресурса, которое надо редактировать.
        """
        for i in range(self.GetPageNumber()):
            lst = self.GetPageAttrLst(i)
            if prop in lst:
                self.GetNB().SelectTitle(i)
                row = lst.index(prop)
                _grid = self.GetPropertyGrid()
                _grid.SetGridCursor(row, 1)
                break
                
    def SetResource(self, res, spec=None, parent_res=None):
        """
        Устанавливает ресурс на редактирование.
        @type res: C{dictionary}
        @param res: Ресурс, который будет редактироваться.
        @type spec: C{dictionary}
        @param spec: Спецификация ресурса. Используется для определения атрибутов, не
            описанных в спецификации. В редакторе они помечаются цветом.
        @type parent_res: C{dictionary}
        @param parent_res: Родительский ресурс.
        """
        #   Принудительно выходим из редактирования
        grid = self.evalSpace['_dict_obj']['PropertyGrid']
        grid.DisableCellEditControl()
        self._prnt_res = parent_res
        self.SetSpc(spec)
        if not res:
            res = {}
            pages = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
            self._pages_flt.update(pages)
            res['__attr_types__'] = {}
            res['__styles__'] = {}
            self._resource = res
            self.SetRenderer()
            self.GetNB().SelectTitle(0)
            return

        self._resource = res
        self._prnt_res = parent_res
        self._spc = spec
        if '__events__' in res:
            events_attr = res['__events__'].keys()
        else:
            events_attr = []
            
        #   Определяем списки атрибутов для каждой закладки
        pages = {}
        self._pages_flt = {}
        
        #   Создаем новый список атрибутов
        #   Закладка базовых атрибутов
        spc_lst = ['type', 'child', 'win1', 'win2', 'cell_attr', 'label_attr']
        spc_flt = []
        
        #   Первичная фильтрация
        for key in res:
            if not key.startswith('_') and key not in spc_lst and \
                    not (key == 'cols' and not res['type'] in ('GridSizer', 'FlexGridSizer')):
                spc_flt.append(key)
        
        #   Сортируем
        spc_flt.sort()
        if 'name' in spc_flt:
            spc_flt.remove('name')
            spc_flt = ['name'] + spc_flt
        
        # ---------------------------------------
        #   0 - Закладка базовых атрибутов
        indx = 0
        lst = []
        sizer_par_lst = []
        for key in icwidget.SPC_IC_SIMPLE:
            if key in spc_flt:
                if key in ('flag', 'proportion', 'size', 'position', 'border', 'span'):
                    sizer_par_lst.append(key)
                else:
                    lst.append(key)
        lst.sort()
        lst.remove('name')
        lst = ['name'] + lst + ['_uuid']
        pages[indx] = lst
        
        # ---------------------------------------
        #   1 - Закладка визуальных атрибутов
        indx = 1
        lst = []
        buff_lst = {}
        buff_lst.update(icwidget.SPC_IC_BASE)
        buff_lst.update(icwidget.SPC_IC_WIDGET)
        for key in buff_lst:
            if key in spc_flt and key not in ('name', 'source') and key not in events_attr:
                lst.append(key)
        
        lst.sort()
        lst = lst + sizer_par_lst
        pages[indx] = lst
        
        # ----------------------------------------
        #   2 - Закладка специальных атрибутов
        indx = 2
        rk = pages[0] + pages[1]
        lst = []
        for key in spc_flt:
            if not key in rk and not key in events_attr:
                lst.append(key)
        
        lst.sort()
        pages[indx] = lst
        
        # ----------------------------------------
        #   3 - Закладка обработчиков событий
        indx = 3
        lst = []
        for attr in events_attr:
            if attr in res.keys():
                lst.append(attr)
                
        lst.sort()
        pages[indx] = lst
        
        # -------------------------------------------
        #   4 - Закладка всех атрибутов
        indx = 4
        pages[indx] = spc_flt
        self._pages_flt.update(pages)
        self.SetRenderer()
        self.GetNB().SelectTitle(res.get('__default_page__', 0) or 0)

    def SetRenderer(self):
        """
        Устанавливает отрисовку свойств.
        """
        grid = self.evalSpace['_dict_obj']['PropertyGrid']
        nb = self.evalSpace['_dict_obj']['NB']
        res = self.GetResource()
        spec = self.GetSpc()
        if not res:
            return
        #   Ищем в ресурсе атрибуты, у которых не описан тип
        lst = []
        def_lst = []
        if '__attr_types__' not in res:
            res['__attr_types__'] = icwidget.SPC_IC_SIMPLE['__attr_types__']
        
        #   Определяем список, описанных атрибутов
        for key in res['__attr_types__']:
            def_lst += res['__attr_types__'][key]
            
        #   Ищем не описанные атрибуты
        for attr in res:
            if not attr.startswith('_') and attr not in def_lst:
                lst.append(attr)
        
        if lst and icDefInf.EDT_PY_SCRIPT in res['__attr_types__']:
            res['__attr_types__'][icDefInf.EDT_PY_SCRIPT] += lst
            
        elif lst and icDefInf.EDT_PY_SCRIPT not in res['__attr_types__']:
            res['__attr_types__'][icDefInf.EDT_PY_SCRIPT] = lst

        grid.render = icrender.PropValueRenderer(grid.GetTable(), color=wx.Colour(0, 85, 170), propEdt=self)
        grid.render.SetColAttrTypes(res['__attr_types__'])
        
        #   Создаем визуальные атрибуты колонки значений
        grid.val_col_attr = Grid.GridCellAttr()
        if self.isReadOnly():
            grid.val_col_attr.SetReadOnly()
            
        grid.val_col_attr.SetRenderer(grid.render)
        #   Задаем базис разложения комбинированных стилей
        if spec and '__styles__' in spec:
            grid._styles_attr = {'style': spec['__styles__']}
        else:
            grid._styles_attr = {}
            
        grid._styles_attr['flag'] = icDefInf.ICSizerFlag
        #   Задаем списки выбора для списковых атрибутов
        if spec and '__lists__' in spec:
            grid._lists_attr = copy.deepcopy(spec['__lists__'])
        else:
            grid._lists_attr = {}

        grid.EnableFreqDict(False)
        
    def SelectPropertyPage(self, indx):
        """
        Открывает нужную страницу свойств.
        """
        self.GetNB().SelectTitle(indx)


# Функции тестирования


class TestFrame(wx.Frame):
    def __init__(self, parent, id, label):
        wx.Frame.__init__(self, parent, id, label)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        self.Refresh()
        evt.Skip()


def test(par=0):
    """
    Тестируем класс PropNotebookEdt.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = TestFrame(None, -1, 'Test')

    #
    # Тестовый код
    #
    cls = PropNotebookEdt(frame)
    res = GetExampleSpc()
    cls.SetResource(res)
    
    frame.Show(True)

    app.MainLoop()


if __name__ == '__main__':
    test()
