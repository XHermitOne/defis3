#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Самый простой грид. 
Его необходимо использовать, если необходимо посмотреть или отредактировать
простую таблицу. Он может также отображать картинки.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других 
    компонентов в данный комопнент. 
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой 
    компонент (ic_can_contain = -1).
"""

import wx
import wx.grid as parentModule

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
import wx.lib.mixins.gridlabelrenderer as glr
from ic.utils import strfunc

from ic.dlg import dlgfunc

# --- Спецификация ---
GRID_SELECTION_MODES = {'cells': parentModule.Grid.wxGridSelectCells,
                        'rows': parentModule.Grid.wxGridSelectRows,
                        'columns': parentModule.Grid.wxGridSelectColumns,
                        }
    
SPC_IC_SIMPLEGRID = {'col_count': 2,    # Количество колонок
                     'row_count': 2,    # Количество строк
                     'col_labels': ['A'],   # Надписи колонок
                     'row_labels': ['1'],   # Надписи строк
                     'wcols': [],   # Размеры колонок
                     'hrows': [],   # Размеры строк
                     'row_label_width': -1,     # Ширина надписей строк
                     'col_label_height': -1,    # Высота надписей колонок
                     'default_row_height': -1,  # Размер по умолчанию строк
                     'default_col_width': -1,   # Размер по умолчанию колонок
                     'selection_mode': 'cells',     # Режим выделения объектов грида
                     'readonly': False,     # Не редакттируемые ячейки грида?
    
                     '__parent__': icwidget.SPC_IC_WIDGET,
                     '__attr_hlp__': {'col_count': u'Количество колонок',
                                      'row_count': u'Количество строк',
                                      'col_labels': u'Надписи колонок',
                                      'row_labels': u'Надписи строк',
                                      'wcols': u'Размеры колонок',
                                      'hrows': u'Размеры строк',
                                      'row_label_width': u'Ширина надписей строк',
                                      'col_label_height': u'Высота надписей колонок',
                                      'default_row_height': u'Размер по умолчанию строк',
                                      'default_col_width': u'Размер по умолчанию колонок',
                                      'selection_mode': u'Режим выделения объектов грида',
                                      'readonly': u'Не редакттируемые ячейки грида?',
                                      },
                     }

# --- Описание компонента для редактора ресурса ---

#   Тип компонента
ic_class_type = icDefInf._icComboType

#   Имя класса
ic_class_name = 'icSimpleGrid'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SimpleGrid',
                'name': 'default',
                'child': [],
                '_uuid': None,
                
                'cellChange': None,
                'cellSelect': None,
                'cellDClick': None,
                'labelClick': None,

                'col_count': 2,    # Количество колонок
                'row_count': 2,    # Количество строк
                'col_labels': ['A'],   # Надписи колонок
                'row_labels': ['1'],   # Надписи строк
                'wcols': [],   # Размеры колонок
                'hrows': [],   # Размеры строк
                'row_label_width': -1,     # Ширина надписей строк
                'col_label_height': -1,    # Высота надписей колонок
                'default_row_height': -1,  # Размер по умолчанию строк
                'default_col_width': -1,   # Размер по умолчанию колонок
                'selection_mode': 'cells',     # Режим выделения объектов грида
                'readonly': False,     # Не редакттируемые ячейки грида?

                '__styles__': ic_class_styles,
                '__lists__': {'selection_mode': list(GRID_SELECTION_MODES.keys()),
                              },
                            
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_NUMBER: ['col_count', 'row_count',
                                                         'row_label_width', 'col_label_height',
                                                         'default_row_height', 'default_col_width'],
                                   icDefInf.EDT_TEXTLIST: ['col_labels',
                                                           'row_labels', 'wcols', 'hrows'],
                                   icDefInf.EDT_CHOICE: ['selection_mode'],
                                   icDefInf.EDT_CHECK_BOX: ['readonly'],
                                   },
                    
                '__events__': {'cellChange': ('wx.EVT_GRID_CELL_CHANGE', 'onCellChange', False),
                               'cellSelect': ('wx.EVT_GRID_SELECT_CELL', 'onCellSelect', False),
                               'cellDClick': ('wx.grid.EVT_GRID_CELL_LEFT_DCLICK', 'onDblClick', False),
                               'labelClick': ('wx.grid.EVT_GRID_LABEL_LEFT_CLICK', 'onLabelClick', False),
                               },
                '__parent__': SPC_IC_SIMPLEGRID,
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtGrid'
ic_class_pic2 = '@common.imgEdtGrid'

#   Путь до файла документации
ic_class_doc = 'public/icsimplegrid.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 3)


# --- Классы ---
class icSimpleImageRenderer(parentModule.PyGridCellRenderer):
    """
    Рендерер для отображений образов.
    """

    def __init__(self, *Images_):
        """
        Конструктор.
        """
        parentModule.PyGridCellRenderer.__init__(self)
        self._images = Images_

    def Draw(self, grid, attr, dc, rect, row, col, bSelected):
        """
        Отрисовка.
        """
        img = self._images[0]
        img_dc = wx.MemoryDC()
        img_dc.SelectObject(img)

        # Очистка фона
        dc.SetBackgroundMode(wx.SOLID)

        if bSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangle(rect)

        # copy the image but only to the size of the grid cell
        width, height = img.GetWidth(), img.GetHeight()

        if width > rect.width-2:
            width = rect.width - 2

        if height > rect.height-2:
            height = rect.height - 2

        dc.Blit(rect.x + 1, rect.y + 1, width, height,
                img_dc, 0, 0, wx.COPY, True)


class icSimpleGrid(icwidget.icWidget,
                   parentModule.Grid,
                   glr.GridWithLabelRenderersMixin):
    """
    Описание пользовательского компонента.
    :type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{child=[]}:
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.
        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.Grid.__init__(self, parent, id=wx.NewId(),
                                   pos=self.position, size=self.size, style=self.style)
        self.CreateGrid(self.row_count, self.col_count)
        glr.GridWithLabelRenderersMixin.__init__(self)
        
        # Установить атрибуты колонок и строк
        if self.col_labels:
            self.setColLabels(self.col_labels)
        if self.row_labels:
            self.setRowLabels(self.row_labels)
        if self.wcols:
            self.setWidthCols(self.wcols)
        if self.hrows:
            self.setHeightRows(self.hrows)
        if self.row_label_width >= 0:
            self.SetRowLabelSize(self.row_label_width)
        if self.col_label_height >= 0:
            self.SetColLabelSize(self.col_label_height)
        if self.default_row_height >= 0:
            self.SetDefaultRowSize(self.default_row_height)
        if self.default_col_width >= 0:
            self.SetDefaultColSize(self.default_col_width)
        self.SetSelectionMode(self.getSelectionModeAttr())
        if self.readonly:
            self.EnableEditing(not self.readonly)
        
        #   Регистрация обработчиков событий
        self.Bind(parentModule.EVT_GRID_CELL_CHANGED, self.onCellChange)
        self.Bind(parentModule.EVT_GRID_SELECT_CELL, self.onCellSelect)
        self.Bind(parentModule.EVT_GRID_CELL_LEFT_DCLICK, self.onDblClick)
        self.Bind(parentModule.EVT_GRID_LABEL_LEFT_CLICK, self.onLabelClick)
        
        self.BindICEvt()
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
            
        # Таблица данных, ассоциируемых с гридом
        self._recordset = []
        
    def get_recordset(self):
        """
        Таблица данных, ассоциируемых с гридом.
        """
        return self._recordset
    
    def get_record(self, rec_idx):
        """
        Получить запись рекордсета.
        """
        return self._recordset[rec_idx]
    
    def get_selected_record(self):
        """
        Получить запись, соответствующую выбранной строке.
        """
        rec_idx = self.GetGridCursorRow()
        return self.get_record(rec_idx)
    
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
    
    #   Обработчики событий
    def setCellImg(self, row, col, img):
        """
        Установить образ в ячейку.
        :param row: Строка ячейки.
        :param col: Колонка ячейки.
        :param img: Объект образа.
        """
        img_renderer = icSimpleImageRenderer(img)
        self.SetCellRenderer(row, col, img_renderer)

    def delCellImg(self, row, col):
        """
        Удалить образ из ячейки.
        :param row: Строка ячейки.
        :param col: Колонка ячейки.
        """
        self.SetCellRenderer(row, col, None)

    def getTable(self):
        """
        Представить данные в гриде в виде таблицы.
        :return: Список кортежей строк или None в случае ошибки.
        """
        table = []
        # Заполнить данными
        for i_row in range(self.GetNumberRows()):
            rec = []
            for i_col in range(self.GetNumberCols()):
                cell = self.GetCellValue(i_row, i_col)
                rec.append(cell)
            table.append(tuple(rec))
        return table
        
    def reCreateGrid(self, row_count, col_count):
        """
        Пересоздать грид.
        :param row_count: Количество строк.
        :param col_count: Количество колонок.
        """
        # Сначала очистить грид
        self.ClearGrid()
        d_row = row_count - self.GetNumberRows()
        d_col = col_count - self.GetNumberCols()
        
        if d_row > 0:
            # Добавление строк
            self.AppendRows(d_row)
        elif d_row < 0:
            # Удаление строк
            self.DeleteRows(numRows=abs(d_row))
                
        if d_col > 0:
            # Добавление колонок
            self.AppendCols(d_col)
        elif d_col < 0:
            # Удаление колонок
            self.DeleteCols(numCols=abs(d_col))
            
    def setTable(self, table, row_labels=None, col_labels=None):
        """
        Установить таблицу в грид.
        :param table: Таблица, представляется в виде списка кортежей.
            По строкам.
        :param row_labels: Список надписей строк.
        :param col_labels: Список надписей колонок.
        """
        self._recordset = table
        
        # Если таблица пустая, то просто очистить грид
        if not self._recordset:
            self._recordset = []
            self.ClearGrid()
            return
        
        row_count = len(table)
        if col_labels:
            col_count = len(col_labels)
        else:
            try:
                col_count = len(self.col_labels)
            except:
                col_count = 0
                
        # Создать грид
        self.reCreateGrid(row_count, col_count)
        # Надписи
        # По строкам
        if row_labels:
            self.setRowLabels(row_labels[:row_count])
        else:
            self.setRowLabels(self.row_labels)
        # По колонкам
        if col_labels:
            self.setColLabels(col_labels[:col_count])
        else:
            self.setColLabels(self.col_labels)
        
        # Заполнить данными
        for i_row, row in enumerate(table):
            for i_col, cell in enumerate(row):
                if i_col < self.GetNumberCols():
                    cell_txt = strfunc.toUnicode(cell)
                    self.SetCellValue(i_row, i_col, cell_txt)
    
    def setRowLabels(self, row_labels):
        """
        Установить надписи строк грида.
        :param row_labels: Список надписей строк.
        """
        row_count = self.GetNumberRows()
        for i, row_label in enumerate(row_labels):
            if row_label and i < row_count:
                self.SetRowLabelValue(i, row_label)
            else:
                break
        
    def setColLabels(self, col_labels):
        """
        Установить надписи колонок грида.
        :param col_labels: Список надписей колонок.
        """
        col_count = self.GetNumberCols()
        for i, col_label in enumerate(col_labels):
            if col_label and i < col_count:
                self.SetColLabelValue(i, col_label)
            else:
                break

    def setWidthCols(self, width_cols):
        """
        Установить размеры/ширину колонок грида.
        :param width_cols: Список размеров колонок. Список целых чисел.
        """
        col_count = self.GetNumberCols()
        for i, wcol in enumerate(width_cols):
            if i < col_count:
                self.SetColSize(i, int(wcol))
            else:
                break

    def setHeightRows(self, height_rows):
        """
        Установить размеры/высоту строк грида.
        :param height_rows: Список размеров строк. Список целых чисел.
        """
        row_count = self.GetNumberRows()
        for i, hrow in enumerate(height_rows):
            if i < row_count:
                self.SetRowSize(i, hrow)
            else:
                break
    
    def setRow(self, row, *args):
        """
        Установить значения в строку.
        :param row: Индекс строки.
        """
        row_count = self.GetNumberRows()
        if row < row_count:
            col_count = self.GetNumberCols()
            for i, value in enumerate(args):
                if i < col_count:
                    self.SetCellValue(row, i, str(value))
                else:
                    break
        
    def appendRow(self, *args):
        """
        Добавить в конц одну строку.
        """
        result = self.AppendRows(1)
        if args:
            self.setRow(self.GetNumberRows()-1, *args)
        return result
    
    def deleteRow(self, row=-1, bAutoSure=True):
        """
        Удалить строку.
        :param row: Индекс строки.
        :param bAutoSure: Автоматическое подтверждение удаления.
        """
        if bAutoSure:
            if row >= 0:
                return self.DeleteRows(row, 1)
        else:
            if dlgfunc.getAskDlg(u'УДАЛЕНИЕ:',
                               u'Удалить строку %d?' % row) == wx.YES:
                if row >= 0:
                    return self.DeleteRows(row, 1)
        return False
        
    def deleteCurRow(self, bAutoSure=True):
        """
        Удалить текущую строку.
        :param bAutoSure: Автоматическое подтверждение удаления.
        """
        cur_row = self.GetGridCursorRow()
        return self.deleteRow(cur_row, bAutoSure)

    def getSelectionModeAttr(self):
        """
        Режим выбора элемента грида.
        """
        attr_value = self.getICAttr('selection_mode')
        return GRID_SELECTION_MODES.setdefault(attr_value,
                                               parentModule.Grid.wxGridSelectCells)
        
    # --- Обработчики событий ---
    def onDblClick(self, event):
        """
        Двойное нажатие на ячейке.
        """
        self.eval_event('cellDClick', event, True)

    def onLabelClick(self, event):
        """
        Нажатие на заголовок ячейки.
        """
        self.eval_event('labelClick', event, True)
    
    def onCellChange(self, event):
        """
        Значение ячейки изменилось.
        """
        self.eval_event('cellChange', event, True)

    def onCellSelect(self, event):
        """
        Выделение ячейки.
        """
        self.eval_event('cellSelect', event, True)


def test(par=0):
    """
    Тестируем пользовательский класс.
    :type par: C{int}
    :param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    app = ictestapp.TestApp(par)
    common.init_img()
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
