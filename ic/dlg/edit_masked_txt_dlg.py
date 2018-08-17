# !/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно редактирования форматированного/маскируемого текста.
"""

import wx
from . import edit_masked_txt_dlg_proto
from ic.log import log
from ic.dlg import ic_dlg


class icEditMaskedTextDlg(edit_masked_txt_dlg_proto.icEditMaskedTextDlgProto):
    """
    Диалоговое окно редактирования форматированного/маскируемого текста.
    """

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <ОК>.
        """
        value = self.masked_textCtrl.GetValue()
        # Контроль значения на правильное заполнение
        if self.masked_textCtrl.IsValid(value):
            self.edit_text = value
        else:
            msg = u'Не корректное введеное значение <%s>' % value
            log.warning(msg)
            ic_dlg.icWarningBox(u'ОШИБКА', msg)
            self.edit_text = None
        self.EndModal(wx.ID_OK)
        event.Skip()

    def init(self, title=u'', label=u'',
             default_txt=u'', mask=u'', reg_exp=r''):
        """
        Инициализация диалогового окна.
        @param title: Заголовок диалогового окна.
        @param label: Текст сообщения.
        @param default_txt: Строка заполняемая по умолчанию.
        @param mask: Маска.
        @param reg_exp: Регулярное выражение.
        """
        # Проверка входных параметров
        if default_txt is None:
            default_txt = u''

        self.edit_text = u''

        self.SetTitle(title)
        self.label_staticText.SetLabelText(label)
        log.debug(u'Установка значения по умолчанию <%s> для редактирования' % default_txt)
        self.masked_textCtrl.SetMaskParameters(mask=mask,
                                               validRegex=reg_exp)
        # ВНИМАНИЕ! Установка значения м.б. только после
        # установки парамеров маски.
        # SetValue производит дополнительный контроль значения
        self.masked_textCtrl.SetValue(default_txt)

    def getEditText(self):
        """
        Отредактированное значение.
        """
        return self.edit_text


def edit_masked_text_dlg(parent=None, title=u'', label=u'',
                         default_txt=u'', mask=u'', reg_exp=r'',
                         *args, **kwargs):
    """
    Функция вызова диалогового окна.
    @param parent: Родительское окно.
    @param title: Заголовок диалогового окна.
    @param label: Текст сообщения.
    @param default_txt: Строка заполняемая по умолчанию.
    @param mask: Маска.
    @param reg_exp: Регулярное выражение.
    @return: Отредатированное значение или None,
        если нажата кнопка <Отмена>.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    dlg = icEditMaskedTextDlg(parent=parent, *args, **kwargs)
    dlg.init(title=title, label=label,
             default_txt=default_txt, mask=mask, reg_exp=reg_exp)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getEditText()
    return None


def test():
    """
    Функция тестирования.
    """
    app = wx.PySimpleApp()

    dlg = icEditMaskedTextDlg(parent=None)
    dlg.init(default_txt=u'000', mask=u'####', reg_exp=r'\d{4}',
             title=u'Тестовое диалоговое окно', label=u'Ввод текста:')
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        print(dlg.getEditText())

if __name__ == '__main__':
    test()
