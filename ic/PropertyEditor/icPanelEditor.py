#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Панель редактора форм.
"""

import wx
from ic.dlg.msgbox import MsgBox
import ic.components.icdialog as icdialog
import ic.components.icfont as icfont
import ic.components.sizers.icgridbagsizer as icgridbagsizer
import ic.components.icwidget as icwidget
import ic.utils.util as util
from ic.utils.util import icSpcDefStruct
from ic.components.icwidget import icBase, icParentShapeType
import ic.PropertyEditor.icPanelTool as icPanelTool
from ic.kernel import io_prnt
from .images import editorimg
from ic.log import log
from ic.components import icwxpanel

_ = wx.GetTranslation

__version__ = (1, 0, 1, 2)

# Локализация сообщений
SPC_IC_BACKGROUND = {'name': '__EditorBackground__',
                     'type': 'Background',
                     'position': (-1, -1),
                     'size': (-1, -1),
                     'title': _('EditorTitle')}

# Указатель на панель инструментов
icPanelToolBuff = None
PARENT_CURSOR_COLOR = (190, 0, 0)


def SetPanelToolBuff(frmTool):
    """
    Сохраняет ссылку на панель инструментов в буфере.
    """
    global icPanelToolBuff
    icPanelToolBuff = frmTool


def GetPanelToolBuff():
    """
    Возвращает ссылку на панель инструментов из буфера.
    """
    return icPanelToolBuff


class icBackground(object):
    """
    Базовый класс для всех подложек редактора форм.
    """

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={}):
        """
        Конструктор для создания объекта icBoxSizer.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        icSpcDefStruct(SPC_IC_BACKGROUND, component)
        # Список всех редактируемых объектов
        self.container = []
        # Текущий выбранный объект
        self.selectedObj = None
        # Родитель выбранного объекта
        self.prntSelObj = None
        # Признак захвата объекта для переноса
        self.bDrag = False

        # Признак захвата маркера для изменеия размеров объекта
        self.bDragLT = False
        self.bDragRT = False
        self.bDragRB = False
        self.bDragLB = False
        self.bDragL = False
        self.bDragR = False
        self.bDragT = False
        self.bDragB = False

        #
        self.bRedrawCursor = True
        self.bRedraw = True
        # Размер маркероа выбранного объекта
        self.markerSize = 4
        # Указатель на редактор свойств (класс icResourceEditor)
        self.propertyTree = None
        # Указатель на подложку редактора, где распологаются редактируемые компоненты
        self.editorPanel = None
        # Указатель на главное окно редактора
        self.editorFrame = None
        # Указатель на панель инструментов
        self.toolpanel = None
        #
        self.bBlockDestroy = False
        self.timer = None
        
    def AddObject(self, obj):
        """
        Добавляет объект в коллекцию редактируемых объектов.
        @param obj: Объект, который будет редактироваться.
        """
        # Для того, чтобы можно было определить ресурсное описание компонента от
        # которого приходять сообщения в обработчик, генерируем для каждого редактируемого
        # объекта уникальное имя. В обработчике кроме имени (по ф-ии GetName) другой
        # идентифицирующей информации получить не получается.
        try:
            nm = obj.GetName()
            id = str(obj.resource['__item_id'])
            name = '%s::%s' % (nm, id)
            obj.SetName(name)
        except:
            io_prnt.outLastErr('SetName ERROR')

        self.container.append(obj)
        obj.editorBackground = self
        try:
            obj.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
            obj.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
            obj.Bind(wx.EVT_MOTION, self.OnMove)
            obj.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            obj.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            obj.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
            obj.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownObj)
            obj.Bind(wx.EVT_CHAR, self.OnChar)
        except:
            pass

    def AddObjectToRes(self, prnt, toggleType, pos=(0, 0), size=(-1, -1)):
        """
        Добавляет объект определенного типа в ресурсное описание в определенное место с
        определенными размерами.
        @type prnt: C{wx.Window}
        @param prnt: Компонент ресурса, куда добавляется новый объект.
        @type toggleType: C{string}
        @param toggleType: Тип добавляемого объекта.
        @type pos: C{wx.Point}
        @param pos: Позиция, где объект будет распологаться.
        @type size: C{wx.Size}
        @param size: Размеры объекта.
        """
        if not prnt:
            prnt = self.GetEditorPanel()
            # В случае диалога, берется иденификатор родителя панели. Т.к. ресурса у
            # графической диалоговой панели нет
            if issubclass(prnt.__class__, icBackgroundPanel):
                item_id = prnt.editorFrame.resource['__item_id']
            else:
                item_id = prnt.resource['__item_id']
        else:
            item_id = prnt.resource['__item_id']

        if issubclass(prnt.__class__, icgridbagsizer.icGridBagSizer):
            row, col = prnt.GetCellInPoint(pos)
            if row >= 0 and col >= 0 and not prnt.FindCell(row, col):
                pos = (row, col)
            else:
                MsgBox(None, u'В ячейку сайзера (row=%s, col=%s) нельзя добавить выбранный компонент' % (row, col))
                pos = None
            
        if pos and self.propertyTree.tree.AddTypeItem(item_id, toggleType, pos, size):
            return True
        
        return False

    def convToBGR(self, obj=None):
        """
        Конвертирует из координат на родительском окне в координаты подложки.
        @type pos: C{wx.Point}
        @parma pos: Координаты на родительском окне.
        """
        if not obj:
            obj = self.selectedObj

        if obj:
            x, y = obj.GetPosition()
            obj = obj.GetParent()
 
            while obj and obj.GetName() != '__EditorBackground__':
                pos = obj.GetPosition()
                x = x + pos.x
                y = y + pos.y
                obj = obj.GetParent()
                
        return wx.Point(x, y)

    def ChangeObjProperty(self, obj, property, value):
        """
        Изменяет заданное свойство объекта в графическом редакторе.
        @param obj: Объекта, у которого меняется свойство.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @rtype: C{bool}
        @return: Признак успешного изменения свойства.
        """
        ret = True
        if obj:
            res_mngr = obj.GetEditorResourceManager()
            if property == 'position':
                obj.SetPosition(value)
                obj.position = value
            elif property == 'span':
                obj.span = value
            elif property == 'size':
                obj.SetSize(value)
                obj.size = value
            elif property == 'style':
                obj.SetWindowStyleFlag(value)
            elif property == 'font':
                font = icfont.icFont(value)
                obj.SetFont(font)
            elif property == 'show':
                try:
                    bShow = int(value)
                    obj.Show(bShow)
                except:
                    pass
            elif property == 'backgroundColor':
                obj.SetBackgroundColour(value)
            elif property == 'foregroundColor':
                obj.SetForegroundColour(value)
            elif property == 'flag':
                old = obj.flag
                obj.flag = value
                # Востанавливаем размер компонентов
                if wx.EXPAND & old and not wx.EXPAND & value:
                    sx, sy = self.GetPointer().notebook.GetPropertyEditor().GetProperty('size')
                    if sx == -1:
                        sx = 75
                    obj.SetSize((sx, sy))
            elif property == 'proportion':
                if obj.proportion == 1 and value != 1:
                    sx, sy = self.GetPointer().notebook.GetPropertyEditor().GetProperty('size')
                    if sy == -1:
                        sy = 23
                    obj.SetSize((sx, sy))
                obj.proportion = value
            elif property == 'border':
                obj.border = value
            elif res_mngr:
                ret = res_mngr.SetObjProperty(obj, property, value)
            else:
                ret = False

            if property in ['position', 'size', 'span', 'flag',
                            'proportion', 'border'] and not obj.IsSizer():
                self.SelectObj(obj, bDrag=False)
                self.ReSizer()
        else:
            ret = False
        
        return ret
        
    def ChangeItemProperty(self, iditem, property, value):
        """
        Изменяет заданное свойство объекта в графическом редакторе.
        @type iditem: C{int}
        @param iditem: Идентификатор ресусного описания объекта.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @rtype: C{bool}
        @return: Признак успешного изменения свойства.
        """
        # По идентификатору находим объкт, у которого меняется свойство
        for obj in self.container:
            try:
                if obj.resource['__item_id'] == iditem and obj.resource['type'] != 'Background':
                    if self.ChangeObjProperty(obj, property, value):
                        return True
            except:
                io_prnt.outLastErr('ChangeItemProperty ERROR')
            
        return False

    def ChangeSelItemProperty(self, property, value):
        """
        Изменяет заданное свойство текущего объекта в графическом редакторе.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @rtype: C{bool}
        @return: Признак успешного изменения свойства.
        """
        # По идентификатору находим объкт, у которого меняется свойство
        ret = False
        try:
            if self.ChangeObjProperty(self.selectedObj, property, value):
                ret = True
                self.ReSizer()
        except:
            io_prnt.outLastErr('ChangeSelObjProperty ERROR')
            ret = False
        return ret

    def ChangeResItemProperty(self, iditem, property, value, bRefresh=True):
        """
        Изменяет заданное свойство ресурсного описания объекта.
        @type iditem: C{int}
        @param iditem: Идентификатор ресурса, у которого изменяем свойство.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @type bRefresh: C{bool}
        @param bRefresh: Признак обновления редактора свойств.
        """
        return self.propertyTree.tree.ChangePropertyId(iditem, property, value, bRefresh)
    
    def ChangeResProperty(self, obj, property, value, bRefresh=True):
        """
        Изменяет заданное свойство ресурсного описания объекта.
        @type obj: C{icBase}
        @param obj: Объект, у которого изменяем свойство.
        @type property: C{string}
        @param property: Имя свойства.
        @type value: C{...}
        @param value: Новое значение свойства.
        @type bRefresh: C{bool}
        @param bRefresh: Признак обновления редактора свойств.
        """
        try:
            iditem = obj.resource['__item_id']
            self.propertyTree.tree.ChangePropertyId(iditem, property, value, bRefresh)
            return True
        except:
            io_prnt.outLastErr('')
            
        return False

    def DestroyEditor(self):
        """
        Уничтожение редактора.
        """
        self.OnClose(None)
        self.GetEditorFrame().Destroy()
        
    def DragSelObj(self, pos):
        """
        Захватывает выбранный объект для перетаскивания.
        @type pos: C{wx.Point}
        @parma pos: Позиция захвата относительно родительского окна.
        """
        self.bDrag = True
        self.selectedObj.SetShapeType()
        self.selectedObj.EraseCursor()
        self.oldPoint = pos

    def DrawAll(self):
        """
        Перерисовывает все объекты на панели редактора.
        """
        try:
            for indx, obj in enumerate(self.container):
                try:
                    obj.DrawShape()
                except:
                    io_prnt.outLastErr('DrawShape  Error')

            self.bRedrawCursor = True
        except:
            io_prnt.outErr('DrawAll Error')
    
    def getEvtObj(self, evt):
        """
        Определяет объект, который послал сообщение. evt.GetEventObject()
        не подходит т. к. он возвращает wx-ий объект.
        """
        name = evt.GetEventObject().GetName()
        for obj in self.container:
            try:
                if name == obj.GetName():
                    return obj
            except:
                pass
        return None

    def GetEditorPanel(self):
        """
        Возвращает указатель на подложку редактора.
        """
        return self.editorPanel

    def GetEditorFrame(self):
        """
        Возвращает указатель на главное окно редактора.
        """
        return self.editorFrame

    def GetBGRPositionXY(self, obj_evt, x, y):
        """
        Вычисляет позицию отностиельно панели редактора по позиции на
        выбранном компоненте.
        """
        try:
            name = obj_evt.GetName()
        except:
            name = ''
            
        if name != '__EditorBackground__':
            pos = obj_evt.GetPosition()
            x = x + pos.x
            y = y + pos.y
            prnt = obj_evt.GetParent()
            while prnt and prnt.GetName() != '__EditorBackground__':
                pos = prnt.GetPosition()
                x = x + pos.x
                y = y + pos.y
                prnt = prnt.GetParent()
        
        return wx.Point(x, y)

    def GetBGRPosition(self, evt):
        """
        Вычисляет позицию события отностиельно панели редактора.
        """
        obj_evt = evt.GetEventObject()
        x, y = evt.GetPosition()
        if obj_evt.GetName() != '__EditorBackground__':
            pos = obj_evt.GetPosition()
            x = x + pos.x
            y = y + pos.y
            prnt = obj_evt.GetParent()

            while prnt and prnt.GetName() != '__EditorBackground__':
                pos = prnt.GetPosition()
                x = x + pos.x
                y = y + pos.y
                prnt = prnt.GetParent()
        
        return wx.Point(x, y)

    def GetParentPos(self, evt):
        """
        Вычисляет позицию отностиельно родительского окна компонента, который
        инициировал сообщение.
        """
        obj_evt = evt.GetEventObject()
        x, y = evt.GetPosition()
        if obj_evt.GetName() != '__EditorBackground__':
            pos = obj_evt.GetPosition()
            x = x + pos.x
            y = y + pos.y

        return wx.Point(x, y)

    def GetIndxObj(self, obj=None):
        """
        Возвращает индекс объекта в списке редактируемых объектов.
        """
        if not obj:
            obj = self.selectedObj
        if not obj or obj not in self.container:
            log.warning('Dont\'t find this obj in container obj=<%s>' % obj)
            return -1

        return self.container.index(obj)

    def isItemInEditor(self, iditem):
        """
        Функция определяет находистя ли компонент с таким идентификатором в
        колекции редактируемых компонентов.
        """
        for obj in self.container:
            try:
                if obj.resource['__item_id'] == iditem:
                        return True
            except:
                pass
            
        return False
        
    def OnSize(self, evt):
        """
        Отрабатывает после изменения размеров <EVT_SIZE>.
        """
        evt.Skip()
        self.Refresh()
        self.ReSizer()
        self.bRedraw = True

    def OnLeftDClick(self, evt):
        """
        Обработка сообщения <EVT_LEFT_DCLICK>.
        """
        obj_evt = evt.GetEventObject()
        x, y = evt.GetPosition()
        self.SelectObj(obj_evt, x, y)
        
    def OnSelectObj(self, evt, bDrag=True):
        """
        Обработка сообщения <EVT_LEFT_DOWN>.
        """
        obj_evt = evt.GetEventObject()
        x, y = evt.GetPosition()
        try:
            obj = self.getEvtObj(evt)
            if obj and obj != self.selectedObj:
                self.propertyTree.tree.SelectResId(obj.resource['__item_id'])
        except:
            io_prnt.outLastErr('OnSelectObj ERROR')
            
        self.SelectObj(obj_evt, x, y, bDrag=bDrag)
        self.RefreshStatusBar()
        
    def OnMove(self, evt):
        """ Обработка события мыши <wx.EVT_MOTION>."""
        if not self.selectedObj or self.selectedObj.name == '__EditorBackground__':
            evt.Skip()
            return

        prnt = self.selectedObj.GetParent()
        pos = self.GetBGRPosition(evt)
        x, y = self.selectedObj.GetPosition()
        sx, sy = self.selectedObj.GetSize()
        dd = 5
        try:
            # Перемещение объекта
            if self.bDrag and self.selectedObj.CanMoveObj():
                if prnt and getattr(prnt, 'type', None) == 'Background':
                    return

                x += pos.x - self.oldPoint.x
                y += pos.y - self.oldPoint.y
                self.selectedObj.SetPosition((x, y))
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragLT and self.selectedObj.CanResizeObj():
                dx = pos.x - self.oldPoint.x
                dy = pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetPosition((x+dx, y+dy))
                self.selectedObj.SetSize((sx-dx, sy-dy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragRT and self.selectedObj.CanResizeObj():
                dx = pos.x - self.oldPoint.x
                dy = pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetPosition((x, y+dy))
                self.selectedObj.SetSize((sx+dx, sy-dy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragRB and self.selectedObj.CanResizeObj():
                sx += pos.x - self.oldPoint.x
                sy += pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetSize((sx, sy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragLB and self.selectedObj.CanResizeObj():
                dx = pos.x - self.oldPoint.x
                dy = pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetPosition((x+dx, y))
                self.selectedObj.SetSize((sx-dx, sy+dy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragL and self.selectedObj.CanResizeObj():
                dx = pos.x - self.oldPoint.x
                self.selectedObj.EraseCursor()
                self.selectedObj.SetPosition((x+dx, y))
                self.selectedObj.SetSize((sx-dx, sy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragR and self.selectedObj.CanResizeObj():
                dx = pos.x - self.oldPoint.x
                self.selectedObj.EraseCursor()
                self.selectedObj.SetSize((sx+dx, sy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragT and self.selectedObj.CanResizeObj():
                dy = pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetPosition((x, y+dy))
                self.selectedObj.SetSize((sx, sy-dy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            elif self.bDragB and self.selectedObj.CanResizeObj():
                dy = pos.y - self.oldPoint.y
                self.selectedObj.EraseCursor()
                self.selectedObj.SetSize((sx, sy+dy))
                self.selectedObj.DrawCursor()
                self.oldPoint = pos
                self.RefreshStatusBar()
            else:
                xr, yr = self.convToBGR(self.selectedObj)
                sx, sy = self.selectedObj.GetSize()
                selR = wx.Rect(xr, yr, sx, sy)
                
                if not selR.Inside(pos):
                    cursor = wx.StockCursor(wx.CURSOR_DEFAULT)
                elif self.selectedObj.CanMoveObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZING)
                else:
                    cursor = wx.StockCursor(wx.CURSOR_NO_ENTRY)
    
                wm = self.markerSize
                r = wx.Rect(0, 0, wm, wm)
    
                # Left-Top
                r.Offset((xr-wm, yr-wm))
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENWSE)
                # Right-Top
                r.Offset((sx+wm, 0))
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENESW)
                # Right-Bottom
                r.Offset((0, sy+wm))
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENWSE)
                # Left-Bottom
                r.Offset((-sx-wm, 0))
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENESW)
    
                # Проверяем стороны
                # Left
                r = wx.Rect(xr-wm, yr, wm, sy)
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZEWE)
                # Right
                r = wx.Rect(xr+sx, yr, wm, sy)
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZEWE)
                # Top
                r = wx.Rect(xr, yr-wm, sx, wm)
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENS)
                # Bottom
                r = wx.Rect(xr, yr+sy, sx, wm)
                if r.Inside(pos) and self.selectedObj.CanResizeObj():
                    cursor = wx.StockCursor(wx.CURSOR_SIZENS)
            
                if selR.Inside(pos) and self.toolpanel and self.toolpanel.GetToggleType():
                    cursor = wx.StockCursor(wx.CURSOR_CROSS)
                if cursor:
                    self.SetCursor(cursor)
        except:
            # Некоторые компоненты (в частности CheckListBox) падают на SetSize
            self.oldPoint = pos
            self.RefreshStatusBar()
            self.selectedObj.DrawCursor()
            io_prnt.outLastErr('Except in OnMove')
            
        evt.Skip()

    def OnLeftDown(self, evt):
        """
        Обработка нажатия левой кнопки мыши <EVT_LEFT_DOWN>.
        """
        self.bBlockDestroy = True
        obj_evt = evt.GetEventObject()
        # Если выбран объект добавления в панели инструментов, то добавляем его
        # в текущий объект в позицию, на которую указывает курсор мыши
        if self.toolpanel:
            toggleType = self.toolpanel.GetToggleType()
            # Убираем признак добавляемого объекта в панели инструментов
            self.toolpanel.ReleaseToggleType()
            if toggleType and self.AddObjectToRes(self.selectedObj, toggleType, evt.GetPosition()):
                self.bBlockDestroy = False
                evt.Skip()
                return
            else:
                log.error('Add: selected object <%s>. toggle type <%s>' % (self.selectedObj, toggleType))
                
        #   Если курсор мыши на выбранном объекте, то происходит захват объекта.
        if self.selectedObj:
            pos = self.GetBGRPosition(evt)
            x,y = self.selectedObj.GetPosition()
            sx, sy = self.selectedObj.GetSize()

            if self.selectedObj.GetRect().Inside(pos) and not self.bDrag:
                self.DragSelObj(pos)
            else:
                self.oldPoint = None
                xr, yr = self.convToBGR(self.selectedObj)
                wm = self.markerSize
                r = wx.Rect(0, 0, wm, wm)
                
                # Проверяем углы
                # Left-Top
                r.Offset((xr-wm, yr-wm))
                if r.Inside(pos):
                    self.bDragLT = True
                    self.oldPoint = pos
                # Right-Top
                r.Offset((sx+wm, 0))
                if r.Inside(pos):
                    self.bDragRT = True
                    self.oldPoint = pos
                # Right-Bottom
                r.Offset((0, sy+wm))
                if r.Inside(pos):
                    self.bDragRB = True
                    self.oldPoint = pos
                # Left-Bottom
                r.Offset((-sx-wm, 0))
                if r.Inside(pos):
                    self.bDragLB = True
                    self.oldPoint = pos

                # Проверяем стороны
                # Left
                r = wx.Rect(xr-wm, yr, wm, sy)
                if r.Inside(pos):
                    self.bDragL = True
                    self.oldPoint = pos
                # Right
                r = wx.Rect(xr+sx, yr, wm, sy)
                if r.Inside(pos):
                    self.bDragR = True
                    self.oldPoint = pos
                # Top
                r = wx.Rect(xr, yr-wm, sx, wm)
                if r.Inside(pos):
                    self.bDragT = True
                    self.oldPoint = pos
                # Bottom
                r = wx.Rect(xr, yr+sy, sx, wm)
                if r.Inside(pos):
                    self.bDragB = True
                    self.oldPoint = pos

        if True not in (self.bDragLT, self.bDragRT, self.bDragLB, self.bDragRB,
                        self.bDragL, self.bDragR, self.bDragT, self.bDragB):
            self.OnSelectObj(evt)

        evt.Skip()
        self.bBlockDestroy = False
        
    def OnRightDownObj(self, evt):
        """
        Обработка нажатия правой кнопки.
        """
        self.bBlockDestroy = True
        obj_evt = evt.GetEventObject()
                
        if True not in (self.bDragLT, self.bDragRT, self.bDragLB, self.bDragRB,
                        self.bDragL, self.bDragR, self.bDragT, self.bDragB):
            self.OnSelectObj(evt, bDrag=False)
            if self.GetPointer():
                self.GetPointer().tree.OnRightClick(evt, bgr_win=self)

        evt.Skip()
        self.bBlockDestroy = False
        
    def OnLeftUp(self, evt):
        """
        Обрабатывет сообщение от мышки EVT_LEFT_UP.
        """
        if not self.selectedObj:
            evt.Skip()
            return
            
        pos = self.GetBGRPosition(evt)
        x, y = self.selectedObj.GetPosition()
        sx, sy = self.selectedObj.GetSize()
        #   Отпускаем захваченный объект
        if self.bDrag or self.bDragLT or self.bDragL or self.bDragT:
            if self.bDrag:
                self.bDrag = False
                self.selectedObj.SetSelected()

            # Изменяем оответствующее свойство <position> в ресурсном описании текущего
            # компонента
            x, y = self.selectedObj.GetPosition()

            # Изменияем свойство <position> в ресурсном описании объекта,
            # если выбранный объект не является сайзером. Поскольку для сайзеров,
            # в частности для icGridBagSizer, этот атрибут трактуется по-другому,
            # как координата ячейки (ряд, колонка).
            try:
                szr = self.selectedObj.contaningSizer
            # Сайзеры не имеют функции GetContainingSizer()
            except:
                szr = None

            if not szr or not issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
                self.ChangeResProperty(self.selectedObj, 'position', self.selectedObj.GetPosition(), bRefresh=True)

            elif szr and issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
                row, col = szr.GetCellInPoint(self.selectedObj.GetPosition())
                if row >= 0 and col >= 0 and not szr.FindCell(row, col):
                    self.selectedObj.position = (row, col)
                    self.ChangeResProperty(self.selectedObj, 'position', self.selectedObj.position, bRefresh=True)
 
        # Чистим признаки направлений изменяемых размеров
        if True in (self.bDragLT, self.bDragRT, self.bDragLB, self.bDragRB,
                    self.bDragL, self.bDragR, self.bDragT, self.bDragB):
            self.bDragLT = False
            self.bDragRT = False
            self.bDragRB = False
            self.bDragLB = False
            self.bDragL = False
            self.bDragR = False
            self.bDragT = False
            self.bDragB = False
            self.ChangeResProperty(self.selectedObj, 'size', self.selectedObj.GetSize(), bRefresh=True)

        self.ReSizer()
        evt.Skip()
        
    def OnKeyUp(self, evt):
        """
        Обработка отпускание клавишь <EVT_KEY_UP>.
        """
        kcod = evt.GetKeyCode()
        if self.selectedObj and kcod in (wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN):
            self.ChangeResProperty(self.selectedObj, 'size', self.selectedObj.GetSize(), bRefresh=True)

            if 1:
                try:
                    szr = self.selectedObj.contaningSizer
                # Сайзеры не имеют функции GetContainingSizer()
                except:
                    szr = None
                # Для компонента изменяется изменяется координаты ячейки, в которой
                # распологается компонент
                if szr and issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
                    self.ChangeResProperty(self.selectedObj, 'position', self.selectedObj.position, bRefresh=True)
                else:
                    self.ChangeResProperty(self.selectedObj, 'position', self.selectedObj.GetPosition(), bRefresh=True)

            self.ReSizer()
        evt.Skip()
    
    def OnKeyDown(self, evt):
        """
        Обработка нажатия клавишь <EVT_KEY_DOWN>.
        """
        kcod = evt.GetKeyCode()
        bCtrl = evt.ControlDown()
        bShift = evt.ShiftDown()
        bAlt = evt.AltDown()
        sel = None
        
        # Обработка табуляции - выбор следующего объекта в качестве текущего.
        # С использованием wx констант не работает.
        if kcod in [313]:
            cLen = len(self.container)
            sel = None
            if cLen > 0:
                if self.selectedObj:
                    indx = fi = self.container.index(self.selectedObj)
                else:
                    indx = fi = 0
                while 1:
                    indx += 1
                    if indx < cLen:
                        sel = self.container[indx]
                        break
                    elif indx == fi:
                        break
                    elif indx >= cLen-1:
                        indx = -1
            if sel:
                self.propertyTree.tree.SelectResId(sel.resource['__item_id'])
                self.SelectObj(sel, bDrag=False)
                self.ReSizer()

            return

        if kcod in (wx.WXK_NUMPAD_ENTER, wx.WXK_RETURN) and self.selectedObj:
            self.propertyTree.tree.SelectResId(self.selectedObj.resource['__item_id'])

        if kcod == 312:
            cLen = len(self.container)
            sel = None
            if cLen > 0:
                if self.selectedObj:
                    indx = fi = self.container.index(self.selectedObj)
                else:
                    indx = fi = 0
                while 1:
                    indx -= 1
                    if indx >= 0:
                        sel = self.container[indx]
                        break
                    elif indx == fi:
                        break
                    elif indx <= 0:
                        indx = cLen
            if sel:
                self.propertyTree.tree.SelectResId(sel.resource['__item_id'])
                self.SelectObj(sel, bDrag=False)
                self.ReSizer()
            
            return
        
        if self.selectedObj and kcod in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN]:
            x, y = self.selectedObj.GetPosition()
            sx, sy = self.selectedObj.GetSize()
            self.selectedObj.EraseCursor()
            ds = 1
            if 1:
                ds = 1
            try:
                # Коды изменения размеров объекта
                if kcod == wx.WXK_LEFT and bCtrl:
                    self.selectedObj.SetSize((sx-ds, sy))
                elif kcod == wx.WXK_RIGHT and bCtrl:
                    self.selectedObj.SetSize((sx+ds, sy))
                elif kcod == wx.WXK_UP and bCtrl:
                    self.selectedObj.SetSize((sx, sy-ds))
                elif kcod == wx.WXK_DOWN and bCtrl:
                    self.selectedObj.SetSize((sx, sy+ds))
                elif 1:
                    # Коды изменения позиции объекта
                    try:
                        szr = self.selectedObj.contaningSizer
                    # Сайзеры не имеют функции GetContainingSizer()
                    except:
                        szr = None
                        
                    # Для компонента изменяется изменяется координаты ячейки, в которой
                    # распологается компонент
                    if szr and issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
                        row, col = self.selectedObj.position
                        if kcod == wx.WXK_LEFT and col > 0 and not szr.FindCell(row, col-1):
                            self.selectedObj.position = (row, col-1)
                        elif kcod == wx.WXK_RIGHT and not szr.FindCell(row, col+1):
                            self.selectedObj.position = (row, col+1)
                        elif kcod == wx.WXK_UP and row > 0 and not szr.FindCell(row-1, col):
                            self.selectedObj.position = (row-1, col)
                        elif kcod == wx.WXK_DOWN and not szr.FindCell(row+1, col):
                            self.selectedObj.position = (row+1, col)

                        self.ChangeResProperty(self.selectedObj, 'position', self.selectedObj.position, bRefresh=True)
                        self.selectedObj.DrawCursor()
                        self.selectedObj.SetFocus()
                        return
                    else:
                        if kcod == wx.WXK_LEFT:
                            self.selectedObj.SetPosition((x-ds, y))
                        elif kcod == wx.WXK_RIGHT:
                            self.selectedObj.SetPosition((x+ds, y))
                        elif kcod == wx.WXK_UP:
                            self.selectedObj.SetPosition((x, y-ds))
                        elif kcod == wx.WXK_DOWN:
                            self.selectedObj.SetPosition((x, y+ds))
            except:
                io_prnt.outLastErr('OnKeyDown')
            
            self.selectedObj.DrawCursor()
        evt.Skip()

    def OnChar(self, evt):
        evt.Skip()

    def ClearBckground(self, dc):
        dc = dc or wx.PaintDC(self)
        dc.BeginDrawing()
        bmp = editorimg.background.GetBitmap()
        
        fx, fy = (1, 1)
        sx, sy = bmp.GetWidth(), bmp.GetHeight()
        cx, cy = self.GetClientSize()
        
        nx = cx/(sx*fx)+1
        ny = cy/(sy*fy)+1
        
        x0 = 0
        y0 = 0
        
        for i in xrange(ny):
            for n in xrange(nx):
                dc.DrawBitmap(bmp, x0 + n*sx*fx, y0 + i*sy*fy, True)
                
        dc.EndDrawing()
        
    def OnPaint(self, event):
        """
        Обрабатывает сообщение <EVT_PAINT>.
        """
        dc = wx.BufferedPaintDC(self)
        width, height = self.GetClientSize()
        if not width or not height:
            return

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)

        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1)

        dc.SetBackground(backBrush)
        dc.SetTextForeground(self.GetForegroundColour())
        dc.Clear()
        self.ClearBckground(dc)
        dc.SetFont(self.GetFont())
        
        if True not in (self.bDrag, self.bDragLT, self.bDragRT, self.bDragLB,
                        self.bDragRB, self.bDragL, self.bDragR, self.bDragT, self.bDragB):
            self.bRedrawCursor = True
        
        wx.CallAfter(self.DrawAll)

    def OnClose(self, evt):
        """
        Обрабатываем сообщение о закрытии окна  <EVT_CLOSE>.
        """
        # Если редактор был привязан к дереву свойств, то пытаемся
        # отвязвться - в редакторе свойств соответствующий указатель
        # устанавливается в None.
        if self.timer:
            self.timer.Stop()

        if self.propertyTree:
            try:
                if self.propertyTree:
                    self.propertyTree.ReleasePointer()
                self.propertyTree = None

                if self.toolframe:
                    # Сохраняем указатель на панель инструментов в буфере
                    SetPanelToolBuff(self.toolframe)
                    self.toolframe.Show(False)

                    # Освобождаем указатель на графический редактор в панели инструментов
                    self.toolpanel.ReleaseGraphEditor()
            except:
                io_prnt.outLastErr('###')
                
        # Удаляем форму
        if evt:
            evt.Skip()

    def OnUpdate(self, evt):
        """
        Update. По соответствующему сообщению, а также по таймеру.
        """
        try:
            if self.bRedrawCursor:
                self.bRedrawCursor = False
                try:
                    if self.selectedObj and not issubclass(self.selectedObj.__class__, icBackgroundFrame):
                        self.selectedObj.DrawCursor()
                    if (not issubclass(self.prntSelObj.__class__, icBackgroundFrame) and
                        not issubclass(self.selectedObj.__class__, icBackgroundPanel) and
                        not issubclass(self.selectedObj.__class__, icBackgroundDocumentFrame)) and self.prntSelObj:
                        self.prntSelObj.DrawCursor(clr=PARENT_CURSOR_COLOR)
                    elif self.selectedObj:
                        self.selectedObj.DrawCursor()
                except:
                    io_prnt.outErr('DrawCursor ERROR In OnUpdate')
                    
            if self.bRedraw:
                self.bRedraw = False
                self.DrawAll()
                self.OnSizeBgr(None)
            if evt:
                evt.Skip()
        except wx.PyDeadObjectError:
            pass

    def RefreshAll(self):
        """
        Обновление всех компонентов.
        """
        for indx, obj in enumerate(self.container):
            try:
                obj.Refresh()
            except:
                pass
        self.bRedraw = True
            
    def RefreshStatusBar(self):
        """
        Обновляет статусную строку.
        """
        try:
            if self.selectedObj:
                pos = self.selectedObj.GetPosition()
                size = self.selectedObj.GetSize()
                sb = self.GetEditorFrame().statusBar
                if sb:
                    sb.SetStatusText('pos:' + str(pos), 0)
                    sb.SetStatusText('size:' + str(size), 1)
        except:
            pass

    def ReSizer(self, obj=None):
        """
        Перестраивает сайзер.
        @param obj: Объект, который изменил свой параметры.
        """
        if not obj:
            obj = self.selectedObj
            
        # Перестраиваем сайзеры
        try:
            szr = obj.contaningSizer
        # Сайзеры не имеют функции GetContainingSizer()
        except:
            szr = None

        if szr and not issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
            if obj:
                obj.EraseCursor()
            if self.prntSelObj:
                self.prntSelObj.EraseCursor()
            if 1:
                for obj in szr.objectList:
                    szr.Detach(obj)
                    
                _list = szr.objectList
                szr.objectList = []
                for obj in _list:
                    szr.Add(obj, obj.proportion, obj.flag, obj.border)
                    szr.SetItemMinSize(obj, obj.GetSize())

            szr.Layout()

        elif szr and issubclass(szr.__class__, icgridbagsizer.icGridBagSizer):
            try:
                if obj:
                    obj.EraseCursor()
                if self.prntSelObj:
                    self.prntSelObj.EraseCursor()
            except:
                pass
            
            szr.Reconstruct()

        try:
            prnt_szr = szr.contaningSizer
            while prnt_szr:
                prnt_szr.Layout()
                prnt_szr = prnt_szr.contaningSizer
        except: pass

        self.RefreshAll()
        self.RefreshStatusBar()

    def SetPointer(self, edt):
        """
        Устанавливает указатель на редактор свойств.
        """
        if self.propertyTree:
            self.propertyTree.ReleasePointer()
        self.propertyTree = edt
    
    def GetPointer(self):
        return self.propertyTree
        
    def SelectObjRes(self, res):
        """
        Выбор объкта в качестве текущего по попределенному идентификатору.
        Идентификатор хранится в ресурсном описании каждого объекта под ключом
        '__item_id'
        @type res: C{dictionary}
        @param res: Ресурсное описания объекта.
        @rtype: C{Bool}
        @return: Признак успешного выбора.
        """
        for obj in self.container:
            try:
                if obj.resource == res:
                    self.SelectObj(obj, bDrag=False)
                    self.ReSizer()
                    return True
            except:
                pass
        return False

    def SelectObjId(self, iditem):
        """
        Выбор объкта в качестве текущего по определенному идентификатору.
        Идентификатор хранится в ресурсном описании каждого объекта под ключом
        '__item_id'
        @type itemid: C{int}
        @param itemid: Идентификатор описания объекта.
        @rtype: C{Bool}
        @return: Признак успешного выбора.
        """
        for obj in self.container:
            try:
                if obj.resource['__item_id'] == iditem:
                    self.SelectObj(obj, bDrag=False)
                    self.ReSizer()
                    obj.SetFocus()
                    return True
            except:
                io_prnt.outLastErr('ERROR in SelectObjId')
        return False
        
    def get_style_panel(self):
        """
        Возвращет указатель на панель стилей.
        """
        return self.toolpanel
        
    def SelectObj(self, obj_evt, x=1, y=1, bDrag=True):
        """
        Функция выбора объкта в качестве текущего. Выбор происходит по
        нажатию левой кнопки мыши на выбираемом объекте.
        @type obj_evt: C{наследник от wx.Window}
        @param obj_evt: Выбираемый объект.
        @type x: C{int}
        @param x: Координата x, где произошло событие.
        @type y: C{int}
        @param y: Координата y, где произошло событие.
        """
        # Отображаем в панели инструментов стили выбранного компонента и типы комопнентов,
        # которые можно добавлять в текущий компонент
        if not getattr(obj_evt, 'type', None):
            return
        
        # Не даем захватывать корневой элемент
        prnt = obj_evt.GetParent()

        if self.toolpanel:
            # Определяем тип текущего объекта
            typObj = getattr(obj_evt, 'type', None)
            # Для подложки диалогового окна типы компонентов, которые можно
            # добавлять такие же как и у диалогового окна
            if typObj == 'Background':
                typObj = 'Group'
            # Активируем типы, которые можно добавлять в текущий объект
            self.toolpanel.EnableCanAddObj(typObj, True)
            # Отображаем информацию (flag, proportion) в панели инструментов
            if self.get_style_panel():
                self.get_style_panel().SetFlag(obj_evt.flag)
                self.get_style_panel().SetProportionStyle(obj_evt.proportion)
        
        if self.selectedObj == obj_evt and not bDrag:
            return
            
        if self.selectedObj:
            self.selectedObj.SetShapeType()
            self.selectedObj.EraseCursor()
            try:
                self.prntSelObj.SetShapeType()
                self.prntSelObj.EraseCursor()
                # Сохраняем размеры колонок грида
                if self.selectedObj.type == 'GridDataset':
                    pass
            except:
                pass
            
        obj_evt.SetSelected()
        self.selectedObj = obj_evt
        pos = self.GetBGRPositionXY(obj_evt, x, y)
        if bDrag:
            self.DragSelObj(pos)
        cursor = wx.StockCursor(wx.CURSOR_SIZING)
        self.SetCursor(cursor)
        try:
            self.prntSelObj = prnt
            self.prntSelObj.SetShapeType(icParentShapeType)
        except:
            pass

        if not bDrag:
            self.bDrag = False

        self.OnUpdate(None)


def BindEditorEvent(self, id=None):
    """
    Функция создает все обработчики событий необходимые редактору форм.
    @param self: Указатель на окно редактора.
    """
    self.Bind(wx.EVT_CLOSE, self.OnClose)
    self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate)
    self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_MOTION, self.OnMove)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDownObj)
    self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
    self.Bind(wx.EVT_CHAR, self.OnChar)


class icBackgroundDialog(icBackground, icdialog.icDialog):
    """
    Подложка для диалогового окна.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={}):
        """
        Конструктор для создания объекта icBackgroundFrame.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        icBackground.__init__(self, parent, id, component, logType, evalSpace)
        icdialog.icDialog.__init__(self, parent, id, component, logType, evalSpace)
        self.editorPanel = self
        # Обработчики событий
        BindEditorEvent(self)
        
    def OnCharHook(self, evt):
        wx.Dialog.OnCharHook(self, evt)
        evt.Skip()


class icBackgroundPanel(icBackground, wx.Panel):
    """
    Положка для панели.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None):
        """
        Конструктор для создания объекта icBackgroundFDialog.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        icBackground.__init__(self, parent, id, component, logType, evalSpace)
        wx.Panel.__init__(self, parent, id=-1)
        self.editorPanel = self
        self.editorFrame = parent
        # Обработчики событий
        BindEditorEvent(self)


class icBackgroundFDialog(icwidget.icSimple, wx.Frame):
    """
    Класс иметирует редактирование диалогового окна.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace={}):
        """
        Конструктор для создания объекта icBackgroundFDialog.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        component['style'] = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        wx.Frame.__init__(self, parent, -1, style=component['style'])
        self.editorPanel = icBackgroundPanel(self, -1,
                                             {'style': wx.TAB_TRAVERSAL, 'keyDown': 'True'},
                                             logType, evalSpace)
        self.editorPanel.resource['__item_id'] = self.resource['__item_id']
        self.statusBar = EditorStatusBar(self)
        self.SetStatusBar(self.statusBar)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # Создаем дочерние компоненты
        self.childCreator(False, None)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prnt = self.GetEditorPanel()
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = prnt

            self.GetKernel().parse_resource(prnt, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
        
    def CreateToolPanel(self, ObjectsInfo=None):
        """
        Создаем панель инструментов.
        """
        self.toolframe = GetPanelToolBuff()
        if not self.toolframe:
            self.toolframe = icPanelTool.icPanelToolFrame(None, 'icPanelTool Test',
                                                          layout='vertical', ObjectsInfo=ObjectsInfo)
        self.toolpanel = self.toolframe.GetToolPanel()
        self.editorPanel.toolpanel = self.toolpanel
        self.toolframe.Show(True)
        self.toolpanel.SetGraphEditor(self.editorPanel)

    def OnKeyDown(self, evt):
        self.editorPanel.OnKeyDown(evt)
        
    def OnClose(self, evt):
        try:
            self.editorPanel.propertyTree.ReleasePointer()
            self.editorPanel.propertyTree = None
            if self.toolframe:
                # Сохраняем указатель на панель инструментов в буфере
                SetPanelToolBuff(self.toolframe)
                self.toolframe.Show(False)
                # Освобождаем указатель на графический редактор в панели инструментов
                self.toolpanel.ReleaseGraphEditor()
        except:
            io_prnt.outLastErr('###')

        if evt:
            evt.Skip()
        
    def GetEditorPanel(self):
        """
        Возвращает указатель на подложку редактора.
        """
        return self.editorPanel
    
    def AddObject(self, obj):
        if self.editorPanel:
            self.editorPanel.AddObject(obj)


class EditorStatusBar(wx.StatusBar):
    """
    """
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        # This status bar has three fields
        self.SetFieldsCount(3)
        self.sizeChanged = False
        # Field 0 ... just text
        self.SetStatusText('pos:', 0)
        self.SetStatusText('size:', 1)


class icBackgroundFrame(icBackground, icwidget.icSimple, wx.Frame):
    """
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None):
        """
        Конструктор для создания icBackgroundFrame.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        icBackground.__init__(self, parent, id, component, logType, evalSpace)
        component['style'] = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        component['name'] = '__EditorBackground__'
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        wx.Frame.__init__(self, parent, -1, style=component['style'])
        self.editorPanel = self
        self.editorFrame = self
        self.statusBar = EditorStatusBar(self)
        self.SetStatusBar(self.statusBar)
        # Обработчики событий
        BindEditorEvent(self)
        # Создаем дочерние компоненты
        self.childCreator(False, None)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)

    def CreateToolPanel(self, ObjectsInfo=None):
        """
        Создаем панель инструментов.
        """
        self.toolframe = GetPanelToolBuff()
        if not self.toolframe:
            self.toolframe = icPanelTool.icPanelToolFrame(None, 'icPanelTool Test',
                                                          layout='vertical', ObjectsInfo=ObjectsInfo)
        self.toolpanel = self.toolframe.GetToolPanel()
        self.toolframe.Show(True)
        self.toolpanel.SetGraphEditor(self.editorPanel)


class icBackgroundDocumentFrame(icBackground, icwidget.icBase, wx.ScrolledWindow):
    """
    Представление подложки в IDE.
    """
    BGR_DOC_ID = wx.NewId()

    def __init__(self, parent, id=-1, component=None, logType=0, context=None):
        """
        Конструктор для создания icBackgroundFrame.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param context: Контекст ресурса.
        @type context: C{dictionary}
        """
        if component is None:
            res = dict(name='__EditorBackground__', type='Background', child=[])
        else:
            res = None
            
        icBackground.__init__(self, parent, id, component, logType, context)
        if not res:
            res = dict(name='__EditorBackground__', type='Background', child=[component])
        
        icwidget.icBase.__init__(self, parent, id, res, logType, context)
        wx.ScrolledWindow.__init__(self, parent, -1)
        wx.ScrolledWindow.SetBackgroundColour(self, wx.WHITE)
        self.editorPanel = self
        self.editorFrame = self
        # Указатель на панель инструментов
        self.toolpanel = None
        # Устанавливаем режим редактора форм
        self.context.setMode(util.IC_RUNTIME_MODE_EDITOR)
        # Создаем объект по ресурсу
        self.object = self.childCreator(False, None)
        if self.object:
            # Не все компоненты наследники от wx.Window
            try:
                self.object.SetPosition((5, 5))
                self.object.SetEditorMode()
                self.object.Bind(wx.EVT_SIZE, self.OnSizeWin)
                self.object.Layout()
            except:
                pass

        # Настоки сайзера
        self.SetVirtualSize((self.getWidth(), self.getHeight()))
        self.rate_x = 20
        self.rate_y = 20
        self.SetScrollRate(self.rate_x, self.rate_y)
        self.EnableScrolling(True, True)

        self.Bind(wx.EVT_SIZE, self.OnSizeBgr)
        # Обработчики событий
        BindEditorEvent(self, self.BGR_DOC_ID)

        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        self.timer.Start(200)
        #
        self._old_pos = None
        
    def TimerHandler(self, evt):
        self.OnUpdate(evt)
    
    def OnSizeBgr(self, evt):
        sx, sy = self.GetViewStart()
        if self.object:
            # Обкладываем try на случай не визуальных компонентов
            try:
                xx, yy = self.object.GetPosition()
                x, y = (5-sx*self.rate_x, 5 - sy*self.rate_y)
                if (x, y) != (xx, yy):
                    self.object.SetPosition((x, y))
                    self.Refresh()
                    
            except Exception, msg:
                log.error('OnSizeBgr <%s>' % msg)
                
        if evt:
            evt.Skip()

    def OnSizeWin(self, evt):
        sx, sy = evt.GetSize()
        self.SetVirtualSize((sx+50, sy+50))
        self.Refresh()
        evt.Skip()
        
    def getWidth(self):
        try:
            return self.object.GetSize()[0]+20
        except:
            return 800

    def getHeight(self):
        try:
            return self.object.GetSize()[1]+20
        except:
            return 800

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            # NOTE: Чистим сконтекст
            self.context.clear_spc_structs()
            self.context['_root_obj'] = self
            self.context['_main_parent'] = self
            sz = self.child[0]['size']
            self.child[0]['size'] = (0, 0)
            obj = self.GetKernel().parse_resource(self, self.child, None, context=self.context,
                                                  bCounter=bCounter, progressDlg=progressDlg)
            obj = self.context.FindObject(self.child[0]['type'],
                                          self.child[0]['name'])
            if obj:
                wx.CallAfter(obj.SetSize, sz)
            return obj
                                            
    def CreateToolPanel(self, ObjectsInfo=None, parent=None):
        """
        Создаем панель инструментов.
        """
        self.toolpanel = GetPanelToolBuff()
        if not self.toolpanel:
            self.toolpanel = icPanelTool.icPanelTool(parent, 'Title', layout='vertical',
                                                     ObjectsInfo=ObjectsInfo)
        self.toolpanel.SetGraphEditor(self.editorPanel)
        return self.toolpanel


def test(par=0):
    """
    Тестируем класс icFrame.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None)
    win = icBackgroundDocumentFrame(frame)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()