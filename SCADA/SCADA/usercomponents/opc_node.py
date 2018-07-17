#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент OPC контроллера/узла SCADA системы.

Компонент работает ч/з библиотеку OpenOPC (http://openopc.sourceforge.net)
"""

from ic.log import log

try:
    import OpenOPC
except ImportError:
    log.fatal(u'SCADA OPC node. Import error <OpenOPC>')

from ic.components import icwidget

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.bitmap import ic_bmp

from . import node

# --- Спецификация ---
SPC_IC_OPC_NODE = {'host': '',
                   'opc_server': '',
                   'topic': '',

                   '__parent__': icwidget.SPC_IC_SIMPLE,

                   '__attr_hlp__': {'host': u'Компьютер с OPC сервером. Если не определен, то считается localhost',
                                    'opc_server': u'Имя OPC сервера',
                                    'topic': u'Топик',
                                    },
                   }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icOPCNode'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'OPCNode',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_PY_SCRIPT: ['host', 'opc_server', 'topic'],
                                   },
                '__parent__': SPC_IC_OPC_NODE,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('network-server.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('network-server.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 5)


class icOPCNode(icwidget.icSimple, node.icSCADANodeProto):
    """
    Компонент OPC контроллера/узла SCADA системы.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        # Компьютер с OPC сервером. Если не определен, то считается localhost.
        self._host = ''

        # Имя OPC сервера
        self._opc_server = ''

        # Топик
        self._topic = ''

    def is_localhost(self, host=None):
        """
        Проверка указан ли хост как localhost.
        @param host: Указанный хост.
        @return: True - localhost/False-нет.
        """
        return (not host) or (type(host) in (str, unicode) and host.lower().strip() in ('localhost', '127.0.0.1'))

    def connect(self, host=None, opc_server=None):
        """
        Создание объекта OPC клиента.
        @param host: Хост OPC сервера для возможности удаленного подключения (через DCOM) к OPC серверу.
            Если не определен, то берется из описания компонента.
        @param opc_server: Имя OPC сервера.
            Если не определен, то берется из описания компонента.
        @return: Объект OPC сервера.
        """
        if host is None:
            host = self.getHost()
        if opc_server is None:
            opc_server = self.getOPCServer()

        if type(host) not in (None.__class__, str, unicode):
            log.error(u'Не корректный тип хоста OPC сервера <%s>' % type(host))
            return None

        is_local_opc = self.is_localhost(host)
        if is_local_opc:
            log.info(u'OPC сервер находится локально')
            opc = OpenOPC.client()
        else:
            log.info(u'OPC сервер находится на <%s>' % host)
            opc = OpenOPC.open_client(host)

        if opc is None:
            log.error(u'Не возможно создать объект клиента OPC. Хост <%s>' % host)
            return None

        # Список серверов OPC
        servers = opc.servers()
        if opc_server not in servers:
            log.warning(u'Сервер <%s> не найден среди %s' % (opc_server, servers))
            self.disconnect(opc)
            return None

        # Соедиенение с сервером
        opc.connect(opc_server)

        return opc

    def disconnect(self, opc_client=None):
        """
        Закрыть соединение.
        @param opc_client: Объект OPC клиента.
        @return: True/False.
        """
        try:
            if opc_client:
                opc_client.close()
            return True
        except:
            log.fatal(u'Ошибка закрытия соединения с OPC сервером')
        return False

    def getHost(self):
        """
        Компьютер с OPC сервером. Если не определен, то считается localhost.
        """
        if not self._host:
            self._host = self.getICAttr('host')
        return self._host

    def getOPCServer(self):
        """
        Имя OPC сервера.
        """
        if not self._opc_server:
            self._opc_server = self.getICAttr('opc_server')
        return self._opc_server

    def getTopic(self):
        """
        Топик.
        """
        if not self._topic:
            topic = self.getICAttr('topic')
            topic = topic.strip()

            # Проверка наличия обрамляющих сигнатур топика
            if node.DO_CONTROL_TOPIC_SIGNATURES:
                if not topic.startswith(node.TOPIC_BEGIN_SIGNATURE):
                    topic = node.TOPIC_BEGIN_SIGNATURE + topic
                if not topic.endswith(node.TOPIC_END_SIGNATURE):
                    topic = topic + node.TOPIC_END_SIGNATURE

            self._topic = topic
        return self._topic

    def read_value(self, address):
        """
        Чтение значения по адресу.
        @param address: Адрес значения в узле.
        @return: Запрашиваемое значение или None в случае ошибки чтения.
        """
        opc = None

        opc_host = self.getHost()
        opc_server = self.getOPCServer()
        topic = self.getTopic()

        try:
            # Создание клиента OPC
            opc = self.connect(opc_host)
            if opc is None:
                return None

            # Прочитать из OPC сервера
            val = opc.read(address)
            result = val[0] if val and val[1] == 'Good' else None

            self.disconnect(opc)

            log.debug(u'Адрес <%s>. Результат чтения данных %s' % (address, result))
            return result
        except:
            self.disconnect()
            log.fatal(u'Ошибка чтения значения по адресу <%s> в <%s>' % (address, self.__class__.__name__))
        return None

    def read_values(self, addresses):
        """
        Чтение значений по адресам.
        @param addresses: Список адресов значений в узле.
        @return: Список запрашиваемых значений или None в случае ошибки чтения.
        """
        opc = None

        opc_host = self.getHost()
        opc_server = self.getOPCServer()
        topic = self.getTopic()

        try:
            # Создание клиента OPC
            opc = self.connect(opc_host)
            if opc is None:
                return None

            # Прочитать из OPC сервера
            values = opc.read(addresses)
            result = [val[1] if val and val[2] == 'Good' else None for val in values]

            self.disconnect(opc)

            log.debug(u'Адреса %s. Результат чтения данных %s' % (addresses, result))
            return result
        except:
            self.disconnect()
            log.fatal(u'Ошибка чтения значения по адресам %s в <%s>' % (addresses, self.__class__.__name__))
        return None

    def readTags(self, *tags):
        """
        Прочитать список тегов.
        @param tags: Список объектов тегов.
        @return: True/False.
        """
        if not tags:
            log.warning(u'Не определен список тегов для чтения')
            return False
        # else:
        #     log.debug(u'Чтение тегов %s из OPC <%s>' % (str(tags), self.getName()))

        # Контроль что все теги соответствуют узлу
        is_my_tags_list = [tag.getNode().GetPassport() == self.GetPassport() for tag in tags]
        is_my_tags = all(is_my_tags_list)
        if not is_my_tags:
            not_my_tags = [tags[i].name for i, is_my_tag in enumerate(is_my_tags_list) if not is_my_tag]
            log.error(u'Не соответствие читаемых тегов %s OPC источнику данных' % not_my_tags)
            return False

        topic = self.getTopic()
        addresses = [topic+tag.getAddress() for tag in tags]

        values = self.read_values(addresses)
        for i, value in enumerate(values):
            tags[i].setCurValue(value)
        return True

    # def write_value(self, address, value):
    #     """
    #     Запись значения по адресу.
    #     @param address: Адрес значения в узле.
    #     @param value: Записываемое значение.
    #     @return: True - запись прошла успешно/False - ошибка.
    #     """
    #     pass
