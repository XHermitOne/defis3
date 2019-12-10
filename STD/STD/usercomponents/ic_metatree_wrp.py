#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дерево метакомпонентов.
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

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf
from ic.log import log
from ic.dlg import dlgfunc
from ic.utils import coderror

# import ic.utils.resource as resource
# import ic.storage.objstore as objstore

from STD.metastruct import metaitem
from STD.metastruct import metatree

# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

# --- Спецификация ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMetaTree'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaTree',
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {'on_init': (None, 'onInit', False),
                               'on_del': (None, 'onDel', False),
                               'on_edit': (None, 'onEdit', False),
                               'on_view': (None, 'onView', False),
                               },
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
                '__parent__': metatree.SPC_IC_METATREE,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMetaTree'
ic_class_pic2 = '@common.imgEdtMetaTree'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_metatree_wrp.icMetaTree-class.html'
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
                dlgfunc.openWarningBox(u'ОШИБКА', u'Выбранный объект не является объектным хранилищем.', ParentWin_=parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('source',):
        return pspEdt.str_to_val_user_property(text, propEdt)


# --- Классы ---
class icMetaTree(icwidget.icSimple, metatree.icMetaTreeEngine):
    """
    Дерево метакомпонентов.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно
        :type id: C{int}
        :param id: Идентификатор окна
        :type component: C{dictionary}
        :param component: Словарь описания компонента
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        metatree.icMetaTreeEngine.__init__(self, component)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
