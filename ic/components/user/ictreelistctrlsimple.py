#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского визуального компонента.
Компонент древовидного представления данных.
Работает с простой словарно-списковой структурой:
{
'name1':{'child1':{...},
    'child2':{...},
    ...,
    '__record__':Данные, прикреплямые к узлу  в виде списка.
    },
...                
}

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.log import ic_log
import wx.gizmos as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTreeListCtrlSimple'

# --- Описание стилей компонента ---
ic_class_styles = {'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
                   'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
                   'TR_NO_LINES': wx.TR_NO_LINES,
                   'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
                   'TR_SINGLE': wx.TR_SINGLE,
                   'TR_MULTIPLE': wx.TR_MULTIPLE,
                   'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS,
                   }

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'TreeListCtrlSimple',
                'name': 'default',

                'titleRoot': 'root',
                'treeDict': {},
                'labels': ['col1'],
                'wcols': [],

                'itemCollapsed': None,
                'itemExpanded': None,
                'selectChanged': None,
                'itemActivated': None,

                '__styles__': ic_class_styles,
                '__events__': {'itemCollapsed': ('wx.EVT_TREE_ITEM_COLLAPSED', 'OnItemCollapsed', False),
                               'itemExpanded': ('wx.EVT_TREE_ITEM_EXPANDED', 'OnItemExpanded', False),
                               'selectChanged': ('wx.EVT_TREE_SEL_CHANGED', 'OnSelectChanged', False),
                               'itemActivated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'OnItemActivated', False),
                               },
                '__attr_types__': {0: ['name', 'type', 'titleRoot'],
                                   icDefInf.EDT_TEXTDICT: ['treeDict'],
                                   icDefInf.EDT_TEXTLIST: ['labels', 'wcols'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeListCtrl'
ic_class_pic2 = '@common.imgEdtTreeListCtrl'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icTreeListCtrlSimple(icwidget.icWidget, parentModule.TreeListCtrl):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='TreeList'}:
        - B{name='default'}:
        - B{titleRoot='root'}: Подписть корневого элемента.
        - B{spravDict={}}: список словарей преобразований имен ключей в имена дерева;
            на каждый уровень вложенности может быть свой словарь.
        - B{treeDict={}}: Словарно-списковая структура, отображаемая в дереве.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        parentModule.TreeListCtrl.__init__(self, parent, id, self.position, self.size,
                                           style=self.style)
        
        # Последний выбранный элемент дерева
        self._last_selection = None

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = fldridx = il.Add(common.imgFolder)
        self.fldropenidx = fldropenidx = il.Add(common.imgFolderOpen)
        self.fileidx = fileidx = il.Add(common.imgBlank)
        self.curidx = curidx = il.Add(common.imgPage)
        self.AssignImageList(il)
        
        # Установки колонок
        self.SetMainColumn(0)   # the one with the tree in it...
        
        for indx, label in enumerate(self.labels):
            self.AddColumn(label)
            
            if len(self.wcols) > indx:
                self.SetColumnWidth(indx, self.wcols[indx])
                
        #   Определяем корень
        self.root = self.AddRoot(self.getTitleRoot())
        self.SetItemImage(self.root, fldridx, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, fldropenidx, which=wx.TreeItemIcon_Expanded)

        self.LoadTree()

        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        self.BindICEvt()

    def getTitleRoot(self):
        """
        Имя самого главного узла.
        @return: Возвращает всегда строку.
        """
        return str(self.getICAttr('titleRoot'))
        
    def getSelectionName(self):
        """
        Имя выбранного узла.
        """
        selection_item = self.GetSelection()
        return self.GetItemText(selection_item)
    
    def _addChildList(self, root, res, level=0, start_level=0):
        """
        Добавить дочерние узлы, описанные списком.
        """
        for indx, el in enumerate(res):
            id_pic, id_exp_pic = self._getPicturesId(el)
            
            nm = self.getElementName(el, indx)
            child = self.AppendItem(root, nm, id_pic)
            self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
            self.SetPyData(child, (level+start_level, el))

            self.addBranch(child, el, level+1, start_level)
        
    def _addChildDict(self, root, res, level=0, start_level=0):
        """
        Добавить дочерние узлы, описанные словарем.
        """
        lst = res.keys()
        lst.sort()
        for key in lst:
            el = res[key]
            id_pic, id_exp_pic = self._getPicturesId(el)
            # Если элемент __record__, то установить список данных на узле.
            if key != '__record__':
                try:
                    nm = lst[level][key]
                except:
                    nm = str(key)

                child = self.AppendItem(root, nm, id_pic)
                self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
                self.SetPyData(child, (level+start_level, el))
                
                self.addBranch(child, el, level+1, start_level)
            else:
                # Установить запись для узла
                self.setItemRecord(root, el)
            
    def addBranch(self, root, res, level=0, start_level=0):
        """
        Добавляет ветку в дерево.
        """
        if level > 1:
            return root
            
        #   Если структура в интерфейсе списка
        if self.isList(res):
            self._addChildList(root, res, level, start_level)
        #   Если структура в интерфейсе словаря
        elif self.isDict(res):
            self._addChildDict(root, res, level, start_level)
        else:
            id_pic, id_exp_pic = (self.fileidx, self.curidx)
            
            child = self.AppendItem(root, str(res), id_pic)
            self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
            self.SetPyData(child, (level+start_level, res))
            
        return root

    def _isChildrenRes(self, Res_):
        """
        Есть ли в описании ресурса описание дочерних элементов?
        @param Res_: Ресурс.
        @return: Возвращает True/False.
        """
        if self.isList(Res_):
            return bool(Res_)
        elif self.isDict(Res_):
            return bool([key for key in Res_.keys() if key != '__record__'])
        else:
            return True
        return False
        
    def _getPicturesId(self, Res_):
        """
        Определение картинок для изобращения узла по ресурсу этого узла.
        @param Res_: Ресурс узла.
        @return: Кортеж из 2-х элементов - идентификаторов картинок.
        """
        # Если нет дочерних элементов в описании, тогда картинки-файлы
        if not self._isChildrenRes(Res_):
            return self.fileidx, self.curidx
        return self.fldridx, self.fldropenidx
    
    def setItemRecord(self, Item_, Record_):
        """
        Установить список записи на узле.
        @param Item_: ID узла у которого устанавливается запись.
        @param Record_: Запись узла. Список.
        """
        if Record_ and self.isList(Record_):
            for idx, value in enumerate(Record_[1:]):
                self.SetItemText(Item_, str(value), idx+1)
        return Item_
        
    def getItemRecord(self, Item_):
        """
        Список записи на узле.
        @param Item_: ID узла у которого устанавливается запись.
        @return: Возвращает список строк записи узла. 
            Или None в случае ошибки.
        """
        try:
            res = self.GetPyData(Item_)[1]
            if isinstance(res, dict) and '__record__' in res:
                return res['__record__']
            return None
        except:
            ic_log.icLogErr(u'ОШИБКА компонента %s метода getItemRecord' % self.name)
            return None

    def getSelectionRecord(self):
        """
        Список записи выбранного узла.
        @return: Возвращает список строк записи узла. 
            Или None в случае ошибки.
        """
        selection_item = self.GetSelection()
        return self.getItemRecord(selection_item)
        
    def setLabelCols(self, LabelCols_):
        """
        Установить надписи колонок.
        @param LabelCols_: Надписи колонок. Список строк.
        @return: Возвращает результат выполнения функции True/False.
        """
        try:
            col_count = self.GetColumnCount()
            for i_col, col_label in enumerate(LabelCols_):
                if i_col < col_count:
                    self.SetColumnText(i_col, col_label)
                else:
                    break
            return True
        except:
            ic_log.icLogErr(u'ОШИБКА компонента %s метода setLabelCols' % self.name)
            return False
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
                                
    def getElementName(self, res, indx):
        """
        Возвращает имя элемента списка.
        """
        return 'element %s:' % str(indx)
        
    def isDict(self, res):
        """
        Признак словарного интерфейса.
        """
        return isinstance(res, dict)

    def isList(self, res):
        """
        Признак интерфейса последовательности.
        """
        return isinstance(res, list)
        
    def LoadTree(self, treeDict=None, AutoSelect_=True, AutoExpand_=True):
        """
        Заполняем дерево.
        
        @type treeDict: C{dictionary}
        @param treeDict: Словарно-списковая структура, отображаемая в дереве.
        @type AutoSelect_: C{bool}
        @param AutoSelect_: Автоматически выбрать последний элемент.
        @type AutoExpand_: C{bool}
        @param AutoExpand_: Автоматически развернуть корневой элемент.
        """
        if treeDict is None:
            treeDict = self.treeDict
        else:
            self.treeDict = treeDict
        
        self.SetPyData(self.root, (-1, treeDict))
        self.DeleteChildren(self.root)
        
        if treeDict is not None:
            self.addBranch(self.root, treeDict)
        else:
            self._testTree()
            
        # Авторазворачивание верхнего уровня
        if AutoExpand_:
            self.Expand(self.root)
            
        # Автовыбор элемента
        if AutoSelect_:
            if self._last_selection:
                self.selectItemPath(self._last_selection)
            else:
                self.SelectItem(self.root)

    def selectItemPath(self, ItemPath_, CurItem_=None):
        """
        Выбрать элемент по пути.
        @param ItemPath_: Путь до элемента.
        @param CurItem_: Текущий элемент поиска. 
            Если None, то поиск начиниется с корня.
        """
        if CurItem_ is None:
            CurItem_ = self.root
        if ItemPath_:
            cur_item = self.FindItem(CurItem_, ItemPath_[0])
            # Есть дочерние элементы
            if ItemPath_[1:]:
                self.Expand(cur_item)
            return self.selectItemPath(ItemPath_[1:], cur_item)
        return self.SelectItem(CurItem_)
        
    def getItemPath(self, Item_, Path_=None):
        """
        Путь до элемента. Путь - список имен элементов.
        @param Item_: Элемент дерева.
        @param Path_: Текущий заполненный путь.
        """
        parent = self.GetItemParent(Item_)
        # Если есть родительский элемент, то вызвать рекурсивно
        if parent:
            if Path_ is None:
                Path_ = []
            Path_.insert(-1, self.GetItemText(Item_))
            return self.getItemPath(parent, Path_)
        return Path_
        
    def reFresh(self):
        """
        Обновление дерева.
        """
        return self.LoadTree(self.GetPyData(self.root)[1])
    
    def getItemChildren(self, Item_=None):
        """
        Список дочерних элементов узла дерева.
        @param Item_: Узел/элемент дерева. Если None, то корневой элемент.
        @return: Список дочерних элементов узла дерева 
            или None в случае ошибки.
        """
        try:
            # Определить узел
            if Item_ is None:
                Item_ = self.root
                
            # Список дочерних элементов
            children = []

            children_count = self.GetChildrenCount(Item_, False)
            for i in range(children_count):
                if i == 0:
                    child, cookie = self.GetFirstChild(Item_)
                else:
                    child, cookie = self.GetNextChild(Item_, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            ic_log.icLogErr(u'ОШИБКА компонента %s метода определения списка дочерних элементов' % self.name)
            return None
        
    def findItemString(self, string, curItem=None, columns=None, bILike=True):
        """
        Функция ищет подстроку в массиве данных. 
    
        @type string: C{string}
        @param string: Строка поиска
        @type curItem: C{int}
        @param curItem: Элемент дерева, с которого начинается поиск.
        @type columns: C{list}
        @param columns: Список колонок записи каждого элемента, по которым ведется поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @return: Возвращает номер элемента дерева, где найдена искомая строка.
        """
        try:
            # Без учета регистра?
            if bILike:
                string = string.upper()

            # Текущий элемент дерева
            if curItem is None:
                curItem = self.root
                
            cur_item_rec = self.getItemRecord(curItem)
            # Колонки
            if columns is None:
                columns = range(len(cur_item_rec))
                
            # Сначала поискать в текущем элементе
            for col in columns:
                if cur_item_rec:
                    # Получить значение поля
                    if bILike:
                        value = str(cur_item_rec[col]).upper()
                    else:
                        value = str(cur_item_rec[col])
                    # Проверка на совпадение подстроки
                    if string in value:
                        return curItem
                
            # Обработка дочерних элементов
            children = self.getItemChildren(curItem)
            if children:
                for child in children:
                    result = self.findItemString(string, child, columns, bILike)
                    if result is not None:
                        # Если нашли в дочерних элементах, то вернуть результат
                        return result

            # Ну если и в дочерних узлах не нашли,
            # то вызвать поиск для следующего элемента
            next = self.GetNextSibling(curItem)
            if next.IsOk():
                return self.findItemString(string, next, columns, bILike)
            
            # Все равно не нашли
            return None
        except:
            ic_log.icLogErr(u'ОШИБКА компонента %s метода поиска узла по строке' % self.name)
            return None
        
    #--- Обработчики событий ---
    def OnItemExpanded(self, event):
        """
        Разворачивание узла.
        """
        root = event.GetItem()
        if self.treeDict:
            level, res = self.GetPyData(root)
            self.DeleteChildren(root)
            
            self.addBranch(root, res, 0, level+1)

        self.evalSpace['evt'] = event
        self.evalSpace['self'] = self
        
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('itemExpanded')
            
        event.Skip()
    
    def OnItemCollapsed(self, event):
        """
        Сворачивание узла.
        """
        self.evalSpace['evt'] = event
        self.evalSpace['self'] = self
        
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('itemCollapsed')
            
        event.Skip()
        
    def OnSelectChanged(self, event):
        """
        Изменение выделенного узла.
        """
        select_item = event.GetItem()
        self._last_selection = None
        if select_item:
            self._last_selection = self.getItemPath(select_item)
            
        self.evalSpace['evt'] = event
        self.evalSpace['self'] = self
        
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('selectChanged')
            
        event.Skip()
        
    def OnItemActivated(self, event):
        """
        Активизация узла.
        """
        self.evalSpace['evt'] = event
        self.evalSpace['self'] = self
        
        if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.eval_attr('itemActivated')
            
        event.Skip()
        
    def _testTree(self):
        """
        """
        for x in range(5):
            txt = 'Item %d' % x
            child = self.AppendItem(self.root, txt)
            self.SetItemText(child, txt + '(c1)')
            self.SetItemImage(child, self.fldridx, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx, which=wx.TreeItemIcon_Expanded)


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    res0 = {'d1': {'__record__': [1, 2, 3, 4]},
            'd2': {'cc1': 'a1', 'cc2': 'a2', '__record__': [1, 2, 3, 4]},
            'd3': {'ee1': 'a1', 'ee2': 'a2', '__record__': [1, 2, 3, 4]},
            '__record__': [1, 2, 3, 4],
            }
    
    res = {'a1': res0,
           'b1': res0,
           'c1': res0,
           'e1': res0,
           '__record__': [1, 2, 3, 4],
           }
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    tree = icTreeListCtrlSimple(win, -1, {'position': (10, 10), 'size': (200, 300),
                                          'style': wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS,
                                          'labels': ['col1', 'col2', 'col3']})

    tree.LoadTree(res)
    
    frame.Show(True)
    app.MainLoop()


def testStorage():
    import ic.storage.storesrc as storesrc
    
    res_path = 'c:/temp/db'
    storage = storesrc.icTreeDirStorage(res_path)
    storage.Open()

    if 'db2005' not in storage:
       storage['db2005'] = storesrc.icDirStorage()
    
    if 'm01' not in storage['db2005']:
       storage['db2005']['m01'] = storesrc.icFileStorage()
    
    ms = storage['db2005']['m01']
    
    for i in range(10):
        a = {}
        for j in range(10):
            a[j] = 'indx i,j=%d.%d' % (i, j)
            print(u'\tms[i][j] = %s' % a[j])
        ms[i] = a
    
    storage.Close()
    storage.Open()
    return storage


if __name__ == '__main__':
    test()
