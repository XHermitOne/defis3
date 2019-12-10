#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Класс уровня справочника.
"""

from ic.components import icwidget
from ic.log import log

# Версия
__version__ = (0, 1, 1, 2)


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


class icSpravLevelInterface(object):
    """
    Класс абстрактного уровня справочника. Реализует только интерфейс.
    """

    def __init__(self, parent_sprav, index=-1):
        """
        Конструктор.
        :param parent_sprav: Справочник-родитель.
        :param index: Индекс уровня в справочнике-родителе.
        """
        self._sprav = parent_sprav
        self._index = index

    def getEditFormName(self):
        """
        Форма для редактирования данных текущего уровня.
        """
        log.warning(u'Не определен метод getEditFormName в <%s>' % self.__class__.__name__)
        return None

    def getHelpFormName(self):
        """
        Форма для выбора данных текущего уровня.
        """
        log.warning(u'Не определен метод getHelpFormName в <%s>' % self.__class__.__name__)
        return None

    def getCodLen(self):
        """
        Длина кода уровня.
        """
        log.warning(u'Не определен метод getCodLen в <%s>' % self.__class__.__name__)
        return None

    def getNoticeDict(self):
        """
        Словарь замен имен полей-реквизитов справочника.
        """
        log.warning(u'Не определен метод getNoticeDict в <%s>' % self.__class__.__name__)
        return {}

    def labelsNotice(self, labels=None):
        """
        Список замененных имен полей-реквизитов справочника.
        :param labels: Список имен полей-реквизитов, которые необходимо заменить.
        """
        log.warning(u'Не определен метод labelsNotice в <%s>' % self.__class__.__name__)
        return None

    def getIndex(self):
        """
        Индекс уровня в справочнике.
        """
        return self._index

    def getSprav(self):
        """
        Справочник-родитель.
        """
        return self._sprav

    def getRefSprav(self):
        """
        Получить ссылку на справочник.
        """
        log.warning(u'Не определен метод getRefSprav в <%s>' % self.__class__.__name__)
        return None

    def getRefLevel(self):
        """
        Получить ссылку на номер уровня связанного справочника, на который ссылается уровень.
        """
        log.warning(u'Не определен метод getRefLevel в <%s>' % self.__class__.__name__)
        return None

    def isAlienCod(self):
        """
        Признак наличия внедренного кода.
        """
        log.warning(u'Не определен метод isAlienCod в <%s>' % self.__class__.__name__)
        return False

    def getAddCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на добавление записи в справочник.
        """
        log.warning(u'Не определен метод getAddCtrl в <%s>' % self.__class__.__name__)
        return None
        
    def getUpdateCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на обновление/изменение записи в справочник.
        """
        log.warning(u'Не определен метод getUpdateCtrl в <%s>' % self.__class__.__name__)
        return None

    def getDelCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на удаление записи из справочника.
        """
        log.warning(u'Не определен метод getDelCtrl в <%s>' % self.__class__.__name__)
        return None

    def isNext(self):
        """
        Есть ли следующий уровень в справочнике.
        """
        return bool((self.getSprav().getLevelCount() - 1) > self.getIndex())

    def getNext(self):
        """
        Следующий уровеньв справочнике.
        """
        try:
            if not self.isNext():
                return None
            next_level = self.getSprav().getLevelByIdx(self.getIndex() + 1)
            return next_level
        except:
            log.fatal(u'УРОВЕНЬ СПРАВОЧНИКА <%s> Ошибка определения следующего уровня справочника' % self.name)
        return None

    def getPrev(self):
        """
        Предыдущий уровень в справочнике.
        """
        if self._index > 0:
            return self.getSprav().getLevelByIdx(self.getIndex() - 1)
        return None

    def getTable(self):
        """
        Таблица хранения данных уровня.
        """
        return self.getSprav().getTable()


class icSpravLevelProto(icSpravLevelInterface):
    """
    Класс уровня справочника.
    """

    def __init__(self, parent_sprav, index=-1):
        """
        Конструктор.
        :param parent_sprav: Справочник-родитель.
        :param index: Индекс уровня в справочнике-родителе.
        """
        icSpravLevelInterface.__init__(self, parent_sprav, index)
        # Форма для редактирования данных текущего уровня.
        # self._edit_form_name=None
        # Форма для выбора данных текущего уровня.
        # self._help_form_name=None
        # Длина кода уровня
        # self._cod_len=None

    def labelsNotice(self, labels=None):
        """
        Список замененных имен полей-реквизитов справочника.
        :param labels: Список имен полей-реквизитов, которые необходимо заменить.
        """
        try:
            if labels is None:
                labels = ['cod', 'name', 'access',
                          's1', 's2', 's3',
                          'n1', 'n2', 'n3',
                          'f1', 'f2', 'f3']
            notice_dict = self.getNoticeDict()

            for old_label, new_label in notice_dict.items():
                if old_label in labels:
                    labels[labels.index(old_label)] = new_label
        except:
            log.fatal(u'Ошибка определения списка замен имен реквизитов')
        return labels
