#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Интерфес взаимодействи редактора ресурсов с IDE drPython.
"""

# --- Подключение библиотек ---
from . import icideinterface
import re

# --- Шаблоны
interfaceTemplate = '''
    def %s(self, evt):
        \"\"\"
        Функция обрабатывает событие <?>.
        \"\"\"
        return None
'''

__version__ = (0, 0, 1, 2)


# --- Классы ---
class drPythonInterface(icideinterface.icIDEInterface):
    """
    Интерфейс взаимодействия с IDE.
    """
    def __init__(self, drFrame=None):
        """
        Конструктор.
        @param drFrame: Указатель на главное окно IDE.
        """
        icideinterface.icIDEInterface.__init__(self, drFrame)

    def OnCloseIC(self, event):
        """
        Пост обработчик закрытия главного окна IDE.
        """
        res_editor_win = self.getResourceEditorWin()

        if res_editor_win:
            prj_root = res_editor_win.prj_edt.getPrj()
            print(prj_root)
            if prj_root:
                # Удалить все блокировки при выходе из редактора
                prj_root.exit()
        event.Skip()

    def getResourceEditorWin(self):
        """
        Окно/Закладка редактора ресурсов.
        """
        browser_notebook = self.GetBrowserNotebook()
        if browser_notebook:
            for i_page in range(browser_notebook.GetPageCount()):
                if browser_notebook.GetPageText(i_page).strip() == u'DEFIS':
                    return browser_notebook.GetPage(i_page)
        return None
        
    def AddToolPanel(self, Panel_):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.
        @param Panel_: Наследник wx.Panel.
        @return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        main_panel = self.GetMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            page, i = main_panel.GetTargetNotebookPage(tool_notebook_indx,
                                                       u'Палитра инструментов')
            Panel_.Reparent(page)
            page.SetPanel(Panel_)
            main_panel.ShowPanel(tool_notebook_indx, i)
            return page
        
    def OpenFile(self, filename, OpenInNewTab=True,
                 editrecentfiles=True, encoding='<Default Encoding>', readonly=False):
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
        self.GetIDEFrame().OpenFile(filename, OpenInNewTab, editrecentfiles, encoding)
        self.GetIDEFrame().txtDocument.SetReadOnly(readonly)
        
    def CloseFile(self, fileName):
        """
        Выгружает файл.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной выгрузки.
        """
        i = self._getOpenedFileIdx(fileName)
        if i >= 0:
            self.SetSelection(i)
            self.GetIDEFrame().OnClose(None)
        return True

    def CloseAllFiles(self):
        """
        Выгрузить все файлы.
        """
        self.GetIDEFrame().OnCloseAllDocuments(None)
        return True

    def GetAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        return self.GetIDEFrame().GetAlreadyOpen()
        
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
        if self.SelectFile(fileName):
            if self.GoToFunc(funcName):
                return True
            else:
                txt = self.GetDocumentText(fileName)
                
                #   Ищем секцию для обработчиков событий
                indx = txt.find('###END EVENT')
                
                #   Если специальная секция не найдена, то вставляем функцию
                #   перед конструктором
                if indx < 0:
                    indx = txt.find('def __init__')
                    
                if indx >= 0:
                    funcTxt = interfaceTemplate % funcName
                    txt = txt[:indx] + funcTxt + '    ' + txt[indx:]
                    self.SetDocumentText(fileName, txt)
                
        return False
        
    def IsOpenedFile(self, fileName):
        """
        Проверить открыт файл или нет.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        # Сначала нормализовать имя файла к UNIX виду
        fileName = fileName.replace('\\', '/').replace('//', '/')
        return fileName in self.GetAlreadyOpen()
        
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
        if self.GetIDEFrame():
            return self.GetIDEFrame().documentnotebook
        
    def GetDocument(self):
        """
        Возвращает текущий документ.
        """
        return self.GetIDEFrame().txtDocument
    
    def GetDocumentObj(self, fileName):
        """
        Возвращает объект документа.

        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        fl = fileName.replace('\\', '/')
        al = self.GetAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            return self.GetIDEFrame().txtDocumentArray[docnumber]
    
    def GetDocumentText(self, fileName):
        """
        Возвращает текст документа.

        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        fl = fileName.replace('\\','/')
        al = self.GetAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            text = self.GetIDEFrame().txtDocumentArray[docnumber].GetText()
            return text
                
    def GetSourceBrowser(self):
        """
        Возвращает указатель на SourceBrowser текста.
        """
        return self.GetIDEFrame().SourceBrowser

    def GetMatches(self, text, resourcebrowser):
        """
        """
        matches = []
        positions = []
            
        matcher = resourcebrowser.finditer(text)
        
        try:
            match = matcher.next()
        except:
            match = None
        while match is not None:
            matches.append(match.group().replace('\t', '    '))
            positions.append(match.start())
            try:
                match = matcher.next()
            except:
                match = None
            
        return matches, positions
        
    def GetModify(self, fileName):
        """
        Возвращает признак измененного документа.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        return self.GetDocumentObj(fileName).GetModify()
        
    def GoToFunc(self, funcname):
        """
        """
        Document = self.GetDocument()

        if Document:
            compchar = Document.GetIndentationCharacter()
            resourcebrowser = re.compile(r'(^'+compchar+'*?class\s.*[(:])|(^'+compchar+'*?def\s.*[(:])|(^'+compchar+'*?import\s.*$)|(^'+compchar+'*?from\s.*$)', re.MULTILINE)
            text = Document.GetText()
            
            matches, positions = self.GetMatches(text, resourcebrowser)
            
            for i, sl in enumerate(matches):
                if funcname in sl:
                    line = Document.LineFromPosition(positions[i])
                    Document.EnsureVisible(line)
                    Document.ScrollToLine(line)
                    Document.GotoLine(line)
                    Document.GotoPos(positions[i])
                    Document.SetFocus()
                    Document.SetSTCFocus(True)
                    return True
        
        return False

    def GetMainPanel(self):
        """
        Гравная панель IDE.
        """
        if self.GetIDEFrame():
            return self.GetIDEFrame().mainpanel

    def GetBrowserNotebook(self):
        """
        Браузер.
        """
        main_panel = self.GetMainPanel()
        if main_panel:
            return main_panel.leftNotebook

    def GetToolNotebook(self):
        """
        Нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.GetMainPanel()
        if main_panel:
            return main_panel.rightNotebook

    def HideToolNotebook(self):
        """
        Скрыть нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.GetMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            main_panel.RightIsVisible = False

    def ReloadFile(self, fileName):
        """
        Перегружает нужный файл в IDE.
        
        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной перезагрузки.
        """
        al = self.GetAlreadyOpen()
        
        if fileName in al:
            indx = al.index(fileName)
            self.GetIDEFrame().setDocumentTo(indx, True)
            self.OpenFile(fileName, False)
            
    def SetDocumentText(self, fileName, txt):
        """
        Изменяет текст документа.
        """
        fl = fileName.replace('\\', '/')
        al = self.GetAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            self.GetIDEFrame().txtDocumentArray[docnumber].SetText(txt)

    def ShowToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.GetMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            main_panel.RightIsVisible = True
