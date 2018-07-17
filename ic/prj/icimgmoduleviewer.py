#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Просмотрщик узла модуля библиотеки образов проекта.
"""

# --- Подключение библиотек ---
import wx
import wx.grid
from ic.log import ic_log
from ic.utils import util
from ic.utils import ic_file
from ic.bitmap import icimglib
from ic.interfaces import icprjnodeviewer
from ic.components.user import icsimplegrid

_ = wx.GetTranslation
# --- Константы ---
# --- Функции управления ---

# --- Описание классов ---


class icImgModulePrjNodeViewer(icprjnodeviewer.icPrjNodeViewerInterface,
                               icsimplegrid.icSimpleGrid):
    """
    Просмотрщик узла модуля библиотеки образов проекта.
    """

    def __init__(self, parent, Node_):
        """
        Конструктор.
        """
        icprjnodeviewer.icPrjNodeViewerInterface.__init__(self, parent, Node_)
        icsimplegrid.icSimpleGrid.__init__(self, parent, wx.NewId(), None)
        
        self._full_py_file_name = Node_.getFullModuleFileName()

        self._img_lib_res = icimglib.icImgLibResource()
        # Словарь образов
        self._img_dict = {}
        self._img_lib_res.loadImgLib(self._full_py_file_name)
        self._img_dict = self._img_lib_res.getImages()
        
        self._init()
        
    def _init(self):
        """
        Инициализация грида просмотра образов.
        """
        self.setColLabels([u'Образ', u'Наименование'])
        self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        # Очистить грид от записей
        self.ClearGrid()
        if not bool((self.GetNumberRows() == 1) and (not self.GetCellValue(0, 1))):
            self.DeleteRows(1, self.GetNumberRows())
        # Заполнить грид записями
        img_names = self._img_dict.keys()
        img_names.sort()    # Отсортировать по именам
        for i, img_name in enumerate(img_names):
            self._addImg(img_name, self._img_dict[img_name])

    def _addImg(self, ImgName_, Img_):
        """
        Добавить образ в грид.
        @param ImgName_: Имя образа.
        @param Img_: Объект образа wx.Bitmap.
        """
        if not bool((self.GetNumberRows() == 1) and (not self.GetCellValue(0, 1))):
            self.AppendRows()
        i = self.GetNumberRows()-1
        # Установить картинку и надпись
        self.setCellImg(i, 0, Img_)
        self.SetCellValue(i, 1, ImgName_)
        # Запретить редактирование
        self.SetReadOnly(i, 0)
        self.SetReadOnly(i, 1)
        # Переразмерить высоту строк
        self.SetRowSize(i, Img_.GetHeight()+5)
        
    def getSelectedObject(self):
        """
        Выделенный объект.
        """
        return {'type': 'wx.StaticBitmap',
                'name': self.GetCellValue(self.GetGridCursorRow(), 1)}
            
    def getNodeResFileName(self):
        """
        Имя файла резурса.
        """
        return self._full_py_file_name
