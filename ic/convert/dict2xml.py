﻿#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль конвертирования словарно-списковой структуры в xml файл.
"""

import sys
import time
from xml.sax import saxutils

__version__ = (0, 1, 1, 1)

# Удалять 'Cyr' из имен шрифтов для Linux систем
# т.к. в Linux все шрифты unicode
FONT_NAME_CYRILIC_DEL = not bool(sys.platform[:3].lower == 'win')


def dict2XmlssFile(data, xml_filename, encoding='utf-8'):
    """
    Функция конвертирования.
    """
    xml_file = None
    try:
        # Начать запись
        xml_file = open(xml_filename, 'wt')
        xml_writer = icDict2XmlssWriter(data, xml_file, encoding=encoding)
        xml_writer.startDocument()
        xml_writer.setBook()

        # Закончить запись
        xml_writer.endDocument()
        xml_file.close()

        return xml_filename
    except:
        if xml_file:
            xml_file.close()
        raise


class icDICT2XMLWriter(saxutils.XMLGenerator):
    """
    Конвертер из словаря в XML представление.
    """
    def __init__(self, data, out=None, encoding='utf-8'):
        """
        Конструктор.
        """
        self._data = data
        # self._encoding=encoding

        saxutils.XMLGenerator.__init__(self, out, encoding)
        # Отступ, определяющий вложение тегов
        self.break_line = ''

        self.time_start = 0

    def _my_write(self, text):
        if not isinstance(text, str):
            # ВНИМАНИЕ! Записываться в файл должен только unicode иначе падает
            # при сохранении русских букв
            text = str(text)
        
        try: 
            self._out.write(text)
        except AttributeError:
            self._write(text)

    def _startElement(self, name, attrs, auto_close=False):
        self._my_write('<' + name)
        for (name, value) in attrs.items():
            # ВНИМАНИЕ! Записываться в файл должен только unicode иначе падает
            # при сохранении русских букв
            if sys.platform[:3].lower() == 'win':
                # if isinstance(value, unicode):
                #    value = value.encode(self._encoding)
                txt = ' %s=%s' % (name, saxutils.quoteattr(value))
            else:
                txt = u' %s=%s' % (name, saxutils.quoteattr(value))
            if isinstance(txt, str):
                # txt = txt.encode(self._encoding)
                self._my_write(txt)

        if auto_close:
            self._my_write('/')
        self._my_write('>')

    def _endElement(self, name, auto_close=False):
        if not auto_close:
            self._my_write('</%s>' % name)

    def startElementLevel(self, name, attrs=dict(), auto_close=False):
        """
        Начало тега.
        @name: Имя тега.
        @attrs: Атрибуты тега (словарь).
        """
        # Дописать новый отступ
        self._my_write('\n'+self.break_line)

        for item in attrs.items():
            if not isinstance(item[1], str):
                attrs[item[0]] = str(item[1])   # self._encoding
        self._startElement(name, attrs, auto_close)
        self.break_line += '  '

    def endElementLevel(self, name, auto_close=False):
        """
        Конец тега.
        @name: Имя, закрываемого тега.
        """
        if self.break_line:
            self.break_line = self.break_line[:-2]

        # Дописать новый отступ
        self._my_write('\n'+self.break_line)

        self._endElement(name, auto_close)

    def startElement(self, name, attrs={}, auto_close=False):
        """
        Начало тега.
        @name: Имя тега.
        @attrs: Атрибуты тега (словарь).
        """
        # Дописать новый отступ
        self._my_write('\n'+self.break_line)

        for item in attrs.items():
            if not isinstance(item[1], str):
                attrs[item[0]] = str(item[1])   # self._encoding
        self._startElement(name, attrs, auto_close)

    def endElement(self, name, auto_close=False):
        """
        Конец тега.
        @name: Имя, закрываемого тега.
        """
        self._endElement(name, auto_close)


class icDict2XmlssWriter(icDICT2XMLWriter):
    """
    Конвертер из словаря в XMLSpreadSheet представление.
    """
    def __init__(self, data, out=None, encoding='utf-8'):
        """
        Конструктор.
        """
        icDICT2XMLWriter.__init__(self, data, out, encoding)

    def setBook(self, data=None):
        """
        Начало книги.
        """
        if data is None:
            data = self._data

        # Время начала создания файла
        self.time_start = time.time()

        self.startElementLevel('Workbook', {'xmlns': 'urn:schemas-microsoft-com:office:spreadsheet',
                                            'xmlns:x': 'urn:schemas-microsoft-com:office:excel',
                                            'xmlns:ss': 'urn:schemas-microsoft-com:office:spreadsheet'})

        # Стили
        styles = [element for element in data['children'] if element['name'] == 'Styles']
        if styles:
            self.setStyles(styles[0])

        # Листы
        worksheets = [element for element in data['children'] if element['name'] == 'Worksheet']
        for worksheet in worksheets:
            self.setSheet(worksheet)

        self.endElementLevel('Workbook')

    def setStyles(self, data=None):
        """
        Начало стилей.
        """
        self.startElementLevel('Styles', {})

        # Стили
        styles = [element for element in data['children'] if element['name'] == 'Style']
        for style in styles:
            self.setStyle(style)

        self.endElementLevel('Styles')

    def setStyle(self, data=None):
        """
        Начало стиля.
        """
        attr = {}
        if 'ID' in data:
            attr['ss:ID'] = str(data['ID'])

        self.startElementLevel('Style', attr)

        # Выравнивание
        align = [element for element in data['children'] if element['name'] == 'Alignment']
        if align:
            self.setAlignment(align[0])

        # Обрамление
        borders = [element for element in data['children'] if element['name'] == 'Borders']
        if borders:
            self.setBorders(borders[0])

        # Шрифт
        font = [element for element in data['children'] if element['name'] == 'Font']
        if font:
            self.setFont(font[0])

        # Заливка
        interior = [element for element in data['children'] if element['name'] == 'Interior']
        if interior:
            self.setInterior(interior[0])

        # Формат
        fmt = [element for element in data['children'] if element['name'] == 'NumberFormat']
        if fmt:
            self.setNumberFormat(fmt[0])

        self.endElementLevel('Style')

    def setAlignment(self, data=None):
        """
        Начало выравнивания.
        """
        attrs = {}
        if 'Horizontal' in data:
            attrs['ss:Horizontal'] = str(data['Horizontal'])
        if 'Vertical' in data:
            attrs['ss:Vertical'] = str(data['Vertical'])
        if 'Indent' in data:
            attrs['ss:Indent'] = str(data['Indent'])
        if 'ReadingOrder' in data:
            attrs['ss:ReadingOrder'] = str(data['ReadingOrder'])
        if 'Rotate' in data:
            attrs['ss:Rotate'] = str(data['Rotate'])
        if 'ShrinkToFit' in data:
            attrs['ss:ShrinkToFit'] = str(data['ShrinkToFit'])
        if 'VerticalText' in data:
            attrs['ss:VerticalText'] = str(data['VerticalText'])
        if 'WrapText' in data:
            attrs['ss:WrapText'] = str(data['WrapText'])

        self.startElement('Alignment', attrs, True)

        self.endElement('Alignment', True)

    def setBorders(self, data=None):
        """
        Начало обрамления.
        """
        self.startElementLevel('Borders', {})

        # Границы
        for border in data['children']:
            self.setBorder(border)

        self.endElementLevel('Borders')

    def setBorder(self, data=None):
        """
        Начало обрамления.
        """
        attr = {}
        if 'Position' in data:
            attr['ss:Position'] = str(data['Position'])
        if 'Color' in data:
            attr['ss:Color'] = str(data['Color'])
        if 'LineStyle' in data:
            attr['ss:LineStyle'] = str(data['LineStyle'])
        if 'Weight' in data:
            attr['ss:Weight'] = str(data['Weight'])

        self.startElement('Border', attr, True)

        self.endElement('Border', True)

    def setFont(self, data=None):
        """
        Начало шрифта.
        """
        attr = {}
        if 'Size' in data:
            attr['ss:Size'] = str(data['Size'])
        if 'Bold' in data:
            attr['ss:Bold'] = str(int(data['Bold']))
        if 'Italic' in data:
            attr['ss:Italic'] = str(int(data['Italic']))
        if 'Color' in data:
            attr['ss:Color'] = str(data['Color'])
        if 'FontName' in data:
            font_name = str(data['FontName'])
            if FONT_NAME_CYRILIC_DEL:
                font_name = font_name.replace(' Cyr', '')
            attr['ss:FontName'] = font_name
        if 'Outline' in data:
            if not isinstance(data['Outline'], str):
                attr['ss:Outline'] = str(int(bool(data['Outline'])))
            else:
                attr['ss:Outline'] = str(int(eval(data['Outline'])))
        if 'Shadow' in data:
            if not isinstance(data['Shadow'], str):
                attr['ss:Shadow'] = str(int(bool(data['Shadow'])))
            else:
                attr['ss:Shadow'] = str(int(eval(data['Shadow'])))
        if 'StrikeThrough' in data:
            attr['ss:StrikeThrough'] = str(int(bool(data['StrikeThrough'])))
        if 'Underline' in data:
            attr['ss:Underline'] = str(data['Underline'])
        if 'VerticalAlign' in data:
            attr['ss:VerticalAlign'] = str(data['VerticalAlign'])
        if 'CharSet' in data:
            attr['x:CharSet'] = str(data['CharSet'])

        self.startElement('Font', attr, True)

        self.endElement('Font', True)

    def setInterior(self, data=None):
        """
        Начало заливки.
        """
        attrs = {}
        if 'Color' in data:
            attrs['ss:Color'] = str(data['Color'])
        if 'PatternColor' in data:
            attrs['ss:PatternColor'] = str(data['PatternColor'])

        if 'Pattern' in data:
            attrs['ss:Pattern'] = str(data['Pattern'])
        else:
            if 'PatternColor' in data:
                attrs['ss:Pattern'] = 'Solid'

        self.startElement('Interior', attrs, True)

        self.endElement('Interior', True)

    def setNumberFormat(self, data=None):
        """
        Начало формата.
        """
        attrs = {}
        if 'Format' in data:
            attrs['ss:Format'] = data['Format']

        self.startElement('NumberFormat', attrs, True)

        self.endElement('NumberFormat', True)

    def setSheet(self, data=None):
        """
        Начало листа.
        """
        self.startElementLevel('Worksheet', {'ss:Name': data['Name']})

        # Именованные диапазоны ячеек
        names = [element for element in data['children'] if element['name'] == 'Names']
        if names:
            for cur_names in names:
                self.setNames(cur_names)

        # Таблица листа
        tables = [element for element in data['children'] if element['name'] == 'Table']

        if tables:
            for table in tables:
                self.setTable(table)

        # Параметры листа
        options = [element for element in data['children'] if element['name'] == 'WorksheetOptions']
        if options:
            for option in options:
                self.setWorksheetOptions(option)

        self.endElementLevel('Worksheet')

    def setNames(self, data=None):
        """
        Секция проименованных диапазонов ячеек.
        """
        self.startElementLevel('Names', {})

        # Именованные диапазоны ячеек
        named_range = [element for element in data['children'] if element['name'] == 'NamedRange']
        if named_range:
            for cur_named_range in named_range:
                self.setNamedRange(cur_named_range)

        self.endElementLevel('Names')

    def setNamedRange(self, data=None):
        """
        Именованные диапазоны ячеек.
        """
        attrs = {}
        if 'Name' in data:
            attrs['ss:Name'] = str(data['Name'])
        if 'RefersTo' in data:
            attrs['ss:RefersTo'] = str(data['RefersTo'])
        if 'Hidden' in data:
            attrs['ss:Hidden'] = str(data['Hidden'])

        self.startElementLevel('NamedRange', attrs, True)
        self.endElementLevel('NamedRange', True)

    def setTable(self, data=None):
        """
        Начало таблицы.
        """
        attrs = {}
        if 'DefaultColumnWidth' in data:
            attrs['ss:DefaultColumnWidth'] = str(data['DefaultColumnWidth'])
        if 'DefaultRowHeight' in data:
            attrs['ss:DefaultRowHeight'] = str(data['DefaultRowHeight'])
        if 'ExpandedColumnCount' in data:
            attrs['ss:ExpandedColumnCount'] = str(data['ExpandedColumnCount'])
        if 'ExpandedRowCount' in data:
            attrs['ss:ExpandedRowCount'] = str(data['ExpandedRowCount'])
            # attrs['ss:ExpandedRowCount']=self._maxRowIdx(data)+1
        if 'StyleID' in data:
            attrs['ss:StyleID'] = str(data['StyleID'])
        if 'FullColumns' in data:
            attrs['x:FullColumns'] = str(data['FullColumns'])
        if 'FullRows' in data:
            attrs['x:FullRows'] = str(data['FullRows'])

        self.startElementLevel('Table', attrs)

        # Колонки
        columns = [element for element in data['children'] if element['name'] == 'Column']
        prev_idx = 0
        for col in columns:
            # Убрать не нуужные индексы
            if 'Index' in col:
                cur_idx = int(col['Index'])
                if cur_idx <= (prev_idx+1):
                    del col['Index']
                prev_idx = cur_idx
            self.setColumn(col)

        # Строки
        rows = [element for element in data['children'] if element['name'] == 'Row']
        prev_idx = 0
        for row in rows:
            # Убрать не нуужные индексы
            if 'Index' in row:
                cur_idx = int(row['Index'])
                if cur_idx <= (prev_idx+1):
                    del row['Index']
                prev_idx = cur_idx
            self.setRow(row)

        self.endElementLevel('Table')

    def setColumn(self, data=None):
        """
        Начало колонки.
        """
        attrs = {}
        if 'Index' in data:
            attrs['ss:Index'] = str(data['Index'])
        if 'Width' in data:
            attrs['ss:Width'] = data['Width']
        if 'Caption' in data:
            attrs['c:Caption'] = str(data['Caption'])
        if 'AutoFitWidth' in data:
            attrs['ss:AutoFitWidth'] = str(data['AutoFitWidth'])
        if 'Hidden' in data:
            attrs['ss:Hidden'] = str(data['Hidden'])
        if 'Span' in data:
            attrs['ss:Span'] = str(data['Span'])
        if 'StyleID' in data:
            attrs['ss:StyleID'] = str(data['StyleID'])

        self.startElement('Column', attrs, True)

        self.endElement('Column', True)

    def setRow(self, data=None):
        """
        Начало строки.
        """
        attrs = {}
        if 'Index' in data:
            attrs['ss:Index'] = str(data['Index'])
        if 'Height' in data:
            attrs['ss:Height'] = data['Height']
        if 'Caption' in data:
            attrs['c:Caption'] = str(data['Caption'])
        if 'AutoFitHeight' in data:
            attrs['ss:AutoFitHeight'] = str(data['AutoFitHeight'])
        if 'Hidden' in data:
            attrs['ss:Hidden'] = str(data['Hidden'])
        if 'StyleID' in data:
            attrs['ss:StyleID'] = str(data['StyleID'])
        if 'AutoFitHeight' in data:
            attrs['ss:AutoFitHeight'] = str(data['AutoFitHeight'])

        self.startElementLevel('Row', attrs)

        # Ячейки
        cells = [element for element in data['children'] if element['name'] == 'Cell']
        prev_idx = 0
        for cell in cells:
            # Убрать не нужные индексы
            if 'Index' in cell:
                cur_idx = int(cell['Index'])
                if cur_idx <= (prev_idx+1):
                    del cell['Index']
                empty_data = self.isEmptyData(cell)
                # ВНИМАНИЕ!!! Проверка на пропуск пустых ячеек
                # т.к. они выкинуться то надо учитывать смещение
                # индекса последующих ячеек
                if bool(set(cell.keys()) & set(['StyleID', 'MergeAcross', 'MergeDown', 'Formula'])) or \
                        (not empty_data):
                    prev_idx = cur_idx
            self.setCell(cell)

        self.endElementLevel('Row')

    def setCell(self, data=None):
        """
        Начало ячейки.
        """
        attrs = {}
        if 'Index' in data:
            attrs['ss:Index'] = str(data['Index'])
        if 'StyleID' in data:
            attrs['ss:StyleID'] = str(data['StyleID'])
        if 'MergeAcross' in data:
            attrs['ss:MergeAcross'] = str(data['MergeAcross'])
        if 'MergeDown' in data:
            attrs['ss:MergeDown'] = str(data['MergeDown'])
        if 'Formula' in data:
            attrs['ss:Formula'] = str(data['Formula'])

        empty_data = self.isEmptyData(data)
        if bool(set(data.keys()) & set(['StyleID', 'MergeAcross', 'MergeDown', 'Formula'])) or \
                (not empty_data):

            self.startElementLevel('Cell', attrs, not bool(data['children']))

            if data['children']:
                # Данные ячейки
                if not empty_data:
                    cell_data = [element for element in data['children'] if element['name'] == 'Data']
                    self.setData(cell_data[0])
                # Именование ячейки
                named_cell = [element for element in data['children'] if element['name'] == 'NamedCell']
                if named_cell:
                    self.setNamedCell(named_cell[0])

            self.endElementLevel('Cell', not bool(data['children']))

    def isEmptyData(self,data):
        """
        Проверка на отсутствие значения в блоке данных ячейки.
        """
        if not data['children']:
            return True
        cell_data = [element for element in data['children'] if element['name'] == 'Data']
        if cell_data and 'value' in cell_data[0] and cell_data[0]['value']:
            return False
        else:
            return True

    def setData(self, data=None):
        """
        Начало данных ячейки.
        """
        value = data['value']

        attrs = {}
        if 'Type' in data:
            attrs['ss:Type'] = data['Type']
        if 'Name' in data:
            attrs['ss:Name'] = data['Name']
        if 'xmlns' in data:
            attrs['xmlns'] = data['xmlns']

        self.startElement('Data', attrs, not bool(value))

        if not isinstance(value, str):
            value = str(value)  # self._encoding)
        if value:
            value = saxutils.escape(value)
            self.characters(value)

        self.endElement('Data', not bool(value))

    def setNamedCell(self, data=None):
        """
        Именованная ячейка.
        """
        attrs = {}
        if 'Name' in data:
            attrs['ss:Name'] = data['Name']

        self.startElement('NamedCell', attrs, True)
        self.endElement('NamedCell', True)

    def setWorksheetOptions(self, data=None):
        """
        Начало данных опций листа.
        """
        attrs = {}
        if 'xmlns' in data:
            attrs['xmlns'] = data['xmlns']
        else:
            attrs['xmlns'] = 'urn:schemas-microsoft-com:office:excel'

        self.startElementLevel('WorksheetOptions', attrs)

        # PageSetup
        page_setup = [element for element in data['children'] if element['name'] == 'PageSetup']
        if page_setup:
            self.setPageSetup(page_setup[0])

        # FitToPage
        fit_to_page = [element for element in data['children'] if element['name'] == 'FitToPage']
        if fit_to_page:
            self.setFitToPage(fit_to_page[0])

        # Print
        print_tag = [element for element in data['children'] if element['name'] == 'Print']
        if print_tag:
            self.setPrint(print_tag[0])

        self.endElementLevel('WorksheetOptions')

    def setFitToPage(self, data=None):
        """
        Начало признака заполнения по страницам.
        """
        self.startElementLevel('FitToPage', {}, True)
        self.endElementLevel('FitToPage', True)

    def setPageSetup(self, data=None):
        """
        Начало параметров печати.
        """
        self.startElementLevel('PageSetup', {})

        # Ориентация
        layouts = [element for element in data['children'] if element['name'] == 'Layout']
        if layouts:
            self.setLayout(layouts[0])

        # Поля
        page_margins=[element for element in data['children'] if element['name'] == 'PageMargins']
        if page_margins:
            self.setPageMargins(page_margins[0])

        self.endElementLevel('PageSetup')

    def setLayout(self, data=None):
        """
        Начало ориентации.
        """
        attrs = {}
        if 'Orientation' in data:
            attrs['x:Orientation'] = data['Orientation']
        if 'CenterHorizontal' in data:
            attrs['x:CenterHorizontal'] = data['CenterHorizontal']
        if 'CenterVertical' in data:
            attrs['x:CenterVertical'] = data['CenterVertical']

        self.startElement('Layout', attrs, True)

        self.endElement('Layout', True)

    def setPageMargins(self, data=None):
        """
        Начало полей листа.
        """
        attrs = {}
        if 'Left' in data:
            attrs['x:Left'] = data['Left']
        if 'Right' in data:
            attrs['x:Right'] = data['Right']
        if 'Top' in data:
            attrs['x:Top'] = data['Top']
        if 'Bottom' in data:
            attrs['x:Bottom'] = data['Bottom']

        self.startElement('PageMargins', attrs, True)

        self.endElement('PageMargins', True)

    def setPrint(self, data=None):
        """
        Начало атрибутов печати.
        """
        self.startElementLevel('Print', {})

        # Валидность информации в шаблоне
        valid_info = [element for element in data['children'] if element['name'] == 'ValidPrinterInfo']
        if valid_info:
            self.setValidPrinterInfo(valid_info[0])

        # Заполнение по страницам
        fit_width = [element for element in data['children'] if element['name'] == 'FitWidth']
        if fit_width:
            self.setFitWidth(fit_width[0])
        fit_height = [element for element in data['children'] if element['name'] == 'FitHeight']
        if fit_height:
            self.setFitHeight(fit_height[0])

        # Напрвление заполнения листов
        left_to_right = [element for element in data['children'] if element['name'] == 'LeftToRight']
        if left_to_right:
            self.setLeftToRight(left_to_right[0])

        # Размер бумаги
        paper_size = [element for element in data['children'] if element['name'] == 'PaperSizeIndex']
        if paper_size:
            self.setPaperSizeIndex(paper_size[0])

        # Масштаб
        scale = [element for element in data['children'] if element['name'] == 'Scale']
        if scale:
            self.setScale(scale[0])

        # Плотность печати
        h_resolution = [element for element in data['children'] if element['name'] == 'HorizontalResolution']
        if h_resolution:
            self.setHorizResolution(h_resolution[0])
        v_resolution = [element for element in data['children'] if element['name'] == 'VerticalResolution']
        if v_resolution:
            self.setVertResolution(v_resolution[0])

        # Количество копий листа
        n_copies = [element for element in data['children'] if element['name'] == 'NumberofCopies']
        if n_copies:
            self.setNumberofCopies(n_copies[0])

        self.endElementLevel('Print')

    def setValidPrinterInfo(self, data=None):
        """
        Начало валидности информации в шаблоне.
        """
        self.startElement('ValidPrinterInfo', {}, True)
        self.endElement('ValidPrinterInfo', True)

    def setFitWidth(self, data=None):
        """
        Заполнение по страницам. Ширина.
        """
        self.startElement('FitWidth', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('FitWidth', not bool(data['value']))

    def setFitHeight(self, data=None):
        """
        Заполнение по страницам. Высота.
        """
        self.startElement('FitHeight', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('FitHeight', not bool(data['value']))

    def setLeftToRight(self, data=None):
        """
        Последовательность заполнения листов: Слева на право.
        """
        self.startElementLevel('LeftToRight', {}, True)
        self.endElementLevel('LeftToRight', True)

    def setPaperSizeIndex(self, data=None):
        """
        Начало размера бумаги.
        """
        self.startElement('PaperSizeIndex', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('PaperSizeIndex', not bool(data['value']))

    def setScale(self, data=None):
        """
        Начало масштаба.
        """
        self.startElement('Scale', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('Scale', not bool(data['value']))

    def setHorizResolution(self, data=None):
        """
        Начало. Плотность печати.
        """
        self.startElement('HorizontalResolution', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('HorizontalResolution', not bool(data['value']))

    def setVertResolution(self, data=None):
        """
        Начало. Плотность печати.
        """
        self.startElement('VerticalResolution', {}, not bool(data['value']))

        if data['value']:
            self.characters(data['value'])

        self.endElement('VerticalResolution', not bool(data['value']))

    def setNumberofCopies(self, data=None):
        """
        Количество копий листа.
        """
        self.startElement('NumberofCopies', {}, not bool(data['value']))

        if data['value']:
            self.characters(str(data['value']))

        self.endElement('NumberofCopies', not bool(data['value']))


def test():
    """
    Тест.
    """
    data = {'name': 'Workbook',
            'children': [
                {'name': 'Styles', 'children': []}
            ]}

    # Начать запись
    xml_file = None
    xml_file = open('./testfiles/test.xml', 'w')
    xml_writer = icDICT2XMLWriter(data, xml_file)
    xml_writer.startDocument()
    xml_writer.setBook()

    xml_writer.startElement('Tst', {'a': 'A'}, True)
    xml_writer.endElement('Tst', True)

    # Закончить запись
    xml_writer.endDocument()
    xml_file.close()


if __name__ == '__main__':
    test()
