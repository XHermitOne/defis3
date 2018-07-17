#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контроллер универсального удаленного чтения <Удаленная служба UniReader>.

Этот контроллер используется для чтения
с помощью XML-RPC данных из службы UniReader.
"""

import xmlrpclib

from ic.log import log

# Version
__version__ = (0, 0, 1, 1)


# Используемый порт по умолчанию
DEFAULT_PORT = 8080

# Имена используемых узлов
OPC_SERVER_NODE = 'OPC_SERVER_NODE'


class icUniReaderControllerProto(object):
    """
    Контроллер универсального удаленного чтения <Удаленная служба UniReader>.
    """
    def __init__(self, host=None, port=DEFAULT_PORT, server=None, node=None, *args, **kwargs):
        """
        Конструктор.
        @param host: Компьютер с сервером
        @param port: Порт сервера. По умолчанию используется 8080.
        @param server: Имя сервера.
        @param node: Наименования узла.
        """
        self.host = host
        self.port = port
        self.server = server
        self.node = node
    
    def read_tags(self, host=None, port=DEFAULT_PORT, server=None, node=None, **tags):
        """
        Чтение данных из UniReader сервера. С помощью XML RPC.
        @param host: Компьютер с сервером
        @param port: Порт сервера. По умолчанию используется 8080.
        @param server: Имя сервера.
        @param node: Наименования узла.
        @param tags: Словарь запрашиваемых тегов.
        @return: Словарь тегов, заполненных данными.
        """
        if host is None:
            host = self.host
            
        if server is None:
            server = self.server
            
        if node is None:
            node = self.node
            
        if not host:
            log.warning(u'Не определен хост для подключения')
            return dict()
            
        if not server:
            log.warning(u'Не определено имя сервера')
            return dict()

        if not node:
            log.warning(u'Не определен узел')
            return dict()
            
        return self._read_data_xmlrpc(host, port, server, node, **tags)
    
    def _read_data_xmlrpc(self, host, port, server, node, **tags):
        """
        Чтение данных из UniReader сервера. С помощью XML RPC.
        @param host: Компьютер с сервером
        @param port: Порт сервера. По умолчанию используется 8080.
        @param opc_server: Имя сервера.
        @param node: Наименования узла.
        @param tags: Словарь запрашиваемых тегов.
        @return: Словарь тегов, заполненных данными.
        """
        tag_items = tags.items()
        addresses = [tag_addr for tag_name, tag_addr in tag_items]
        tag_names = [tag_name for tag_name, tag_addr in tag_items]

        try:
            # Создание клиента OPC
            opc = xmlrpclib.ServerProxy('http://%s:%d' % (host, port))
            values = opc.sources.ReadValuesAsStrings(node, server, *addresses)

            result = dict([(tag_name, values[i]) for i, tag_name in enumerate(tag_names)])
            return result
        except:
            # Ошибка
            log.fatal(u'Ошибка чтения данных сервера <%s:%d / %s>' % (host, port, server))
            # Скорее всего это ошибка связи с сервером
            return dict([(tag_name, u'') for tag_name in tag_names])
