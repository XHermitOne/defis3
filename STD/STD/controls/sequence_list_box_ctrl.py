#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Контрол организации последовательности списка.
"""

from . import sequence_list_box
from ic.bitmap import ic_bmp
from ic.log import log

__version__ = (0, 0, 0, 2)


class icSequenceListBox(sequence_list_box.icSequenceListBoxProto):
    """
    Контрол организации последовательности списка.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        sequence_list_box.icSequenceListBoxProto.__init__(self, *args, **kwargs)

        # Данные последовательности
        # Запись может быть в формате либо словаря либо списка
        self.sequence_data = list()

        # Идентификатор колонки текста, отображающегося в контроле списка
        # Если запись-словарь, то это ключ, если список, то индекс
        self.label_column = None

        self.init()

    def setSequenceData(self, sequence_data):
        """
        Данные последовательности. Список записей.
        Запись может быть в формате либо словаря либо списка.
        """
        self.sequence_data = sequence_data

    def getSequenceData(self):
        return self.sequence_data

    def setLabelColumn(self, label_column):
        """
        Идентификатор колонки текста, отображающегося в контроле списка
        Если запись-словарь, то это ключ, если список, то индекс
        """
        self.label_column = label_column

    def init(self):
        """
        Инициализация.
        """
        self.init_images()

    def init_images(self):
        """
        Инициализация образов.
        """
        # <wx.Tool>
        bmp = ic_bmp.createLibraryBitmap('control-stop-090.png')
        tool_id = self.first_tool.GetId()
        # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
        # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
        # Для этого вызываем метод панели инструметнтов
        # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('control-090.png')
        tool_id = self.prev_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('control-270.png')
        tool_id = self.next_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('control-stop-270.png')
        tool_id = self.last_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('arrow-skip-090.png')
        tool_id = self.move_up_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = ic_bmp.createLibraryBitmap('arrow-skip-270.png')
        tool_id = self.move_down_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        self.ctrl_toolBar.Realize()

    def refreshSequence(self):
        """
        Обновить список последовательности.
        """
        self.sequence_listBox.Clear()
        if self.sequence_data:
            for rec in self.sequence_data:
                label = rec[self.label_column]
                self.sequence_listBox.Append(label)
        else:
            log.warning(u'Не опрелены данные последовательности')

    def refreshToolbar(self):
        """
        Обновить кнопки панели инструментов
        """
        # Определить какой элемент списка выбран
        select_idx = self.sequence_listBox.GetSelection()
        len_items = self.sequence_listBox.GetCount()
        if select_idx == -1 or len_items <= 1:
            # Ничего не выбрано
            self.ctrl_toolBar.EnableTool(self.last_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.move_down_tool.GetId(), False)

            self.ctrl_toolBar.EnableTool(self.first_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.move_up_tool.GetId(), False)
        elif select_idx == 0:
            # Выбрана первая строка
            self.ctrl_toolBar.EnableTool(self.first_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.move_up_tool.GetId(), False)

            self.ctrl_toolBar.EnableTool(self.last_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.move_down_tool.GetId(), True)
        elif select_idx == (len_items - 1):
            # Выбрана последняя строка
            self.ctrl_toolBar.EnableTool(self.first_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.move_up_tool.GetId(), True)

            self.ctrl_toolBar.EnableTool(self.last_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), False)
            self.ctrl_toolBar.EnableTool(self.move_down_tool.GetId(), False)
        else:
            self.ctrl_toolBar.EnableTool(self.last_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.move_down_tool.GetId(), True)

            self.ctrl_toolBar.EnableTool(self.first_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), True)
            self.ctrl_toolBar.EnableTool(self.move_up_tool.GetId(), True)

    def onSequenceSelectListBox(self, event):
        """
        Обработчик выбора элемента списка.
        """
        self.refreshToolbar()
        event.Skip()

    def onFirstToolClicked(self, event):
        """
        Обработчик инструмента перехода на первый элемент списка.
        """
        count = self.sequence_listBox.GetCount()
        if count:
            self.sequence_listBox.Select(0)
            self.refreshToolbar()

        event.Skip()

    def onLastToolClicked(self, event):
        """
        Обработчик инструмента перехода на последний элемент списка.
        """
        count = self.sequence_listBox.GetCount()
        if count:
            self.sequence_listBox.Select(count - 1)
            self.refreshToolbar()

        event.Skip()

    def onPrevToolClicked(self, event):
        """
        Обработчик инструмента перехода на предыдущий элемент списка.
        """
        selected_idx = self.sequence_listBox.GetSelection()
        if selected_idx > 0:
            self.sequence_listBox.Select(selected_idx - 1)
            self.refreshToolbar()

        event.Skip()

    def onNextToolClicked(self, event):
        """
        Обработчик инструмента перехода на следующий элемент списка.
        """
        selected_idx = self.sequence_listBox.GetSelection()
        count = self.sequence_listBox.GetCount()
        if (selected_idx >= 0) and selected_idx < (count - 1):
            self.sequence_listBox.Select(selected_idx + 1)
            self.refreshToolbar()

        event.Skip()

    def onMoveUpToolClicked(self, event):
        """
        Передвижение записи выше в последовательности.
        """
        selected_idx = self.sequence_listBox.GetSelection()
        if selected_idx > 0:
            selected_rec = self.sequence_data[selected_idx]
            rec = self.sequence_data[selected_idx - 1]
            self.sequence_data[selected_idx - 1] = selected_rec
            self.sequence_data[selected_idx] = rec
            self.refreshSequence()

            self.sequence_listBox.Select(selected_idx - 1)
            self.refreshToolbar()

        event.Skip()

    def onMoveDownToolClicked(self, event):
        """
        Передвижение записи ниже в последовательности.
        """
        selected_idx = self.sequence_listBox.GetSelection()
        count = self.sequence_listBox.GetCount()
        if (selected_idx >= 0) and selected_idx < (count - 1):
            selected_rec = self.sequence_data[selected_idx]
            rec = self.sequence_data[selected_idx + 1]
            self.sequence_data[selected_idx + 1] = selected_rec
            self.sequence_data[selected_idx] = rec
            self.refreshSequence()

            self.sequence_listBox.Select(selected_idx + 1)
            self.refreshToolbar()

        event.Skip()
