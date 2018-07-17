#!/usr/bin/env python"""
# -*- coding: utf-8 -*-

"""
Табличный реквизит. 
Табличный реквизит определяет табличный атрибут объекта.
Табличный реквизит включает в себя другие реквизиты.
Описывает подчиненную таблицу объекта. 

@type SPC_IC_TAB_REQUISITE: C{dictionary}
@var SPC_IC_TAB_REQUISITE: Спецификация на ресурсное описание табличного реквизита.
Описание ключей SPC_IC_TAB_REQUISITE:

    - B{name = 'default'}: Имя.
    - B{type = 'NSIRequisite'}: Тип объекта.
    - B{description = ''}: Описание.
    - B{fields = None}: Соответствие полей таблицы и справочника, в котором храниться значения реквизита (словарь).
    - B{defaults = None}: Значения по умолчанию (словарь).
    - B{set_value = None}: Функционал, исполняемый при установке значения реквизита.
    - B{get_value = None}: Функционал, исполняемый при получениии значения реквизита.
    - B{nsi_res = None}: Ресурс справочника. Если None, то 'nsi_sprav'.
    - B{nsi_type = None}: Справочник.
    - B{auto_set = True}: Признак автоматического заполнения полей при редактировании.
"""

# --- Подключение библиотек ---
import ic
from ic.utils import resource
from ic.kernel import io_prnt

import work_flow.work_sys.icworkbase as icworkbase

# Версия
__version__ = (0, 0, 1, 1)

# --- Specifications ---
SPC_IC_TAB_REQUISITE = {'type': 'TABRequisite',
                        'name': 'default',
                        'description': '',    # Описание
    
                        # --- Свойства генерации контролов редактирования/просмотра ---
                        'grp_title': u'',  # Реквизиты могут группироваться по страницам
                                           # Страницы различаются только по русским заголовкам.
                                           # Если заголовок страницы не определен, то
                                           # считается что реквизит располагается на главной
                                           # странице 'Основные'
                        
                        'label': u'',  # Надпись реквизита
                                       # Если надпись пустая, то берется вместо надписи описание (description)
    
                        'is_init': True,  # Реквизит является инициализируемым пользователем
                        'is_view': True,  # Реквизит можно просматривать на форме просмотра
                        'is_edit': True,  # Реквизит можно редактировать на форме редактировать
    
                        # --- Таблица хранения ---
                        'table': None,  # Паспорт таблицы хранения, если None то генерируется по имени реквизита
    
                        '__parent__': icworkbase.SPC_IC_WORKBASE,
                        }

# --- Функции ---

# --- Классы ---


class icTABRequisitePrototype(icworkbase.icTabRequisiteBase):
    """
    Табличный реквизит.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        icworkbase.icTabRequisiteBase.__init__(self, Parent_)
        
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

    def getTable(self):
        """
        Таблица хранения.
        """
        if self._table is None:
            tab_name = self.getTableName()
            tab_res = resource.icGetRes(tab_name, 'tab', nameRes=tab_name)
            self._table = self.GetKernel().createObjBySpc(parent=None, res=tab_res)
        return self._table

    def getStrData(self):
        """
        Данные реквизита в строковом представлении.
        @return: Список строк реквизита.
        """
        str_data = list()
        data = self.getData()
        for rec in data:
            new_rec = dict([(name, str(value)) for name, value in rec.items()])
            str_data.append(new_rec)
        return str_data

    def del_children(self, UUID_=None):
        """
        Удалить из таблицы реквизита все записи текущего родительского объекта.
        @param UUID_: Идентификатор родительского объекта.
        Если None, то берется uuid родительского объекта.
        @return: Возвращает результат выполнения операции True/False.
        """
        if UUID_ is None:
            # Если uuid не указан явно, то взять текущий объекта
            UUID_ = self.getParent().getUUID()

        transaction = None
        try:
            tab = self.getTable()
            if tab:
                # Начать транзакцию
                transaction = tab.db.getSession()
                transaction.begin()

                # Получить данные объекта в каскадном представлении
                recs = tab.get_where(tab.c.parent == UUID_)
                rec_id = recs.first().id if recs else 0
                if rec_id:
                    result = self._delCascadeData(tab, rec_id, transaction)
                else:
                    io_prnt.outWarning(u'Не найдены дочерние записи объекта с UUID <%s>' % UUID_)
                    result = False

                # Завершить транзакцию
                transaction.commit()

                return result
        except:
            if transaction:
                # Откатить транзакцию
                transaction.rollback()
            io_prnt.outErr(u'Ошибка удаления из хранилища дочерних записей объекта [%s]' % self.getParent().name)
        return False
