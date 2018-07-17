#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент контроллера/узла SCADA системы памяти.

Используется для вычисляемых тегов.
Все теги Memory узла являются вычисляемыми.
Выражение для вычисления записывается в 'address' тега.

ВНИМАНИЕ! Все блоки кода вычисляемых тегов выполняются в контексте
Memory узла. Поэтому все функции расчетов необходимо расмолагать
в менеджере Memory Node.
"""

from ic.log import log

from ic.components import icwidget

from ic.utils import util
from ic.utils import coderror
from ic.PropertyEditor import icDefInf

from ic.bitmap import ic_bmp

from . import node

# --- Спецификация ---
SPC_IC_MEMORY_NODE = {'__parent__': icwidget.SPC_IC_SIMPLE,

                      '__attr_hlp__': {},
                      }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMemoryNode'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MemoryNode',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   },
                '__parent__': SPC_IC_MEMORY_NODE,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('memory.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('memory.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 7)


class icMemoryNode(icwidget.icSimple, node.icSCADANodeProto):
    """
    Компонент контроллера/узла SCADA системы памяти.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

    def doExpression(self, expression, environment=None):
        """
        Выполнить выражение.
        ВНИМАНИЕ! Все блоки кода вычисляемых тегов выполняются в контексте
        Memory узла. Поэтому все функции расчетов необходимо расмолагать
        в менеджере Memory Node.
        @param expression: Выполняемое выражение.
        @param environment: Дополнительное окружение выполнения выражения.
            Если не определено, то берется автоматически заполняемое при
            помощи getEnv().
        @return: Результат выполнения выражения или None в случае ошибки.
        """
        if environment is None:
            environment = self.getEnv()
        context = self.GetContext()
        context.update(environment)

        tag = context.get('TAG', None)
        tag_name = tag.getName() if tag else 'default'

        # ВНИМАНИЕ! Чтобы привязать обработчики к конкретному тегу
        # необходимо указывать имя тега для выражения.
        # В данном случае функция-обработчик будет идентифицироваться по имени тега
        #                                      V
        result = self.eval_expr(expression, tag_name)

        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            log.warning(u'''ВНИМАНИЕ! Все блоки кода вычисляемых тегов выполняются в контексте
        Memory узла. Поэтому все функции расчетов необходимо расмолагать
        в менеджере Memory Node.''')
        return None

    def read_value(self, address):
        """
        Чтение значения по адресу.
        @param address: Адрес значения в узле.
            В качестве адреса используется блок кода для вычисления значения тега.
        @return: Запрашиваемое значение или None в случае ошибки чтения.
        """
        return self.doExpression(address)

    def read_values(self, addresses):
        """
        Чтение значений по адресам.
        @param addresses: Список адресов значений в узле.
            В качестве адреса используется блок кода для вычисления значения тега.
        @return: Список запрашиваемых значений или None в случае ошибки чтения.
        """
        return [self.read_value(address) for address in addresses]

    def readTags(self, *tags):
        """
        Прочитать список тегов.
        @param tags: Список объектов тегов.
        @return: True/False.
        """
        if not tags:
            log.warning(u'Не определен список тегов для чтения')
            return False

        # Контроль что все теги соответствуют узлу
        is_my_tags_list = [tag.getNode().GetPassport() == self.GetPassport() for tag in tags]
        is_my_tags = all(is_my_tags_list)
        if not is_my_tags:
            not_my_tags = [tags[i].name for i, is_my_tag in enumerate(is_my_tags_list) if not is_my_tag]
            log.error(u'Не соответствие читаемых тегов %s Memory источнику данных' % not_my_tags)
            return False

        for tag in tags:
            # Все теги Memory узла являются вычисляемыми.
            # Выражение для вычисления записывается в 'address'
            expression = tag.GetResource().get('address', None)
            if not expression:
                log.warning(u'Не определена функция вычисляемого тега <%s> для определения значения' % tag.getName())
                value = None
            else:
                self.setEnv(TAG=tag)
                # log.debug(u'Обработка вычисляемого тега <%s>. Выражение <%s>' % (tag.getName(), expression))
                value = self.read_value(expression)
            tag.setCurValue(value)
        return True
