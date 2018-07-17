#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Конвертер табличного представления.

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

from ic.kernel import io_prnt

import ic.convert.icconvertquery as icconvertquery


#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icConvertQuery'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': icconvertquery.CONVERTQUERY_TYPE,
                'name': 'default', 
                'activate': True,
                'init_expr': None,

                'driver': None,  # Драйвер доступа к данным
                'auto_clear': True,  # Автоматическое очищение результирующей таблицы

                '_uuid': None,
                'child': [],
                '__events__': {},
                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description',
                                                            'driver'],
                                   icDefInf.EDT_CHECK_BOX: ['auto_clear'],
                                   },
                '__lists__': {},
                '__parent__': icconvertquery.SPC_IC_CONVERTQUERY,
                '__attr_hlp__': {'driver': u'Драйвер доступа к данным',
                                 'auto_clear': u'Автоматическое очищение результирующей таблицы',
                                 },
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtQuery'
ic_class_pic2 = '@common.imgEdtQuery'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_convertquery_wrp.icConvertQuery-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['ConvertField', 'DBFConvertDriver']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icConvertQuery(icwidget.icSimple, icconvertquery.icConvertQueryPrototype):
    """
    Конвертер табличного представления.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
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
        icconvertquery.icConvertQueryPrototype.__init__(self, component)
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getDriverName(self):
        """
        Имя драйвера источника данных.
        """
        return self.getICAttr('driver')

    def getDriver(self):
        """
        Объект драйвера источника данных.
        """
        try:
            driver_name = self.getDriverName()
            if driver_name:
                return self.components[driver_name]
        except:
            io_prnt.outErr(u'Не определен драйвер источника данных в объекте %s' % self.getName())
        return None
        
    def getFirstField(self):
        """
        Первое поле.
        """
        first_field_name = None
        for field in self.resource['child']:
            if field['type'] == 'ConvertField':
                first_field_name = field['name']
                break
                
        if first_field_name:
            return self.components[first_field_name]
            
        return None

    def getFields(self):
        """
        Список полей.
        """
        return [self.components[field_name] for field_name in [fld_spc['name'] for fld_spc in [field_spc for field_spc in self.resource['child'] if field_spc['type'] == 'ConvertField']]]
