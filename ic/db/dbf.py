#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль классов и функций работы с простым файлом *.DBF.

ВНИМАНИЕ! Если необходимо только читать данные из DBF
(при загрузке данных или конвертации),
то лучше использовать icDBFFileReadOnly.
"""

# Подключение библиотек
import os
import os.path
import copy
import time

from ic.log import log

try:
    from . import pyDBF
    is_pyd_import = True
except ImportError:
    is_pyd_import = False


# Константы
# Коды ошибок:
NOT_ERROR = 0       # Нет ошибки
NOT_OPEN = 1        # файл не возможно открыть
NOT_GET = 2         # ошибка чтения байта из файла
NOT_PUT = 3         # ошибка записи байта в файл
NOT_SEEK = 4        # ошибка при позиционировании файла
NOT_TELL = 5        # ошибка при определении позиции файла
NOT_FIELD = 6       # ошибка поиска имени поля (поле с таким именем не найдено)
NOT_TYPE = 7        # неверно указанный тип поля при создании базы
NOT_MEMORY = 8      # ошибка выделения памяти (не хватает памяти)
NOT_ALLOC = 9       # память не выделена
NOT_LIBRARY = 10    # библиотека dll_dbf.dll не может быть загружена
NOT_DEL = 11        # не могу удалить файл ( возможно где-то он используется)
NOT_RENAME = 12     # не могу переименовать временный файл

# Текстовые сообщения ошибок:
ErrorTxt = {NOT_ERROR: u'Нет ошибки',
            NOT_OPEN: u'Файл не возможно открыть',
            NOT_GET: u'Ошибка чтения байта из файла',
            NOT_PUT: u'Ошибка записи байта в файл',
            NOT_SEEK: u'Ошибка при позиционировании файла',
            NOT_TELL: u'Ошибка при определении позиции файла',
            NOT_FIELD: u'Ошибка поиска имени поля (поле с таким именем не найдено)',
            NOT_TYPE: u'Неверно указанный тип поля при создании базы',
            NOT_MEMORY: u'Ошибка выделения памяти (не хватает памяти)',
            NOT_ALLOC: u'Память не выделена',
            NOT_LIBRARY: u'Библиотека <dll_dbf> не может быть загружена',
            NOT_DEL: u'Не могу удалить файл ( возможно где-то он используется)',
            NOT_RENAME: u'Не могу переименовать временный файл',
            }

# Спецификация описания поля DBF файла
SPC_DBF_FIELD = {'name': 'field1',      # Имя поля
                 'type': 'C',           # Тип поля
                 'len': 10,             # Длина поля
                 'decimal': 0,          # Указание десятичной точки поля
                 }

# Флаги управлением удаления записи
DEL_REC_FLAG = 1        # Пометить запись как удаленную
UNDEL_REC_FLAG = 0      # Снять удаление с записи
IS_DEL_REC_FLAG = 99    # Проверка на удаление

# Символ окончания файла
DBF_FILE_EOF_CHAR = 0x1A

# Выравнивание по краю значений текстовых полей
# (По умолчанию производится выравнивание по правому краю)
LEFT_ALIGN = 1
RIGHT_ALIGN = 0

DEFAULT_DBF_ENCODING = 'cp866'

__version__ = (0, 1, 2, 1)


class icDBFFilePrototype:
    """
    Файл *.DBF.
    """

    def __init__(self, dbf_filename=None):
        """
        Конструктор.
        @param dbf_filename: Имя DBF файла, с которым работает класс.
        """
        self._dbf_file_name = dbf_filename

    def getDBFFileName(self):
        return self._dbf_file_name

    def __del__(self):
        """
        Деструктор.
        """
        self.Close()

    def Create(self, dbf_struct=[], dbf_filename=None, bReCreate=True):
        """
        Создать DBF файл по описанию его структуры.
        @param dbf_struct: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param dbf_filename: Имя DBF файла.
        @param bReCreate: Указание того, что если файл существует,
            то пересоздать его.
        """
        assert 0, u'Метод не определен'

    def Open(self, dbf_filename=None):
        """
        Открыть DBF файл.
        @param dbf_filename: Имя DBF файла.
        """
        assert 0, u'Метод не определен'

    def Close(self):
        """
        Закрыть.
        """
        assert 0, u'Метод не определен'

    def FieldCount(self):
        """
        Количество полей.
        """
        assert 0, u'Метод не определен'

    def getFieldByNum(self, n_field):
        """
        Получить значение поля по его индексу.
        @param n_field: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldByName(self, field_name):
        """
        Получить значение поля по его имени.
        @param field_name: Имя поля.
        """
        assert 0, u'Метод не определен'

    def setFieldByNum(self, n_field, field_value, align=None):
        """
        Установить значение поля по индексу.
        @param n_field: Номер/индекс поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        assert 0, u'Метод не определен'

    def setFieldByName(self, field_name, field_value, align=None):
        """
        Установить значение поля по имени.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        assert 0, u'Метод не определен'

    def setDateFieldByNum(self, n_field, datetime_tuple):
        """
        Установить значение поля даты по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        assert 0, u'Метод не определен'
        
    def setDateFieldByName(self, field_name, datetime_tuple):
        """
        Установить значение поля даты по имени.
        @param field_name: Имя поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        assert 0, u'Метод не определен'

    def setDateFieldFmtByNum(self, n_field, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
        
    def setDateFieldFmtByName(self, field_name, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param field_name: Имя поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        assert 0, u'Метод не определен'

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param n_field: Номер/индекс поля.
        @param datetime_fmt: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
        
    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param field_name: Имя поля.
        @param datetime_fmt: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
            
    def Skip(self, step=1):
        """
        Движение по таблице.
        @param step: Шаг, если <0 то к началу,
            если >0 то к концу таблицы.
        """
        assert 0, u'Метод не определен'

    def Next(self):
        """
        Перейти на следующую запись.
        """
        assert 0, u'Метод не определен'

    def Prev(self):
        """
        Перейти на предыдущую запись.
        """
        assert 0, u'Метод не определен'

    def Goto(self, rec_no=0):
        """
        Перейти на запись.
        @param rec_no: Номер записи.
        """
        assert 0, u'Метод не определен'

    def First(self):
        """
        Перейти на первую запись.
        """
        assert 0, u'Метод не определен'

    def Last(self):
        """
        Перейти на последнюю запись.
        """
        assert 0, u'Метод не определен'

    def EOF(self):
        """
        Конец таблицы.
        """
        assert 0, u'Метод не определен'

    def BOF(self):
        """
        Начало таблицы.
        """
        assert 0, u'Метод не определен'

    def DelRec(self):
        """
        Пометить запись как удаленную.
        """
        assert 0, u'Метод не определен'

    def UnDelRec(self):
        """
        Снять метку о удалении записи.
        """
        assert 0, u'Метод не определен'

    def IsDelRec(self):
        """
        Помечена запись как удаленная?
        """
        assert 0, u'Метод не определен'

    def Del(self, del_flag):
        """
        Управление удалением записи.
        @param del_flag: Флаг управления.
        """
        assert 0, u'Метод не определен'

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        assert 0, u'Метод не определен'

    def AppendRec(self, *rec_num, **rec_name):
        """
        Добавление пустой записи в конец таблицы.
        @param rec_num: Запись по номерам.
        @param rec_name: Запись по именам.
        """
        assert 0, u'Метод не определен'

    def getRecDict(self):
        """
        Получить текущую запись в виде словаря.
        """
        assert 0, u'Метод не определен'
        
    def getErrorCode(self):
        """
        Возвратить код ошибки.
        """
        assert 0, u'Метод не определен'

    def getRecCount(self):
        """
        Количество записей в таблице.
        """
        assert 0, u'Метод не определен'

    def getFieldNum(self, field_name):
        """
        Получить индекс поля по его имени.
        @param field_name: Имя поля.
        """
        assert 0, u'Метод не определен'

    def FindSort(self, field_name, find_text):
        """
        Поиск текста в поле.
        @param field_name: Имя поля.
        @param find_text: Искомый текст.
        """
        assert 0, u'Метод не определен'

    def filterRecsByField(self, field_name, value):
        """
        Отфильтровать все записи DBF файла по значению поля.
            Функция вначале открывает DBF файл.
            Затем пробегается по записям.
            Выбирает нужные.
            В конце закрывает DBF файл.
        @param field_name: Имя поля.
        @param value: Значение поля.
        @return: Возвращает список отфильтрованных записей-строк в виде словарей.
        """
        assert 0, u'Метод не определен'

    def getRecNo(self):
        """
        Номер текущей записи.
        """
        assert 0, u'Метод не определен'

    def isUsed(self):
        """
        Используется?
        """
        assert 0, u'Метод не определен'

    def Zap(self):
        """
        Запнуть.
        """
        assert 0, u'Метод не определен'

    def Pack(self):
        """
        Упаковать.
        """
        assert 0, u'Метод не определен'

    def getFieldName(self, n_field):
        """
        Получить имя поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldType(self, n_field):
        """
        Получить тип поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldLen(self, n_field):
        """
        Получить длину поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldDecimal(self, n_field):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def _del_last_eof_char(self, dbf_filename):
        """
        Удалить последний символ,  если он символ EOF.
        @param dbf_filename: Имя *.DBF файла.
        """
        if os.path.isfile(dbf_filename):
            try:
                dbf_file = None
                dbf_file = open(dbf_filename, 'r+')
                dbf_file.seek(0, 2)
                dbf_file_size = dbf_file.tell()
                last_char = dbf_file.read(1)
                if last_char and ord(last_char) == DBF_FILE_EOF_CHAR:
                    # Отрезать последний байт
                    dbf_file.trancate(dbf_file_size-2)
                dbf_file.close()
            except:
                log.fatal(u'_del_las_eof_char Function error')
                if dbf_file:
                    dbf_file.close()
                return False
            return True
        return False

    def _alignValueByName(self, field_name, field_value, align=RIGHT_ALIGN):
        """
        Выравнивание по краю.
            По умолчаниу выравнивается по правому краю
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param align: Указание выравнивания.
        @return: Возвращает строку, выравненную по полю.
        """
        if field_value is None:
            field_value = ''

        field_len = self.getFieldLen(self.getFieldNum(str(field_name).upper()))
        field_val = str(field_value)[:field_len]
        if align == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif align == RIGHT_ALIGN:
            # По умолчаниу выравнивается по правому краю
            pass
        return field_val

    def _alignValueByNum(self, n_field, field_value, align=RIGHT_ALIGN):
        """
        Выравнивание по краю.
            По умолчаниу выравнивается по правому краю
        @param n_field: Индекс/номер поля.
        @param field_value: Значение поля.
        @param align: Указание выравнивания.
        @return: Возвращает строку, выравненную по полю.
        """
        if field_value is None:
            field_value = ''

        field_len = self.getFieldLen(n_field)
        field_val = str(field_value)[:field_len]
        if align == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif align == RIGHT_ALIGN:
            # По умолчаниу выравнивается по правому краю
            pass
        return field_val


class icDBFFilePYD(icDBFFilePrototype):
    """
    Файл *.DBF.
    """

    def __init__(self, dbf_filename=None):
        """
        Конструктор.
        @param dbf_filename: Имя DBF файла, с которым работает класс.
        """
        icDBFFilePrototype.__init__(self, dbf_filename)
        # Автовыравнивание значений полей
        self.AutoAlign = RIGHT_ALIGN

    def Create(self, dbf_struct=[], dbf_filename=None, bReCreate=True):
        """
        Создать DBF файл по описанию его структуры.
        @param dbf_struct: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param dbf_filename: Имя DBF файла.
        @param bReCreate: Указание того, что если файл существует,
            то пересоздать его.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            # Можно пересоздать?
            if os.path.exists(self._dbf_file_name):
                if bReCreate:
                    os.remove(self._dbf_file_name)
                else:
                    return False

            # Сначала очистить все определения полей
            pyDBF.ClearFields()
            # Добавить поля
            for dbf_field in dbf_struct:
                # Нормализовать описание по специфиации
                field = copy.deepcopy(SPC_DBF_FIELD)
                field.update(dbf_field)
                # Добавить описание поля
                pyDBF.AddField(field['name'].upper(), field['type'], 
                               field['len'], field['decimal'])

            # Создать файл
            return not pyDBF.Create(self._dbf_file_name)
        return False

    def Open(self, dbf_filename=None):
        """
        Открыть DBF файл.
        @param dbf_filename: Имя DBF файла.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            if self._del_last_eof_char(self._dbf_file_name):
                return not pyDBF.Open(self._dbf_file_name)
        return False

    def Close(self):
        """
        Закрыть.
        """
        return pyDBF.Close()

    def FieldCount(self):
        """
        Количество полей.
        """
        return pyDBF.FieldCount()

    def getFieldByNum(self, n_field):
        """
        Получить значение поля по его индексу.
        @param n_field: Номер/индекс поля.
        """
        return pyDBF.GetFieldByNum(n_field)

    def getFieldByName(self, field_name):
        """
        Получить значение поля по его имени.
        @param field_name: Имя поля.
        """
        return pyDBF.GetFieldByName(str(field_name).upper())

    def setFieldByNum(self, n_field, field_value, align=None):
        """
        Установить значение поля по индексу.
        @param n_field: Номер/индекс поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        return pyDBF.SetFieldByNum(int(n_field),
                                   self._alignValueByNum(n_field, field_value, self.AutoAlign))

    def setFieldByName(self, field_name, field_value, align=None):
        """
        Установить значение поля по имени.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        if align is None:
            align = self.AutoAlign
        field_name = str(field_name).upper()
        return pyDBF.SetFieldByName(field_name,
                                    self._alignValueByName(field_name, field_value, align))

    def setDateFieldByNum(self, n_field, datetime_tuple):
        """
        Установить значение поля даты по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        return self.setFieldByNum(n_field, time.strftime('%Y%m%d', datetime_tuple))
        
    def setDateFieldByName(self, field_name, datetime_tuple):
        """
        Установить значение поля даты по имени.
        @param field_name: Имя поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        return self.setFieldByName(str(field_name).upper(), time.strftime('%Y%m%d', datetime_tuple))

    def setDateFieldFmtByNum(self, n_field, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        return self.setDateFieldByNum(n_field, time.strptime(datetime_value, datetime_fmt))
        
    def setDateFieldFmtByName(self, field_name, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param field_name: Имя поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        return self.setDateFieldByName(str(field_name).upper(), time.strptime(datetime_value, datetime_fmt))

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param n_field: Номер/индекс поля.
        @param datetime_fmt: Строковый формат даты.
        """
        return time.strftime(datetime_fmt, time.strptime(self.getFieldByNum(n_field), '%Y%m%d'))
        
    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param field_name: Имя поля.
        @param datetime_fmt: Строковый формат даты.
        """
        return time.strftime(datetime_fmt, time.strptime(self.getFieldByName(str(field_name).upper()), '%Y%m%d'))
            
    def Skip(self, step=1):
        """
        Движение по таблице.
        @param step: Шаг, если <0 то к началу,
            если >0 то к концу таблицы.
        """
        return pyDBF.Skip(step)

    def Next(self):
        """
        Перейти на следующую запись.
        """
        return pyDBF.Skip(1)

    def Prev(self):
        """
        Перейти на предыдущую запись.
        """
        return pyDBF.Skip(-1)

    def Goto(self, rec_no=0):
        """
        Перейти на запись.
        @param rec_no: Номер записи.
        """
        return pyDBF.Goto(rec_no)

    def First(self):
        """
        Перейти на первую запись.
        """
        return pyDBF.Goto(0)

    def Last(self):
        """
        Перейти на последнюю запись.
        """
        return pyDBF.Goto(self.getRecCount()-1)

    def EOF(self):
        """
        Конец таблицы.
        """
        return pyDBF.Eof()

    def BOF(self):
        """
        Начало таблицы.
        """
        return pyDBF.Bof()

    def DelRec(self):
        """
        Пометить запись как удаленную.
        """
        return pyDBF.Delete(DEL_REC_FLAG)

    def UnDelRec(self):
        """
        Снять метку о удалении записи.
        """
        return pyDBF.Delete(UNDEL_REC_FLAG)

    def IsDelRec(self):
        """
        Помечена запись как удаленная?
        """
        return pyDBF.Delete(IS_DEL_REC_FLAG)

    def Del(self, del_flag):
        """
        Управление удалением записи.
        @param del_flag: Флаг управления.
        """
        return pyDBF.Delete(del_flag)

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        return None

    def AppendRec(self, *rec_num, **rec_name):
        """
        Добавление пустой записи в конец таблицы.
        @param rec_num: Запись по номерам.
        @param rec_name: Запись по именам.
        """
        ok = pyDBF.Append()
        if rec_num:
            for i_field in range(len(rec_num)):
                self.setFieldByNum(i_field, rec_num[i_field])
        if rec_name:
            for field_name in rec_name.keys():
                self.setFieldByName(field_name, rec_name[field_name])
        return ok

    def getRecDict(self):
        """
        Получить текущую запись в виде словаря.
        """
        if self.IsDelRec():
            log.warning(u'Обращение к записи DBF помеченной на удаление')
            return None
        return dict([(self.getFieldName(field_num),
                    self.getFieldByNum(field_num)) for field_num in range(self.FieldCount())])
        
    def getErrorCode(self):
        """
        Возвратить код ошибки.
        """
        return pyDBF.GetErrorCode()

    def getRecCount(self):
        """
        Количество записей в таблице.
        """
        return pyDBF.GetRecCount()

    def getFieldNum(self, field_name):
        """
        Получить индекс поля по его имени.
        @param field_name: Имя поля.
        """
        return pyDBF.GetFieldNum(str(field_name).upper())

    def FindSort(self, field_name, find_text):
        """
        Поиск текста в поле.
        @param field_name: Имя поля.
        @param find_text: Искомый текст.
        """
        return pyDBF.FindSort(str(field_name).upper(), find_text)

    def getRecNo(self):
        """
        Номер текущей записи.
        """
        return pyDBF.GetRecNo()

    def isUsed(self):
        """
        Используется?
        """
        return pyDBF.IsUsed()

    def Zap(self):
        """
        Запнуть.
        """
        return pyDBF.Zap()

    def Pack(self):
        """
        Упаковать.
        """
        return pyDBF.Pack()

    def getFieldName(self, n_field):
        """
        Получить имя поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        return str(pyDBF.GetFieldName(n_field)).upper()

    def getFieldType(self, n_field):
        """
        Получить тип поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        return pyDBF.GetFieldType(n_field)

    def getFieldLen(self, n_field):
        """
        Получить длину поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        return pyDBF.GetFieldLength(n_field)

    def getFieldDecimal(self, n_field):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        return pyDBF.GetFieldDecimal(n_field)


class icDBFFileDBFPY(icDBFFilePrototype):
    """
    Файл *.DBF.
    """

    def __init__(self, dbf_filename=None):
        """
        Конструктор.
        @param dbf_filename: Имя DBF файла, с которым работает класс.
        """
        icDBFFilePrototype.__init__(self, dbf_filename)
        # Автовыравнивание значений полей
        self.AutoAlign = RIGHT_ALIGN
        
        self._dbf = None        # Объект DBF
        self._cur_rec_no = -1   # Номер текущей записи
        self._rec_count = -1    # Количество записей

    def Create(self, dbf_struct=[], dbf_filename=None, bReCreate=True):
        """
        Создать DBF файл по описанию его структуры.
        @param dbf_struct: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param dbf_filename: Имя DBF файла.
        @param bReCreate: Указание того, что если файл существует,
            то пересоздать его.
        @return: True/False.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            try:
                import dbfpy3.dbf
            except ImportError:
                log.error(u'Ошибка импорта dbfpy3.dbf')
                return False

            self._dbf = dbfpy3.dbf.Dbf(dbf_filename, new=bReCreate)
            # Добавить поля
            fields = [(fld['name'].upper(), fld['type'], fld['len'], fld['decimal']) for fld in dbf_struct]
            self._dbf.addField(*fields)

            # Создать файл
            self._dbf.flush()
            self._dbf.close()
            return True
        return False

    def Open(self, dbf_filename=None):
        """
        Открыть DBF файл.
        @param dbf_filename: Имя DBF файла.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            try:
                import dbfpy3.dbf
            except ImportError:
                log.error(u'Ошибка импорта dbfpy3.dbf')
                return False

            self._dbf = dbfpy3.dbf.Dbf(self._dbf_file_name)
            self._cur_rec_no = 0
            return True
        return False

    def Close(self):
        """
        Закрыть.
        """
        if self._dbf:
            self._cur_rec_no = -1
            return self._dbf.close()
        return False

    def FieldCount(self):
        """
        Количество полей.
        """
        if self._dbf:
            return len(self._dbf.fieldDefs)
        return -1

    def getFieldByNum(self, n_field):
        """
        Получить значение поля по его индексу.
        @param n_field: Номер/индекс поля.
        """
        if self._dbf:
            cur_record = self._get_current_record()
            return cur_record.asList()[int(n_field)]
        return None

    def getFieldByName(self, field_name):
        """
        Получить значение поля по его имени.
        @param field_name: Имя поля.
        """
        if self._dbf:
            cur_record = self._get_current_record()
            return cur_record[str(field_name).upper()]
        return None

    def setFieldByNum(self, n_field, field_value, align=None):
        """
        Установить значение поля по индексу.
        @param n_field: Номер/индекс поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        field_name=self.getFieldName(n_field)
        return self.setFieldByName(field_name, field_value, align)

    def setFieldByName(self, field_name, field_value, align=None):
        """
        Установить значение поля по имени.
        @param field_name: Имя поля.
        @param field_value: Значение поля.
        @param align: Выравнивание.
        """
        if align is None:
            align = self.AutoAlign
        field_name = str(field_name).upper()
        
        if self._dbf:
            cur_record = self._get_current_record()
            cur_record[field_name] = self._alignValueByName(field_name, field_value, align)
            cur_record.store()
            return True
        return False

    def setDateFieldByNum(self, n_field, datetime_tuple):
        """
        Установить значение поля даты по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        pass
        
    def setDateFieldByName(self, field_name, datetime_tuple):
        """
        Установить значение поля даты по имени.
        @param field_name: Имя поля.
        @param datetime_tuple: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        pass

    def setDateFieldFmtByNum(self, n_field, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param n_field: Номер/индекс поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        pass
        
    def setDateFieldFmtByName(self, field_name, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param field_name: Имя поля.
        @param datetime_value: Значение поля даты(строка)
            в формате datetime_fmt.
        @param datetime_fmt: Строковый формат даты.
        """
        pass

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param n_field: Номер/индекс поля.
        @param datetime_fmt: Строковый формат даты.
        """
        pass
        
    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param field_name: Имя поля.
        @param datetime_fmt: Строковый формат даты.
        """
        pass
            
    def Skip(self, step=1):
        """
        Движение по таблице.
        @param step: Шаг, если <0 то к началу,
            если >0 то к концу таблицы.
        """
        self._cur_rec_no += step
        self._cur_rec_no = max(0, self._cur_rec_no)
        self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
        return self._cur_rec_no

    def Next(self):
        """
        Перейти на следующую запись.
        """
        return self.Skip(1)

    def Prev(self):
        """
        Перейти на предыдущую запись.
        """
        return self.Skip(-1)

    def Goto(self, rec_no=0):
        """
        Перейти на запись.
        @param rec_no: Номер записи.
        """
        self._cur_rec_no = rec_no
        self._cur_rec_no = max(0, self._cur_rec_no)
        self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
        return self._cur_rec_no

    def First(self):
        """
        Перейти на первую запись.
        """
        return self.Goto(0)

    def Last(self):
        """
        Перейти на последнюю запись.
        """
        return self.Goto(self.getRecCount()-1)

    def EOF(self):
        """
        Конец таблицы.
        """
        return bool(self._cur_rec_no >= self.getRecCount())

    def BOF(self):
        """
        Начало таблицы.
        """
        return bool(self._cur_rec_no <= 0)

    def _get_current_record(self):
        """
        Объект текущей записи.
        """
        if 0 <= self._cur_rec_no < self.getRecCount():
            try:
                return self._dbf[self._cur_rec_no]
            except:
                log.fatal(u'Ошибка получения данных строки [%d] DBF файла <%s>' % (self._cur_rec_no,
                                                                                   self.getDBFFileName()))
        return None
        
    def DelRec(self):
        """
        Пометить запись как удаленную.
        """
        cur_record = self._get_current_record()
        if cur_record:
            cur_record.delete()
            self._rec_count -= 1
            return True
        return False            

    def UnDelRec(self):
        """
        Снять метку о удалении записи.
        """
        pass

    def IsDelRec(self):
        """
        Помечена запись как удаленная?
        """
        cur_record = self._get_current_record()
        if cur_record:
            return cur_record.deleted
        return False            

    def Del(self, del_flag):
        """
        Управление удалением записи.
        @param del_flag: Флаг управления.
        """
        pass

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        pass

    def AppendRec(self, *rec_num, **rec_name):
        """
        Добавление пустой записи в конец таблицы.
        @param rec_num: Запись по номерам.
        @param rec_name: Запись по именам.
        """
        ok = False
        if self._dbf:
            rec = self._dbf.newRecord()
            if rec_num:
                for i_field in range(len(rec_num)):
                    self.setFieldByNum(i_field, rec_num[i_field])
            if rec_name:
                for field_name in rec_name.keys():
                    self.setFieldByName(field_name, rec_name[field_name])
            rec.store()
            self._rec_count += 1
        return ok

    def getRecDict(self):
        """
        Получить текущую запись в виде словаря.
        """
        cur_record = self._get_current_record()
        if cur_record is None:
            log.warning(u'Не определена текущая запись DBF файла')
            return None
        if cur_record.deleted:
            log.warning(u'Обращение к записи DBF помеченной на удаление')
            return None

        if cur_record:
            return cur_record.asDict()
        return None
        
    def getErrorCode(self):
        """
        Возвратить код ошибки.
        """
        pass

    def getRecCount(self):
        """
        Количество записей в таблице.
        """
        if self._dbf:
            if self._rec_count < 0:
                self._rec_count = len(self._dbf)
        else:
            self._rec_count = -1
        return self._rec_count

    def getFieldNum(self, field_name):
        """
        Получить индекс поля по его имени.
        @param field_name: Имя поля.
        """
        if self._dbf:
            return self._dbf.indexOfFieldName(str(field_name).upper())
        return -1

    def FindSort(self, field_name, find_text):
        """
        Поиск текста в поле.
        @param field_name: Имя поля.
        @param find_text: Искомый текст.
        """
        pass

    def filterRecsByField(self, field_name, value):
        """
        Отфильтровать все записи DBF файла по значению поля.
            Функция вначале открывает DBF файл.
            Затем пробегается по записям.
            Выбирает нужные.
            В конце закрывает DBF файл.
        @param field_name: Имя поля.
        @param value: Значение поля.
        @return: Возвращает список отфильтрованных записей-строк в виде словарей
            или пустой список в случае ошибки.
        """
        try:
            records = list()
            open_ok = self.Open()
            if not open_ok:
                log.warning(u'Ошибка открытия файла <%s>' % self.getDBFFileName())
                return list()

            record = self.getRecDict()
            while not self.EOF():
                if field_name in record:
                    field_value = record[field_name]
                    if field_value == value:
                        records.append(record)
                else:
                    log.warning(u'Поле <%s> не найдено в записи среди %s' % (field_name, record.keys()))
                self.Next()
                record = self.getRecDict()
            self.Close()

            return records
        except:
            self.Close()
            log.fatal(u'Ошибка фильтрации записей DBF файла <%s> поля <%s> по значению <%s>' % (self.getDBFFileName(),
                                                                                                field_name, value))
        return list()

    def getRecNo(self):
        """
        Номер текущей записи.
        """
        return self._cur_rec_no

    def isUsed(self):
        """
        Используется?
        """
        pass

    def Zap(self):
        """
        Запнуть.
        """
        pass

    def Pack(self):
        """
        Упаковать.
        """
        pass

    def getFieldName(self, n_field):
        """
        Получить имя поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        if self._dbf:
            field_name = self._dbf.fieldNames[int(n_field)]
            return str(field_name).upper()
        return None

    def getFieldType(self, n_field):
        """
        Получить тип поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.typeCode
        return None

    def getFieldLen(self, n_field):
        """
        Получить длину поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.length
        return None

    def getFieldDecimal(self, n_field):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param n_field: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.decimalCount
        return None


class icDBFFileReadOnly(icDBFFilePrototype):
        """
        Файл *.DBF только для чтения.
        Этот класс сделан для работы с DBF файлами в режиме только для чтения.
        Требуется установленная библиотека <dbfread>. [https://github.com/olemb/dbfread/]
        Некоторые DBF файлы не читаются штатными библиотеками.
        Для этого используем этот класс.
        """

        def __init__(self, dbf_filename=None, encoding=DEFAULT_DBF_ENCODING):
            """
            Конструктор.
            @param dbf_filename: Имя DBF файла, с которым работает класс.
            @param encoding: Кодировка DBF файла.
            """
            icDBFFilePrototype.__init__(self, dbf_filename)

            self.encoding = encoding

            self._dbf = None  # Объект DBF
            self._cur_rec_no = -1  # Номер текущей записи
            self._rec_count = -1  # Количество записей

        def Open(self, dbf_filename=None, encoding=DEFAULT_DBF_ENCODING):
            """
            Открыть DBF файл.
            @param dbf_filename: Имя DBF файла.
            """
            if dbf_filename:
                self._dbf_file_name = dbf_filename

            if encoding:
                self.encoding = encoding

            if self._dbf_file_name and os.path.exists(self._dbf_file_name):
                try:
                    import dbfread
                except ImportError:
                    log.error(u'Для использования этого класса необходимо установить библиотеку <dbfread> [https://github.com/olemb/dbfread/]')
                    return False
                self._dbf = dbfread.DBF(self._dbf_file_name, load=True, encoding=self.encoding)
                self._cur_rec_no = 0
                return True
            return False

        def Close(self):
            """
            Закрыть.
            """
            if self._dbf:
                self._cur_rec_no = -1
                self._dbf = None
                return True
            return False

        def FieldCount(self):
            """
            Количество полей.
            """
            if self._dbf:
                return len(self._dbf.fields)
            return -1

        def getFieldByNum(self, n_field):
            """
            Получить значение поля по его индексу.
            @param n_field: Номер/индекс поля.
            """
            if self._dbf:
                cur_record = self._get_current_record()
                return list(cur_record.values())[int(n_field)]
            return None

        def getFieldByName(self, field_name):
            """
            Получить значение поля по его имени.
            @param field_name: Имя поля.
            """
            if self._dbf:
                cur_record = self._get_current_record()
                return dict(cur_record)[str(field_name).upper()]
            return None

        def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
            """
            Получить значение поля даты в определенном формате по номеру/индексу поля.
            @param n_field: Номер/индекс поля.
            @param datetime_fmt: Строковый формат даты.
            """
            dt_value = self.getFieldByNum(n_field)
            if dt_value:
                return dt_value.strftime(datetime_fmt)
            return None

        def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
            """
            Получить значение поля даты в определенном формате по имени поля.
            @param field_name: Имя поля.
            @param datetime_fmt: Строковый формат даты.
            """
            dt_value = self.getFieldByName(field_name)
            if dt_value:
                return dt_value.strftime(datetime_fmt)
            return None

        def Skip(self, step=1):
            """
            Движение по таблице.
            @param step: Шаг, если <0 то к началу,
                если >0 то к концу таблицы.
            """
            self._cur_rec_no += step
            self._cur_rec_no = max(0, self._cur_rec_no)
            self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
            return self._cur_rec_no

        def Next(self):
            """
            Перейти на следующую запись.
            """
            return self.Skip(1)

        def Prev(self):
            """
            Перейти на предыдущую запись.
            """
            return self.Skip(-1)

        def Goto(self, rec_no=0):
            """
            Перейти на запись.
            @param rec_no: Номер записи.
            """
            self._cur_rec_no = rec_no
            self._cur_rec_no = max(0, self._cur_rec_no)
            self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
            return self._cur_rec_no

        def First(self):
            """
            Перейти на первую запись.
            """
            return self.Goto(0)

        def Last(self):
            """
            Перейти на последнюю запись.
            """
            return self.Goto(self.getRecCount() - 1)

        def EOF(self):
            """
            Конец таблицы.
            """
            return bool(self._cur_rec_no >= self.getRecCount())

        def BOF(self):
            """
            Начало таблицы.
            """
            return bool(self._cur_rec_no <= 0)

        def _get_current_record(self):
            """
            Объект текущей записи.
            """
            if 0 <= self._cur_rec_no < self.getRecCount():
                try:
                    return self._dbf.records[self._cur_rec_no]
                except:
                    log.fatal(u'Ошибка получения данных строки [%d] DBF файла <%s>' % (self._cur_rec_no,
                                                                                       self.getDBFFileName()))
            return None

        def IsDelRec(self):
            """
            Помечена запись как удаленная?
            """
            # cur_record = self._get_current_record()
            # if cur_record:
            #     return cur_record.deleted
            return False

        def getRecDict(self):
            """
            Получить текущую запись в виде словаря.
            """
            cur_record = self._get_current_record()

            if self.IsDelRec():
                log.warning(u'Обращение к записи DBF помеченной на удаление')
                return None

            if cur_record:
                return dict(cur_record)
            return None

        def getErrorCode(self):
            """
            Возвратить код ошибки.
            """
            pass

        def getRecCount(self):
            """
            Количество записей в таблице.
            """
            if self._dbf:
                if self._rec_count < 0:
                    self._rec_count = len(self._dbf)
            else:
                self._rec_count = -1
            return self._rec_count

        def getFieldNum(self, field_name):
            """
            Получить индекс поля по его имени.
            @param field_name: Имя поля.
            """
            if self._dbf:
                field_names = [field.name for field in self._dbf.fields]
                return field_names.index(str(field_name).upper())
            return -1

        def FindSort(self, field_name, find_text):
            """
            Поиск текста в поле.
            @param field_name: Имя поля.
            @param find_text: Искомый текст.
            """
            pass

        def filterRecsByField(self, field_name, value):
            """
            Отфильтровать все записи DBF файла по значению поля.
                Функция вначале открывает DBF файл.
                Затем пробегается по записям.
                Выбирает нужные.
                В конце закрывает DBF файл.                
            @param field_name: Имя поля.
            @param value: Значение поля.
            @return: Возвращает список отфильтрованных записей-строк в виде словарей
                или пустой список в случае ошибки.
            """
            try:
                records = list()
                open_ok = self.Open()
                if not open_ok:
                    log.warning(u'Ошибка открытия файла <%s>' % self.getDBFFileName())
                    return list()

                value = value.strip()
                record = self.getRecDict()
                while not self.EOF():
                    if field_name in record:
                        field_value = record[field_name].strip()
                        if field_value == value:
                            records.append(record)
                    else:
                        log.warning(u'Поле <%s> не найдено в записи среди %s' % (field_name, record.keys()))
                    self.Next()
                    record = self.getRecDict()
                self.Close()

                return records
            except:
                self.Close()
                log.fatal(
                    u'Ошибка фильтрации записей DBF файла <%s> поля <%s> по значению <%s>' % (self.getDBFFileName(),
                                                                                              field_name, value))
            return list()

        def getIndexRecsByField(self, sFieldName):
            """
            Отфильтровать все записи DBF файла по значению поля и представить их в виде словаря.
                Функция вначале открывает DBF файл.
                Затем пробегается по записям.
                Выбирает нужные.
                В конце закрывает DBF файл.                
            @param sFieldName: Имя поля.
            @return: Словарь:
                {
                    Значение 1 поля :
                        список отфильтрованных записей-строк в виде словарей
                    , ...
                }
                или пустой словарь в случае ошибки.
            """
            try:
                index_records = dict()
                open_ok = self.Open()
                if not open_ok:
                    log.warning(u'Ошибка открытия файла <%s>' % self.getDBFFileName())
                    return dict()

                record = self.getRecDict()
                while not self.EOF():
                    if sFieldName in record:
                        field_value = record[sFieldName].strip()
                        if field_value in index_records:
                            index_records[field_value].append(record)
                        else:
                            index_records[field_value] = [record]
                    else:
                        log.warning(u'Поле <%s> не найдено в записи среди %s' % (sFieldName, record.keys()))
                    self.Next()
                    record = self.getRecDict()
                self.Close()

                return index_records
            except:
                self.Close()
                log.fatal(
                    u'Ошибка фильтрации записей DBF файла <%s> поля <%s>' % (self.getDBFFileName(),
                                                                             sFieldName))
            return dict()

        def getRecNo(self):
            """
            Номер текущей записи.
            """
            return self._cur_rec_no

        def isUsed(self):
            """
            Используется?
            """
            pass

        def getFieldName(self, n_field):
            """
            Получить имя поля по номеру/индексу.
            @param n_field: Номер/индекс поля.
            """
            if self._dbf:
                field_names = [field.name for field in self._dbf.fields]
                return str(field_names[n_field]).upper()
            return None

        def getFieldType(self, n_field):
            """
            Получить тип поля по номеру/индексу.
            @param n_field: Номер/индекс поля.
            """
            if self._dbf:
                field_types = [field.type for field in self._dbf.fields]
                return field_types[n_field]
            return None

        def getFieldLen(self, n_field):
            """
            Получить длину поля по номеру/индексу.
            @param n_field: Номер/индекс поля.
            """
            if self._dbf:
                field_lengths = [field.length for field in self._dbf.fields]
                return field_lengths[n_field]
            return None

        def getFieldDecimal(self, n_field):
            """
            Получить указание десятичной точки поля по номеру/индексу.
            @param n_field: Номер/индекс поля.
            """
            if self._dbf:
                field_decimals = [field.decimal_count for field in self._dbf.fields]
                return field_decimals[n_field]
            return None


# Подменить класс в зависимости от возможности импортировать pyDBF.pyd
if is_pyd_import:
    icDBFFile = icDBFFilePYD
else:
    icDBFFile = icDBFFileDBFPY


def test():
    """
    Функция тестирования.
    """
    dbf_f = icDBFFile()
    dbf_f.AutoAlign = LEFT_ALIGN
    dbf_f1 = icDBFFile()
    struct = [{'name': 's',
               'type': 'C',
               'len': 52,
               'decimal': 0},
              {'name': 'n',
               'type': 'N',
               'len': 10,
               'decimal': 4},
              {'name': 'function',
               'type': 'N',
               'len': 10,
               'decimal': 4},
              ]
    dbf_f.Create(struct, 'test.dbf')
    dbf_f1.Create(struct, 'test1.dbf')
    for i in range(10):
        print(i)
        dbf_f.Open()
        dbf_f.AppendRec(n=float(i), f=float(i)+float(i)/1000000.0)
        dbf_f.setFieldByName('s', '%s%d ' % ('AAA', i), LEFT_ALIGN)
        dbf_f.Close()

        dbf_f1.Open()
        dbf_f1.AppendRec('%s%d ' % ('?', i), i, float(i)+float(i)/1000000.0)
        dbf_f1.Close()


def test2():
    d = icDBFFile('C:/defis/STIS/arch/ik051023.olp')
    print(d.Open())
    d.First()
    print(d.EOF())
    d.Close()


if __name__ == '__main__':
    test()
