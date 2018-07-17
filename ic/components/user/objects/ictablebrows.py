#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.components.icgrid as icgrid

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'obj_module': None, 'show': 1, '__attr_types__': {0: ['moveAfterInTabOrder', 'name', 'type', 'data_name', 'docstr', 'label', 'alias', 'field_name'], 1: ['layout', 'alignment'], 2: ['enable'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 9: ['font'], 10: ['position', 'span'], 11: ['size'], 12: ['source', 'activate', 'pre_init_expr', 'refresh', 'show', 'init_expr', 'onClose', 'recount', 'keyDown', 'description', 'onRightMouseClick', 'component_module', 'onLeftMouseClick', 'child', 'onInit'], 17: ['res_module', '_uuid', 'obj_module'], 40: ['border', 'proportion']}, 'child': [{'activate': 1, 'obj_module': None, '__default_page__': 0, '__attr_types__': {0: ['name', 'data_name', 'alias', 'type'], 16: ['sourcePsp'], 12: ['activate', 'description', 'component_module', 'filter', 'init_expr', 'pre_init_expr'], 17: ['obj_module', '_uuid', 'res_module'], 7: ['style']}, 'data_name': None, 'style': 0, 'alias': None, '__version__base': '0.0.0.0', '__version__': '0.0.0.0', 'type': u'Recordset', '__doc__': '', 'res_module': None, '__styles__': None, '__events__': {}, 'description': None, '__item_id': 1, '_uuid': u'fd23d1afafaf9f0c11c29761391e86bf', '__brief_attrs__': [], 'component_module': None, 'name': u'table', 'filter': None, '__init_res_by_wizard__': None, '__interface__': None, 'init_expr': None, 'sourcePsp': None}, {'activate': 1, 'obj_module': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'type': u'BoxSizer', 'res_module': None, 'hgap': 0, 'description': None, '__item_id': 2, '_uuid': u'e1874b23a10e1caf170832c22bfcd696', 'flag': 0, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': None, 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': wx.Size(512, 28), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'res_module': None, 'init_expr': None, 'description': None, 'shortHelpString': u'', '__item_id': 3, 'backgroundColor2': None, '_uuid': u'51371847b580e2b254f2c12f26490c70', 'moveAfterInTabOrder': u'', 'bgrImage': None, 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'text': u'\u041a\u043b\u0430\u0441\u0441 \u0434\u0430\u043d\u043d\u044b\u0445:', 'keyDown': None, 'font': {'style': 'italic', 'size': 11, 'underline': False, 'family': 'sansSerif', 'faceName': 'Arial'}, 'border': 0, 'size': (70, 18), 'style': 0, 'foregroundColor': (0, 74, 149), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'StaticText', 'res_module': None, 'description': None, '__item_id': 4, '_uuid': u'105653d02c1208a1b80210ca0d73fb55', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'tableName', 'refresh': None, 'alias': None, 'init_expr': None, 'position': wx.Point(8, 5), 'onInit': None}], 'onLeftDown': None, 'cursorColor': (100, 100, 100), 'borderStyle': None, 'borderStep': 2, 'borderLeftColor': None, 'name': u'HeadCell_1415_1570', 'borderBottomColor': None, 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 0), 'backgroundType': 0, 'onInit': None}, {'alias': None, 'activate': 1, 'obj_module': None, 'show': 1, '__attr_types__': {0: ['alias', 'moveAfterInTabOrder', 'name', 'type', 'data_name', 'field_name', 'label'], 1: ['layout', 'alignment'], 2: ['enable', 'buttonHelp', 'buttonDel', 'buttonUpdate', 'buttonAdd', 'buttonPrint'], 7: ['flag', 'style'], 8: ['foregroundColor', 'backgroundColor'], 9: ['font'], 10: ['position', 'span'], 11: ['size'], 12: ['activate', 'description', 'show', 'pre_init_expr', 'refresh', 'source', 'keyDown', 'recount', 'init_expr', 'component_module', 'onPrint', 'onAdd', 'object_link', 'onHelp', 'onUpdate', 'onDelete', 'onInit'], 17: ['res_module', '_uuid', 'obj_module'], 40: ['border', 'proportion']}, 'buttonDel': 1, 'data_name': None, 'proportion': 0, '__default_page__': 0, 'keyDown': None, 'border': 0, 'size': (200, -1), 'style': 2097188, 'object_link': None, 'span': (1, 1), '__init_res_by_wizard__': None, 'component_module': None, 'onPrint': None, 'buttonAdd': 1, 'source': u'table', '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, 'onAdd': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': u'DatasetNavigator', '__doc__': None, 'res_module': None, '__styles__': None, '__events__': {'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False), 'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False)}, 'enable': True, 'description': None, '__item_id': 5, 'buttonPrint': 0, '_uuid': u'bec136af8f15b7df3ae3933d2b570904', 'onHelp': None, 'moveAfterInTabOrder': u'', '__brief_attrs__': [], 'onUpdate': None, 'flag': 8192, 'foregroundColor': None, 'recount': None, 'onDelete': None, 'onInit': None, 'name': u'navigator', 'refresh': None, '__version__icwidget': '0.0.0.0', '__version__base': '0.0.0.0', '__interface__': None, 'init_expr': None, 'buttonHelp': 0, 'position': wx.Point(0, 0), 'buttonUpdate': 0}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1169_1324', '__item_id': 6, 'type': u'SizerSpace', '_uuid': u'29a00cf50432d7e21752c02c7ae4af08', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 5)}, {'activate': 1, 'name': u'GenGrid', '__item_id': 7, '_uuid': 'f4d29e9172825281759e648d9cbd566f', 'docstr': 'ic.db.icdataset-module.html', 'filter': None, 'alias': None, 'res_query': u'', 'init_expr': u"ctrl = WrapperObj.GetNameObj('tableName')\r\nctrl.SetLabel(GetObject('table').resource['name'])", 'file': u'', 'type': u'DataLink', 'link_expr': u'WrapperObj.generateGridRes()'}, {'style': 0, 'activate': 1, 'span': (1, 1), 'name': u'DefaultName_1169', '__item_id': 8, 'type': u'SizerSpace', '_uuid': u'29a00cf50432d7e21752c02c7ae4af08', 'proportion': 0, 'alias': None, 'flag': 0, 'init_expr': None, 'position': (-1, -1), 'border': 0, 'size': (0, 2)}], 'layout': u'vertical', 'name': u'bszr', 'alias': None, 'init_expr': None, 'position': wx.Point(56, 45), 'vgap': 0}], 'refresh': None, 'border': 0, 'size': wx.Size(519, 576), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'alias': None, 'component_module': None, '__default_page__': 1, 'proportion': 0, 'source': None, '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, 'onLeftMouseClick': None, 'backgroundColor': None, '__version__': '0.0.0.0', 'type': u'Panel', '__doc__': None, 'res_module': None, '__styles__': {'DOUBLE_BORDER': 268435456, 'MINIMIZE_BOX': 1024, 'NO_FULL_REPAINT_ON_RESIZE': 0, 'CLIP_CHILDREN': 4194304, 'SUNKEN_BORDER': 134217728, 'RAISED_BORDER': 67108864, 'TAB_TRAVERSAL': 524288, 'MAXIMIZE_BOX': 512, 'STATIC_BORDER': 16777216, 'SIMPLE_BORDER': 33554432, 'CAPTION': 536870912, 'WANTS_CHARS': 262144, 'VSCROLL': -2147483648, 'THICK_FRAME': 64, 'HSCROLL': 1073741824, 'TRANSPARENT_WINDOW': 1048576}, '__events__': {'onRightMouseClick': ('wx.EVT_RIGHT_DOWN', 'OnRightDown', False), 'onClose': ('wx.EVT_CLOSE', 'ObjDestroy', False), 'onLeftMouseClick': ('wx.EVT_LEFT_DOWN', 'OnLeftDown', False), 'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False), 'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False)}, 'enable': True, 'description': None, '__item_id': 0, 'onClose': None, '_uuid': u'4eb34c1581ee8ba9eb3b67f36fde8957', 'style': 524288, '__brief_attrs__': [], 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 0, 'recount': None, 'name': u'browsPanel', 'data_name': None, '__version__base': '0.0.0.0', 'keyDown': None, '__version__icwidget': '0.0.0.0', '__init_res_by_wizard__': None, '__interface__': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}

#   Version
__version__ = (1, 0, 1, 9)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'TableBrows'


class TableBrows:

    def __init__(self, parent, table='analitic', ext='tab'):
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        
        # Устанавливаем имя таблицы
        self._setRSSourcePsp(table, ext)
        
        self.__obj = prs.icBuildObject(parent, resource, evalSpace=self.evalSpace, bIndicator=False)
        self.object = self.evalSpace['_root_obj']
        
    def getObject(self):
        """
        """
        return self.object

    def GetNameObj(self, name):
        """
        Возвращает указатель на объект с указанным именем.
        """
        if name in self.evalSpace['_dict_obj']:
            return self.evalSpace['_dict_obj'][name]
        else:
            return None
        
    def generateGridRes(self, ds_res=None):
        """
        Генерируется ресурсное описание грида по классу данных.
        @type ds_res: C{dictionary}
        @param ds_res: Ресурсное описание вкласса данных.
        """
        if not ds_res:
            ds_res = self.GetNameObj('table').resource
            
        grid_res = {}
        util.icSpcDefStruct(icgrid.SPC_IC_GRID, grid_res)
        grid_res['name'] = 'grid'
        grid_res['type'] = 'GridDataset'
        grid_res['source'] = 'table'
        grid_res['cols'] = []
        grid_res['_uuid'] = ds_res['_uuid']
        if not ds_res.get('table', None):
            grid_res['table'] = ds_res['name']
        
        # Генерируем описание колонок
        for i, fld_res in enumerate(ds_res['child']):
            col = {}
            util.icSpcDefStruct(icgrid.SPC_IC_CELL, col)
            col['label'] = fld_res['name']
            col['width'] = 100
            
            if fld_res['type'] == 'Field':
                col['name'] = fld_res['name']
                if '_uuid' in fld_res:
                    col['_uuid'] = fld_res['_uuid']
                
                if fld_res['type_val'] == 'F':
                    col['pic'] = 'F'
                elif fld_res['type_val'] == 'I':
                    col['pic'] = 'N'
                    
                grid_res['cols'].append(col)
            
        return grid_res
        
    def _getGridRes(self):
        """
        Возвращает ресурсное описание грида.
        """
        bszr = resource['child'][1]
        
        for i, res in enumerate(bszr['child']):
            if res['name'] == 'grid':
                return res
        
        return None
        
    def _setDataLinkTableName(self, table, ext):
        """
        Устанавливает имя таблицы просмотра - прописываются соответствующие
        атрибуты в объекте DataLink.
        """
        if table:
            res = resource['child'][0]
            res['file'] = '%s.%s' % (table, ext)
            res['res_query'] = table
            return True
            
        return False

    def _setRSSourcePsp(self, table, ext):
        """
        Устанавливает паспорт таблицы в Recordset.
        """
        if table:
            for res in resource['child']:
                if res['type'] == 'Recordset':
                    res['sourcePsp'] = ((None, None, None, '%s.%s' % (table, ext), None),)
                    return True
            
        return False


def test(par=0):
    """
    Тестируем класс TableBrows.
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
