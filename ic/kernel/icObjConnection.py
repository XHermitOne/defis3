#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Описание связей между объектами системы.
"""

__version__ = (0, 1, 1, 1)


class icConnection:
    """
    Базовый класс описания соединений между объектами.
    """

    def __init__(self, src, slotLst, func_trans=None, *arg, **kwarg):
        """
        Конструктор.
        
        :type src: C{icSignalSrc}
        :param src: Источник сигнала.
        :type slotLst: C{list | tuple}
        :param slotLst: Список слотов.
        :type func_trans: C{function}
        :param func_trans: Функция преобразования сигналов.
        """
        self.src = src
        self.slotLst = slotLst
        self._func = func_trans
        self.init_connection()

    def getSlotLst(self):
        """
        Возвращает список слотов соединения.
        """
        return self.slotLst

    def getSrc(self):
        """
        Возвращает список источников соединения.
        """
        return self.src
        
    def init_connection(self):
        """
        """
        pass

    def isListener(self, passport):
        """
        Возвращает признак того, что объект, обладающий опрделенным набором
        идентификаторов (паспортом) прописан в качестве приемника соединения.
        
        :type passport: C{icObjectPassport}
        :param passport: Паспорт объекта.
        """
        for sign in self.slotLst:
            if sign.passport == passport:
                return True
                
        return False
        
    def isValidSignal(self, signal):
        """
        Проверка соответствия сигнала соединению.
        """
        if self.src.get_signal_type() == signal.get_signal_type():
            return True
                
        return False
        
    def generate(self, event):
        """
        """
        
    def output_signal(self, signal):
        """
        Функция передачи сигнала - преобразование сигнала на соединении.
        """
        pass


class icDirectConnection(icConnection):
    """
    Класс прямого соединения минуя ядро системы.
    """

    def init_connection(self):
        """
        Инициализация соединения.
        """
        pass


def test():
    pass


if __name__ == '__main__':
    test()
