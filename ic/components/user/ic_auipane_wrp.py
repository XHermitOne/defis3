#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс Панель главного окна. Технология AUI.

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
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.engine import icAUIpane
import ic.utils.coderror as coderror

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icAUIPane'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'AUIPane',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                
                'title': None,     # Заголовок
                'control_res': None,       # Имя ресурса прикрепленного контрола
                # 'control_name':None,     # Имя прикрепленного контрола
                # Размеры
                'min_size': (100, 100),    # Минимальный размер
                'best_size': (150, 150),   # Размер панели
                'max_size': (500, 500),    # Максимальный размер
                # Кнопки управления
                'maximize_button': True,   # Кнопка распахивания
                'close_button': True,      # Кнопка закрытия
                # Указание местаположения
                'direction': 'Left',   # Направление
                'layer': 0,    # Уравень/Слой
                'pos': 0,      # Позиция
                'row': 0,      # Строка
                'visible': True,   # Видимость при старте

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'direction': icAUIpane.AUI_PANE_DIRECTIONS, },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'title',
                                                            ],
                                   icDefInf.EDT_CHECK_BOX: ['maximize_button',
                                                            'close_button', 'visible'],
                                   icDefInf.EDT_CHOICE: ['direction'],
                                   icDefInf.EDT_NUMBER: ['layer', 'pos', 'row'],
                                   icDefInf.EDT_SIZE: ['min_size', 'best_size', 'max_size'],
                                   icDefInf.EDT_USER_PROPERTY: ['control_res'],
                                   },
                '__parent__': icAUIpane.SPC_IC_AUIPANE,
                '__attr_hlp__': {'title': u'Заголовок',
                                 'control_res': u'Имя ресурса прикрепленного контрола',
                                 'min_size': u'Минимальный размер',
                                 'best_size': u'Размер панели',
                                 'max_size': u'Максимальный размер',
                                 'maximize_button': u'Кнопка распахивания',
                                 'close_button': u'Кнопка закрытия',
                                 'direction': u'Направление',
                                 'layer': u'Уравень/Слой',
                                 'pos': u'Позиция',
                                 'row': u'Строка',
                                 'visible': u'Видимость при старте',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtFrame'
ic_class_pic2 = '@common.imgEdtFrame'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_auipane_wrp.icAUIPane-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('control_res',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value
    
    return ret


INS_TYPES = ('Panel', 'Window', 'ScrolledWindow', 'ScrolledPanel')


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('control_res',):
        ret=str_to_val_user_property(attr, value, propEdt)
        if ret and type(ret) == tuple:
            typ, name, ifs, fl, subsys = ret[0]
            if not typ in INS_TYPES:
                wx.MessageBox(u'%s <%s>. %s %s' % (_('Object type is'), typ, _('Object type must be'), INS_TYPES))
            else:
                return coderror.IC_CTRLKEY_OK 

        return coderror.IC_CTRL_FAILED_IGNORE


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('control_res',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icAUIPane(icwidget.icSimple, icAUIpane.icAUIPanePrototype):
    """
    Панель главного окна приложения. Технология AUI.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType = 0, evalSpace = None,
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        icAUIpane.icAUIPanePrototype.__init__(self, parent, component)

