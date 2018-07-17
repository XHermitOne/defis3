#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфейс взаимодействия с IDE.
"""

# Подключение библиотек
import wx

__version__ = (0, 0, 1, 2)

DEFAULT_ENCODINT_STR = '<Default Encoding>'


class icIDEInterface:
    """
    Интерфейс взаимодействия с IDE.
    """

    def __init__(self, IDEFrame=None):
        """
        Конструктор.
        @param IDEFrame: Указатель на главное окно IDE.
        """
        self._ide = IDEFrame
        if self._ide:
            self._ide.Bind(wx.EVT_CLOSE, self.OnCloseIC)

    def OnCloseIC(self, event):
        """
        Пост обработчик закрытия главного окна IDE.
        """
        pass

    def getResourceEditorWin(self):
        """
        Окно/Закладка редактора ресурсов.
        """
        pass
        
    def AddToolPanel(self, Panel_):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.
        @param Panel_: Наследник wx.Panel.
        @return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        pass
        
    def OpenFile(self, filename, OpenInNewTab=True,
                 editrecentfiles=True, encoding=DEFAULT_ENCODINT_STR, readonly=False):
        """
        Загружает нужный файл в IDE.
        
        @type filename: C{string}
        @param filename: Имя загружаемого файла.
        @type OpenInNewTab: C{bool}
        @param OpenInNewTab: Признак загрузки файла на новой закладке.
        @type editrecentfiles: C{bool}
        @param editrecentfiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        @type encoding: C{string}
        @param encoding: Кодировка файла.
        @type readonly: C{bool}
        @param readonly: Указание, что файл откроется только для чтения.
        @rtype: C{bool}
        @return: Признак успешной загрузки.
        """
        pass
        
    def CloseFile(self, fileName):
        """
        Выгружает файл.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной выгрузки.
        """
        pass
        
    def CloseAllFiles(self):
        """
        Выгрузить все файлы.
        """
        pass

    def GetAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        pass
        
    def insertEvtFuncToInterface(self, fileName, funcName, bodyFunc=None):
        """
        Вставляет в тело интерфейсного модуля заготовку функции с заданным именем.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        @type funcName: C{string}
        @param funcName: Имя функции.
        @type bodyFunc: C{string}
        @param bodyFunc: Тело функции.
        """
        pass
        
    def IsOpenedFile(self, fileName):
        """
        Проверить открыт файл или нет.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        pass
        
    def SetSelection(self, i):
        """
        Устанавливает нужный файл в качестве текущего.
        """
        if self.GetDocumentNotebook():
            self.GetDocumentNotebook().SetSelection(i)
            self.GetDocumentNotebook().SetTab()
    
    def _getOpenedFileIdx(self, fileName):
        """
        Индекс открытого файла.
        @type fileName: C{string}
        @param fileName: Имя файла.
        @return: Индекс открытого файла или
            -1, если файл не открыт.
        """
        alreadyopen = self.GetAlreadyOpen()
        i = -1
        try:
            i = alreadyopen.index(fileName)
        except ValueError:
            i = -1
        return i
        
    def SelectFile(self, fileName):
        """
        Устанавливает нужный файл в качестве текущего.

        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешного выбора.
        """
        fl = fileName.replace('\\', '/')
        alreadyopen = self.GetAlreadyOpen()
            
        if alreadyopen and fl in alreadyopen:
            i = alreadyopen.index(fl)
            self.SetSelection(i)
            return True
            
        return False
        
    def GetDocumentNotebook(self):
        """
        Возвращает указатель на документы, организованные в 'записной книжке'.
        """
        pass
        
    def GetDocument(self):
        """
        Возвращает текущий документ.
        """
        pass
    
    def GetDocumentObj(self, fileName):
        """
        Возвращает объект документа.

        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        pass
    
    def GetDocumentText(self, fileName):
        """
        Возвращает текст документа.

        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        pass
                
    def GetSourceBrowser(self):
        """
        Возвращает указатель на SourceBrowser текста.
        """
        pass

    def GetMatches(self, text, resourcebrowser):
        """
        """
        pass
        
    def GetModify(self, fileName):
        """
        Возвращает признак измененного документа.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        pass
        
    def GoToFunc(self, funcname):
        """
        Переход на нужную функцию.
        """
        pass

    def GetMainPanel(self):
        """
        Главная панель IDE.
        """
        pass

    def GetBrowserNotebook(self):
        """
        Браузер.
        """
        pass
        
    def GetToolNotebook(self):
        """
        Нотебук инструменнтов/палитры компонентов.
        """
        pass

    def HideToolNotebook(self):
        """
        Скрыть нотебук инструменнтов/палитры компонентов.
        """
        pass

    def ReloadFile(self, fileName):
        """
        Перегружает нужный файл в IDE.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной перезагрузки.
        """
        pass
            
    def SetDocumentText(self, fileName, txt):
        """
        Изменяет текст документа.
        """
        pass
        
    def ShowToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        pass

    def GetIDEFrame(self):
        """
        """
        return self._ide
