#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Таблица/Класс данных.
Класс пользовательского компонента Таблица/Класс данных.

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

import copy
import wx
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.db import icsqlalchemy
from ic.db import icdb
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.engine import glob_functions
from ic.log import log

from ic.components.user import ic_field_wrp

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icTable'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}


# --- Спецификация на ресурсное описание класса ---
def getBDNames():
    """
    Получить в спецификации список имен БД.
    """
    prj = glob_functions.getPrjRoot()
    if prj:
        return prj.getResNamesByTypes('src')
    return None


ic_class_spc = {'type': 'Table',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'scheme': None,
                'table': None,
                'import': None,
                'filter': None,
                'source': None,
                'idx': None,

                '__styles__': ic_class_styles,
                '__events__': {'init': (None, None, False),
                               'ctrl': (None, None, False),
                               'del': (None, None, False),
                               'post_init': (None, None, False),
                               'post_ctrl': (None, None, False),
                               'post_del': (None, None, False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['import', 'filter',
                                                            'description'],
                                   icDefInf.EDT_PY_SCRIPT: ['table'],
                                   icDefInf.EDT_USER_PROPERTY: ['source', 'scheme'],
                                   },

                '__parent__': icsqlalchemy.SPC_IC_TABLE,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTable'
ic_class_pic2 = '@common.imgEdtTable'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_tab_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Field', 'Link']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 5)

# ВНИМАНИЕ! Для таблиц хранения справочников создадим
# предварительно заполненную спецификацию
SPC_IC_NSI_TABLE = copy.deepcopy(ic_class_spc)
SPC_IC_NSI_TABLE['description'] = u'Таблица хранения справочника'
# Добавляем поля
ic_cod_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
ic_cod_field_spc['name'] = 'cod'
ic_cod_field_spc['description'] = u'Код справочника'
ic_cod_field_spc['label'] = u'Код'
ic_cod_field_spc['type_val'] = 'T'

ic_type_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
ic_type_field_spc['name'] = 'type'
ic_type_field_spc['description'] = u'Тип справочника'
ic_type_field_spc['label'] = u'Тип'
ic_type_field_spc['type_val'] = 'T'

ic_name_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
ic_name_field_spc['name'] = 'name'
ic_name_field_spc['description'] = u'Наименование'
ic_name_field_spc['label'] = u'Наименование'
ic_name_field_spc['type_val'] = 'T'

ic_count_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
ic_count_field_spc['name'] = 'count'
ic_count_field_spc['description'] = u'Количество ссылок на строку справочника'
ic_count_field_spc['label'] = u'Счетчик'
ic_count_field_spc['type_val'] = 'I'

ic_access_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
ic_access_field_spc['name'] = 'access'
ic_access_field_spc['description'] = u'Права доступа'
ic_access_field_spc['label'] = u'Доступ'
ic_access_field_spc['type_val'] = 'T'

#
SPC_IC_NSI_TABLE['child'] = [ic_cod_field_spc,
                             ic_type_field_spc,
                             ic_name_field_spc,
                             ic_count_field_spc,
                             ic_access_field_spc]

for i in range(1, 6):
    ic_s_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
    ic_s_field_spc['name'] = 's%d' % i
    ic_s_field_spc['description'] = u'Текстовое значение %d' % i
    ic_s_field_spc['label'] = u'S%d' % i
    ic_s_field_spc['type_val'] = 'T'
    SPC_IC_NSI_TABLE['child'].append(ic_s_field_spc)

for i in range(1, 6):
    ic_n_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
    ic_n_field_spc['name'] = 'n%d' % i
    ic_n_field_spc['description'] = u'Целое значение %d' % i
    ic_n_field_spc['label'] = u'N%d' % i
    ic_n_field_spc['type_val'] = 'I'
    SPC_IC_NSI_TABLE['child'].append(ic_n_field_spc)

for i in range(1, 6):
    ic_f_field_spc = copy.deepcopy(ic_field_wrp.ic_class_spc)
    ic_f_field_spc['name'] = 'function%d' % i
    ic_f_field_spc['description'] = u'Вещественное значение %d' % i
    ic_f_field_spc['label'] = u'F%d' % i
    ic_f_field_spc['type_val'] = 'F'
    SPC_IC_NSI_TABLE['child'].append(ic_f_field_spc)


# --- Функции редактирования ---
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('source', 'scheme'):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('source', 'scheme'):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            ctrl_types = list(icdb.DB_TYPES) + [icsqlalchemy.TABLE_TYPE, None]
            if ret[0][0] not in ctrl_types:
                dlgfunc.openWarningBox(u'ОШИБКА', u'Объект не БД типа.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('source', 'scheme'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icTable(icwidget.icSimple, icsqlalchemy.icSQLAlchemyDataClass):
    """
    Таблица.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента таблицы в режиме редактора ресурса.

        :param res:
        :param context:
        :param parent:
        :param arg:
        :param kwarg:
        :return:
        """
        import ic.components.user.objects.ictablebrows as brws
        log.info(u'Тестирование таблицы <%s>. Имя файла <%s>. Расширение <%s>' % (res['name'], parent._formName,
                                                                                  parent.file.split('.')[1]))
        cl = brws.TableBrows(None, parent._formName, parent.file.split('.')[1])
        win = cl.getObject()
        if win:
            win.Show(True)
            win.SetFocus()
        return
    
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
        icsqlalchemy.icSQLAlchemyDataClass.__init__(self, component, DB_=parent)
        self.countAttr('init_expr')

    def getAliasTableName(self):
        """
        Альтернативное имя таблицы.
        """
        tab_name = self.getICAttr('table')
        return self.name if tab_name is None else tab_name
