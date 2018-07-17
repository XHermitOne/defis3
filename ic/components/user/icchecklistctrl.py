#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс многоколоночного списка с возможностью отметки строки/элемента списка.
"""

import wx
import wx.lib.mixins.listctrl

from ic.bitmap import ic_bmp
from ic.log import log
from ic.utils import util

import ic.PropertyEditor.icDefInf as icDefInf
from ic.components import icwidget

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCheckListCtrl'

# --- Описание стилей компонента ---
ic_class_styles = {'DEFAULT': wx.LC_HRULES | wx.LC_VRULES}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'CheckListCtrl',
                'name': 'default',
                'child': [],
                'style': wx.LC_HRULES | wx.LC_VRULES,

                'labels': ['col1'],     # Заголовки колонок
                'wcols': [],            # Ширины колонок

                'on_toggle_item': None,     # Обработчик вкл./выкл. элемента списка
                'on_select_item': None,     # Обработчик выделения элемента списка

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type', 'titleRoot'],
                                   icDefInf.EDT_TEXTLIST: ['labels', 'wcols'],
                                   icDefInf.EDT_PY_SCRIPT: ['on_toggle_item', 'on_select_item'],
                                   },
                '__attr_hlp__': {'labels': u'Заголовки колонок',
                                 'wcols': u'Ширины колонок',
                                 'on_toggle_item': u'Обработчик вкл./выкл. элемента списка',
                                 'on_select_item': u'Обработчик выделения элемента списка',
                                 },

                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ui-check-boxes-list.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ui-check-boxes-list.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 2, 1)


class icCheckListCtrl(icwidget.icWidget, wx.ListCtrl,
                      wx.lib.mixins.listctrl.CheckListCtrlMixin):
    """
    Класс многоколоночного списка с возможностью отметки строки.
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

        icwidget.icWidget.__init__(self, parent,
                                   id, component, logType, evalSpace)

        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        wx.lib.mixins.listctrl.CheckListCtrlMixin.__init__(self)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)

    def onToggleItem(self, event, index_item=None, check=False):
        """
        Обработчик вкл./выкл. элемента списка.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = event
        self.evalSpace['event'] = event
        self.evalSpace['CHECK'] = self.IsChecked(event.m_itemIndex) if event else check
        self.evalSpace['ITEM'] = self.GetFirstSelected() if index_item is None else index_item

        self.eval_attr('on_toggle_item')
        if event:
            event.Skip()

    def onItemActivated(self, event):
        """
        Обработчик активации элемента списка.
        """
        self.ToggleItem(event.m_itemIndex)
        self.onToggleItem(event)

    def OnCheckItem(self, index_item, flag):
        """
        This is called by the base class when an item is checked/unchecked.
        @param index_item: Индекс элемента списка. 
        @param flag: Вкл. или выкл. элемент списка.
        @return: 
        """
        self.onToggleItem(None, index_item, flag)

    def onItemSelected(self, event):
        """
        Обработчик выделения элемента списка.
        """
        selected_item_idx = event.m_itemIndex if event else self.GetFirstSelected()
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = event
        self.evalSpace['event'] = event
        self.evalSpace['CHECK'] = self.IsChecked(selected_item_idx) if selected_item_idx >= 0 else False
        self.evalSpace['ITEM'] = selected_item_idx

        self.eval_attr('on_select_item')
        if event:
            event.Skip()
