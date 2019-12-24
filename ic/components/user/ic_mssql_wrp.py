#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
БД MSSQL.
Класс пользовательского компонента БД MSSQL.

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

import wx

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

from ic.utils import toolfunc

from ic.db import icdb

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icMSSQL'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': icdb.MSSQL_DB_TYPE,
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                
                'user': '',
                'dbname': '',
                'password': '',
                'host': '',
                'encoding': 'UTF-8',
                'convert_unicode': False,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'encoding': toolfunc.get_encodings_list(),
                              },
                            
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 
                                                            'user', 'dbname',
                                                            'password', 'host'],
                                   icDefInf.EDT_CHOICE: ['encoding'],
                                   icDefInf.EDT_CHECK_BOX: ['convert_unicode'],
                                   },
                '__parent__': icdb.SPC_IC_MSSQL,
                '__attr_hlp__': {'user': u'Имя пльзователя',
                                 'dbname': u'Имя БД',
                                 'password': u'Пароль',
                                 'host': u'Сервер БД',
                                 'encoding': u'Кодировка БД',
                                 'convert_unicode': u'Автоматическое преобразование в UNICODE?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMSSQL'
ic_class_pic2 = '@common.imgEdtMSSQL'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_mssql_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icMSSQL(icwidget.icSimple, icdb.icSQLAlchemyDB):
    """
    БД MSSQL.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно
        :type id: C{int}
        :param id: Идентификатор окна
        :type component: C{dictionary}
        :param component: Словарь описания компонента
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
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
        icdb.icSQLAlchemyDB.__init__(self, component)
