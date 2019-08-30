#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Интерфес взаимодействи редактора ресурсов с IDE drPython.
"""

# --- Подключение библиотек ---
from . import icideinterface
import re

# --- Шаблоны
interfaceTemplate = '''
    def %s(self, event):
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

    def onPostClose(self, event):
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
        browser_notebook = self.getBrowserNotebook()
        if browser_notebook:
            for i_page in range(browser_notebook.GetPageCount()):
                if browser_notebook.GetPageText(i_page).strip() == u'DEFIS':
                    return browser_notebook.GetPage(i_page)
        return None
        
    def addToolPanel(self, panel):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.
        @param panel: Наследник wx.Panel.
        @return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        main_panel = self.getMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            page, i = main_panel.GetTargetNotebookPage(tool_notebook_indx,
                                                       u'Палитра инструментов')
            panel.Reparent(page)
            page.SetPanel(panel)
            main_panel.ShowPanel(tool_notebook_indx, i)
            return page
        
    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding='<Default Encoding>', bReadonly=False):
        """
        Загружает нужный файл в IDE.
        
        @type filename: C{string}
        @param filename: Имя загружаемого файла.
        @type bOpenInNewTab: C{bool}
        @param bOpenInNewTab: Признак загрузки файла на новой закладке.
        @type bEditRecentFiles: C{bool}
        @param bEditRecentFiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        @type encoding: C{string}
        @param encoding: Кодировка файла.
        @type bReadonly: C{bool}
        @param bReadonly: Указание, что файл откроется только для чтения.
        @rtype: C{bool}
        @return: Признак успешной загрузки.
        """
        self.getIDEFrame().openFile(filename, bOpenInNewTab, bEditRecentFiles, encoding)
        self.getIDEFrame().txtDocument.SetReadOnly(bReadonly)
        
    def closeFile(self, filename):
        """
        Выгружает файл.
        
        @type filename: C{string}
        @param filename: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной выгрузки.
        """
        i = self._getOpenedFileIdx(filename)
        if i >= 0:
            self.setSelection(i)
            self.getIDEFrame().OnClose(None)
        return True

    def closeAllFiles(self):
        """
        Выгрузить все файлы.
        """
        self.getIDEFrame().OnCloseAllDocuments(None)
        return True

    def getAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        return self.getIDEFrame().getAlreadyOpen()
        
    def insertEvtFuncToInterface(self, filename, func_name, function_body=None):
        """
        Вставляет в тело интерфейсного модуля заготовку функции с заданным именем.
        
        @type filename: C{string}
        @param filename: Имя файла.
        @type func_name: C{string}
        @param func_name: Имя функции.
        @type function_body: C{string}
        @param function_body: Тело функции.
        """
        if self.selectFile(filename):
            if self.goToFunc(func_name):
                return True
            else:
                txt = self.getDocumentText(filename)
                
                #   Ищем секцию для обработчиков событий
                indx = txt.find('###END EVENT')
                
                #   Если специальная секция не найдена, то вставляем функцию
                #   перед конструктором
                if indx < 0:
                    indx = txt.find('def __init__')
                    
                if indx >= 0:
                    funcTxt = interfaceTemplate % func_name
                    txt = txt[:indx] + funcTxt + '    ' + txt[indx:]
                    self.setDocumentText(filename, txt)
                
        return False
        
    def isOpenedFile(self, filename):
        """
        Проверить открыт файл или нет.
        @type filename: C{string}
        @param filename: Имя файла.
        """
        # Сначала нормализовать имя файла к UNIX виду
        filename = filename.replace('\\', '/').replace('//', '/')
        return filename in self.getAlreadyOpen()
        
    def setSelection(self, idx):
        """
        Устанавливает нужный файл в качестве текущего.
        """
        if self.getDocumentNotebook():
            self.getDocumentNotebook().setSelection(idx)
            self.getDocumentNotebook().SetTab()
    
    def _getOpenedFileIdx(self, filename):
        """
        Индекс открытого файла.
        @type filename: C{string}
        @param filename: Имя файла.
        @return: Индекс открытого файла или
            -1, если файл не открыт.
        """
        alreadyopen = self.getAlreadyOpen()
        i = -1
        try:
            i = alreadyopen.index(filename)
        except ValueError:
            i = -1
        return i
        
    def selectFile(self, filename):
        """
        Устанавливает нужный файл в качестве текущего.

        @type filename: C{string}
        @param filename: Имя файла.
        @rtype: C{bool}
        @return: Признак успешного выбора.
        """
        fl = filename.replace('\\', '/')
        alreadyopen = self.getAlreadyOpen()
            
        if alreadyopen and fl in alreadyopen:
            i = alreadyopen.index(fl)
            self.setSelection(i)

            return True
            
        return False
        
    def getDocumentNotebook(self):
        """
        Возвращает указатель на документы, организованные в 'записной книжке'.
        """
        if self.getIDEFrame():
            return self.getIDEFrame().documentnotebook
        
    def getDocument(self):
        """
        Возвращает текущий документ.
        """
        return self.getIDEFrame().txtDocument
    
    def getDocumentObj(self, filegame):
        """
        Возвращает объект документа.

        @type filegame: C{string}
        @param filegame: Имя файла.
        """
        fl = filegame.replace('\\', '/')
        al = self.getAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            return self.getIDEFrame().txtDocumentArray[docnumber]
    
    def getDocumentText(self, filename):
        """
        Возвращает текст документа.

        @type filename: C{string}
        @param filename: Имя файла.
        """
        fl = filename.replace('\\', '/')
        al = self.getAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            text = self.getIDEFrame().txtDocumentArray[docnumber].GetText()
            return text
                
    def getSourceBrowser(self):
        """
        Возвращает указатель на SourceBrowser текста.
        """
        return self.getIDEFrame().SourceBrowser

    def getMatches(self, text, resource_browser):
        """
        """
        matches = []
        positions = []
            
        matcher = resource_browser.finditer(text)
        
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
        
    def getModify(self, filename):
        """
        Возвращает признак измененного документа.
        
        @type filename: C{string}
        @param filename: Имя файла.
        """
        return self.getDocumentObj(filename).getModify()
        
    def goToFunc(self, func_name):
        """
        """
        Document = self.getDocument()

        if Document:
            compchar = Document.GetIndentationCharacter()
            resourcebrowser = re.compile(r'(^'+compchar+'*?class\s.*[(:])|(^'+compchar+'*?def\s.*[(:])|(^'+compchar+'*?import\s.*$)|(^'+compchar+'*?from\s.*$)', re.MULTILINE)
            text = Document.GetText()
            
            matches, positions = self.getMatches(text, resourcebrowser)
            
            for i, sl in enumerate(matches):
                if func_name in sl:
                    line = Document.LineFromPosition(positions[i])
                    Document.EnsureVisible(line)
                    Document.ScrollToLine(line)
                    Document.GotoLine(line)
                    Document.GotoPos(positions[i])
                    Document.SetFocus()
                    Document.SetSTCFocus(True)
                    return True
        
        return False

    def getMainPanel(self):
        """
        Гравная панель IDE.
        """
        if self.getIDEFrame():
            return self.getIDEFrame().mainpanel

    def getBrowserNotebook(self):
        """
        Браузер.
        """
        main_panel = self.getMainPanel()
        if main_panel:
            return main_panel.leftNotebook

    def getToolNotebook(self):
        """
        Нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.getMainPanel()
        if main_panel:
            return main_panel.rightNotebook

    def hideToolNotebook(self):
        """
        Скрыть нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.getMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            main_panel.RightIsVisible = False

    def reloadFile(self, filename):
        """
        Перегружает нужный файл в IDE.
        
        @type filename: C{string}
        @param filename: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной перезагрузки.
        """
        al = self.getAlreadyOpen()
        
        if filename in al:
            indx = al.index(filename)
            self.getIDEFrame().setDocumentTo(indx, True)
            self.openFile(filename, False)
            
    def setDocumentText(self, filename, txt):
        """
        Изменяет текст документа.
        """
        fl = filename.replace('\\', '/')
        al = self.getAlreadyOpen()
        
        if fl in al:
            docnumber = al.index(fl)
            self.getIDEFrame().txtDocumentArray[docnumber].SetText(txt)

    def showToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        main_panel = self.getMainPanel()
        tool_notebook_indx = 1
        if main_panel:
            main_panel.RightIsVisible = True
