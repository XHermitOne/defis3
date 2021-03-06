#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент контроллера универсальной удаленной
записи <Удаленная служба UniWriter>.

Этот контроллер используется для записи значений тегов
с помощью XML-RPC данных из службы UniWriter.
"""

from ic.log import log

from ic.components import icwidget

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.bitmap import bmpfunc

from SCADA.controllers import uni_writer_controller

# Поддерживаемые сервера
RSLINX_SERVER = u'RSLinx OPC Server'
LOGIKA_DA_SERVER = u'Logika.DA.2'
SERVERS = (RSLINX_SERVER, LOGIKA_DA_SERVER)

# Имена используемых узлов
OPC_SERVER_NODE = 'OPC_SERVER_NODE'
OPC_DA_NODE = 'OPC_DA'
NODES = (OPC_SERVER_NODE, OPC_DA_NODE)

# --- Спецификация ---
SPC_IC_UNI_WRITER_CTRL = {'host': u'',
                          'port': uni_writer_controller.DEFAULT_PORT,
                          'server': RSLINX_SERVER,
                          'node': OPC_SERVER_NODE,
                          'tags': None,
                          '__parent__': icwidget.SPC_IC_SIMPLE,
                          '__attr_hlp__': {'host': u'Хост',
                                           'port': u'Порт',
                                           'server': u'Имя сервера подключения',
                                           'node': u'Имя узла подключания',
                                           'tags': u'Словарь значений тегов с адресами и типами',
                                           },
                          }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icUniWriterController'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'UniWriterController',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                'host': u'',
                'port': uni_writer_controller.DEFAULT_PORT,
                'server': RSLINX_SERVER,
                'node': OPC_SERVER_NODE,
                'tags': None,

                '__events__': {},
                '__lists__': {'server': list(SERVERS),
                              'node': list(NODES),
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_NUMBER: ['port'],
                                   icDefInf.EDT_CHOICE: ['server', 'node'],
                                   icDefInf.EDT_DICT: ['tags'],
                                   },
                '__parent__': SPC_IC_UNI_WRITER_CTRL,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('server--pencil.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('server--pencil.png')

#   Путь до файла документации
ic_class_doc = 'SCADA/doc/_build/html/SCADA.usercomponents.uni_writer_ctrl.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icUniWriterController(icwidget.icSimple,
                            uni_writer_controller.icUniWriterControllerProto):
    """
    Компонент контроллера универсальной удаленной
    записи <Удаленная служба UniWriter>.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        """
        Функция тестирования компонента в режиме редактора ресурса.

        :param res:
        :param context:
        :param parent:
        :param arg:
        :param kwarg:
        :return:
        """
        # import ic
        # from SCADA.controllers import test_uni_reader_ctrl_dlg
        log.info(u'Тестирование контроллера <%s>. Имя файла <%s>. Расширение <%s>' % (res['name'], parent._formName,
                                                                                      parent.file.split('.')[1]))
        # controller = ic.getKernel().createObjBySpc(None, res, context=context)
        # test_uni_reader_ctrl_dlg.view_test_uni_reader_ctrl_dlg(parent=None, controller=controller)

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        host = self.getHost()
        port = self.getPort()
        server = self.getServer()
        node = self.getNode()
        uni_writer_controller.icUniWriterControllerProto.__init__(self, host=host, port=port,
                                                                  server=server, node=node)

    def getHost(self):
        """
        Хост.
        """
        return self.getICAttr('host')

    def getPort(self):
        """
        Порт.
        """
        return self.getICAttr('port')

    def getServer(self):
        """
        Сервер.
        """
        # log.info(u'\tResource server attr: %s' % self.resource['server'])
        return self.getICAttr('server')

    def getNode(self):
        """
        Узел.
        """
        # log.info(u'\tResource node attr: %s' % self.resource['node'])
        return self.getICAttr('node')

    def getTags(self):
        """
        Словарь тегов в формате:
            {'имя_тега': ('Адрес_тега', Значение_тега, 'Тип_тега'), ...}
        """
        return self.getICAttr('tags')

    def print_connection_param(self):
        """
        Вывести параметры связи с UniWriter Gateway.
        """
        log.info(u'UniWriter. Параметры связи <%s>' % self.getName())
        log.info(u'\tХост <%s>' % self.host)
        log.info(u'\tПорт <%s>' % self.port)
        log.info(u'\tУзел <%s>' % self.node)
        log.info(u'\tСервер <%s>' % self.server)
