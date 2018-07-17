#!/usr/bin/env python
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

__version__ = (0, 0, 2, 2)

_ = wx.GetTranslation

DEFIS_PANE = 'DefisPanel'

# Шаблоны
interfaceTemplate = '''
    def %s(self, event):
        return None
'''

resmoduleTemplate = '''
def %s(obj, event):
    return None
'''

DEFAULT_ENCODING = 'utf-8'


class EditraDocumentInterface(object):
    """
    Интерфейс документа для IDE Editra.
    """

    def __init__(self, filename, *arg, **kwarg):
        """
        Конструктор.
        @param filename: Имя файла документа.
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
        return self.designer.CreateToolPanel(ObjectsInfo, parent, *arg, **kwarg)
        
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
        @param filename: Имя файла документа.
        @param component: Ресурсное описание компонента.
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
        @param filename: Имя файла документа.
        @param component: Ресурсное описание компонента.
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
        self.designer.propertyTree.OnSave(None)
        return True
        
    def PageToolPanel(self):
        """
        Создаем панель инструментов.
        """
        if self.designer and issubclass(self.designer.object.__class__, icdesignerinterface.icDesignerInterface):
            self.top_panel = self.designer.object.GetToolPanel(self)
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
            cls = self.designer.object.GetToolPanelCls()
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
        @return: wx.Bitmap (16x16)
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
        @param IDEFrame: Указатель на главное окно IDE.
        """
        self._ide = IDEFrame
        self._ide.Bind(wx.EVT_CLOSE, self.OnCloseIC)

    def get_formeditor_interface(self):
        """
        Возвращает интерфейс документа.
        """
        return self.formeditor_interface
    
    def OnCloseIC(self, event):
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
        
    def OpenFormEditor(self, res, res_editor=None, *arg, **kwarg):
        """
        Открыть редактор форм для редактирования ресурса.
        @param res: Ресурсное описание.
        @param res_editor: Указатель на редактор ресурсов.
        """
        nb = self.GetDocumentNotebook()
        res_name = ''
        if res_editor:
            res_name = res_editor.GetResFileName()
            if res_name:
                p, res_name = os.path.split(res_name)
        title = '%s (%s)' % (_('Designer'), res_name)
        bAddPage = True
        for i in xrange(nb.GetPageCount()):
            ctrl = nb.GetPage(i)
            if 'FormEditor' == ctrl.GetFileName():
                bAddPage = False
                if not self.formeditor_interface.can_reload_designer:
                    self.CloseFile('FormEditor')
                    bAddPage = True
                else:
                    ctrl.ReLoadDesigner(res)
                    nb.SetPageText(i, title)
                    nb.SetSelection(i)
                break
                
        if bAddPage:
            ctrl = self.formeditor_interface('FormEditor', component=res,
                                             parent=self.GetIDEFrame())
            nb.GetTopLevelParent().Freeze()
            nb.pg_num += 1
            nb.control = ctrl
            nb.LOG('[ed_pages][evt] Page Creation ID: %d' % ctrl.GetId())

            nb.control.Hide()
            nb.AddPage(nb.control, title)
            nb.control.Show()
            nb.GetTopLevelParent().Thaw()
            nb.SetSelection(nb.GetSelection())
        
        # Связываем редактор форм с редактором ресурсов.
        if res_editor:
            ctrl.SetPointer(res_editor)
        return ctrl
            
    def AddToolPanel(self, Panel_):
        """
        Добавить панель в нотебук инструментов/палитры инструментов.
        @param Panel_: Наследник wx.Panel.
        @return: Возвращает указатель на страницу нотебука(наследник drSidePanel),
            которая соответствует этой панели.
        """
        pass

    def getDefaultEncoding(self):
        """
        Кодировка по умолчанию.
        """
        return DEFAULT_ENCODING

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
        if isinstance(filename, str):
            filename = unicode(filename, self.getDefaultEncoding())
        self.GetIDEFrame().nb.OnDrop([filename])
        
    def CloseFile(self, fileName):
        """
        Выгружает файл.
        @type fileName: C{string}
        @param fileName: Имя файла.
        @rtype: C{bool}
        @return: Признак успешной выгрузки.
        """
        ipg = self._getOpenedFileIdx(fileName)
        if ipg >= 0:
            nb = self.GetDocumentNotebook()
            nb.DeletePage(ipg)
            nb.GoCurrentPage()
            ipg = self._getOpenedFileIdx(fileName)
            
    def CloseAllFiles(self):
        """
        Выгрузить все файлы.
        """
        self.GetDocumentNotebook().CloseAllPages()

    def GetAlreadyOpen(self):
        """
        Возвращает список имен открытых файлов.
        """
        return [fl.replace('\\', '/') for fl in self.GetDocumentNotebook().GetFileNames() or []]
    
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
                    txt = txt[:indx]+funcTxt + '    ' + txt[indx:]
                # В противном случа добавляем в конец модуля.
                else:
                    funcTxt = resmoduleTemplate % funcName
                    txt = txt + '\n' + funcTxt
                    
                self.SetDocumentText(fileName, txt)
        return False
        
    def IsOpenedFile(self, fileName):
        """
        Проверить открыт файл или нет.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        return self.GetDocumentNotebook().HasFileOpen(fileName)
        
    def SetSelection(self, i):
        """
        Устанавливает нужный файл в качестве текущего.
        """
        if self.GetDocumentNotebook():
            self.GetDocumentNotebook().SetSelection(i)
            self.GetDocumentNotebook().GoCurrentPage()

    def _getOpenedFileIdx(self, fileName):
        """
        Индекс открытого файла.
        @type fileName: C{string}
        @param fileName: Имя файла.
        @return: Индекс открытого файла или
            -1, если файл не открыт.
        """
        nb = self.GetDocumentNotebook()
        alreadyopen = [nb.GetPage(i).GetFileName() for i in xrange(nb.GetPageCount())]
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
        fileName = fileName.replace('\\', '/')
        nb = self.GetDocumentNotebook()
        for i in xrange(nb.GetPageCount()):
            ctrl = nb.GetPage(i)
            # log.debug(u'IDE. Is opened <%s> in page <%s>' % (fileName, ctrl.GetFileName()))
            if (ctrl.GetFileName() or '').replace('\\', '/') == fileName:
                self.SetSelection(i)
                return True
                        
        return False

    def GetDocumentNotebook(self):
        """
        Возвращает указатель на документы, организованные в 'записной книжке'.
        """
        return self.GetIDEFrame().nb

    def GetDocument(self):
        """
        Возвращает текущий документ.
        """
        return self.GetDocumentNotebook().GetCurrentCtrl()
    
    def GetDocumentObj(self, fileName):
        """
        Возвращает объект документа.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        docs = self.GetDocumentNotebook().GetTextControls()
        for doc in docs:
            if doc.GetFileName().replace('\\', '/') == fileName:
                return doc
    
    def GetDocumentText(self, fileName):
        """
        Возвращает текст документа.
        @type fileName: C{string}
        @param fileName: Имя файла.
        """
        return self.GetDocument().GetText()
                
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
        doc = self.GetDocumentObj(fileName)
        if doc:
            return doc.GetModify()
        
    def GoToFunc(self, funcname, fileName=None):
        """
        Переход на нужную функцию.
        @param funcname: Имя функции.
        @param fileName: Имя файла.
        """
        if not fileName:
            doc = self.GetDocument()
        else:
            doc = self.GetDocumentObj(fileName)
        try:
            txt = doc.GetText()
            for pos, r in enumerate(txt.split('\n')):
                if r.find('def '+funcname) >= 0:
                    doc.MarkerAdd(pos, 0)
                    doc.GotoLine(pos)
                    return pos
        except:
            log.fatal(u'Invalid document type: doc.GetText() - failed')

    def GetMainPanel(self):
        """
        Гравная панель IDE.
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
        fl = fileName.replace('\\', '/')
        doc = self.GetDocumentObj(fl)
        if doc:
            ret = doc.SetText(txt)
            self.SelectFile(fl)
            return ret 
        return False
        
    def ShowToolNotebook(self):
        """
        Показать нотебук инструменнтов/палитры компонентов.
        """
        pass

    def GetIDEFrame(self):
        """
        Возвращает главное окно ide.
        """
        return self._ide
