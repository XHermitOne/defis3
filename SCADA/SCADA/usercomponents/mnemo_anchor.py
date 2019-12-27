#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Якорь мнемосхемы SCADA системы.
"""

import wx
from ic.components import icwidget
# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from ic.PropertyEditor import icDefInf

from ic.log import log
from ic.bitmap import bmpfunc
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.utils import util

from ..mnemonic import mnemoanchor


ANCHOR_DIRECTION_CHOICES = {'ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT': mnemoanchor.ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT,
                            'ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT': mnemoanchor.ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT,
                            'ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM': mnemoanchor.ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
                            'ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP': mnemoanchor.ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP,
                            }

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
                'style': mnemoanchor.ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | mnemoanchor.ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,

                '__events__': {},
                '__lists__': {},
                '__styles__': ANCHOR_DIRECTION_CHOICES,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_POINT: ['svg_pos', ],
                                   icDefInf.EDT_SIZE: ['svg_size', 'min_size', 'max_size'],
                                   icDefInf.EDT_COMBINE: ['style'],
                                   icDefInf.EDT_USER_PROPERTY: ['attachment'],
                                   },
                '__parent__': mnemoanchor.SPC_IC_MNEMOANCHOR,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('anchor.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('anchor.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.mnemo_anchor.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('attachment',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('attachment',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('TextField', 'StaticText', 'StaticBitmap', 'Speedmeter', 'LEDNumberCtrl', 'Button', 'PlateButton'):
                dlgfunc.openWarningBox(u'ОШИБКА',
                                       u'Выбранный объект не является КОНТРОЛОМ, размещаемым на мнемосхеме.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('attachment',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icMnemoAnchor(icwidget.icSimple, mnemoanchor.icMnemoAnchorProto):
    """
    Якорь мнемосхемы SCADA системы.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

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

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        mnemoanchor.icMnemoAnchorProto.__init__(self,
                                                mnemoscheme=parent,
                                                pos=self.svg_pos,
                                                size=self.svg_size,
                                                direction=self.style,
                                                min_size=self.min_size,
                                                max_size=self.max_size)

    def getStyle(self):
        """
        Получить стиль якоря.
        """
        return self.style

    # Другое наименование метода
    getDirection = getStyle

    def getAttachmentPsp(self):
        """
        Получить паспорт объекта прикрепленного к якорю контрола.
        """
        return self.getICAttr('attachment')

    def getAttachment(self):
        """
        Получить объект прикрепленного к якорю контрола.

        :return: Объект контрола, который может быть размещен на мнемосхеме
            или None в случае ошибки.
        """
        psp = self.getAttachmentPsp()

        if psp:
            name = psp[0][1]
            if self.parent.isChild(name):
                return self.parent.GetChildByName(name)
            else:
                log.warning(u'Объект <%s> не является дочерним мнемосхемы якоря <%s>' % (name, self.getName()))
        return None

