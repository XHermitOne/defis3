#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Интерфейс взаимодействия с IDE.
"""

# Подключение библиотек
import wx

from ic.utils import txtfunc
from ic.log import log

__version__ = (0, 1, 2, 1)

DEFAULT_ENCODINT_STR = '<Default Encoding>'

# Шаблоны
# Шаблон метода класса
METHOD_TEMPLATE = '''
    def %s(self, event):
        return None
'''

# Шаблон функции - обработчика
FUNCTION_TEMPLATE = '''
def %s(obj, event):
    return None
'''

DEFAULT_ENCODING = 'utf-8'


class icIDEInterface(object):
    """
    Интерфейс взаимодействия с IDE.
    """
    def __init__(self, IDEFrame=None):
        """
        Конструктор.

        :param IDEFrame: Указатель на главное окно IDE.
        """
        self._ide = IDEFrame
        if self._ide:
            self._ide.Bind(wx.EVT_CLOSE, self.onPostClose)

    def onPostClose(self, event):
        """
        Пост обработчик закрытия главного окна IDE.
        """
        pass

    def getResourceEditorWin(self):
        """
        Окно/Закладка редактора ресурсов.
        """
        pass
        
    def addToolPanel(self, panel):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.

        :param panel: Наследник wx.Panel.
        :return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        pass
        
    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding=DEFAULT_ENCODINT_STR, bReadonly=False):
        """
        Загружает нужный файл в IDE.
        
        :type filename: C{string}
        :param filename: Имя загружаемого файла.
        :type bOpenInNewTab: C{bool}
        :param bOpenInNewTab: Признак загрузки файла на новой закладке.
        :type bEditRecentFiles: C{bool}
        :param bEditRecentFiles: Признак сохранении в списке недавно загружаемых файлов
            (пункт меню <File->Recent Open>).
        :type encoding: C{string}
        :param encoding: Кодировка файла.
        :type bReadonly: C{bool}
        :param bReadonly: Указание, что файл откроется только для чтения.
        :rtype: C{bool}
        :return: Признак успешной загрузки.
        """
        pass
        
    def closeFile(self, filename):
        """
        Выгружает файл.
        
        :type filename: C{string}
        :param filename: Имя файла.
        :rtype: C{bool}
        :return: Признак успешной выгрузки.
        """
        pass
        
    def closeAllFiles(self):
        """
        Выгрузить все файлы.
        """
        pass

    def getAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        pass
        
    def insertEvtFuncToInterface(self, filename, func_name, function_body=None):
        """
        Вставляет в тело интерфейсного модуля заготовку функции с заданным именем.
        По умолчанию вставка производится в текстовый файл
        в секцию обработчиков событий.

        :type filename: C{string}
        :param filename: Имя файла.
        :type func_name: C{string}
        :param func_name: Имя функции.
        :type function_body: C{string}
        :param function_body: Тело функции.
        :return: True/False.
        """
        if self.goToFunc(func_name, filename=filename):
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
                funcTxt = METHOD_TEMPLATE % func_name
                txt = txt[:indx] + funcTxt + '    ' + txt[indx:]
            else:
                funcTxt = FUNCTION_TEMPLATE % func_name
                # В противном случае добавляем в конец модуля.
                txt = txt + '\n' + funcTxt

            self.setDocumentText(filename, txt)
        return self.goToFunc(func_name=func_name, filename=filename)

    def isOpenedFile(self, filename):
        """
        Проверить открыт файл или нет.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        pass
        
    def setSelection(self, idx):
        """
        Устанавливает нужный файл в качестве текущего.
        """
        if self.getDocumentNotebook():
            self.getDocumentNotebook().SetSelection(idx)
            self.getDocumentNotebook().SetTab()
    
    def _getOpenedFileIdx(self, filename):
        """
        Индекс открытого файла.

        :type filename: C{string}
        :param filename: Имя файла.
        :return: Индекс открытого файла или
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

        :type filename: C{string}
        :param filename: Имя файла.
        :rtype: C{bool}
        :return: Признак успешного выбора.
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
        pass
        
    def getDocument(self):
        """
        Возвращает текущий документ.
        """
        pass
    
    def getDocumentObj(self, filegame):
        """
        Возвращает объект документа.

        :type filegame: C{string}
        :param filegame: Имя файла.
        """
        pass
    
    def getDocumentText(self, filename):
        """
        Возвращает текст документа.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        return txtfunc.load_file_text(filename=filename)
                
    def getSourceBrowser(self):
        """
        Возвращает указатель на SourceBrowser текста.
        """
        pass

    def getMatches(self, text, resource_browser):
        """
        """
        pass
        
    def getModify(self, filename):
        """
        Возвращает признак измененного документа.
        
        :type filename: C{string}
        :param filename: Имя файла.
        """
        pass
        
    def goToFunc(self, func_name, filename=None):
        """
        Переход на нужную функцию.

        :param func_name: Имя функции.
        :param filename: Имя файла.
        :return: True - есть такая функция и переход успешно произошел/
            False - такой функции нет и переход не возможен.
            None - Ошибка.
        """
        if filename is None:
            # Имя файла не определено, то переход не возможен
            log.warning(u'Не определено имя файла модуля для перехода на функцию <%s>' % func_name)
            return False

        try:
            txt = self.getDocumentText(filename=filename)
            for n_line, line in enumerate(txt.split('\n')):
                if line.find('def ' + func_name) >= 0:
                    return self.goToLine(filename=filename, n_line=n_line)
            return False
        except:
            log.fatal(u'Ошибка перехода на функцию <%s> в модуле <%s>' % (func_name, filename))
        return None

    def goToLine(self, filename, n_line=0):
        """
        Выпонить переход на линию модуля.

        :param filename: Имя файла модуля.
        :param n_line: Номер линии для перехода.
        :return: True - выполнен переход / False - переход не выполнен.
        """
        return False

    def getMainPanel(self):
        """
        Главная панель IDE.
        """
        pass

    def getBrowserNotebook(self):
        """
        Браузер.
        """
        pass
        
    def getToolNotebook(self):
        """
        Нотебук инструменнтов/палитры компонентов.
        """
        pass

    def hideToolNotebook(self):
        """
        Скрыть нотебук инструменнтов/палитры компонентов.
        """
        pass

    def reloadFile(self, filename):
        """
        Перегружает нужный файл в IDE.
        
        :type filename: C{string}
        :param filename: Имя файла.
        :rtype: C{bool}
        :return: Признак успешной перезагрузки.
        """
        pass
            
    def setDocumentText(self, filename, txt):
        """
        Изменяет текст документа.
        """
        return txtfunc.save_file_text(filename=filename, txt=txt)
        
    def showToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        pass

    def getIDEFrame(self):
        """
        """
        return self._ide

    def openFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.

        :param res: Ресурсное описание.
        :param res_editor: Указатель на редактор ресурсов.
        """
        pass
