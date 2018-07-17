#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Абстрактный класс тега SCADA системы.
"""

from ic.log import log
from ic.components import icwidget

__version__ = (0, 0, 1, 1)

# --- Спецификация ---
# Типы данных тега
INT_TAG_TYPE = 'IntSCADATag'
FLOAT_TAG_TYPE = 'FloatSCADATag'
STR_TAG_TYPE = 'StrSCADATag'
DT_TAG_TYPE = 'DateTimeSCADATag'
TAG_TYPES = (INT_TAG_TYPE, FLOAT_TAG_TYPE, STR_TAG_TYPE, DT_TAG_TYPE)

SPC_IC_SCADA_TAG = {'node': None,
                    'scan_class': None,

                    'address': '',

                    '__parent__': icwidget.SPC_IC_SIMPLE,

                    '__attr_hlp__': {'node': u'Узел-источник данных',
                                     'scan_class': u'Класс сканирования',
                                     'address': u'Адрес в контроллере/узле SCADA',
                                     },
                    }


class icSCADATagProto(object):
    """
    Абстрактный класс тега SCADA системы.
    """
    def __init__(self, *args, **kwargs):
        """
        Контсруктор.
        """
        # Объект узла-источника данных SCADA.
        self._node = None

        # Объект класса сканирования данных SCADA.
        self._scan_class = None

        # Текущее значение тега
        self._cur_value = None

        # Предыдущее значение тега
        # Для анализа скорости изменения значения
        self._prev_value = None

    def readValue(self):
        """
        Прочитать из узла-источника данных SCADA текущее значение тега.
        @return: Текущее значение тега.
        """

        node = self.getNode()
        if node:
            address = self.getAddress()
            new_value = node.read_value(address)
            if new_value:
                self.setCurValue(new_value)
            # else:
            #     log.warning(u'Ошибка чтения значения SCADA тега <%s>' % self.name)
        return self._cur_value

    def getCurValue(self, do_read=False):
        """
        Текущее значение тега.
        @param do_read: Произвести автоматическое чтение из источника данных?
        @return: Текущее значение тега.
        """
        if do_read:
            self.readValue()
        return self.normValueOut(self._cur_value)

    # Другое наименование метода
    def getValue(self):
        """
        Текущее значение тега.
        """
        return self.getCurValue()

    def setCurValue(self, value):
        """
        Установить текущее значение тега.
        @param value: Текущее значение тега.
        @return: True/False.
        """
        # Переместить текущее значение в предыдущее
        self._prev_value = self._cur_value
        # Обновить текущее значение
        self._cur_value = self.normValueInto(value)
        return True

    # Другое наименование метода
    def setValue(self, value):
        """
        Текущее значение тега.
        """
        return self.setCurValue(value)

    def normValueInto(self, value):
        """
        Преобразование типа значения для установки внутреннего значения.
        @param value: Текущее значение тега.
        @return: Преобразованное значение.
        """
        return value

    def normValueOut(self, value):
        """
        Преобразование типа значения для получения из внутреннего значения.
        @param value: Текущее значение тега.
        @return: Преобразованное значение.
        """
        return value

    def getPrevValue(self):
        """
        Предыдущее значение тега.
        @return: Предыдущее значение тега.
        """
        return self._prev_value

    def getNodePsp(self):
        """
        Паспорт узла-источника данных SCADA.
        @return: Паспорт или None в случае ошибки.
        """
        log.error(u'Функция getNodePsp не реализована в <%s>' % self.__class__.__name__)
        return None

    def getNode(self, node_psp=None):
        """
        Объект узла-источника данных SCADA.
        @param node_psp: Паспорт узла-источника данных SCADA.
            Если не определено, то задается функцией self.getNodePsp.
        @return: Объект узла-источника данных SCADA или
            None в случае ошибки.
        """
        log.error(u'Функция getNode не реализована в <%s>' % self.__class__.__name__)
        return None

    def getScanClassPsp(self):
        """
        Паспорт класса сканирования данных SCADA.
        @return: Паспорт или None в случае ошибки.
        """
        log.error(u'Функция getScanClassPsp не реализована в <%s>' % self.__class__.__name__)
        return None

    def getScanClass(self, scan_class_psp=None):
        """
        Объект класса сканирования данных SCADA.
        @param scan_class_psp: Паспорт класса сканирования данных SCADA.
            Если не определено, то задается функцией self.getScanClassPsp.
        @return: Объект класса сканирования данных SCADA или
            None в случае ошибки.
        """
        return None

    def getAddress(self):
        """
        Адрес в источнике данных/контроллере/узле SCADA.
        """
        return None
