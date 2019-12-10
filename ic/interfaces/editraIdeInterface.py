#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Интерфейс взаимодействия с IDE Editra.
"""

# Подключение библиотек
import os.path
import wx

from . import icideinterface
from . import icdesignerinterface
from ic.PropertyEditor import icPanelEditor
from ic.imglib import common
from ic.log import log

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

DEFIS_PANE = 'DefisPanel'


class EditraDocumentInterface(object):
    """
    Интерфейс документа для IDE Editra.
    """

    def __init__(self, filename, *arg, **kwarg):
        """
        Конструктор.

        :param filename: Имя файла документа.
        """
        self._finfo = dict(filename=filename, encoding='utf-8', hasbom=False, modtime=0)
        self._cursor = 0
        
    def GetFileName(self):
        """
        Имя файла хранения документа.
        """
        return self._finfo['filename']
    
    def GetModTime(self):
        """
        Возращает время модификации документа.
        """
        return self._finfo['modtime']
    
    def SetModTime(self, modtime):
        """
        Возращает время модификации документа.
        """
        self._finfo['modtime'] = modtime

    def GetLangId(self):
        """
        Возвращает идентификатор языка.
        """
        return 0
    
    def CanUndo(self):
        """
        Возвращает признак возможности сделать откат изменений.
        """
        return False

    def CanRedo(self):
        """
        Возвращает признак возможности вернуть изменения после отката.
        """
        return False

    def CanPaste(self):
        return False

    def GetDocument(self):
        return self
        
    def GetEncoding(self):
        """
        Кодировка документа.
        """
        return 'utf-8'
        
    def GetSelectionStart(self):
        return -1

    def GetSelectionEnd(self):
        return -1

    def GetZoom(self):
        return 0
    
    def GetModify(self):
        """
        Признак измененного документа.
        """
        return False
    
    def GetCurrentPos(self):
        """
        Текущее положение курсора в документе.
        """
        return self._cursor
    
    def SetSelected(self, *arg, **kwarg):
        pass
    
    def GetIndentationGuides(self, *arg, **kwarg):
        pass
    
    def GetAutoComplete(self, *arg, **kwarg):
        return False
        
    def GetEdgeMode(self, *arg, **kwarg):
        pass
        
    def GetEOLModeId(self, *arg, **kwarg):
        pass
        
    def GetUseTabs(self, *arg, **kwarg):
        pass
        
    def GetLength(self, *arg, **kwarg):
        pass
        
    def GetViewEOL(self, *arg, **kwarg):
        pass
        
    def GetMarginWidth(self, *arg, **kwarg):
        pass
        
    def GetViewWhiteSpace(self, *arg, **kwarg):
        pass
        
    def ControlDispatch(self, *arg, **kwarg):
        pass
        
    def GetWrapMode(self, *arg, **kwarg):
        pass
        
    def PostPositionEvent(self, *arg, **kwarg):
        pass
        
    def DoOnIdle(self, *arg, **kwarg):
        pass
        
    def GetTitleString(self, *arg, **kwarg):
        return ''
        
    def CanCloseTab(self, *arg, **kwarg):
        return True
        
    def DoTabSelected(self, *arg, **kwarg):
        pass
        
    def DoTabClosing(self, *arg, **kwarg):
        pass        

    def SetTabLabel(self, *arg, **kwarg):
        pass        
    
    def DoDeactivateTab(self, *arg, **kwarg):
        pass
    
    def GetCaretLineVisible(self, *arg, **kwarg):
        return 0
    
    def GetBracePair(self, *arg, **kwarg):
        return -1, -1
    
    def GetAutoIndent(self, *arg, **kwarg):
        return False
    
    def IsBracketHlOn(self, *arg, **kwarg):
        return False
    
    def IsFoldingOn(self, *arg, **kwarg):
        return False
    
    def IsHighlightingOn(self, *arg, **kwarg):
        return False
    
    def OnTabMenu(self, *arg, **kwarg):
        pass
    
    def SetTabIndex(self, *arg, **kwarg):
        pass
    
    def GetEOLMode(self, *arg, **kwarg):
        return wx.stc.STC_EOL_LF
    
    def GetCurrentLineNum(self, *arg, **kwarg):
        return 0

    def SaveFile(self, *arg, **kwarg):
        return True


class AbsDesignerInterface:

    def __init__(self, designer, *arg, **kwarg):
        self.designer = designer
        
    def SetPointer(self, edt):
        """
        Устанавливает указатель на редактор свойств.
        """
        self.designer.SetPointer(edt)
        
    def CreateToolPanel(self, ObjectsInfo=None, parent=None, *arg, **kwarg):
        """
        Создаем панель инструментов.
        """
        return self.designer.createToolPanel(ObjectsInfo, parent, *arg, **kwarg)
        
    def GetEditorPanel(self, *arg, **kwarg):
        """
        Возвращает указатель на подложку редактора.
        """
        return self.designer.GetEditorPanel(*arg, **kwarg)

    def GetEditorFrame(self, *arg, **kwarg):
        """
        Возвращает указатель на главное окно редактора.
        """
        return self.designer.GetEditorFrame(*arg, **kwarg)
        
    def SelectObjId(self, iditem, *arg, **kwarg):
        return self.designer.SelectObjId(iditem, *arg, **kwarg)
    
    def SelectObj(self, *arg, **kwarg):
        return self.designer.SelectObj(*arg, **kwarg)


class FormEditorDoc(icPanelEditor.icBackgroundDocumentFrame, EditraDocumentInterface):
    """
    Простой дизайнер форм.
    """
    can_reload_designer = False
    
    def __init__(self, filename, component, parent, *arg, **kwarg):
        """
        Конструктор.

        :param filename: Имя файла документа.
        :param component: Ресурсное описание компонента.
        """
        icPanelEditor.icBackgroundDocumentFrame.__init__(self, parent, -1, component)
        self.designer = self

        if not filename:
            filename = 'Form editor document-%d' % self.GetId()
        EditraDocumentInterface.__init__(self, filename)


class DesignerPanel(icPanelEditor.icBackgroundDocumentFrame):

    def __init__(self, *arg, **kwarg):
        icPanelEditor.icBackgroundDocumentFrame.__init__(self, *arg, **kwarg)
        self.style_panel = None
        
    def set_style_panel(self, panel):
        """
        Устанавливает указатель на панель стилей.
        """
        self.style_panel = panel
        
    def get_style_panel(self):
        """
        Возвращет указатель на панель стилей.
        """
        return self.style_panel


class DesignerDoc(wx.Panel, EditraDocumentInterface, AbsDesignerInterface):
    """
    Стандартный дизайнер форм.
    """
    can_reload_designer = True
    
    def __init__(self, filename, component, parent, *arg, **kwarg):
        """
        Конструктор.

        :param filename: Имя файла документа.
        :param component: Ресурсное описание компонента.
        """
        from ic.PropertyEditor import icstylepanel
        self.default_panel_tool_cls = icstylepanel.icStyleToolPanel
        
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.top_panel_cls = None
        self.designer = DesignerPanel(self, -1, component)
        self.PageToolPanel()        
        self.LinkToPanel()
        self.sizer.Add(self.designer, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        if not filename:
            filename = 'Form editor document-%d' % self.GetId()
            
        AbsDesignerInterface.__init__(self, self.designer)
        EditraDocumentInterface.__init__(self, filename)

    def LinkToPanel(self):
        if self.top_panel:
            self.designer.set_style_panel(self.top_panel)
            self.top_panel.designer_panel = self.designer
        
    def SaveFile(self, *arg, **kwarg):
        self.designer.propertyTree.onSave(None)
        return True
        
    def PageToolPanel(self):
        """
        Создаем панель инструментов.
        """
        if self.designer and issubclass(self.designer.object.__class__, icdesignerinterface.icDesignerInterface):
            self.top_panel = self.designer.object.getToolPanel(self)
        else:
            self.top_panel = self.default_panel_tool_cls(self)
        
        if self.top_panel:
            self.sizer.Add(self.top_panel, 0, wx.GROW | wx.ALL, 1)
            self.top_panel.Show()
                
    def ReLoadDesigner(self, res):
        """
        Перегружает редактор.
        """
        # Удаляем старый
        self.designer.Hide()
        self.sizer.Remove(self.designer)
        self.designer.Destroy()
        # Создаем новый
        self.designer = DesignerPanel(self, -1, res)
        
        # Определяем класс панели инструментов
        if issubclass(self.designer.object.__class__, icdesignerinterface.icDesignerInterface):
            cls = self.designer.object.getToolPanelCls()
        else:
            cls = self.default_panel_tool_cls
        
        # Если класс панели инструментов изменился пересоздаем панель
        if self.top_panel and self.top_panel.__class__ != cls:
            # Удаляем из сайзера старую панель инструментов
            self.sizer.Remove(self.top_panel)
            self.top_panel.Destroy()
            # Создаем новую панель инструментов
            if cls:
                self.top_panel = cls(self)
                if self.top_panel:
                    self.sizer.Insert(0, self.top_panel, 0, wx.GROW | wx.ALL, 1)
        elif not self.top_panel and cls:
            # Создаем новую панель инструментов
            self.top_panel = cls(self)
            if self.top_panel:
                self.sizer.Insert(0, self.top_panel, 0, wx.GROW | wx.ALL, 1)

        # Востанавливаем связь панели инструментов с дизайнером
        self.LinkToPanel()
        
        # Вставляем панель дизайнера
        if self.top_panel:
            self.sizer.Insert(1, self.designer, 1, wx.EXPAND)
        else:
            self.sizer.Insert(0, self.designer, 1, wx.EXPAND)
            
        self.sizer.Layout()

    def GetTabImage(self):
        """
        Get the Bitmap to use for the tab

        :return: wx.Bitmap (16x16)
        """
        return common.imgDesigner


class EditraIDEInterface(icideinterface.icIDEInterface):
    """
    Интерфейс взаимодействия с IDE Editra.
    """
    formeditor_interface = DesignerDoc

    def __init__(self, IDEFrame=None):
        """
        Конструктор.

        :param IDEFrame: Указатель на главное окно IDE.
        """
        self._ide = IDEFrame
        self._ide.Bind(wx.EVT_CLOSE, self.onPostClose)

    def get_formeditor_interface(self):
        """
        Возвращает интерфейс документа.
        """
        return self.formeditor_interface
    
    def onPostClose(self, event):
        """
        Пост обработчик закрытия главного окна IDE.
        """
        log.info('Close IDE Editra')
        res_editor_win = wx.GetApp().GetActiveWindow()

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
        mgr = wx.GetApp().GetActiveWindow().GetFrameManager()
        pane = mgr.GetPane(DEFIS_PANE)
        if pane.name == DEFIS_PANE:
            return pane
        
    def openFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.

        :param res: Ресурсное описание.
        :param res_editor: Указатель на редактор ресурсов.
        """
        nb = self.getDocumentNotebook()
        res_name = ''
        if res_editor:
            res_name = res_editor.GetResFileName()
            if res_name:
                p, res_name = os.path.split(res_name)
        title = '%s (%s)' % (_('Designer'), res_name)
        bAddPage = True
        for i in range(nb.GetPageCount()):
            ctrl = nb.GetPage(i)
            if 'FormEditor' == ctrl.GetFileName():
                bAddPage = False
                if not self.formeditor_interface.can_reload_designer:
                    self.closeFile('FormEditor')
                    bAddPage = True
                else:
                    ctrl.ReLoadDesigner(res)
                    nb.SetPageText(i, title)
                    nb.setSelection(i)
                break
                
        if bAddPage:
            ctrl = self.formeditor_interface('FormEditor', component=res,
                                             parent=self.getIDEFrame())
            nb.GetTopLevelParent().Freeze()
            nb.pg_num += 1
            nb.control = ctrl
            nb.LOG('[ed_pages][event] Page Creation ID: %d' % ctrl.GetId())

            nb.control.Hide()
            nb.AddPage(nb.control, title)
            nb.control.Show()
            nb.GetTopLevelParent().Thaw()
            nb.setSelection(nb.GetSelection())
        
        # Связываем редактор форм с редактором ресурсов.
        if res_editor:
            ctrl.SetPointer(res_editor)
        return ctrl
            
    def addToolPanel(self, panel):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.

        :param panel: Наследник wx.Panel.
        :return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        pass

    def getDefaultEncoding(self):
        """
        Кодировка по умолчанию.
        """
        return icideinterface.DEFAULT_ENCODING

    def openFile(self, filename, bOpenInNewTab=True,
                 bEditRecentFiles=True, encoding='<Default Encoding>', bReadonly=False):
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
        if isinstance(filename, str):
            filename = str(filename)    # self.getDefaultEncoding())
        self.getIDEFrame().nb.OnDrop([filename])
        
    def closeFile(self, filename):
        """
        Выгружает файл.

        :type filename: C{string}
        :param filename: Имя файла.
        :rtype: C{bool}
        :return: Признак успешной выгрузки.
        """
        ipg = self._getOpenedFileIdx(filename)
        if ipg >= 0:
            nb = self.getDocumentNotebook()
            nb.DeletePage(ipg)
            nb.GoCurrentPage()
            ipg = self._getOpenedFileIdx(filename)
            
    def closeAllFiles(self):
        """
        Выгрузить все файлы.
        """
        self.getDocumentNotebook().CloseAllPages()

    def getAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        return [fl.replace('\\', '/') for fl in self.getDocumentNotebook().GetFileNames() or []]
    
    def insertEvtFuncToInterface(self, filename, func_name, function_body=None):
        """
        Вставляет в тело интерфейсного модуля заготовку функции с заданным именем.

        :type filename: C{string}
        :param filename: Имя файла.
        :type func_name: C{string}
        :param func_name: Имя функции.
        :type function_body: C{string}
        :param function_body: Тело функции.
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
                    funcTxt = icideinterface.METHOD_TEMPLATE % func_name
                    txt = txt[:indx]+funcTxt + '    ' + txt[indx:]
                # В противном случа добавляем в конец модуля.
                else:
                    funcTxt = icideinterface.FUNCTION_TEMPLATE % func_name
                    txt = txt + '\n' + funcTxt
                    
                self.setDocumentText(filename, txt)
        return False
        
    def isOpenedFile(self, filename):
        """
        Проверить открыт файл или нет.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        return self.getDocumentNotebook().HasFileOpen(filename)
        
    def setSelection(self, idx):
        """
        Устанавливает нужный файл в качестве текущего.
        """
        if self.getDocumentNotebook():
            self.getDocumentNotebook().setSelection(idx)
            self.getDocumentNotebook().GoCurrentPage()

    def _getOpenedFileIdx(self, filename):
        """
        Индекс открытого файла.

        :type filename: C{string}
        :param filename: Имя файла.
        :return: Индекс открытого файла или
            -1, если файл не открыт.
        """
        nb = self.getDocumentNotebook()
        alreadyopen = [nb.GetPage(i).GetFileName() for i in range(nb.GetPageCount())]
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
        filename = filename.replace('\\', '/')
        nb = self.getDocumentNotebook()
        for i in range(nb.GetPageCount()):
            ctrl = nb.GetPage(i)
            # log.debug(u'IDE. Is opened <%s> in page <%s>' % (filename, ctrl.GetFileName()))
            if (ctrl.GetFileName() or '').replace('\\', '/') == filename:
                self.setSelection(i)
                return True
                        
        return False

    def getDocumentNotebook(self):
        """
        Возвращает указатель на документы, организованные в 'записной книжке'.
        """
        return self.getIDEFrame().nb

    def getDocument(self):
        """
        Возвращает текущий документ.
        """
        return self.getDocumentNotebook().GetCurrentCtrl()
    
    def getDocumentObj(self, filegame):
        """
        Возвращает объект документа.

        :type filegame: C{string}
        :param filegame: Имя файла.
        """
        docs = self.getDocumentNotebook().GetTextControls()
        for doc in docs:
            if doc.GetFileName().replace('\\', '/') == filegame:
                return doc
    
    def getDocumentText(self, filename):
        """
        Возвращает текст документа.

        :type filename: C{string}
        :param filename: Имя файла.
        """
        return self.getDocument().GetText()
                
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
        doc = self.getDocumentObj(filename)
        if doc:
            return doc.getModify()
        
    def goToFunc(self, func_name, filename=None):
        """
        Переход на нужную функцию.

        :param func_name: Имя функции.
        :param filename: Имя файла.
        """
        if not filename:
            doc = self.getDocument()
        else:
            doc = self.getDocumentObj(filename)
        try:
            txt = doc.GetText()
            for pos, r in enumerate(txt.split('\n')):
                if r.find('def ' + func_name) >= 0:
                    doc.MarkerAdd(pos, 0)
                    doc.GotoLine(pos)
                    return pos
        except:
            log.fatal(u'Invalid document type: doc.GetText() - failed')
        return None

    def getMainPanel(self):
        """
        Гравная панель IDE.
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
        fl = filename.replace('\\', '/')
        doc = self.getDocumentObj(fl)
        if doc:
            ret = doc.SetText(txt)
            self.selectFile(fl)
            return ret 
        return False
        
    def showToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        pass

    def getIDEFrame(self):
        """
        Возвращает главное окно ide.
        """
        return self._ide
