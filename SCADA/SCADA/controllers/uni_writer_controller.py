#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контроллер универсальной удаленной записи <Удаленная служба UniWriter>.

Этот контроллер используется для записи значений тегов
с помощью XML-RPC данных из службы UniWriter.
"""

import xmlrpc.client

from ic.log import log

# Version
__version__ = (0, 1, 1, 1)


# Используемый порт по умолчанию
DEFAULT_PORT = 8081

# Имена используемых узлов
OPC_SERVER_NODE = 'OPC_SERVER_NODE'
# OPC_SERVER_NODE = 'OPC_DA'

# Поддерживаемые типы тегов
INT2_TAG_TYPE = 'int2'
INT4_TAG_TYPE = 'int4'
STRING_TAG_TYPE = 'string'
BOOL_TAG_TYPE = 'bool'
TAG_TYPES = (INT2_TAG_TYPE, INT4_TAG_TYPE, STRING_TAG_TYPE, BOOL_TAG_TYPE)


class icUniWriterControllerProto(object):
    """
    Контроллер универсальной удаленной записи <Удаленная служба UniWriter>.
    """
    def __init__(self, host=None, port=DEFAULT_PORT, server=None, node=None, *args, **kwargs):
        """
        Конструктор.

        :param host: Компьютер с сервером
        :param port: Порт сервера. По умолчанию используется 8081.
        :param server: Имя сервера.
        :param node: Наименования узла.
        """
        self.host = host
        self.port = port
        self.server = server
        self.node = node
    
    def write_tags(self, host=None, port=DEFAULT_PORT, server=None, node=None, **tags):
        """
        Запись данных в UniWriter сервер. С помощью XML RPC.

        :param host: Компьютер с сервером
        :param port: Порт сервера. По умолчанию используется 8081.
        :param server: Имя сервера.
        :param node: Наименования узла.
        :param tags: Словарь записываемых тегов.
            {'имя_тега': ('Адрес_тега', Значение_тега, 'Тип_тега'), ...}
        :return: True - запись прошла успешно / False - ошибка записи данных.
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
            
        return self._write_data_xmlrpc(host, port, server, node, **tags)
    
    def _write_data_xmlrpc(self, host, port, server, node, **tags):
        """
        Запись данных в UniWriter сервер. С помощью XML RPC.

        :param host: Компьютер с сервером
        :param port: Порт сервера. По умолчанию используется 8080.
        :param opc_server: Имя сервера.
        :param node: Наименования узла.
        :param tags: Словарь записываемых тегов.
            {'имя_тега': ('Адрес_тега', Значение_тега, 'Тип_тега'), ...}
        :return: True - запись прошла успешно / False - ошибка записи данных.
        """
        tag_items = tags.items()
        address_value_list = [tag_data for tag_name, tag_data in tag_items]
        check_types = all([isinstance(tag_data, (list, tuple)) and len(tag_data) >= 2 for tag_data in address_value_list])
        if not check_types:
            log.warning(u'Не корректные данные записываемых тегов')
            log.warning(u'Словарь записываемых тегов задается как {\'имя_тега\': (\'Адрес_тега\', Значение_тега, \'Тип_тега\'), ...}')
            return False
        tag_names = [tag_name for tag_name, tag_addr in tag_items]

        try:
            # Создание клиента OPC
            opc = xmlrpc.client.ServerProxy('http://%s:%d' % (host, port))

            results = list()
            for address, field in address_value_list:
                if len(field) >= 3:
                    address = field[0]
                    value = field[1]
                    tag_type = field[2]
                else:
                    address = field[0]
                    value = field[1]
                    tag_type = None

                if tag_type == INT2_TAG_TYPE:
                    result = opc.destinations.WriteValueAsInt2(node, server, address, int(value))
                elif tag_type == INT4_TAG_TYPE:
                    result = opc.destinations.WriteValueAsInt4(node, server, address, int(value))
                elif isinstance(value, int):
                    # По умолчанию целое число - 2-х байтовое
                    result = opc.destinations.WriteValueAsInt2(node, server, address, int(value))
                elif isinstance(value, bool) or tag_type == BOOL_TAG_TYPE:
                    result = opc.destinations.WriteValueAsBoolean(node, server, address,
                                                                  eval(value) if isinstance(value, str) else bool(value))
                elif isinstance(value, str) or tag_type == STRING_TAG_TYPE:
                    result = opc.destinations.ReadValuesAsStrings(node, server, address, str(value))
                else:
                    log.warning(u'UniWriter. Не поддерживаемый тип тегов <%s : %s>' % (tag_type, type(value)))
                    result = False
                results.append(result)

            return all(results)
        except:
            # Ошибка
            log.fatal(u'UniWriter. Ошибка записи данных сервера <%s:%d / %s>' % (host, port, server))
        return False
