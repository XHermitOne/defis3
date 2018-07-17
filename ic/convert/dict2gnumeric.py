#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль конвертирования словарно-списковой структуры в xml файл.
"""

import time
from . import dict2xml

__version__ = (0, 0, 1, 2)


def Dict2GnumericFile(Data_, GnumericFileName_, encoding='utf-8'):
    """
    Функция конвертирования.
    """
    try:
        # Начать запись
        xml_file = None
        xml_file = open(GnumericFileName_, 'wt')
        xml_writer = icDict2GnumericWriter(Data_, xml_file, encoding=encoding)
        xml_writer.startDocument()
        xml_writer.setBook()

        # Закончить запись
        xml_writer.endDocument()
        xml_file.close()

        return GnumericFileName_
    except:
        if xml_file:
            xml_file.close()
        raise


class icDict2GnumericWriter(dict2xml.icDICT2XMLWriter):
    """
    Конвертер из словаря в Gnumeric XML представление.
    """
    def __init__(self, data, out=None, encoding='utf-8'):
        """
        Конструктор.
        """
        dict2xml.icDICT2XMLWriter.__init__(self, data, out, encoding)

    def setBook(self, data=None):
        """
        Начало книги.
        """
        if data is None:
            data = self._data
            
        # Время начала создания файла
        self.time_start = time.time()

        self.startElementLevel('gmr:Workbook', {'xmlns:gnm': 'http://www.gnumeric.org/v10.dtd',
                                                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                                'xsi:schemaLocation': 'http://www.gnumeric.org/v9.xsd'})

        # Стили

        # Листы
        worksheets = [element for element in data['children'] if element['name'] == 'Worksheet']
        # Имена листов
        self.setSheetNameIndex(worksheets)
        # Данные листов
        self.setSheets(worksheets)

        self.endElementLevel('gmr:Workbook')
        
        print(u'END SAVE GNUMERIC XML FILE. Time = %s' % time.time()-self.time_start)

    def setSheetNameIndex(self, data):
        """
        Имена листов.
        """
        self.startElementLevel('gmr:SheetNameIndex')
        
        for worksheet in data:
            self.setSheetName(worksheet)
            
        self.endElementLevel('gmr:SheetNameIndex')
        
    def setSheetName(self, data):
        """
        Имя листа.
        """
        self.startElement('gmr:SheetName')
        self.characters(str(data['Name']))
        self.endElement('gmr:SheetName')
        
    def setSheets(self, data):
        """
        Данные листов.
        """
        self.startElementLevel('gmr:Sheets')
        
        for worksheet in data:
            self.setSheet(worksheet)
        
        self.endElementLevel('gmr:Sheets')

    def setSheet(self, data):
        """
        Лист.
        """
        name = data.get('Name', '')
        max_col = 0
        max_row = 0
        tables = [element for element in data['children'] if element['name'] == 'Table']
        table = []
        cols = []
        rows = []
        default_col_width = 48
        default_row_height = 12.8
        if tables:
            table = tables[0]
            max_col = table.get('ExpandedColumnCount', 0)
            max_row = table.get('ExpandedRowCount', 0)
            cols = [element for element in table['children'] if element['name'] == 'Column']
            rows = [element for element in table['children'] if element['name'] == 'Row']
            default_col_width = table.get('DefaultColumnWidth', 48)
            default_row_height = table.get('DefaultRowHeight', 12.8)
        
        self.startElementLevel('gmr:Sheet')
        
        self.setName(name)
        self.setMaxCol(max_col)
        self.setMaxRow(max_row)
        
        self.setCols(self, default_col_width)
        self.setRows(self, default_row_height)
        
        self.endElementLevel('gmr:Sheet')

    def setName(self, data):
        """
        Имя.
        """
        self.startElement('gmr:Name')
        self.characters(str(data))
        self.endElement('gmr:Name')
        
    def setMaxCol(self, data):
        """
        Максимальное количество колонок.
        """
        self.startElement('gmr:MaxCol')
        self.characters(str(data))
        self.endElement('gmr:MaxCol')
        
    def setMaxRow(self, data):
        """
        Максимальное количество строк.
        """
        self.startElement('gmr:MaxRow')
        self.characters(str(data))
        self.endElement('gmr:MaxRow')

    def setCols(self, data):
        """
        Колонки.
        """
        attrs = {'DefaultSizePts': str(data)}
        self.startElement('gmr:Cols', attrs, True)
        self.endElement('gmr:Cols', True)
        
    def setRows(self, data):
        """
        Строки.
        """
        attrs = {'DefaultSizePts': str(data)}
        self.startElement('gmr:Cols', attrs, True)
        self.endElement('gmr:Cols', True)


def test():
    """
    Тест.
    """
    from . import xml2dict
    data = xml2dict.XmlFile2Dict('./testfiles/SF02.xml')
    # Начать запись
    xml_file = Dict2GnumericFile(data['children'][0], './testfiles/test.gnumeric')

    
if __name__ == '__main__':
    test()
