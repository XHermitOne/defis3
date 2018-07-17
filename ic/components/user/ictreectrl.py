#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент древовидного представления данных.
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
import wx as parentModule
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg
import time
import ic.interfaces.icMetaTreeCtrlInterface as metaCtrl

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
                   'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS
                   }

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TreeCtrl',
                'name': 'default',

                'titleRoot': 'root',
                'selected': None,
                'activated': None,
                'onRightClick': None,
                'onExpand': None,
                'treeDict': {},

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type', 'titleRoot'],
                                   icDefInf.EDT_TEXTDICT: ['treeDict'],
                                   },
                '__events__': {'onRightClick': ('wx.EVT_TREE_ITEM_RIGHT_CLICK', 'OnRightClick', False),
                               'onExpand': ('wx.EVT_TREE_ITEM_EXPANDED', 'OnExpand'),
                               },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }
                    

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTreeListCtrl'
ic_class_pic2 = '@common.imgEdtTreeListCtrl'

#   Путь до файла документации
ic_class_doc = 'public/ictreectrl.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)


class treeItemData:
    """
    Класс для описания элемента дерева.
    """
    def __init__(self, descr={}):
        pass


class icTreeCtrl(icwidget.icWidget, parentModule.TreeCtrl, metaCtrl.MetaTreeCtrlInterface):
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
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelected)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpand)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.BindICEvt()
        
    def isDict(self, res):
        """
        Признак словарного интерфейса.
        """
        return isinstance(res, dict)

    #   Обработчики событий


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    @type par: C{int}
    @param par: Тип консоли.
    """
    res0 = {'d1': {'dd1': 'a1', 'dd2': 'a2'},
            'd2': {'cc1': 'a1', 'cc2': 'a2'},
            'd3': {'ee1': 'a1', 'ee2': 'a2'},
            }
    
    res = [res0, res0]

    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)
    common.img_init()

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
