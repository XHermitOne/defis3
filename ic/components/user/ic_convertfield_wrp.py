#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поле конвертера табличного представления.

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

from ic.convert import icconvertquery

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icConvertField'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': icconvertquery.CONVERTFIELD_TYPE,
                'name': 'default',
                'activate': True,
                'init_expr': None,

                'driver': None,     # Драйвер доступа к данным
                
                '_uuid': None,
                '__events__': {},
                '__styles__': ic_class_styles,
                '__lists__': {'store': ['', ''],
                              'type_val': ['T', 'D', 'I', 'F'],
                              'attr': [None, 0, 1, 2, 3],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description',
                                                            'label', 'dict', 'field'],
                                   icDefInf.EDT_NUMBER: ['len'],
                                   icDefInf.EDT_CHOICE: ['type_val', 'store',
                                                         'attr', 'idx'],
                                   },
                '__parent__': icconvertquery.SPC_IC_CONVERTFIELD,
                '__attr__hlp__': {'driver': u'Драйвер доступа к данным',
                                  },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtField'
ic_class_pic2 = '@common.imgEdtField'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_convertfield_wrp.icConvertField-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['DBFConvertDriver']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icConvertField(icwidget.icSimple,icconvertquery.icConvertFieldPrototype):
    """
    Поле конвертера табличного представления.
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
        icconvertquery.icConvertFieldPrototype.__init__(self, parent, component)

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
