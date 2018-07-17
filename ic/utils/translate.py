#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит функции перекодировки из одного представления в другое.
"""

import wx
from . import resource
from ic.kernel import io_prnt

_ = wx.GetTranslation


def icNamesSQLObj2SQL(Txt_, DataClassName_, DataClassScheme_=None):
    """
    Перевод имен таблиц и полей из контекста SQLObject в контекст sqlite.
    @param Txt_: Корректируемый текст.
    @param DataClassName_: Имя класса данных (класса таблицы).
    @param DataClassScheme_: Схема описания класса данных (класса таблицы).
    """
    try:
        txt = Txt_
        # Коррекция имен таблиц
        txt = txt.replace(DataClassName_, mixedToUnder(DataClassName_))
        # Если есть описнаие схемы, то сделать коррекцию имен полей таблицы
        if DataClassScheme_:
            # Коррекция имен полей
            for fld in DataClassScheme_:
                # Если поле-не повторяющаяся группа
                if not isinstance(fld['group'], list):
                    # .. то просто заменить его имя
                    txt = txt.replace(fld['name'], mixedToUnder(fld['name']))
                else:
                    # .. но если поле-повторяющаяся группа,то рекурсивно вызвать
                    # эту же функцию
                    txt = icNamesSQLObj2SQL(txt, fld['name'], fld['group'])
        return txt
    except:
        return Txt_


def icQuerySQLObj2SQL(SQLTxt_, ResTab_):
    """
    Преобразование имен в тексте SQL запроса в контексте SQLObject в имена
    в контексте sqlite.
    @param SQLTxt_: Текст SQL запроса.
    @param ResTab_: Ресурсное описание таблиц.
    """
    try:
        sql_txt = SQLTxt_
        # Для корректной обработки имен полей и таблиц они д.б.
        # отсортированны по убыванию длин имен классов данных
        data_class_names = ResTab_.keys()
        data_class_names.sort()
        data_class_names.reverse()
        for data_class_name in data_class_names:
            sql_txt = icNamesSQLObj2SQL(sql_txt, data_class_name, ResTab_[data_class_name]['child'])
    
        return sql_txt
    except:
        return SQLTxt_


def fcmpLen(x, y):
    """
    Функция сравнения для сортировки списка в порядке уменьшения длины.
    """
    if len(x) > len(y):
        return -1
    elif len(x) < len(y):
        return 1
    else:
        return 0


def sortLen(lst):
    """
    Функция сортирует в порядке уменьшения длины элементов списка.
    @type lst: C{list}
    @param lst: Список, который надо отсортировать.
    """
    try:
        lst.sort(fcmpLen)
        return True
    except:
        return False


def dictFilterToSQL(flt, tables, _id='id'):
    """
    Функция конвертирует структурный фильтр в SQL выражение. Структурный фильтр
    задается словарем. В качестве ключей используются поля, в качестве значений
    значения полей либо список подзапроса на значение поля. Список подзапроса
    задает разбиение значения поля на подстроки и условия выбора по ним. Подстроки
    выделяются SQL функцией substr. Размер подстроки задается размерами элемента
    списка. Значение элемента задает условие на значение подстроки, если элемент
    является строкой, если элемент является числом, то это тому что подстрока с
    данным размером может быть любой.
    
        B{Пример:} C{{'f1':['gh', 2, '123', '3MM']}}
        
    @type flt: C{dictionary}
    @param flt: Словарь задающий структурный фильтр.
    """
    if type(flt) in (str, unicode):
        return flt
    if not isinstance(flt, dict):
        io_prnt.outLog(_('Unexpected filter type. Must be srting type or dictionary.'))
        return None
        
    condition = ''
    for fld in flt:
        val = flt[fld]
        if not isinstance(val, list) and not isinstance(val, tuple):
            if type(val) in (str, unicode):
                val = '"'+val+'"'
            if condition == '':
                condition = ' %s=%s ' % (fld, val)
            else:
                condition += 'and %s=%s ' % (fld, val)
        else:
            s = ''
            cur = 1
            for x in val:
                if type(x) in (str, unicode):
                    if s == '':
                        s = ' substr(%s, %d, %d)=\'%s\' ' % (fld, cur, len(x), x)
                    else:
                        s += 'and substr(%s, %d, %d)=\'%s\' ' % (fld, cur, len(x), x)
                    cur += len(x)
                elif isinstance(x, int):
                    cur += x
            
            if condition == '':
                if s:
                    condition = s + ' and length(%s)=%d ' % (fld, cur-1)
                else:
                    condition = ' length(%s)=%d ' % (fld, cur-1)
            elif s:
                condition += 'and ' + s + ' and length(%s)=%d ' % (fld, cur-1)
            else:
                condition += 'and length(%s)=%d ' % (fld, cur-1)
                
    if condition != '':
        filterSQL = 'select %s from %s where %s' % (_id, tables, condition)
    else:
        filterSQL = 'select %s from %s' % (_id, tables)

    return filterSQL


def convQueryToSQL(query, classes=None):
    """
    Преобразует запрос c SQLObject-ими именами в полноценный SQL запрос
    к базе.
    @type classes: C{list | tuple}
    @param classes: Список
    """
    dictRepl = {}
    if type(classes) in [list, tuple]:
        for cln in classes:
            dictRepl[cln] = mixedToUnder(cln)
            #   Получаем ресурсное описание класса данных
            res = resource.icGetRes(cln, nameRes=cln)
            if res is None:
                continue
            #   Отбираем описания полей
            fld_names = [x['name'] for x in [x for x in res['child'] if x['type'] == 'Field']]
            #   Отдельно отбираем описание ссылок
            link_names = [x['name'] for x in [x for x in res['child'] if x['type'] == 'Link']]

            #   Замены имен полей
            for fldName in fld_names:
                dictRepl[fldName] = mixedToUnder(fldName)
                
            #   Замены имен ссылок
            for lnk in link_names:
                dictRepl[mixedToUnder(lnk)+'_id'] = lnk
                dictRepl[lnk] = mixedToUnder(lnk)+'_id'

    return replSQLObjNamesToSQL(query, dictRepl)


def replSQLObjNamesToSQL(query, dictRepl):
    """
    Преобразует запрос имен в SQL запросе.
    @type flt: C{dictionary | string}
    @param flt: Словарь задающий фильтр.
    @type dictRepl: C{dictionary}
    @param dictRepl: Словарь замен имен из представления SQLObject в
        представление SQL выражений.
    @rtype: C{string}
    @return: SQL выражение на фильтрацию объектов класса данных.
    """
    if type(query) not in (str, unicode):
        return None
    #   Сортируем в порядке убывание длины с ключа, для того чтобы не возникло ситуации,
    #   когда более короткое ключевое слово инициирует замену в более длинном.
    #   Пример: Есть словарь замен {'Codk':codk, 'CodkS':'codk_s'} и выражение
    #   'select * from t where Codk=1 and Codks=0'. Если заменять по порядку,
    #   то получим не верное выражение: 'select * from t where сodk=1 and сodks=0'. 
    #   Если же отсортировать ключи в порядке убывания длины, то эту проблему 
    #   можно решить.
    rlist = dictRepl.keys()
    sortLen(rlist)
    #   Заменяем все имена, используемых при описании классов на имена, испольозуемые в базе данных
    for word in rlist:
        query = query.replace(word, dictRepl[word])
    #   Заменяем <'> на <'>. Т. к. некоторые базы данных не переваривают <'> (PostgreSQL)
    query = query.replace('"', '\'')
    return query


def isInFilteredVal(flt, fld, value, isVerSize=True):
    """
    Функция проверяет принадлежит ли значение заданому фильтру.
    @type flt: C{dictionary}
    @param flt: Словарь задающий структурный фильтр.
    @type fld: C{string}
    @param fld: Имя атрибута, для которого проверяется значение.
    @type value: C{...}
    @param value: Проверяемое значение.
    @type isVerSize: C{bool}
    @param isVerSize: Признак того, что размер значения не может быть больше
        размера шаблона.
    @rtype: C{bool}
    @return: Признак принадлежность значения заданному фильтру.
    """
    if not isinstance(flt, dict):
        io_prnt.outLog(_('Unexpected filter type. Must be srting type or dictionary.'))
        return None
    
    if fld not in flt.keys():
        io_prnt.outLog(_('Filter has not key: <%s>.'))
        return False
    
    filt = flt[fld]
    if not isinstance(filt, list):
        if filt == value:
            return True
        else:
            return False
    else:
        cur = 0
        for x in filt:
            if type(x) in (str, unicode):
                if value[cur:cur+len(x)] != x:
                    return False
                else:
                    cur += len(x)
            elif isinstance(x, int):
                cur += x
            
            if cur >= len(value):
                break
    
        #   Вычисляем размер шаблона
        if isVerSize:
            cur = 0
            for x in filt:
                if type(x) in (str, unicode):
                    cur += len(x)
                elif isinstance(x, int):
                    cur += x
                
            if cur < len(value):
                return False
        
    return True


def InitValidValue(flt, fld, value):
    """
    Функция модифицирует значение под заданный шаблон.
    @type flt: C{dictionary}
    @param flt: Словарь задающий структурный фильтр. Действие фильта зависимости
        от типа значения словаря. Если:
            1) катеж, список - задает шаблон по подстрокам; если элемент списка/картежа
               строка размер и значение подстроки; если число, то только размер.
            2) остальные тиаы - дадают точное значение ключа.
        Пример <см. функцию test_InitValidValue()>:
            flt1 = {'f0':'f2',                     - строгое соответствие строке 'f2'
                    'f1':('ab', 'cde', 2, '123'),  - шаблон 'abcde**123' (* - любой символ)
                    'f3_0':['12','34'],            - шаблон '1234'
                    'f3':[2,'ASD', '##']}          - шаблон '**ASD##' (* - любой символ)

    @type fld: C{string}
    @param fld: Имя атрибута, для которого модифицируется значение.
    @type value: C{...}
    @param value: Проверяемое значение.
    @rtype: C{string}
    @return: Возвращает модифицированное значение. Не обозначенные позиции будут
        заполнены '*'
    """
    if fld not in flt.keys():
        io_prnt.outLog(_('Filter has not key: <%s>.'))
        return False
    
    filt = flt[fld]
    if value is None:
        value = ''
        
    if not isinstance(filt, list) and not isinstance(filt, tuple):
        return filt
    else:
        cur = 0
        ret = ''
        for x in filt:
            if type(x) in (str, unicode):
                ret += x
                cur += len(x)
            elif isinstance(x, int):
                if cur >= len(value):
                    ret += ''.join(['*' for i in range(x)])
                elif len(value) >= cur+x:
                    ret += value[cur:cur+x]
                elif len(value) < cur+x:
                    ret += value[cur:cur+x] + ''.join(['*' for i in range(cur+x-len(value))])
                    
                cur += x
        return ret


def test_InitValidValue():
    """
    Тестируем функцию <InitValidValue>.
    """
    flt = {'f0': 'f2', 'f1': ('ab', 'cde', 2, '123'),
           'f3_0': ['12', '34'], 'f3': [2, 'ASD', '##']}
    print(u'--------------- Проверяем работоспособность функции <InitValidValue> -------------')
    print('fld=%s, value=%s -> %s ' % ('f0', '', InitValidValue(flt, 'f0', '')))
    print('fld=%s, value=%s -> %s ' % ('f0', '1234', InitValidValue(flt, 'f0', '1234')))
    print('fld=%s, value=%s -> %s ' % ('f1', '', InitValidValue(flt, 'f1', '')))
    print('fld=%s, value=%s -> %s ' % ('f3', '', InitValidValue(flt, 'f3', '')))
    print('fld=%s, value=%s -> %s ' % ('f1', '12345678977777', InitValidValue(flt, 'f1', '12345678977777')))


def test():
    """
    Проверяем работоспособность функции <convFilterToSQL>2004-01-01 00:00:00.00
    """
    flt = {'f0': 'f2', 'f1': ('ab', 'cde', 2, '123'),
           'f3_0': ['12', '34'], 'f3': [2, 'ASD', '##']}
    s = dictFilterToSQL(flt, 't1')
    print('SQL:', s)


if __name__ == '__main__':
    test()
    test_InitValidValue()
