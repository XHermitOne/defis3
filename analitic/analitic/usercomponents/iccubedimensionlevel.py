#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Уровень измерения OLAP Куба.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util
from ic.dlg import dlgfunc
from ic.utils import coderror

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from analitic.olap import cube_dimension_level_proto

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubeDimensionLevel'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubeDimensionLevel',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'attributes': None,  # Список имен полей дополнительных атрибутов

                'key': None,  # Указывает, какой атрибут будет использоваться для фильтрации
                'label_attribute': None,  # Указывает, какой атрибут будет отображаться в пользовательском интерфейсе
                'label': None,  # Надпись уровня измерения
                'mapping': None,  # Физичекое указание поля для отображения

                'get_normal': None,  # Функция нормирования данных уровня

                '__events__': {'get_normal': (None, 'getNormal', False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'mapping'],
                                   icDefInf.EDT_TEXTLIST: ['attributes'],
                                   icDefInf.EDT_USER_PROPERTY: ['key', 'label_attribute'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_normal']
                                   },
                '__parent__': cube_dimension_level_proto.SPC_IC_CUBEDIMENSIONLEVEL,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('node-select-child.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('node-select-child.png')

#   Путь до файла документации
ic_class_doc = 'analitic/doc/_build/html/analitic.usercomponents.iccubedimensionlevel.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('key', 'label_attribute'):
        spc = propEdt.getResource()
        choices = [u''] + [attribute for attribute in spc.get('attributes', [])] if spc.get('attributes', None) else []
        result = dlgfunc.getSingleChoiceDlg(parent=None, title=u'Аттрибуты',
                                            prompt_text=u'Выберите аттрибут',
                                            choices=choices)
        if result == u'':
            return None
        else:
            ret = result if result else None

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('key', 'label_attribute'):
        return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('key', 'label_attribute'):
        return text if text else None


class icCubeDimensionLevel(icwidget.icSimple,
                           cube_dimension_level_proto.icCubeDimensionLevelProto):
    """
    Уровень измерения OLAP Куба.
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        cube_dimension_level_proto.icCubeDimensionLevelProto.__init__(self)

    def getAttributes(self):
        """
        Список имен полей дополнительных атрибутов.
        """
        attributes = self.getICAttr('attributes')
        return [attribute for attribute in attributes if attribute] if attributes else list()

    def getKey(self):
        """
        Ключ. Указывает, какой атрибут будет использоваться для фильтрации.
        """
        key = self.getICAttr('key')
        return key

    def getLabelAttribute(self):
        """
        Атрибут надписи. Указывает, какой атрибут будет отображаться в пользовательском интерфейсе.
        """
        label_attribute = self.getICAttr('label_attribute')
        # log.debug(u'Атрибут надписи <%s>' % label_attribute)
        return label_attribute

    def getLabel(self):
        """
        Надпись уровня измерения.
        Если не определено, то берется description.
        Если и в этом случае не определено, то берем name.
        """
        label = self.getICAttr('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

    def getMapping(self):
        """
        Физичекое указание поля для отображения уровня.
        """
        return self.getICAttr('mapping')

    def getNormal(self):
        """
        Функция нормирования данных уровня.
        """
        if self.isICAttrValue('get_normal'):
            return self.eval_attr('get_normal')
        return None
