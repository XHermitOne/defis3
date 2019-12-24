#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент древовидного представления данных.
Класс пользовательского визуального компонента.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import wx as parentModule

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
import ic.interfaces.icMetaTreeCtrlInterface as metaCtrl
from ic.engine import treectrl_manager

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTreeCtrl'

#   Описание стилей компонента
ic_class_styles = {'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
                   'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
                   'TR_NO_LINES': wx.TR_NO_LINES,
                   'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
                   'TR_SINGLE': wx.TR_SINGLE,
                   'TR_MULTIPLE': wx.TR_MULTIPLE,
                   # 'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   # 'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS
                   }

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TreeCtrl',
                'name': 'default',

                'titleRoot': 'root',
                'selected': None,
                'activated': None,
                'onRightClick': None,
                'onExpand': None,
                'onCollapse': None,
                'selectChanged': None,
                'itemActivated': None,
                'treeDict': {},

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type', 'titleRoot'],
                                   icDefInf.EDT_TEXTDICT: ['treeDict'],
                                   },
                '__events__': {'onRightClick': ('wx.EVT_TREE_ITEM_RIGHT_CLICK', 'OnRightClick', False),
                               'onExpand': ('wx.EVT_TREE_ITEM_EXPANDED', 'OnExpand', False),
                               'onCollapse': ('wx.EVT_TREE_ITEM_COLLAPSED', 'OnCollapse', False),
                               'selectChanged': ('wx.EVT_TREE_SEL_CHANGED', 'onSelectChanged', False),
                               'itemActivated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'onItemActivated', False),
                               'keyDown': ('wx.EVT_TREE_KEY_DOWN', 'OnTreeListKeyDown', False),
                               },
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'titleRoot': u'Надпись корневого элемента',
                                 },
                }
                    

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeListCtrl'
ic_class_pic2 = '@common.imgEdtTreeListCtrl'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ictreectrl.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class treeItemData:
    """
    Класс для описания элемента дерева.
    """
    def __init__(self, descr={}):
        pass


class icTreeCtrl(icwidget.icWidget, parentModule.TreeCtrl,
                 metaCtrl.MetaTreeCtrlInterface,
                 treectrl_manager.icTreeCtrlManager):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
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

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        #   Признак разрешающий редактировать дерево
        self._bEditMode = True
        #   Признак заполнения буфера
        self.bObjBuff = False

        for key in lst_keys:
            setattr(self, key, component[key])

        parentModule.TreeCtrl.__init__(self, parent, id, self.position, self.size,
                                       style=self.style)

        metaCtrl.MetaTreeCtrlInterface.__init__(self)

        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpand)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapse)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        # self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnTreeListKeyDown)
        # self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelected)
        # self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        # self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpand)
        # self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.BindICEvt()
        
    def isDict(self, res):
        """
        Признак словарного интерфейса.
        """
        return isinstance(res, dict)

    def getTitleRoot(self):
        """
        Надпись корневого элемента.

        :return:
        """
        return self.getICAttr('titleRoot')

    def setTree(self, tree_data, label=None, expand_root=True, expand_all=False):
        """
        Установить данные дерева.

        :param tree_data: Данные дерева:
            Каждый узел дерева - словарь.
            Дочерние элементы находяться в ключе '__children__' в виде списка.
            Если корневой узел данных является списком,
            то в контроле присутствует несколько корневых узлов.
        :param label: Ключ для определения надписи элемента дерева.
        :param expand_root: Произвести автоматическое распахивание корневого элемента?
        :param expand_all: Произвести автоматическое распахивание
            всех дочерних элементовкорневого элемента?
        :return: True/False.
        """
        result = self.setTree_TreeCtrl(self, tree_data, label=label)
        title_root = self.getTitleRoot()
        self.setRootTitle(self, title_root)
        if expand_root:
            # Произвести автоматическое распахивание корневого элемента
            self.expandChildren(self, all_children=expand_all)

        return result

    def setItemColour(self, fg_colour=None, bg_colour=None, requirement=None):
        """
        Установить цвет элементов дерева в контроле по определенному условию.

        :param fg_colour: Цвет текста, если условие выполненно.
        :param bg_colour: Цвет фона, если условие выполненно.
        :param requirement: lambda выражение, формата:
            lambda item: ...
            Которое возвращает True/False.
            Если True, то установка цвета будет сделана.
            False - строка не расцвечивается.
        :return:
        """
        return self.setItemColour_requirement(ctrl=self, fg_colour=fg_colour,
                                              bg_colour=bg_colour, requirement=requirement,
                                              item=None)

    def setItemData(self, item, data):
        """
        Привязать данные к элементу дерева.

        :param item: Элемент дерева.
        :param data: Прикрепляемые данные.
        """
        return self.setItemData_TreeCtrl(self, item, data)

    def getItemData(self, item):
        """
        Получить прикрепленные данные к элементу дерева.

        :param item: Элемент дерева.
        :return: Прикрепленные данные к элементу дерева или None в случае ошибки.
        """
        return self.getItemData_TreeCtrl(self, item)

    # Другое наименование метода
    getItemRecord = getItemData

    def findItem(self, requirement=None):
        """
        Поиск элемента дерева по требованию.

        :param requirement: lambda выражение, формата:
            lambda item: ...
            Которое возвращает True/False.
            Если True, то элемент удовлетворяет критерию поиска.
            False - строка не удовлетворяет.
        :return: Найденный элемент или None если не найден элемент.
        """
        return self.findItem_requirement(ctrl=self, requirement=requirement)

    #   Обработчики событий
    def OnExpand(self, event):
        """
        Разворачивание узла.
        """
        self.eval_event('onExpand', event, True)

    def OnCollapse(self, event):
        """
        Сворачивание узла.
        """
        self.eval_event('onCollapse', event, True)

    def OnSelectChanged(self, event):
        """
        Изменение выделенного узла.
        """
        select_item = event.GetItem()
        # self._last_selection = None
        # if select_item:
        #     self._last_selection = self.getItemPath(self, select_item)

        # --- НАЧАЛО: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        if not self.HasFlag(wx.TR_MULTIPLE):
            selections = self.GetSelections()
            if len(selections) > 1:
                for selection in selections:
                    if selection != select_item:
                        selection.SetHilight(0)
                        self._main_win.RefreshLine(selection)
        # --- КОНЕЦ: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        self.eval_event('selectChanged', event, True)

    def OnItemActivated(self, event):
        """
        Активизация узла.
        """
        self.eval_event('itemActivated', event, True)


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    :type par: C{int}
    :param par: Тип консоли.
    """
    res0 = {'d1': {'dd1': 'a1', 'dd2': 'a2'},
            'd2': {'cc1': 'a1', 'cc2': 'a2'},
            'd3': {'ee1': 'a1', 'ee2': 'a2'},
            }
    
    res = [res0, res0]

    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.init_img()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    tree = icTreeCtrl(win, -1, {'position': (10, 10), 'size': (200, 300),
                                'style': wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS})

    tree.LoadTree(res)
    
    frame.Show(True)
    app.MainLoop()


def testStorage():
    """
    Тестируем пользовательский класс.
    """
    from ic.storage import storesrc
    
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
            a[j] = 'indx idx,j=%d.%d' % (i, j)
            print(u'\tms[idx][j] = %s' % a[j])
        ms[i] = a
    
    storage.Close()
    storage.Open()
    return storage


if __name__ == '__main__':
    test()
