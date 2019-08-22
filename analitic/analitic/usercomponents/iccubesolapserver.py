#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Сервер движка Cubes OLAP Framework.
"""

import os.path

from ic.log import log
from ic.bitmap import bmpfunc
from ic.dlg import ic_dlg
from ic.utils import util
from ic.utils import coderror
from ic.db import icdb
from ic.utils import ic_file

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.components import icResourceParser as prs

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
                'exec': cubes_olap_server.ALTER_SLICER_EXEC,  # Файл запуска OLAP сервера
                'srv_path': None,     # Папка расположения файлов настроек OLAP сервера

                'log_filename': None,   # Путь до файла журнала
                'log_level': 'info',  # Уровень журналирования
                'host': 'localhost',  # Хост сервера
                'port': 5000,  # Порт сервера
                'reload': True,  #
                'prettyprint': True,  # Демонстрационные цели
                'allow_cors_origin': '*',   # Заголовок совместного использования ресурсов. Другие
                                            # связанные заголовки также добавляются, если эта опция присутствует.

                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'ini_filename', 'model_filename', 'exec',
                                                            'host', 'allow_cors_origin'],
                                   icDefInf.EDT_DIR: ['srv_path'],
                                   icDefInf.EDT_USER_PROPERTY: ['source'],
                                   icDefInf.EDT_FILE: ['log_filename'],
                                   icDefInf.EDT_TEXTLIST: ['log_level'],
                                   icDefInf.EDT_NUMBER: ['port'],
                                   icDefInf.EDT_CHECK_BOX: ['active', 'reload', 'prettyprint']
                                   },
                '__parent__': cubes_olap_server.SPC_IC_CUBESOLAPSERVER,
                '__lists__': {'log_level': cubes_olap_server.LOG_LEVELS,
                              },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('server_components.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('server_components.png')

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

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента OLAP Сервер движка Cubes в режиме редактора ресурса.
        @param res:
        @param context:
        @param parent:
        @param arg:
        @param kwarg:
        @return:
        """
        import ic
        from ..olap.cubes import cubes_olap_srv_test_dialog
        log.info(u'Тестирование OLAP Сервер движка Cubes <%s>. Имя файла <%s>. Расширение <%s>' % (res['name'], parent._formName,
                                                                                                   parent.file.split('.')[1]))

        olap_srv = ic.getKernel().createObjBySpc(parent=None, res=res, context=context)
        # olap_srv.run()
        cubes_olap_srv_test_dialog.show_cubes_olap_srv_test_dlg(parent=None, olap_srv=olap_srv)

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

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return self.getICAttr('source')

    def getDB(self):
        """
        Объект БД.
        """
        if self._db is None:
            db_psp = self.getDBPsp()
            if db_psp:
                kernel = self.GetKernel()
                self._db = kernel.Create(db_psp)
            else:
                log.warning(u'Не определен объект БД в <%s>' % self.getName())
        return self._db

    def getSrvPath(self):
        """
        Папка расположения файлов настроек OLAP сервера.
        """
        srv_path = self.getICAttr('srv_path')
        if not srv_path:
            srv_path = os.path.join(cubes_olap_server.DEFAULT_OLAP_SERVER_DIRNAME, self.getName())
        if srv_path and not os.path.exists(srv_path):
            # Создать папку
            ic_file.makeDirs(srv_path)
        return srv_path

    def getINIFileName(self):
        """
        Имя настроечного файла.
        """
        if not self._ini_filename:
            ini_base_filename = self.getICAttr('ini_filename')
            srv_path = self.getSrvPath()
            self._ini_filename = os.path.join(srv_path if srv_path else os.path.join(cubes_olap_server.DEFAULT_OLAP_SERVER_DIRNAME,
                                                                                     self.getName()),
                                              ini_base_filename if ini_base_filename else cubes_olap_server.DEFAULT_INI_FILENAME)
        return self._ini_filename

    def getModelFileName(self):
        """
        Имя файла описания кубов.
        """
        if not self._model_filename:
            model_base_filename = self.getICAttr('model_filename')
            srv_path = self.getSrvPath()
            self._model_filename = os.path.join(srv_path if srv_path else os.path.join(cubes_olap_server.DEFAULT_OLAP_SERVER_DIRNAME,
                                                                                       self.getName()),
                                                model_base_filename if model_base_filename else cubes_olap_server.DEFAULT_MODEL_FILENAME)
        return self._model_filename

    def getLogFileName(self):
        """
        Путь до файла журнала.
        """
        return self.getICAttr('log_filename')

    def getLogLevel(self):
        """
        Уровень журналирования.
        """
        return self.getICAttr('log_level')

    def getHost(self):
        """
        Хост сервера.
        """
        return self.getICAttr('host')

    def getPort(self):
        """
        Порт сервера.
        """
        return self.getICAttr('port')

    def isReload(self):
        """
        """
        return self.getICAttr('reload')

    def isPrettyPrint(self):
        """
        Демонстрационные цели.
        """
        return self.getICAttr('prettyprint')

    def getAllowCorsOrigin(self):
        """
        Заголовок совместного использования ресурсов.
        Другие связанные заголовки также добавляются,
        если эта опция присутствует.
        """
        return self.getICAttr('allow_cors_origin')

    def getExec(self):
        """
        Файл запуска OLAP сервера.
        """
        return self.getICAttr('exec')

    def getCubes(self):
        """
        Список объектов кубов OLAP сервера.
        """
        return self.component_lst
