#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Сигнал сигнально-слотной событийной системы.
Класс пользовательского компонента СИГНАЛ СИГНАЛЬНО-СЛОТНОЙ СОБЫТИЙНОЙ СИСТЕМЫ.
Подается при смене значения атрибута.

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

import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.kernel import icobject
import ic.kernel.icsignalsrc as parentModule


# --- Спецификация ---
SPC_IC_CHANGEATTRSIGNAL = {'class_name': None,  # Имя класса объекта-источника
                           'obj_name': None,    # Имя объекта-источника
                           'res_name': None,    # Имя ресурса, где описан объект-источника
                           'sub_sys': None,     # Подсистема, в которой описан ресурс объекта-источника
                           'args': None,        # Кортеж дополнительных аргументов
                           'attr_name': None,   # Имя изменяемого атрибута
                           '__parent__': icwidget.SPC_IC_SIMPLE,
                           '__attr_hlp__': {'class_name': u'Имя класса объекта-источника',
                                            'obj_name': u'Имя объекта-источника',
                                            'res_name': u'Имя ресурса, где описан объект-источника',
                                            'sub_sys': u'Подсистема, в которой описан ресурс объекта-источника',
                                            'args': u'Кортеж дополнительных аргументов',
                                            'attr_name': u'Имя изменяемого атрибута',
                                            },
                           }
    
# --- Описание компонента для редактора ресурса ---

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icChangeAttrSignal'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ChangeAttrSignal',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                '__events__': {},
                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'class_name', 'obj_name',
                                                            'res_name', 'sub_sys', 'attr_name'],
                                   icDefInf.EDT_TEXTLIST: ['args'],
                                   },

                '__parent__': SPC_IC_CHANGEATTRSIGNAL,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtSignal'
ic_class_pic2 = '@common.imgEdtSignal'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icChangeAttrSignal(icwidget.icSimple,parentModule.icChangedAttrSrc):
    """
    Описание пользовательского компонента СИГНАЛ СИГНАЛЬНО-СЛОТНОЙ СОБЫТИЙНОЙ СИСТЕМЫ.
    Подается при смене значения атрибута.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

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

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') <> 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.

        # Создать паспорт объекта-источника
        pasport = icobject.icObjectPasport((self.class_name, self.obj_name, self.res_name, self.sub_sys))

        parentModule.icChangedAttrSrc.__init__(self, pasport, self.eval_attr('attr_name'))

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий
