#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Поддержка в системе сверток/срезов.
"""

#--- Подключение библиотек ---
from ic.db import tabclass
from ic.utils import resource
#import NSI.spravfunc

# Версия
__version__ = (0, 1, 1, 1)


class icSlice:
    """
    Класс свертки/среза.
    """
    def __init__(self,Cod_):
        """
        Конструктор.
        :param Cod_: Код свертки в справочнике.
        """
        self.sprav_type='Slices'
        #Код свертки в справочнике.
        self.cod=Cod_
        
        self._curData(self.cod)
        
    def getTabSrcName(self):
        """
        Имя таблицы-источника(данных).
        """
        return self.src_tab
        
    def getTabDstName(self):
        """
        Имя таблицы-результата.
        """
        return self.dst_tab
        
    def getSQLBody(self):
        """
        Запрос свертки.
        """
        return  self.sql_body

    def execute(self,DBName_):
        """
        Выполнить.
        """
        sql = self.getSQLBody()
        # print('SLICE SQL:',sql)
        db_connection=tabclass.CreateDBConnection(resource.icGetRes(DBName_,
                                                  'src', nameRes=DBName_))
        if db_connection:
            db_connection.
        
    def _curSlice(self,Cod_):
        """
        Запомнить текущий срез/свертку.
        :param Cod_: Код свертки в справочнике.
        """
        slice_data = NSI.spravfunc.FSprav(self.sprav_type,
                                          Cod_, ['name','s1','s2','s3'])
        self.name = slice_data['name']
        self.src_tab = slice_data['s1']
        self.dst_tab = slice_data['s2']
        self.sql_body = slice_data['s3']
