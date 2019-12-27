#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Связь сигнально-слотной системы.
Класс пользовательского компонента СВЯЗЬ СИГНАЛЬНО-СЛОТНОЙ СИСТЕМЫ.

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

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
from ic.engine import glob_functions
from ic.log import log

import ic.kernel.icObjConnection as parentModule

# --- Спецификация ---
SPC_IC_CONNECTION = {'__parent__': icwidget.SPC_IC_SIMPLE,
                     }
    
# --- Описание компонента для редактора ресурса ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icConnection'

#   Описание стилей компонента
ic_class_styles = None

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'Connection',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type']},

                '__parent__': SPC_IC_CONNECTION,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtConnection'
ic_class_pic2 = '@common.imgEdtConnection'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['WxSignal', 'ChangeAttrSignal', 'PostFuncSignal', 'SimpleSlot']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icConnection(icwidget.icSimple, parentModule.icConnection):
    """
    Описание пользовательского компонента СВЯЗЬ СИГНАЛЬНО-СЛОТНОЙ СИСТЕМЫ.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

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

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        # ВНИМАНИЕ!!! Сначала нужно создать все сигналы и слоты
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        first_signal = None
        try:
            signals = [signal for signal in self.components.values() if signal.type in ('WxSignal', 'ChangeAttrSignal', 'PostFuncSignal')]
            first_signal = signals[0]
        except IndexError:
            log.warning(u'Соединение <%s> не имеет сигналов' % self.name)
        slot_list = [item for item in self.components.values() if item.type in ('SimpleSlot',)]
        if not slot_list:
            log.warning(u'Соединение <%s> не имеет слотов' % self.name)
            
        parentModule.icConnection.__init__(self, first_signal, slot_list)

        # Регистрируем соединение через ядро
        kernel = glob_functions.getEngine()
        if kernel:
            log.info(u'>>> Регистрируем соединение first_signal = <%s>, slot_list = <%s>' % (first_signal,
                                                                                             slot_list))
            kernel.add_connection_lst([self])
        else:
            log.warning(u'Ядро системы не инициализировано')

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
