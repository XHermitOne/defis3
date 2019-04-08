#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import copy
#from sqlobject import AND
import ic.components.user.ictabletreelist as ictabletreelist

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877120, 'foregroundColor': None, 'span': (1, 1), 'title': u'', 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'onClose': u'', '_uuid': u'0ccd9321b4dadadd2d428fab5327ef57', 'moveAfterInTabOrder': u'', 'killFocus': u'', 'flag': 0, 'child': [{'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'name': u'DefaultName_1467', 'position': (0, 0), 'type': u'BoxSizer', '_uuid': u'cfcbda6926a8a94afd6cb1a6b33c7770', 'proportion': 1, 'alias': None, 'flag': 8192, 'init_expr': None, 'child': [{'activate': 1, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'onRightMouseClick': None, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 1, 'source': None, 'onLeftMouseClick': None, 'backgroundColor': None, 'type': u'Panel', 'onClose': u'', '_uuid': u'c1c7a0cd0b55fbc5aa9973151c411928', 'style': 524288, 'docstr': u'ic.components.icwxpanel-module.html', 'flag': 8192, 'child': [{'style': 0, 'activate': 1, 'prim': u'', 'name': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0445', '_uuid': u'021e5c865e1872481b37388b13643dbc', 'alias': None, 'init_expr': None, 'child': [{'activate': 1, 'name': u'Table', '_uuid': u'3f569e1d1a7d12722275519ea5863610', 'docstr': u'ic.db.icdataset-module.html', 'filter': u'WrapperObj.filterFuncTable(evt)', 'alias': None, 'res_query': u'analitic', 'init_expr': None, 'file': u'analitic.tab', 'type': u'DataLink', 'link_expr': None}], 'type': u'Group'}, {'hgap': 0, 'style': 0, 'activate': 1, 'layout': u'vertical', 'description': None, 'position': (0, 0), 'component_module': None, 'type': u'BoxSizer', '_uuid': u'd150e8c27a77f8d4add04024891528d9', 'proportion': 0, 'name': u'BSZR', 'alias': None, 'flag': 0, 'init_expr': None, 'child': [{'orderBy': u'', 'activate': 1, 'show': 1, 'labels': [u'\u0410\u043d\u0430\u043b\u0438\u0442\u0438\u043a\u0430', u'\u0421\u0443\u043c\u043c\u0430', u'\u041f\u043b\u0430\u043d'], 'activated': u'WrapperObj.activatedFuncAnaliticTreeList(evt)', 'refresh': None, 'border': 0, 'init_sprav_buff': u'', 'size': wx.Size(341, 378), 'style': 8201, 'foregroundColor': None, 'span': (1, 1), 'selected': None, 'proportion': 1, 'source': u'Table', 'backgroundColor': None, 'codfield': [(u'dtoper', (0, 10), None), (u'reg', (0, 4), (u'Region', u'name')), (u'mens', (1, 4), (u'Menager', u'name')), (u'codt', (0, 3), (u'Product', u'name'))], 'titleRoot': u'\u0420\u0435\u0433\u0438\u043e\u043d\u044b', 'type': u'TableTreeList', 'filterExpr': u"_Table.q.dtoper.startswith('2005.03.11')", '_uuid': u'c97a43b850d08752bd78a9c911ba9393', 'moveAfterInTabOrder': u'', 'flag': 8192, 'recount': None, 'name': u'AnaliticTreeList', 'wcols': [200], 'fields': [u'summa', u'plan_sum'], 'keyDown': None, 'alias': None, 'init_expr': u'', 'position': (-1, -1), 'onInit': u'WrapperObj.OnInit(evt)'}, {'activate': 1, 'show': 1, 'borderRightColor': None, 'recount': None, 'keyDown': None, 'borderTopColor': None, 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (50, 25), 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435...', 'source': None, 'backgroundColor': None, 'isSort': False, 'type': u'HeadCell', 'init_expr': u"_dict_obj['AnaliticTreeList']._indicator = self", 'shortHelpString': u'', '_uuid': u'cc70607336bd40dae835e72f950ca17c', 'style': 0, 'flag': 8192, 'child': [{'activate': 1, 'show': 1, 'mouseClick': u'WrapperObj.mouseClickFuncTableBtn(evt)', 'font': {}, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'proportion': 0, 'label': u'\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435', 'source': u'WrapperObj.sourceFuncdefault_1050(evt)', 'mouseDown': None, 'backgroundColor': None, 'type': u'Button', '_uuid': u'08995cf3a88278956614895f265b5270', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': None, 'name': u'tableBtn', 'mouseUp': None, 'keyDown': u'', 'alias': None, 'init_expr': None, 'position': wx.Point(3, 0), 'onInit': None, 'refresh': None, 'mouseContextDown': u''}], 'cursorColor': (100, 100, 100), 'backgroundType': 0, 'borderStep': 0, 'borderLeftColor': None, 'name': u'MsgCtrl', 'borderBottomColor': None, 'refresh': None, 'alias': None, 'borderWidth': 1, 'position': wx.Point(0, 333), 'borderStyle': None, 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'name': u'treePanel', 'keyDown': None, 'alias': None, 'init_expr': u'', 'position': wx.Point(0, 0), 'onInit': None}], 'span': (1, 1), 'border': 0, 'vgap': 0, 'size': (-1, -1)}], 'setFocus': u'', 'name': u'TableDialog', 'keyDown': u'WrapperObj.keyDownFuncDialog_1386(evt)', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': u''}

#   Версия объекта
__version__ = (1, 0, 2, 6)
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
        self.evalSpace['AND'] = AND
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
        if res and self.codfield <> None:
            res['codfield'] = self.codfield
        if res and self.fields <> None:
            res['fields'] = self.fields
        if res and self.filterExpr <> None:
            res['filterExpr'] = self.filterExpr
        if res and self.labels <> None:
            res['labels'] = self.labels
        if res and self.titleRoot <> None:
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
#            def func(row, level):
#                try:
#                    if row[2] < 0:
#                        return 1
#                    elif row[2] > 10000:
#                        return 2
#                except:
#                    pass
#
#                return 0
            
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
        #dlg = IAnaliticTable.IAnaliticTable(self.GetNameObj('MsgCtrl'))
        tree = self.GetNameObj('AnaliticTreeList')
        
        item = tree.GetSelection()
        row = tree.GetPyData(item)
        #print '---->>> row=', row
        
        #   Вызываем внешнюю функцию
        if self._linkFunction and self.period:
            result = self._linkFunction(self)
        
        #dlg.ShowModal()
        #dlg.Destroy()
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