#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ОБЪЕКТ ИМЕЮЩИЙ СОСТОЯНИЕ.
Объект, один из реквизитов которого содержит состояние объекта.
Состояние объекта задается справочником состояний.
От БИЗНЕС ОБЪЕКТА отличается наличием метода
change_state и обработчиком изменения состояния on_change_state.
Аналог объекта пошаговой обработки и конечной публикации.
"""

# Подключение библиотек
import datetime
from ic.log import log
from . import icbusinessobj

from ic.engine import ic_user
from ic.utils import ic_extend

# Версия
__version__ = (0, 0, 2, 1)

# Спецификация
SPC_IC_STATEOBJ = {'type': 'StateObj',
                   'name': 'default',

                   # Обработчик события смены состояния объекта
                   'on_change_state': None,

                   '__parent__': icbusinessobj.SPC_IC_BUSINESSOBJ,
                   }


DEFAULT_STATE_REQUISITE_NAME = 'state'


class icStateObjProto(icbusinessobj.icBusinessObjPrototype):
    """
    ОБЪЕКТ ИМЕЮЩИЙ СОСТОЯНИЕ. Прототип компонента.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструтор.
        """
        icbusinessobj.icBusinessObjPrototype.__init__(self, *args, **kwargs)

    def getHistory(self):
        """
        История изменения состояния объекта.
        Абстрактный метод. Переопределяется в классе компонента.
        """
        return None

    def doOnChangeState(self):
        """
        Функция обработчика смены состояния.
        Абстрактный метод. Переопределяется в классе компонента.
        @return: True/False.
        """
        return True

    def getState(self):
        """
        Определить состояние объекта.
        """
        return self.getRequisiteValue('state')

    def change_state(self, new_state,
                     state_requisite_name=DEFAULT_STATE_REQUISITE_NAME,
                     auto_save=True):
        """
        Функция изменения состояния.
        ВНИМАНИЕ! Для документов эта функция может вызываться только
        в обработчике выполнения операции документа!
        @param new_state: Код нового состояния.
        @param state_requisite_name: Имя реквизита состояния.
        @param auto_save: Сохранять данные объекта автоматически?
        @return: True/False.
        """
        # ВНИМАНИЕ! При смене состояния любого документа/объекта запоминаем
        # компьютер и пользователя которым были сделаны изменения
        if self.isRequisite('computer') and not self.getRequisiteValue('computer'):
            self.setRequisiteValue('computer', ic_extend.getComputerName())
        if self.isRequisite('username') and not self.getRequisiteValue('username'):
            self.setRequisiteValue('username', ic_user.getCurUserName())
        # Дата-время изменения состояния
        if self.isRequisite('dt_state') and not self.getRequisiteValue('dt_state'):
            self.setRequisiteValue('dt_state', datetime.datetime.now())

        state_requisite = self.findRequisite(state_requisite_name)
        if state_requisite is None:
            log.warning(u'Изменение состояния объекта. Не найден реквизит <%s> в объекте <%s>' % (state_requisite_name,
                                                                                                  self.getName()))
            return False

        on_change_state_result = self.doOnChangeState()
        if not on_change_state_result:
            # Какаято ошибка. Дальше выполнять нельзя.
            log.warning(u'Ошибка выполнения обработки смены состояния объекта <%s> на <%s>' % (self.getName(),
                                                                                               new_state))
            return False

        # Сохранить в истории
        history = self.getHistory()
        if history is not None:
            # Перед изменением значений полей историей
            # необходимо сохранить текущие значения реквизитов
            self.save_obj()

            requisites = dict(uuid=self.getUUID())
            requisite_values = dict([(requisite_name, requisite.getValue()) for requisite_name, requisite in self.requisites.items()])
            requisites.update(requisite_values)
            requisites[state_requisite_name] = new_state
            try:
                history.connect()
                history.do_state(**requisites)
                history.disconnect()
            except:
                history.disconnect()
                log.fatal(u'Ошибка сохранения истории')

            # Обновить значения реквизитов
            # из БД, т.к. история изменила некоторые значения
            self.load_obj(self.getUUID())
        else:
            # Установить значение нового состояния в реквизите
            state_requisite.setValue(new_state)
            if auto_save:
                self.save_obj()

        return True

    # Другое название метода
    changeState = change_state

    def add_state_object(self, new_state,
                         state_requisite_name=DEFAULT_STATE_REQUISITE_NAME):
        """
        Добавить новый объект состояния в указанном состоянии.
        ВНИМАНИЕ! Для документов эта функция может вызываться только
        в обработчике выполнения операции документа!
        @param new_state: Код нового состояния.
        @param state_requisite_name: Имя реквизита состояния.
        @return: True/False.
        """
        # ВНИМАНИЕ! При смене состояния любого документа/объекта запоминаем
        # компьютер и пользователя которым были сделаны изменения
        if self.isRequisite('computer') and not self.getRequisiteValue('computer'):
            self.setRequisiteValue('computer', ic_extend.getComputerName())
        if self.isRequisite('username') and not self.getRequisiteValue('username'):
            self.setRequisiteValue('username', ic_user.getCurUserName())
        # Дата-время изменения состояния
        if self.isRequisite('dt_state') and not self.getRequisiteValue('dt_state'):
            self.setRequisiteValue('dt_state', datetime.datetime.now())

        state_requisite = self.findRequisite(state_requisite_name)
        if state_requisite is None:
            log.warning(u'Изменение состояния объекта. Не найден реквизит <%s> в объекте <%s>' % (state_requisite_name,
                                                                                                  self.getName()))
            return False

        on_change_state_result = self.doOnChangeState()
        if not on_change_state_result:
            # Какаято ошибка. Дальше выполнять нельзя.
            log.warning(u'Ошибка выполнения обработки смены состояния объекта <%s> на <%s>' % (self.getName(),
                                                                                               new_state))
            return False

        # Сохранить в истории
        history = self.getHistory()
        if history is not None:
            # Перед изменением значений полей историей
            # необходимо сохранить текущие значения реквизитов
            self.save_obj()

            requisites = dict(uuid=self.getUUID())
            requisite_values = dict([(requisite_name, requisite.getValue()) for requisite_name, requisite in self.requisites.items()])
            requisites.update(requisite_values)
            requisites[state_requisite_name] = new_state
            try:
                history.connect()
                history.do_state(**requisites)
                history.disconnect()
            except:
                history.disconnect()
                log.fatal(u'Ошибка сохранения истории')

            # Обновить значения реквизитов
            # из БД, т.к. история изменила некоторые значения
            self.load_obj(self.getUUID())
        else:
            # Установить значение нового состояния в реквизите
            state_requisite.setValue(new_state)
            self.add(Data_=self.getRequisiteData())

        return True

    # Другое название метода
    addStateObj = add_state_object
