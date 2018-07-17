#!/usr/bin/env python
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

@type SPC_IC_BUSINESSOBJ: C{dictionary}
@var SPC_IC_BUSINESSOBJ: Спецификация на ресурсное описание БИЗНЕСС-ОБЪЕКТА.
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
from ic.utils import ic_uuid
from ic.utils import ic_util
from ic.interfaces import icdatasetinterface

import work_flow.work_sys.icworkbase as icworkbase
from work_flow.work_sys import persistent
from work_flow.work_sys import form_generator
from STD.queries import filter_convert

# Версия
__version__ = (0, 0, 4, 2)


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
                      }


class icBusinessObjInterface(icworkbase.icWorkBase, persistent.icObjPersistent, form_generator.icObjFormGenerator, icdatasetinterface.icDatasetInterface):
    """
    Интерфейс абстрактного бизнес-объекта.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icWorkBase.__init__(self, Parent_)
        
        persistent.icObjPersistent.__init__(self, Parent_)
        form_generator.icObjFormGenerator.__init__(self, Parent_)
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
       
    def Init(self, ParentForm_=None, Context_=None, auto_add=False,
             init_form_psp=None):
        """
        Запуск инициализации/создания.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param auto_add: Признак автодобавления в БД.
        @param init_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Init> in class %s' % self.__class__.__name__

    Add = Init

    def Edit(self, ParentForm_=None, Context_=None, UUID_=None,
             edit_form_psp=None):
        """
        Запуск на редактирование.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param UUID_: Уникальный идентификатор редактируемого объекта.
            Если None, то уникальный идентификатор self.uuid
        @param edit_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Edit> in class %s' % self.__class__.__name__
        
    def View(self, ParentForm_=None, Context_=None, UUID_=None,
             view_form_psp=None):
        """
        Режим просмотра.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param view_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <View> in class %s' % self.__class__.__name__
    
    def Search(self, ParentForm_=None, Context_=None,
               search_form_psp=None):
        """
        Режим поиска объекта.
        @param ParentForm_: Родительская форма.
        @param Context_:Контекст.
        @param search_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Search> in class %s' % self.__class__.__name__
    
    def Choice(self, ParentForm_=None, Context_=None,
               choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.
        @param ParentForm_: Родительская форма.
        @param Context_:Контекст.
        @param choice_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <Choice> in class %s' % self.__class__.__name__

    def Browse(self, ParentForm_=None, Context_=None,
               choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.
        В виде страницы главного нотебука.
        @param ParentForm_: Родительская форма.
        @param Context_:Контекст.
        @param choice_from_psp: Паспорт формы для подмены стандартной формы вывода.
        """
        assert None, 'Abstract method <ChoicePage> in class %s' % self.__class__.__name__

    def Print(self, Report_=None, Preview_=False, evalSpace=None):
        """
        Печать.
        @param Report_: Указание альтернативного отчета вывода.
            Если None, то отчет берется из спецификации.
        @param Preview_: Открыть отчет в режиме предварительного просмотра?
        @param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <Print> in class %s' % self.__class__.__name__
    
    def Del(self, UUID_=None, evalSpace=None):
        """
        Удаление.
        @param UUID_: uuid удаляемого объекта.
        @param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <Del> in class %s' % self.__class__.__name__
        
    def SendTo(self, To_=None, evalSpace=None):
        """
        Отправка.
        @param To_: Указание адресата.
        @param evalSpace_: Пространство имен.
        """
        assert None, 'Abstract method <SendTo> in class %s' % self.__class__.__name__
    
    def save_obj(self, UUID_=None):
        """
        Сохранить внутренние данные в хранилище.
        @param UUID_: Идентификатор. Если None, то сохранить текущий.
        """
        assert None, 'Abstract method <save_obj> in class %s' % self.__class__.__name__
        
    def load_obj(self, UUID_=None):
        """
        Загрузить внутренние данные из хранилища.
        @param UUID_: Идентификатор.
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
        
    def startEdit(self, UUID_=None):
        """
        Запуск на редактирование.
        """
        assert None, 'Abstract method <startEdit> in class %s' % self.__class__.__name__
        
    def stopEdit(self):
        """
        Остановка редактирования.
        """
        assert None, 'Abstract method <stopEdit> in class %s' % self.__class__.__name__


class icBusinessObjPrototype(icBusinessObjInterface):
    """
    Бизнесс-объект.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icBusinessObjInterface.__init__(self, Parent_)
        
        # Описание объекта. Храниться в таблице для каждого объекта

        # Словарь всех реквизитов.
        # Инициализируется непосредственно в конструкторе компонента.
        self.requisites = {}
        
        # История изменения состояний объекта
        self._history_obj = None

    def isDoInit(self):
        """
        Определена функция инициализации?
        @return: True/False.
        """
        return False

    def isDoEdit(self):
        """
        Определена функция редактирования?
        @return: True/False.
        """
        return False

    def isDoView(self):
        """
        Определена функция просмотра?
        @return: True/False.
        """
        return False

    def isDoSearch(self):
        """
        Определена функция поиска?
        @return: True/False.
        """
        return False

    def isDoChoice(self):
        """
        Определена функция выбора?
        @return: True/False.
        """
        return False

    def doInit(self, *args, **kwargs):
        """
        Функция инициализации.
        @return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def doEdit(self, *args, **kwargs):
        """
        Функция редактирования.
        @return: Объект функции редактирования,
            или None если не определена.
        """
        return None

    def doView(self, *args, **kwargs):
        """
        Функция просмотра.
        @return: Объект функции просмотра,
            или None если не определена.
        """
        return None

    def doSearch(self, *args, **kwargs):
        """
        Функция поиска.
        @return: Объект функции поиска,
            или None если не определена.
        """
        return None

    def doChoice(self, *args, **kwargs):
        """
        Функция выбора.
        @return: Объект функции выбора,
            или None если не определена.
        """
        return None

    def isValidInit(self):
        """
        Определена функция валидации при инициализации?
        @return: True/False.
        """
        return False

    def isValidEdit(self):
        """
        Определена функция валидации при редактировании?
        @return: True/False.
        """
        return False

    def isValidDel(self):
        """
        Определена функция валидации при удалении?
        @return: True/False.
        """
        return False

    def validInit(self, *args, **kwargs):
        """
        Функция валидации при инициализации.
        @return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def validEdit(self, *args, **kwargs):
        """
        Функция валидации при редактировании.
        @return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def validDel(self, *args, **kwargs):
        """
        Функция валидации при удалении.
        @return: Объект функции инициализации,
            или None если не определена.
        """
        return None

    def getObjDescription(self, UUID_=None):
        """
        Описание бизнес-объекта  предметной области.
        @param UUID_: Уникальный идентификатор объекта.
        """
        if UUID_ is not None:
            self.loadRequisiteData(UUID_)
            
        description = u' '.join([ic_util.toUnicode(requisite.getValue()) for requisite in self.getChildrenRequisites() if requisite.isDescription()])

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
        
    def Init(self, ParentForm_=None, Context_=None, auto_add=False,
             init_form_psp=None):
        """
        Запуск инициализации/создания.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param auto_add: Признак автодобавления в БД.
        @param init_from_psp: Паспорт формы для подмены стандартной формы вывода.
        @return: Словарь нового объекта или None в случае ошибки.
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
            if Context_ is None:
                Context_ = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self
            
            # Заполнение значений по умолчанию реквизитов через контекст
            requisite_values = self.getRequisiteDataDefault()

            init_values = None
            if not self.isDoInit():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                context=Context_)
                frm_obj.GetContext().setValueInCtrl(frm_obj, requisite_values)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    # Сохранить реквизиты доокумента
                    init_values = frm_obj.GetContext().getValueInCtrl(frm_obj)
                    if auto_add:
                        add_ok = self.validInit(requisite_values=init_values) if self.isValidInit() else True
                        if add_ok:
                            uuid_new_obj = self.addRequisiteData(init_values)
                            ic.io_prnt.outLog(u'Автодобавление объекта [%s] в <%s>' % (uuid_new_obj, self.name))

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
                        ic.io_prnt.outLog(u'Автодобавление объекта [%s] в <%s>' % (uuid_new_obj, self.name))

            # Сохранение реквизитов не произошло
            return init_values
        except:
            ic.io_prnt.outErr(u'Ошибка  инициализации БИЗНЕС-ОБЪЕКТА <%s>' % self.name)
        return None

    Add = Init

    def Search(self, ParentForm_=None, Context_=None,
               search_form_psp=None):
        """
        Режим поиска объекта.
        @param ParentForm_: Родительская форма.
        @param Context_: Пространство имен.
        @param search_from_psp: Паспорт формы для подмены стандартной формы вывода.
        @return: Возвращает UUID выбранного объекта или None,
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
            if Context_ is None:
                Context_ = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self

            obj_uuid = None
            if not self.isDoSearch():
                # Создать и открыть форму
                panel_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                  context=Context_)
                
                # Создать и открыть форму
                frm_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                context=Context_)
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
            ic.io_prnt.outErr(u'Ошибка режима поиска БИЗНЕС-ОБЪЕКТА %s' % self.name)
        
    def Choice(self, ParentForm_=None, Context_=None,
               choice_form_psp=None):
        """
        Режим выбора объекта сэлементом поиска/фильтра.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст формы.
        @param choice_from_psp: Паспорт формы для подмены стандартной формы вывода.
        @return: Возвращает UUID выбранного объекта или None,
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
            if Context_ is None:
                Context_ = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self

            obj_uuid = None
            if not self.isDoChoice():
                # Создать и открыть форму
                frm_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                context=Context_)
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
            ic.io_prnt.outErr(u'Ошибка режима выбора БИЗНЕС-ОБЪЕКТА <%s>' % self.name)

    def Browse(self, ParentForm_=None, Context_=None,
               choice_form_psp=None):
        """
        Режим выбора объекта с элементом поиска/фильтра.
        В виде страницы главного нотебука.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param choice_form_psp: Паспорт формы для подмены стандартной формы вывода.
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
            if Context_ is None:
                Context_ = self.GetContext()

            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self

            # Создать и открыть
            obj = ic.getKernel().Create(psp, parent=ParentForm_, context=Context_)
            ic.getKernel().GetContext().getMainWin().AddOrgPage(obj, self.description)
        except:
            ic.io_prnt.outErr(u'Ошибка режима выбора БИЗНЕС-ОБЪЕКТА <%s>' % self.name)

    def Edit(self, ParentForm_=None, Context_=None, UUID_=None,
             edit_form_psp=None):
        """
        Запуск объекта на редактирование.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param UUID_: Уникальный идентификатор редактируемого объекта.
        Если None, то идентификатор берется из текущего объекта.
        @param edit_from_psp: Паспорт формы для подмены стандартной формы вывода.
        @return: True-исменения успешно сохранены, False-нажата <Отмена>.
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

        if UUID_ is None:
            UUID_ = self.getUUID()
            
        if not self.startEdit():
            # Объект заблокирован
            return False
        
        try:
            # Сначала полностью проинициализировать контекст
            if Context_ is None:
                Context_ = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self
            
            # Заполнение значений реквизитов через контекст
            requisite_values = self.loadRequisiteData(UUID_)

            ok_save = False
            edit_values = None
            if not self.isDoEdit():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                context=Context_)
                frm_obj.GetContext().setValueInCtrl(frm_obj, requisite_values)
                frm_obj.ShowModal()

                if frm_obj.isPressOk():
                    # Сохранить реквизиты объекта
                    edit_values = frm_obj.GetContext().getValueInCtrl(frm_obj)
                    edit_ok = self.validEdit(requisite_values=edit_values, obj_uuid=UUID_) if self.isValidEdit() else True
                    if edit_ok:
                        ok_save = self.saveRequisiteData(edit_values)

                # ВНИМАНИЕ!
                # Обязательно удалять форму после использования, а то
                # остаются ссылки на нее
                frm_obj.Destroy()
            else:
                edit_values = self.doEdit(requisite_values=requisite_values)
                edit_ok = self.validEdit(requisite_values=edit_values, obj_uuid=UUID_) if self.isValidEdit() else True
                if edit_ok:
                    ok_save = self.saveRequisiteData(edit_values)

            self.stopEdit()     # Снять блокировку

            return ok_save
        except:
            ic.io_prnt.outErr(u'Ошибка редактирования БИЗНЕС-ОБЪЕКТА <%s>' % self.name)

        # Снять блокировку
        self.stopEdit()
        return False        
        
    def View(self, ParentForm_=None, Context_=None, UUID_=None,
             view_form_psp=None):
        """
        Режим просмотра объекта.
        @param ParentForm_: Родительская форма.
        @param Context_: Контекст.
        @param UUID_: Уникальный идентификатор.
        @param view_from_psp: Паспорт формы для подмены стандартной формы вывода.
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

        if UUID_ is None:
            UUID_ = self.getUUID()

        try:
            # Сначала полностью проинициализировать контекст
            if Context_ is None:
                Context_ = self.GetContext()
                
            # Добавить в пространство имен указатель на текущий БИЗНЕС-ОБЪЕКТ
            Context_['OBJ'] = self
            
            # Заполнение значений по умолчанию реквизитов через контекст
            requisite_values = self.loadRequisiteData(UUID_)

            ok = None
            if not self.isDoView():
                # Создать и открыть форму инициализации документа
                frm_obj = ic.getKernel().Create(frm_psp, parent=ParentForm_,
                                                context=Context_)
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
            ic.io_prnt.outErr(u'Ошибка просмотра БИЗНЕС-ОБЪЕКТА <%s>' % self.name)
        return False        
    
    def Print(self, Report_=None, Preview_=False, evalSpace=None):
        """
        Печать документа.
        @param Report_: Указание альтернативного отчета вывода.
            Если None, то отчет берется из спецификации.
        @param Preview_: Открыть отчет в режиме предварительного просмотра?
        @param evalSpace_: Пространство имен.
        """
        pass
        
    def Del(self, UUID_=None, evalSpace=None, ask=True):
        """
        Удаление документа.
        @param UUID_: uuid удаляемого объекта.
        @param evalSpace_: Пространство имен.
        @param ask: Спросить об удалении?
        @return: True - удаление прошло успешно.
            False - удаление отменено по какойто причине
        """
        if UUID_ is None:
            ic.io_prnt.outWarning(u'Не определен объект для удаления')
            return False

        # Определить можно ли удалить объект
        is_del = (not ask) or (ask and ic.ic_dlg.icAskBox(u'УДАЛЕНИЕ ОБЪЕКТА', u'Удалить текущий объект?'))
        if is_del:
            # Заполнение значений реквизитов через контекст
            del_values = self.loadRequisiteData(UUID_)
            del_ok = self.validDel(requisite_values=del_values, obj_uuid=UUID_) if self.isValidDel() else True
            if del_ok:
                self.delete(UUID_)
            return del_ok
        return False

    def SendTo(self, To_=None, evalSpace=None):
        """
        Отправка документа.
        @param To_: Указание адресата.
        @param evalSpace_: Пространство имен.
        """
        pass

    def saveRequisite(self):
        """
        Сохранить в хранилище значения реквизитов.
        """
        storage = self.getWorkStorage()
        storage.saveObject(self)

    def save_obj(self, UUID_=None):
        """
        Сохранить внутренние данные документа в хранилище.
        ВНИМАНИЕ! Метод нельзя называть save, т.к.
        будет происходить переопределение метода save
        в персистент классе.
        @param UUID_: Идентификатор документа. 
        Если None, то сохранить текущий документ.
        """
        if UUID_ is not None:
            self.uuid = UUID_   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        storage.saveObject(self)

    # Другое наименование метода
    # ВНИМАНИЕ! Метод нельзя называть save, т.к.
    # будет происходить переопределение метода save
    # в персистент классе.
    # save = save_obj

    def load_obj(self, UUID_=None):
        """
        Загрузить внутренние данные документа из хранилища.
        @param UUID_: Идентификатор документа.
        """
        if UUID_ is not None:
            self.uuid = UUID_   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        storage.loadObject(self, self.uuid)

    def update_obj(self, UUID_=None, **requisite_values):
        """
        Изменить внутренние данные документа из хранилища.
        @param UUID_: Идентификатор документа.
        @param requisite_values: Словарь значений изменяемых реквизитов.
        """
        if UUID_ is not None:
            self.uuid = UUID_   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        # Загрузить данные объекта
        storage.loadObject(self, self.uuid)
        # Установить значения реквизитов
        for requisite_name, requisite_value in requisite_values.items():
            self.setRequisiteValue(requisite_name, requisite_value)
        # Сохранить объект
        storage.saveObject(self)

    def is_obj(self, UUID_=None):
        """
        Проверка на существование данных документа в хранилище.
        @param UUID_: Идентификатор документа.
        @return: True/False.
        """
        if UUID_ is None:
             UUID_ = self.uuid   # Запомнить идентификатор документа
        storage = self.getWorkStorage()
        return storage.isObject(self, UUID_)

    def delete_obj(self, UUID_=None):
        """
        Удаление данных документа из хранилища.
        @param UUID_: Идентификатор документа.
        @return: True/False.
        """
        if UUID_ is None:
             UUID_ = self.uuid   # Запомнить идентификатор документа
        # ВНИМАНИЕ! Не определен метод в icWorkStorage! Поэтому используем метод
        # в icObjPersistent. Надо бы дописать метод в icWorkStorage
        return self.delete(UUID_)

    def getAllUUID(self, order_sort=None):
        """
        UUIDы всех объектов.
        @param order_sort: Порядок сортировки.
            Список имен полей, в котором надо сортировать.
        @return: Список UUID всех объектов.
        """
        storage = self.getWorkStorage()
        return storage.getAllUUID(self, order_sort=order_sort)

    def init_data(self):
        """
        Инициализация объекта.
        """
        # Генерация идентификатора документа
        self.uuid = ic_uuid.get_uuid()
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
        @return: Словарь значений реквизитов.
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
            ic.io_prnt.outErr(u'ОШИБКА определения словаря данных ДОКУМЕНТЫ <%s>' % self.name)
            return None

    def _getRequisiteData(self, ParentID_=None):
        """
        Получить все реквизиты документа/спецификации в виде словаря.
        @param ParentID_: Родительский идентификатор.
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
        @return: Словарь значений реквизитов.
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
        
    def saveRequisiteData(self, RequisiteData_=None):
        """
        Сохранить все реквизиты объекта в хранилище. Данные реквизитов в виде словаря.
        @param RequisiteData_: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
            Если словарь значений реквизитов не определен, 
            тогда значения беруться из реквизитов.
        @return: Возвращает True-сохранение прошло удачно, False-не удачно,None-ошибка.
        """
        try:
            if RequisiteData_ is None:
                RequisiteData_ = self.getRequisiteData()
                
            if 'uuid' in RequisiteData_:
                obj_uuid = RequisiteData_['uuid']
            else:
                obj_uuid = self.getUUID()
            result = self.save(obj_uuid, RequisiteData_)
            return result
        except:
            ic.io_prnt.outErr(u'ОШИБКА сохранения словаря данных объекта <%s>' % self.name)
            return None

    def loadRequisiteData(self, UUID_=None):
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
        @param UUID_: Уникальный идентификатор объекта, если
            None, то берется текущий uuid объекта.
        @return: Данные реквизитов в виде словаря или None-ошибка.
        """
        if UUID_ is None:
            UUID_ = self.getUUID()
        try:
            requisite_data = self._load_data(UUID_)
            # Идентифицировать загруженный объект
            if requisite_data:
                self.uuid = requisite_data.get('uuid', None)
            
                # Установить загруженные данные у всех реквизитов
                if isinstance(requisite_data, dict):
                    self._setRequisiteData(requisite_data)
            
            return requisite_data
        except:
            ic.io_prnt.outErr(u'ОШИБКА загрузки словаря данных объекта <%s>' % self.name)
            return None

    def _setRequisiteData(self, RequisiteData_):
        """
        Установить значений реквизитов объекта из данных.
        @param RequisiteData_: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя табличного':[список словарей реквизитов],
                ...
                }
        @return: Возвращает True-установка прошла удачно, 
            False-не удачно,None-ошибка.
        """
        if not RequisiteData_:
            ic.io_prnt.outWarning(u'Не заполнен словарь реквизитов для сохранения в бизнес объекте <%s>' % self.name)
            return False

        try:
            for requisite in self.getChildrenRequisites():
                
                if issubclass(requisite.__class__, icworkbase.icRequisiteBase):
                    # ВНИМАНИЕ! Данные реквизита могут передаваться по имени поля таблицы
                    # и по имени реквизита. Необходимо обрабатывать оба случая.
                    req_field_name = requisite.getFieldName()
                    req_name = requisite.getName()
                    req_data_name = req_field_name if req_field_name in RequisiteData_ else req_name
                elif issubclass(requisite.__class__, icworkbase.icTabRequisiteBase):
                    # ВНИМАНИЕ! Данные табличной части могут передаваться по имени таблицы
                    # и по имени реквизита. Необходимо обрабатывать оба случая.
                    req_tab_name = requisite.getTableName()
                    req_name = requisite.getName()
                    req_data_name = req_tab_name if req_tab_name in RequisiteData_ else req_name
                else:
                    ic.io_prnt.outLog(u'Не определен тип реквизита <%s>' % requisite)
                    return False
                
                if req_data_name in RequisiteData_:
                    requisite.setValue(RequisiteData_[req_data_name])
                else:
                    ic.io_prnt.outWarning(u'Не определено значение реквизита <%s>. Используется значение по умолчанию' % req_data_name)
                    # Если данные в словаре значений не определены,
                    # тогда значение реквизита установить по умолчанию
                    requisite.setValue(requisite.getDefault())
            return True
        except:
            ic.io_prnt.outErr(u'Ошибка в функции _setRequisiteData объекта <%s>' % self.name)
            return None

    setRequisiteData = _setRequisiteData

    def addRequisiteData(self, RequisiteData_=None):
        """
        Создать новую запись со всеми реквизиты объекта в хранилище. 
        Данные реквизитов в виде словаря.
        @param RequisiteData_: Словарь значений реквизитов.
            Словарь реквизитов представлен в виде 
                {
                'имя реквизита':значение реквизита,
                ...
                'имя спецификации документа':[список словарей реквизитов],
                ...
                }
            Если словарь значений не определен, тогда значения 
            реквизитов заполняются значениями по умолчанию.
        @return: Возвращает True-сохранение прошло удачно, False-не удачно,None-ошибка.
        """
        try:
            if RequisiteData_ is None:
                RequisiteData_ = {}
            self._setRequisiteData(RequisiteData_)
                
            if 'uuid' in RequisiteData_:
                obj_uuid = RequisiteData_['uuid']
            else:
                obj_uuid = ic_uuid.get_uuid()
            result = self.add(obj_uuid, RequisiteData_)
            return obj_uuid
        except:
            ic.io_prnt.outErr(u'ОШИБКА сохранения словаря данных объекта <%s>' % self.name)
            return None

    def startEdit(self, UUID_=None):
        """
        Запуск на редактирование.
        @return: True - запуск редактирования, 
        False - объект заблокирован.
        """
        if UUID_ is not None:
            self.uuid = UUID_   # Запомнить идентификатор документа
            
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
    
    def findRequisite(self, RequisiteName_):
        """
        Найти реквизит по имени.
        Поиск ведется рекурсивно.
        @param RequisiteName_: Имя искомого реквизита.
        @return: Возвращает объект реквизита или None,
            если реквизит с таким именем не найден.
        """
        for requisite in self.getChildrenRequisites():
            if requisite.name == RequisiteName_:
                return requisite
            # Проверка стоит ли искать в дочерних реквизитах
            if hasattr(requisite, 'findRequisite'):
                find_requisite = requisite.findRequisite(RequisiteName_)
                # Если нашли реквизит то вернуть его
                if find_requisite:
                    return find_requisite
        return None

    # Другое наименование метода
    getRequisite = findRequisite

    def isRequisite(self, requitite_name):
        """
        Проверка есть ли такой реквизит в объекте.
        @param requitite_name: Имя реквизита.
        @return: True/False.
        """
        return self.findRequisite(requitite_name) is not None

    def setRequisiteValue(self, requisite_name, value):
        """
        Установить значение реквизита.
        @param requisite_name: Имя реквизита.
        @param value: Значение реквизита.
        @return: True/False.
        """
        requisite = self.getRequisite(requisite_name)
        if requisite:
            requisite.setValue(value)
            return True
        else:
            ic.io_prnt.outWarning(u'Не определен реквизит <%s> в объекте <%s>' % (requisite_name, self.name))
        return False

    def getRequisiteValue(self, requisite_name):
        """
        Определить значение реквизита.
        @param requisite_name: Имя реквизита.
        @return: Значение реквизита или None в случае ошибки.
        """
        requisite = self.getRequisite(requisite_name)
        if requisite:
            return requisite.getValue()
        else:
            ic.io_prnt.outWarning(u'Не определен реквизит <%s> в объекте <%s>' % (requisite_name, self.name))
        return None

    def getChildRequisite(self, requisite_name):
        """
        Получить объект реквизита по имени.
        @param requisite_name: Имя реквизита.
        @return: Объект реквизита или None если нет такого реквизита.
        """
        for requisite in self.getChildrenRequisites():
            if requisite.name == requisite_name:
                return requisite
        return None

    def getChildrenRequisiteData(self):
        """
        Получить данные реквизитов в виде словаря.
        @return: Заполненный словарь значений реквизитов.
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
        @return: Заполненный словарь строковых значений реквизитов.
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
        @return: Список имен реквизитов.
        """
        return [requisite.name for requisite in self.getChildrenRequisites()]
