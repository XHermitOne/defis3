#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол выбора элемента справочника в виде выпадающего дерева.

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
from ic.dlg import ic_dlg
import ic.components.icResourceParser as prs
from NSI.nsi_sys import nsi_images
import ic.PropertyEditor.icDefInf as icDefInf

from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import NSI.nsi_sys.icspravtreecomboctrl as parentModule

ICComboCtrlStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                    'CB_DROPDOWN': wx.CB_DROPDOWN,
                    'CB_READONLY': wx.CB_READONLY,
                    'CB_SORT': wx.CB_SORT,
                    }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpravTreeComboCtrl'

#   Описание стилей компонента
ic_class_styles = ICComboCtrlStyle

# Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SpravTreeComboCtrl',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'sprav': None,         # Паспорт справочника-источника данных
                'root_code': None,     # Код корневого элемента ветки справочника
                'view_all': False,     # Показывать все элементы справочника
                'level_enable': -1,    # Номер уровня с которого включаются элементы для выбора
                'popup_type': 0,
                'expand': True,        # Распахнуть
                'complex_load': True,  # Комплексная загрузка всех элементов справочника

                'get_label': None,     # Функция определения надписи элемента дерева
                'find_item': None,     # Функция поиска элемента дерева
                'get_selected_code': None,  # Функция получения выбранного кода
                'set_selected_code': None,  # Функция установки выбранного кода

                'on_change': None,     # Обработчик изменения выбранного кода

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description', 'root_code'],
                                   icDefInf.EDT_NUMBER: ['level_enable', 'popup_type'],
                                   icDefInf.EDT_USER_PROPERTY: ['sprav'],
                                   icDefInf.EDT_CHECK_BOX: ['view_all', 'complex_load'],
                                   },
                '__events__': {'on_change': ('wx.EVT_TEXT', 'onTextChange', False),
                               },
                '__parent__': parentModule.SPC_IC_SPRAVTREECOMBOCTRL,
                '__attr_hlp__': {'sprav': u'Паспорт справочника-источника данных',
                                 'root_code': u'Код корневого элемента ветки справочника',
                                 'view_all': u'Показывать все элементы справочника',
                                 'level_enable': u'Номер уровня с которого включаются элементы для выбора',
                                 'popup_type': u'',
                                 'expand': u'Распахнуть',
                                 'complex_load': u'Комплексная загрузка всех элементов справочника',
                                 'get_label': u'Функция определения надписи элемента дерева',
                                 'find_item': u'Функция поиска элемента дерева',
                                 'get_selected_code': u'Функция получения выбранного кода',
                                 'set_selected_code': u'Функция установки выбранного кода',
                                 'on_change': u'Обработчик изменения выбранного кода',
                                 },
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = nsi_images.style_sprav_combo
ic_class_pic2 = nsi_images.style_sprav_combo

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('sprav',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('sprav',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Sprav',):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Выбранный объект не является Справочником.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('sprav',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSpravTreeComboCtrl(parentModule.icSpravTreeComboCtrlPrototype, icwidget.icWidget):
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

        sprav_psp = self.getSpravPsp()
        root_code = self.getRootCode()
        view_all = self.getViewAll()
        complex_load = self.getComplexLoad()

        parentModule.icSpravTreeComboCtrlPrototype.__init__(self,
                                                            parent, id,
                                                            size=self.size, pos=self.position, style=self.style,
                                                            popup_type=component['popup_type'],
                                                            )

        self.init(sprav_psp, root_code, view_all, complex_load)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        # Регистрация обработчиков
        self.Bind(wx.EVT_TEXT, self.onTextChange, id=id)
        self.BindICEvt()

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getSpravPsp(self):
        """
        Паспорт справочника-источника данных.
        """
        return self.getICAttr('sprav')

    def getRootCode(self):
        """
        Код корневого элемента.
        """
        return self.getICAttr('root_code')

    def getViewAll(self):
        """
        Отображать все элементы?
        """
        return self.getICAttr('view_all')

    def getComplexLoad(self):
        """
        Комплексная загрузка всех элементов?
        """
        return self.getICAttr('complex_load')

    def getLevelEnable(self):
        """
        Индекс уровня с которого можно выбирать.
        """
        return self.getICAttr('level_enable')

    def getLabelFunc(self, *arg, **kwarg):
        """
        Получить функцию определения надписи элемента дерева.
        """
        result = self.eval_attr('get_label')
        if result[0]:
            return result[1]
        return None

    def getFindItemFunc(self, *args, **kwargs):
        """
        Получить функцию альтернативного поиска.
        """
        self.evalSpace.update(kwargs)
        self.evalSpace['args'] = args

        result = self.eval_attr('find_item')
        if result[0]:
            return result[1]
        return None

    def getSelectedCodeFunc(self):
        """
        Получить функцию определения выбранного кода.
        """
        result = self.eval_attr('get_selected_code')
        if result[0]:
            return result[1]
        return None

    def setSelectedCodeFunc(self, *args, **kwargs):
        """
        Получить функцию определения выбранного кода.
        """
        self.evalSpace.update(kwargs)
        self.evalSpace['args'] = args

        result = self.eval_attr('set_selected_code')
        if result[0]:
            return result[1]
        return None

    #   Обработчики событий

    def onTextChange(self, event):
        """
        Обработчик изменений значения контрола.
        """
        self.eval_event('on_change', event, True)
