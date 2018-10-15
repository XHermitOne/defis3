#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций установки связи с БД через ODBC.

Using an ODBC driver

Microsoft have written and distributed multiple ODBC drivers for SQL Server:

    {SQL Server} - released with SQL Server 2000
    {SQL Native Client} - released with SQL Server 2005 (also known as version 9.0)
    {SQL Server Native Client 10.0} - released with SQL Server 2008
    {SQL Server Native Client 11.0} - released with SQL Server 2012
    {ODBC Driver 11 for SQL Server} - supports SQL Server 2005 through 2014
    {ODBC Driver 13 for SQL Server} - supports SQL Server 2005 through 2016
    {ODBC Driver 13.1 for SQL Server} - supports SQL Server 2008 through 2016
    {ODBC Driver 17 for SQL Server} - supports SQL Server 2008 through 2017
"""

try:
    import mx.ODBC.Windows as mx_odbc
except ImportError:
    pass
    
from ic.interfaces import icsourceinterface
from ic.log import log

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
    log.info(u'Создание коннекшна ODBC <%s : %s : %s : %s>' % (DB_['dbname'],
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
            log.error(u'ODBC: Ошибка установления связи с БД. ConnectionString: <%s>' % connection_string)
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
            log.error(u'ODBC: Ошибка разрыва связи с БД.')
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
            log.error(u'ODBC: Ошибка выполнения запроса. SQL: <%s>' % SQLTxt_)
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
                log.info(u'ODBC: Не определена связь с БД!')
        except:
            log.error(u'ODBC: Ошибка создания курсора.')
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
            log.error(u'ODBC: Ошибка закрытия курсора')
