#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса редактора модулей питона.
"""

# Подключение библиотек
import string
import keyword
import wx
from wx import stc
from ic.components import icframe

from ic.imglib import common
from ic.dlg.msgbox import MsgBox
from ic.components.icwidget import icEvent

_PyCard = u'Скрипты (*.py)|*.py|All files (*.*)|*.*'

# Основные константы
if wx.Platform == '__WXMSW__':
    faces = {'times': 'Times New Roman',
             'mono': 'Courier New',
             'helv': 'Arial',
             'other': 'Courier',
             'size': 10,
             'size2': 8,
             }
else:
    faces = {'times': 'Times',
             'mono': 'Courier',
             'helv': 'Helvetica',
             'other': 'new century schoolbook',
             'size': 12,
             'size2': 10,
             }


__version__ = (0, 0, 1, 2)


class icPyEditor(stc.StyledTextCtrl):
    """
    Класс редактора модулей питона.
    """
    
    def SetReadOnlyMode(self, bReadOnly=True):
        """
        Устанавливает режим 'только для чтения'.
        """
        self.isReadOnly = bReadOnly

    def isReadOnlyMode(self):
        """
        """
        return self.isReadOnly
        
    def __init__(self, Parent_, id, ModuleText_=None, ModuleName_=None, pos=(-1, -1), size=(-1, -1)):
        """
        Конструктор.
        @param Parent_: Родительское окно.
        @parent ModuleText_: Имя модуля для редактирования.
        """
        stc.StyledTextCtrl.__init__(self, Parent_, id, pos, size, style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.BORDER_NONE)

        # Свойства
        self.type = 'PyEditor'
        self.parent = Parent_
        self._ModuleName = ModuleName_
        self.IsChanged = False
        self.SetReadOnlyMode(False)
        self._Breakpoints = []      # список точек останова, номера строк
        # параметры маркеров точек останова
        self.icBreakpointMarker = 8
        self.icBreakpointBackgroundMarker = 9
        # Горячие клавиши редактора
        # Масштабирование
        self.CmdKeyAssign(ord('+'), stc.STC_SCMOD_ALT, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('-'), stc.STC_SCMOD_ALT, stc.STC_CMD_ZOOMOUT)
        
        # Установка лексического анализа
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, string.join(keyword.kwlist))

        self.SetProperty('fold', '1')
        self.SetProperty('tab.timmy.whinge.level', '1')
        self.SetMargins(0, 0)

        # Не видеть пустые пробелы в виде точек
        self.SetViewWhiteSpace(False)

        # Установить ширину 'таба'
        # Indentation and tab stuff
        self.SetIndent(4)                 # Proscribed indent size for wx
        self.SetIndentationGuides(True)   # Show indent guides
        self.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)          # Tab key indents
        self.SetTabWidth(4)               # Proscribed tab size for wx
        self.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Установка поле для захвата маркеров папки
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(1, True)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(1, 25)
        self.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,  'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,  'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,    'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Маркеры режима отладки
        self.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        self.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')
        # этот код нужен только для того чтобы установить маску точки останова
        self.MarkerAdd(0, self.icBreakpointMarker)
        self.mask = self.MarkerGet(0)
        self.MarkerDelete(0, self.icBreakpointMarker)
        # ---------------------------------------------

        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI, id=self.GetId())
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick, id=self.GetId())

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        self.StyleClearAll()

        # Following style specs only indicate differences from default.
        # The rest remains unchanged.

        # Line numbers in margin
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, 'back:#99A9C2,face:Arial Narrow,size:8')
    
        # Highlighted brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        # Indentation guide
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, 'fore:#CDCDCD')
        # Python styles
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        # Comments
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,  'fore:#008000')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000')
        # Numbers
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        # Strings and characters
        self.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        self.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        # Triple quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#000080')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#000080')
        # Class names
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#000000,bold')
        # Operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # Identifiers. I leave this as not bold because everything seems
        # to be an identifier if it doesn't match the above criterae
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        # Caret color
        self.SetCaretForeground('BLUE')
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        # ---------- Внутренние атрибуты ------------------------
        self.finddata = wx.FindReplaceData()
        
        # ---------- Обработчики событий ------------------------
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeft)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWin)

        #   Поиск в тексте модуля
        self.Bind(wx.EVT_COMMAND_FIND, self.OnFind)
        self.Bind(wx.EVT_COMMAND_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_COMMAND_FIND_CLOSE, self.OnFindClose)
        
        if ModuleText_ is not None:
            # Установить текст в окне редактора
            self.SetText(ModuleText_)

    def Clear(self):
        """
        Чистит содержимое редактора.
        """
        self.ClearAll()

    def SetInsertionPoint(self, pos):
        """
        """
        self.SetCurrentPos(pos)

    def ShowPosition(self, pos):
        """
        """
        self.GotoPos(pos)

    def GetLastPosition(self):
        """
        """
        return self.GetLength()

    def GetRange(self, start, end):
        """
        """
        return self.GetTextRange(start, end)

    def GetSelection(self):
        """
        """
        return self.GetAnchor(), self.GetCurrentPos()

    def SetSelection(self, start, end):
        """
        """
        self.SetSelectionStart(start)
        self.SetSelectionEnd(end)

    def OnHelpFind(self):
        """
        """
        self.finddlg = wx.FindReplaceDialog(self, self.finddata, 'Find',
                                            wx.FR_NOUPDOWN |
                                            wx.FR_NOMATCHCASE |
                                            wx.FR_NOWHOLEWORD)
        self.finddlg.Show(True)

    def OnFind(self, event):
        """
        Поиск подстроки в тексте.
        """

        end = self.GetLastPosition()
        textstring = self.GetRange(0, end).lower()
        start = self.GetSelection()[1]
        findstring = self.finddata.GetFindString().lower()
        loc = textstring.find(findstring, start)
        if loc == -1 and start != 0:
            # string not found, start at beginning
            start = 0
            loc = textstring.find(findstring, start)
        if loc == -1:
            dlg = wx.MessageDialog(self, u'Find String Not Found',
                                   u'Find String Not Found in Module',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if self.finddlg:
            if loc == -1:
                self.finddlg.SetFocus()
                return
            else:
                self.finddlg.Destroy()

        self.ShowPosition(loc)
        self.SetSelection(loc, loc + len(findstring))

    def OnFindNext(self, event):
        """
        Продолжает поиск (по Ctrl-G)
        """
        
        if self.finddata.GetFindString():
            self.OnFind(event)
        else:
            self.OnHelpFind(event)

    def OnFindClose(self, event):
        event.GetDialog().Destroy()

    # обработчики событий
    def OnKeyPressed(self, event):
        """
        Обработчик нажатия клавиши на объекте редактора.
        """
        # Определить нажатую клавишу
        key = event.GetKeyCode()

        # Обрабатываем Ctrl-F - поиск подстроки в тексте
        if event.ControlDown() and key in [ord('f'), ord('F'), ord('А'), ord('а')]:
            self.OnHelpFind()

        # Обрабатываем Ctrl-G - продолжить поиск подстроки в тексте
        if event.ControlDown() and key in [ord('п'), ord('П'), ord('g'), ord('G')]:
            self.OnFindNext(event)
        
        if self.isReadOnlyMode() and key not in [wx.WXK_UP, wx.WXK_DOWN, wx.WXK_ESCAPE, wx.WXK_HOME, wx.WXK_END,
                                                 wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN]:
            return
        
        # Если всплывающие подсказки были активны, то деактивировать их
        if self.CallTipActive():
            self.CallTipCancel()

        # Если нажат пробел и 'CTRL', то ...
        if key == wx.WXK_SPACE and event.ControlDown():
            pos = self.GetCurrentPos()
            # а если еще нажат 'SHIFT', то высплывающая подсказка
            if event.ShiftDown():
                self.CallTipSetBackground('yellow')
                self.CallTipShow(pos, 'param1,param2')
            # Окно поиска ключевых слов
            else:
                kw = keyword.kwlist[:]
                # Пересортировать - Python sorts are case sensitive
                kw.sort()
                self.AutoCompSetIgnoreCase(False)  # so this needs to match
                self.AutoCompShow(0,string.join(kw))
        # Если нажата клавиша 'PageUp'+'CTRL' или 'PageDown'+'CTRL',
        # то это команда для сворачивания/разворачивания текущей папки
        elif (key == wx.WXK_PRIOR or key == wx.WXK_NEXT) and event.ControlDown():
            # Определить текущую линию
            cur_line = self.GetCurrentLine()
            # Переключить состояние папки на этой линии (свернута/развернута)
            self.ToggleFold(cur_line)
        elif key == 83 and event.ControlDown():
            self.parent.Save()
        else:
            try:
                self.parent.OnKeyDown(event)
            except:
                pass

            event.Skip()

    def OnLeaveWin(self, evt):
        """
        """
        evt.Skip()
        
        try:
            self.parent.OnLeaveWin(evt)
        except:
            pass
            
    def OnMouseLeft(self, evt):
        """
        """
        evt.Skip()
        
        try:
            self.parent.OnMouseLeft(evt)
        except:
            pass

    def OnKillFocus(self, evt):
        """
        """
        try:
            self.parent.OnKillFocus(evt)
        except:
            pass
        
        evt.Skip()

    def OnUpdateUI(self, event):
        """
        Проверка для согласованых скрепок - check for matching braces.
        """
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # Проверить до - check before
        if charBefore and chr(charBefore) in '[]{}()' and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # Проверить после - check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in '[]{}()' and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def OnMarginClick(self, event):
        """
        Обработчик щелчка мыши при развороте/свертывании папки.
        """
        # fold and unfold as needed
        if event.GetMargin() == 2:
            if event.GetShift() and event.GetControl():
                self.FoldAll()
            else:
                line_clicked = self.LineFromPosition(event.GetPosition())
                if self.GetFoldLevel(line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if event.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self.Expand(line_clicked, True, True, 1)
                    elif event.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self.Expand(line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
                            self.Expand(line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(line_clicked)
        elif event.GetMargin() == 1:
            # Добавление точки останова
            line_clicked = self.LineFromPosition(event.GetPosition())+1
            # проверить существует ли здесь точка останова
            num_str = self.MarkerNext(line_clicked-1, self.mask)
            if num_str+1 == line_clicked:
                # есть точка останова, удалим ее
                self.MarkerDelete(line_clicked-1, self.icBreakpointMarker)
                self.MarkerDelete(line_clicked-1, self.icBreakpointBackgroundMarker)
            else:
                # нет точки останова, установить ее
                self.MarkerAdd(line_clicked-1, self.icBreakpointMarker)
                self.MarkerAdd(line_clicked-1, self.icBreakpointBackgroundMarker)
        event.Skip()
                        
    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break;

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line += 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line += 1

        return line

    # --- Свойства ---
    def GetModuleName(self):
        return self._ModuleName

    def SetModuleName(self, NewName_):
        self._ModuleName = NewName_
        
    def GetBreakpoints(self):
        """
        Получить список точек останова
        """
        self._Breakpoints = []
        num_str = 0
        num_str = self.MarkerNext(num_str, self.mask)
        if not(num_str < 0):
            self._Breakpoints.append(num_str+1)
        while not(num_str < 0):
            num_str = num_str+1
            num_str = self.MarkerNext(num_str, self.mask)
            if not(num_str < 0):
                self._Breakpoints.append(num_str+1)

    def SetBreakpoints(self, PointList):
        """
        Расставить точки останова
        """
        if isinstance(PointList, list):
            self._Breakpoints = PointList
            try:
                for LineNo_ in self._Breakpoints:
                    # Отобразить маркер
                    self.MarkerAdd(LineNo_-1, self.icBreakpointMarker)
                    self.MarkerAdd(LineNo_-1, self.icBreakpointBackgroundMarker)
            except:
                self.MarkerDeleteAll()
                self._Breakpoints = []


class icPyEditorFrame(icframe.icFrame):
    """
    Простой редактор исходников на Python.
    """
    
    def __init__(self, parent, component={}, text=None, logType=0, evalSpace={}):
        """
        Конструктор для редактора питоновских текстов.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type txt: C{string}
        @param txt: Текст.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}

        """
        icframe.icFrame.__init__(self, parent, wx.NewId(), component, logType, evalSpace)
        
        self.SetIcon(common.icoPyEditor)
        editor_id = wx.NewId()
                
        if text is None:
            self.editor.IsFirstLoad = False
        else:
            self.editor = icPyEditor(self, editor_id, text)
            self.editor.IsFirstLoad = True
        
        self.toolbar = wx.ToolBar(self, wx.NewId(), style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_NODIVIDER)
        self.toolbar.SetToolBitmapSize(wx.Size(16, 16))
        
        id = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgOpen, shortHelpString='Open', id=id)
        self.Bind(wx.EVT_TOOL, self.OnLoad, id=id)
            
        id = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgSave, shortHelpString='Save (Ctrl-S)', id=id)
        self.Bind(wx.EVT_TOOL, self.OnSave, id=id)
            
        id = wx.NewId()
        self.toolbar.AddTool(bitmap=common.imgSaveAs, shortHelpString='SaveAs', id=id)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, id=id)
        
        self.toolbar.Realize()
        self.SetToolBar(self.toolbar)
                
        self.Bind(stc.EVT_STC_CHANGE, self.OnChangeText, id=editor_id)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
            
        self.editor.IsChanged = False
        self.editor.closed = False
        
    def OnChangeText(self, evt):
        """
        Обрабатывает изменения текста в редакторе.
        """
        
        if not self.editor.IsFirstLoad:
            if self.editor.GetModuleName() is None:
                self.editor.SetModuleName('default.py')
                
            self.SetTitle(u'Редактор (%s)*' % self.editor.GetModuleName())
            self.editor.IsChanged = True
        
        self.editor.IsFirstLoad = False
        self.editor.closed = False

    def OnClose(self, evt):
        """
        Обрабатываем закрытие окна.
        """
        if not self.editor.closed:
            
            self.editor.closed = True
            
            if self.editor.IsChanged and MsgBox(self, u'Файл %s был изменен. Сохранить?' % self.editor.GetModuleName(),
                                                style=wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
                self.editor.IsChanged = False
                self.Save()
        
        evt.Skip()
        
    def OnLoad(self, evt):
        """
        Загружает файл.
        """
        evt.Skip()
        
        if self.editor.IsChanged and MsgBox(self, u'Файл %s был изменен. Сохранить?' % self.editor.GetModuleName(),
                                            style=wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
            self.Save()
                            
        dlg = wx.FileDialog(self, u'Выбери имя файла', '', '', _PyCard, wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            f = open(path)
            txt = f.read()
            f.close()
            
            self.editor.IsFirstLoad = True
            self.editor.SetText(txt)
            self.editor.IsFirstLoad = True
            self.editor.SetModuleName(path)
            self.SetTitle(u'Редактор (%s)' % path)
                            
        self.editor.IsChanged = False

    def Save(self, path=None):
        """
        Сохраняет файл.
        
        @type path: C{string}
        @param path: Путь до файла.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """
        try:
            if path is None:
                path = self.editor.GetModuleName()
                
            file = open(path, 'wb')
            file.write(str(self.editor.GetText()))
            file.close()
            self.SetTitle(u'Редактор (%s)' % path)
            self.editor.IsChanged = False
            
        except:
            MsgLastError(None, u'Exception in Save ...')
            return False
        
        return True
    
    def OnSave(self, evt):
        """
        """
        if self.editor.GetModuleName() in [None, '']:
            self.OnSaveAs(evt)
        else:
            self.Save(self.editor.GetModuleName())
            
        evt.Skip()
        
    def OnSaveAs(self, evt):
        """
        Обрабатывает нажатие кнопки 'сохранить как'.
        """
        
        dlg = wx.FileDialog(self, u'Выбери имя файла', '', '', _PyCard, wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            self.Save(path)
            self.editor.SetModuleName(path)
            self.SetTitle(u'Редактор (%s)' % path)

        evt.Skip()


class icPyEditorDlg(icEvent, wx.Dialog):
    """
    """

    def __init__(self, parent, text, pos=(-1, -1), size=(-1, -1), style=wx.DEFAULT_DIALOG_STYLE):
        """
        """
        icEvent.__init__(self)
        wx.Dialog.__init__(self, parent, wx.NewId(), u'Редактирование скрипта',
                           pos, (-1, -1), style)
                            
        editor_id = wx.NewId()
        self.editor = icPyEditor(self, editor_id, text, pos=(0, 0), size=(200, 200))

        self.SetSize(size)
        self.text = text
        self.bEndModal = False
        
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(stc.EVT_STC_CHANGE, self.OnChangeText, id=editor_id)

    def OnLeaveWin(self, evt):
        """
        """
        return

    def OnChangeText(self, evt):
        """
        """
        evt.Skip()
        
    def OnKeyDown(self, evt):
        """
        """
        key = evt.GetKeyCode()
        evt.Skip()
        
        if key == wx.WXK_ESCAPE:
            if not self.bEndModal:
                self.EndModal(wx.ID_OK)
                self.bEndModal = True
        
    def OnKillFocus(self, evt):
        """
        """
        evt.Skip()
        
        if not self.bEndModal:
            self.EndModal(wx.ID_OK)
            self.bEndModal = True

                
# -------------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    
    f = open('icResTree.py')
    res = f.read()
    f.close()

    dlg = icPyEditorDlg(None, '123weee', (20, 20), (400, 500), style=wx.THICK_FRAME)
    ret = dlg.ShowModal()
    
    if ret == wx.ID_OK:
        print('Ok!')
    else:
        print('Cancel')
        
    app.MainLoop()
