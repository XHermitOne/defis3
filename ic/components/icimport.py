#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит описпние класс icImport. Используется для импорта модулей и визуальных
объектов в форму.

@type SPC_IC_IMPORT: C{dictionary}
@var SPC_IC_IMPORT: Спецификация на ресурсное описание класси icImport.
    
    Описание ключей SPC_IC_IMPORT:
    - B{type='Import'}: Тип компонента.
    - B{name='imp'}: Имя компонента.
    - B{init_expr=None}: Выражение, выполняемое после импортирования имен.
    - B{object=None}: Импортируемый визуальный объект. Объкт должен быть наследником
        от wx.Windows.
    - B{modules={}}: [depricated] Словарь импортируемых имен. Пример:{'ic.db':['ic_base', 'icdataset'], 'util':['*']}
"""

import wx
import ic.utils.util as util
from . import icwidget
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_IMPORT = {'type': 'Import',
                 'name': 'imp',
                 'object': None,
                 'init_expr': None,
                 'modules': {},
                 '__attr_types__': {icDefInf.EDT_TEXTDICT: ['modules'],
                                    },
                 '__parent__': icwidget.SPC_IC_BASE,
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icServiceType

#   Имя пользовательского класса
ic_class_name = 'icImport'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_IMPORT
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImport'
ic_class_pic2 = '@common.imgEdtImport'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icimport.icImport-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 4)


class icImport(icwidget.icBase):
    """
    Объект, описания импортируемых модулей. depricated.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, isDebug=False):
        """
        Конструктор для создания объекта icImport.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        util.icSpcDefStruct(SPC_IC_IMPORT, component)
        self.object = component['object']
        icwidget.icBase.__init__(self, parent, id, component, logType, evalSpace)
        #   Импорьтруем модули
        util.ic_import(component['modules'], evalSpace, isDebug)
        #   Указатель на импортируемый объект
        self._object = None
        if self.object:
            ret, obj = self.eval_attr('object')
            if ret and obj:
                self._object = obj
                if type not in dir(obj):
                    obj.type = type(obj)
                
                obj.name = self.name
                obj.size = self.size
                obj.position = self.position
                obj.span = self.span
                obj.border = self.border
                obj.flag = self.flag
                obj.proportion = self.proportion
                if not issubclass(obj.__class__, icwidget.icSimple):
                    obj.resource = self.resource
            
    def GetObject(self):
        """
        Возыращает импортируемый объект.
        """
        return self._object
