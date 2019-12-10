#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Якорь мнемосхемы SCADA системы.
"""

import wx
from ic.components import icwidget
# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

from ic.PropertyEditor import icDefInf

from ic.log import log
from ic.bitmap import bmpfunc
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.utils import util

from SCADA.mnemonic import mnemoanchor


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMnemoAnchor'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MnemoAnchor',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   },
                '__parent__': mnemoanchor.SPC_IC_MNEMOANCHOR,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('anchor.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('anchor.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования
# def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
#     """
#     Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
#     """
#     ret = None
#     if attr in ('scan_class',):
#         ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
#     elif attr in ('engines',):
#         ret = pspListEdt.get_user_property_editor(value, pos, size, style, propEdt)
#
#     if ret is None:
#         return value
#
#     return ret
#
#
# def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
#     """
#     Стандартная функция контроля.
#     """
#     if attr in ('scan_class',):
#         ret = str_to_val_user_property(attr, value, propEdt)
#         if ret:
#             parent = propEdt
#             if not ret[0][0] in ('ScanClass',):
#                 dlgfunc.openWarningBox(u'ОШИБКА',
#                                        u'Выбранный объект не является КЛАССОМ СКАНИРОВАНИЯ.')
#                 return coderror.IC_CTRL_FAILED_IGNORE
#             return coderror.IC_CTRL_OK
#     elif attr in ('engines',):
#         ret = str_to_val_user_property(attr, value, propEdt)
#         if ret:
#             parent = propEdt
#             first_menubar_type = ret[0][0][0]
#             for cur_psp in ret:
#                 if not cur_psp[0][0] in ('SCADAEngine',):
#                     dlgfunc.openWarningBox(u'ОШИБКА',
#                                            u'Выбранный объект [%s] не является ДВИЖКОМ SCADA СИСТЕМЫ.' % cur_psp)
#                     return coderror.IC_CTRL_FAILED_IGNORE
#             return coderror.IC_CTRL_OK
#
#
# def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
#     """
#     Стандартная функция преобразования текста в значение.
#     """
#     if attr in ('scan_class',):
#         return pspEdt.str_to_val_user_property(text, propEdt)
#     elif attr in ('engines',):
#         return pspListEdt.str_to_val_user_property(text, propEdt)


class icMnemoAnchor(icwidget.icSimple, mnemoanchor.icMnemoAnchorProto):
    """
    Якорь мнемосхемы SCADA системы.

    :type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        mnemoanchor.icMnemoAnchorProto.__init__(self)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])
