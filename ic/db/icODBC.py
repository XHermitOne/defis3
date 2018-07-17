#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с БД через ODBC.
"""

try:
    import mx.ODBC.Windows as mx_odbc
except ImportError:
    pass
    
from ic.kernel import io_prnt
from ic.interfaces import icsourceinterface

# Константы
# Тип БД
ODBC_DATASOURCE_TYPE = 'ODBC'

# Спецификация БД
SPC_IC_ODBC = {'type': ODBC_DATASOURCE_TYPE,
               'user': '',
               'connetion_string': '',
               'password': '',
               'from_charset': None,
               'to_charset': None,
               }


def _db_connection_odbc(DB_):
    """
    Создать коннекшн.
    """
    io_prnt.outLog(u'Создание коннекшна ODBC <%s : %s : %s : %s>' % (DB_['dbname'],
                                                                     DB_['host'],
                                                                     DB_['user'],
                                                                     DB_['password']))
    db = MSSQLConnection(db=DB_['dbname'], host=DB_['host'],
                         user=DB_['user'], password=DB_['password'], autoCommit=1)
    return db


class icODBCDataSourcePrototype(icsourceinterface.icSourceInterface):
    """
    Источник данных ODBC.
    """
    
    def __init__(self, Resource_=None):
        """
        Конструктор.
        @param Resource_: Ресурс описания компонента.
        """
        icsourceinterface.icSourceInterface.__init__(self, Resource_)
        
        self._connection_string = Resource_['connection_string']
        self._user = Resource_['user']
        self._password = Resource_['password']
        
        self.conection = None   # Связь с БД
        self.cursor = None      # Курсор последнего запроса

    def getConnectionString(self):
        """
        Строка соединения.
        """
        connection_string = self._connection_string
        if self._user:
            connection_string += ';UID='+self._user
        if self._password:
            connection_string += ';PWD='+self._password
        return connection_string
        
    def connect(self):
        """
        Установить связь с БД.
        """
        self.disconnect()
        connection_string = self.getConnectionString()
        try:
            self.connection = mx_odbc.DriverConnect(connection_string)
        except:
            io_prnt.outErr(u'ODBC: Ошибка установления связи с БД. ConnectionString: <%s>' % connection_string)
        return self.connection
        
    def getConnection(self):
        """
        Связь с БД.
        """
        return self.connection
        
    def disconnect(self):
        """
        Разорвать связь с БД.
        """
        self.closeCursor()
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except:
            io_prnt.outErr(u'ODBC: Ошибка разрыва связи с БД.')
        return self.connection
    
    def execSQL(self, SQLTxt_):
        """
        Выполнить SQL запрос.
        @param SQLTxt_: Текст SQL запроса.
        @return: Результат возвращается в формате icquery.QUERY_TABLE_RESULT.
        Либо None в случае ошибки.
        """
        result = None
        self.createCursor()
        try:
            self.cursor.execute(SQLTxt_)
            recordset = self.cursor.fetchall()
            fields = self.cursor.description
            result = {'__fields__': fields, '__data__': recordset}
        except:
            io_prnt.outErr(u'ODBC: Ошибка выполнения запроса. SQL: <%s>' % SQLTxt_)
        self.closeCursor()
        return result
            
    def createCursor(self):
        """
        Создание курсора.
        """
        try:
            if self.connection:
                self.closeCursor()
                self.cursor = self.connection.cursor()
            else:
                io_prnt.outLog(u'ODBC: Не определена связь с БД!')
        except:
            io_prnt.outErr(u'ODBC: Ошибка создания курсора.')
        return self.cursor

    def getCursor(self):
        """
        Курсор.
        """
        return self.cursor
        
    def closeCursor(self):
        """
        Закрытие курсора.
        """
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
        except:
            io_prnt.outErr(u'ODBC: Ошибка закрытия курсора')
