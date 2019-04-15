#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления мета-деревьями.
"""

import wx

from ic.log import log
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.utils import util
from ic.bitmap import ic_bmp
from ic.components import icwidget
import ic.components.icResourceParser as prs

import STD.metastruct.icmetatreelistctrl as parentModule

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

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

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMetaTreeListCtrl'

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaTreeListCtrl',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'metatree': None,   # Паспорт объекта описания мета-дерева

                'on_item_collapsed': None,
                'on_item_expanded': None,
                'on_select_changed': None,
                'on_item_activated': None,
                'on_item_right_click': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'description'],
                                   icDefInf.EDT_USER_PROPERTY: ['metatree'],
                                   },
                '__events__': {'on_item_collapsed': ('wx.EVT_TREE_ITEM_COLLAPSED', 'onItemCollapsed', False),
                               'on_item_expanded': ('wx.EVT_TREE_ITEM_EXPANDED', 'onItemExpanded', False),
                               'on_select_changed': ('wx.EVT_TREE_SEL_CHANGED', 'onSelectChanged', False),
                               'on_item_activated': ('wx.EVT_TREE_ITEM_ACTIVATED', 'onItemActivated', False),
                               'on_item_right_click': ('wx.EVT_TREE_ITEM_RIGHT_CLICK', 'onItemRightClick', False),
                               },
                '__parent__': parentModule.SPC_IC_METATREELISTCTRL,

                '__attr_hlp__': {'on_item_collapsed': u'Обработчик сворачивания элемента',
                                 'on_item_expanded': u'Обработчик развертывания элемента',
                                 'on_select_changed': u'Обработчик изменения выбора',
                                 'on_item_activated': u'Обработчик активации элемента',
                                 'on_item_right_click': u'Обработчик клика правой кнопкой на элементе',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('ui-scroll-pane-block.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('ui-scroll-pane-block.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['GridCell']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('metatree',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('metatree',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('MetaTree', 'Plan'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является объектом описания мета-дерева.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('metatree',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icMetaTreeListCtrl(parentModule.icMetaTreeListCtrlProto, icwidget.icWidget):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

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

        parentModule.icMetaTreeListCtrlProto.__init__(self, parent, id,
                                                      size=self.size, pos=self.position, style=self.style)

        # Установить метадерево
        metatree_psp = self.getMetaTreePsp()
        metatree = self.GetKernel().Create(metatree_psp) if metatree_psp else None
        self.setMetaTree(metatree)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemActivated)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)
        self.BindICEvt()

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getMetaTreePsp(self):
        """
        Паспорт объекта мета-дерева.
        """
        return self.getICAttr('metatree')

    def getColumnLabels(self):
        """
        Получить надписи колонок.
        Контрол в любом случае имеет одну колонку для отображения метадерева.
        Переопределяемый метод.
        @return: Список надписай колонок.
        """
        return [column.get('label', u'') for column in self.resource['child']]

    def getColumnWidths(self):
        """
        Получить ширины колонок.
        Контрол в любом случае имеет одну колонку для отображения метадерева.
        Переопределяемый метод.
        @return: Список ширин колонок.
        """
        return [column.get('width', wx.DefaultSize.GetWidth()) for column in self.resource['child']]

    # --- Обработчики событий ---
    def onItemExpanded(self, event):
        """
        Разворачивание узла.
        """
        self.eval_event('on_item_expanded', event, True)
        event.Skip()

    def onItemCollapsed(self, event):
        """
        Сворачивание узла.
        """
        self.eval_event('on_item_collapsed', event, True)
        event.Skip()

    def onSelectChanged(self, event):
        """
        Изменение выделенного узла.
        """
        select_item = event.GetItem()
        self._last_selection = None
        if select_item:
            self._last_selection = self.getItemPath(select_item)

        # --- НАЧАЛО: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        if not self.HasFlag(wx.TR_MULTIPLE):
            selections = self.GetSelections()
            if len(selections) > 1:
                for selection in selections:
                    if selection != select_item:
                        selection.SetHilight(0)
                        self._main_win.RefreshLine(selection)
        # --- КОНЕЦ: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        self.eval_event('on_select_changed', event, True)
        event.Skip()

    def onItemActivated(self, event):
        """
        Активизация узла.
        """
        self.eval_event('on_item_activated', event, True)
        event.Skip()

    def onItemRightClick(self, event):
        """
        Обработчик клика правой кнопкой на элементе.
        """
        if self.isICAttrValue('on_item_right_click'):
            self.eval_event('on_item_right_click', event, True)
        else:
            # По умолчанию производим вызов меню добавления нового элемента
            menu = wx.Menu()
            item = event.GetItem()
            meta_item = self.getItemData_tree(ctrl=self, item=item)
            label = u'Добавить <%s>' % meta_item.description
            add_id = wx.NewId()
            menu.Append(add_id, label)
            self.Bind(wx.EVT_MENU, self.onAddMetaItem, id=add_id)
            label = u'Удалить <%s>' % meta_item.description
            del_id = wx.NewId()
            menu.Append(del_id, label)
            self.Bind(wx.EVT_MENU, self.onDelMetaItem, id=del_id)

            self.PopupMenu(menu)
        event.Skip()

    def onAddMetaItem(self, event):
        """
        Обработчик добавления мета-объекта.
        """
        log.debug(u'Обработчик добавления мета-объекта')
        event.Skip()

    def onDelMetaItem(self, event):
        """
        Обработчик удаления мета-объекта.
        """
        log.debug(u'Обработчик удаления мета-объекта')
        event.Skip()
