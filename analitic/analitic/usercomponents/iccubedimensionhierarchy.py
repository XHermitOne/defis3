#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Иерархия уровней измерения OLAP Куба.
"""

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.utils import coderror
from ic.dlg import dlgfunc

from analitic.olap import cube_dimension_hierarchy_proto

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubeDimensionHierarchy'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubeDimensionHierarchy',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'levels': None,  # Список имен уровней измерения данной иерархии

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            ],
                                   icDefInf.EDT_USER_PROPERTY: ['levels'],
                                   },
                '__parent__': cube_dimension_hierarchy_proto.SPC_IC_CUBEDIMENSIONHIERARCHY,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('node-select-all.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('node-select-all.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

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
    if attr in ('levels', ):
        choices = [(spc['name'] in value, u'%s : %s' % (spc['name'], spc.get('description', u''))) for spc in propEdt.getParentResource()['child'] if spc.get('type', None) == 'CubeDimensionLevel']
        # log.debug(u'ВЫБОР %s' % str(choices))
        items = dlgfunc.getMultiChoiceDlg(parent=None, title=u'Уровни измерения',
                                          prompt_text=u'Выберите уровни измерения',
                                          choices=choices)
        # log.debug(u'Выбранные элементы %s' % str(items))
        ret = [item.split(u' : ')[0].strip() for check, item in items if check] if items else value

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('levels',):
        return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('levels', ):
        return eval(text) if text else None


class icCubeDimensionHierarchy(icwidget.icSimple,
                               cube_dimension_hierarchy_proto.icCubeDimensionHierarchyProto):
    """
    Иерархия уровней измерения OLAP Куба.
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

        cube_dimension_hierarchy_proto.icCubeDimensionHierarchyProto.__init__(self)

    def getLevelNames(self):
        """
        Список имен полей дополнительных атрибутов.
        """
        level_names = self.getICAttr('levels')
        return level_names if level_names else list()
