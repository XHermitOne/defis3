#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс объекта-ссылки/справочника.

Объект-ссылка отличается от справочника тем что
организует свое хранение в виде каскада таблиц уровней.

На каждом уровне таблица содержит поля code и status.
code - код объекта-ссылки/справочника.
status - вкл./выкл. объекта.
"""

from ic.components import icwidget

from ic.log import log
from ic.utils import system_cache
from ic.engine import glob_functions
from ic.dlg import dlgfunc
from ic.utils import coderror

from . import icsprav
from ..nsi_dlg import icspraveditdlg
from ..nsi_dlg import icspravchoicetreedlg

# Версия
__version__ = (0, 1, 1, 1)

# Спецификация
SPC_IC_REFOBJECT = {'type': 'RefObject',
                    'name': 'default',
                    'description': '',      # Описание справочника

                    'db': None,             # Паспорт БД хранения данных
                    'cache': True,          # Автоматически кэшировать?
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    '__attr_hlp__': {'db': u'Паспорт БД хранения данных',
                                     'cache': u'Автоматически кэшировать?',
                                     },
                    }


class icRefObjectProto(icsprav.icSpravInterface):
    """
    Класс объекта-ссылки/справочника.
    """

    def __init__(self, sprav_manager=None, name=None):
        """
        Конструктор.

        :param sprav_manager: Объект менеджера справочника.
        :param name: Имя справочника в списке менеджера справочников.
        """
        icsprav.icSpravInterface.__init__(self, sprav_manager, name)

    def Edit(self, parent_code=(None,), parent=None):
        """
        Запуск окна редактирования объекта-ссылки/справочника.

        :param parent_code: Код более верхнего уровня.
        :param parent: Родительская форма.
            Если не определена, то берется главная форма.
        :return: Возвращает результат выполнения опереции True/False.
        """
        # Перед редактированием необходмо создать
        # все ресурсы таблиц хранения объекта, если
        # их нет
        self.createLevelTabRes()

        if parent is None:
            parent = glob_functions.getMainWin()

        try:
            return icspraveditdlg.edit_sprav_dlg(parent=parent, nsi_sprav=self)
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка редактирования' % self.name)
            return False

    def getLevels(self):
        """
        Список уровней объекта-ссылки/справочника.
        """
        log.warning(u'Не определен метод получения списка уровней объекта-ссылки/справочника в <%s>' % self.__class__.__name__)
        return list()

    def getLevel(self, level_id=0):
        """
        Получить уровень объекта-ссылки/справочника.

        :param level_id: Идентификатор уровня.
            Может быть как индексом так и наменованием уровня.
        :return: Объект уровня или None если уровень не найден.
        """
        levels = self.getLevels()
        if isinstance(level_id, int):
            # Идентификатор уровня задается индексом
            if 0 <= level_id < len(levels):
                return levels[level_id]
        elif isinstance(level_id, str):
            # Идентификатор уровня задается как имя
            level_names = [level.getName() for level in levels]
            if level_id in level_names:
                level_idx = level_names.index(level_id)
                return levels[level_idx]
        return None

    def createLevelTabRes(self):
        """
        Создать все ресурсы таблиц всех уровней объекта-ссылки/справочника.

        :return: True/False.
        """
        levels = self.getLevels()
        if levels:
            for level in levels:
                level.genTableRes()
            return True
        return False

    def getTable(self, index=0):
        """
        Таблица объекта-ссылки.
        Считаем что это таблица уровня.

        :param index: Индекс уровня объекта-ссылки.
            Если не определен, то берется первый уровень.
        """
        levels = self.getLevels()
        if levels:
            try:
                return levels[index].getTable()
            except IndexError:
                log.fatal(u'Ошибка получения таблицы объекта-ссылки/справочника <%s>' % self.getName())
        return None

    def Hlp(self, parent_code=(None,), field=None, form=None, parent=None, dt=None,
            default_selected_code=None, view_fields=None, search_fields=None):
        """
        Запуск визуального интерфейса просмотра,  поиска и выбора значений поля
            или группы полей из отмеченной строки указанного объекта-ссылки/справочника.

        :type parent_code: C{...}
        :param parent_code: Код более верхнего уровня.
        :param field: Задает поле или группу полей, которые надо вернуть.
            Полу задается строкой. Поля задаются словарем.
        :param form: имя формы визуального интерфейса работы со справочником.
        :param parent: Родительская форма.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :param default_selected_code: Выбранный код по умолчанию.
            Если None, то ничего не выбирается.
        :param view_fields: Список имен полей для просмотра.
            Если не определено то отображаются <Код> и <Наименование>.
        :param search_fields: Список имен полей для поиска.
            Если не определено то поиск только по <Код> и <Наименование>.
        :return: Код ошибки, Результат выбора
        """
        result = coderror.IC_HLP_OK
        res_val = None

        try:
            if parent_code is None:
                parent_code = (None,)

            # Для обработки необходимо преобразовать в список
            parent_code = list(parent_code)
            # Запрашиваемый уровень
            x_level = parent_code.index(None)

            # Если запрашиваемый уровень больше общего количества уровней, то выйти
            # Нет такого уровня в справочнике
            if self.getLevelCount() <= x_level:
                log.warning(u'Не корректный номер уровня %d' % x_level)
                return coderror.IC_HLP_FAILED_LEVEL, res_val

            # определить длину кода уровня
            level_len = self.getLevels()[x_level].getCodLen()

            if level_len is None:
                dlgfunc.openMsgBox(u'ОШИБКА', u'Не определена длина кода уровня!')
                return coderror.IC_HLP_FAILED_LEVEL, res_val

            # Обработка штатной функцией
            code = icspravchoicetreedlg.choice_sprav_dlg(parent=parent,
                                                         nsi_sprav=self,
                                                         fields=view_fields,
                                                         default_selected_code=default_selected_code,
                                                         search_fields=search_fields)
            if code:
                return coderror.IC_HLP_OK, code, self.getFields(field, code)
            return coderror.IC_HLP_FAILED_IGNORE, code, None
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка в методе Hlp/Choice' % self._name)
            result = coderror.IC_HLP_FAILED_TYPE_SPRAV

        return result, res_val, self.getFields(field, res_val)

    def addRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Добавить запись в справочник по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции True/False.
        """
        level = self.getLevelByCod(cod)
        if level:
            # Контроль на уровне
            add_ctrl_result = level.getAddCtrl(locals())
            if add_ctrl_result is None:
                # Контроля производить не надо
                return self._addRec(cod, record_dict, dt, bClearCache)
            elif add_ctrl_result == coderror.IC_CTRL_OK:
                # Контроль успешный
                return self._addRec(cod, record_dict, dt, bClearCache)
            elif add_ctrl_result in (coderror.IC_CTRL_FAILED,
                                     coderror.IC_CTRL_FAILED_IGNORE,
                                     coderror.IC_CTRL_FAILED_TYPE_SPRAV,
                                     coderror.IC_CTRL_FAILED_LOCK):
                # Контроль не прошел
                log.warning(u'Не прошел контроль добавления записи в объекте-ссылке/справочник [%s]. Код ошибки: <%d>' %
                            (self.getName(), add_ctrl_result))

        return False

    def _addRec(self, cod, record_dict, dt=None, bClearCache=False):
        """
        Добавить запись в справочник по коду.

        :param cod: Код.
        :param record_dict: Словарь изменений.
        :param dt: Период актуальности.
        :param bClearCache: Обновить кеш?
        :return: Возвращает результат выполнения операции True/False.
        """
        storage = self.getStorage()
        if storage:
            if storage.isCod(cod):
                result = storage.updateRecByCod(cod, record_dict, dt)
            else:
                record_dict['cod'] = cod
                result = storage.addRecDictDataTab(record_dict)
            # Если запись прошла удачно, то сбросить кэш
            if bClearCache:
                self.clearInCache()
            return result

        return False

    def Find(self, cod, field='name', dt=None):
        """
        Поиск по коду.

        :type cod: C{...}
        :param cod: Код строки справочника.
        :type field: C{string | list }
        :param field: Имя поля или список полей.
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :rtype: C{dictionary}
        :return: Значение либо словарь значений (если поле field задает список полей).
            None, если строка с заданным кодом не найдена.
        """
        if isinstance(field, str):
            fields = [field]
            is_return_dict = False
        else:
            fields = [x for x in field]
            is_return_dict = True

        # Формируем словарь соотношений для функции контроля
        field_dict = dict([(field_name, field_name) for field_name in fields])

        # Используем функцию для контроля. Она возвращает словарь значений.
        level_cod = self.getParentLevelCod(cod)
        log.debug(u'Код родительского уровня <%s>' % level_cod)
        ctrl_cod, ctrl_dict = self.Ctrl(cod, None, 'cod', field_dict, cod=level_cod, dt=dt)

        if ctrl_cod != coderror.IC_CTRL_OK:
            result = None
        elif is_return_dict:
            result = ctrl_dict
        else:
            result = ctrl_dict[field]

        return result

    def Ctrl(self, val, old=None, field='name', flds=None, bCount=True, cod='', dt=None):
        """
        Функция контроля наличия в справочнике значения поля
        с указанным значением.

        :type cod: C{string}
        :param cod: Начальная подстрока структурного кода, ограничивающая множество возможных кодов.
        :type val: C{...}
        :param val: Проверяемое значение. Если тип картеж, то это означает, что проверяем структурное
            значение (например иерархический код справочника).
        :type old: C{...}
        :param old: Старое значение.
        :type field: C{string}
        :param field: Поле, по которому проверяется значение.
        :type flds: C{dictionary}
        :param flds: Словарь соответствий между полями определенного класса данных и
            полями справочника. Если контроль значения пройдет успешно, то
            соответствующие значения из справочника будут перенесены в поля класса
            данных. Пример: {'summa':'f1', 'summa2':'f2'}
        :type dt: C{string}
        :param dt: Время актуальности кода.
        :type bCount: C{string}
        :param bCount: признак того, что необходимо вести количество ссылок.
        :rtype: C{int}
        :return: Код возврата функции контроля.
        """
        result = coderror.IC_CTRL_OK
        res_val = None

        try:
            storage = self.getStorage()
            level_tab = storage.getLevelTable(cod, dt)
            # Получаем следующий уровень за уровнем родительского кода
            level = self.getLevelByCod(cod).getNext() if cod else self.getLevels()[0]
            # Список имен полей
            field_names = storage.getSpravFieldNames(level_idx=level.getIndex())
            # Словарь индексов
            field_indexes = dict([(field_name, i) for i, field_name in enumerate(field_names)])
            field_idx = field_indexes[field]
            log.debug(u'Уровень %d %s %s' % (level.getIndex(), str(field_names), str(field_indexes)))

            # Перебор строк
            for rec in level_tab:
                if rec[field_idx] == val:
                    # Перебор полей
                    if flds and isinstance(flds, dict):
                        res_val = dict([(item[0], rec[field_indexes[item[1]]]) for item in flds.items()])
                    else:
                        res_val = None
                    # Нашли запись и заполнили выходной словарь
                    return result, res_val
            # Не найдено
            result = coderror.IC_CTRL_FAILED
            log.warning(u'Не найден код <%s> в объекте-ссылке/справочнике <%s>' % (val, self.getName()))
        except:
            log.fatal(u'ОБЪЕКТ-ССЫЛКА/СПРАВОЧНИК [%s] Ошибка контроля' % self.getName())
            result = coderror.IC_CTRL_FAILED_TYPE_SPRAV

        return result, res_val
