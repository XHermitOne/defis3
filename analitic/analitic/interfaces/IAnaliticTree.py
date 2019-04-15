#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import wx

import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.components.user.ictabletreelist as ictabletreelist

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource = {'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': '', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': 'Dialog', 'onClose': '', '_uuid': '0ccd9321b4dadadd2d428fab5327ef57', 'moveAfterInTabOrder': '', 'killFocus': '', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': 'vertical', 'name': 'DefaultName_1467', 'position': (0, 0), 'type': 'BoxSizer', '_uuid': 'cfcbda6926a8a94afd6cb1a6b33c7770', 'proportion': 1, 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': 'Panel', 'onClose': '', '_uuid': 'c1c7a0cd0b55fbc5aa9973151c411928', 'style': 524288, 'docstr': 'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'style': 0, 'activate': 1, 'prim': '', 'name': 'Описание данных', '_uuid': '021e5c865e1872481b37388b13643dbc', 'alias': None, 'init_expr': None, 'child': [{'activate': 1, 'name': 'Table', '_uuid': '3f569e1d1a7d12722275519ea5863610', 'docstr': 'ic.db.icdataset-module.html', 'filter': 'WrapperObj.filterFuncTable(evt)', 'alias': None, 'res_query': 'analitic', 'init_expr': None, 'file': 'analitic.tab', 'type': 'DataLink', 'link_expr': None, '__item_id': 4}], 'type': 'Group', '__item_id': 3, '__attr_types__': {12: ['init_expr', 'pre_init_expr', 'description'], 0: ['name', 'alias', 'data_name', 'type'], 17: ['_uuid', 'obj_module', 'res_module'], 7: ['style'], 2: ['activate']}, '__styles__': {'DEFAULT': 0}, 'component_module': None, 'res_module': None, 'obj_module': None, 'description': None, 'data_name': None, '__default_page__': 0, '__interface__': None, '__brief_attrs__': [], '__doc__': None, '__version__base': '0.0.0.0', '__version__': '0.0.0.0', '__init_res_by_wizard__': None, '__attr_hlp__': {'name': 'Имя объекта', 'type': 'Тип объекта', 'activate': 'Вкл./Выкл. создание объекта', 'data_name': 'Имя данных из контекста', 'description': 'Описание', 'style': 'Стиль компонента', 'init_expr': 'Выражение, выполняемой при инициализации компонента', 'component_module': 'Модуль компонента', 'res_module': 'Модуль ресурса', 'obj_module': 'Модуль объекта'}}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': 'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': 'BoxSizer', '_uuid': 'd150e8c27a77f8d4add04024891528d9', 'proportion': 0, 'name': 'BSZR', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'orderBy': '', 'activate': 1, 'show': 1, 'labels': ['Аналитика', 'Сумма', 'План'], 'activated': 'WrapperObj.activatedFuncAnaliticTreeList(evt)', 'refresh': None, 'border': 0, 'init_sprav_buff': '', 'size': wx.Size(341, 378), 'style': 8201, 'foregroundColor': None, 'span': (1, 1), 'selected': None, 'proportion': 1, 'source': 'Table', 'backgroundColor': None, 'codfield': [('dtoper', (0, 10), None), ('reg', (0, 4), ('Region', 'name')), ('mens', (1, 4), ('Menager', 'name')), ('codt', (0, 3), ('Product', 'name'))], 'titleRoot': 'Регионы', 'type': 'TableTreeList', 'filterExpr': "_Table.q.dtoper.startswith('2005.03.11')", '_uuid': 'c97a43b850d08752bd78a9c911ba9393', 'moveAfterInTabOrder': '', 'flag': 8192, 'recount': None, 'name': 'AnaliticTreeList', 'wcols': [200], 'fields': ['summa', 'plan_sum'], 'keyDown': None, 'alias': None, 'init_expr': '', 'position': (-1, -1), 'onInit': 'WrapperObj.OnInit(evt)', '__item_id': 6, '__attr_types__': {0: ['orderBy', 'name', 'alias', 'data_name', 'titleRoot', 'label', 'moveAfterInTabOrder', 'mask', 'field_name', 'type'], 20: ['fields', 'labels', 'codfield', 'wcols'], 12: ['activated', 'refresh', 'selected', 'recount', 'keyDown', 'description', 'init_expr', 'show', 'pre_init_expr', 'source'], 8: ['foregroundColor', 'backgroundColor'], 2: ['enable', 'activate'], 9: ['font'], 10: ['position', 'span'], 11: ['size'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 1: ['layout', 'alignment'], 17: ['res_module', '_uuid', 'obj_module']}, '__styles__': {'TR_NO_BUTTONS': 0, 'TR_HAS_BUTTONS': 1, 'TR_NO_LINES': 4, 'TR_LINES_AT_ROOT': 8, 'TR_SINGLE': 0, 'TR_MULTIPLE': 32, 'TR_HAS_VARIABLE_ROW_HEIGHT': 128, 'TR_EDIT_LABELS': 512, 'TR_HIDE_ROOT': 2048, 'TR_ROW_LINES': 1024, 'TR_FULL_ROW_HIGHLIGHT': 8192, 'TR_DEFAULT_STYLE': 5, 'TR_TWIST_BUTTONS': 16}, '__events__': {'selected': ('wx.EVT_TREE_SEL_CHANGED', 'OnSelected', False), 'activated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'OnActivated', False), 'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDWN', False), 'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False)}, 'enable': True, '__version__icwidget': '0.0.0.0', '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, 'component_module': None, 'res_module': None, 'obj_module': None, 'description': None, 'data_name': None, '__default_page__': 0, '__interface__': None, '__brief_attrs__': [], '__doc__': None, '__version__base': '0.0.0.0', '__version__': '0.0.0.0', '__init_res_by_wizard__': None, '__attr_hlp__': {'name': 'Имя объекта', 'type': 'Тип объекта', 'activate': 'Вкл./Выкл. создание объекта', 'data_name': 'Имя данных из контекста', 'description': 'Описание', 'style': 'Стиль компонента', 'init_expr': 'Выражение, выполняемой при инициализации компонента', 'component_module': 'Модуль компонента', 'res_module': 'Модуль ресурса', 'obj_module': 'Модуль объекта', 'size': 'Размер объекта', 'position': 'Позиция', 'span': 'Определяет сколько ячеек по горизонтали и вертикали должен занимать компонент', 'proportion': 'Признак пропорционального размера', 'flag': 'Флаг размещения', 'border': 'Величина отступа вокруг компонента', 'foregroundColor': 'Цвет текста', 'backgroundColor': 'Цвет фона', 'show': 'Признак видимости', 'enable': 'Вкл./Выкл. объект', 'onInit': 'Обработчик инициализации объекта', 'keyDown': 'Обработчик нажатия кнопки клавиатуры'}}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': None, 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': ('centred', 'middle'), 'size': (50, 25), 'moveAfterInTabOrder': '', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': 'Подождите...', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': 'HeadCell', 'init_expr': "_dict_obj['AnaliticTreeList']._indicator = self", 'shortHelpString': '', '_uuid': 'cc70607336bd40dae835e72f950ca17c', 'style': 0, 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'mouseClick': 'WrapperObj.mouseClickFuncTableBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': 'Подробнее', 'source': 'WrapperObj.sourceFuncdefault_1050(evt)', 'mouseDown': None, 'backgroundColor': None, 'type': 'Button', '_uuid': '08995cf3a88278956614895f265b5270', 'moveAfterInTabOrder': '', 'flag': 0, 'recount': None, 'name': 'tableBtn', 'mouseUp': None, 'keyDown': '', 'alias': None, 'init_expr': None, 'position': wx.Point(3, 0), 'onInit': None, 'refresh': None, 'mouseContextDown': '', '__item_id': 8}], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': 'MsgCtrl', 'borderBottomColor': None, 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 333), 'borderStyle': None, 'onInit': None, '__item_id': 7}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1), '__item_id': 5}], 'name': 'treePanel', 'keyDown': None, 'alias': None, 'init_expr': '', 'position': wx.Point(0, 0), 'onInit': None, '__item_id': 2, '__attr_types__': {12: ['init_expr', 'show', 'pre_init_expr', 'refresh', 'description', 'source', 'recount', 'keyDown', 'onClose'], 0: ['name', 'docstr', 'alias', 'data_name', 'label', 'moveAfterInTabOrder', 'field_name', 'type'], 8: ['foregroundColor', 'backgroundColor'], 2: ['enable', 'activate'], 9: ['font'], 10: ['position', 'span'], 11: ['size'], 7: ['flag', 'style'], 40: ['border', 'proportion'], 1: ['layout', 'alignment'], 17: ['res_module', '_uuid', 'obj_module']}, '__default_page__': 1, '__events__': {'onClose': ('wx.EVT_CLOSE', 'ObjDestroy', False), 'onLeftMouseClick': ('wx.EVT_LEFT_DOWN', 'OnLeftDown', False), 'onRightMouseClick': ('wx.EVT_RIGHT_DOWN', 'OnRightDown', False), 'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False), 'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False)}, 'enable': True, '__version__icwidget': '0.0.0.0', '__lists__': {'layout': ['vertical', 'horizontal'], 'alignment': ["('left', 'middle')", "('left', 'top')", "('left', 'bottom')", "('centred', 'middle')", "('centred', 'top')", "('centred', 'bottom')", "('right', 'middle')", "('right', 'top')", "('right', 'bottom')"]}, 'component_module': None, 'res_module': None, 'obj_module': None, 'description': None, 'data_name': None, '__styles__': None, '__interface__': None, '__brief_attrs__': [], '__doc__': None, '__version__base': '0.0.0.0', '__version__': '0.0.0.0', '__init_res_by_wizard__': None, '__attr_hlp__': {'name': 'Имя объекта', 'type': 'Тип объекта', 'activate': 'Вкл./Выкл. создание объекта', 'data_name': 'Имя данных из контекста', 'description': 'Описание', 'style': 'Стиль компонента', 'init_expr': 'Выражение, выполняемой при инициализации компонента', 'component_module': 'Модуль компонента', 'res_module': 'Модуль ресурса', 'obj_module': 'Модуль объекта', 'size': 'Размер объекта', 'position': 'Позиция', 'span': 'Определяет сколько ячеек по горизонтали и вертикали должен занимать компонент', 'proportion': 'Признак пропорционального размера', 'flag': 'Флаг размещения', 'border': 'Величина отступа вокруг компонента', 'foregroundColor': 'Цвет текста', 'backgroundColor': 'Цвет фона', 'show': 'Признак видимости', 'enable': 'Вкл./Выкл. объект', 'onInit': 'Обработчик инициализации объекта', 'keyDown': 'Обработчик нажатия кнопки клавиатуры'}}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1), '__item_id': 1}], 'setFocus': '', 'name': 'TableDialog', 'keyDown': 'WrapperObj.keyDownFuncDialog_1386(evt)', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': '', '__item_id': 0}

#   Version
__version__ = (1, 1, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IAnaliticTree'


def GetStatePlanFunc(treelist, row, level):
    """
    """
    try:
        if row[2] < 0:
            return 1
#        elif row[2] > 10000:
#            return 2
    except:
        pass
    
    return 0


class IAnaliticTree:
    """
    Интерфейс к панели, которая представляет таблицы в виде дерева в разрезе
    аналитических полей.
    """
    
    def __init__(self, parent, codfield=None, fields=None,
                filterExpr=None, labels=None, titleRoot=None, tableName=None):
        """
        Конструктор интерфейса.
        
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type codfield: C{list}
        @param codfield: Описание структуры дерева.
        @type fields: C{list}
        @param fields: Список дополнительных отображаемых полей.
        @type filterExpr: C{string}
        @param filterExpr: Выражение фильтрации.
        @type labels: C{list}
        @param labels: Список заголовков колонок.
        @param tableName: Имя таблицы.
        """
        self.evalSpace = util.InitEvalSpace()
        self.evalSpace['WrapperObj'] = self
        # self.evalSpace['AND'] = AND
        self._res = copy.deepcopy(resource)
        
        #   Указатель на функцию, отрабатывающую после нажати кнопки <подробнее>
        self._linkFunction = None
        #   Временной период
        self.period = None
        
        #   Переопределяемые атрибуты ресурса
        self.codfield = codfield
        self.fields = fields
        self.filterExpr = filterExpr
        self.labels = labels
        self.titleRoot = titleRoot
        res = self.getAnaliticTreeListRes()
        
        #   Переопределяем атрибуты ресурса
        if res and self.codfield is not None:
            res['codfield'] = self.codfield
        if res and self.fields is not None:
            res['fields'] = self.fields
        if res and self.filterExpr is not None:
            res['filterExpr'] = self.filterExpr
        if res and self.labels is not None:
            res['labels'] = self.labels
        if res and self.titleRoot is not None:
            res['titleRoot'] = self.titleRoot
            
        link_res = self.getDataLinkRes()
        if link_res and tableName:
            link_res['res_query'] = tableName
            link_res['file'] = tableName + '.tab'
        
        self.__obj = prs.icBuildObject(parent, self._res, evalSpace=self.evalSpace, bIndicator=True)
        self.object = self.evalSpace['_root_obj']
        
    def getAnaliticTreeListRes(self):
        """
        """
        return self._res['child'][0]['child'][0]['child'][1]['child'][0]
    
    def getDataLinkRes(self):
        """
        Возвращает ресурсы ссылки на источник данных.
        """
        return self._res['child'][0]['child'][0]['child'][0]['child'][0]
        
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
        
    def OnInit(self, evt):
        """
        Обработка сообщения OnInit. В данной форме это сообщение генерится
        компонентом <TableTreeList> после 0.1 сек (время необходимо на отрисовку
        формы после создания).
        """
        obj = self.GetNameObj('AnaliticTreeList')
        
        if obj and not obj.timer:
            # def func(row, level):
            #     try:
            #         if row[2] < 0:
            #             return 1
            #         elif row[2] > 10000:
            #             return 2
            #     except:
            #         pass
            #
            #     return 0
            
            msg_obj = self.GetNameObj('MsgCtrl')
            msg_obj.SetLabel('Подготовка справочников...')
            msg_obj.DirectRefresh()
            self.PrepareSpravBuff()
            
            msg_obj.SetLabel('Загружаем данные...')
            msg_obj.DirectRefresh()
            obj.SetStateFunction(GetStatePlanFunc)
            obj.LoadTableTree(obj.root)
            msg_obj.SetLabel('')

    ###BEGIN EVENT BLOCK
    def mouseClickFuncTableBtn(self, evt):
        """
        Функция обрабатывает событие <EVT_CLICK>.
        """
        evt.Skip()
        # dlg = IAnaliticTable.IAnaliticTable(self.GetNameObj('MsgCtrl'))
        tree = self.GetNameObj('AnaliticTreeList')
        
        item = tree.GetSelection()
        row = tree.GetPyData(item)
        # print '---->>> row=', row
        
        #   Вызываем внешнюю функцию
        if self._linkFunction and self.period:
            result = self._linkFunction(self)
        
        # dlg.ShowModal()
        # dlg.Destroy()
        return None
    
    def activatedFuncAnaliticTreeList(self, evt):
        """
        Функция обрабатывает событие <?>.
        """
        self.mouseClickFuncTableBtn(evt)
    ###END EVENT BLOCK
    
    def PrepareSpravBuff(self):
        """
        Подготавливавем буфер справочников
        """
        obj = self.GetNameObj('AnaliticTreeList')
        
        if obj and obj.codfield:
            import NSI.spravfunc as spravfunc
            buff = {}
            
            for st in obj.codfield:
                fld, sl, spr = st
                
                if spr:
                    nm, fld = spr
                    dct = spravfunc.getReplDict(nm, 'cod', fld)
                    buff[nm] = dct
                    
            if buff:
                obj.SetSpravBuff(buff)
                return True
                
        return False
        
    def SetLinkFunction(self, func):
        """
        Устанавливаем функцию, которая отрабатывает по нажатию кнопки <Подробнее>
        """
        self._linkFunction = func

    def SetStateFunction(self, func):
        """
        Устанавливает функцию определения состояния каждого узла дерева. Данная
        функция должна возвращать идентификатор текущего состояния элемента дерева
        Возможные состояния:
            ictabletreelist.ROW_STATE_NORMAL
            ictabletreelist.ROW_STATE_RED
            ictabletreelist.ROW_STATE_YELLOW
        """
        obj = self.GetNameObj('AnaliticTreeList')
        obj.SetStateFunction(func)


def test(par=0):
    """
    Тестируем класс new_form.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = IAnaliticTree(frame)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
