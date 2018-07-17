#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Панель WMS конструктора загрузки седельного тягача.
"""

import sys
import wx
import wx.dataview

from ic.log import log
from ic.utils import ic_time
from ic.dlg import ic_dlg
from ic.engine import form_manager

from . import constructor_ctrl
from . import layout_scheme

# --- Блок для отладки ---
# if __name__ == '__main__':
#     import os
#     import os.path
#     import sys
#     file_path = os.path.dirname(__file__) if os.path.dirname(__file__) else os.getcwd()
#     sys.path.append(os.path.dirname(os.path.dirname(file_path)))

# from SCADA.usercomponents import speedmeter

from . import truck_constructor_panel_proto

__version__ = (0, 0, 1, 2)

# Надпись ящика по умолчанию
DEFAULT_BOX_LABEL = u'Составной паллет'


class icAddBoxDialog(truck_constructor_panel_proto.icAddBoxDialogProto):
    """
    Стандартное диалоговое окно добавления нового бокса для загрузки.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        truck_constructor_panel_proto.icAddBoxDialogProto.__init__(self, *args, **kwargs)

        # Установить по умолчанию 5-ти рядный паллет
        self.row_edit.setValue('05')

        # Результаты выбора в форме
        self.data = None

    def onCancelButtonClick(self, event):
        """
        Обработка кнопки <Отмена>.
        """
        self.data = None
        self.EndModal(wx.CANCEL)

    def onOkButtonClick(self, event):
        """
        Обработка кнопки <ОК>.
        """
        self.data = self.get_data()
        self.EndModal(wx.OK)

    def get_data(self):
        """
        Данные выбранные в диалоговой форме.
        @return: Словарь данных.
            Формат:
            {
                'nomenklature': {
                                    'label': Наименование номенклатуры,
                                    'value': Код номенклатуры,
                                },
                'row': {
                            'label': Наименование рядности паллета,
                            'value': Код рядности паллета,
                       },
                'made_date': {
                                    'label': Дата розлива,
                                    'value': Дата производства в формате datetime.date.
                             }

            }
        """
        nomenklature = self.nomenklature_choice.getValue()
        if nomenklature:
            # Если определили номенклатуру, то и определили данные
            result = dict()
            label = self.nomenklature_choice.getSprav().Find(nomenklature, 'name')
            result['nomenklature'] = dict(label=label, value=nomenklature)
            label = self.row_edit.getSprav().Find(self.row_edit.getValue(), 'name')
            result['row'] = dict(label=label, value=self.row_edit.getValue())
            result['made_date'] = dict(label=u'Дата розлива:', value=ic_time.wxdate2pydate(self.made_datePicker.GetValue()))
            return result
        else:
            log.warning(u'Не заполнена номенклатура продукции')
        return None

    def getData(self):
        return self.data


class icWMSTruckConstructorPanel(truck_constructor_panel_proto.icWMSTruckConstructorPanelProto,
                                 form_manager.icFormManager):
    """
    Панель WMS конструктора загрузки седельного тягача.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        truck_constructor_panel_proto.icWMSTruckConstructorPanelProto.__init__(self, *args, **kwargs)

        # Создание внутренних объектов конструктора
        self.truck_constructor = constructor_ctrl.icWMSSimpleTruckConstructorCtrl(self.constructor_panel)

        # Установить в конструктре яруса, то что необходимо и обновлять информацию
        # в конструкторе погрузки при выделении ящика
        self.truck_constructor.truck_load_constructor.refresh_selected_obj = self
        constructor_sizer = self.constructor_panel.GetSizer()
        constructor_sizer.Add(self.truck_constructor, 1, wx.GROW | wx.EXPAND, 5)

        # Установить ширины колонок
        self.n_column.SetWidth(25)
        self.nomenklature_column.SetWidth(350)
        self.row_column.SetWidth(50)
        self.madedate_column.SetWidth(100)
        self.weight_column.SetWidth(50)

        # Заполнить позициями
        self.refreshBoxList()

        self.Layout()

        # Количество осей
        self.axle_count = 1

        # Альтернативный обработчик кнопки добавления
        # нового ящика для погрузки
        self.on_add_button_click = None

        self.truck_constructor.truck_load_constructor.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvents)

    def init(self, axle_count=1, tier_count=1,
             box_layout_scheme=None):
        """
        Инициализация внутренних объектов конструктора по внешним параметрам.
        @param axle_count: Количество осей тягача.
        @param tier_count: Количество ярусов погрузки.
        @param box_layout_scheme: Схема погрузки ящиков/паллет.
        Схема задается по позициям.
        """
        if axle_count > 0:
            self.axle_count = axle_count
        if box_layout_scheme and tier_count > 0:
            # Сначала удалить все доски при инициализации
            self.truck_constructor.truck_load_constructor.deleteBoards()
            # А затем добавить
            self.truck_constructor.setTierCount(tier_count, box_layout_scheme)

    def setAxleCount(self, axle_count=2):
        """
        Установить количество осей.
        @param axle_count: Количество осей.
        """
        self.axle_count = axle_count
        
        self.meter_listCtrl.DeleteCols(numCols=self.meter_listCtrl.GetNumberCols())
        for i_axle in range(self.axle_count):
            self.meter_listCtrl.AppendCols()
            col_label = u'Ось %d' % (i_axle + 1)
            self.meter_listCtrl.SetColLabelValue(i_axle, col_label)
            self.meter_listCtrl.SetColSize(i_axle, 150)

    def onAddButtonClick(self, event):
        """
        Обработчик кнопки <Добавить> для добавления нового ящика для погрузки.
        """
        if self.on_add_button_click is None:
            # Стандартный обработчик
            self.addNewBox()
        else:
            # Альтернативный обработчик
            self.on_add_button_click(self)
        # После добавления нового бокса необходимо
        # обнвить список загруженных ящиков
        self.refreshBoxList()

        event.Skip()

    def addBoxes(self, boxes):
        """
        Добавление ящиков в конструктор.
        @param boxes: Список описания ящиков/паллет.
        """
        for box in boxes:
            self.addBox(box)

        # После добавления нового бокса необходимо
        # обновить список загруженных ящиков
        self.refreshBoxList()

    def delBoxes(self):
        """
        Удалить все ящики.
        @return: True/False.
        """
        return self.truck_constructor.truck_load_constructor.deleteShapes()

    def setBoxes(self, boxes):
        """
        Установить ящики в конструктор.
        @param boxes: Список описания ящиков/паллет.
        """
        # Сначала удалить все ящики
        self.delBoxes()

        # а затем добавить
        self.addBoxes(boxes)

    def getBoxListRecords(self):
        """
        Список описаний ящиков/паллет. 
        @return: 
        """
        records = list()
        board = self.truck_constructor.truck_load_constructor.getBoard()
        if board:
            tags = board.getShapeTags()
            for i, tag in enumerate(tags):
                if tag:
                    try:
                        n = str(i+1)
                        label = tag['nomenklature']['label'] if tag['nomenklature']['label'] is not None else DEFAULT_BOX_LABEL
                        row_value = tag['row']['value']
                        made_date = str(tag['made_date']['value'])
                        weight = str(tag['weight']['value'])
                        row = [n, label, row_value, made_date, weight]
                        records.append(row)
                    except:
                        log.fatal(u'Ошибка добавления строки. Индекс [%d]' % i)
                        # Добавить пустую строку
                        records.append([str(i+1), u'', u'', u'', u''])
                else:
                    log.warning(u'Нет прикрепленного тега у фигуры размещения. Индекс [%d]' % i)
                    # Если тег не прикреплен, то добавить пустую строку
                    records.append([str(i+1), u'', u'', u'', u''])
        return records

    def refreshBoxList(self):
        """
        Обновить список загруженных ящиков.
        """
        board = self.truck_constructor.truck_load_constructor.getBoard()
        if board:
            records = self.getBoxListRecords()

            # Запомнить выбранную строку
            selected_row = self.getItemSelectedIdx(self.box_ListCtrl)
            self.setRows_list_ctrl(self.box_ListCtrl, records)

            if selected_row != wx.NOT_FOUND:
                # Если строка была выбрана, то восстановить выбор
                self.box_ListCtrl.SelectRow(selected_row)
        else:
            log.warning(u'Не определен объект доски размещения в конструкторе погрузки')

    def addBox(self, box):
        """
        Добавить ящик для погрузки.
        @param box: Словарь описания ящика.
        ВНИМАНИЕ! Внутренняя информация о ящиках/паллетах в конструкторе храниться в
        формате:
            {
                'nomenklature': {
                                    'label': Наименование номенклатуры,
                                    'value': Код номенклатуры,
                                },
                'content': {
                               'label': Наименование содержания,
                               'value': Содержание ящика/паллета в случае составного паллета (список строк),
                           },
                'row': {
                            'label': Наименование рядности паллета,
                            'value': Код рядности паллета,
                       },
                'made_date': {
                                    'label': Дата розлива,
                                    'value': Дата производства в формате datetime.date.
                             }
                'weight': {
                            'value': Вес паллета,
                       },
                'pos': (x, y), # Позиция ящика
            }
        """
        # log.debug(u'Box: %s' % box)
        if box:
            box_pos = box.get('pos', None)
            is_pos = bool(box_pos)
            if not is_pos:
                # Если позиция ящика не определена, то просто добавляем в конец
                self.truck_constructor.truck_load_constructor.appendShape(tag=box)
            else:
                # Определена позиция ящика. Необходимо установить его в позицию
                self.truck_constructor.truck_load_constructor.appendShape(pos_x=box_pos[0],
                                                                          pos_y=box_pos[1],
                                                                          tag=box)
        else:
            log.warning(u'Не определена структуры ящика для добавления в конструктор')

    def addNewBox(self):
        """
        Добавить новый ящик для погрузки.
        """
        dlg = icAddBoxDialog(self)
        dlg.ShowModal()
        box = dlg.getData()
        self.addBox(box)

    def getBoxes(self):
        """
        Получить список ящиков.
        Формат:
        [
            {
                'nomenklature': {
                                    'label': Наименование номенклатуры,
                                    'value': Код номенклатуры,
                                },
                'content': {
                               'label': Наименование содержания,
                               'value': Содержание ящика/паллета в случае составного паллета,
                           },
                'row': {
                            'label': Наименование рядности паллета,
                            'value': Код рядности паллета,
                       },
                'made_date': {
                                    'label': Дата розлива,
                                    'value': Дата производства в формате datetime.date.
                             }
                'weight': {
                            'value': Вес паллета,
                       },
                'pos': (x, y), # Позиция ящика
            }, ...
        ]
        """
        board = self.truck_constructor.truck_load_constructor.getBoard()
        if board:
            boxes = board.getShapeTags()
        else:
            boxes = list()
        return boxes

    def onMouseEvents(self, event):
        """
        Любые действия мыши. Обработчик.
        Закончили перетаскивание фигуры.
        """
        # Надо обновит погрузочный список
        self.refreshBoxList()
        event.Skip()

    def refreshSelected(self, selected_point, **kwargs):
        """
        Обновить информацию о выбранном ящике.
        @param selected_point: Точка выбора.
        """
        if selected_point:
            selected_cell = self.truck_constructor.truck_load_constructor.find_cell(x=selected_point[0],
                                                                                    y=selected_point[1])
            if selected_cell:
                idx = selected_cell.getIndex()
                self.box_ListCtrl.SelectRow(idx)

                # Сначала скрываем предыдущее окно
                self.truck_constructor.truck_load_constructor.hideShapeTagInfo()

                # А затем открываем новое, если нажата правая кнопка мыши
                mouse_pressed = kwargs.get('mouse_pressed', wx.MOUSE_BTN_LEFT)
                if mouse_pressed == wx.MOUSE_BTN_RIGHT:
                    cell_shape = selected_cell.getShape()
                    self.truck_constructor.truck_load_constructor.showShapeTagInfo(cell_shape)
            else:
                idx = self.box_ListCtrl.GetSelectedRow()
                if idx >= 0:
                    self.box_ListCtrl.UnselectRow(idx)
                self.truck_constructor.truck_load_constructor.hideShapeTagInfo()

    def onBoxListCtrlSelectionChanged(self, event):
        """
        Обработчик выбора ящика/паллета в списке ящиков.
        """
        selected_idx = self.getItemSelectedIdx(self.box_ListCtrl)

        if selected_idx >= 0:
            selected_cell = self.truck_constructor.truck_load_constructor.getCellByIdx(selected_idx)
            if selected_cell:
                # Сначала скрываем предыдущее окно
                self.truck_constructor.truck_load_constructor.hideShapeTagInfo()
                # А затем открываем новое
                cell_shape = selected_cell.getShape()
                self.truck_constructor.truck_load_constructor.showShapeTagInfo(cell_shape)
        elif selected_idx == wx.NOT_FOUND:
            self.box_ListCtrl.UnselectAll()

        # Отключить кнопки если достигнут край списка
        data_list = self.getBoxListRecords()
        last_item_idx = len(data_list)-1
        self.enableTools_toolbar(self.box_toolBar,
                                 moveup_tool=selected_idx != wx.NOT_FOUND and selected_idx > 0,
                                 movedown_tool=selected_idx != wx.NOT_FOUND and selected_idx < last_item_idx)

        event.Skip()

    def onMoveUpToolClicked(self, event):
        """
        Обработчик инструмента перемещения ящика/паллета вверх в списке ящиков.
        """
        selected_idx = self.getItemSelectedIdx(self.box_ListCtrl)

        if selected_idx == wx.NOT_FOUND:
            log.warning(u'Не выбран ящик/паллет')
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Необходимо выбрать позицию для перемещения!')
            event.Skip()
            return

        data_list = self.getBoxListRecords()
        is_move = self.moveUpRow_list_ctrl(self.box_ListCtrl, data_list, idx=selected_idx, n_col=0)

        if is_move:
            src_cell = self.truck_constructor.truck_load_constructor.getCellByIdx(selected_idx)
            dst_cell = self.truck_constructor.truck_load_constructor.getCellByIdx(selected_idx-1)
            self.truck_constructor.truck_load_constructor.replaceCells(src_cell, dst_cell)
            self.refreshBoxList()

        # Отключить кнопки если достигнут край списка
        selected_idx = self.getItemSelectedIdx(self.box_ListCtrl)
        last_item_idx = len(data_list)-1
        self.enableTools_toolbar(self.box_toolBar,
                                 moveup_tool=selected_idx != wx.NOT_FOUND and selected_idx > 0,
                                 movedown_tool=selected_idx != wx.NOT_FOUND and selected_idx < last_item_idx)
        event.Skip()

    def onMoveDownToolClicked(self, event):
        """
        Обработчик инструмента перемещения ящика/паллета вниз в списке ящиков.
        """
        selected_idx = self.getItemSelectedIdx(self.box_ListCtrl)

        if selected_idx == wx.NOT_FOUND:
            log.warning(u'Не выбран ящик/паллет')
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', u'Необходимо выбрать позицию для перемещения!')
            event.Skip()
            return

        data_list = self.getBoxListRecords()
        is_move = self.moveDownRow_list_ctrl(self.box_ListCtrl, data_list, idx=selected_idx, n_col=0)

        if is_move:
            src_cell = self.truck_constructor.truck_load_constructor.getCellByIdx(selected_idx)
            dst_cell = self.truck_constructor.truck_load_constructor.getCellByIdx(selected_idx+1)
            self.truck_constructor.truck_load_constructor.replaceCells(src_cell, dst_cell)
            self.refreshBoxList()

        # Отключить кнопки если достигнут край списка
        selected_idx = self.getItemSelectedIdx(self.box_ListCtrl)
        last_item_idx = len(data_list)-1
        self.enableTools_toolbar(self.box_toolBar,
                                 moveup_tool=selected_idx != wx.NOT_FOUND and selected_idx > 0,
                                 movedown_tool=selected_idx != wx.NOT_FOUND and selected_idx < last_item_idx)
        event.Skip()


def test_defis():
    """
    Функция тестирования в среде DEFIS.
    """
    import ic
    parent = ic.getMainWin()
    panel = icWMSTruckConstructorPanel(parent)
    panel.init(box_layout_scheme=layout_scheme.DEFAULT_WINTER_1_AXLE_POS)
    parent.AddOrgPage(panel, u'Конструктор погрузки')


def test():
    """
    Функция тестирования.
    """
    from ic import config
    log.init(config)

    app = wx.PySimpleApp()
    # Внимание!
    # Это отключает ошибку
    # wx._core.PyAssertionError: C++ assertion "m_window" failed at ../src/gtk/dcclient.cpp(2043)
    # in DoGetSize(): GetSize() doesn't work without window
    app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)

    frame = wx.Frame(None, size=wx.Size(900, 500))

    panel = icWMSTruckConstructorPanel(frame)
    panel.init(box_layout_scheme=layout_scheme.DEFAULT_WINTER_1_AXLE_POS)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
