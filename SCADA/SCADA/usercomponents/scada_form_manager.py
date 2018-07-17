#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер форм/панелей SCADA системы.
"""

import wx
from ic.engine import form_manager
from ic.components import icwidget
from ic.components import icwxpanel

from ic.log import log

__version__ = (0, 0, 5, 1)

# Период сканирования формы/панели SCADA системы по умолчанию
DEFAULT_SCAN_TICK = -1

ADDRESS_DELIMETER = u'.'

ENGINE_ADDRESS_IDX = 0
OBJ_ADDRESS_IDX = 1


class icSCADAFormManager(form_manager.icFormManager):
    """
    Менеджер форм/панелей SCADA системы.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        form_manager.icFormManager.__init__(self, *args, **kwargs)

        # Список движков сканирования SCADA системы
        self.scada_engines = list()

        # Период сканирования для обновления формы/панели
        self.scan_tick = DEFAULT_SCAN_TICK

        self.timer = None

        # Признак автозапуска и автоостанова всех движков при создании/закрытии окна
        self.auto_run = False

        try:
            self.Bind(wx.EVT_TIMER, self.onTimerTick)
        except:
            log.fatal(u'Ошибка связи обработчика события таймера')

        # Кэш соответствий {Имя контрола: Адрес тега}
        self._obj_addresses_cache = None

    def get_panel_obj_addresses(self, *ctrl_names):
        """
        Получить адреса объектов указанных в data_name свойстве контролов панели.
        Адреса объектов указываются как <Имя_движка.Имя_объекта_в_движке>.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        @return: Заполненный список [(контрол, адрес тега),...)
        """
        if self._obj_addresses_cache is None:
            self._obj_addresses_cache = self._get_panel_obj_addresses(None, *ctrl_names)
        return self._obj_addresses_cache

    def _get_panel_obj_addresses(self, data_list=None, *ctrl_names):
        """
        Получить адреса объектов указанных в data_name свойстве контролов панели.
        Адреса объектов указываются как <Имя_движка.Имя_объекта_в_движке>.
        @param data_list: Список для заполнения.
            Если не определен то создается новый список.
        @param ctrl_names: Взять только контролы с именами...
            Если имена контролов не определены,
            то обрабатываются контролы,
            указанные в соответствиях (accord).
        @return: Заполненный список [(контрол, адрес тега),...)
        """
        result = list() if data_list is None else data_list
        if not ctrl_names:
            ctrl_names = self.getAllChildrenNames()

        for ctrlname in ctrl_names:
            ctrl = self.FindObjectByName(ctrlname)
            if issubclass(ctrl.__class__, icwidget.icWidget) and ctrl.isEnabled():
                if issubclass(ctrl.__class__, icwxpanel.icWXPanel):
                    log.warning(u'ВНИМАНИЕ! Для обновлений контролов в панели <%s>, панель должна быть SCADAPanel' % ctrlname)

                if issubclass(ctrl.__class__, self.__class__):
                    data = ctrl._get_panel_obj_addresses(data_list, *ctrl_names)
                    result += data
                else:
                    address = ctrl.getDataName()
                    if address:
                        if self.is_address(address):
                            # Сразу разделить адрес на имя движка и имя объекта
                            result.append((ctrl, tuple(address.split(ADDRESS_DELIMETER))))
                        else:
                            log.error(u'Ошибка адресации <%s> в контроле <%s>. Адреса указываются как <Имя_движка.Имя_объекта_в_движке>' % (address, ctrlname))
                    else:
                        log.warning(u'Контрол <%s> не может принимать данные' % ctrlname)
        return result

    def is_address(self, value):
        """
        Проверка является ли строковое значение адресом SCADA объекта.
        @param value: Проверяемое значение.
        @return: True - это адрес объекта / False - нет.
        """
        return bool(value) and (ADDRESS_DELIMETER in value) and (value.count(ADDRESS_DELIMETER) == 1)

    def startEngines(self):
        """
        Запуск движков.
        @return: True-все движки успешно запущены / False - ошибка запуска.
        """
        return all([engine.start(self) for engine in self.scada_engines])

    def stopEngines(self):
        """
        Останов движков.
        @return: True-все движки успешно остановлены / False - ошибка останова.
        """
        return all([engine.stop(self) for engine in self.scada_engines])

    def addSCADAEngine(self, scada_engine):
        """
        Добавить движок в список.
        @param scada_engine: Объект движка.
        @return: True/False.
        """
        if scada_engine is None:
            log.warning(u'Не определен объект движка сканирования SCADA системы')
            return False

        if isinstance(self.scada_engines, list):
            if scada_engine not in self.scada_engines:
                scada_engine.setEnv(SCADA_PANEL=self)
                self.scada_engines.append(scada_engine)
                return False
            else:
                log.warning(u'Движок <%s> у же присутствует в списке обработки' % scada_engine)
        else:
            log.warning(u'Ошибка типа списка движков сканирования SCADA системы <%s>' % self.scada_engines.__class__.__name__)
        return False

    def startTimer(self):
        """
        Запуск таймера обновления данных.
        @return: True/False.
        """
        if self.scan_tick > 0:
            # Обновить данные в начале запуска в любом случае
            # self.updateValues()

            self.timer = wx.Timer(self)
            # ВНИМАНИЕ! Период сканирования задается в секундах,
            # а таймер работает с миллисекундами. Необходимо сделать преобразование
            milliseconds = self.scan_tick * 1000
            self.timer.Start(milliseconds)
            return True
        else:
            self.timer = None
            log.warning(u'Не указан период сканирования панели SCADA системы')
        return False

    def stopTimer(self):
        """
        Останов таймера обновления данных.
        @return: True/False.
        """
        if self.timer:
            self.timer.Stop()
            self.timer = None
            return True
        return False

    def onTimerTick(self, event):
        """
        Обработчик одного тика таймера.
        """
        if self.timer is not None:
            # Если таймер запущен, то обновлять форму
            self.updateValues()

    def findSCADAEngine(self, engine_name):
        """
        Поиск движка скада системы в списке по имени.
        @param engine_name: Имя движка.
        @return: Объект движка или None, ели объект движка не найден.
        """
        for engine in self.scada_engines:
            if engine.name == engine_name:
                return engine
        engine_names = [engine.name for engine in self.scada_engines]
        log.warning(u'Движок SCADA не найден среди обрабатываемых %s' % engine_names)
        return None

    def updateValues(self):
        """
        Обновить значения контролов.
        """
        try:
            log.debug(u'Старт процедуры обновления значений контролов')
            obj_addresses = self.get_panel_obj_addresses()
            # obj_addresses_names = [ctrl.getName() for ctrl, address in obj_addresses]
            # log.debug(u'Список обрабатываемых контролов %s' % obj_addresses_names)

            for ctrl, address in obj_addresses:
                engine_name, obj_name = address
                engine = self.findSCADAEngine(engine_name)
                if engine:
                    obj = engine.FindObjectByName(obj_name)
                    if obj:
                        value = obj.getCurValue()
                        # ctrl = self.FindObjectByName(ctrlname)
                        ctrl.setValue(value)
                    else:
                        log.warning(u'Объект <%s> не найден в движке <%s>' % (obj_name, engine_name))
            log.debug(u'Конец процедуры обновления значений контролов')
        except:
            log.fatal(u'Ошибка обновления значений контролов формы SCADA системы')

    def findSCADAObject(self, obj_address):
        """
        Поиск объекта по его адресу.
        @param obj_address: Адрес объекта.
            Адреса объектов указываются как <Имя_движка.Имя_объекта_в_движке>.
        @return: Найденный объект или None, если объект не найден.
        """
        if type(obj_address) not in (str, unicode):
            log.error(u'Не корректный тип адреса <%s> объекта SCADA движка' % obj_address.__class__.__name__)
            return None

        engine_name, obj_name = obj_address.split(ADDRESS_DELIMETER)
        if engine_name and obj_name:
            engine = self.findSCADAEngine(engine_name)
            if engine:
                obj = engine.findObject(obj_name)
                return obj
        return None

    # Другие наименования метода
    findTag = findSCADAObject
    findEvent = findSCADAObject
    findAlarm = findSCADAObject

    def start(self):
        """
        Функция общего запуска.
        @return: True/False.
        """
        result_engines = self.startEngines()
        result_timer = self.startTimer()
        return result_engines and result_timer

    def stop(self):
        """
        Функция общего останова.
        @return: True/False.
        """
        result_timer = self.stopTimer()
        result_engines = self.stopEngines()
        return result_engines and result_timer
