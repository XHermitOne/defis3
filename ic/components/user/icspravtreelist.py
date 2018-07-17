#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Иерархический справочник.
Класс пользовательского визуального компонента.

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
from ic.dlg import ic_dlg

from ic.kernel import io_prnt

import wx.gizmos as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'SpravTreeList'

#   Описание стилей компонента
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
ic_class_spc = {'type': 'SpravTreeList',
                'name': 'default',
                'style': wx.TR_DEFAULT_STYLE,

                'fields': [],
                'labels': ['col1'],
                'mask': '',
                'codfield': 'cod',
                'typeSprav': '',
                'selected': None,
                'activated': None,
                'titleRoot': '',
                'wcols': [],

                '__styles__': ic_class_styles,
                '__events__': {'selected': ('wx.EVT_TREE_SEL_CHANGED', 'OnSelected', False),
                               'activated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'OnActivated', False),
                               'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDWN', False),
                               },
                '__attr_types__': {0: ['typeSprav', 'name', 'type', 'mask', 'codfield', 'titleRoot'],
                                   20: ['fields', 'labels', 'wcols'],
                                   12: ['selected', 'activated'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeListCtrl'
ic_class_pic2 = '@common.imgEdtTreeListCtrl'

#   Путь до файла документации
ic_class_doc = 'ic.components.user.icspravtreelist.SpravTreeList-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 4)


class SpravTreeList(icwidget.icWidget, parentModule.TreeListCtrl):
    """
    Класс представления структурного справочника в виде дерева.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{name='default'}:
        - B{labels=[]}: Список заголовков колонок.
        - B{wcols=[]}: Список размеров колонок. C{Пример:[100,20]}.
        - B{fields=[]}: Список дополнительных отображаемых полей. C{Пример: ['n1']}.
        - B{mask=''}: Значение кода корневого элемента справочника.
        - B{codfield='cod'}: Имя поля, содержащего иерархический код.
        - B{typeSprav=''}: Тип справочника.
        - B{titleRoot=''}: Заголовок корневого элемента.
        - B{selected=None}: Выражение после выбора элемента.
        - B{activated=None}: Выражение после выбора элемента по <Enter> или двойному щелчку
            мыши.
        - B{type='SpravTreeList'}:
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
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.TreeListCtrl.__init__(self, self.parent, id, self.position, self.size,
                                           style=self.style)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = fldridx = il.Add(common.imgFolder)
        self.fldropenidx = fldropenidx = il.Add(common.imgFolderOpen)
        self.fileidx = fileidx = il.Add(common.imgBlank)
        self.smileidx = smileidx = il.Add(common.imgPage)

        self.SetImageList(il)
        self.il = il
        
        #   Словарь связывает структурный код и узел дерева
        self._codItemDict = {}
        
        # create some columns
        if not self.fields:
            self.fields = ['name']
            
        #   Читаем сохраненные настройки пользователя
        wcols = self.LoadUserProperty('wcols')
        if wcols:
            self.wcols = wcols
            
        self.SetMainColumn(0)   # the one with the tree in it...
        
        for indx, label in enumerate(self.labels):
            self.AddColumn(label)
            
            if len(self.wcols) > indx:
                self.SetColumnWidth(indx, self.wcols[indx])

        self.root = self.AddRoot(self.getTitleRoot())
        self.SetItemImage(self.root, fldridx, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, fldropenidx, which=wx.TreeItemIcon_Expanded)

        if not self.source:
            for x in range(15):
                txt = 'Item %d' % x
                child = self.AppendItem(self.root, txt)
                self.SetItemText(child, txt + '(c1)', 1)
                self.SetItemImage(child, fldridx, which=wx.TreeItemIcon_Normal)
                self.SetItemImage(child, fldropenidx, which=wx.TreeItemIcon_Expanded)
    
                for y in range(5):
                    txt = 'item %d-%s' % (x, chr(ord('a')+y))
                    last = self.AppendItem(child, txt)
                    self.SetItemText(last, txt + '(c1)', 1)
                    self.SetItemText(last, txt + '(c2)', 2)
                    self.SetItemImage(last, fileidx, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(last, smileidx, which=wx.TreeItemIcon_Selected)
        else:
            self.LoadSpravTree(self.root)
            
        self.Expand(self.root)
        
        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelected)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDWN)

        self.BindICEvt()

    def RefreshSpravTree(self):
        """
        Обновление дерева справочника.
        """
        if self.root:
            self.DeleteChildren(self.root)
            self.LoadSpravTree(self.root)
            self.Expand(self.root)
            return True
        return False

    def getTitleRoot(self):
        """
        Текст корневого элемента.
        """
        return self.getICAttr('titleRoot')
        
    def getTypeSprav(self):
        """
        Тип справочника.
        """
        return self.getICAttr('typeSprav')
        
    def ObjDestroy(self):
        """
        Функция уничтожения компонента.
        """
        #   Сохраняем размеры колонок грида
        wcols = []
        for indx, label in enumerate(self.labels):
            try:
                w = self.GetColumnWidth(indx)
                wcols.append(w)
            except: pass

        self.SaveUserProperty('wcols', wcols)
        
    def AddCodItem(self, parent_item, cod_mask, level, levelLenList, rows_dict):
        """
        Добавляет в определенный узел дочерние элементы, которые определяются
        по маске кода.
        
        @type parent_item: C{wx.CtrlTreeItem}
        @param parent_item: Узел, куда добавляются дочерние элементы.
        @type cod_mask: C{string}
        @param cod_mask: Маска кода справочника, по которой определяются дочерние
            элементы.
        @type level: C{int}
        @param level: Номер уровня кода родительского элемента.
        @type levelLenList: C{list}
        @param levelLenList: Список размеров уровней. Индекс списка соответствует номеру
            уровня кода.
        @type rows_dict: C{dictionary}
        @param rows_dict: Словарь записей из справочника. В качестве ключей размеры кодов,
            в качестве значений список записей с данным размером кода.
        @rtype: C{bool}
        @return: Признак того, что в узел добавлены дочерние элементы.
        """
        if level >= len(levelLenList):
            return False
        
        bret = False
        cod_level = levelLenList[level]
        
        for row in rows_dict[cod_level]:
            cod = row[0]
            name = row[1]
            if not cod_mask or cod.find(cod_mask) == 0:
                bret = True
                child = self.AppendItem(parent_item, name)
                self.SetPyData(child, row)
                self._codItemDict[cod] = child
                
                for indx in range(2, len(row)):
                    self.SetItemText(child, str(row[indx]), indx-1)
                
                if self.AddCodItem(child, cod, level+1, levelLenList, rows_dict):
                    self.SetItemImage(child, self.fldridx, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
                else:
                    self.SetItemImage(child, self.fileidx, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child, self.smileidx, which=wx.TreeItemIcon_Selected)
        return bret

    def LoadSpravTree(self, root):
        """
        Создает дерево со структрурой заданного иерархического справочника.
        """
        if not self.getTypeSprav():
            ic_dlg.icWarningBox(u'ОШИБКА', u'Не указан тип справочника <typeSprav>')
            return False
        
        #   Получаем ссылку на класс данных
        cl = self.dataset.dataclass
        rs = cl.select(cl.q.type == self.getTypeSprav())
        
        rows_dict = {}
        
        #   Буфферизируем справочник - раскидываем по разным уровням кода
        for r in rs:
            cod = getattr(r, self.codfield)
            row_buff = range(len(self.fields) + 1)
            row_buff[0] = cod
            
            #   Читаем значения дополнительных полей
            for i, fld in enumerate(self.fields):
                row_buff[i + 1] = getattr(r, fld)
        
            cod_len = len(cod)
            
            if cod_len > 0:
                if cod_len in rows_dict:
                    rows_dict[cod_len].append(row_buff)
                else:
                    rows_dict[cod_len] = [row_buff]
        
        #   Сортируем по размеру кода
        keyList = rows_dict.keys()
        keyList.sort()
        
        #   Заполняем дерево
        self.AddCodItem(self.root, self.mask, 0, keyList, rows_dict)
    
    def SelectItemByCod(self, cod):
        """
        Выбирает элемент дерева по структурному коду.
        
        @type cod: C{string}
        @param cod: Структурный код.
        @rtype: C{bool}
        @return: Возвращает признак успешного выполнения.
        """
        if cod in self._codItemDict:
            item = self._codItemDict[cod]
            self.EnsureVisible(item)
            self.SelectItem(item)
            return True
            
        return False

    def getSelectionRow(self):
        """
        Вернуть запись выбранного элемента.
        """
        selection_item = self.GetSelection()
        row = self.GetPyData(selection_item)
        return row
    
    def setItemRow(self, Item_, Row_):
        """
        Установить запись элемента.
        """
        self.SetPyData(Item_, Row_)
        
    def setSelectionRow(self, Row_):
        """
        Установить запись выбранного элемента.
        """
        selection_item = self.GetSelection()
        self.setItemRow(selection_item, Row_)
        
    def getSelectionCod(self):
        """
        Вернуть код выбранного элемента.
        """
        selection_item = self.GetSelection()
        row = self.GetPyData(selection_item)
        if row is None:
            return None
        return row[0]

    def getDataTab(self, CurItem_=None):
        """
        Получить таблицу записей всех элементов.
        @param CurItem_: Текущий обработываемый узел дерева.
            Если None, то корневой элемент.
        @return: Список записей дочерних элементов или None в случае ошибки.
        """
        try:
            table = []
            # Определение текущего элемента дерева.
            if CurItem_ is None:
                CurItem_ = self.GetRootItem()
            # Если есть дочерние элементы у узла
            if self.ItemHasChildren(CurItem_):
                # Перебор всех дочерних элементов
                child, cookie = self.GetFirstChild(CurItem_)
                if child.IsOk():
                    row = self.GetPyData(child)
                    table.append(row)
                    # Если дочерний элемент имеет подъэлементы,
                    # то обработать его
                    if self.ItemHasChildren(child):
                        table += self.getDataTab(child)
                while 1:
                    child, cookie = self.GetNextChild(CurItem_, cookie)
                    if child.IsOk():
                        row = self.GetPyData(child)
                        table.append(row)
                        # Если дочерний элемент имеет подъэлементы,
                        # то обработать его
                        if self.ItemHasChildren(child):
                            table += self.getDataTab(child)
                    else:
                        break

            return table
        except:
            io_prnt.outErr(u'Ошибка определения таблицы записей справочника %s' % self.getTypeSprav())
            return None
        
    def OnSelected(self, evt):
        """
        Обработчик события wx.EVT_TREE_SEL_CHANGED, атрибут=selected
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('selected')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnActivated(self, evt):
        """
        Обработчик события wx.EVT_TREE_ITEM_ACTIVATED, атрибут=activated
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('activated')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnKeyDWN(self, evt):
        """
        Обработчик события wx.EVT_KEY_DOWN, атрибут=keyDown
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('keyDown')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    ctrl = SpravTreeList(win, -1, {'position': (0, 0), 'size': (300, 300),
                                   'labels': ['tree', 'par1']})
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
