#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского визуального компонента.
Компонент древовидного представления данных с возможностью множественного выбора элементов.
Работает с простой словарно-списковой структурой:
[
    {
    'name':Имя узла,
    'child':[...], Список словарей дочерних узлов
    '__record__':Данные, прикреплямые к узлу  в виде списка.
    },
    ...
]
"""

import wx
from wx.lib.agw import customtreectrl

import ic.utils.util as util
import ic.PropertyEditor.icDefInf as icDefInf

from . import icsimpletreelistctrl

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMultiCheckTreeListCtrl'

# --- Описание стилей компонента ---
ic_class_styles = icsimpletreelistctrl.ic_class_styles

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'MultiCheckTreeListCtrl',
                'name': 'default',
                'child': [],
                'style': wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT,
                
                'titleRoot': 'root',
                'treeDict': {},
                'labels': ['col1'],
                'wcols': [],
                'hideHeader': False,

                'itemCollapsed': None,
                'itemExpanded': None,
                'selectChanged': None,
                'itemActivated': None,
                'itemChecked': None,
                'keyDown': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type', 'titleRoot'],
                                   icDefInf.EDT_TEXTDICT: ['treeDict'],
                                   icDefInf.EDT_CHECK_BOX: ['hideHeader'],
                                   icDefInf.EDT_TEXTLIST: ['labels', 'wcols'],
                                   },

                '__events__': {'itemCollapsed': ('wx.EVT_TREE_ITEM_COLLAPSED', 'OnItemCollapsed', False),
                               'itemExpanded': ('wx.EVT_TREE_ITEM_EXPANDED', 'OnItemExpanded', False),
                               'selectChanged': ('wx.EVT_TREE_SEL_CHANGED', 'OnSelectChanged', False),
                               'itemActivated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'OnItemActivated', False),
                               'itemChecked': ('castomtree.EVT_TREE_ITEM_CHECKED', 'OnItemChecked', False),
                               'keyDown': ('wx.EVT_TREE_KEY_DOWN', 'OnTreeListKeyDown', False),
                               },
                '__parent__': icsimpletreelistctrl.ic_class_spc,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeCheckCtrl'
ic_class_pic2 = '@common.imgEdtTreeCheckCtrl'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)

# --- Constants ---
GREY_ITEM_TEXT_COLOR = wx.Colour(192, 192, 192)
ITEM_TEXT_COLOR = wx.Colour(0, 0, 0)

# Description of item state:
# 0 - not check and not bold
# 1 - check and bold
# 2 - check and not bold
CHECK_ID = 1
UNCHECK_ID = 0
CHECK_NOBOLD_ID = 2


class icMultiCheckTreeListCtrl(icsimpletreelistctrl.icSimpleTreeListCtrl):
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

        icsimpletreelistctrl.icSimpleTreeListCtrl.__init__(self, parent, 
                                                           id, component, logType, evalSpace)
            
        self.AssignImageList(wx.ImageList(5, 16))

        self.Bind(customtreectrl.EVT_TREE_ITEM_CHECKED, self.MultiCheckTree_itemChecked)

    def addNode(self, root, res, level=0, start_level=0):
        """
        Добавить дочерние узлы, описанные словарем.
        """
        id_pic, id_exp_pic = self._getPicturesId(res)
        st = u'  ' + (unicode(res['__record__'][0]) or '')
        child = self.AppendItem(root, res['name'] + st, ct_type=res.get('__type__', 0))
        self.SetItemImage(child, id_pic, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
        self.SetPyData(child, (level+start_level, res))
        self.setItemRecord(child, res['__record__'])
        
        # Обработка дочерних элементов
        if 'child' in res and res['child']:
            for node in res['child']:
                self.addNode(child, node, level+1, start_level)

    def get_item_cod(self, item, cod=None):
        """
        Возвращает полный код элемента.
        """
        cod = cod or []
        if item != self.GetRootItem():
            lev, res = self.GetPyData(item)
            cod.insert(0, res['name'])
            return self.get_item_cod(item.GetParent(), cod)
        return cod
                
    def get_check_list(self, lst=None, root_item=None):
        """
        Возвращает список картежей с информацией об
        отобранных элементах.
        """
        root = root_item or self.GetRootItem()
        lst = lst or []
        for item in root.GetChildren():
            st = self.get_state(item)
            lev, res = self.GetPyData(item)
            lst.append((res['name'], st, self.get_item_cod(item)))
            self.get_check_list(lst, item)
        return lst

    def get_state(self, item):
        """
        Return item state.
        """
        if self.IsItemChecked(item) and self.IsBold(item):
            return CHECK_ID
        elif self.IsItemChecked(item) and not self.IsBold(item):
            return CHECK_NOBOLD_ID

        return UNCHECK_ID

    def set_state(self, item, state):
        """
        Set Item state.
        """
        flag, bBold = self.get_state_tuple(state)
        self.CheckItem2(item, flag, True)
        self.SetItemBold(item, bBold)

    def get_state_tuple(self, state):
        """
        Return check/uncheck and bold flags.
        """
        if state == CHECK_ID:
            return True, True
        elif state == UNCHECK_ID:
            return False, False
        return True, False

    def set_state_up(self, item, state=1):
        """
        Set flags up.
        """
        if item != self.GetRootItem():
            prnt = item.GetParent()
            if prnt != self.GetRootItem():
                lst = [self.IsItemChecked(el) for el in prnt.GetChildren()]
                lstb = [self.IsBold(el) for el in prnt.GetChildren()]
                if all(lst) and all(lstb):
                    self.set_state(prnt, state)
                    self.set_state_up(prnt, state)
                elif any(lst) or any(lstb):
                    self.set_state(prnt, CHECK_NOBOLD_ID)
                    self.set_state_up(prnt, CHECK_NOBOLD_ID)
                else:
                    self.set_state(prnt, UNCHECK_ID)
                    self.set_state_up(prnt, UNCHECK_ID)

    def set_state_down(self, item, state=1):
        """
        Set flags down.
        """
        self.set_state(item, state)
        for chld in item.GetChildren():
            self.set_state(chld, state)
            if chld.GetChildren():
                self.set_state_down(chld, state)

    def MultiCheckTree_itemChecked(self, evt):
        item = evt.GetItem()
        if item:
            # Disenable child items
            bch = self.IsItemChecked(item)
            self.set_state_down(item, bch)
            self.set_state_up(item, bch)
            
        return icsimpletreelistctrl.icSimpleTreeListCtrl.OnItemChecked(self, evt)


def load_data(tree=None):
    res0 = {'d1': {'__record__': [1, 2, 3, 4]},
            'd2': {'cc1': 'a1', 'cc2': 'a2', '__record__': [1, 2, 3, 4]},
            'd3': {'ee1': 'a1', 'ee2': 'a2', '__record__': [1, 2, 3, 4]},
            '__type__': 1,
            '__record__': [u'Краснодарский край', 3, 4],
            }

    res1 = {'name': '77',
            'child': [],
            '__type__': 1,
            '__record__': [u'Красноярский край', 3, 4],
            }

    res2 = {'name': '19',
            'child': [],
            '__type__': 1,
            '__record__': [u'Республика Хакасия', 3, 4],
            }
    res11 = {'name': '9507',
             'child': [],
             '__type__': 1,
             '__record__': [u'Мытищинский мун.', 3, 4],
             }

    res12 = {'name': '9534',
             'child': [],
             '__type__': 1,
             '__record__': [u'Жуковский мун.', 3, 4],
             }

    res3 = {'name': '95',
            'child': [res11, res12],
            '__type__': 1,
            '__record__': [u'Московская область', 3, 4],
            }

    res = [{'name': 'RU',
            'child': [res1, res2, res3],
            '__type__': 1,
            '__record__': [u'Россия', 3, 4],
            },
           {'name': 'RU1',
            'child': [res1, res2, res3],
            '__type__': 1,
            '__record__': [u'Россия', 3, 4],
            }
           ]

    return res


def test(par=0):
    """
    Test class CMultiChoiceTree.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    ctrl = icMultiCheckTreeListCtrl(frame, -1, None)
    tree_data = load_data()
    ctrl.LoadTree(tree_data)

    ################
    # Test code    #
    ################

    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    test()
