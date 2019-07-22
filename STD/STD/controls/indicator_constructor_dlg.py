#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Форма конструктора индикатора фильтра.

Модуль формы <icIndicatorConstructorDlgProto>.
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
"""

import os.path
import keyword
import wx
import wx.stc

from . import indicator_constructor_dlg_proto

import ic
from ic.log import log
from ic.bitmap import bmpfunc

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager

__version__ = (0, 1, 1, 1)

UNKNOWN_STATE_NAME_FMT = u'Состояние %d'


class icIndicatorConstructorDlg(indicator_constructor_dlg_proto.icIndicatorConstructorDlgProto,
                                form_manager.icFormManager):
    """
    Форма конструктора индикатора фильтра.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        indicator_constructor_dlg_proto.icIndicatorConstructorDlgProto.__init__(self, *args, **kwargs)

        # Редактироуемый индикатор
        self._indicator = list()

    def setIndicator(self, indicator=None, refresh_ctrl=False):
        """
        Установить индикатор для редактирования.
        @param indicator: Список редактируемого индикатора фильтра.
        @param refresh_ctrl: Произвести обновление контролов конструктора?
        """
        if indicator is None:
            self._indicator = list()
        else:
            self._indicator = indicator

        if refresh_ctrl:
            self.setIndicatorListCtrl()

    def getIndicator(self):
        """
        Редактироуемый индикатор.
        """
        return self._indicator

    def setIndicatorListCtrl(self, indicator=None):
        """
        Установить список состояний индикатора.
        @param indicator: Список редактируемого индикатора фильтра.
        @return: True/False
        """
        if indicator is None:
            indicator = self._indicator

        self.indicator_listCtrl.DeleteAllItems()
        for state_idx, state_indicator in enumerate(indicator):
            self.appendRow_list_ctrl(ctrl=self.indicator_listCtrl, row=('', ''))
            self.refreshStateRow(state_idx, state_indicator)
        return True

    def init(self):
        """
        Инициализация панели.
        """
        self.init_img()
        self.init_ctrl()
        
    def init_img(self):
        """
        Инициализация изображений.
        """
        pass
        
    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        self.init_toolbar()
        self.init_indicator_grid()
        self.init_expression_edit()

        self.image_filePicker.SetInitialDirectory(bmpfunc.getImageLibDir())
        self.image_filePicker.Enable(False)
        self.textcolor_colourPicker.Enable(False)
        self.bgcolor_colourPicker.Enable(False)

    def init_indicator_grid(self):
        """
        Инициализация грида индикатора.
        """
        self.setColumns_list_ctrl(ctrl=self.indicator_listCtrl,
                                  cols=(dict(label=u'Наименование', width=200),
                                        # dict(label=u'Образ', width=50),
                                        dict(label=u'Выражение', width=450)))

    def init_toolbar(self):
        """
        Инициализация панели инструментов.
        """
        self.ctrl_toolBar.EnableTool(self.moveup_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.movedown_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), False)

    def init_expression_edit(self):
        """
        Инициализация редактора выражения.
        """
        # Настройка обозревателя кода
        self.expression_edit.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.expression_edit.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.expression_edit.SetProperty('fold', '1')
        self.expression_edit.SetProperty('tab.timmy.whinge.level', '1')
        self.expression_edit.SetMargins(0, 0)

        # Не видеть пустые пробелы в виде точек
        self.expression_edit.SetViewWhiteSpace(False)

        # Установить ширину 'таба'
        # Indentation and tab stuff
        self.expression_edit.SetIndent(4)                 # Proscribed indent size for wx
        self.expression_edit.SetIndentationGuides(True)   # Show indent guides
        self.expression_edit.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.expression_edit.SetTabIndents(True)          # Tab key indents
        self.expression_edit.SetTabWidth(4)               # Proscribed tab size for wx
        self.expression_edit.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Установка поле для захвата маркеров папки
        self.expression_edit.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.expression_edit.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.expression_edit.SetMarginSensitive(1, True)
        self.expression_edit.SetMarginSensitive(2, True)
        self.expression_edit.SetMarginWidth(1, 25)
        self.expression_edit.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,    'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Маркеры режима отладки
        # self.expression_edit.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        # self.expression_edit.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')

    def setDefaultStateCtrlValue(self):
        """
        Установить значения по умолчанию для
            контролов редактора состояния индикатора.
        """
        self.setStateCtrlValue()

    def getStateCtrlValue(self):
        """
        Получить отредактированное состояние из контролов
        @return: Словарь отредактированного состояния индикатора.
        """
        name = self.name_textCtrl.GetValue()
        if not name.strip():
            name = UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1)

        img_filename = self.image_filePicker.GetPath() if self.image_checkBox.GetValue() else None
        if img_filename:
            img_filename = os.path.basename(img_filename) if img_filename.startswith(bmpfunc.getImageLibDir()) else img_filename

        text_color = self.textcolor_colourPicker.GetColour() if self.textcolor_checkBox.GetValue() else None

        bg_color = self.bgcolor_colourPicker.GetColour() if self.bgcolor_checkBox.GetValue() else None

        expression = self.expression_edit.GetValue()
        if not expression.strip():
            expression = None

        return dict(name=name, image=img_filename,
                    text_color=text_color, background_color=bg_color,
                    expression=expression)

    def setStateCtrlValue(self, state_indicator=None):
        """
        Установить значения в контролы состояния индикатора.
        @param state_indicator: Словарь состояния индикатора:
            {
                'name': Наименование состояния,
                'image': Файл образа,
                'text_color': Кортеж (R, G, B) цвета текста,
                'background_color': Кортеж (R, G, B) цвета фона,
                'expression': Текст блока кода выражения проверки состояния,
            }
        @return: True/False.
        """
        if state_indicator is None:
            state_indicator = dict()

        name = state_indicator.get('name',
                                   UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1))
        img_filename = state_indicator.get('image', None)
        text_color = state_indicator.get('text_color', None)
        bg_color = state_indicator.get('background_color', None)
        expression = state_indicator.get('expression', None)

        self.name_textCtrl.SetValue(name)
        self.image_checkBox.SetValue(img_filename is not None)
        if img_filename:
            self.image_filePicker.SetPath(img_filename)
        else:
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU, (16, 16))
            self.image_bitmap.SetBitmap(bmp)
        self.textcolor_checkBox.SetValue(text_color is not None)
        if text_color:
            self.textcolor_colourPicker.SetColour(text_color)
        self.bgcolor_checkBox.SetValue(bg_color is not None)
        if bg_color:
            self.bgcolor_colourPicker.SetColour(bg_color)
        if expression is None:
            self.expression_edit.ClearAll()
        else:
            self.expression_edit.SetValue(expression)

        return True

    def refreshStateRow(self, state_idx, state_indicator):
        """
        Обновить строку списка индикатора соответствующему состоянию.
        @param state_idx: Индекс в списке состояния.
        @param state_indicator: Словарь описания состояния индикатора.
            {
                'name': Наименование состояния,
                'image': Файл образа,
                'text_color': Кортеж (R, G, B) цвета текста,
                'background_color': Кортеж (R, G, B) цвета фона,
                'expression': Текст блока кода выражения проверки состояния,
            }
        @return: True/False
        """
        if state_idx < 0:
            log.warning(u'Не корректный индекс состояния')
            return False

        if state_indicator is None:
            state_indicator = dict(name=UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1),
                                   image=None, text_color=None, background_color=None,
                                   expression=None)

        self._indicator[state_idx] = state_indicator

        # Обновить контрол
        name = state_indicator.get('name', u'')
        image = None
        img_filename = state_indicator.get('image', None)
        if img_filename:
            if os.path.exists(img_filename):
                # Абсолютный путь до файла
                image = bmpfunc.createBitmap(img_filename)
            else:
                # Во всех других случаях считаем что это библиотечный файл
                image = bmpfunc.createLibraryBitmap(img_filename)
        line = u''
        expression = state_indicator.get('expression', None)
        if expression:
            lines = expression.splitlines()
            line = lines[0] + u' ...'

        text_color = state_indicator.get('text_color', None)
        bg_color = state_indicator.get('background_color', None)

        self.setRow_list_ctrl(ctrl=self.indicator_listCtrl, row_idx=state_idx,
                              row=(name, line))
        if image:
            # self.indicator_listCtrl.SetItemImage(state_idx, image)
            self.setItemImage_list_ctrl(ctrl=self.indicator_listCtrl, item=state_idx, image=image)

        if text_color:
            log.debug(u'Цвет текста %s' % str(text_color))
            self.indicator_listCtrl.SetItemTextColour(state_idx, text_color)
        else:
            self.indicator_listCtrl.SetItemTextColour(state_idx, wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        if bg_color:
            log.debug(u'Цвет фона %s' % str(bg_color))
            self.indicator_listCtrl.SetItemBackgroundColour(state_idx, bg_color)
        else:
            self.indicator_listCtrl.SetItemBackgroundColour(state_idx, wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        return True

    def onMoveUpToolClicked(self, event):
        """
        Передвижение состояния выше по списку.
        """
        event.Skip()

    def onMoveDownToolClicked(self, event):
        """
        Передвижение состояния ниже по списку.
        """
        event.Skip()

    def onAddToolClicked(self, event):
        """
        Обработчик кнопки добавления состояния индикатора.
        """
        try:
            self.setDefaultStateCtrlValue()
            state_indicator = self.getStateCtrlValue()
            new_name = state_indicator['name']
            # new_image = state_indicator.get('image', None)
            # new_exp = state_indicator.get('expression', None)

            # Добавить состояние индикатора в список
            self._indicator.append(state_indicator)

            # log.debug(u'Добавленное состояние %s' % str(state_indicator))
            # Добавляем строку в список
            self.appendRow_list_ctrl(ctrl=self.indicator_listCtrl, row=(new_name, None, None),
                                     auto_select=True)
            #
            self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), True)
        except:
            log.fatal(u'Ошибка добавления состояния индикатора')
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Обработчик кнопки удаления состояния индикатора.
        """
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        Обработчик кнопки сохранения состояния индикатора.
        """
        try:
            state_indicator = self.getStateCtrlValue()
            idx = self.getItemSelectedIdx(self.indicator_listCtrl)
            self.refreshStateRow(idx, state_indicator)
        except:
            log.fatal(u'Ошибка сохранения состояния индикатора')
        event.Skip()

    def onImageCheckBox(self, event):
        """
        Обработчик вкл/выкл картинки состояния индикатора.
        """
        checkbox_state = event.IsChecked()
        self.image_filePicker.Enable(checkbox_state)
        # if not checkbox_state:
        #     self.image_filePicker.SetPath(u'')
        event.Skip()

    def onTextColorCheckBox(self, event):
        """
        Обработчик вкл/выкл цвета текста состояния индикатора.
        """
        checkbox_state = event.IsChecked()
        self.textcolor_colourPicker.Enable(checkbox_state)
        event.Skip()

    def onBGColorCheckBox(self, event):
        """
        Обработчик вкл/выкл цвета фона состояния индикатора.
        """
        checkbox_state = event.IsChecked()
        self.bgcolor_colourPicker.Enable(checkbox_state)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки ОТМЕНА.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки ОК.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onImageFileChanged(self, event):
        """
        Обработчик смены файла образа.
        """
        img_filename = event.GetPath()
        if img_filename and os.path.exists(img_filename):
            bmp = bmpfunc.createBitmap(img_filename)
            self.image_bitmap.SetBitmap(bmp)
        event.Skip()

    def onIndicatorListItemSelected(self, event):
        """
        Обработчик выбора состояния индикатора из списка.
        """
        idx = event.GetIndex()
        state_indicator = self._indicator[idx]
        log.debug(u'Редактирование индикатора %s' % str(state_indicator))
        self.setStateCtrlValue(state_indicator=state_indicator)

        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), True)

        event.Skip()


def show_indicator_constructor_dlg(parent=None):
    """
    @param parent: Родительское окно.
    @return: True/False.
    """
    try:
        if parent is None:
            parent = ic.getMainWin()

        dlg = icIndicatorConstructorDlg(parent)
        dlg.init()
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            return True
    except:
        log.fatal(u'Ошибка')
    return False


def edit_indicator_constructor_dlg(parent=None, indicator=None):
    """
    Запустить редактирование индикатора фильтра.
    @param parent: Родительское окно.
    @param indicator: Список описания индикатора.
    @return: Отредактированный список индикатора или None если нажата ОТМЕНА.
    """
    try:
        if parent is None:
            parent = ic.getMainWin()

        dlg = icIndicatorConstructorDlg(parent)
        dlg.init()
        dlg.setIndicator(indicator=indicator, refresh_ctrl=True)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            indicator = dlg.getIndicator()
            dlg.Destroy()
            log.debug(u'Список отредактированного индикатора фильтра %s' % str(indicator))
            return indicator
    except:
        log.fatal(u'Ошибка редактирования индикатора фильтра')
    return None
