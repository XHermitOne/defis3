#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Сервер движка Cubes OLAP Framework.
"""

from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import util
from ic.utils import coderror
from ic.db import icdb

from ic.components import icwidget
from ic.PropertyEditor import icDefInf

from analitic.olap.cubes import cubes_olap_server

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icCubesOLAPServer'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'CubesOLAPServer',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'source': None,    # Паспорт объекта БД хранения OLAP кубов
                'ini_filename': None,     # Файл настройки OLAP сервера
                'model_filename': None,   # JSON Файл описания кубов OLAP сервера
                'exec': cubes_olap_server.DEFAULT_SLICER_EXEC,  # Файл запуска OLAP сервера
                'srv_path': None,     # Папка расположения файлов настроек OLAP сервера

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'ini_filename', 'model_filename', 'exec'],
                                   icDefInf.EDT_DIR: ['srv_path'],
                                   icDefInf.EDT_USER_PROPERTY: ['source'],
                                   },
                '__parent__': cubes_olap_server.SPC_IC_CUBESOLAPSERVER,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('server_components.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('server_components.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Cube']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('source',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('source',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in icdb.DB_TYPES:
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является объектом БД.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('source',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icCubesOLAPServer(icwidget.icSimple,
                        cubes_olap_server.icCubesOLAPServerProto):
    """
    OLAP Сервер движка Cubes OLAP Framework.
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

        cubes_olap_server.icCubesOLAPServerProto.__init__(self)

