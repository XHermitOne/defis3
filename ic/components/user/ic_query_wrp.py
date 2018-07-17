#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SQL Запрос к БД.
Класс пользовательского компонента Запрос.

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

import wx
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.db import icsqlalchemy
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.imglib import common
from ic.PropertyEditor import icDefInf

from ic.db import icquery

from ic.log import log

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icQuery'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

SRC_EXT = '.src'


# --- Спецификация на ресурсное описание класса ---
def getBDNames():
    """
    Получить в спецификации список имен БД.
    """
    from ic.engine import ic_user
    prj = ic_user.getPrjRoot()
    if prj:
        return prj.getResNamesByTypes(SRC_EXT[1:])
    return None


ic_class_spc = {'type': icquery.QUERY_TYPE,
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'sql_txt': None,    # Текст прямого SQL запроса
                'source': None,     # Имя источника данных/БД

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_USER_PROPERTY: ['source'],
                                   },
                '__lists__': {},
                '__parent__': icquery.SPC_IC_QUERY,
                '__attr_hlp__': {'sql_txt': u'Текст прямого SQL запроса',
                                 'source': u'Имя источника данных/БД',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtQuery'
ic_class_pic2 = '@common.imgEdtQuery'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_query_wrp.icQuery-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Field']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


# --- Функции редактирования ---
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('source', ):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('source', ):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            ctrl_types = icsqlalchemy.DB_TYPES
            if ret[0][0] not in ctrl_types:
                ic_dlg.icWarningBox(u'ОШИБКА', u'Объект не БД типа.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('source',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icQuery(icwidget.icSimple, icquery.icQueryPrototype):
    """
    Запрос к источнику данных в табличном представлении.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента SQL запроса в режиме редактора ресурса.
        @param res:
        @param context:
        @param parent:
        @param arg:
        @param kwarg:
        @return:
        """
        import ic
        from ic.components.user.objects import view_sql_query_dlg
        log.info(u'Тестирование запроса <%s>. Имя файла <%s>. Расширение <%s>' % (res['name'], parent._formName,
                                                                                  parent.file.split('.')[1]))

        db = ic.getKernel().Create(res['source'])
        view_sql_query_dlg.view_sql_query_dlg(parent=None, db=db, sql_txt=res['sql_txt'])

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
        icquery.icQueryPrototype.__init__(self, component)
        self.countAttr('init_expr')

    def getDataSource(self):
        """
        Источник данных/БД.
        """
        if self.data_source is None:
            if self._data_src is None:
                log.warning(u'Не определен источник данных/БД запроса <%s>' % self.name)
                return None
            elif type(self._data_src) in (str, unicode):
                # Источник данных задается именем
                psp = ((None, self._data_src, None, self._data_src+SRC_EXT, None),)
                self.data_source = self.GetKernel().getObjectByPsp(psp)
            elif self.isPassport(self._data_src):
                # Источник данных задается паспортом
                self.data_source = self.GetKernel().getObjectByPsp(self._data_src)

        return self.data_source
