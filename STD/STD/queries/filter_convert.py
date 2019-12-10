#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции конвертации результатов фильтров в разные представления,
например в SQL представление.

Фильтр представляет собой словарно-списковую структуру, состоящую из 
структур двух типов объектов: группа и реквизит.

Группа - структура, описывающая группировку связанных скобками элементов и
соединяемых одним логическим операндом (И, ИЛИ, НЕ).

Группа:
{
 'name': Наименование группы. Обычно соответствует логическому операнду.
 'type': Тип группы. Строка <group>.
 'logic': Логический операнд. AND или OR или NOT.
 'children': Список реквизитов - элементов группы.
}

Реквизит - структура, описывающая элемент группы, соответствует 
полю таблицы. Кроме указания поля включает в себя оператор сравнения
и аргументы оператора сравнения.

Реквизит:

{
 'requisite': Наименование реквизита. Обычно соответствует имени поля таблицы.
 'type': Тип. Слово <compare>.
 'arg_1': Значение аргумента 1.
 'arg_2': Значение аргумента 2.
 'get_args': Дополнительная функция получения аргументов.
 'function': Имя функции сравнения. Функция сравнения выбирается по имени из
            словаря функций сравнения, определенного 
            в модуле filter_builder_env.
 '__sql__': Кортеж элментов sql выражения соответствующего данному реквизиту.
            Поэтому генерация WHERE секции SQL заключается в правильном
            соединении нужных строк этого ключа.
}
"""

import sqlalchemy

import ic

# Version
__version__ = (0, 1, 1, 2)


def convertFilter2PgSQL(filter_data, table_name, fields=('*',), limit=None):
    """
    Конвертировать фильтр в SQL представление Postgres.
    :param filter_data: Структура фильтра.
    :param table_name: Имя таблицы запроса.
    :param fields: Список/Кортеж имен полей используемых в запросе.
    :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
    :return: Возвращает строковое представление оператора
    SELECT диалекта PgSQL.
    """
    sql_fmt = '''SELECT %s
    FROM %s
    WHERE %s
    '''
    fields_sql = ', '.join(fields)
    converter = icFilter2PostgreSQLConverter(filter_data)
    where = converter.convert()
    if not where:
        sql_fmt = 'SELECT %s FROM %s'
        sql = sql_fmt % (fields_sql, table_name)
    else:
        sql = sql_fmt % (fields_sql, table_name, where)
    if limit:
        sql += 'LIMIT %d' % limit
    return sql


class icFilter2PostgreSQLConverter(object):
    """
    Класс конвертера фильтра в PostgreSQL.
    """
    def __init__(self, filter_data, code_page='utf-8'):
        """
        Конструктор.
        :param filter_data: Структура фильтра.
        :param code_page: Кодировка текста в фильтре.
        """
        self.filter = filter_data
        self.codepage = code_page
    
    def convert(self):
        """
        Запуск конвертации.
        :return: Возвращает строковое представление секции WHERE оператора
        SELECT диалекта PgSQL.
        """
        # ВНИМАНИЕ!
        # Корневой элемент фильтра должен быть всегда группой
        if self.filter:
            sql_txt = self.gen_group_sql(self.filter)
            return sql_txt
        return ''
    
    def gen_group_sql(self, group_data):
        """
        Генерация части SQL выражения, соответствующего группе реквизитов-элементов.
        :param group_data: Структура группы.
        :return: Возвращает строку секции WHERE SQL, соответствующую данной группе.
        """
        sql_fmt = '''( %s )'''
        
        sql_elements = []
        for element in group_data['children']:
            if element['type'] == 'group':
                sql_element = self.gen_group_sql(element)
            elif element['type'] == 'compare':
                sql_element = self.gen_requisite_sql(element)
            else:
                ic.log.info(u'Неопределенный тип элемента фильтра: %s' % element['type'])
                continue
            sql_elements.append(sql_element)
            
        sql_group = (' ' + group_data['logic'] + ' ').join(sql_elements)
        return sql_fmt % sql_group
    
    def gen_requisite_sql(self, requisite):
        """
        Генерация части SQL выражения, соответствующую данному реквизиту.
        :param requisite: Структура реквизита.
        :return: Возвращает строку секции WHERE SQl, соответствующую данному элементу.
        """
        return ' '.join(requisite['__sql__'])
    

# --- Конвертация фильтра в SQLAlchemy представление ---
# Словарь преобразования логических операций
LOGIC_NAME2SQLALCHEMY_LOGIC = {'AND': sqlalchemy.and_,
                               'OR': sqlalchemy.or_,
                               'NOT': sqlalchemy.not_,
                               }


def convertFilter2SQLAlchemy(filter_data, table, fields=('*',), limit=None):
    """
    Конвертация фильтра в представление SQLAlchemy.
    :param filter_data: Структура фильтра.
    :param table: Таблица запроса.
    :param fields: Список/Кортеж имен полей используемых в запросе.
    :param limit: Ограничение по строкам. Если не определено, то ограничения нет.
    :return: Объект sqlalchemy.sql.selectable.Select.
    """
    converter = icFilter2SQLAlchemyConverter(filter_data, table)
    where = converter.convert()
    columns = None
    if '*' not in fields:
        columns = [getattr(table.c, fld_name) for fld_name in fields]
    else:
        columns = [table]
    query = sqlalchemy.select(columns, where)
    if limit:
        query = query.limit(int(limit))
    return query


class icFilter2SQLAlchemyConverter(object):
    """
    Класс конвертера фильтра в представление SQLAlchemy.
    """

    def __init__(self, filter_data, table, code_page='utf-8'):
        """
        Конструктор.
        :param filter_data: Структура фильтра.
        :param table: Объект таблицы.
        """
        self.filter = filter_data
        self.table = table
        self.codepage = code_page
        
    def convert(self):
        """
        Функция запуска конвертации.
        """
        # ВНИМАНИЕ!
        # Корневой элемент фильтра должен быть всегда группой
        if self.filter:
            query = self.gen_group_section(self.filter)
            return query
        else:
            ic.log.warning(u'Не определен фильтр <%s>' % self.filter)
        return None
    
    def gen_group_section(self, group_data):
        """
        Генерация секции группы.
        :param group_data: Структура группы.
        :return: Возвращает результат.
        """
        sql_alchemy_elements = []
        for element in group_data.get('children', []):
            if element['type'] == 'group':
                sql_alchemy_element = self.gen_group_section(element)
            elif element['type'] == 'compare':
                sql_alchemy_element = self.gen_requisite_section(element)
            else:
                ic.log.warning(u'Неопределенный тип элемента фильтра: %s' % element['type'])
                continue

            if sql_alchemy_element is not None:
                # Надо сделать проверку на корректные данные элемента
                # может по какойто причине не быть поддержки генерации
                sql_alchemy_elements.append(sql_alchemy_element)
                
        sql_alchemy_elements = tuple(sql_alchemy_elements)
        return LOGIC_NAME2SQLALCHEMY_LOGIC.get(group_data['logic'].upper())(*sql_alchemy_elements)

    def gen_requisite_section(self, requisite):
        """
        Генерация секции реквизита.
        :param requisite: Структура реквизита.
        :return: Возвращает результат.
        """
        try:
            if 'get_args' in requisite and requisite['get_args']:
                ext_dict = requisite['get_args']()
                requisite.update(ext_dict)
        except:
            ic.log.fatal(u'Ошибка получения аргументов')

        try:
            if requisite['function'] == 'equal':
                # Проверка на <равно>
                return getattr(self.table.c, requisite['requisite']) == requisite['arg_1']
            elif requisite['function'] == 'not_equal':
                # Проверка на <неравенство>
                return getattr(self.table.c, requisite['requisite']) != requisite['arg_1']
            elif requisite['function'] == 'great':
                # Проверка на <больше>
                return getattr(self.table.c, requisite['requisite']) > requisite['arg_1']
            elif requisite['function'] == 'great_or_equal':
                # Проверка на <больше или равно>
                return getattr(self.table.c, requisite['requisite']) >= requisite['arg_1']
            elif requisite['function'] == 'lesser':
                # Проверка на <меньше>
                return getattr(self.table.c, requisite['requisite']) < requisite['arg_1']
            elif requisite['function'] == 'lesser_or_equal':
                # Проверка на <меньше или равно>
                return getattr(self.table.c, requisite['requisite']) <= requisite['arg_1']
            elif requisite['function'] == 'between':
                # Проверка <МЕЖДУ>
                return getattr(self.table.c, requisite['requisite']).between(requisite['arg_1'],
                                                                             requisite['arg_2'])
            elif requisite['function'] == 'not_between':
                # Проверка <не МЕЖДУ>
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).between(requisite['arg_1'],
                                                                                             requisite['arg_2']))
            elif requisite['function'] == 'contain':
                # Проверка <СОДЕРЖИТ>
                return getattr(self.table.c, requisite['requisite']).contains(requisite['arg_1'])
            elif requisite['function'] == 'not_contain':
                # Проверка <не СОДЕРЖИТ>
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).contains(requisite['arg_1']))
            elif requisite['function'] in ('left_equal', 'startswith'):
                # Проверка <начинается с>
                return getattr(self.table.c, requisite['requisite']).startswith(requisite['arg_1'])
            elif requisite['function'] in ('right_equal', 'endswith'):
                # Проверка <заканчивается на>
                return getattr(self.table.c, requisite['requisite']).endswith(requisite['arg_1'])
            elif requisite['function'] == 'mask':
                # Проверка <соответствует маске>
                ic.log.warning(u'Проверка на соответствие маски пока не реализованно')
                return None
            elif requisite['function'] == 'not_mask':
                # Проверка <не соответствует маске>
                ic.log.warning(u'Проверка на не соответствие маски пока не реализованно')
                return None
            elif requisite['function'] == 'is_null':
                # Проверка <пусто>
                return getattr(self.table.c, requisite['requisite']) is None
            elif requisite['function'] == 'is_not_null':
                # Проверка <не пусто>
                return getattr(self.table.c, requisite['requisite']) is not None
            elif requisite['function'] == 'into':
                # Проверка <любое из>
                return getattr(self.table.c, requisite['requisite']).in_(requisite['arg_1'])
            elif requisite['function'] == 'not_into':
                # Проверка <не одно из>
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).in_(requisite['arg_1']))
        
            ic.log.warning(u'Не определен тип функции <%s> реквизита фильтра при конвертации' % requisite['function'])
        except:
            ic.log.fatal(u'Ошибка конвертации реквизита фильтра <%s>' % requisite)
            
        return None
