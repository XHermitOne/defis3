#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Агрегация OLAP Куба.
"""

from ic.log import log
from ic.bitmap import ic_bmp
from ic.utils import util
from ic.utils import coderror
from ic.dlg import ic_dlg

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from analitic.olap import cube_aggregate_proto

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubeAggregate'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubeAggregate',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'function': None,   # Функция агрегации
                'measure': None,    # Мера/Факт, которое агрегируется
                'expression': None,     # Выражение агрегации

                'label': None,  # Надпись агрегации

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'label'],
                                   icDefInf.EDT_CHOICE: ['function'],
                                   icDefInf.EDT_USER_PROPERTY: ['measure'],
                                   },
                '__parent__': cube_aggregate_proto.SPC_IC_CUBEAGGREGATE,
                '__lists__': {'function': cube_aggregate_proto.AGGREGATE_FUNCTIONS},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('sum.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('sum.png')

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
    if attr in ('measure',):
        choices = [u''] + [u'%s : %s' % (spc['name'], spc.get('description', u'')) for spc in propEdt.getParentResource()['child'] if spc.get('type', None) == 'CubeMeasure']
        text = ic_dlg.icSingleChoiceDlg(parent=None, title=u'Меры/Факты',
                                        prompt_text=u'Выберите меру/факт агрегации',
                                        choices=choices)
        ret = text.split(u' : ')[0].strip() if text else u''

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('measure',):
        return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('measure',):
        return text.split(u' : ')[0].strip() if text else None


class icCubeAggregate(icwidget.icSimple,
                      cube_aggregate_proto.icCubeAggregateProto):
    """
    Агрегация OLAP Куба.
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        cube_aggregate_proto.icCubeAggregateProto.__init__(self)

    def getFunctionName(self):
        """
        Функция агрегации.
        """
        return self.getICAttr('function')

    def getMeasureName(self):
        """
        Мера/Факт, которое агрегируется.
        """
        return self.getICAttr('measure')

    def getExpressionCode(self):
        """
        Выражение агрегации.
        """
        return self.getICAttr('expression')

    def getLabel(self):
        """
        Надпись измерения.
        Если не определено, то берется description.
        Если и в этом случае не определено, то берем name.
        """
        label = self.getICAttr('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label
