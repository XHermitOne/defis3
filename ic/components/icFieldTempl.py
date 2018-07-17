#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции модуля используются для форматированного вывода.
Формат   |  идентификатор        |  Примеры форматов и значений
{'S:n'     IC_N_STRING_FORMAT     'S:10'           'DdfgnФЫВk1' }
{'N:n'     IC_N_NUMBER_FORMAT     'N:10'           '1234567890' }
{'F:n,m'   IC_N_FLOAT_FORMAT      'F:6,2'          '123456.12'  }
{'B'       IC_BOOL_FORMAT         'B'              '1'          }
{'X*'      IC_STRING_FORMAT       'XXX'            'qwe'        }
{'9'       IC_NUMBER_FORMAT       '9999'           '1234'       }
{'9*.9*'   IC_FLOAT_FORMAT        '999.99'         '123.30'     }
{'X*-*'    IC_DIV_STRING_FORMAT   'XX-XX'          'as-DF'      }
{'9*-*'    IC_DIV_NUMBER_FORMAT   '99-99-99'       '25-01-02'   }
{'X*-9*'   IC_DIV_MIX_FORMAT      'XX-99-XX'       'as-10-BV'   }
{'9*,9*    IC_C_NUMBER_FORMAT     '999,999,999'    '123,300,000'}
{'9*,9*.9* IC_C_FLOAT_FORMAT      '99,999.99'      '20,230.90'  }
{'D:*      IC_DATE_FORMAT         'dd.mm.yyyy'     '01.01.2005' }
{'NSI:*    IC_NSI_FORMAT          'NSI'            'XXX'        }

Форматы wxPython:

    - B{grid.GRID_VALUE_STRING}
    - B{grid.GRID_VALUE_BOOL}
    - B{grid.GRID_VALUE_NUMBER}
    - B{grid.GRID_VALUE_FLOAT}
    - B{grid.GRID_VALUE_CHOICE}
    - B{grid.GRID_VALUE_LONG}
    - B{grid.GRID_VALUE_DATETIME}
"""

from ic.dlg.msgbox import MsgBox
from ic.log.iclog import LogLastError
from operator import truth
import wx
from wx import grid
import re
import string
import types

__version__ = (0, 0, 0, 3)

#   Типы форматирования
IC_N_STRING_FORMAT = 0
IC_N_NUMBER_FORMAT = 1
IC_N_FLOAT_FORMAT = 2
IC_BOOL_FORMAT = 3
IC_STRING_FORMAT = 4
IC_NUMBER_FORMAT = 5
IC_FLOAT_FORMAT = 6
IC_DIV_STRING_FORMAT = 7
IC_DIV_NUMBER_FORMAT = 8
IC_DIV_MIX_FORMAT = 9
IC_MIX_FORMAT = 10
IC_C_NUMBER_FORMAT = 11
IC_C_FLOAT_FORMAT = 12
IC_DATETIME_FORMAT = 14
IC_DATE_FORMAT = 15
IC_TIME_FORMAT = 16
IC_TEXT_FORMAT = 17
IC_NSI_FORMAT = 18

GRID_TEXT_FORMAT = 'text'
ICDB_StringType = (IC_N_STRING_FORMAT, IC_STRING_FORMAT,
                   IC_DIV_STRING_FORMAT, IC_DIV_MIX_FORMAT,
                   IC_MIX_FORMAT, IC_TEXT_FORMAT, IC_NSI_FORMAT)
            
ICDB_NumberType = (IC_N_NUMBER_FORMAT, IC_BOOL_FORMAT,
                   IC_NUMBER_FORMAT, IC_DIV_NUMBER_FORMAT)

ICDB_DoubleType = (IC_N_FLOAT_FORMAT, IC_FLOAT_FORMAT,
                   IC_C_FLOAT_FORMAT)
            
ICDB_DateTimeType = (IC_DATETIME_FORMAT, IC_DATE_FORMAT,
                     IC_TIME_FORMAT)

#   Список разделителей, используемых в шаблонах
ListDIV = (u'-', u':', u'|', u'/', u'\'', u',', u'*', u' ')


def isStringTypeCell(templ):
    """
    Признак строкового типа вывода. К таким типам относятся шаблоны состоящие
    из любых строк кроме '999*', '*9.9*', 'N:*', 'N'
    @param templ: Шаблон вывода
    @type templ: C{string}
    @return: Признак строкового типа вывода.
    @rtype: C{bool}
    """
    if templ.find(u'X') >= 0 or templ.find(u'S') >= 0 or templ.find(u'CH') >= 0:
        return 1
    else:
        for ch in ListDIV:
            if templ.find(ch) >= 0:
                return 1
    return 0


def defPicType(pic, valid):
    """
    Функция по атрибуту шаблона 'pic' определяет тип шаблона и тип ячейки
    грида.
    @return: Возвращет тип шаблона
    @param pic: Шаблон вывода
    @type pic: C{string}
    @param valid: Строка, определяющая возможные значения ячейки. Информация 
        используется wxPython для задания форматов ячеек. Например, 
        wxGRID_VALUE_NUMBER + ':1,10' задает минимальное и максимальное 
        значение вводимого целого числа.
    @type valid: C{string}
    """
    try:
        prz = pic[0]
        #   Форматированный целочисленный тип   (пример: '999 999.99')
        if pic.find(u'9') >= 0 and pic.find(u',') >= 0 and pic.find(u'.') >= 0:
            spctype = IC_C_FLOAT_FORMAT
            typ = grid.GRID_VALUE_STRING
        elif pic in ('T', 'TEXT'):
            spctype = IC_TEXT_FORMAT
            typ = GRID_TEXT_FORMAT
        #   Форматированный числовой тип Float
        elif pic.find(u'9') >= 0 and pic.find(u'.') >= 0:
            pos = pic.find(u'.')
            spctype = IC_FLOAT_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Форматированный целочисленный тип   (пример: '999-99')
        elif pic.find(u'9') >= 0 and pic.find(u'-') >= 0:
            spctype = IC_DIV_NUMBER_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Форматированный целочисленный тип   (пример: '999,999', '230 900')
        elif pic.find(u'9') >= 0 and pic.find(u',') >= 0:
            spctype = IC_C_NUMBER_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Форматированный строковый тип   (пример: 'A10-DF')
        elif pic.find(u'X') >= 0 and pic.find(u'-') >= 0:
            spctype = IC_DIV_STRING_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Форматированный численно-строковый тип   (пример: '10-DF')
        elif pic.find(u'X') >= 0 and pic.find(u'-') >= 0 and pic.find(u'9') >= 0:
            spctype = IC_DIV_MIX_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Численно-строковый тип   (пример: '99XX'; '10DF')
        elif pic.find(u'X') >= 0 and pic.find(u'9') >= 0:
            spctype = IC_MIX_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Целочисленный тип
        elif prz == u'9':
            spctype = IC_NUMBER_FORMAT
            try:
                if len(valid) > 0:
                    typ = grid.GRID_VALUE_NUMBER + u':' + valid
                else:
                    typ = grid.GRID_VALUE_STRING
            except KeyError:
                typ = grid.GRID_VALUE_STRING
        #   Дополнительная форма записи числового типа S
        elif prz == u'S':
            spctype = IC_N_STRING_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Дополнительная форма записи числового типа Int
        elif prz == u'N':
            spctype = IC_N_NUMBER_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   форма записи числового типа Long
        elif prz == u'L':
            spctype = IC_NUMBER_FORMAT
            typ = grid.GRID_VALUE_LONG
        #   форма записи даты
        elif prz == u'D':
            spctype = IC_DATE_FORMAT
            typ = wx.grid.GRID_VALUE_DATETIME  # grid.GRID_VALUE_STRING
        #   форма записи времени
        elif prz == u'T':
            spctype = IC_TIME_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   форма записи даты и времени
        elif pic[0:2] == u'DT':
            spctype = IC_DATETIME_FORMAT
            typ = grid.GRID_VALUE_STRING
        elif pic == u'NSI':
            spctype = IC_NSI_FORMAT
            typ = grid.GRID_VALUE_STRING
        #   Дополнительная форма записи числового типа Float
        elif prz == u'F':
            spctype = IC_FLOAT_FORMAT
            try:
                if valid is not None and valid != u'':
                    typ = grid.GRID_VALUE_FLOAT + u':' + valid
                else:
                    typ = grid.GRID_VALUE_FLOAT + pic[1:]
            except KeyError:
                typ = grid.GRID_VALUE_FLOAT
        #   Бинарный тип
        elif prz == u'B':
            spctype = IC_BOOL_FORMAT
            typ = grid.GRID_VALUE_BOOL
        #   Текстовый тип
        else:
            spctype = IC_STRING_FORMAT
            try:
                if len(valid) > 0:
                   typ = grid.GRID_VALUE_CHOICE + u':' + valid
                else:
                    typ = grid.GRID_VALUE_STRING
            except KeyError:
                typ = grid.GRID_VALUE_STRING
    except Exception:
        spctype = IC_STRING_FORMAT
        typ = grid.GRID_VALUE_STRING

    return spctype, typ


def isEqTemplate(typ, templ, oldText, key_cod, ins_pos, evt=None):
    """
    Функция определяет удолетворяет ли вводимый символ шаблону.
    @param typ: Тип шаблона.
    @type typ: C{int}
    @param templ: Шаблон ввода/вывода.
    @type templ: C{string}
    @param oldText: Текст поля.
    @type oldText: C{string}
    @param ins_pos: Положение курсора в редакторе поля ввода.
    @type ins_pos: C{int}
    @param key_cod: Код нажатой клавиши.
    @type key_cod: C{int}
    """
    txt = None
    try:
        bShift = evt.ShiftDown()
    except:
        bShift = False
        
    # --- IC_N_STRING_FORMAT
    if typ == IC_N_STRING_FORMAT:
        size = len(oldText)
        try:
            if size >= int(templ[2:]):
                return False
        except Exception:
            pass
    # --- IC_N_NUMBER_FORMAT
    elif typ == IC_N_NUMBER_FORMAT:
        size = len(oldText)
        try:
            #   Учитываем '-'
            if size > 0:
                if oldText[0] == u'-':
                    size -= 1
            if size >= int(templ[2:]):
                return False
            else:
                return not bShift and ((key_cod in [45, 394] and ins_pos == 0) or (48 <= key_cod <= 57) or (326 <= key_cod <= 335))
        except Exception:
            return not bShift and ((key_cod in [45, 394] and ins_pos == 0) or (48 <= key_cod <= 57) or (326 <= key_cod <= 335))
    elif typ == IC_N_FLOAT_FORMAT:
        pass
    elif typ == IC_BOOL_FORMAT:
        pass
    # --- IC_STRING_FORMAT
    elif typ == IC_STRING_FORMAT:
        size = len(oldText)
        if size >= len(templ):
            return False
    # --- IC_NUMBER_FORMAT
    elif typ == IC_NUMBER_FORMAT:
        size = len(oldText)
        #   Учитываем '-'
        if size > 0:
            if oldText[0] is u'-':
                size -= 1
        if size >= len(templ):
            return False
        else:
            return not bShift and ((key_cod in [45, 394] and ins_pos == 0) or (48 <= key_cod <= 57) or (326 <= key_cod <= 335))
    # XX-XX
    elif typ == IC_DIV_STRING_FORMAT:
        size = len(oldText)
        #   Ограничение по размерам
        if size >= len(templ):
            return False
        else:
            ret = isSimbEqTemplate(key_cod, ins_pos, oldText, templ)
            return ret
    elif typ == IC_DIV_NUMBER_FORMAT:
        size = len(oldText)
        #   Ограничение по размерам
        if size >= len(templ):
            return False
        else:
            ret = isSimbEqTemplate(key_cod, ins_pos, oldText, templ)
            return ret
    elif typ == IC_DIV_MIX_FORMAT:
        size = len(oldText)
        #   Ограничение по размерам
        if size >= len(templ):
            return False
        else:
            ret = isSimbEqTemplate(key_cod, ins_pos, oldText, templ)
            return ret
    elif typ == IC_MIX_FORMAT:
        size = len(oldText)
        if size >= len(templ):
            return False
        else:
            ret = isSimbEqTemplate(key_cod, ins_pos, oldText, templ)
            return ret
    # --- IC_C_FLOAT_FORMAT
    elif typ == IC_C_FLOAT_FORMAT:
        size = len(oldText)
        #   Ограничение по размерам
        if key_cod in (395, ord(u'.')) and u'.' not in oldText:
            return True
        else:
            return (not bShift and ((key_cod in [45, 394] and ins_pos == 0) or
                                    (48 <= key_cod <= 57) or
                                    (326 <= key_cod <= 335)))
    # --- IC_FLOAT_FORMAT
    elif typ == IC_FLOAT_FORMAT:
        if key_cod in (395, ord(u'.')) and u'.' not in oldText:
            return True
        else:
            return (not bShift and ((key_cod in [45, 394] and ins_pos == 0) or
                                    (48 <= key_cod <= 57) or
                                    (326 <= key_cod <= 335)))
    # --- IC_C_NUMBER_FORMAT
    elif typ == IC_C_NUMBER_FORMAT:
        size = len(oldText)
        #   Ограничение по размерам
        if size >= len(templ):
            return False
        else:
            return (not bShift and ((key_cod in [45, 394] and ins_pos == 0) or
                                    (48 <= key_cod <= 57) or
                                    (326 <= key_cod <= 335)))
    return True


#   Удаляет из текста символы форматирования
def delTempl(pic, txt, list_div=ListDIV):
    """
    Удаляет из текста символы форматирования.
    B{Пример:}
    C{__delTempl('123-AS') -> '123AS'}
    @return: Возвращает текст без символов форматирования.
    @rtype:  C{string}
    @param pic: Шаблон вывода (например, 'XX-XX')
    @type pic: C{string}
    @param txt: Текст, который необходимо преобразовать
    @type txt: C{string}
    @param list_div: Список разделителей, используемых в шаблонах
    @type list_div: C{List}
    """
    #   Если в шаблоне находим признаки не форматируемых полей (F, S, N), то
    #   выходим из процедуры
    try:
        fs = pic[0]
        if fs == u'F' or fs == u'S' or fs == u'N' or fs == u'D':
            return txt
    except Exception:
        return txt
    #   Удаляет из шаблона разделители
    for s in pic:
        if s in list_div:
            txt = txt.replace(s, u'')
    return txt


def setTempl(pic, txt, ins_pos, list_div=ListDIV):
    """
    Устанавливает необходимый шаблон вывода.
    B{Пример:}
    C{__setTempl('XX-XXX, '1234', 2) -> '12-34'}
    C{__setTempl('XX-XXX, '1234', 1) -> '1-234'}
    @return: Возвращает отформатированный текст
    @rtype: C{string}
    @param pic: Шаблон вывода (например, 'XX-XX')
    @type pic: C{unicode}
    @param txt: Текст, который необходимо преобразовать
    @type txt: C{unicode}
    @param ins_pos: Позиция, куда будет вставляться символ. Если =-1, то в текст ничего вставляться не будет.
    @type ins_pos: C{int}
    @param list_div: Список разделителей, используемых в шаблонах
    @type list_div: C{List}
    """
    if type(txt) in (str, unicode):
        value = txt
    else:
        value = unicode(txt)
        
    bTempl = True
    oDiv = []
    #   Если в шаблоне находим признаки не форматируемых полей (F, S, N), то
    #   выходим из процедуры
    try:
        fs = pic[0]
        if fs == u'F' or fs == u'S' or fs == u'N' or fs == u'D':
            return value, ins_pos
    except Exception:
        return value, ins_pos

    if ins_pos >= 0:
        value = txt[:ins_pos]+chr(12)+txt[ins_pos:]
    #   Обработка численного шаблона
    #   120 300.25 (999,999.99)
    if u'X' not in pic and (pic.find(u',') >= 0 or pic.find(u'.') >= 0):
        pos_point = pic.find(u'.')
        value = value.replace(u',', u'')
        #   Представление с десятичной дробной частью (1234.89)
        if pos_point >= 0:
            ltempl = len(pic[:pos_point])
            rtempl = len(pic[pos_point:])
            bef_templ = pic[:pos_point]
            #   Определяем представление числа после запятой
            #
            nf = value.find(u'.')
            after = u''
            zstr = string.join([u'0' for x in range(rtempl-1)], u'')
            if nf >= 0:
                after = value[nf:] + zstr
                before = value[:nf]
            else:
                after = u'.' + zstr
                before = value
            #   Количество знаков перед запятой подстраиваем под шаблон
            if nf > ltempl:
                before = before[:ltempl]
            #   Обрезаем лишнии символы после запятой
            if len(after) > rtempl:
                after = after[:rtempl]
        #   Представление целых чисел  (999,999) -> (120, 230)
        else:
            before = value
            bef_templ = pic
            after = u''

        buff = u''
        count = 0
        j = 0
        while count < len(before):
            j -= 1
            try:
                st = bef_templ[j]
            except Exception:
                break

            if st == u',':
                sval = u','
            else:
                count += 1
                s = before[-count]
                sval = s

            buff = sval + buff

        #   Собираем полное представление числа
        buff += after
        ins_pos = buff.find(chr(12))
        value = buff.replace(chr(12), u'')
        return value, ins_pos

    #   Проверяем есть ли в шаблоне разделители
    for s in pic:
        if s in list_div:
            value = value.replace(s, u'')
            oDiv.append(s)
    #   Обработка шаблонов выравненных по левому краю
    if len(oDiv) > 0:
        nDiv = 0
        div = oDiv[nDiv]
        buff = u''
        count = 0
        count_s = 0
        for i in range(len(pic)):
            s = pic[i]
            if i+1 < len(pic):
                sn = pic[i+1]
            else:
                sn = None

            if s == div:
                sval = div
                nDiv += 1
                if nDiv < len(oDiv):
                    div = oDiv[nDiv]
                else:
                    div = u''

            elif count < len(value):
                sval = value[count]
                count += 1
            else:
                break

            buff = buff + sval

        ins_pos = buff.find(chr(12))
        value = buff.replace(chr(12), u'')
        return value, ins_pos

    value = value.replace(chr(12), u'')
    return value, ins_pos


#   Проверяет соответствует ли шаблону вводимый символ
def isSimbEqTemplate(keycod, ins_pos, text, templ):
    """
    Проверяет соответствует ли шаблону вводимый символ
    @return: Возвращает признак соответствия вводимого символа шаблону
    @rtype: C{true | false}
    @param keycod: Код (wxPython) нажатой клавиши.
    @type keycod: C{int}
    @param ins_pos: Позиция курсора
    @type ins_pos: C{int}
    @param text: Текст
    @type text: C{string}
    @param templ: Шаблон вывода
    @type templ: C{string}
    """
    ret = 0
    oldTxt = text
    if keycod > 256:
        return False
    try:
        #   Получаем текст, который получится после ввода символа
        txt = text[:ins_pos] + chr(keycod) + text[ins_pos:]
        #   Сравниваем c шаблоном
        for i in range(len(txt)):
            ch = txt[i]
            cht = templ[i]
            #   Проверяем на разделители шаблонов
            for div in ListDIV:
                if cht == div and i+1 < len(templ):
                    cht = templ[i+1]
            if cht == u'X':
                ret = True
            elif 48 <= ord(cht) <= 57:
                ret = (ord(ch) == 45 or (48 <= ord(ch) <= ord(cht)))
            else:
                ret = (cht == ch)
            if ret == 0:
                return False
        ret = True
    #   Если шаблон не определен, то считаем, что ввод правильный
    except:
        LogLastError(u'Exception')
        ret = True

    return ret


def GetTextByTemplate(typ, templ, text, kcod, oldPoint):
    """
    """
    #   Проверяем соответствут вводимый символ шаблону вывода
    #   При необходимости вставляет символы форматирования
    ret = isEqTemplate(typ, templ, text, kcod, oldPoint)
    if not ret:
        point = -1
        if (kcod in [395, 46]) and (typ in [IC_C_FLOAT_FORMAT, IC_FLOAT_FORMAT]):
            point = text.find(u'.')+1
        return False, (text, point)
    else:
        return True, setTempl(templ, text, oldPoint)


def PrepareTextByTempl(editor, typ, templ, text, kcod):
    """
    Подстраивает текст под шаблон.
    @rtype: C{bool}
    @return: Признак разрешающий редактору ввести текущий символ.
    """
    oldPoint = editor.GetInsertionPoint()
    #   Выделенный текст удаляем
    beg, end = editor.GetSelection()
    if beg < end:
        txt = text[:beg] + text[end:]
    else:
        txt = text
    
    isEq, (txt, point) = GetTextByTemplate(typ, templ, txt, kcod, oldPoint)
    if not isEq:
        if point >= 0:
            editor.SetInsertionPoint(point)
        return False
    elif point >= 0:
        editor.bBlockChangeEvt = True
        if txt != text and kcod not in (395, ord(u'.')):
            wx.TextCtrl.SetValue(editor, txt)

        editor.SetInsertionPoint(point)
        editor.bBlockChangeEvt = False
        return True

    return False


if __name__ == '__main__':
    pass
