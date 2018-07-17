#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль классов и функций работы с простым файлом *.DBF.
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
    import dbfpy.dbf
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

__version__ = (0, 0, 3, 1)


class icDBFFilePrototype:
    """
    Файл *.DBF.
    """

    def __init__(self, DBFFileName_=None):
        """
        Конструктор.
        @param DBFFileName_: Имя DBF файла, с которым работает класс.
        """
        self._dbf_file_name = DBFFileName_

    def getDBFFileName(self):
        return self._dbf_file_name

    def __del__(self):
        """
        Деструктор.
        """
        self.Close()

    def Create(self, DBFStruct_=[], DBFFileName_=None, ReCreate_=True):
        """
        Создать DBF файл по описанию его структуры.
        @param DBFStruct_: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param DBFFileName_: Имя DBF файла.
        @param ReCreate_: Указание того, что если файл существует, 
            то пересоздать его.
        """
        assert 0, u'Метод не определен'

    def Open(self, DBFFileName_=None):
        """
        Открыть DBF файл.
        @param DBFFileName_: Имя DBF файла.
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

    def getFieldByNum(self, FieldNum_):
        """
        Получить значение поля по его индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldByName(self, FieldName_):
        """
        Получить значение поля по его имени.
        @param FieldName_: Имя поля.
        """
        assert 0, u'Метод не определен'

    def setFieldByNum(self, FieldNum_, FieldValue_, Align_=None):
        """
        Установить значение поля по индексу.
        @param FieldNum_: Номер/индекс поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        assert 0, u'Метод не определен'

    def setFieldByName(self, FieldName_, FieldValue_, Align_=None):
        """
        Установить значение поля по имени.
        @param FieldName_: Имя поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        assert 0, u'Метод не определен'

    def setDateFieldByNum(self, FieldNum_, DateTimeTuple_):
        """
        Установить значение поля даты по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        assert 0, u'Метод не определен'
        
    def setDateFieldByName(self, FieldName_, DateTimeTuple_):
        """
        Установить значение поля даты по имени.
        @param FieldName_: Имя поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        assert 0, u'Метод не определен'

    def setDateFieldFmtByNum(self, FieldNum_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
        
    def setDateFieldFmtByName(self, FieldName_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param FieldName_: Имя поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        assert 0, u'Метод не определен'

    def getDateFieldFmtByNum(self, FieldNum_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
        
    def getDateFieldFmtByName(self, FieldName_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param FieldName_: Имя поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        assert 0, u'Метод не определен'
            
    def Skip(self, Step_=1):
        """
        Движение по таблице.
        @param Step_: Шаг, если <0 то к началу, 
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

    def Goto(self, RecNo_=0):
        """
        Перейти на запись.
        @param RecNo_: Номер записи.
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

    def Del(self, DelFlag_):
        """
        Управление удалением записи.
        @param DelFlag_: Флаг управления.
        """
        assert 0, u'Метод не определен'

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        assert 0, u'Метод не определен'

    def AppendRec(self, *RecNum_, **RecName_):
        """
        Добавление пустой записи в конец таблицы.
        @param RecNum_: Запись по номерам.
        @param RecName_: Запись по именам.
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

    def getFieldNum(self, FieldName_):
        """
        Получить индекс поля по его имени.
        @param FieldName_: Имя поля.
        """
        assert 0, u'Метод не определен'

    def FindSort(self, FieldName_, FindText_):
        """
        Поиск текста в поле.
        @param FieldName_: Имя поля.
        @param FindText_: Искомый текст.
        """
        assert 0, u'Метод не определен'

    def filterRecsByField(self, sFieldName, sValue):
        """
        Отфильтровать все записи DBF файла по значению поля.
            Функция вначале открывает DBF файл.
            Затем пробегается по записям.
            Выбирает нужные.
            В конце закрывает DBF файл.
        @param sFieldName: Имя поля.
        @param sValue: Значение поля.
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

    def getFieldName(self, FieldNum_):
        """
        Получить имя поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldType(self, FieldNum_):
        """
        Получить тип поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldLen(self, FieldNum_):
        """
        Получить длину поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def getFieldDecimal(self, FieldNum_):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        assert 0, u'Метод не определен'

    def _del_last_eof_char(self, DBFFileName_):
        """
        Удалить последний символ,  если он символ EOF.
        @param DBFFileName_: Имя *.DBF файла.
        """
        if os.path.isfile(DBFFileName_):
            try:
                dbf_file = None
                dbf_file = open(DBFFileName_, 'r+')
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

    def _alignValueByName(self, FieldName_, FieldValue_, Align_=RIGHT_ALIGN):
        """
        Выравнивание по краю.
            По умолчаниу выравнивается по правому краю
        @param FieldName_: Имя поля.
        @param FieldValue_: Значение поля.
        @param Align_: Указание выравнивания.
        @return: Возвращает строку, выравненную по полю.
        """
        if FieldValue_ is None:
            FieldValue_ = ''

        field_len = self.getFieldLen(self.getFieldNum(str(FieldName_).upper()))
        field_val = str(FieldValue_)[:field_len]
        if Align_ == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif Align_ == RIGHT_ALIGN:
            # По умолчаниу выравнивается по правому краю
            pass
        return field_val

    def _alignValueByNum(self, FieldNum_, FieldValue_, Align_=RIGHT_ALIGN):
        """
        Выравнивание по краю.
            По умолчаниу выравнивается по правому краю
        @param FieldNum_: Индекс/номер поля.
        @param FieldValue_: Значение поля.
        @param Align_: Указание выравнивания.
        @return: Возвращает строку, выравненную по полю.
        """
        if FieldValue_ is None:
            FieldValue_ = ''

        field_len = self.getFieldLen(FieldNum_)
        field_val = str(FieldValue_)[:field_len]
        if Align_ == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif Align_ == RIGHT_ALIGN:
            # По умолчаниу выравнивается по правому краю
            pass
        return field_val


class icDBFFilePYD(icDBFFilePrototype):
    """
    Файл *.DBF.
    """

    def __init__(self, DBFFileName_=None):
        """
        Конструктор.
        @param DBFFileName_: Имя DBF файла, с которым работает класс.
        """
        icDBFFilePrototype.__init__(self, DBFFileName_)
        # Автовыравнивание значений полей
        self.AutoAlign = RIGHT_ALIGN

    def Create(self, DBFStruct_=[], DBFFileName_=None, ReCreate_=True):
        """
        Создать DBF файл по описанию его структуры.
        @param DBFStruct_: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param DBFFileName_: Имя DBF файла.
        @param ReCreate_: Указание того, что если файл существует, 
            то пересоздать его.
        """
        if DBFFileName_:
            self._dbf_file_name = DBFFileName_
        if self._dbf_file_name:
            # Можно пересоздать?
            if os.path.exists(self._dbf_file_name):
                if ReCreate_:
                    os.remove(self._dbf_file_name)
                else:
                    return False

            # Сначала очистить все определения полей
            pyDBF.ClearFields()
            # Добавить поля
            for dbf_field in DBFStruct_:
                # Нормализовать описание по специфиации
                field = copy.deepcopy(SPC_DBF_FIELD)
                field.update(dbf_field)
                # Добавить описание поля
                pyDBF.AddField(field['name'].upper(), field['type'], 
                               field['len'], field['decimal'])

            # Создать файл
            return not pyDBF.Create(self._dbf_file_name)
        return False

    def Open(self, DBFFileName_=None):
        """
        Открыть DBF файл.
        @param DBFFileName_: Имя DBF файла.
        """
        if DBFFileName_:
            self._dbf_file_name = DBFFileName_
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

    def getFieldByNum(self, FieldNum_):
        """
        Получить значение поля по его индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        return pyDBF.GetFieldByNum(FieldNum_)

    def getFieldByName(self, FieldName_):
        """
        Получить значение поля по его имени.
        @param FieldName_: Имя поля.
        """
        return pyDBF.GetFieldByName(str(FieldName_).upper())

    def setFieldByNum(self, FieldNum_, FieldValue_, Align_=None):
        """
        Установить значение поля по индексу.
        @param FieldNum_: Номер/индекс поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        return pyDBF.SetFieldByNum(int(FieldNum_),
                                   self._alignValueByNum(FieldNum_, FieldValue_, self.AutoAlign))

    def setFieldByName(self, FieldName_, FieldValue_, Align_=None):
        """
        Установить значение поля по имени.
        @param FieldName_: Имя поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        if Align_ is None:
            Align_ = self.AutoAlign
        field_name = str(FieldName_).upper()
        return pyDBF.SetFieldByName(field_name, 
                                    self._alignValueByName(field_name, FieldValue_, Align_))

    def setDateFieldByNum(self, FieldNum_, DateTimeTuple_):
        """
        Установить значение поля даты по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        return self.setFieldByNum(FieldNum_, time.strftime('%Y%m%d', DateTimeTuple_))
        
    def setDateFieldByName(self, FieldName_, DateTimeTuple_):
        """
        Установить значение поля даты по имени.
        @param FieldName_: Имя поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        return self.setFieldByName(str(FieldName_).upper(), time.strftime('%Y%m%d', DateTimeTuple_))

    def setDateFieldFmtByNum(self, FieldNum_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        return self.setDateFieldByNum(FieldNum_, time.strptime(DateTime_, DateTimeFmt_))
        
    def setDateFieldFmtByName(self, FieldName_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param FieldName_: Имя поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        return self.setDateFieldByName(str(FieldName_).upper(), time.strptime(DateTime_, DateTimeFmt_))

    def getDateFieldFmtByNum(self, FieldNum_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        return time.strftime(DateTimeFmt_, time.strptime(self.getFieldByNum(FieldNum_), '%Y%m%d'))
        
    def getDateFieldFmtByName(self, FieldName_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param FieldName_: Имя поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        return time.strftime(DateTimeFmt_, time.strptime(self.getFieldByName(str(FieldName_).upper()), '%Y%m%d'))
            
    def Skip(self, Step_=1):
        """
        Движение по таблице.
        @param Step_: Шаг, если <0 то к началу, 
            если >0 то к концу таблицы.
        """
        return pyDBF.Skip(Step_)

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

    def Goto(self, RecNo_=0):
        """
        Перейти на запись.
        @param RecNo_: Номер записи.
        """
        return pyDBF.Goto(RecNo_)

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

    def Del(self, DelFlag_):
        """
        Управление удалением записи.
        @param DelFlag_: Флаг управления.
        """
        return pyDBF.Delete(DelFlag_)

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        return None

    def AppendRec(self, *RecNum_, **RecName_):
        """
        Добавление пустой записи в конец таблицы.
        @param RecNum_: Запись по номерам.
        @param RecName_: Запись по именам.
        """
        ok = pyDBF.Append()
        if RecNum_:
            for i_field in range(len(RecNum_)):
                self.setFieldByNum(i_field, RecNum_[i_field])
        if RecName_:
            for field_name in RecName_.keys():
                self.setFieldByName(field_name, RecName_[field_name])
        return ok

    def getRecDict(self):
        """
        Получить текущую запись в виде словаря.
        """
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

    def getFieldNum(self, FieldName_):
        """
        Получить индекс поля по его имени.
        @param FieldName_: Имя поля.
        """
        return pyDBF.GetFieldNum(str(FieldName_).upper())

    def FindSort(self,FieldName_, FindText_):
        """
        Поиск текста в поле.
        @param FieldName_: Имя поля.
        @param FindText_: Искомый текст.
        """
        return pyDBF.FindSort(str(FieldName_).upper(), FindText_)

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

    def getFieldName(self, FieldNum_):
        """
        Получить имя поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        return str(pyDBF.GetFieldName(FieldNum_)).upper()

    def getFieldType(self, FieldNum_):
        """
        Получить тип поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        return pyDBF.GetFieldType(FieldNum_)

    def getFieldLen(self, FieldNum_):
        """
        Получить длину поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        return pyDBF.GetFieldLength(FieldNum_)

    def getFieldDecimal(self, FieldNum_):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        return pyDBF.GetFieldDecimal(FieldNum_)


class icDBFFileDBFPY(icDBFFilePrototype):
    """
    Файл *.DBF.
    """

    def __init__(self, DBFFileName_=None):
        """
        Конструктор.
        @param DBFFileName_: Имя DBF файла, с которым работает класс.
        """
        icDBFFilePrototype.__init__(self, DBFFileName_)
        # Автовыравнивание значений полей
        self.AutoAlign = RIGHT_ALIGN
        
        self._dbf = None        # Объект DBF
        self._cur_rec_no = -1   # Номер текущей записи
        self._rec_count = -1    # Количество записей

    def Create(self, DBFStruct_=[], DBFFileName_=None, ReCreate_=True):
        """
        Создать DBF файл по описанию его структуры.
        @param DBFStruct_: Описание структуры DBF файла в формате:
            [{'name':имя поля1,
                'type':тип поля1('C', 'N' и т.п.), 
                'len':длина поля1,
                'decimal':указание десятичной точки поля1}, 
             ...].
        @param DBFFileName_: Имя DBF файла.
        @param ReCreate_: Указание того, что если файл существует, 
            то пересоздать его.
        @return: True/False.
        """
        if DBFFileName_:
            self._dbf_file_name = DBFFileName_
        if self._dbf_file_name:
            self._dbf = dbfpy.dbf.Dbf(DBFFileName_, new=ReCreate_)
            # Добавить поля
            fields = [(fld['name'].upper(), fld['type'], fld['len'], fld['decimal']) for fld in DBFStruct_ ]
            self._dbf.addField(*fields)

            # Создать файл
            self._dbf.flush()
            self._dbf.close()
            return True
        return False

    def Open(self, DBFFileName_=None):
        """
        Открыть DBF файл.
        @param DBFFileName_: Имя DBF файла.
        """
        if DBFFileName_:
            self._dbf_file_name = DBFFileName_
        if self._dbf_file_name:
            self._dbf = dbfpy.dbf.Dbf(self._dbf_file_name)
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

    def getFieldByNum(self, FieldNum_):
        """
        Получить значение поля по его индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        if self._dbf:
            cur_record = self._get_current_record()
            return cur_record.asList()[int(FieldNum_)]
        return None

    def getFieldByName(self, FieldName_):
        """
        Получить значение поля по его имени.
        @param FieldName_: Имя поля.
        """
        if self._dbf:
            cur_record = self._get_current_record()
            return cur_record[str(FieldName_).upper()]
        return None

    def setFieldByNum(self, FieldNum_, FieldValue_, Align_=None):
        """
        Установить значение поля по индексу.
        @param FieldNum_: Номер/индекс поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        field_name=self.getFieldName(FieldNum_)
        return self.setFieldByName(field_name, FieldValue_, Align_)

    def setFieldByName(self, FieldName_, FieldValue_, Align_=None):
        """
        Установить значение поля по имени.
        @param FieldName_: Имя поля.
        @param FieldValue_: Значение поля.
        @param Align_: Выравнивание.
        """
        if Align_ is None:
            Align_ = self.AutoAlign
        field_name = str(FieldName_).upper()
        
        if self._dbf:
            cur_record = self._get_current_record()
            cur_record[field_name] = self._alignValueByName(field_name, FieldValue_, Align_)
            cur_record.store()
            return True
        return False

    def setDateFieldByNum(self, FieldNum_, DateTimeTuple_):
        """
        Установить значение поля даты по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        pass
        
    def setDateFieldByName(self, FieldName_, DateTimeTuple_):
        """
        Установить значение поля даты по имени.
        @param FieldName_: Имя поля.
        @param DateTimeTuple_: Значение поля даты в формате
            кортежа дата+время(см. описание библиотечного модуля time).
        """
        pass

    def setDateFieldFmtByNum(self, FieldNum_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        pass
        
    def setDateFieldFmtByName(self, FieldName_, DateTime_, DateTimeFmt_='%d/%m/%Y'):
        """
        Установить значение поля даты указанного формата по имени.
        @param FieldName_: Имя поля.
        @param DateTime_: Значение поля даты(строка)
            в формате DateTimeFmt_.
        @param DateTimeFmt_: Строковый формат даты.
        """
        pass

    def getDateFieldFmtByNum(self, FieldNum_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по номеру/индексу поля.
        @param FieldNum_: Номер/индекс поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        pass
        
    def getDateFieldFmtByName(self, FieldName_, DateTimeFmt_='%d/%m/%Y'):
        """
        Получить значение поля даты в определенном формате по имени поля.
        @param FieldName_: Имя поля.
        @param DateTimeFmt_: Строковый формат даты.
        """
        pass
            
    def Skip(self, Step_=1):
        """
        Движение по таблице.
        @param Step_: Шаг, если <0 то к началу, 
            если >0 то к концу таблицы.
        """
        self._cur_rec_no += Step_
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

    def Goto(self, RecNo_=0):
        """
        Перейти на запись.
        @param RecNo_: Номер записи.
        """
        self._cur_rec_no = RecNo_
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

    def Del(self, DelFlag_):
        """
        Управление удалением записи.
        @param DelFlag_: Флаг управления.
        """
        pass

    def SetDel(self):
        """
        Cброс/установка/проверка  фильтрации удаленных записей.
        """
        pass

    def AppendRec(self, *RecNum_, **RecName_):
        """
        Добавление пустой записи в конец таблицы.
        @param RecNum_: Запись по номерам.
        @param RecName_: Запись по именам.
        """
        ok = False
        if self._dbf:
            rec = self._dbf.newRecord()
            if RecNum_:
                for i_field in range(len(RecNum_)):
                    self.setFieldByNum(i_field, RecNum_[i_field])
            if RecName_:
                for field_name in RecName_.keys():
                    self.setFieldByName(field_name, RecName_[field_name])
            rec.store()
            self._rec_count += 1
        return ok

    def getRecDict(self):
        """
        Получить текущую запись в виде словаря.
        """
        cur_record = self._get_current_record()
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

    def getFieldNum(self, FieldName_):
        """
        Получить индекс поля по его имени.
        @param FieldName_: Имя поля.
        """
        if self._dbf:
            return self._dbf.indexOfFieldName(str(FieldName_).upper())
        return -1

    def FindSort(self, FieldName_, FindText_):
        """
        Поиск текста в поле.
        @param FieldName_: Имя поля.
        @param FindText_: Искомый текст.
        """
        pass

    def filterRecsByField(self, sFieldName, sValue):
        """
        Отфильтровать все записи DBF файла по значению поля.
            Функция вначале открывает DBF файл.
            Затем пробегается по записям.
            Выбирает нужные.
            В конце закрывает DBF файл.
        @param sFieldName: Имя поля.
        @param sValue: Значение поля.
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
                if sFieldName in record:
                    field_value = record[sFieldName]
                    if field_value == sValue:
                        records.append(record)
                else:
                    log.warning(u'Поле <%s> не найдено в записи среди %s' % (sFieldName, record.keys()))
                self.Next()
                record = self.getRecDict()
            self.Close()

            return records
        except:
            self.Close()
            log.fatal(u'Ошибка фильтрации записей DBF файла <%s> поля <%s> по значению <%s>' % (self.getDBFFileName(),
                                                                                                sFieldName, sValue))
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

    def getFieldName(self, FieldNum_):
        """
        Получить имя поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        if self._dbf:
            field_name = self._dbf.fieldNames[int(FieldNum_)]
            return str(field_name).upper()
        return None

    def getFieldType(self, FieldNum_):
        """
        Получить тип поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(FieldNum_)]
            return field.typeCode
        return None

    def getFieldLen(self, FieldNum_):
        """
        Получить длину поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(FieldNum_)]
            return field.length
        return None

    def getFieldDecimal(self, FieldNum_):
        """
        Получить указание десятичной точки поля по номеру/индексу.
        @param FieldNum_: Номер/индекс поля.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(FieldNum_)]
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

        def __init__(self, DBFFileName_=None, encoding=DEFAULT_DBF_ENCODING):
            """
            Конструктор.
            @param DBFFileName_: Имя DBF файла, с которым работает класс.
            @param encoding: Кодировка DBF файла.
            """
            icDBFFilePrototype.__init__(self, DBFFileName_)

            self.encoding = encoding

            self._dbf = None  # Объект DBF
            self._cur_rec_no = -1  # Номер текущей записи
            self._rec_count = -1  # Количество записей

        def Open(self, DBFFileName_=None, encoding=DEFAULT_DBF_ENCODING):
            """
            Открыть DBF файл.
            @param DBFFileName_: Имя DBF файла.
            """
            if DBFFileName_:
                self._dbf_file_name = DBFFileName_

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

        def getFieldByNum(self, FieldNum_):
            """
            Получить значение поля по его индексу.
            @param FieldNum_: Номер/индекс поля.
            """
            if self._dbf:
                cur_record = self._get_current_record()
                return cur_record.values()[int(FieldNum_)]
            return None

        def getFieldByName(self, FieldName_):
            """
            Получить значение поля по его имени.
            @param FieldName_: Имя поля.
            """
            if self._dbf:
                cur_record = self._get_current_record()
                return dict(cur_record)[str(FieldName_).upper()]
            return None

        def getDateFieldFmtByNum(self, FieldNum_, DateTimeFmt_='%d/%m/%Y'):
            """
            Получить значение поля даты в определенном формате по номеру/индексу поля.
            @param FieldNum_: Номер/индекс поля.
            @param DateTimeFmt_: Строковый формат даты.
            """
            dt_value = self.getFieldByNum(FieldNum_)
            if dt_value:
                return dt_value.strftime(DateTimeFmt_)
            return None

        def getDateFieldFmtByName(self, FieldName_, DateTimeFmt_='%d/%m/%Y'):
            """
            Получить значение поля даты в определенном формате по имени поля.
            @param FieldName_: Имя поля.
            @param DateTimeFmt_: Строковый формат даты.
            """
            dt_value = self.getFieldByName(FieldName_)
            if dt_value:
                return dt_value.strftime(DateTimeFmt_)
            return None

        def Skip(self, Step_=1):
            """
            Движение по таблице.
            @param Step_: Шаг, если <0 то к началу, 
                если >0 то к концу таблицы.
            """
            self._cur_rec_no += Step_
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

        def Goto(self, RecNo_=0):
            """
            Перейти на запись.
            @param RecNo_: Номер записи.
            """
            self._cur_rec_no = RecNo_
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
            #cur_record = self._get_current_record()
            #if cur_record:
            #    return cur_record.deleted
            return False

        def getRecDict(self):
            """
            Получить текущую запись в виде словаря.
            """
            cur_record = self._get_current_record()
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

        def getFieldNum(self, FieldName_):
            """
            Получить индекс поля по его имени.
            @param FieldName_: Имя поля.
            """
            if self._dbf:
                field_names = [field.name for field in self._dbf.fields]
                return field_names.index(str(FieldName_).upper())
            return -1

        def FindSort(self, FieldName_, FindText_):
            """
            Поиск текста в поле.
            @param FieldName_: Имя поля.
            @param FindText_: Искомый текст.
            """
            pass

        def filterRecsByField(self, sFieldName, sValue):
            """
            Отфильтровать все записи DBF файла по значению поля.
                Функция вначале открывает DBF файл.
                Затем пробегается по записям.
                Выбирает нужные.
                В конце закрывает DBF файл.                
            @param sFieldName: Имя поля.
            @param sValue: Значение поля.
            @return: Возвращает список отфильтрованных записей-строк в виде словарей
                или пустой список в случае ошибки.
            """
            try:
                records = list()
                open_ok = self.Open()
                if not open_ok:
                    log.warning(u'Ошибка открытия файла <%s>' % self.getDBFFileName())
                    return list()

                sValue = sValue.strip()
                record = self.getRecDict()
                while not self.EOF():
                    if sFieldName in record:
                        field_value = record[sFieldName].strip()
                        if field_value == sValue:
                            records.append(record)
                    else:
                        log.warning(u'Поле <%s> не найдено в записи среди %s' % (sFieldName, record.keys()))
                    self.Next()
                    record = self.getRecDict()
                self.Close()

                return records
            except:
                self.Close()
                log.fatal(
                    u'Ошибка фильтрации записей DBF файла <%s> поля <%s> по значению <%s>' % (self.getDBFFileName(),
                                                                                              sFieldName, sValue))
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
                    u'Ошибка фильтрации записей DBF файла <%s> поля <%s> по значению <%s>' % (self.getDBFFileName(),
                                                                                              sFieldName, sValue))
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

        def getFieldName(self, FieldNum_):
            """
            Получить имя поля по номеру/индексу.
            @param FieldNum_: Номер/индекс поля.
            """
            if self._dbf:
                field_names = [field.name for field in self._dbf.fields]
                return str(field_names[FieldNum_]).upper()
            return None

        def getFieldType(self, FieldNum_):
            """
            Получить тип поля по номеру/индексу.
            @param FieldNum_: Номер/индекс поля.
            """
            if self._dbf:
                field_types = [field.type for field in self._dbf.fields]
                return field_types[FieldNum_]
            return None

        def getFieldLen(self, FieldNum_):
            """
            Получить длину поля по номеру/индексу.
            @param FieldNum_: Номер/индекс поля.
            """
            if self._dbf:
                field_lengths = [field.length for field in self._dbf.fields]
                return field_lengths[FieldNum_]
            return None

        def getFieldDecimal(self, FieldNum_):
            """
            Получить указание десятичной точки поля по номеру/индексу.
            @param FieldNum_: Номер/индекс поля.
            """
            if self._dbf:
                field_decimals = [field.decimal_count for field in self._dbf.fields]
                return field_decimals[FieldNum_]
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
              {'name': 'f',
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
