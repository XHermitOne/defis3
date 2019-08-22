#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Мета компонент управления планами.
Планирование может осуществляться в определенной иерархии разноса плановых
значений по подчиненным метаэлементам.
Характеризуется автоматическим разносом плановых значений в соответствии с
весовыми коэффициентами.

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

from ic.PropertyEditor import icDefInf

from ic.bitmap import bmpfunc
from ic.log import log
from ic.dlg import ic_dlg
from ic.utils import coderror

from STD.metastruct import metaitem
from STD.usercomponents import ic_metatree_wrp

# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icPlan'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'Plan',
                'name': 'default',

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'storage_type': [metaitem.FILE_NODE_STORAGE_TYPE,
                                               metaitem.FILE_STORAGE_TYPE,
                                               metaitem.DIR_STORAGE_TYPE],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description',
                                                            'view_form', 'edit_form', 'print_report'],
                                   icDefInf.EDT_CHECK_BOX: ['container'],
                                   icDefInf.EDT_TEXTDICT: ['spc', 'const_spc'],
                                   icDefInf.EDT_CHOICE: ['storage_type'],
                                   icDefInf.EDT_USER_PROPERTY: ['source'],
                                   },

                '__parent__': ic_metatree_wrp.ic_class_spc,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart-up-color.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart-up-color.png')

#   Путь до файла документации
ic_class_doc = 'doc/public/icplan.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['MetaItem', 'MetaConst', 'MetaAttr']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования свойств
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('source',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('source',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('ObjectStorage',):
                ic_dlg.openWarningBox(u'ОШИБКА', u'Выбранный объект не является объектным хранилищем.', ParentWin_=parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('source',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icPlan(ic_metatree_wrp.icMetaTree):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{child=[]}:
        - B{type='ModPlanManager'}: Тип.
        - B{name='default'}: Имя.
        - B{metaclass=None}: Ссылка (паспорт) на метокласса, описывающего элементы базового плана.
            Пример: ((None, IMetaplan, None, metadata/planProdaj.py, 'STIS'), <uuid>)

    """
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
        ic_metatree_wrp.icMetaTree.__init__(self, parent, id, component, logType, evalSpace, bCounter, progressDlg)
