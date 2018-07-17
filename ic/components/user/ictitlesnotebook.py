#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Набор закладок.
Класс реализует набор закладок, между которыми можно переключаться. К закладке
можно привязать визуалльный компонет (ф-ия ConnectObjToTitle). При выборе данной
закладки компонент будет отображаться при выборе других закладок исчезать. К
закладке можно привязать несколько компонентов, а также можно один компонент привязать
к нескольким закладкам. При выборе определенной закладки выполняется выражение атрибута
<onSelectTitle>.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import os
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import ic.components.icfont as icfont
import ic.bitmap.icbitmap as icbitmap
import ic.components.custom.icheadcell as icheadcell
import ic.utils.graphicUtils as graphicUtils
import wx as parentModule
from ic.kernel import io_prnt

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icTitlesNotebook'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'TitlesNotebook',
                'name': 'default',
                'child': [],

                'icDelButton': 1,
                'onSelectTitle': None,
                'titles': [],
                'isLocaleTitles': True,
                'images': [],
                'path': '',
                'selPageColor': (200, 200, 200),
                'backgroundColor': (100, 100, 100),
                'font': {},

                '__styles__': ic_class_styles,
                '__events__': {'onSelectTitle': ('wx.EVT_LEFT_UP', 'OnSelectTitle', False),
                               },
                '__attr_types__': {0: ['name', 'type'],
                                   12: ['path', 'onSelectTitle'],
                                   20: ['titles', 'images'],
                                   icDefInf.EDT_CHECK_BOX: ['icDelButton', 'isLocaleTitles'],
                                   9: ['font'],
                                   icDefInf.EDT_COLOR: ['selPageColor'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtNotebook'
ic_class_pic2 = '@common.imgEdtNotebook'

#   Путь до файла документации
ic_class_doc = None
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'DatasetNavigator', 'GridCell']

#   Версия компонента
__version__ = (0, 0, 0, 2)

#   Некоторые размеры панели

#   Высота панели
IC_NB_HEIGHT = 23
#   Высота активной страницы
IC_NB_PAGE = 20
#   Отступы от края
IC_NB_STEP = 7
#   Размер иконки на странице
IC_NB_ICON = (16, 16)
#   Размер ссервисной зоны
IC_NB_SERV_ZONE = 40

# Кнопка Next
NextPointsDark = [(0, 0), (0, 8), (4, 4), (0, 0)]
NextPointsLight = [(0, 9), (5, 4), (0, -1), (0, 0)]

# Кнопка Prev
PrevPointsDark = [(4, 0), (4, 8), (0, 4), (4, 0)]
PrevPointsLight = [(4, -1), (-1, 4), (4, 9), (4, 8)]

# Идентификаторы типов активных страничек
usual_page_id = 0
square_page_id = 1
gradient_page_id = 2
round_angle_page_id = 3


class icTitle:
    """
    Класс представления закладки.
    """

    def __init__(self, title, size, st, img=None, descr=''):
        """
        Конструктор.
        @type title: C{string}
        @param title: Заголовок закладки.
        @type size: C{wx.Size}
        @param size: Размер закладки.
        @type st: C{int}
        @param st: Отступ текста от края закладки.
        @type img: C{wx.StaticBitmap}
        @param img: Картинка на закладке.
        """
        self.title = title
        self.size = size
        self._image = img
        self.bitmap = None
        #   Краткое описание закладки
        self._descr = descr
        #   Список привязанных объектов
        self._objList = []
        # Отступ текста от края
        self.step_text = st
        
    def Show(self, bShow=True, activeTitle=None):
        """
        Показывает или скрывает компоненты привязанные к закладке.
        @type bShow: C{bool}
        @param bShow: Призка, который определяет скрывать или показывать компоненты.
        @type activeTitle: C{icTitle}
        @param activeTitle: Указывает на активную страницу. Это необходимо для того, чтобы
            не скрыть компонент активной страницы, в случае если компонент одновременно
            привязан к нескольким страницам.
        """
        for obj in self._objList:
            try:
                if not bShow and activeTitle and obj in activeTitle.GetConnectedObj():
                    pass
                else:
                    obj.Show(bShow)
            except:
                io_prnt.outLastErr('##?: Show Error')

    def GetConnectedObj(self):
        return self._objList

    def RemoveObjects(self):
        """
        Удаляет все привязанные объекты из закладки.
        """
        self.Show()
        self._objList = []
    
    def UnConnectObj(self, obj):
        """
        Удаляет объект из закладки.
        """
        try:
            obj.Show()
        except:
            pass
            
        self._objList.remove(obj)
        
    def ConnectObj(self, obj):
        """
        Привязывает объект к закладке.
        """
        self._objList.append(obj)
    
    def SetImage(self, img):
        """
        Устанвливает иконку закладки.
        """
        self._image = img
        
    def GetImage(self):
        """
        Возвращает иконку закладки.
        """
        return self._image
        
    def SetDescription(self, descr):
        """
        Устанавливает краткое описание закладки.
        """
        self._descr = descr

    def GetDescription(self):
        """
        Возвращет краткое описание закладки.
        """
        return self._descr
        
    def GetWidth(self):
        sx, sy = self.size
        return sx

    def GetHeight(self):
        sx, sy = self.size
        return sy


class icTitlesNotebook(icwidget.icWidget, parentModule.PyControl):
    """
    Описание пользовательского компонента.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{name='default'}:
        - B{icDelButton=0}: Признак наличия кнопки 'удалить закладку'.
        - B{onSelectTitle=None}: Выражение выполняемое после выбора закладки.
        - B{titles=[]}: Список заголовков закладок.
        - B{isLocaleTitles=True}: Признак локализации заголовков закладок,
        - B{images=[]}: Список картинок для закладок.
        - B{path=''}: Путь до папки с картинками.
        - B{font={}}: Шифт текста на закладках.
        - B{selPageColor}: Цвет текщей выбранной страницы.
        - B{child=[]}: Список привязанных объектов.
        - B{type='defaultType'}:
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        for key in lst_keys:
            setattr(self, key, component[key])

        #   Локализуем подписи закладок
        if self.isLocaleTitles:
            self.titles = [_(el) for el in self.titles]
        #   Цвета текста и фона
        self.bgr = bgr = component['backgroundColor'] or (100, 100, 100)
        self.fgr = fgr = component['foregroundColor']

        # -----------------------------------------------------------
        style = wx.ST_NO_AUTORESIZE | wx.NO_BORDER
        parentModule.PyControl.__init__(self, parent, id,
                                        self.position, self.size,
                                        style, name=self.name)
        # -----------------------------------------------------------
        self.SetAutoLayout(True)

        #   Устанавливаем шрифт
        if not self.font:
            font = parent.GetFont()
            if not font.Ok():
                font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.passiveFont = font
        else:
            self.passiveFont = icfont.icFont(self.font)

        parentModule.PyControl.SetFont(self, self.passiveFont)
        #   Устанавливаем цвета
        if bgr:
            self.SetBackgroundColour(bgr)
        if fgr:
            self.SetForegroundColour(fgr)

        #   Размер
        rw, rh = self.size
        self.SetSize(wx.Size(rw, IC_NB_HEIGHT+3))
        
        # ----------------------------------------------
        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_LEFT_UP, self.OnSelectTitle)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnPreSelect)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.BindICEvt()
        # ----------------------------------------------
        self.clientPanel = self

        #   Признаки, определяющие можно нажать кнопки Next, Prev
        self._canNext = False
        self._canPrev = False
        #   Список закладок
        self._tilesObjList = []
        #   Индекс первой видимой закладки
        self._firstVisible = 0
        #   Индекс последней видимой закладки
        self._lastVisible = -1
        #   Индекс активной закладки
        self._selected = 0
        #   Список присоединеных объектов
        self._connectedObjList = []
        #   Указатель на окно подсказки
        self._helpWin = None
        self._lastHelp = -1
        
        self.path = self.getICAttr('path')
        if not self.path:
            self.path = os.getcwd()
        
        self.path = self.path.replace('\\', '/')
        if self.path[-1] != '/':
            self.path += '/'
            
        #   Наполняем панель закладками
        for indx, title in enumerate(self.titles):
            img = None
            if indx < len(self.images):
                filename = self.path+self.images[indx]
                bmptype = icbitmap.icBitmapType(filename)
                if bmptype is not None and os.path.isfile(filename):
                    img = wx.Image(filename, bmptype).ConvertToBitmap()
                
            self.AddTitle(title, img=img)
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
            #   Привязвыаем объекты к панели закладок
            for indx, spc in enumerate(self.child):
                try:
                    #   Если описанием подключаемого объекта является группа,
                    #   то к закладке подключаются объекты из группы
                    if spc['type'] == 'Group':
                        for spc_grp in spc['child']:
                            obj = self.evalSpace['_dict_obj'][spc_grp['name']]
                            if obj not in self.GetConnectedObjLst():
                                self.ConnectObjToTitle(indx, obj)
                    else:
                        obj = self.evalSpace['_dict_obj'][spc['name']]
                        if obj not in self.GetConnectedObjLst():
                            self.ConnectObjToTitle(indx, obj)
                except:
                    io_prnt.outLastErr('')
        self.SelectTitle()

    def OnSize(self, evt):
        evt.Layout()
        evt.Skip()
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self.clientPanel, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)

    def RemoveTitleObjects(self, indx=-1):
        """
        Удаляет все объекты с закладки.
        @type indx: C{int}
        @param indx: Индекс закладки. Если -1, то компоненты удаляются из текущей
            закладки.
        """
        if indx < 0:
            indx = self.GetSelected()
        self.GetTitle(indx).RemoveObjects()

    def RemoveAllObjects(self):
        """
        Удаляет все объекты с панели.
        """
        for indx, obj in enumerate(self.GetTitlesList()):
            self.RemoveTitleObjects(indx)
            
    def ConnectObjToTitle(self, indx, obj):
        """
        Привязывает объект к нужной странице.
        @type indx: C{int}
        @param indx: Индекс закладки.
        """
        try:
            titleObj = self.GetTitlesList()[indx]
            titleObj.ConnectObj(obj)
            if obj not in self._connectedObjList:
                self._connectedObjList.append(obj)
        except:
            io_prnt.outLastErr('###?: ConnectObjToTitle() ERROR')
            
    def GetConnectedObjLst(self):
        """
        Возвращает полный список привязанных обектов.
        """
        return self._connectedObjList
        
    def GetSelected(self):
        """
        Возвращает номер текущей выбранной страницы.
        """
        return self._selected
    
    def IsVisible(self, indx):
        """
        Возвращет признак видимости нужной закладки.
        @type indx: C{int}
        @param indx: Индекс закладки.
        """
        return self.GetFirstVisible() <= indx <= self.GetLastVisible()
            
    def GetFirstVisible(self):
        """
        Возвращает номер первой видимой страницы.
        """
        return self._firstVisible

    def GetLastVisible(self):
        """
        Возвращает номер первой видимой страницы.
        """
        return self._lastVisible
    
    def SetFirstVisible(self, indx):
        """
        Возвращает номер первой видимой страницы.
        """
        if indx >= len(self.GetTitlesList()):
            indx = len(self.GetTitlesList())-1
            
        if indx < 0:
            indx = 0
        
        self._firstVisible = indx
        self.Refresh()
        
    def AddTitle(self, title, descr='', img=None):
        """
        Добавления закладки в панель.
        @type title: C{string}
        @param title: Заголовок закладки.
        @type descr: C{string}
        @param descr: Короткое описание закладки.
        @type img: C{wx.Bitmap}
        @param img: Иконка, которая будет распологаться на закладке.
        """
        sx, sy = wx.Window.GetTextExtent(self, title)
        if img:
            ctrl_img = wx.StaticBitmap(self, -1, img)
            if wx.Platform == '__WXMSW__':
                ctrl_img.Enable(False)
            w = sx + 3 * IC_NB_STEP + IC_NB_ICON[0]
            obj = icTitle(title, (w, IC_NB_HEIGHT), 2*IC_NB_STEP+IC_NB_ICON[0], img=ctrl_img)
            obj.bitmap = img
        else:
            w = sx + 2*IC_NB_STEP
            obj = icTitle(title, (w, IC_NB_HEIGHT), IC_NB_STEP+2)
            
        self._selected = len(self._tilesObjList)
        self._tilesObjList.append(obj)
        
    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the
        button based on the label size.
        """
        return self.GetSize()
        
    def GetTitlesList(self):
        return self._tilesObjList
        
    def GetTitle(self, indx):
        """
        Возвращет ссылку на нужную закладку.
        @type indx: C{int}
        @param indx: Индекс закладки.
        """
        try:
            return self.GetTitlesList()[indx]
        except:
            io_prnt.outLastErr('##?: GetTitle ERROR')
            return None
            
    def CanPressNext(self):
        return self._canNext

    def CanPressPrev(self):
        return self._canPrev
        
    def SelectTitle(self, indx=-1):
        """
        Выбирает нужную закладку в качестве текущей.
        @type indx: C{int}
        @param indx: Индекс закладки.
        """
        if indx < 0:
            indx = self.GetSelected()
            
        if 0 <= indx < len(self.GetTitlesList()):
            self._selected = indx
            for i, obj in enumerate(self.GetTitlesList()):
                if i == indx:
                    obj.Show(True)
                else:
                    obj.Show(False, self.GetTitlesList()[indx])
                
            if not self.IsVisible(indx):
                self.SetFirstVisible(indx)
            else:
                self.Refresh()
                
            self.evalSpace['index'] = indx
            self.evalSpace['self'] = self
            self.eval_attr('onSelectTitle')
            return True
            
        return False
        
    def OnLeave(self, evt):
        """
        Обработчик события wx.EVT_LEAVE_WINDOW.
        """
        if self._helpWin:
            self._helpWin.Show(False)
            self._helpWin.Destroy()
            self._helpWin = None
        evt.Skip()
            
    def OnMove(self, evt):
        """
        Обработчик события wx.EVT_MOTION.
        """
        evt.Skip()
        pos = x, y = evt.GetPosition()
        px, py = self.GetPosition()
        sx, sy = self.GetSize()
        findx = self.GetTitleIndx(pos)
        #   Создаем окно подсказки
        if findx >= 0:
            if self._lastHelp != findx and self._helpWin:
                self._helpWin.Show(False)
                self._helpWin.Destroy()
                self._helpWin = None

            if not self._helpWin:
                descr = self.GetTitlesList()[findx].GetDescription()
                if descr:
                    self._helpWin = icwidget.icShortHelpString(self.parent, descr,
                                                               (x + px, y + py + 20), 5000)
        elif self._helpWin:
            self._helpWin.Show(False)
            self._helpWin.Destroy()
            self._helpWin = None
            
        self._lastHelp = findx

    def GetTitleIndx(self, pos):
        """
        Определяет индекс закладки по позиции на панели.
        """
        x, y = pos
        sx, sy = self.GetSize()
        
        # Определяем номер страницы, которая будет выбранна
        w = 0
        findx = -1
        for indx, obj in enumerate(self.GetTitlesList()[self.GetFirstVisible():]):
            if indx == self.GetSelected():
                wo = obj.GetWidth() + IC_NB_STEP
            else:
                wo = obj.GetWidth()

            if w+wo > sx - (IC_NB_SERV_ZONE + IC_NB_STEP):
                break
            
            if w <= x < w + wo:
                findx = indx + self.GetFirstVisible()
                break
            
            w += wo
        return findx
        
    def OnPreSelect(self, evt):
        """
        Обработчик события wx.EVT_LEFT_DOWN.
        """
        pos = evt.GetPosition()
        sx, sy = self.GetSize()
        
        # Определяем номер страницы, которая будет выбранна
        findx = self.GetTitleIndx(pos)
                
        # Обработчик пользователя
        rectList = wx.Rect(sx - IC_NB_SERV_ZONE + 2, (IC_NB_HEIGHT - 8)/2-1, 13, 12)
        rectNext = wx.Rect(sx - IC_NB_SERV_ZONE + 26, (IC_NB_HEIGHT - 8)/2, 8, 8)
        rectPrev = wx.Rect(sx - IC_NB_SERV_ZONE + 17, (IC_NB_HEIGHT - 8)/2, 8, 8)
        if findx >= 0 and self.SelectTitle(findx):
            pass
        elif rectNext.Inside(pos) and self.CanPressNext():
            self.SetFirstVisible(self.GetFirstVisible()+1)

        elif rectPrev.Inside(pos) and self.CanPressPrev():
            self.SetFirstVisible(self.GetFirstVisible()-1)

        elif rectList.Inside(pos) and (self.CanPressPrev() or self.CanPressNext()):
            menu = wx.Menu()
            id = 10000
            for indx, obj in enumerate(self.GetTitlesList()):
                if indx < self.GetFirstVisible() or indx > self.GetLastVisible():
                    item = wx.MenuItem(menu, id, obj.title)
                    if obj.bitmap:
                        try:
                            item.SetBitmap(obj.bitmap)
                        except:
                            io_prnt.outLastErr('')
                        
                    menu.AppendItem(item)
                    self.Bind(wx.EVT_MENU, self.OnMenu, id=id)
                id += 1
            self.PopupMenu(menu, evt.GetPosition())
        else:
            evt.Skip()

    def OnMenu(self, evt):
        sel = evt.GetId() - 10000
        self.SetFirstVisible(sel)
        self.SelectTitle(sel)
        evt.Skip()
        
    def OnSelectTitle(self, evt):
        """
        Обработчик события wx.EVT_LEFT_UP, атрибут=onSelectTitle.
        """
        evt.Skip()

    def AcceptsFocus(self):
        """
        Overridden base class virtual.
        """
        return False

    def DrawTitle(self):
        pass
        
    def DrawActiveTitle(self, dc, obj, w, typeTitle=0):
        """
        Рисует активную закладку.
        @type typeTitle: C{int}
        @param typeTitle: Тип закладки: 0 - стандартная, 1 - квадратная,
            2 - квадратная с градиентной заливкой.
        """
        sx, sy = self.GetSize()
        pst = IC_NB_HEIGHT - IC_NB_PAGE
        dp = 3
        wo = obj.GetWidth()
        fgrPen = wx.Pen(self.GetForegroundColour(), 1, wx.SOLID)
        lightPen = wx.Pen(wx.Colour(255, 255, 255))
        pagePen = wx.Pen(self.selPageColor)
        pageBrush = wx.Brush(self.selPageColor)

        # Подсветка панели
        dc.SetPen(fgrPen)
        dc.DrawLine(0, IC_NB_HEIGHT-1, sx-1, IC_NB_HEIGHT-1)
        
        # Нижняя кайма
        dc.SetBrush(pageBrush)
        dc.SetPen(pagePen)
        wo += IC_NB_STEP

        if typeTitle == round_angle_page_id:
            fgr = self.GetForegroundColour()
            dc.SetPen(wx.Pen(fgr))
            dc.DrawRectangle(w, pst, wo, IC_NB_HEIGHT-pst)
            dc.SetPen(pagePen)
            dc.DrawLine(w+1, IC_NB_HEIGHT-1, w+wo-1, IC_NB_HEIGHT-1)

            clr1 = graphicUtils.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), -50)
            clr2 = graphicUtils.AdjustColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE), 50)
            
            graphicUtils.DrawGradientRect(dc, wo-2, IC_NB_HEIGHT-pst, clr1, clr2, 1, x0=w+1, y0=pst+1)
            graphicUtils.drawRoundCornersRect(dc, (w, pst), (wo, IC_NB_HEIGHT-pst),
                                              fgr, self.selPageColor,
                                              self.backgroundColor, 0,
                                              (fgr, fgr, fgr, fgr),
                                              (1, 1, 0, 0), 0)
        else:
            pagePoints = [(2, IC_NB_HEIGHT), (2, pst), (wo-dp, pst),
                          (wo, pst+dp), (wo, IC_NB_HEIGHT), (2, IC_NB_HEIGHT)]
            
            # Страница
            dc.DrawPolygon(pagePoints, w, 0)
            clr = wx.Colour(self.selPageColor[0], self.selPageColor[1], self.selPageColor[2])
            dc.SetPen(lightPen)
            dc.DrawLines([(1, IC_NB_HEIGHT-1), (1, pst-1), (wo-dp+1, pst-1)], w, 0)
            dc.SetPen(fgrPen)
            dc.DrawLines([(wo-dp+1, pst), (wo+1, pst+dp), (wo+1, IC_NB_HEIGHT)], w, 0)

        font = self.GetFont()
        font.SetWeight(wx.BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.Colour(0, 0, 0))
        dc.DrawText(obj.title, w+obj.step_text, (IC_NB_HEIGHT - obj.GetHeight())/2+pst+2)

        if obj.GetImage():
            obj.GetImage().Show(True)
            obj.GetImage().SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
            obj.GetImage().SetPosition((w+IC_NB_STEP, pst+2))
        
    def Draw(self, dc):
        """
        Функция рисует ячейку.
        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        """
        dc.BeginDrawing()

        #   Рисуем курсор компонента
        fgr = self.GetForegroundColour()
        bgr = self.GetBackgroundColour()
        fgrPen = wx.Pen(fgr, 1, wx.SOLID)
        fgrBrush = wx.Brush(fgr)
        bgrBrush = wx.Brush(bgr)
        
        dc.SetPen(fgrPen)
        dc.SetBrush(bgrBrush)

        sx, sy = self.GetSize()
        dc.DrawRectangle(0, 0, sx, sy)
        
        pen = wx.Pen((100, 100, 100))
        penNav = wx.Pen((50, 50, 50))
        blackClr = wx.Colour(10, 10, 10)
        pagePen = wx.Pen(self.selPageColor)
        pageBrush = wx.Brush(self.selPageColor)
        
        font = self.GetFont()
        
        # Рисуем страницы
        dc.SetPen(pen)
        lst = self.GetTitlesList()
        w = 0
        indx = self.GetFirstVisible()
        pst = IC_NB_HEIGHT - IC_NB_PAGE
        dp = 3
        bCanNext = False
        findLast = False
        self._lastVisible = len(lst)-1
        for indx, obj in enumerate(lst):
            wo = obj.GetWidth()
            if w+wo >= sx - (IC_NB_SERV_ZONE + IC_NB_STEP):
                bCanNext = True
                
                if not findLast:
                    self._lastVisible = indx - 1
                    findLast = True
                
            if indx >= self.GetFirstVisible() and not bCanNext:
                #   Рисуем активную страницу
                if indx == self.GetSelected():
                    self.DrawActiveTitle(dc, obj, w, 3)
                    wo += IC_NB_STEP
                else:
                    font.SetWeight(wx.NORMAL)
                    dc.SetFont(font)
                    dc.SetPen(fgrPen)
                    dc.DrawLine(w+wo+2, pst, w+wo+2, IC_NB_HEIGHT-pst)
                    dc.SetTextForeground(fgr)
                    dc.DrawText(obj.title, w+obj.step_text, (IC_NB_HEIGHT - obj.GetHeight())/2+pst+2)
                
                    if obj.GetImage():
                        obj.GetImage().Show(True)
                        obj.GetImage().SetBackgroundColour(bgr)
                        obj.GetImage().SetPosition((w+IC_NB_STEP, pst+2))
                    
                w += wo
            elif obj.GetImage():
                obj.GetImage().Show(False)

        # Компоненты навигации
        dc.SetPen(fgrPen)

        #   Список не видемых компонентов
        if self.GetFirstVisible() > 0 or bCanNext:
            dc.SetBrush(bgrBrush)
            dc.DrawRectangle(sx - IC_NB_SERV_ZONE + 2, (IC_NB_HEIGHT - 8)/2-1, 13, 12)
            dc.SetBrush(fgrBrush)
            dc.DrawPolygon([(0, 0), (8, 0), (4, 4), (0, 0)],
                           sx - IC_NB_SERV_ZONE+4, (IC_NB_HEIGHT - 8)/2+3)
        # Next
        if bCanNext:
            dc.SetBrush(fgrBrush)
            self._canNext = True
        else:
            dc.SetBrush(bgrBrush)
            self._canNext = False
            
        dc.DrawPolygon(NextPointsDark, sx - IC_NB_SERV_ZONE + 28, (IC_NB_HEIGHT - 8)/2)

        # Prev
        if self.GetFirstVisible() > 0:
            dc.SetBrush(fgrBrush)
            self._canPrev = True
        else:
            dc.SetBrush(bgrBrush)
            self._canPrev = False

        dc.DrawPolygon(PrevPointsDark, sx - IC_NB_SERV_ZONE+19, (IC_NB_HEIGHT - 8)/2)
        dc.EndDrawing()
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        width, height = self.GetClientSize()

        if not width or not height:
            return

        self.Draw(dc)

    def SetStatusVisible(self, bVisible=True, lst=None):
        """
        Функция устанавливает признак, по которому программа определяет нужно ли
        данному компоненту обновлять представление при изменении данных. Например,
        для всех объектов неактивной страницы органайзера этот признак будет устана-
        вливаться в False. Для компонента 'icNotebook' эта функция переопределена
        т. к. только на активной странице компоненты видимы.
        @type bVisual: C{bool}
        @param bVisual: Признак обновления представления объекта данных.
        @type lst: C{list}
        @param lst: Список видимых объектов.
        @rtype: C{list}
        @return: Список видимых объектов.
        """
        self.bStatusVisible = bVisible
        if lst is None:
            lst = []
        if bVisible:
            lst.append(self.name)
        try:
            id_page = self.GetSelected()
            winLst = self.GetTitlesList[id_page].GetConnectedObj()
            #   Устанавливаем у дочерних объектов такой же признак видимости
            for child in self.GetConnectedObjLst():
                if bVisible:
                    try:
                        if self.components[child] in winLst:
                            self.components[child].SetStatusVisible(True, lst)
                        else:
                            self.components[child].SetStatusVisible(False, lst)
                    except:
                        pass
                else:
                    try:
                        self.components[child].SetStatusVisible(False, lst)
                    except:
                        pass
        except:
            pass
    
        return lst


def test(par=0):
    """
    Тестируем пользовательский класс.
    @type par: C{int}
    @param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    app = ictestapp.TestApp(par)
    common.img_init()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    win.SetBackgroundColour(wx.Colour(100, 100, 100))
    
    nb = icTitlesNotebook(win, -1, {'position': (10, 10),
                          'size': (310, 50),
                          'foregroundColor': (120, 120, 100),
                          'backgroundColor': (240, 240, 240),
                          'titles': ['first page', 'second', 'third', 'forth'],
                          'onSelectTitle': 'print \'OnSelect->\', self.GetSelected()',
                          'path': 'C:/Python23/Lib/site-packages/ic/imglib/common/',
                          'images': ['py_src.png', 'blankCorel.png'],
                          'font': {'style': 'regular', 'size': 8, 'underline': False, 'faceName': 'MS Sans Serif', 'family': 'sansSerif'}})

    nb.GetTitle(0).SetDescription('Short Help for <First>')
    nb.GetTitle(1).SetDescription('Short Help for <2>')
    nb.GetTitle(2).SetDescription('Short Help for <3>')
    nb.SetFirstVisible(0)
    nb.selPageColor = graphicUtils.GetMidColor(win.GetBackgroundColour(), wx.Colour(0, 0, 0), 0.15)
    clr = graphicUtils.GetMidColor(win.GetBackgroundColour(), wx.Colour(255, 255, 255), 0.5)
    nb.SetBackgroundColour(clr)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
