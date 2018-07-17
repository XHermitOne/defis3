#!/usr/bin/env python
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
 'func': Имя функции сравнения. Функция сравнения выбирается по имени из 
            словаря функций сравнения, определенного 
            в модуле filter_builder_env.
 '__sql__': Кортеж элментов sql выражения соответствующего данному реквизиту.
            Поэтому генерация WHERE секции SQL заключается в правильном
            соединении нужных строк этого ключа.
}
"""

# Imports
import sqlalchemy

import ic

# Version
__version__ = (0, 0, 2, 1)


def convertFilter2PgSQL(Filter_, TableName_, Fields_=('*',), limit=None):
    """
    Конвертировать фильтр в SQL представление Postgres.
    @param Filter_: Структура фильтра.
    @param TableName_: Имя таблицы запроса.
    @param Fields_: Список/Кортеж имен полей используемых в запросе.
    @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
    @return: Возвращает строковое представление оператора
    SELECT диалекта PgSQL.
    """
    sql_fmt = '''SELECT %s
    FROM %s
    WHERE %s
    '''
    fields = ', '.join(Fields_)
    converter = icFilter2PostgreSQLConverter(Filter_)
    where = converter.convert()
    if not where:
        sql_fmt = 'SELECT %s FROM %s'
        sql = sql_fmt % (fields, TableName_)
    else:
        sql = sql_fmt % (fields, TableName_, where)
    if limit:
        sql += 'LIMIT %d' % limit
    return sql


class icFilter2PostgreSQLConverter:
    """
    Класс конвертера фильтра в PostgreSQL.
    """

    def __init__(self, Filter_, CodePage_='utf-8'):
        """
        Конструктор.
        @param Filter_: Структура фильтра.
        @param CodePage_: Кодировка текста в фильтре.
        """
        self.filter = Filter_
        self.codepage = CodePage_
    
    def convert(self):
        """
        Запуск конвертации.
        @return: Возвращает строковое представление секции WHERE оператора
        SELECT диалекта PgSQL.
        """
        # ВНИМАНИЕ!
        # Корневой элемент фильтра должен быть всегда группой
        if self.filter:
            sql_txt = self.gen_group_sql(self.filter)
            return sql_txt
        return ''
    
    def gen_group_sql(self, Grp_):
        """
        Генерация части SQL выражения, соответствующего группе реквизитов-элементов.
        @param Grp_: Структура группы.
        @return: Возвращает строку секции WHERE SQL, соответствующую данной группе.
        """
        sql_fmt = '''( %s )'''
        
        sql_elements = []
        for element in Grp_['children']:
            if element['type'] == 'group':
                sql_element = self.gen_group_sql(element)
            elif element['type'] == 'compare':
                sql_element = self.gen_requisite_sql(element)
            else:
                ic.io_prnt.outLog(u'Неопределенный тип элемента фильтра: %s' % element['type'])
                continue
            sql_elements.append(sql_element)
            
        sql_group = (' '+Grp_['logic']+' ').join(sql_elements)
        return sql_fmt % sql_group
    
    def gen_requisite_sql(self, Requisite_):
        """
        Генерация части SQL выражения, соответствующую данному реквизиту.
        @param Requisite_: Структура реквизита.
        @return: Возвращает строку секции WHERE SQl, соответствующую данному элементу.
        """
        return ' '.join(Requisite_['__sql__'])
    

# --- Конвертация фильтра в SQLAlchemy представление ---
# Словарь преобразования логических операций
logicName2SQLAlchemyLogic = {'AND': sqlalchemy.and_,
                             'OR': sqlalchemy.or_,
                             'NOT': sqlalchemy.not_,
                             }


def convertFilter2SQLAlchemy(Filter_, Table_, Fields_=('*',), limit=None):
    """
    Конвертация фильтра в представление SQLAlchemy.
    @param Filter_: Структура фильтра.
    @param Table_: Таблица запроса.
    @param Fields_: Список/Кортеж имен полей используемых в запросе.
    @param limit: Ограничение по строкам. Если не определено, то ограничения нет.
    """
    converter = icFilter2SQLAlchemyConverter(Filter_, Table_)
    where = converter.convert()
    columns = None
    if '*' not in Fields_:
        columns = [getattr(Table_.c, fld_name) for fld_name in Fields_]
    else:
        columns = [Table_]
    query = sqlalchemy.select(columns, where)
    if limit:
        query = query.limit(int(limit))
    return query


class icFilter2SQLAlchemyConverter:
    """
    Класс конвертера фильтра в представление SQLAlchemy.
    """

    def __init__(self, Filter_, Table_, CodePage_='utf-8'):
        """
        Конструктор.
        @param Filter_: Структура фильтра.
        @param Table_: Объект таблицы.
        """
        self.filter = Filter_
        self.table = Table_
        self.codepage = CodePage_
        
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
            ic.io_prnt.outWarning(u'Не определен фильтр <%s>' % self.filter)
        return None
    
    def gen_group_section(self, Grp_):
        """
        Генерация секции группы.
        @param Grp_: Структура группы.
        @return: Возвращает результат.
        """
        sql_alchemy_elements = []
        for element in Grp_.get('children', []):
            if element['type'] == 'group':
                sql_alchemy_element = self.gen_group_section(element)
            elif element['type'] == 'compare':
                sql_alchemy_element = self.gen_requisite_section(element)
            else:
                ic.io_prnt.outWarning(u'Неопределенный тип элемента фильтра: %s' % element['type'])
                continue

            if sql_alchemy_element is not None:
                # Надо сделать проверку на корректные данные элемента
                # может по какойто причине не быть поддержки генерации
                sql_alchemy_elements.append(sql_alchemy_element)
                
        sql_alchemy_elements = tuple(sql_alchemy_elements)
        return logicName2SQLAlchemyLogic.get(Grp_['logic'].upper())(*sql_alchemy_elements)

    def gen_requisite_section(self, Requisite_):
        """
        Генерация секции реквизита.
        @param Requisite_: Структура реквизита.
        @return: Возвращает результат.
        """
        try:
            if 'get_args' in Requisite_ and Requisite_['get_args']:
                ext_dict = Requisite_['get_args']()
                Requisite_.update(ext_dict)
        except:
            ic.io_prnt.outLastErr(u'Ошибка получения аргументов')

        try:
            if Requisite_['func'] == 'equal':
                # Проверка на <равно>
                return getattr(self.table.c, Requisite_['requisite']) == Requisite_['arg_1']
            elif Requisite_['func'] == 'not_equal':
                # Проверка на <неравенство>
                return getattr(self.table.c, Requisite_['requisite']) <> Requisite_['arg_1']
            elif Requisite_['func'] == 'great':
                # Проверка на <больше>
                return getattr(self.table.c, Requisite_['requisite']) > Requisite_['arg_1']
            elif Requisite_['func'] == 'great_or_equal':
                # Проверка на <больше или равно>
                return getattr(self.table.c, Requisite_['requisite']) >= Requisite_['arg_1']
            elif Requisite_['func'] == 'lesser':
                # Проверка на <меньше>
                return getattr(self.table.c, Requisite_['requisite']) < Requisite_['arg_1']
            elif Requisite_['func'] == 'lesser_or_equal':
                # Проверка на <меньше или равно>
                return getattr(self.table.c, Requisite_['requisite']) <= Requisite_['arg_1']
            elif Requisite_['func'] == 'between':
                # Проверка <МЕЖДУ>
                return getattr(self.table.c, Requisite_['requisite']).between(Requisite_['arg_1'],
                                                                              Requisite_['arg_2'])
            elif Requisite_['func'] == 'not_between':
                # Проверка <не МЕЖДУ>
                return sqlalchemy.not_(getattr(self.table.c, Requisite_['requisite']).between(Requisite_['arg_1'],
                                                                                              Requisite_['arg_2']))
            elif Requisite_['func'] == 'contain':
                # Проверка <СОДЕРЖИТ>
                return getattr(self.table.c, Requisite_['requisite']).contains(Requisite_['arg_1'])
            elif Requisite_['func'] == 'not_contain':
                # Проверка <не СОДЕРЖИТ>
                return sqlalchemy.not_(getattr(self.table.c, Requisite_['requisite']).contains(Requisite_['arg_1']))
            elif Requisite_['func'] in ('left_equal', 'startswith'):
                # Проверка <начинается с>
                return getattr(self.table.c, Requisite_['requisite']).startswith(Requisite_['arg_1'])
            elif Requisite_['func'] in ('right_equal', 'endswith'):
                # Проверка <заканчивается на>
                return getattr(self.table.c, Requisite_['requisite']).endswith(Requisite_['arg_1'])
            elif Requisite_['func'] == 'mask':
                # Проверка <соответствует маске>
                ic.io_prnt.outWarning(u'Проверка на соответствие маски пока не реализованно')
                return None
            elif Requisite_['func'] == 'not_mask':
                # Проверка <не соответствует маске>
                ic.io_prnt.outWarning(u'Проверка на не соответствие маски пока не реализованно')
                return None
            elif Requisite_['func'] == 'is_null':
                # Проверка <пусто>
                return getattr(self.table.c, Requisite_['requisite']) is None
            elif Requisite_['func'] == 'is_not_null':
                # Проверка <не пусто>
                return getattr(self.table.c, Requisite_['requisite']) is not None
            elif Requisite_['func'] == 'into':
                # Проверка <любое из>
                return getattr(self.table.c, Requisite_['requisite']).in_(Requisite_['arg_1'])
            elif Requisite_['func'] == 'not_into':
                # Проверка <не одно из>
                return sqlalchemy.not_(getattr(self.table.c, Requisite_['requisite']).in_(Requisite_['arg_1']))
        
            ic.io_prnt.outWarning(u'Не определен тип функции <%s> реквизита фильтра при конвертации' % Requisite_['func'])
        except:
            ic.io_prnt.outErr(u'Ошибка конвертации реквизита фильтра <%s>' % Requisite_)
            
        return None
