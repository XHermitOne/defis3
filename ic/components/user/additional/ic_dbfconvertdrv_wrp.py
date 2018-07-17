#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Драйвер конвертера данных из DBF файлов.

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

#import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.convert.icconvertdriver as icconvertdriver

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icDBFConvertDriver'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT':0}

#--- Спецификация на ресурсное описание класса ---
ic_class_spc = {'__events__': {}, 
                'child': [], 
                'type': 'DBFConvertDriver', 
                'name': 'default', 
                'activate':1,
                'init_expr':None,
                '_uuid':None,

                'dbf_file':None, #Имя DBF файла источника данных
                'dbf_field': None, #Имя поля DBF файла источника данных
                
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description','dbf_field'],
                                   },
                '__lists__':{
                    },
                '__parent__':icconvertdriver.SPC_IC_DBFCONVERTDRIVER, 
                }
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtODBC'
ic_class_pic2 = '@common.imgEdtODBC'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_dbfconvertdrv_wrp.icDBFConvertDriver-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['ConvertField']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,1)

class icDBFConvertDriver(icwidget.icSimple,icconvertdriver.icDBFConvertDriverPrototype):
    """
    Драйвер конвертера данных из DBF файлов.
    """
    #Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType = 0, evalSpace = None,
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
        icwidget.icSimple.__init__(self,parent,id,component,logType,evalSpace)
        icconvertdriver.icDBFConvertDriverPrototype.__init__(self,component)

