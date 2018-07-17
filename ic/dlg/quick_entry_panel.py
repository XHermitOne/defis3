#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Классы и функции поддержки панели быстрого ввода.
Панель быстрого предназначена для ввода информации рекордсета.
Панель быстрого ввода привязывается и используется с контролами списка такими как
wx.ListCtrl, wx.DataListView и т.п.
Панель быстрого ввода оформляется в виде проекта wxFormBuilder.
Для вызова панели используется функции quick_entry_panel и quick_entry_dlg.
Ввод на панели быстрого ввода осуществляется при помощи клавиатуры 
без использования компьютерной мыши:
        F1 - Окно помощи
        ESC - Отмена ввода
        ENTER - Подтверждение ввода
        BACKSPACE - Возврат значений по умолчанию
        TAB - Переключение  между объектами ввода
        UP(^) - Переход на предыдущий элемент списка без сохранения данных 
        DOWN(v) - Переход на следующий элемент списка без сохранения данных
"""

import wx

import quick_entry_panel_ctrl_proto

from ic.engine import form_manager
from ic.log import log

__version__ = (0, 0, 1, 1)

GO_PREV_ITEM_CMD = -1
GO_NEXT_ITEM_CMD = 1
ENTRY_CANCEL_CMD = False
ENTRY_OK_CMD = True
ENTRY_ADD_CMD = '+'
ENTRY_DEL_CMD = '-'


class icQuickEntryPanelCtrl(quick_entry_panel_ctrl_proto.icQuickEntryPanelCtrlProto):
    """
    Панель управления панелью быстрого ввода.
    """
    def __init__(self, parent, quick_entry_panel_class, *args, **kwargs):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param quick_entry_panel_class: Класс панели быстрго ввода. 
        """
        quick_entry_panel_ctrl_proto.icQuickEntryPanelCtrlProto.__init__(self, parent)

        # Сама панель быстрого ввода
        if quick_entry_panel_class:
            # Создать панель быстрог ввода
            self.quick_entry_panel = quick_entry_panel_class(self, *args, **kwargs)
            # Разместить в сайзере
            panel_Sizer = self.GetSizer()
            panel_Sizer.Add(self.quick_entry_panel, 0, wx.EXPAND, 5)
            self.Layout()
        else:
            log.warning(u'Не определен класс панели быстрого ввода')

        # Признак подтверждения ввода
        self.entry_check = None

    def onCancelToolClicked(self, event):
        """
        Обработчик инструмента отмены ввода.
        """
        self.entry_check = ENTRY_CANCEL_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkToolClicked(self, event):
        """
        Обработчик инструмента подтверждения ввода.
        """
        self.entry_check = ENTRY_OK_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onAddToolClicked(self, event):
        """
        Обработчик инструмента добавление нового элемента.
        """
        self.entry_check = ENTRY_ADD_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Обработчик инструмента удаления существующего элемента.
        """
        self.entry_check = ENTRY_DEL_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onDefaultToolClicked(self, event):
        """
        Обработчик инструмента установки значений по умолчанию в контролах.
        ВНИМАНИЕ! В обработчике не вызываем event.Skip() чтобы окно не закрывалось
            по умолчанию.
        """
        self.GetParent().set_defaults()

    def onHelpToolClicked(self, event):
        """
        Обработчик инструмента помощи о горячих клавишах.
        ВНИМАНИЕ! В обработчике не вызываем event.Skip() чтобы окно не закрывалось
            по умолчанию.
        """
        help_txt = u'''Горячие клавиши:
        F1 - Окно помощи
        ESC - Отмена ввода
        ENTER - Подтверждение ввода
        BACKSPACE - Возврат значений по умолчанию
        TAB - Переключение  между объектами ввода
        
        CTRL+UP(^) - Переход на предыдущий элемент списка без сохранения данных 
        CTRL+DOWN(v) - Переход на следующий элемент списка без сохранения данных
         
        INS - Добавление нового элемента 
        DEL - Удаление существующего элемента 
        '''
        parent = self   # .GetParent().GetParent()
        wx.MessageBox(help_txt, u'ПОМОЩЬ', style=wx.OK | wx.ICON_QUESTION, parent=parent)

    def onPrevToolClicked(self, event):
        """
        Переход на предыдущий элемент без сохранения данных.
        """
        self.entry_check = GO_PREV_ITEM_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def onNextToolClicked(self, event):
        """
        Переход на следующий элемент без сохранения данных.
        """
        self.entry_check = GO_NEXT_ITEM_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def enableTools(self, prev_tool=True, next_tool=True, add_tool=True, del_tool=True,
                    ok_tool=True, cancel_tool=True, default_tool=True, help_tool=True,
                    *args, **kwargs):
        """
        Вкл./Выкл инструментов управления.
        Вместе с инструментами откл./вкл. комбинации клавиш.
        @param prev_tool: Вкл./выкл. инструмент перехода на предыдущий элемент.  
        @param next_tool: Вкл./выкл. инструмент перехода на следующий элемент.
        @param add_tool: Вкл./выкл. инструмент добавления нового элемента.
        @param del_tool: Вкл./выкл. инструмент удаления существующего элемента.
        @param ok_tool: Вкл./выкл. инструмент подтверждения ввода.
        @param cancel_tool: Вкл./выкл. инструмент отмены ввода.
        @param default_tool: Вкл./выкл. инструмент восстановления значений по умолчанию.
        @param help_tool: Вкл./выкл. инструмент помощи.
        @return: True/False. 
        """
        self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), prev_tool)
        self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), next_tool)
        self.ctrl_toolBar.EnableTool(self.add_tool.GetId(), add_tool)
        self.ctrl_toolBar.EnableTool(self.del_tool.GetId(), del_tool)
        self.ctrl_toolBar.EnableTool(self.ok_tool.GetId(), ok_tool)
        self.ctrl_toolBar.EnableTool(self.cancel_tool.GetId(), cancel_tool)
        self.ctrl_toolBar.EnableTool(self.default_tool.GetId(), default_tool)
        self.ctrl_toolBar.EnableTool(self.help_tool.GetId(), help_tool)

        hot_key_connections = dict()
        if prev_tool:
            hot_key_connections['CTRL_UP'] = self.prev_tool.GetId()
        if next_tool:
            hot_key_connections['CTRL_DOWN'] = self.next_tool.GetId()
        if add_tool:
            hot_key_connections['INS'] = self.add_tool.GetId()
        if del_tool:
            hot_key_connections['DEL'] = self.del_tool.GetId()
        if ok_tool:
            hot_key_connections['ENTER'] = self.ok_tool.GetId()
        if cancel_tool:
            hot_key_connections['ESC'] = self.cancel_tool.GetId()
        if default_tool:
            hot_key_connections['BACKSPACE'] = self.default_tool.GetId()
        if help_tool:
            hot_key_connections['F1'] = self.help_tool.GetId()
        self.GetParent().setAcceleratorTable_win(win=self, **hot_key_connections)


class icQuickEntryPanelDialog(wx.Dialog, form_manager.icFormManager):
    """
    Подложка панели быстрого ввода.
    Выполненно в виде диалогового окна, потому что диалоговое окно обеспечивает
        открытие в модальном режиме.
    """
    def __init__(self, parent, title, pos, size, quick_entry_panel_class, *args, **kwargs):
        """
        Конструктор.
        @param parent: Родительское окно.
        @param title: Заголовок окна.
        @param pos: Позиция отображения панели быстрого ввода.
        @param size: Размер отображения панели быстрого ввода.
        @param quick_entry_panel_class: Класс панели быстрго ввода. 
        """
        form_manager.icFormManager.__init__(self)

        wx.Dialog.__init__(self, parent, title=title,
                           pos=pos if pos else wx.DefaultPosition,
                           size=size if size else wx.DefaultSize,
                           style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)

        # На подложке создаем панель управления
        self.ctrl_panel = icQuickEntryPanelCtrl(self, quick_entry_panel_class, *args, **kwargs)
        if self.ctrl_panel.quick_entry_panel:
            accord = self.find_panel_accord(self.ctrl_panel.quick_entry_panel)
            # log.debug(u'Accord %s' % str(accord))
            self.set_accord(**accord)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        # Значения по умолчанию
        self.defaults = None

        # Загрузить сохраненные данные
        ext_data = self.load_ext_data(self.get_ext_data_name())
        if pos is None:
            new_pos = ext_data.get('pos', wx.DefaultPosition)
            self.SetPosition(new_pos)
        if size is None:
            new_size = ext_data.get('size', wx.DefaultSize)
            self.SetSize(new_size)

    def get_ext_data_name(self):
        """
        Имя файла дополнительных сохраняемых данных формы.
        """
        return self.ctrl_panel.quick_entry_panel.__class__.__name__

    def set_defaults(self, defaults=None):
        """
        Установить значения по умолчанию.
        @param defaults: Словарь значений по умолчанию.
            Если не определен, то берется ранее 
        @return: True/False.
        """
        if defaults is not None:
            self.defaults = defaults
        if self.defaults is not None:
            self.set_panel_data(self.ctrl_panel.quick_entry_panel, self.defaults)
        else:
            log.warning(u'Не определен словарь значений по умолчанию')

    def onClose(self, event):
        """
        Обработчик закрытия окна.
        """
        # Сохранить текущее состояние
        self.save_ext_data(self.get_ext_data_name(),
                           pos=tuple(self.GetPosition()),
                           size=tuple(self.GetSize()))
        event.Skip()


def quick_entry_ctrl(parent, title=u'', pos=None, size=None,
                     quick_entry_panel_class=None, defaults=None,
                     tool_disabled=None,
                     *args, **kwargs):
    """
    Вызов и отображение панели быстрого ввода.
    @param parent: Родительское окно.
    @param title: Заголовок окна.
    @param pos: Позиция отображения панели быстрого ввода.
        Если не определена, то берется сохраненная пользовательская позиция. 
    @param size: Размер отображения панели быстрого ввода.
        Если не определен, то берется сохраненный пользовательския размер. 
    @param quick_entry_panel_class: Класс панели быстрго ввода.
    @param defaults: Словарь значений по умолчанию.
    @param tool_disabled: Список отключенных инструментов управления.
        Если не определен, то все инструменты включены.
        Список определяется например как ('add', 'del').
        Т.е. отключены инструменты добавления и удаления.
    @return: Кортеж из двух элементов:
        1. True - данные ввода подтверждены. Требуется сохранение введенных данных.
           False - данные не подтверждены. Сохранения данных не требуется 
           None - ошибка выполненния.
           -1 - Сделан переход на предыдущий элемент без сохранения данных
           1 - Сделан переход на следующий элемент без сохранения данных
        2. Словарь заполненных значений
    """
    # Создаем подложку
    dlg = icQuickEntryPanelDialog(parent=parent, title=title, pos=pos, size=size,
                                  quick_entry_panel_class=quick_entry_panel_class,
                                  *args, **kwargs)
    # Отключить не нужные инструменты
    if tool_disabled:
        tool_disabled_arg = dict([(tool_name+'_tool', False) for tool_name in tool_disabled])
        dlg.ctrl_panel.enableTools(**tool_disabled_arg)
    else:
        dlg.ctrl_panel.enableTools()

    # Устанавливаем значения по умолчанию
    if defaults:
        dlg.set_defaults(defaults)
    dlg.ShowModal()
    return dlg.ctrl_panel.entry_check, dlg.get_panel_data(dlg.ctrl_panel.quick_entry_panel)


def quick_entry_edit_dlg(parent, title=u'', pos=None, size=None,
                         quick_entry_panel_class=None, defaults=None, *args, **kwargs):
    """
    Вызов и отображение диалога быстрого ввода в режиме редактирования.
    @param parent: Родительское окно.
    @param title: Заголовок окна.
    @param pos: Позиция отображения панели быстрого ввода.
        Если не определена, то берется сохраненная пользовательская позиция. 
    @param size: Размер отображения панели быстрого ввода.
        Если не определен, то берется сохраненный пользовательския размер. 
    @param quick_entry_panel_class: Класс панели быстрго ввода.
    @param defaults: Словарь значений по умолчанию. 
    @return: Словарь заполненных значений, либо значение -1 или 1 для
        перехода на элемент без сохранения, либо None если нажата <Отмена>.
    """
    entry_check, entry_data = quick_entry_ctrl(parent, title=title, pos=pos, size=size,
                                               quick_entry_panel_class=quick_entry_panel_class,
                                               defaults=defaults, tool_disabled=('add', 'del'),
                                               *args, **kwargs)
    if entry_check is ENTRY_OK_CMD:
        return entry_data
    elif entry_check in (GO_PREV_ITEM_CMD, GO_NEXT_ITEM_CMD):
        return entry_check
    # Инструменты добавления и удаления отключены, поэтому их здесь не обрабатываем
    return None


def test():
    """
    Функция тестирования
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    frame = wx.Frame(None)

    btn = wx.Button(frame, label=u'Тест')

    class testPanel(quick_entry_panel_ctrl_proto.testPanelProto):
        pass

    def onBtn(event):
        values = {'m_checkBox1': True, 'm_spinCtrl1': 3, 'm_textCtrl2': u'www'}
        result = quick_entry_edit_dlg(btn, u'Тестовое окно',
                                      quick_entry_panel_class=testPanel,
                                      defaults=values)
        log.debug(u'Результат: %s' % str(result))
        event.Skip()

    frame.Bind(wx.EVT_BUTTON, onBtn)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
