#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Описание сигнальной системы объектов, наследованных от icObject.
Основные идеи:
"""

from ic.utils import ic_uuid

class icSignal:
    """
    Базовый класс сигнала.
    """
    def __init__(self, passport, obj=None, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type passport: C{icObjectPassport}
        @param passport: Объект идентификации (паспорт) объекта источника сигнала.
        @type obj: C{icObject}
        @param obj: Объект - источник сигнала.
        """
        self.passport = passport
        # Объект, сгенерировавший сигнал
        self.obj = obj
        # Инициация сигнала
        self.init_signal()
        
    def get_signal_type(self):
        """
        Возвращает тип сигнала.
        """
        return self.__class__.__name__
        
    def getObject(self):
        """
        Возвращает указатель на объект, к который возбудил сигнал.
        """
        return self.obj
        
    def init_signal(self):
        """
        Функция инициации сигнала.
        """
        #   Генерируем uuid
        self.uuid = ic_uuid.get_uuid()
        #   Значение
        self.value = None
        #   Признак дальнейшей обработки сигнала.
        self._bSkip = True
        #   Тип сигнала
        self.type = self.__class__.__name__
        
    def isEq(self, other):
        """
        Эквивалентность сигналов.
        """
        return self.passport == other.passport and self.value == other.value
        
    def isEqType(self, other):
        """
        Определяется эквивалентность типов.
        """
        return self.__class__ == other.__class__
                
    def isSkip(self):
        """
        Возвращает признак дальнейшей обработки сигнала другими слотами.
        """
        return self._bSkip
        
    def Stop(self):
        """
        Останавливает последующую обработку сигнала диспетчером сигналов.
        """
        self._bSkip = False
        
    def Skip(self, val=True):
        """
        """
        self._bSkip = val


class icBeginTransactSignal(icSignal):
    """
    Сервисный сигнал - 'начать транзакцию'.
    """
    pass


class icRollBackTransactSignal(icSignal):
    """
    Откатить транзакцию.
    """
    pass


class icCommitTransackSignal(icSignal):
    """
    Сервисный сигнал - 'завершить транзакцию'.
    """
    pass


class icWxEvtSignal(icSignal):
    """
    Сигнал генерируемый на основе wx - события.
    """
    def __init__(self, passport, obj, evt, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type passport: C{icObjectPassport}
        @param passport: Объект идентификации (паспорт) объекта источника сигнала.
        """
        self.passport = passport
        #   Событие, которое сгенерировало сигнал (если оно было)
        self.event = evt

        # Инициация сигнала
        self.init_signal()
        #
        icSignal.__init__(self, passport, obj)

    def get_signal_type(self):
        """
        Возвращает тип сигнала.
        """
        return self.event.GetEventType()

    def Skip(self, val=True):
        """
        """
        self._bSkip = val


class icChangedAttrSignal(icSignal):
    """
    Уведомляющий сигнал о изменении атрибута объекта.
    """
    def __init__(self, passport, attr=None, value=None, obj=None, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type passport: C{icObjectPassport}
        @param passport: Объект идентификации (паспорт) объекта источника сигнала.
        @type attr: C{string}
        @param attr: Атрибут объекта.
        """
        # Инициация сигнала
        self.init_signal()
        #
        icSignal.__init__(self, passport, obj)

        self.attr = attr
        self.value = value

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'ChangedAttr', self.attr


class icPreFuncSignal(icSignal):
    """
    Сигнал уведомляет, что произошел вызов определнной функции объекта.
    """
    def __init__(self, obj, func_name, *arg, **kwarg):
        """
        Конструктор сигнала.

        @type obj: C{icObject}
        @param obj: Объект, сгенерировавший сигнал.
        @type func_name: C{string}
        @param func_name: Имя функции.
        """
        # Инициация сигнала
        self.init_signal()
        #
        icSignal.__init__(self, obj.GetPassport(), obj)
        # Имя функции
        self.func_name = func_name

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'PreFunction', self.func_name


class icPostFuncSignal(icSignal):
    """
    Сигнал уведомляет, что произошел выход из определнной функции объекта.
    """

    def __init__(self, obj, func_name, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type obj: C{icObject}
        @param obj: Объект, сгенерировавший сигнал.
        @type func_name: C{string}
        @param func_name: Имя функции.
        """
        # Инициация сигнала
        self.init_signal()
        #
        icSignal.__init__(self, obj.GetPassport(), obj)
        # Имя функции
        self.func_name = func_name

    def get_signal_type(self):
        """
        Возвращает тип возбуждаемого сигнала.
        """
        return 'PostFunction', self.func_name


class icInitObjectSignal(icSignal):
    """
    Уведомляющий сигнал о создании объекта.
    """
    def __init__(self, obj, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type obj: C{icObject}
        @param obj: Объект, инициировавший сигнал.
        """
        self.passport = obj.GetPassport()
        #   Указатель на объект, инициировавший сигнал
        self._object = obj
        
        # Инициация сигнала
        self.init_signal()
        icSignal.__init__(self, self.passport)


class icDelObjectSignal(icSignal):
    """
    Уведомляющий сигнал о удалении объекта.
    """

    def __init__(self, obj, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type obj: C{icObject}
        @param obj: Объект, инициировавший сигнал.
        """
        self.passport = obj.GetPassport()
        #   Указатель на объект, инициировавший сигнал
        self._object = obj
        
        # Инициация сигнала
        self.init_signal()
        icSignal.__init__(self, self.passport)


class icSlot:
    """
    Базовый класс слотов.
    """

    def __init__(self, passport, func, *arg, **kwarg):
        """
        Конструктор сигнала.
        
        @type passport: C{icObjectPassport}
        @param passport: Объект идентификации (паспорт) объекта приемника сигнала.
        """
        self.uuid = ic_uuid.get_uuid()
        self.passport = passport
        #   Указатель на объект, к которому прикреплен слот
        self._object = None
        #   Функция возбуждения
        self._func = func
        #   Признак активации слота
        self._bAcivated = True
        
        #
        self.init_slot()
        
    def activte(self, prz=True):
        """
        Активирует слот.
        """
        self._bAcivated = prz
        
    def getObject(self):
        """
        Возвращает указатель на объект, к которому прикреплен слот.
        """
        return self._object
    
    def GetPassportLinkObj(self):
        """
        Возвращает паспорт объекта, к которому прикреплен слот.
        """
        return self.passport
        
    def init_slot(self):
        """
        Инициализация слота.
        """
        pass
        
    def isActivated(self):
        """
        Возвращает признак активации слота.
        """
        return self._bAcivated
        
    def isValidSignal(self, signal):
        """
        Проверяет входной сигнал на соответствие типов.
        """
        return True
        
    def parse_signal(self, signal):
        """
        Обработка сигнала.
        """
        pass
        
    def setObject(self, obj):
        """
        Устанавливает указатель на объект, к которому прикреплен слот.
        """
        self._object = obj
        
    def SendSignal(self):
        """
        Возбуждение слотового сисгнала.
        """
        pass


class icSimpleSlot(icSlot):
    """
    Простой слот. После получения сигнала происходит выполнение функции возбуждения.
    """

    def parse_signal(self, signal):
        """
        Обработка сигнала.
        """
        if self.isActivated() and self._func:
            self._func(signal, self)


class icPackSlot(icSlot):
    """
    Слот с пакетной обработкой сигнала.
    """
    def parse_signal(self, signal):
        """
        Обработка сигнала.
        """
        if self.isActivated() and self._func:
            if issubclass(signal.__class__, icBeginTransactSignal):
                self.Begin()
            elif issubclass(signal.__class__, icRollBackTransactSignal):
                self.RollBack()
            elif issubclass(signal.__class__, icCommitTransactSignal):
                self.Commit()
            else:
                self.AppendToPack()

    def AppendToPack(self, signal):
        """
        Добавляем сигнал в пакет.
        """
        self.signalLst.append(signal)
        
    def Begin(self):
        """
        Начинаем сбор сигналов.
        """
        self.signalLst = []
        
    def Commit(self):
        """
        Завершаем сбор пакета и запускаем пакетную обработку.
        """
        if self.signalLst:
            self._func(self.signalLst, self)
            
    def init_slot(self):
        """
        Инициализация слота.
        """
        self.signalLst = []

    def RollBack(self):
        """
        """
        pass


def test():
    pass


if __name__ == '__main__':
    test()
