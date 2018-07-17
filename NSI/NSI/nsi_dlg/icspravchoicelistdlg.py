#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора элемента справочника по уровням в виде списка.
"""

import sys
import os
import os.path
import wx
from . import nsi_dialogs_proto

import ic
from ic.kernel import io_prnt
from ic.utils import ic_util

#   Version
__version__ = (0, 0, 0, 1)


class icSpravChoiceListDialog(nsi_dialogs_proto.icSpravChoiceListDlgProto):
    """
    Диалоговое окно выбора элемента справочника по уровням в виде списка.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        nsi_dialogs_proto.icSpravChoiceListDlgProto.__init__(self, *args, **kwargs)

        # Справочник
        self._sprav = None
        # Выбранный код справочника
        self._selected_code = None

        # Текущий код уровня
        self._cur_code = (None, )

        # Последняя искомая строка
        self._last_search_value = None
        # Последний найденный результат
        self._last_search_result = None
        self._last_search_idx = 0

        # Создать колонки контрола списка
        self.sprav_list_ctrl.InsertColumn(0, u'Код')
        self.sprav_list_ctrl.InsertColumn(1, u'Наименование')
        self.sprav_list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.sprav_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def _getStrCode(self, code=None):
        """
        Преобразовать структурный код справочника в строковый вид.
        @param code: Код справочника в виде кортежа.
        @return: Строка-код справочника или None если код пустой.
        """
        if code is None:
            code = self._cur_code
        return u'' if code and code[0] is None else ''.join(code)

    def isEmptyCode(self, code=None):
        """
        Проверка на пустой код.
        @param code: Код справочника в виде кортежа.
        @return: True/False.
        """
        if code is None:
            code = self._cur_code
        result = False
        if not code:
            result = True
        elif code and code[0] is None:
            result = True
        return result

    def setNextCurCode(self, code):
        """
        Установить следующий уровень кода справочника.
        @param code: Код справочника.
        @return: Текуший код уровня.
        """
        code_list = [subcode for subcode in self._sprav.StrCode2ListCode(code) if subcode]
        self._cur_code = tuple(code_list)

        code_path = self.getSpravPath(self._cur_code)
        self.path_statictext.SetLabel(code_path)

        return self._cur_code

    def setPrevCurCode(self):
        """
        Установить предыдущий уровень кода справочника.
        @return: Предыдущий код уровня.
        """
        if len(self._cur_code) > 1:
            self._cur_code = self._cur_code[:-1]
        else:
            if self._cur_code[0]:
                self._cur_code = (None, )

        code_path = self.getSpravPath(self._cur_code)
        self.path_statictext.SetLabel(code_path)
        return self._cur_code

    def getSpravPath(self, code):
        """
        Путь справочника по структурному коду.
        @param code: Код справочника в виде кортежа.
        @return:
        """
        names = []
        for i, cod in enumerate(code):
            if cod:
                name = self._sprav.Find(u''.join(code[:i+1]))
                if name:
                    names.append(name)
        return u' -> '.join(names)

    def setSprav(self, sprav):
        """
        Установить активный справочник.
        @param sprav: Объект справочника.
        """
        self._sprav = sprav

        if self._sprav is not None:
            description = self._sprav.description if self._sprav.description else self._sprav.name
            self.SetLabel(u'Справочник: '+description)
            code = self._getStrCode()
            dataset = self._sprav.getStorage().getLevelTable(code)
            self.setDataset(dataset)
        else:
            io_prnt.outWarning(u'Не определен справочник для выбора')

    def setDataset(self, dataset):
        """
        Установить данные справочника.
        """
        if dataset:
            # Удаляем все элемены справочника только
            # если у нас есть что отобразить
            self.sprav_list_ctrl.DeleteAllItems()

            for record in dataset:
                code = record[0]
                name = record[1]

                index = self.sprav_list_ctrl.InsertStringItem(sys.maxint, code)
                self.sprav_list_ctrl.SetStringItem(index, 1, name)
            self.sprav_list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.sprav_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

            # Вкл./Выкл. кнопки перехода на родительский уровень
            self.dlg_toolbar.EnableTool(self.return_tool.GetId(),
                                        not self.isEmptyCode())
        else:
            io_prnt.outWarning(u'Не определен датасет справочника (код <%s>) для выбора' % self._getStrCode())

    def selectCode(self, code):
        """
        Выбрать код и отобразить его в списке.
        """
        code_list = self._sprav.StrCode2ListCode(code)
        if code_list:
            code_list = [sub_code for sub_code in code_list if sub_code]
            self._cur_code = code_list[:-1]
        else:
            self._cur_code = (None, )
        self.setSelectedCode(code)

        parent_code = self._getStrCode()
        dataset = self._sprav.getStorage().getLevelTable(parent_code)
        self.setDataset(dataset)
        # Отобразить путь
        code_path = self.getSpravPath(self._cur_code)
        self.path_statictext.SetLabel(code_path)

        try:
            codes = [rec[0] for rec in dataset]
            idx = codes.index(code)
            self.sprav_list_ctrl.Select(idx)
            self.sprav_list_ctrl.Focus(idx)
        except ValueError:
            print(code, self._cur_code, code_list)
            io_prnt.outWarning(u'Ошибка определения кода справочника <%s> при выборе из <%s>' % (code, parent_code))

    def getSprav(self):
        """
        Возвращает объкт справочника.
        """
        return self._sprav

    def getSelectedCode(self):
        """
        Выбранный код.
        """
        return self._selected_code

    def setSelectedCode(self, code):
        """
        Выбранный код.
        """
        self._selected_code = code

    def onCancelButtonClick(self, event):
        self._selected_code = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSpravListItemActive(self, event):
        """
        Обработчик двойного клика на элементе списка.
        """
        current_item = event.m_itemIndex
        self.setSelectedCode(self.sprav_list_ctrl.GetItemText(current_item))
        dataset = self._sprav.getStorage().getLevelTable(self._selected_code)
        if dataset:
            self.setNextCurCode(self._selected_code)
        self.setDataset(dataset)

        event.Skip()

    def onSpravListItemSelect(self, event):
        """
        Обработчик выбора элемента списка.
        """
        current_item = event.m_itemIndex
        self.setSelectedCode(self.sprav_list_ctrl.GetItemText(current_item))
        event.Skip()

    def onReturnToolClick(self, event):
        """
        Кнопка возврата на предыдущий уровень.
        """
        # Убрать последний код
        self.setPrevCurCode()
        code = self._getStrCode()
        dataset = self._sprav.getStorage().getLevelTable(code)
        self.setDataset(dataset)
        event.Skip()

    def onSearchToolClick(self, event):
        """
        Обработчик нажатия на кнопку поиска.
        """
        search_value = self.search_textctrl.GetValue()
        if search_value and search_value != self._last_search_value:
            # Поиск производится по наименованию
            search_result = self._sprav.getStorage().search(search_value)
            code = search_result[0]
            self.selectCode(code)
            self._last_search_value = search_value
            self._last_search_result = search_result
            self._last_search_idx = 0
        elif search_value and search_value == self._last_search_value:
            # Просто перейти на следующую строку в списке найденных
            self._last_search_idx += 1
            if self._last_search_idx >= len(self._last_search_result):
                self._last_search_idx = 0
            code = self._last_search_result[self._last_search_idx]
            self.selectCode(code)

        event.Skip()


def getSpravChoiceListDlg(parent=None, sprav=None):
    """
    Вызов диалогового окна выбора кода справочника.
    @param parent: Родительское окно.
    @param sprav: Справочник. Может задаваться как объектом,
        так и паспортом справочника.
    @return: Строковый выбранный код.
    """
    result = None
    if parent is None:
        parent = wx.GetApp().GetTopWindow()
    if sprav:
        if ic_util.is_pasport(sprav):
            # Справочник задается паспортом
            # Надо создать объект
            sprav = ic.getKernel().Create(sprav)

        dlg = None
        try:
            dlg = icSpravChoiceListDialog(parent)
            dlg.setSprav(sprav)
            dlg.ShowModal()
            result = dlg.getSelectedCode()
            dlg.Destroy()
            dlg = None
        except:
            if dlg:
                dlg.Destroy()
            io_prnt.outErr(u'Ошибка диалогового окна выбора кода справочника.')
    else:
        io_prnt.outWarning(u'Не определен справочник диалогового окна выбора кода справочника.')
    return result


def test():
    """
    Тестирование.
    """
    import ic
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)

    sprav_manager = ic.metadata.THIS.mtd.kladr_rf.create()
    sprav = sprav_manager.getSpravByName('nas_punkts')

    frame = wx.Frame(None, -1)

    dlg = icSpravChoiceListDialog(frame)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


def test2():
    """
    Тестирование.
    """
    import ic
    THIS_PRJ_DIR = os.path.dirname(os.getcwd())

    try:
        # Сразу установить режим отладки для отображения всех
        # вспомогательных сообщений
        ic.utils.ic_mode.setDebugMode()
        ic.log.init(ic.config)

        print('LOGIN PROJECT:', THIS_PRJ_DIR)
        if ic.Login('test_user', '', THIS_PRJ_DIR, True):
            print('LOGIN - OK')
            print('ENVIRONMENT:')
            ic.printEnvironmentTable()
            print('START TESTS...')

            sprav_manager = ic.metadata.THIS.mtd.kladr_rf.create()
            sprav = sprav_manager.getSpravByName('nas_punkts')

            print('RESULT CODE:', getSpravChoiceListDlg(sprav=sprav))
            print('...STOP TESTS')
        else:
            print('LOGIN - FAILED')
        ic.Logout()
    except:
        ic.Logout()
        raise


if __name__ == '__main__':
    test2()
