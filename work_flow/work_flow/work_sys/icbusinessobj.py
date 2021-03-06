#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Бизнес - объект.
Бизнес объект в общем случае представляет собой объект/сущность 
предметной области, который имеет свою историю исзмения состояний,
может являться субъектом или объектом по отношению к другим бизнес объектам.
Любой бизнес объект имеет уникальный идентификатор UUID,
который храниться в БД.
Бизнес объект отличается от метаобъектов тем что алгоритм учета изменений(истории) 
его отличен от понятия work flow в классическом понимании.
Обработкой истории занимается движок исторического процесса бизнес объекта.

:type SPC_IC_BUSINESSOBJ: C{dictionary}
:var SPC_IC_BUSINESSOBJ: Спецификация на ресурсное описание БИЗНЕСС-ОБЪЕКТА.
Описание ключей SPC_IC_BUSINESSOBJ:

    - B{name = 'default'}: Имя.
    - B{type = 'BusinessObj'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{init_form = None}: Форма/Визард для создания/инициализации.
    - B{edit_form = None}: Форма для редактирования.
    - B{view_form = None}: Форма для просмотра.
    - B{report = None}: Отчет для распечатки.
    - B{prototype = None}: Прототип, у которого наследуются реквизиты/атрибуты.
    
"""

# Подключение библиотек
import ic
from ic.utils import uuidfunc
from ic.utils import toolfunc
from ic.log import log
from ic.interfaces import icdatasetinterface

import work_flow.work_sys.icworkbase as icworkbase
from work_flow.work_sys import persistent
from work_flow.work_sys import form_generator
from STD.queries import filter_convert

# Версия
__version__ = (0, 1, 2, 3)


# Спецификация
SPC_IC_BUSINESSOBJ = {'type': 'BusinessObj',
                      'name': 'default',
                      'description': '',    # Описание
                      'db': None,           # Паспорт БД

                      # Автоматически создавать компоненты группировки в формах?
                      'auto_group': False,

                      # Формы управления/взаимодействия с объектом(ами)
                      # Если форма не определена, то она генерируется при первом запуске,
                      # добавляется в проект и затем используется.
                      'init_form': None,    # Форма/Визард для создания/инициализации
                      'edit_form': None,    # Форма для редактирования
                      'view_form': None,    # Форма для просмотра
                      'search_form': None,  # Форма поиска бизнес объекта по значениям его атрибутов
                      'choice_form': None,  # Форма выбора бизнес объекта

                      'report': None,       # Отчет для распечатки

                      'prototype': None,    # Прототип, у которого наследуются реквизиты/атрибуты
    
                      # Дополнительные свойства управления генерацией
                      'is_page_grp_init': False,  # Производить группировку реквизитов по страницам/
                                                  # или выводить все реквизиты одним списком на форме инициализации?
                      'is_page_grp_edit': True,   # Производить группировку реквизитов по страницам/
                                                  # или выводить все реквизиты одним списком на форме редактирования?
                      'is_page_grp_view': True,   # Производить группировку реквизитов по страницам/
                                                  # или выводить все реквизиты одним списком на форме просмотра?
                      'is_page_grp_search': True,  # Производить группировку реквизитов по страницам/
                                                   # или выводить все реквизиты одним списком на форме поиска?

                      'do_init': None,    # Функция инициализации
                      'do_edit': None,    # Функция редактирования
                      'do_view': None,    # Функция просмотра
                      'do_search': None,  # Функция поиска
                      'do_choice': None,  # Функция выбора

                      'valid_init': None,    # Функция валидации при инициализации
                      'valid_edit': None,    # Функция валидации при редактировании
                      'valid_del': None,     # Функция валидации при удалении

                      'history': None,      # История хранения изменений состояния объекта

                      'limit': None,  # Ограничение количества объектов для обработки

                      'child': [],
    
                      '__parent__': icworkbase.SPC_IC_WORKBASE,
                      '__attr_hlp__': {'db': u'Паспорт БД',
                                       'auto_group': u'Автоматически создавать компоненты группировки в формах?',
                                       'init_form': u'Форма/Визард для создания/инициализации',
                                       'edit_form': u'Форма редактирования',
                                       'view_form': u'Форма просмотра',
                                       'search_form': u'Форма поиска бизнес объекта по значениям его атрибутов',
                                       'choice_form': u'Форма выбора бизнес объекта',
                                       'report': u'Отчет для распечатки',
                                       'prototype': u'Прототип, у которого наследуются реквизиты/атрибуты',
                                       'is_page_grp_init': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме инициализации?',
                                       'is_page_grp_edit': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме редактирования?',
                                       'is_page_grp_view': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме просмотра?',
                                       'is_page_grp_search': u'Производить группировку реквизитов по страницам/или выводить все реквизиты одним списком на форме поиска?',
                                       'do_init': u'Функция инициализации',
                                       'do_edit': u'Функция редактирования',
                                       'do_view': u'Функция просмотра',
                                       'do_search': u'Функция поиска',
                                       'do_choice': u'Функция выбора',
                                       'valid_init': u'Функция валидации при инициализации',
                                       'valid_edit': u'Функция валидации при редактировании',
                                       'valid_del': u'Функция валидации при удалении',
                                       'history': u'История хранения изменений состояния объекта',
                                       'limit': u'Ограничение количества объектов для обработки',
                                       },
                      }


class icBusinessObjInterface(icworkbase.icWorkBase, persistent.icObjPersistent, form_generator.icObjFormGenerator,
                             icdatasetinterface.icDatasetInterface):
    """
    Интерфейс абстрактного бизнес-объекта.
    """

    def __init__(self, parent=None):
        """
        Конструктор.

        :param parent: Родительский объект.
        """
        icworkbase.icWorkBase.__init__(self, parent)
        
        persistent.icObjPersistent.__init__(self, parent)
        form_generator.icObjFormGenerator.__init__(self, parent)
        icdatasetinterface.icDatasetInterface.__init__(self)
        
    def getWorkStorage(self):
        """
        Хранилище.
        """
        return self.getStorage()

    def getReport(self):
        """
        Отчет для распечатки.
        """
        return None
       
    def Init(self, parent=None, context=None, auto_add=False,
             init_form_psp=None):
        """
        Запуск инициализации/создания.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param auto_add: Признак автодобавления в БД.
        :param init_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Init> in class %s' % self.__class__.__name__

    Add = Init

    def Edit(self, parent=None, context=None, UUID=None,
             edit_form_psp=None):
        """
        Запуск на редактирование.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param UUID: Уникальный идентификатор редактируемого объекта.
            Если None, то уникальный идентификатор self.uuid
        :param edit_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <edit> in class %s' % self.__class__.__name__
        
    def View(self, parent=None, context=None, UUID=None,
             view_form_psp=None):
        """
        Режим просмотра.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param view_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <View> in class %s' % self.__class__.__name__
    
    def Search(self, parent=None, context=None,
               search_form_psp=None):
        """
        Режим поиска объекта.

        :param parent: Родительская форма.
        :param context:Контекст.
        :param search_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Search> in class %s' % self.__class__.__name__
    
    def Choice(self, parent=None, context=None,
               choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.

        :param parent: Родительская форма.
        :param context:Контекст.
        :param choice_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Choice> in class %s' % self.__class__.__name__

    def Browse(self, parent=None, context=None,
               choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.
        В виде страницы главного нотебука.

        :param parent: Родительская форма.
        :param context:Контекст.
        :param choice_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <ChoicePage> in class %s' % self.__class__.__name__

    def Print(self, report=None, bPreview=False, eval_space=None):
        """
        Печать.

        :param report: Указание альтернативного отчета вывода.
            Если None, то отчет берется из спецификации.
        :param bPreview: Открыть отчет в режиме предварительного просмотра?
        :param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <Print> in class %s' % self.__class__.__name__
    
    def Del(self, UUID=None, eval_space=None):
        """
        Удаление.

        :param UUID: uuid удаляемого объекта.
        :param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <Del> in class %s' % self.__class__.__name__
        
    def sendTo(self, to_address=None, eval_space=None):
        """
        Отправка.

        :param to_address: Указание адресата.
        :param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <sendTo> in class %s' % self.__class__.__name__
    
    def save_obj(self, UUID=None):
        """
        Сохранить внутренние данные в хранилище.

        :param UUID: Идентификатор. Если None, то сохранить текущий.
        """
        assert None, 'Abstract method <save_obj> in class %s' % self.__class__.__name__
        
    def load_obj(self, UUID=None):
        """
        Загрузить внутренние данные из хранилища.

        :param UUID: Идентификатор.
        """
        assert None, 'Abstract method <load_obj> in class %s' % self.__class__.__name__
        
    def init_obj(self):
        """
        Инициализация объекта.
        """
        assert None, 'Abstract method <init_obj> in class %s' % self.__class__.__name__
        
    def getObjId(self):
        """
        Идентификтор объекта.
        """
        assert None, 'Abstract method <getObjId> in class %s' % self.__class__.__name__
        
    def startEdit(self, UUID=None):
        """
        Запуск на редактирование.
        """
        assert None, 'Abstract method <startEdit> in class %s' % self.__class__.__name__
        
    def stopEdit(self):
        """
        Остановка редактирования.
        """
        assert None, 'Abstract method <stopEdit> in class %s' % self.__class__.__name__


class icBusinessObjProto(icBusinessObjInterface):
    """
    Бизнесс-объект.
    """

    def __init__(self, parent=None):
        """
        Конструктор.

        :param parent: Родительский объект.
        """
        icBusinessObjInterface.__init__(self, parent)
        
        # Описание объекта. Храниться в таблице для каждого объекта

        # Словарь всех реквизитов.
        # Инициализируется непосредственно в конструкторе компонента.
        self.requisites = {}
        
        # История изменения состояний объекта
        self._history_obj = None

    def isDoInit(self):
        """
        Определена функция инициализации?

        :return: True/False.
        """
        return False

    def isDoEdit(self):
        """
        Определена функция редактирования?

        :return: True/False.
        """
        return False

    def isDoView(self):
        """
        Определена функция просмотра?

        :return: True/False.
        """
        return False

    def isDoSearch(self):
        """
        Определена функция поиска?

        :return: True/False.
        """
        return False

    def isDoChoice(self):
        """
        Определена функция выбора?

        :return: True/False.
        """
        return False

    def doInit(self, *args, **kwargs):
        """
        Функция инициализации.

        :return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def doEdit(self, *args, **kwargs):
        """
        Функция редактирования.

        :return: Объект функции редактирования,
            или None если не определена.
        """
        return None

    def doView(self, *args, **kwargs):
        """
        Функция просмотра.

        :return: Объект функции просмотра,
            или None если не определена.
        """
        return None

    def doSearch(self, *args, **kwargs):
        """
        Функция поиска.

        :return: Объект функции поиска,
            или None если не определена.
        """
        return None

    def doChoice(self, *args, **kwargs):
        """
        Функция выбора.

        :return: Объект функции выбора,
            или None если не определена.
        """
        return None

    def isValidInit(self):
        """
        Определена функция валидации при инициализации?

        :return: True/False.
        """
        return False

    def isValidEdit(self):
        """
        Определена функция валидации при редактировании?

        :return: True/False.
        """
        return False

    def isValidDel(self):
        """
        Определена функция валидации при удалении?

        :return: True/False.
        """
        return False

    def validInit(self, *args, **kwargs):
        """
        Функция валидации при инициализации.

        :return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def validEdit(self, *args, **kwargs):
        """
        Функция валидации при редактировании.

        :return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def validDel(self, *args, **kwargs):
        """
        Функция валидации при удалении.

        :return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def getObjDescription(self, UUID=None):
        """
        Описание бизнес-объекта  предметной области.

        :param UUID: Уникальный идентификатор объекта.
        """
        if UUID is not None:
            self.loadRequisiteData(UUID)
            
        description = u' '.join([toolfunc.toUnicode(requisite.getValue()) for requisite in self.getChildrenRequisites() if requisite.isDescription()])

        if description:
            return description

        # Если описания бизнесобъекта предметной области нет, тогда
        # вернуть описание компонента
        return self.description
    
    def getAllRequisites(self):
        """
        Список всех реквизитов.
        """
        return self.getChildrenRequisites()
        
    def Init(self, parent=None, context=None, auto_add=False, init_form_psp=None):
        """
        Запуск инициализации/создания.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param auto_add: Признак автодобавления в БД.
        :param init_form_psp: Паспорт формы для подмены стандартной формы вывода.
        :return: Словарь нового объекта или None в случае ошибки.
        """
        # Перед созданием формы необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()
                    
        # Создание и вывод формы инициализации
        if init_form_psp is None:
            frm_psp = self.getInitFormPsp()
            if not frm_psp:
                frm_psp = self.createInitFormRes()
        else:
            frm_psp = init_form_psp

        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self
            
            # Заполнение значений по умолчанию реквизитов через контекст
            requisite_values = self.getRequisiteDataDefault()

            init_values = None
            if not self.isDoInit():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                context=context)
                frm_obj.GetContext().setValueInCtrl(frm_obj, requisite_values)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    # Сохранить реквизиты доокумента
                    init_values = frm_obj.GetContext().getValueInCtrl(frm_obj)
                    if auto_add:
                        add_ok = self.validInit(requisite_values=init_values) if self.isValidInit() else True
                        if add_ok:
                            uuid_new_obj = self.addRequisiteData(init_values)
                            log.info(u'Автодобавление объекта [%s] в <%s>' % (uuid_new_obj, self.name))

                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
            else:
                init_values = self.doInit(requisite_values=requisite_values)
                if auto_add and init_values:
                    add_ok = self.validInit(requisite_values=init_values) if self.isValidInit() else True
                    if add_ok:
                        uuid_new_obj = self.addRequisiteData(init_values)
                        log.info(u'Автодобавление объекта [%s] в <%s>' % (uuid_new_obj, self.name))

            # Сохранение реквизитов не произошло
            return init_values
        except:
            log.fatal(u'Ошибка  инициализации БИЗНЕС-ОБЪЕКТА <%s>' % self.name)
        return None

    Add = Init

    def Search(self, parent=None, context=None, search_form_psp=None):
        """
        Режим поиска объекта.

        :param parent: Родительская форма.
        :param context: Пространство имен.
        :param search_form_psp: Паспорт формы для подмены стандартной формы вывода.
        :return: Возвращает UUID выбранного объекта или None,
        если объект не выбран.
        """
        # Перед созданием формы необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()
                    
        # Создание и вывод формы
        if search_form_psp is None:
            frm_psp = self.getSearchFormPsp()
            if not frm_psp:
                frm_psp = self.createSearchFormRes()
        else:
            frm_psp = search_form_psp
            
        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self

            obj_uuid = None
            if not self.isDoSearch():
                # Создать и открыть форму
                panel_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                  context=context)
                
                # Создать и открыть форму
                frm_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                context=context)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    obj_uuid = frm_obj.get_manager().getSelectedObjUUID()
            
                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
            else:
                obj_uuid = self.doSearch()

            return obj_uuid
        except:
            log.fatal(u'Ошибка режима поиска БИЗНЕС-ОБЪЕКТА %s' % self.name)
        return None
        
    def Choice(self, parent=None, context=None, choice_form_psp=None):
        """
        Режим выбора объекта сэлементом поиска/фильтра.

        :param parent: Родительская форма.
        :param context: Контекст формы.
        :param choice_form_psp: Паспорт формы для подмены стандартной формы вывода.
        :return: Возвращает UUID выбранного объекта или None,
        если объект не выбран.
        """
        # Перед созданием формы необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()
                    
        # Создание и вывод формы
        if choice_form_psp is None:
            frm_psp = self.getChoiceFormPsp()
            if not frm_psp:
                frm_psp = self.createChoiceFormRes()
        else:
            frm_psp = choice_form_psp
            
        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self

            obj_uuid = None
            if not self.isDoChoice():
                # Создать и открыть форму
                frm_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                context=context)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    obj_uuid = frm_obj.get_manager().getSelectedObjUUID()
                
                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
            else:
                obj_uuid = self.doChoice()

            return obj_uuid
        except:
            log.fatal(u'Ошибка режима выбора БИЗНЕС-ОБЪЕКТА <%s>' % self.name)
        return None

    def Browse(self, parent=None, context=None, choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.
        В виде страницы главного нотебука.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param choice_form_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        # Перед созданием необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()

        # Создание и вывод
        if choice_form_psp is None:
            psp = self.getChoiceFormPsp()
            if not psp:
                psp = self.createChoicePanelRes()
        else:
            psp = choice_form_psp

        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()

            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self

            # Создать и открыть
            obj = ic.getKernel().Create(psp, parent=parent, context=context)
            ic.getKernel().GetContext().getMainWin().addOrgPage(obj, self.description)
        except:
            log.fatal(u'Ошибка режима выбора БИЗНЕС-ОБЪЕКТА <%s>' % self.name)

    def Edit(self, parent=None, context=None, UUID=None, edit_form_psp=None):
        """
        Запуск объекта на редактирование.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param UUID: Уникальный идентификатор редактируемого объекта.
        Если None, то идентификатор берется из текущего объекта.
        :param edit_form_psp: Паспорт формы для подмены стандартной формы вывода.
        :return: True-исменения успешно сохранены, False-нажата <Отмена>.
        """
        # Перед созданием формы необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()
                    
        # Создание и вывод формы
        if edit_form_psp is None:
            frm_psp = self.getEditFormPsp()
            if not frm_psp:
                frm_psp = self.createEditFormRes()
        else:
            frm_psp = edit_form_psp

        if UUID is None:
            UUID = self.getUUID()
            
        if not self.startEdit():
            # Объект заблокирован
            return False
        
        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self
            
            # Заполнение значений реквизитов через контекст
            requisite_values = self.loadRequisiteData(UUID)

            ok_save = False
            edit_values = None
            if not self.isDoEdit():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                context=context)
                frm_obj.GetContext().setValueInCtrl(frm_obj, requisite_values)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    # Сохранить реквизиты объекта
                    edit_values = frm_obj.GetContext().getValueInCtrl(frm_obj)
                    edit_ok = self.validEdit(requisite_values=edit_values, obj_uuid=UUID) if self.isValidEdit() else True
                    if edit_ok:
                        ok_save = self.saveRequisiteData(edit_values)

                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
            else:
                edit_values = self.doEdit(requisite_values=requisite_values)
                edit_ok = self.validEdit(requisite_values=edit_values, obj_uuid=UUID) if self.isValidEdit() else True
                if edit_ok:
                    ok_save = self.saveRequisiteData(edit_values)

            self.stopEdit()     # Снять блокировку

            return ok_save
        except:
            log.fatal(u'Ошибка редактирования БИЗНЕС-ОБЪЕКТА <%s>' % self.name)

        # Снять блокировку
        self.stopEdit()
        return False        
        
    def View(self, parent=None, context=None, UUID=None, view_form_psp=None):
        """
        Режим просмотра объекта.

        :param parent: Родительская форма.
        :param context: Контекст.
        :param UUID: Уникальный идентификатор.
        :param view_form_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        # Перед созданием формы необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self._createTableResource()
                    
        # Создание и вывод формы
        if view_form_psp is None:
            frm_psp = self.getViewFormPsp()
            if not frm_psp:
                frm_psp = self.createViewFormRes()
        else:
            frm_psp = view_form_psp

        if UUID is None:
            UUID = self.getUUID()

        try:
            # Сначала полностью проинициализировать контекст
            if context is None:
                context = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            context['OBJ'] = self
            
            # Заполнение значений по умолчанию реквизитов через контекст
            requisite_values = self.loadRequisiteData(UUID)

            ok = None
            if not self.isDoView():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=parent,
                                                context=context)
                frm_obj.GetContext().setValueInCtrl(frm_obj, requisite_values)
                frm_obj.ShowModal()

                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
                ok = frm_obj.isPressOk()
            else:
                ok = self.doView(requisite_values=requisite_values)

            return ok
        except:
            log.fatal(u'Ошибка просмотра БИЗНЕС-ОБЪЕКТА <%s>' % self.name)
        return False        
    
    def Print(self, report=None, bPreview=False, eval_space=None):
        """
        Печать документа.

        :param report: Указание альтернативного отчета вывода.
            Если None, то отчет берется из спецификации.
        :param bPreview: Открыть отчет в режиме предварительного просмотра?
        :param evalSpace_: Пространство имен.
        """
        pass
        
    def Del(self, UUID=None, eval_space=None, ask=True):
        """
        Удаление документа.

        :param UUID: uuid удаляемого объекта.
        :param evalSpace_: Пространство имен.
        :param ask: Спросить об удалении?
        :return: True - удаление прошло успешно.
            False - удаление отменено по какойто причине
        """
        if UUID is None:
            log.warning(u'Не определен объект для удаления')
            return False

        # Определить можно ли удалить объект
        is_del = (not ask) or (ask and ic.dlgfunc.openAskBox(u'УДАЛЕНИЕ ОБЪЕКТА', u'Удалить текущий объект?'))
        if is_del:
            # Заполнение значений реквизитов через контекст
            del_values = self.loadRequisiteData(UUID)
            del_ok = self.validDel(requisite_values=del_values, obj_uuid=UUID) if self.isValidDel() else True
            if del_ok:
                self.delete(UUID)
            return del_ok
        return False

    def sendTo(self, to_address=None, eval_space=None):
        """
        Отправка документа.

        :param to_address: Указание адресата.
        :param evalSpace_: Пространство имен.
        """
        pass

    def saveRequisite(self):
        """
        Сохранить в хранилище значения реквизитов.
        """
        storage = self.getWorkStorage()
        storage.saveObject(self)

    def save_obj(self, UUID=None):
        """
        Сохранить внутренние данные документа в хранилище.
        ВНИМАНИЕ! Метод нельзя называть save, т.к.
        будет происходить переопределение метода save
        в персистент классе.

        :param UUID: Идентификатор документа.
        Если None, то сохранить текущий документ.
        """
        if UUID is not None:
            self.uuid = UUID   # Запомнить идентификатор документа
        # log.debug(u'Запись объекта <%s>' % self.uuid)
        if self.uuid is None:
            log.warning(u'Не определен UUID объекта. Запись не возможна')
        else:
            storage = self.getWorkStorage()
            storage.saveObject(self)

    # Другое наименование метода
    # ВНИМАНИЕ! Метод нельзя называть save, т.к.
    # будет происходить переопределение метода save
    # в персистент классе.
    # save = save_obj

    def load_obj(self, UUID=None):
        """
        Загрузить внутренние данные документа из хранилища.

        :param UUID: Идентификатор документа.
        """
        if UUID is not None:
            self.uuid = UUID   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        storage.loadObject(self, self.uuid)

    def update_obj(self, UUID=None, **requisite_values):
        """
        Изменить внутренние данные документа из хранилища.

        :param UUID: Идентификатор документа.
        :param requisite_values: Словарь значений изменяемых реквизитов.
        """
        if UUID is not None:
            self.uuid = UUID   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        # Загрузить данные объекта
        storage.loadObject(self, self.uuid)
        # Установить значения реквизитов
        for requisite_name, requisite_value in requisite_values.items():
            self.setRequisiteValue(requisite_name, requisite_value)
        # Сохранить объект
        storage.saveObject(self)

    def is_obj(self, UUID=None):
        """
        Проверка на существование данных документа в хранилище.

        :param UUID: Идентификатор документа.
        :return: True/False.
        """
        if UUID is None:
             UUID = self.uuid   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        return storage.isObject(self, UUID)

    def delete_obj(self, UUID=None):
        """
        Удаление данных документа из хранилища.

        :param UUID: Идентификатор документа.
        :return: True/False.
        """
        if UUID is None:
             UUID = self.uuid   # Запомнить идентификатор документа
        # ВНИМАНИЕ! Не определен метод в icWorkStorage! Поэтому используем метод
        # в icObjPersistent. Надо бы дописать метод в icWorkStorage
        return self.delete(UUID)

    def getAllUUID(self, order_sort=None):
        """
        UUIDы всех объектов.

        :param order_sort: Порядок сортировки.
            Список имен полей, в котором надо сортировать.
        :return: Список UUID всех объектов.
        """
        storage = self.getWorkStorage()
        return storage.getAllUUID(self, order_sort=order_sort)

    def init_data(self):
        """
        Инициализация объекта.
        """
        # Генерация идентификатора документа
        self.uuid = uuidfunc.get_uuid()
        # Проинициализировать все дочерние объекты
        self.init_children_data()
        
        self.save()
        
    def init_children_data(self):
        """
        Проинициализировать все дочерние объекты.
        """
        # Проинициализировать все дочерние объекты
        for child in self.getAllRequisites():
            child.init_data()
            
    def getDocId(self):
        """
        Идентификтор документа.
        """
        return self.getUUID()

    def getRequisiteData(self):
        """
        Получить все реквизиты документа/спецификации в виде словаря.

        :return: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
        """
        try:
            return self._getRequisiteData()
        except:
            log.fatal(u'ОШИБКА определения словаря данных ДОКУМЕНТЫ <%s>' % self.name)
        return None

    def _getRequisiteData(self, parent_id=None):
        """
        Получить все реквизиты документа/спецификации в виде словаря.

        :param parent_id: Родительский идентификатор.
        """
        # Заполнить данными реквизитов
        data = {}
        for requisite in self.getChildrenRequisites():
            child_data = requisite.getValue()
            if isinstance(child_data, dict):
                # Сразу определен словарь
                data.update(child_data)
            else:
                if issubclass(requisite.__class__, icworkbase.icRequisiteBase):
                    req_data_name = requisite.getFieldName()
                elif issubclass(requisite.__class__, icworkbase.icTabRequisiteBase):
                    req_data_name = requisite.getTableName()
                    
                data[req_data_name] = child_data
                
        # Добавить идентификатор
        data['uuid'] = self.getUUID()
        return data
        
    def getRequisiteDataDefault(self):
        """
        Получить все значения по умолчанию реквизитов объекта в виде словаря.

        :return: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
        """
        # Заполнить данными реквизитов
        data = {}
        for child in self.getChildrenRequisites():
            child_data = child.getDefault()
            if isinstance(child_data, dict):
                # Сразу определен словарь
                data.update(child_data)
            else:
                data[child.name] = child_data
                
        return data
        
    def saveRequisiteData(self, requisite_data=None):
        """
        Сохранить все реквизиты объекта в хранилище.
        Данные реквизитов в виде словаря.

        :param requisite_data: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
            Если словарь значений реквизитов не определен, 
            тогда значения беруться из реквизитов.
        :return: Возвращает True-сохранение прошло удачно, False-не удачно,None-ошибка.
        """
        try:
            if requisite_data is None:
                requisite_data = self.getRequisiteData()
                
            if 'uuid' in requisite_data:
                obj_uuid = requisite_data['uuid']
            else:
                obj_uuid = self.getUUID()
            result = self.save(obj_uuid, requisite_data)
            return result
        except:
            log.fatal(u'ОШИБКА сохранения словаря данных объекта <%s>' % self.name)
        return None

    def loadRequisiteData(self, UUID=None):
        """
        Загрузить данные всех реквизитов объекта из хранилища. 
        Данные реквизитов в виде словаря.
        Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }

        :param UUID: Уникальный идентификатор объекта, если
            None, то берется текущий uuid объекта.
        :return: Данные реквизитов в виде словаря или None-ошибка.
        """
        if UUID is None:
            UUID = self.getUUID()
        try:
            requisite_data = self._load_data(UUID)
            # Идентифицировать загруженный объект
            if requisite_data:
                self.uuid = requisite_data.get('uuid', None)
            
                # Установить загруженные данные у всех реквизитов
                if isinstance(requisite_data, dict):
                    self._setRequisiteData(requisite_data)
            
            return requisite_data
        except:
            log.fatal(u'ОШИБКА загрузки словаря данных объекта <%s>' % self.name)
        return None

    def _setRequisiteData(self, requisite_data):
        """
        Установить значений реквизитов объекта из данных.

        :param requisite_data: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя табличного':[список словарей реквизитов],
                ...
                }
        :return: Возвращает True-установка прошла удачно, 
            False-не удачно,None-ошибка.
        """
        requisite_data = self._correctRequisiteData(requisite_data)
        
        if not requisite_data:
            log.warning(u'Не заполнен словарь реквизитов для сохранения в бизнес объекте <%s>' % self.name)
            return False

        try:
            for requisite in self.getChildrenRequisites():
                
                if issubclass(requisite.__class__, icworkbase.icRequisiteBase):
                    # ВНИМАНИЕ! Данные реквизита могут передаваться по имени поля таблицы
                    # и по имени реквизита. Необходимо обрабатывать оба случая.
                    req_field_name = requisite.getFieldName()
                    req_name = requisite.getName()
                    req_data_name = req_field_name if req_field_name in requisite_data else req_name
                elif issubclass(requisite.__class__, icworkbase.icTabRequisiteBase):
                    # ВНИМАНИЕ! Данные табличной части могут передаваться по имени таблицы
                    # и по имени реквизита. Необходимо обрабатывать оба случая.
                    req_tab_name = requisite.getTableName()
                    req_name = requisite.getName()
                    req_data_name = req_tab_name if req_tab_name in requisite_data else req_name
                else:
                    log.info(u'Не определен тип реквизита <%s>' % requisite)
                    return False
                
                if req_data_name in requisite_data:
                    requisite.setValue(requisite_data[req_data_name])
                else:
                    log.warning(u'Не определено значение реквизита <%s>. Используется значение по умолчанию' % req_data_name)
                    # Если данные в словаре значений не определены,
                    # тогда значение реквизита установить по умолчанию
                    requisite.setValue(requisite.getDefault())
            return True
        except:
            log.fatal(u'Ошибка в функции _setRequisiteData объекта <%s>' % self.name)
        return None

    setRequisiteData = _setRequisiteData

    def _correctRequisiteData(self, requisite_data=None):
        """
        ВНИМАНИЕ! Перед установкой необходимо скорректировать данные реквизитов.
        Для того чтобы в реквизиты NSI попадали коды справочников а не их надписи.
        Ключи кодов справочников начинаются с _ и имеют более высокий приоритет.

        :param requisite_data: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                '_имя реквизита справочника': код справочника,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
        :return: Откорректированный для установки словарь значений реквизитов.
        """
        if requisite_data is None:
            requisite_data = dict()
        
        # Берем только имена реквизитов без имен полей кодов
        requisite_names = [requisite_name for requisite_name in list(requisite_data.keys()) if not requisite_name.startswith('_')]
        for requisite_name in requisite_names:
            code_requisite_name = '_' + requisite_name
            if code_requisite_name in requisite_data:
                requisite_data[requisite_name] = requisite_data[code_requisite_name]
                del requisite_data[code_requisite_name]
                
            if isinstance(requisite_data[requisite_name], list):
                # Обработка табличных реквизитов
                for i, record in enumerate(requisite_data[requisite_name]):
                    requisite_data[requisite_name][i] = self._correctRequisiteData(record)
        return requisite_data
        
    def addRequisiteData(self, requisite_data=None):
        """
        Создать новую запись со всеми реквизиты объекта в хранилище. 
        Данные реквизитов в виде словаря.

        :param requisite_data: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
            Если словарь значений не определен, тогда значения 
            реквизитов заполняются значениями по умолчанию.
        :return: Возвращает True-сохранение прошло удачно, False-не удачно,None-ошибка.
        """
        try:
            self._setRequisiteData(requisite_data)
                
            if 'uuid' in requisite_data:
                obj_uuid = requisite_data['uuid']
            else:
                obj_uuid = uuidfunc.get_uuid()
            result = self.add(obj_uuid, requisite_data)
            return obj_uuid
        except:
            log.fatal(u'ОШИБКА сохранения словаря данных объекта <%s>' % self.name)
        return None

    def startEdit(self, UUID=None):
        """
        Запуск на редактирование.

        :return: True - запуск редактирования, 
        False - объект заблокирован.
        """
        if UUID is not None:
            self.uuid = UUID   # Запомнить идентификатор документа
            
        if not self.isLock() or self.isMyLock():
            # Поставить блокировку на документ
            self.lock()
            self.read_only = False
            return True
        else:
            # Документ заблокирован другим пользователем
            self.read_only = True
            return False
        
    def stopEdit(self):
        """
        Остановка редактирования.
        """
        if not self.read_only:
            self.unLock()

    def genAllResources(self):
        """
        Генерировать все ресурсы объекта.
        """
        self._createTableResource()
        self.createInitFormRes()        
        self.createSerachFormRes()                
        self.createEditFormRes()                
        self.createViewFormRes()
        
    def getHistory(self):
        """
        История измений состояния объекта.
        """
        return self._history_obj
    
    def findRequisite(self, requisite_name):
        """
        Найти реквизит по имени.
        Поиск ведется рекурсивно.

        :param requisite_name: Имя искомого реквизита.
        :return: Возвращает объект реквизита или None,
            если реквизит с таким именем не найден.
        """
        for requisite in self.getChildrenRequisites():
            if requisite.name == requisite_name:
                return requisite
            # Проверка стоит ли искать в дочерних реквизитах
            if hasattr(requisite, 'findRequisite'):
                find_requisite = requisite.findRequisite(requisite_name)
                # Если нашли реквизит то вернуть его
                if find_requisite:
                    return find_requisite
        return None

    # Другое наименование метода
    getRequisite = findRequisite

    def isRequisite(self, requitite_name):
        """
        Проверка есть ли такой реквизит в объекте.

        :param requitite_name: Имя реквизита.
        :return: True/False.
        """
        return self.findRequisite(requitite_name) is not None

    def setRequisiteValue(self, requisite_name, value):
        """
        Установить значение реквизита.

        :param requisite_name: Имя реквизита.
        :param value: Значение реквизита.
        :return: True/False.
        """
        requisite = self.getRequisite(requisite_name)
        if requisite:
            requisite.setValue(value)
            return True
        else:
            log.warning(u'Не определен реквизит <%s> в объекте <%s>' % (requisite_name, self.name))
        return False

    def getRequisiteValue(self, requisite_name):
        """
        Определить значение реквизита.

        :param requisite_name: Имя реквизита.
        :return: Значение реквизита или None в случае ошибки.
        """
        requisite = self.getRequisite(requisite_name)
        if requisite:
            return requisite.getValue()
        else:
            log.warning(u'Не определен реквизит <%s> в объекте <%s>' % (requisite_name, self.name))
        return None

    def getChildRequisite(self, requisite_name):
        """
        Получить объект реквизита по имени.

        :param requisite_name: Имя реквизита.
        :return: Объект реквизита или None если нет такого реквизита.
        """
        for requisite in self.getChildrenRequisites():
            if requisite.name == requisite_name:
                return requisite
        return None

    def getChildrenRequisiteData(self):
        """
        Получить данные реквизитов в виде словаря.

        :return: Заполненный словарь значений реквизитов.
            Формат:
            {...
                'Имя реквизита': значение реквизита, ...
            ...
            }
        """
        data = dict()
        for requisite in self.getChildrenRequisites():
            data[requisite.name] = requisite.getData()
        return data

    def getChildrenRequisiteStrData(self):
        """
        Получить данные реквизитов в виде словаря.

        :return: Заполненный словарь строковых значений реквизитов.
            Формат:
            {...
                'Имя реквизита': строковое значение реквизита, ...
            ...
            }
        """
        data = dict()
        for requisite in self.getChildrenRequisites():
            data[requisite.name] = requisite.getStrData()
        return data

    def getChildrenRequisiteNames(self):
        """
        Имена всех реквизитов.
        Эта функция необходима для отфильтровывания
        значений не принадлежащих к БИЗНЕС-ОБЪЕКТУ.

        :return: Список имен реквизитов.
        """
        return [requisite.name for requisite in self.getChildrenRequisites()]
