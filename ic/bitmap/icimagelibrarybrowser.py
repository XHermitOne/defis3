#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Браузер серилизованных графических библиотек.
"""

# Подключение библиотек
import os
import os.path
import wx
import wx.grid
import ic.interfaces.icobjectinterface as icobjectinterface

from ic.dlg import dlgfunc
from ic.utils import filefunc
from ic.utils import inifunc
from ic.bitmap import bmpfunc
from ic.bitmap import icimglib
from ic.log import log

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Resource description of class
resource={'recount': None, 'activate': 1, 'obj_module': None, 'show': 1, 'data_name': None, 'refresh': None, 'border': 0, 'size': (500, 400), 'style': 536877056, 'foregroundColor': None, 'span': (1, 1), 'fit': False, 'title': u'\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430 \u043e\u0431\u0440\u0430\u0437\u043e\u0432', 'component_module': None, 'proportion': 1, 'source': None, 'backgroundColor': None, 'type': u'Dialog', 'res_module': None, 'description': None, 'onClose': None, '_uuid': 'a9512aacba25ec93fa925609430fe8fc', 'moveAfterInTabOrder': u'', 'killFocus': None, 'flag': 8192, 'alias': None, 'child': [{'style': 0, 'activate': 1, 'obj_module': None, 'description': None, 'alias': None, 'component_module': None, 'proportion': 0, '_uuid': u'32486e1b40f14bc15c5c2a923448a305', 'modules': {'ic.imglib.common': '*'}, 'object': None, 'name': u'imp_imglib', 'flag': 0, 'init_expr': None, 'type': u'Import', 'position': (-1, -1), 'span': (1, 1), 'res_module': None, 'border': 0, 'size': (-1, -1)}, {'activate': 1, 'obj_module': None, 'minCellWidth': 10, 'minCellHeight': 10, 'flexCols': [], 'size': (-1, -1), 'style': 0, 'span': (1, 1), 'flexRows': [], 'component_module': None, 'border': 0, 'proportion': 1, 'type': u'GridBagSizer', 'res_module': None, 'hgap': 0, 'description': None, '_uuid': u'c460a19b041eb3c63d90de7344c455d5', 'flag': 8192, 'child': [{'activate': 1, 'obj_module': None, 'show': 1, 'recount': None, 'refresh': None, 'border': 0, 'size': (-1, -1), 'style': 2097188, 'foregroundColor': None, 'span': (1, 3), 'component_module': None, 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ToolBar', 'res_module': None, 'description': None, '_uuid': u'df29fd61b7b15d685ff579ace30e6434', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [{'activate': 1, 'name': u'NewTool', 'toolType': 0, 'shortHelpString': u'\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u0443\u044e \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443 \u043e\u0431\u0440\u0430\u0437\u043e\u0432', 'longHelpString': u'', '_uuid': u'75b88fac730f7e0ee381bbbf8544c830', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@imgNew', 'type': u'ToolBarTool', 'onTool': u'WrapperObj.OnToolFuncNewTool(evt)'}, {'activate': 1, 'name': u'OpenTool', 'toolType': 0, 'shortHelpString': u'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443 \u043e\u0431\u0440\u0430\u0437\u043e\u0432', 'longHelpString': u'', '_uuid': u'5e63fe0a371a590ecaa8a7a180905bb1', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@imgOpen', 'type': u'ToolBarTool', 'onTool': u'WrapperObj.OnToolFuncOpenTool(evt)'}, {'activate': 1, 'name': u'addTool', 'toolType': 0, 'shortHelpString': u'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043e\u0431\u0440\u0430\u0437', 'longHelpString': u'', '_uuid': u'80468b49f6fac942fe2840de8de98a09', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@imgPlus', 'type': u'ToolBarTool', 'onTool': u'WrapperObj.OnToolFuncAddTool(evt)'}, {'activate': 1, 'name': u'DelTool', 'toolType': 0, 'shortHelpString': u'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043e\u0431\u0440\u0430\u0437', 'longHelpString': u'', '_uuid': u'6ab8e9eda5adf9871471abae76256858', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@imgMinus', 'type': u'ToolBarTool', 'onTool': u'WrapperObj.OnToolFuncDelTool(evt)'}, {'activate': u'0', 'name': u'_2239', '_uuid': u'0f3446f7c1cc5cab64de9ab200207473', 'init_expr': None, 'type': u'Separator', 'size': 5}, {'activate': u'0', 'ctrl': None, 'pic': u'S', 'hlp': None, 'keyDown': None, 'font': {}, 'border': 0, 'size': (-1, 18), 'style': 0, 'foregroundColor': (0, 0, 0), 'span': (1, 1), 'component_module': None, 'show': 1, 'proportion': 0, 'source': None, 'init': None, 'valid': None, 'backgroundColor': (255, 255, 255), 'type': u'TextField', '_uuid': u'aa3b0eb0f62ac96172d59645a3d9f826', 'moveAfterInTabOrder': u'', 'flag': 0, 'recount': [], 'getvalue': None, 'field_name': None, 'setFocus': None, 'setvalue': None, 'name': u'NameEditTool', 'changed': None, 'value': u'', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None, 'refresh': []}, {'activate': u'0', 'name': u'_2413', '_uuid': u'343d8e95f5bf51add53f521885d5f57a', 'init_expr': None, 'type': u'Separator', 'size': 5}, {'activate': u'0', 'name': u'SettingsTool', 'toolType': 0, 'shortHelpString': u'\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438...', 'longHelpString': u'', '_uuid': u'8d96afc15d90f13c591e9bcf11707ac7', 'pushedBitmap': None, 'label': u'', 'isToggle': 0, 'init_expr': None, 'bitmap': u'@imgProperties', 'type': u'ToolBarTool', 'onTool': None}], 'name': u'ImgLibToolbar', 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (0, 0), 'onInit': None, 'bitmap_size': (16, 16)}, {'activate': u'0', 'show': 1, 'recount': None, 'keyDown': None, 'border': 0, 'size': (-1, -1), 'style': 0, 'foregroundColor': None, 'span': (1, 1), 'title': u'default', 'component_module': None, 'scrollRate': [5, 5], 'proportion': 0, 'source': None, 'backgroundColor': None, 'type': u'ScrolledWindow', '_uuid': u'80f2e98673b90d6d7a89aa304ff028ef', 'moveAfterInTabOrder': u'', 'flag': 8192, 'child': [], 'name': u'ImgLibWin', 'refresh': None, 'alias': None, 'init_expr': None, 'position': (-1, -1), 'onInit': None}, {'activate': 1, 'obj_module': None, 'show': 1, 'cellChange': None, 'col_count': 2, 'refresh': None, 'hrows': [], 'border': 0, 'size': wx.Size(488, 323), 'row_labels': [u'1'], 'col_label_height': -1, 'moveAfterInTabOrder': u'', 'foregroundColor': None, 'span': (3, 3), 'row_label_width': -1, 'cellSelect': None, 'source': None, 'component_module': None, 'proportion': 1, 'row_count': 1, 'backgroundColor': None, 'type': u'SimpleGrid', 'res_module': None, 'description': None, '_uuid': u'c961ca9502e53b34ad3d349a80dd72b6', 'style': 0, 'flag': 0, 'recount': None, 'child': [], 'name': u'ImgLibGrid', 'wcols': [], 'keyDown': None, 'alias': None, 'init_expr': None, 'position': (1, 0), 'onInit': None, 'col_labels': [u'A']}], 'name': u'DefaultName_1718', 'alias': None, 'init_expr': None, 'position': (-1, -1), 'vgap': 0}], 'icon': None, 'setFocus': None, 'name': u'ImgLibDlg', 'keyDown': None, 'init_expr': None, 'position': wx.Point(0, 0), 'onInit': None}

#   Version
__version__ = (1, 1, 1, 2)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'icImageLibraryBrowser'

# Константы


# Функции
def runImageLibraryBrowser(parent, prj_ini_filename=None, img_lib_filename=None):
    """
    Запуск браузера библиотеки образов.
    @param parent: РОдительское окно.
    @param prj_ini_filename: Файл настроек проекта.
    @param img_lib_filename: Имя файла библиотеки образов.
    """
    img_lib_browser = icImageLibraryBrowser(parent)
    if prj_ini_filename:
        img_lib_browser.loadImgDir(prj_ini_filename)
        
    if img_lib_filename and os.path.exists(img_lib_filename):
        result = img_lib_browser.openImgLib(img_lib_filename)
        if result:
            img_lib_browser.refreshImgGrid()
            
            # Прописть в заголовке диалогового окна имя файла библиотеки образов
            dlg = img_lib_browser.GetNameObj('ImgLibDlg')
            dlg.setTitle(u'Библиотека образов ' + img_lib_filename)
        

class icImageLibraryBrowser(icobjectinterface.icObjectInterface):
    """
    Браузер серилизованных графических библиотек.
    """
    def __init__(self, parent):
        """
        Конструктор интерфейса.
        """
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)
        self._img_lib_res = icimglib.icImgLibResource()
        # Словарь образов
        self._img_dict = {}
        
        # Папка образов
        self._img_dir = None
        # Файл настроек
        self._ini_file = None
        
        # Инициализация главного грида библиотеки образов
        img_grd = self.GetNameObj('ImgLibGrid')
        # События грида
        img_grd.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnImgGridCellChange)
        img_grd.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnImgGridEditorShown)

        # Имя редактируемого образа
        self._edit_img_name = None
        
        # Изменение некотоорых параметров грида
        if img_grd:
            img_grd.SetColLabelValue(0, u'Образ')
            img_grd.SetColLabelValue(1, u'Наименование')
            img_grd.AutoSizeColumn(1)
            
    def createNewImgLibFile(self):
        """
        Создание нового файла библиотеки образов.
        """
        dlg = self.GetNameObj('ImgLibDlg')
        img_lib_name = dlgfunc.getTextEntryDlg(dlg, u'Имя библиотеки образов',
                                             u'Введите имя библиотеки образов:', 'default')
        img_lib_dir = dlgfunc.getDirDlg(dlg, u'Папка размещения библиотеки образов')
        if img_lib_dir and img_lib_name:
            img_lib_file_name = os.path.join(img_lib_dir, img_lib_name+'.py')
            if os.path.exists(img_lib_file_name):
                dlgfunc.openMsgBox(title=u'ОШИБКА', prompt_text=u'Файл %s уже существует!' % img_lib_file_name, parent=dlg)
                return False
            # Создать новый файл
            self._img_lib_res.createNewImgLib()
            return self._img_lib_res.saveImgLib(img_lib_file_name)
        return False
            
    def addImg(self, img_filename=None):
        """
        Добавить новый образ в библиотеку.
        """
        if self._img_lib_res.isEmpty():
            dlgfunc.openMsgBox(title=u'ОШИБКА', prompt_text=u'Не определена библиотека образов!',
                               parent=self.getObject())
            return None

        dlg = self.GetNameObj('ImgLibDlg')
        if img_filename is None:
            img_filename = dlgfunc.getImageDlg(dlg, self._img_dir)
            # Сохранить выбранную папку как папку картинок
            self.setImgDir(os.path.dirname(img_filename))
            self.saveImgDir()
            
        if img_filename:
            # Серилизовать и добавить образ
            self._img_lib_res.addImg(img_filename)
            self._img_lib_res.saveImgLib()
            
            # Добавить в словарь образов
            img_name=os.path.splitext(os.path.basename(img_filename))[0]
            # Заменить все минусы на подчеркивание
            # иначе в генерирумом фалйе будут имена объектов с минусами (SyntaxisError)
            img_name = img_name.replace('-', '_')
            img = bmpfunc.createBitmap(img_filename)
            self._img_dict[img_name] = img
            return img_name
        return None

    def delImg(self, image_name=None):
        """
        Добавить новый образ в библиотеку.
        """
        yes_del = dlgfunc.getAskDlg(u'УДАЛЕНИЕ',
                                  u'Удалить образ <%s> из библиотеки образов?' % image_name)
        
        if (yes_del == wx.YES) and image_name:
            ok = self._img_lib_res.delImgBlock(image_name)
            if ok:
                if image_name in self._img_dict:
                    del self._img_dict[image_name]
                # Сохранить изменение в библиотеке образов.
                self._img_lib_res.saveImgLib()
                return True
        return False
            
    def renameImg(self, old_image_name, new_image_name):
        """
        Переименовать образ в библиотеке образов.
        """
        if old_image_name != new_image_name:
            ok=self._img_lib_res.renameImgBlock(old_image_name, new_image_name)
            if ok:
                if old_image_name in self._img_dict:
                    self._img_dict[new_image_name] = self._img_dict[old_image_name]
                    del self._img_dict[old_image_name]
                # Сохранить изменение в библиотеке образов.
                self._img_lib_res.saveImgLib()
                return True
        return False
            
    def openImgLib(self, img_lib_filename=None):
        """
        Открыть библиотеку образов.
        @param img_lib_filename: Имя файла библиотеки образов.
        """
        dlg = self.GetNameObj('ImgLibDlg')
        if img_lib_filename is None:
            img_lib_filename = dlgfunc.getFileDlg(dlg, u'',
                                               u'Библиотеки образов (*.py)|*.py')

        if img_lib_filename:
            self._img_lib_res.loadImgLib(img_lib_filename)
            self._img_dict = self._img_lib_res.getImages()
            return True
            
        return False
        
    def refreshImgGrid(self, image_dictionary=None):
        """
        Обновить грид просмотра образов.
        @param image_dictionary: Словарь образов.
        """
        if image_dictionary is None:
            image_dictionary = self._img_dict
            
        img_grid = self.GetNameObj('ImgLibGrid')
        if img_grid:
            # Очистить грид от записей
            img_grid.ClearGrid()
            if not self.isEmptyGrid(img_grid):
                img_grid.DeleteRows(1, img_grid.GetNumberRows()-2)
            # Заполнить грид записями
            img_names = list(image_dictionary.keys())
            img_names.sort()    # Отсортировать по именам
            for i,img_name in enumerate(img_names):
                self.addImgToGrid(img_name, image_dictionary[img_name])
    
    def isEmptyGrid(self, grid):
        """
        Проверить пустой грид или нет.
        @param grid: Сам грид.
        """
        return bool((grid.GetNumberRows() == 1) and (not grid.GetCellValue(0, 1)))
        
    def addImgToGrid(self, image_name, image):
        """
        Добавить образ в грид.
        @param image_name: Имя образа.
        @param image: Объект образа wx.Bitmap.
        """
        img_grid = self.GetNameObj('ImgLibGrid')
        if img_grid:
            if not self.isEmptyGrid(img_grid):
                img_grid.AppendRows()
            i = img_grid.GetNumberRows()-1
            # Установить картинку и надпись
            img_grid.setCellImg(i, 0, image)
            img_grid.SetCellValue(i, 1, image_name)
            # Переразмерить высоту строк
            img_grid.SetRowSize(i, image.GetHeight() + 5)
        
    def getImgName(self, img_filename=None):
        """
        Имя образа по файлу образа.
        """
        if img_filename:
            return 'img'+os.path.splitext(os.path.basename(img_filename))[0]
        return 'img'+str(wx.NewId())

    def setImgDir(self, img_directory):
        """
        Установить папку образов.
        """
        self._img_dir = img_directory
    
    def loadImgDir(self, ini_filename=None):
        """
        Загрузить папку образов из настроек.
        """
        if ini_filename:
            self._ini_file = ini_filename
        
        if self._ini_file:
            img_dir = inifunc.loadParamINI(self._ini_file, 'IMAGES', 'img_dir')
            self.setImgDir(img_dir)
        
    def saveImgDir(self, ini_filename=None):
        """
        Сохранить папку образов в настройках.
        """
        if ini_filename:
            self._ini_file = ini_filename
        
        if self._ini_file:
            if self._img_dir:
                return inifunc.saveParamINI(self._ini_file, 'IMAGES', 'img_dir', self._img_dir)
        return None
        
    ###BEGIN EVENT BLOCK
    
    def OnToolFuncNewTool(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        ok = self.createNewImgLibFile()
        
        # Прописть в заголовке диалогового окна имя файла библиотеки образов
        img_lib_file_name = self._img_lib_res.getImgLibFileName()
        if img_lib_file_name and ok:
            dlg = self.GetNameObj('ImgLibDlg')
            dlg.setTitle(u'Библиотека образов ' + img_lib_file_name)
            
        event.Skip()

    def OnToolFuncAddTool(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        img_name = self.addImg()
        if img_name:
            self.addImgToGrid(img_name, self._img_dict[img_name])

        event.Skip()

    def OnToolFuncOpenTool(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        ok = self.openImgLib()
        
        if ok:
            self.refreshImgGrid()
            
        # Прописть в заголовке диалогового окна имя файла библиотеки образов
        img_lib_file_name = self._img_lib_res.getImgLibFileName()
        if img_lib_file_name and ok:
            dlg = self.GetNameObj('ImgLibDlg')
            dlg.setTitle(u'Библиотека образов ' + img_lib_file_name)
            
        event.Skip()

    def OnToolFuncDelTool(self, event):
        """
        Функция обрабатывает событие <?>.
        """
        img_grid = self.GetNameObj('ImgLibGrid')
        img_grid_row = img_grid.GetGridCursorRow()
        img_name = img_grid.GetCellValue(img_grid_row, 1)
        if img_name:
            ok = self.delImg(img_name)
            img_grid.DeleteRows(img_grid_row, 1)
            
        event.Skip()

    def OnImgGridCellChange(self, event):
        """
        Изменение значения ячейки.
        """
        row = event.GetRow()
        col = event.GetCol()
        if col == 1:
            img_grid = self.GetNameObj('ImgLibGrid')
            new_img_name = img_grid.GetCellValue(row, 1)
            log.info(u'IMAGE RENAME <%s> -> <%s>' % (self._edit_img_name, new_img_name))
            self.renameImg(self._edit_img_name, new_img_name)
        event.Skip()
        
    def OnImgGridEditorShown(self, event):
        """
        ОТкрытие редактора ячейки.
        """
        row = event.GetRow()
        col = event.GetCol()
        if col == 1:
            img_grid = self.GetNameObj('ImgLibGrid')
            self._edit_img_name = img_grid.GetCellValue(row, 1)
        event.Skip()

    ###END EVENT BLOCK


def test(par=0):
    """
    Тестируем класс ImageLibraryBrowser.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    
    #
    # Тестовый код
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
