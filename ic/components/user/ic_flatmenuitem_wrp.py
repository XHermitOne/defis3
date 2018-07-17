#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пункт меню.
Класс пользовательского визуального компонента ПУНКТ МЕНЮ.

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
from wx.lib.agw import flatmenu
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from ic.engine import icflatmenuitem
from ic.engine import icflatmenu
from ic.utils import coderror
from ic.dlg import ic_dlg

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icFlatMenuItem'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
SPC_IC_FLATMENUITEM_WRP = icflatmenuitem.SPC_IC_FLATMENUITEM
SPC_IC_FLATMENUITEM_WRP['__parent__'] = icwidget.SPC_IC_WIDGET

ic_class_spc = {'type': 'FlatMenuItem',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'label': 'item',   # Надпись
                'hot_key': None,   # Горячая клавиша
                'short_help': None,    # Всплывающая подсказка
                'pic1': None,          # Образ пункта
                'pic2': None,          # Образ выключенного пункта
                'onSelected': None,    # Блок кода на выбор пункта
                'kind': 'normal',      # Вид пункта меню

                '__styles__': ic_class_styles,
                '__lists__': {'kind': icflatmenuitem.IC_ITEM_KIND,
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'label', 'short_help',
                                                            'hot_key', 'item'],
                                   icDefInf.EDT_CHOICE: ['kind'],
                                   icDefInf.EDT_USER_PROPERTY: ['pic1', 'pic2', ],
                                   icDefInf.EDT_CHECK_BOX: ['activate'],
                                   },
                '__events__': {'onSelected': ('wx.lib.agw.flatmenu.EVT_FLAT_MENU_SELECTED', 'OnSelected', False),
                               },

                '__parent__': SPC_IC_FLATMENUITEM_WRP,
                '__attr_hlp__': {'label': u'Надпись',
                                 'hot_key': u'Горячая клавиша',
                                 'short_help': u'Всплывающая подсказка',
                                 'pic1': u'Образ пункта',
                                 'pic2': u'Образ выключенного пункта',
                                 'onSelected': u'Блок кода на выбор пункта',
                                 'kind': u'Вид пункта меню',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMenuItem'
ic_class_pic2 = '@common.imgEdtMenuItem'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_flatmenuitem_wrp.icFlatMenuItem-class.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 5)

# Функции редактирования


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('pic1', 'pic2'):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('pic1', 'pic2'):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Bitmap',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является картинкой.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('pic1', 'pic2'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icFlatMenuItem(icwidget.icWidget, icflatmenuitem.icFlatMenuItemPrototype):
    """
    Пункт меню.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
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

        id = wx.NewId()
        self.label = self.getLabel()
        self.short_help = self.getShortHelp()
        self.kind = self.getKind()
        self.pic1 = self.getPic1()
        self.pic2 = self.getPic2()

        # Version 2.9.1
        if wx.VERSION > (2, 8, 11, 10):
            icflatmenuitem.icFlatMenuItemPrototype.__init__(self, parent, id=id,
                                                            label=self.label, helpString=self.short_help,
                                                            kind=self.kind,
                                                            normalBmp=self.pic1, disabledBmp=self.pic2)
        else:
            icflatmenuitem.icFlatMenuItemPrototype.__init__(self, parent, id=id,
                                                            text=self.label, helpString=self.short_help,
                                                            kind=self.kind,
                                                            normalBmp=self.pic1, disabledBmp=self.pic2)

        if parent:
            # Добавить пункт в родительское меню
            self.appendIntoParent(parent)

        # Обработчик выбора пункта меню
        menubar = self.getMenuBar()
        if menubar:
            menubar.Bind(flatmenu.EVT_FLAT_MENU_SELECTED, self.OnSelected, id=id)
        else:
            menu = self.GetMenu()
            menu.GetParent().Bind(flatmenu.EVT_FLAT_MENU_SELECTED, self.OnSelected, id=id)
            # menu.Bind(flatmenu.EVT_FLAT_MENU_SELECTED, self.OnSelected, id=id)

    def appendIntoParent(self, Parent_):
        """
        Добавить пункт в родительское меню.
        """
        if Parent_:
            if issubclass(Parent_.__class__, icflatmenu.icFlatMenuPrototype):
                # Добавляем в выпадающее меню
                kind = self.getKind()
                if kind == wx.ITEM_NORMAL:
                    Parent_.AppendItem(self)
                elif kind == wx.ITEM_SEPARATOR:
                    Parent_.AppendSeparator()
                elif kind == wx.ITEM_CHECK:
                    pass
                elif kind == wx.ITEM_RADIO:
                    pass

    def OnSelected(self, event):
        """
        Обработчик выбора пункта меню.
        """
        self.eval_event('onSelected', event, True)

    def GetName(self):
        """
        Имя объекта.
        """
        return self.name

    def SetName(self, name):
        """
        Имя объекта.
        """
        self.name = name

    def getLabel(self):
        """
        Надпись.
        """
        return self.getICAttr('label')

    def getShortHelp(self):
        """
        Всплывающая подсказка.
        """
        return self.getICAttr('short_help')

    def getKind(self):
        """
        Вид пункта меню.
        """
        kind_str = self.getICAttr('kind')
        if kind_str == 'normal':
            return wx.ITEM_NORMAL
        elif kind_str == 'separator':
            return wx.ITEM_SEPARATOR
        elif kind_str == 'check':
            return wx.ITEM_CHECK
        elif kind_str == 'radio':
            return wx.ITEM_RADIO
        # Вид пункта меню не определен
        return None

    def _createPicBmp(self, bmp_psp):
        """
        Создать картинку по паспорту.
        """
        # Паспорт не определен
        if not bmp_psp:
            return None

        item_kind = self.getKind()
        # для разделителя нельзя установить картинку
        if item_kind == wx.ITEM_SEPARATOR:
            return None

        bitmap_obj = self.GetKernel().Create(bmp_psp)
        bmp = bitmap_obj.getBitmap()
        return bmp

    def getPic1(self):
        """
        Картинка нормального состояния пункта меню.
        """
        bmp_psp = self.getICAttr('pic1')
        bmp = self._createPicBmp(bmp_psp)
        if bmp is None:
            return wx.NullBitmap
        return bmp

    def getPic2(self):
        """
        Картинка выключенного состояния пункта меню.
        """
        bmp_psp = self.getICAttr('pic2')
        bmp = self._createPicBmp(bmp_psp)
        if bmp is None:
            return wx.NullBitmap
        return bmp
