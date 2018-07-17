#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент движка SCADA системы.

Основной функцией SCADA движка является сканирование контроллеров
и обновление значений тегов, которые содержатся в движке.
Также происходит проверка и выполнение событий и аварий.
"""

import time
import thread

from ic.components import icwidget
from ic.components import icResourceParser as prs

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import ic_bmp

# from . import scada_tag
from . import int_tag
from . import float_tag
from . import bool_tag
from . import str_tag
from . import datetime_tag

from . import scada_event
from . import scada_alarm

# --- Спецификация ---
SPC_IC_SCADA_ENGINE = {'__parent__': icwidget.SPC_IC_SIMPLE,
                       }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSCADAEngine'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SCADAEngine',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   },
                '__parent__': SPC_IC_SCADA_ENGINE,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('recycle.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('recycle.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['IntSCADATag', 'FloatSCADATag', 'BoolSCADATag', 'StrSCADATag', 'DateTimeSCADATag',
                  'SCADAEvent', 'SCADAAlarm']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 4, 3)


# Классы тегов
TAG_CLASSES = (int_tag.icIntSCADATag, float_tag.icFloatSCADATag, bool_tag.icBoolSCADATag,
               str_tag.icStrSCADATag, datetime_tag.icDateTimeSCADATag)

# Таймаут ожидания запуска движка в секундах
ENGINE_START_TIMEOUT = 5


class icSCADAEngine(icwidget.icSimple):
    """
    Компонент движка SCADA системы.

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

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

        # Словарь классов сканирования для обработки в цикле
        # {паспорт класс сканирования: объект класса сканирования,...}
        self._scan_classes = dict()
        # Словарь cканируемых тегов для обработки в цикле
        # {паспорт класс сканирования: [объект сканируемого тега,...],..}
        self._scan_tags = dict()
        # Словарь обрабатываемых событий для обработки в цикле
        # {паспорт класс сканирования: [объект события,...],...}
        self._scan_events = dict()
        # Словарь обрабатываемых аварий для обработки в цикле
        # {паспорт класс сканирования: [объект аварии,...],...}
        self._scan_alarms = dict()

        # Признак запущенного цикла обработки
        self.is_running = False
        # Флаг-команда выхода из цикла обработки
        self.exit_run =True

        # Закешированные списки внутренних объектов
        self._tags_cache = None
        self._events_cache = None
        self._alarms_cache = None

    def childCreator(self, bCounter=False, progressDlg=None):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getChildrenTags(self):
        """
        Дочерние теги.
        """
        if self._tags_cache is None:
            # Нужно отфильтровать дочерние объекты
            self._tags_cache = [child for child in self.component_lst
                                if any([isinstance(child, tag_class) for tag_class in TAG_CLASSES])]
        return self._tags_cache

    def getChildrenEvents(self):
        """
        Дочерние объекты событий.
        """
        if self._events_cache is None:
            # Нужно отфильтровать дочерние объекты
            self._events_cache = [child for child in self.component_lst if isinstance(child, scada_event.icSCADAEvent)]
        return self._events_cache

    def getChildrenAlarms(self):
        """
        Дочерние объекты аварийных событий.
        """
        if self._alarms_cache is None:
            # Нужно отфильтровать дочерние объекты
            self._alarms_cache = [child for child in self.component_lst if isinstance(child, scada_alarm.icSCADAAlarm)]
        return self._alarms_cache

    def findObject(self, obj_name):
        """
        Найти объект по имени.
        @param obj_name: Имя объекта движка SCADA.
        @return: Объект или None в случае если объект не найден.
        """
        obj = self.components.get(obj_name, None)
        if obj is None:
            log.warning(u'Объект <%s> не найден в движке SCADA <%s>' % (obj_name, self.getName()))
        return obj

    def findTag(self, tag_name):
        """
        Найти объект тега по имени.
        @param tag_name: Имя тега.
        @return: Объект тега или None в случае ошибки.
        """
        tags = self.getChildrenTags()
        for tag in tags:
            if tag.name == tag_name:
                return tag
        log.warning(u'Тег <%s> не найден в движке SCADA <%s>' % (tag_name, self.getName()))
        return None

    def _init_scan_objects(self, obj_list, scan_obj_dict=None):
        """
        Инициализация сканируемых объектов.
        @param obj_list: Список объектов сканирования.
        @param scan_obj_dict: Словарь сканирумых объектов.
        @return: Заполненный словарь сканируемых объектов.
        """
        if scan_obj_dict is None:
            scan_obj_dict = dict()

        for obj in obj_list:
            scan_class_psp = obj.getScanClassPsp()
            if scan_class_psp not in self._scan_classes:
                self._scan_classes[scan_class_psp] = obj.getScanClass()
            if scan_class_psp not in scan_obj_dict:
                scan_obj_dict[scan_class_psp] = list()
            scan_obj_dict[scan_class_psp].append(obj)
        return scan_obj_dict

    def _log_scan_objects(self, scan_dict):
        """
        """
        for psp in scan_dict.keys():
            log.info(u'\t\tКласс сканирования <%s>' % psp[0][1])
            for obj in scan_dict[psp]:
                log.info(u'\t\t\tОбъект <%s>' % obj.name)

    def init_scan_objects(self):
        """
        Инициализация сканируемых объектов.
        @return: True/False.
        """
        self._scan_classes = dict()

        # Теги
        self._scan_tags = self._init_scan_objects(self.getChildrenTags())
        # События
        self._scan_events = self._init_scan_objects(self.getChildrenEvents())
        # Аварии
        self._scan_alarms = self._init_scan_objects(self.getChildrenAlarms())

        log.info(u'Информация о сканируемых объектах в <%s>:' % self.getName())
        if not self._scan_classes:
            log.warning(u'\tНе определены классы сканирования')
        else:
            log.info(u'\tКлассы сканирования: %s' % [psp[0][1] for psp in self._scan_classes.keys()])
        if not self._scan_tags:
            log.warning(u'\tНе определены сканируемые теги')
        else:
            log.info(u'\tСканируемые теги:')
            self._log_scan_objects(self._scan_tags)
        if not self._scan_events:
            log.warning(u'\tНе определены сканируемые события')
        else:
            log.info(u'\tСканируемые события:')
            self._log_scan_objects(self._scan_events)
        if not self._scan_alarms:
            log.warning(u'\tНе определены сканируемые аварии')
        else:
            log.info(u'\tСканируемые аварии:')
            self._log_scan_objects(self._scan_alarms)

    def start(self, update_panels=None):
        """
        Запуск основного цикла обработки тегов.
        @param update_panels: Принудительно обновить панели.
            Может задаваться как списком так и объектом.
        @return: True/False.
        """
        self.init_scan_objects()

        self.exit_run = False
        thread.start_new(self.run, ())

        # Ожидание запуска движка
        start_time = time.time()
        stop_time = start_time + ENGINE_START_TIMEOUT
        cur_time = time.time()

        log.debug(u'Начало ожидания запуска')
        while not self.is_running and cur_time < stop_time:
            cur_time = time.time()
        log.debug(u'Окончание ожидания запуска. Ожидание %s секунд.' % (cur_time - start_time))

        # После удачного запуска движка принудительно обновить панели вызывающие их
        self.update_panels(update_panels)

        return self.is_running

    def update_panels(self, update_panels=None):
        """
        Принудительно обновить панели.
        @param update_panels: Принудительно обновить панели.
            Может задаваться как списком так и объектом.
        @return: True/False.
        """
        try:
            if update_panels:
                if type(update_panels) in (list, tuple):
                    # Список панелей
                    for panel in update_panels:
                        panel.updateValues()
                else:
                    update_panels.updateValues()
                return True
        except:
            log.fatal(u'Ошибка обновления данных панели <%s>' % update_panels)
        return False

    def stop(self, update_panels=None):
        """
        Остановка основного цикла обработки тегов.
        @param update_panels: Принудительно обновить панели.
            Может задаваться как списком так и объектом.
        @return: True/False.
        """
        self.exit_run = True
        # Обновление пока не реализовано
        return True

    def isRunning(self):
        """
        Признак запущенного цикла обработки.
        @return: True/False.
        """
        return self.is_running

    def run(self):
        """
        Функция основного цикла обработки.
        """
        log.info(u'Запуск цикла обработки <%s>' % self.getName())
        self.is_running = False
        while not self.exit_run:
            start_tick = time.time()

            scan_classes_psp = self.get_active_scan_classes_psp(start_tick)

            # Подготовка тегов для чтения
            read_tags = self.get_refreshable_tags(*scan_classes_psp)
            # Чтение тегов
            self.read_tags(*read_tags)

            # События
            self.do_events(*scan_classes_psp)

            # Аварии
            self.do_alarms(*scan_classes_psp)

            # Движок считается запущенным после удачного первого цикла обработки
            self.is_running = True

        self.is_running = False
        log.info(u'Останов цикла обработки <%s>' % self.getName())

    def get_active_scan_classes_psp(self, ctrl_tick):
        """
        Список паспортов классов сканирования, которые необходимо обновить.
        @param ctrl_tick: Контрольное значение времени,
            для определения необходимости обработки.
        @return: Список паспортов классов сканирования.
        """
        return [scan_class_psp for scan_class_psp, scan_class in self._scan_classes.items() if scan_class.isOverTick(ctrl_tick)]

    def get_refreshable_tags(self, *scan_classes_psp):
        """
        Список всех тегов, которые пора прочитать/обновить значения.
        @param scan_classes_psp: Список паспортов классов сканирования,
            которые необходимо обновить.
        @return: Список тегов, которые необходимо обновить/прочитать из источника данных.
        """
        read_tags = list()
        for scan_class_psp in scan_classes_psp:
            tags = self._scan_tags.get(scan_class_psp, list())
            read_tags += tags
        return read_tags

    def read_tags(self, *tags):
        """
        Запустить процедуру чтение тегов.
        @param tags: Список читаемх тегов.
        @return: True/False.
        """
        if not tags:
            # log.warning(u'Не определен список тегов для чтения')
            return False
        # else:
        #     log.debug(u'Чтение тегов %s в движке <%s>' % (str(tags), self.getName()))

        # Подготовка списка узлов
        tag_nodes = [tag.getNode() for tag in tags]
        nodes = dict()
        for tag_node in tag_nodes:
            tag_node_name = tag_node.getName()
            if tag_node_name not in nodes:
                nodes[tag_node_name] = tag_node

        # Подготовка списка тегов
        node_tags = dict([(node_name, list()) for node_name in nodes.keys()])
        for tag in tags:
            tag_node = tag.getNode()
            tag_node_name = tag_node.getName()
            node_tags[tag_node_name].append(tag)

        # Запустить процедуру чтения данных
        for node_name, node in nodes.items():
            env = self.getEnv()
            node.setEnv(**env)
            node.setEnv(SCADA_ENGINE=self)
            node.readTags(*node_tags[node_name])

        return True

    def do_events(self, *scan_classes_psp):
        """
        Обработка событий.
        @param scan_classes_psp: Список паспортов классов сканирования,
            которые необходимо обновить.
        @return: True/False.
        """
        for scan_class_psp in scan_classes_psp:
            events = self._scan_events.get(scan_class_psp, list())
            for event in events:
                event.do()
        return True

    def do_alarms(self, *scan_classes_psp):
        """
        Обработка аварий.
        @param scan_classes_psp: Список паспортов классов сканирования,
            которые необходимо обновить.
        @return: True/False.
        """
        # for scan_class_psp in scan_classes_psp:
        #     alarms = self._scan_alarms.get(scan_class_psp, list())
        #     for alarm in alarms:
        #         alarm.do()
        return True

    def setEnv(self, **environment):
        """
        Добавить дополнительное окружение движка.
        Необходимо для выполнения вычисляемых тегов.
        @param environment: Словарь дополнительных переменных окружения движка.
        @return: True/False.
        """
        if not hasattr(self, '_engine_environment'):
            self._engine_environment = dict()
        self._engine_environment.update(environment)
        return True

    def getEnv(self):
        """
        Дополнительное окружение движка.
        Необходимо для выполнения вычисляемых тегов.
        @return: Словарь дополнительных переменных окружения движка.
        """
        if not hasattr(self, '_engine_environment'):
            return dict()
        return self._engine_environment
