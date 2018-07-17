#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Класс уровня справочника.
"""

from ic.components import icwidget
from ic.log import log

# Версия
__version__ = (0, 0, 0, 2)


# --- Спецификация ---
SPC_IC_SPRAVLEVEL = {'hlp_form': None,      # Форма для выбора кода на текушем уровне
                     'edit_form': None,     # Форма для редактирования записей справоника текушего уровня
                     'access': '',          # Права доступа
                     'len': 2,              # Длина кода уровня
                     'cod_type': 'string',  # Тип значения субкода (число/строка)
                     'description': '',     # Описание
                     'notice': {},          # Словарь описания семантики дополнительных полей данных справочника
                     'pic': None,           # Картинка-образ
                     'pic2': None,          # Картинка-образ
                     'ref_sprav': None,     # Справочник, на который ссылается текущий уровень
                     'ref_level': 0,        # Уровень кода, на который ссылается текущий уровень
                     'add_ctrl': None,      # Функция дополнительного контроля на добавление записи в справочник
                     'update_ctrl': None,   # Функция дополнительного контроля на обновление/изменение записи в справочник
                     'del_ctrl': None,      # Функция дополнительного контроля на удаление записи из справочника
    
                     '__parent__': icwidget.SPC_IC_SIMPLE,
                     }


class icSpravLevelInterface:
    """
    Класс абстрактного уровня справочника. Реализует только интерфейс.
    """

    def __init__(self, SpravParent_, Index_=-1):
        """
        Конструктор.
        @param SpravParent_: Справочник-родитель.
        @param Index_: Индекс уровня в справочнике-родителе.
        """
        self._sprav = SpravParent_
        self._index = Index_

    def getEditFormName(self):
        """
        Форма для редактирования данных текущего уровня.
        """
        return None

    def getHelpFormName(self):
        """
        Форма для выбора данных текущего уровня.
        """
        return None

    def getCodLen(self):
        """
        Длина кода уровня.
        """
        return None

    def getNoticeDict(self):
        """
        Словарь замен имен полей-реквизитов справочника.
        """
        return {}

    def labelsNotice(self, Labels_=None):
        """
        Список замененных имен полей-реквизитов справочника.
        @param Labels_: Список имен полей-реквизитов, которые необходимо заменить.
        """
        return None

    def getIndex(self):
        """
        Индекс уровня в справочнике.
        """
        return self._index

    def isNext(self):
        """
        Есть ли следующий уровень в справочнике.
        """
        return False

    def getNext(self):
        """
        Следующий уровеньв справочнике.
        """
        return None

    def getSprav(self):
        """
        Справочник-родитель.
        """
        return self._sprav

    def getRefSprav(self):
        """
        Получить ссылку на справочник.
        """
        return None

    def getRefLevel(self):
        """
        Получить ссылку на номер уровня связанного справочника, на который ссылается уровень.
        """
        return None

    def isAlienCod(self):
        """
        Признак наличия внедренного кода.
        """
        pass

    def getAddCtrl(self,*args,**kwargs):
        """
        Функция дополнительного контроля на добавление записи в справочник.
        """
        return None
        
    def getUpdateCtrl(self,*args,**kwargs):
        """
        Функция дополнительного контроля на обновление/изменение записи в справочник.
        """
        return None

    def getDelCtrl(self,*args,**kwargs):
        """
        Функция дополнительного контроля на удаление записи из справочника.
        """
        return None


class icSpravLevelPrototype(icSpravLevelInterface):
    """
    Класс уровня справочника.
    """

    def __init__(self, SpravParent_, Index_=-1):
        """
        Конструктор.
        @param SpravParent_: Справочник-родитель.
        @param Index_: Индекс уровня в справочнике-родителе.
        """
        icSpravLevelInterface.__init__(self, SpravParent_, Index_)
        # Форма для редактирования данных текущего уровня.
        # self._edit_form_name=None
        # Форма для выбора данных текущего уровня.
        # self._help_form_name=None
        # Длина кода уровня
        # self._cod_len=None

    def labelsNotice(self, Labels_=None):
        """
        Список замененных имен полей-реквизитов справочника.
        @param Labels_: Список имен полей-реквизитов, которые необходимо заменить.
        """
        try:
            if Labels_ is None:
                Labels_ = ['cod', 'name', 'access',
                           's1', 's2', 's3',
                           'n1', 'n2', 'n3',
                           'f1', 'f2', 'f3']
            notice_dict = self.getNoticeDict()

            for old_label, new_label in notice_dict.items():
                if old_label in Labels_:
                    Labels_[Labels_.index(old_label)] = new_label
        except:
            log.fatal(u'Ошибка определения списка замен имен реквизитов')
        return Labels_

    def isNext(self):
        """
        Есть ли следующий уровень в справочнике.
        """
        return bool((self._sprav.getLevelCount()-1) > self._index)

    def getNext(self):
        """
        Следующий уровеньв справочнике.
        """
        try:
            if not self.isNext():
                return None
            next_level = self._sprav.getLevelByIdx(self._index + 1)
            return next_level
        except:
            log.fatal(u'УРОВЕНЬ СПРАВОЧНИКА <%s> Ошибка определения следующего уровня справочника' % self.name)
            return None

    def getPrev(self):
        """
        Предыдущий уровеньв справочнике.
        """
        if self._index > 0:
            return self._sprav.getLevelByIdx(self._index - 1)
