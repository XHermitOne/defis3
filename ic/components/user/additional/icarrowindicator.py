#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Стрелочный индикатор.
Класс пользовательского визуального компонента.

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

import time
import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import ic.components.icfont as icfont
import ic.components.custom.icheadcell as icheadcell
import ic.components.user.objects.icarrowindicatortrend as icarrowindicatortrend
import ic.components.user.icArrowIndDef as indDef
import ic.bitmap.icbitmap as icbitmap
import ic.utils.graphicUtils as graphicUtils

from ic.db import icsqlalchemy
import ic.dlg.msgbox as msgbox
from ic.log import log
import ic

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icArrowIndicator'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ArrowIndicator',
                'name': 'default',
                'label': u'Подпись',
                'typPar': '',
                'cod': '',
                'aggregationType': 'USUAL',
                'aggregationFunc': 'SUM',
                'majorValues': '(0,10)',
                'majorLabels': None,
                'minorValues': None,
                'ei': '',
                'factor': 1,
                'value': None,
                'periodIzm': None,
                'colorRegions': '[(\'100%\', \'BLUE\')]',
                'font': {},
                'shortHelpString': u'Индикатор',
                'layout': 'horizontal',
                'attrTime': None,
                'attrVal': None,
                'attrPlan': None,
                'structQuery': {},
                'onGraph': None,
                'onColor': None,
                'onSaveProperty': None,
                'onLeftDblClick': None,
                '__styles__': ic_class_styles,
                '__events__': {'onGraph': ('wx.EVT_LEFT_DOWN', 'OnGraphClick', False),
                               'onLeftDblClick': ('wx.EVT_LEFT_DCLICK', 'OnLeftDblClick', False),
                               'onColor': ('wx.EVT_LEFT_DOWN', 'OnColorClick', False),
                               'onSaveProperty': ('wx.EVT_RIGHT_DOWN', 'OnRightDown', False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'typPar', 'cod'],
                                   icDefInf.EDT_NUMBER: ['factor'],
                                   icDefInf.EDT_CHOICE: ['aggregationType', 'aggregation'],
                                   icDefInf.EDT_TEXTDICT: ['structQuery'],
                                   },
                '__lists__': {'aggregationType': (u'Обычный', u'День', u'Месяц', u'Квартал', u'Год'),
                              'aggregationFunc': ('SUM', ),
                              },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgArrowIndicator'
ic_class_pic2 = '@common.imgArrowIndicator'

#   Путь до файла документации
ic_class_doc = 'public/icarrowindicator.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)

# --- Описываем константы, которые используются для рисования шкалы
#   Сдвиг шкалы от начала координат контрола
SHIFT_X_HORIZ = 20
SHIFT_Y_HORIZ = 30
SHIFT_Y_LABEL = 3

#   Высота мажорной разметки
H_MAJOR = 12
#   Высота минорной разметки
H_MINOR = 7
#   Высота области цветовой индикации
H_COLOR_REG = 10
WIDTH_BTN = 15
HEIGHT_BTN = 10
WIDTH_GRPH_BTN = 15
HEIGHT_GRPH_BTN = 10

#   Типы представлений индикатора
#   Индикатор со шкалой
LINE_TYPE_PREDST = 0
#   Индикатор в виде цветной кнопки
BRIEF_TYPE_PREDST = 1
#   Индикатор в виде текста и рядом цветовой кнопкой
TEXT_TYPE_PREDST = 2

#   Описания типов накопления
AGR_TYPE_USUAL = indDef.AGR_TYPE_USUAL
AGR_TYPE_DAY = indDef.AGR_TYPE_DAY
AGR_TYPE_MONTH = indDef.AGR_TYPE_MONTH
AGR_TYPE_QUARTER = indDef.AGR_TYPE_QUARTER
AGR_TYPE_YEAR = indDef.AGR_TYPE_YEAR
AGR_TYPE_PERIOD = indDef.AGR_TYPE_PERIOD
                        
aggregationTypeDict = indDef.aggregationTypeDict
                        
#   Описание функций накопления
AGR_FUNC_SUM = indDef.AGR_FUNC_SUM
AGR_FUNC_MIN = indDef.AGR_FUNC_MIN
AGR_FUNC_MAX = indDef.AGR_FUNC_MAX
AGR_FUNC_AVRG = indDef.AGR_FUNC_AVRG
AGR_FUNC_DISP = indDef.AGR_FUNC_DISP

aggregationFuncDict = indDef.aggregationFuncDict


# --- Функции агрегации
def _get_day_plan(date, cod):
    """
    """
    return 2000000.0

aggregationFuncMap = indDef.aggregationFuncMap

#   Словарь соответствий месяцов определенному кварталу
ic_month_qwart_indx = indDef.ic_month_qwart_indx


class icIndicatorSkin:
    """
    Скины индикатора.
    """
    def __init__(self, skinName, path=None):
        """
        Конструктор скина.
        """
        #   Путь до папки с картинками скина
        self.path = path
        
        #   Имя скина
        self.name = skinName

        #   Картинки для фонов заголовка в разных режимах (развернутом/свернутом)
        self.bmpTitleBgr = None
        self.bmpTitleBgr2 = None

        #   Картинка для фона индикатора
        self.bmpBgr = None
        
        #   Картинки для кнопки открытия графика
        self.bmpGraphBtnPic = None
        self.bmpGraphBtnPic2 = None

        #   Картинки для кнопки разварачивания/сварачивания индикатора
        self.bmpClrBtnPic = None
        self.bmpClrBtnPic2 = None

        #   Область кнопки разварачивания/сварачивания
        self.regClrBtn = None
        #   Область кнопки вызова графика
        self.regGraphBtn = None
        
        #   Шрифт множителя
        self.factorFont = None
        
    def createBmp(self, file):
        """
        Создаем объект картинки.
        """
        return wx.Image(file, icbitmap.icBitmapType(file)).ConvertToBitmap()
    
    def Load(self):
        """
        """
        pass

    def Draw(self, dc, indicator):
        """
        """
        pass
    
    def DrawTextMode(self, dc, indicator):
        """
        """
        pass


class icClassicSkin(icIndicatorSkin):
    """
    Скины индикатора.
    """
    def __init__(self, path=None):
        """
        Конструктор скина.
        """
        if not path:
            path = ic.__file__.replace('__init__.pyo',
                                       '__init__.pyc').replace('__init__.pyc',
                                                               'components/user/IndicatorSkins/Classic/')
        icIndicatorSkin.__init__(self, 'Classic', path)
        self._isLoad = self.Load()
        
    def isLoad(self):
        """
        """
        return self._isLoad
        
    def Load(self, path=None):
        """
        """
        if not path:
            path = self.path

        try:
            #   Картинки для фонов заголовка в разных режимах (развернутом/свернутом)
            self.bmpTitleBgr = self.createBmp(path + 'title2.png')

            #   Картинка для фона индикатора
            self.bmpBgr = self.createBmp(path + 'indBgrPic3.png')
            
            #   Картинки для кнопки открытия графика
            self.bmpGraphBtnPic = self.createBmp(path + 'graphPicBtn.png')
            self.bmpGraphBtnPic2 = None
    
            self.bmpClrBtnPic = self.createBmp(path + 'clrPic.png')
            
            self.factorFont = icfont.icFont({'size': 8})

            return True
        except:
            return False
    
    def _drawTittleBtn(self, dc, indicator, dq=0):
        """
        Отрисовывает специальные кнопки.
        """
        clr = indicator.GetValColor()
        pen = wx.Pen(clr)
        dc.SetPen(pen)
        br = wx.Brush(clr)
        dc.SetBrush(br)
        sx, sy = indicator.GetSize()
        
        dx = 3
        lx = sx - self.bmpClrBtnPic.GetWidth() - self.bmpGraphBtnPic.GetWidth()+dq - dx
        ly = (23 - self.bmpClrBtnPic.GetWidth())/2+dq
        dc.DrawEllipse(lx, ly,
                       self.bmpClrBtnPic.GetWidth()-2*dq, self.bmpClrBtnPic.GetHeight()-2*dq)
        
        #   Подрисовываем
        dc.DrawLine(lx + self.bmpClrBtnPic.GetWidth()/2 - 4, ly,
                    lx + self.bmpClrBtnPic.GetWidth()/2 + 2, ly)
        
        dc.DrawLine(lx, ly+self.bmpClrBtnPic.GetHeight()/2-3,
                    lx, ly+self.bmpClrBtnPic.GetHeight()/2+2)

        lly = ly+self.bmpClrBtnPic.GetHeight()-3
        dc.DrawLine(lx + self.bmpClrBtnPic.GetWidth()/2 - 4, lly,
                    lx + self.bmpClrBtnPic.GetWidth()/2 + 2, lly)

        lx += self.bmpClrBtnPic.GetWidth()-3
        dc.DrawLine(lx, ly+self.bmpClrBtnPic.GetHeight()/2-3,
                    lx, ly+self.bmpClrBtnPic.GetHeight()/2+2)
                
        dc.DrawBitmap(self.bmpClrBtnPic, sx - dx - self.bmpClrBtnPic.GetWidth() - self.bmpGraphBtnPic.GetWidth(),
                      (23 - self.bmpClrBtnPic.GetWidth())/2, True)

        dc.DrawBitmap(self.bmpGraphBtnPic, 1 + sx - dx - self.bmpGraphBtnPic.GetWidth(),
                      (23 - self.bmpGraphBtnPic.GetWidth())/2+2, True)
        
    def Draw(self, dc, indicator):
        """
        Функция рисует индикатор.

        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        """
        dc.BeginDrawing()

        clr = indicator.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        
        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            backBrush.SetMacTheme(1)

        dc.SetBackground(backBrush)
        dc.SetTextForeground(indicator.GetForegroundColour())
        sx, sy = indicator.GetSize()

        if self.bmpBgr:
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmpBgr)

            for n in range(int(sx/self.bmpBgr.GetWidth())+1):
                dc.Blit(n*self.bmpBgr.GetWidth(), 0, self.bmpBgr.GetWidth(),
                        self.bmpBgr.GetHeight(), memDC, 0, 0, wx.COPY, True)
        else:
            dc.Clear()

        # --- Скругленные углы
        clr_ = (150, 150, 170)
        pen = wx.Pen(clr_)
        dc.SetPen(pen)
        dc.DrawLine(0, 0, 0, sy)
        dc.DrawLine(sx-1, 0, sx-1, sy)
        dc.DrawLine(0, 0, sx-1, 0)
        dc.DrawLine(0, sy-1, sx-1, sy-1)

        graphicUtils.drawRoundCorners(dc, indicator.GetClientSize(),
                                      indicator.GetForegroundColour(), indicator.GetBackgroundColour(),
                                      indicator.GetParent().GetBackgroundColour(), 0,
                                      (clr_, clr_, clr_, clr_),
                                      (1, 1, 1, 1), 0)

        width, height = indicator.GetClientSize()
        dc.SetFont(indicator.GetFont())
        label = indicator.GetLabel()
        style = indicator.GetWindowStyleFlag()
                
        # --- Рисуем шкалу индикатора
        sx, sy = indicator.GetSize()
        dx = SHIFT_X_HORIZ
        dy = SHIFT_Y_HORIZ+ H_MAJOR/2
        
        majorLst = indicator.majorValues
        
        if not indicator.majorLabels:
            labelLst = indicator.majorValues
        else:
            labelLst = indicator.majorLabels
            
        minorLst = indicator.minorValues
        clrLst = indicator.colorRegions

        max = indicator.GetMaxValue()
        min = indicator.GetMinValue()
        
        if indicator.GetValue():
            cursor = indicator.GetValue()/indicator.factor
        else:
            cursor = min
        
        # --- Рисуем цветовые индикаторы
        x = SHIFT_X_HORIZ
        h = H_MAJOR/2
        old = 0
        y = dy
        
        for i, obj in enumerate(clrLst):
            val, clr = obj
            
            if type(val) in (str, unicode):
                v = float(val.replace('%', ''))
                if v > 100:
                    v = 100
                val = (max-min)*v/100
                
            val = val * indicator._planFactor
            br = wx.Brush(clr)
            dc.SetBrush(br)
            pen = wx.Pen(clr)
            dc.SetPen(pen)
            w = (sx - 2*dx)*(val-old)/(max - min)
            
            if i == len(clrLst)-1:
                w = (sx - dx) - x
            dc.DrawRectangle(x, y, w+1, h)

            x += w
            old = val
        
        # --- Рисуем текущее значение индикатора
        clr_cur = (0, 0, 0)
        br = wx.Brush(clr_cur)
        dc.SetBrush(br)
        pen = wx.Pen(clr_cur)
        dc.SetPen(pen)
        
        if cursor > max:
            cursor = max
        
        if cursor > min and min != max:
            w = (sx - 2*dx)*(cursor-min)/(max - min)+1
            dc.DrawRectangle(dx, dy-h, w, h)

        pen = wx.Pen((0, 0, 0))
        dc.SetPen(pen)
        br = wx.Brush((255, 255, 255), wx.TRANSPARENT)
        dc.SetBrush(br)
        w = (sx - 2*dx)
        dc.DrawRectangle(dx, dy-h, w+1, h+1)
        
        # --- Рисуем основную ось
        dc.SetTextForeground((0, 0, 0))
        br = wx.Brush(indicator.indicatorColor)
        dc.SetBrush(br)
        dc.DrawLine(dx, dy, sx - dx, dy)
        
        # --- Рисуем мажорную сетку
        dp = float((sx - 2.0*dx)/(len(majorLst)-1.0))
        w, h = indicator.GetTextExtent('o')
        
        for indx, val in enumerate(majorLst):
            dc.DrawLine(dx+dp*indx, dy-H_MAJOR/2, dx+dp*indx, dy+H_MAJOR/2)
            
            if indx < len(labelLst):
                if isinstance(labelLst[indx], float):
                    l = ('%1.1f' % labelLst[indx]).replace('.0', '')
                else:
                    l = str(labelLst[indx])
                    
                dc.DrawText(l, dx+dp*indx-w*len(l)/2, dy+H_MAJOR/2)
        
        # --- Рисуем минорную сетку
        dp = float((sx - 2.0*dx)/(len(minorLst)-1.0))
        for indx, val in enumerate(minorLst):
            dc.DrawLine(dx+dp*indx, dy-H_MINOR/2, dx+dp*indx, dy)

        # --- Рисуем положение планового значения
        pen = wx.Pen((250, 0, 0))
        dc.SetPen(pen)
        plan = indicator._planFactor*max/2
        cx = dx + (sx - 2*dx)*(plan-min)/(max - min)
        dc.DrawLine(cx, dy-H_MAJOR/2, cx, dy+H_MAJOR/2)

        # --- Рисуем заголовок
        dx = (sx - w*len(label))/2
        dc.SetTextForeground(indicator.foregroundColor)
        dc.DrawText(label, dx, SHIFT_Y_LABEL)

        # --- Рисуем множитель
        if self.factorFont:
            dc.SetTextForeground((0, 0, 0))
            dc.SetFont(self.factorFont)
        
        if indicator.factor > 1:
            dx = (sx - w*len(str(indicator.factor)))/2
            dc.DrawText('x '+str(indicator.factor).replace('000', ' 000'), dx, SHIFT_Y_LABEL + 14)
            
        # --- Рисуем светофор
        clr_pen = (255, 255, 255)
        self._drawTittleBtn(dc, indicator, 1)
        
        dc.EndDrawing()

    def DrawTextMode(self, dc, indicator):
        """
        Отрисовывает индикатор в свернутом режиме.
        """
        dc.BeginDrawing()
        clr = indicator.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        
        if wx.Platform == '__WXMAC__' and clr == indicator.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1)

        dc.SetBackground(backBrush)
        dc.Clear()
        sx, sy = indicator.GetSize()
        
        if self.bmpTitleBgr:
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmpTitleBgr)

            for n in range(int(sx/self.bmpTitleBgr.GetWidth())+1):
                dc.Blit(n*self.bmpTitleBgr.GetWidth(), 0, self.bmpTitleBgr.GetWidth(),
                        self.bmpTitleBgr.GetHeight(), memDC, 0, 0, wx.COPY, True)
        else:
            dc.Clear()
        
        # --- Скругленные углы
        clr_ = (100, 100, 200)
        pen = wx.Pen(clr_)
        dc.SetPen(pen)
        dc.DrawLine(0, 0, 0, sy)
        dc.DrawLine(sx-1, 0, sx-1, sy)
        graphicUtils.drawRoundCorners(dc, indicator.GetClientSize(),
                                      indicator.GetForegroundColour(), indicator.GetBackgroundColour(),
                                      indicator.GetParent().GetBackgroundColour(), 0,
                                      ((100, 100, 200), (100, 100, 200), (100, 100, 200), (100, 100, 200)),
                                      (1, 1, 1, 1), 0)
                
        w, h = indicator.GetTextExtent('o')
        label = indicator.GetLabel()
        
        # --- Рисуем заголовок
        dx = 10
        dc.SetFont(indicator.GetFont())
        dc.SetTextForeground(indicator.foregroundColor)
        dc.DrawText(label, dx, SHIFT_Y_LABEL)
        
        # --- Рисуем светофор
        clr_pen = (100, 100, 100)
        self._drawTittleBtn(dc, indicator, 1)

        self.regClrBtn = wx.Rect(sx - self.bmpClrBtnPic.GetWidth() - self.bmpGraphBtnPic.GetWidth(), 0,
                                 self.bmpClrBtnPic.GetWidth(), self.bmpClrBtnPic.GetHeight())
        self.regGraphBtn = wx.Rect(sx-self.bmpGraphBtnPic.GetWidth(), 0,
                                   self.bmpGraphBtnPic.GetWidth(), self.bmpGraphBtnPic.GetHeight())

        dc.EndDrawing()


def _getColor(clr):
    """
    """
    if type(clr) in (str, unicode):
        try:
            clr = getattr(wx, clr)
        #
        except:
            log.fatal(u'INVALID COLOR NAME <%s> in _getColor()' % clr)
            return None
    return clr


def GetValColor(value, min, max, clrReg, planFactor=1):
    """
    Возвращает цвет зоны значения индикатора.

    @type value: C{float}
    @param value: Значение индикатора.
    @type min: C{float}
    @param min: Минимальное значение шкалы индикатора.
    @type max: C{float}
    @param max: Максимальное значение шкалы индикатора.
    @type clrReg: C{list}
    @param clrReg: Описание цветовых зон. Первый элемент списка - значение
        правой границы зоны, второй элемент описание цвета зоны. Описание
        зоны должно быть в виде кортежа (rr, gg, bb) название цвета, принятое
        в библиотеке wx.
        Пример:[('40%', 'RED'), ('50%', (255, 200, 0)),('100%', 'GREEN')]
    """
    if value > max:
        clr = clrReg[-1][1]
        return _getColor(clr)
        
    if clrReg and max is not None and min is not None and value:
        for v, clr in clrReg:
            if type(v) in (str, unicode):
                v = float(v.replace('%', ''))
                if v > 100:
                    v = 100
                v = planFactor*(max-min)*(v-min)/100
            if value <= v:
                return _getColor(clr)

        clr = clrReg[-1][1]
        return _getColor(clr)


def GetStateIndx(value, min, max, clrReg, planFactor=1):
    """
    Возвращает индекс зоны, соответствующей значению.

    @type value: C{float}
    @param value: Значение индикатора.
    @type min: C{float}
    @param min: Минимальное значение шкалы индикатора.
    @type max: C{float}
    @param max: Максимальное значение шкалы индикатора.
    @type clrReg: C{list}
    @param clrReg: Описание цветовых зон. Первый элемент списка - значение
        правой границы зоны, второй элемент описание цвета зоны. Описание
        зоны должно быть в виде кортежа (rr, gg, bb) название цвета, принятое
        в библиотеке wx.
        Пример:[('40%', 'RED'), ('50%', (255, 200, 0)),('100%', 'GREEN')]
    """
    if value > max:
        return len(clrReg) - 1
        
    if clrReg and max is not None and min is not None and value:
        for indx, r in enumerate(clrReg):
            v, clr = r
            if type(v) in (str, unicode):
                v = float(v.replace('%', ''))
                if v > 100:
                    v = 100
                v = planFactor*(max-min)*(v-min)/100
            if value <= v:
                return indx

        return len(clrReg) - 1
        
    return 0


class icArrowIndicator(icwidget.icWidget, wx.PyControl):
    """
    Стрелочный индикатора финансовых показателей. Компонент может работать в двух
    режимах: 1- отображения данных таблицы; 2-отображения агрегированных данных.
    В первом случае по происходит привязка к компоненту icSQLObjDataset. Компонент
    отображает значение поля в строке, определяемой курсором. Во стором случае
    компонент привязывается непосредственно к классу данных. При вызове функции
    RefreshState() компонент формирует запрос через механизм SQLObject к источнику
    данных и обновляет свое состояние. При наличии плановых значений состояния
    индикатора происходит автоматический пересчет максимального значения шкалы
    индикатора такми образом, чтобы плановому значению соответствовала середина
    шкалы (это сделано для того, чтобы не пересчитывать цветовые зоны индикатора,
    которые задаются в %).
    
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='ArrowIndicator'}:
        - B{name='default'}:
        - B{typPar=''}: Тип наблюдаемого параметра (см описание атрибута 'cod').
        - B{cod=''}: Код наблюдаемого параметра. Наблюдаемые параметры описываются в
            стандартном справочнике типом и кодом. Тип и код нужен для того, чтобы
            получить информацию о плановых значениях параметра.
        - B{label='Подпись'}: Подписи индикатора.
        - B(majorValues=None}: Список значений мажорной сетки. Вычисляемый атрибут.
            Пример: @[0, 10, 20, 30, 40]
        - B(majorLabels=None}: Список отметок мажорной сетки. Вычисляемый атрибут.
            Пример: @[0, 5, 10, 15, 20, 25, 30, 35, 40]
        - B{minorValues=None}: Список значений минорной сетки. Вычисляемый атрибут.
            Пример: @['A', 'B', 'C', 'D', 'E']
        - B{minorLabels=None}: Список отметок минорной сетки. Вычисляемый атрибут.
        - B{ei=''}: Единицы измерения.
        - B{factor=1}: Множитель между показаниями и реальными значениями.
        - B{colorRegions=None}: Список описаний цветовых зон индикатора. Цветовая
            зона описывается картежем из двух элементов: 1 - значение правого края
            зоны (зону можно задавть также в % - значение должно быть стровым и в
            конце стоять символ '%');
            2 - цвет зоны. Цвет зоны определяется картежем (red, green, blue)
            либо символьным значением цвета: 'RED', 'BLUE', 'GREEN', 'BLACK',
            'YELLOW', 'WHITE', 'CYAN', 'GREY';
            Пример 1: ((20, 'GREEN'), (32, 'GREY'), (50, (250, 0, 0)))
            Пример 1: ((20%, 'GREEN'), ('70%', 'GREY'), ('100%', (250, 0, 0)))
            
        - B{font={}}: Шрифт подписей индикатора.
        - B{attrVal=None}: Атрибут значения.
        - B{attrPlan=None}: Атрибут планового значения.
        - B{aggregationType='USUAL'}: Тип накопления данных:
            'USUAL' - Без накопления;
            'DAY' - Накопления за один день;
            'MONTH' - За месяц;
            'QUARTER' - За квартал;
            'YEAR' - За год.
        - B{aggregationFunc='SUM'}: Функция накопления.
        - B{structQuery={}}: Структурный запрос; ключ - имя поля таблицы, к
            которой подключен индикатор; значение - значение поля, по которому
            отираются записи для отображения.
        - B{layout='horizontal'}: Вид индикатора (вертикальный/горизонтальный).
        - B{onGraph=None}: Выражение, выполняемое после нажатия указателя на график.
        - B{onSaveProperty=None}: Выражение, выполняемое для того, чтобы сохранить
            настройки индикатора. Если данный атрибут определен, то при нажатии
            правой кнопки мыши вызывается окно настроек индикатора.
        - B{onLeftDblClick=None}: Выражение, выполняемое при получении сообщения
            <wx.EVT_LEFT_DCLICK>
        - B{periodIzm=[]}: Выражение, определяющее период измерения и накопления
            значения параметра, который отображает индикатор. Период определяется
            списком из двух элементов [<начало периода>, <конец периода>]. Если
            в качестве первого элемента стоит None, то список определяет до какого
            времени ведется накопление, если None вторым элементом, то с какого
            времени.
            Пример 1: ['2005.05.10', '2005.10.31']
            Пример 2: [None, '2005.10.31']
            Пример 3: [None, None]
            
        - B{source=None}: Имя источника данных.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType = 0, evalSpace = None,
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
        component = util.icSpcDefStruct(icArrowIndicator.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        self.periodIzm = self.countAttr('periodIzm')
        
        #   Если период не определен, то считаем что период изм. [None, time.now()]
        if not self.periodIzm:
            tt = time.gmtime()
            mm = ('00'+str(tt[1]))[-2:]
            dd = ('00'+str(tt[2]))[-2:]
            self.periodIzm = [None, '%s.%s.%s' % (tt[0], mm, dd)]
        
        self.label = self.getICAttr('label')
        self.attrVal = self.getICAttr('attrVal')
        self.attrPlan = self.getICAttr('attrPlan')
        self.attrTime = self.getICAttr('attrTime')
        
        if not self.label:
            self.label = ''
            
        #   Внутренние переменные
        self._helpWin = None
        self.indicatorColor = (0, 0, 0)
        #   Указатель на интерфэйс класса данных
        self._dataclassI = None
        #   Указатель на функцию опрделяющую дневные планы наблюдаемого параметра
        self._dayPlanFunc = None
        #   Поправочный параметр, для определения планового значения
        #   определяется как max/(2*plan)
        self._planFactor = 1
        
        #   Статистика
        self._statistic = None
        #   Картеж описания функции сбора статистики
        #   первый элемент - функция
        #   второй         - *arg
        #   третий         - **kwarg
        self._statisticFuncPar = None
        
        #   Указатель на скин индикатора
        self.skin = icClassicSkin()
        if not self.skin.isLoad():
            self.skin = None
            
        #   Значение индикатора
        self._value = self.countAttr('value')
        if not self._value:
            self._value = 0
            
        self.majorValues = self.countAttr('majorValues')
        self.minorValues = self.countAttr('minorValues')
        self.majorLabels = self.countAttr('majorLabels')
        self.colorRegions = self.countAttr('colorRegions')
        log.debug(u'factor type = <%s>' % type(self.factor))
        
        if not self.majorValues:
            self.majorValues = []

        if not self.minorValues:
            self.minorValues = []

        if not self.majorLabels:
            self.majorLabels = []

        if not self.colorRegions:
            self.colorRegions = []
            
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        style = wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE | wx.NO_BORDER
        wx.PyControl.__init__(self, parent, id, self.position, self.size, style, name=self.name)
        
        #   Устанавливаем подпись
        self.SetLabel(self.label)

        #   Тип представления:
        self._typePredst = 0

        #   Цвета текста и фона
        obj = icfont.icFont(self.font)
        self.SetFont(obj)
           
        if self.backgroundColor:
            self.SetBackgroundColour(self.backgroundColor)

        if self.foregroundColor:
            self.SetForegroundColour(self.foregroundColor)

        rw, rh = self.size
        bw, bh = self.GetBestSize()
        if rw == -1:
            rw = bw
        if rh == -1:
            rh = bh
        self.SetSize(wx.Size(rw, rh))
        self.SetTypePredst(2)
        
        # --- Регистрация обработчиков событий
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDblClick)
        
        self.BindICEvt()
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        #   Флаг блокировки перерисавывания компонента, используется
        #   если опрделен обработчик на событие <EVT_PAINT>. У данного
        #   компонента блокировка отменяется в обработчике сообщения
        #   <icEvents.EVT_POST_INIT>
        self._blockEvtPoint = False
        
    def aggregatePar(self, rs, t1=None, t2=None):
        """
        Функция накопления значений параметра за период.
        
        @type rs: C{SQLObject.Recordset}
        @param rs: Набор отобранных записей.
        @type t1: C{string}
        @param t1: Имя накапливаемого параметра.
        @type t2: C{string}
        @param t2: Имя накапливаемого параметра плана.
        """
        agr_func = self.GetAggregationFunc()
        log.debug(u'\tself.attrVal = <%s>' % self.attrVal)
        if agr_func in aggregationFuncMap:
            return aggregationFuncMap[agr_func](rs, self.attrTime, self.attrVal,
                                                self.attrPlan, t1, t2, self.cod, self.GetDayPlanFunc())
        else:
            log.warning(u'Invalid Func <%s> identificator' % agr_func)
        
        return None, None
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)

    def CreateIndicatorTrend(self):
        """
        """
        #   Создаем диалоговое окно с графиком динамики изменений значения индикатора
        if not self._statisticFuncPar and not self._statistic:
            msgbox.MsgBox(self, u'Нет данных')
            return
        
        cls = icarrowindicatortrend.ArrowIndicatorTrend(self, self)
        
        if self._statisticFuncPar:
            f, arg, kwarg = self._statisticFuncPar
            self._statistic = f(*arg, **kwarg)
        
        if self._statistic:
            cls.SetGraphFromData(self._statistic)

    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of the
        button based on the label size.
        """
        return self.GetSize()

    def Draw(self, dc):
        """
        Функция рисует индикатор.

        @type dc: C{wx.DC}
        @param dc: Контекст устройства.
        """
        if self._blockEvtPoint:
            return
        
        dc.BeginDrawing()

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        
        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1)

        dc.SetBackground(backBrush)
        dc.SetTextForeground(self.GetForegroundColour())
        dc.Clear()

        width, height = self.GetClientSize()
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        style = self.GetWindowStyleFlag()
                
        # --- Рисуем шкалу индикатора
        sx, sy = self.GetSize()
        dx = SHIFT_X_HORIZ
        dy = SHIFT_Y_HORIZ + H_MAJOR/2
        
        majorLst = self.majorValues
        
        if not self.majorLabels:
            labelLst = self.majorValues
        else:
            labelLst = self.majorLabels
            
        minorLst = self.minorValues
        clrLst = self.colorRegions

        max = self.GetMaxValue()
        min = self.GetMinValue()
        
        if self.GetValue():
            cursor = self.GetValue()/self.factor
        else:
            cursor = min
        
        # --- Рисуем цветовые индикаторы
        x = SHIFT_X_HORIZ
        h = H_MAJOR/2
        old = 0
        y = dy
        
        for obj in clrLst:
            val, clr = obj
            
            if type(val) in (str, unicode):
                v = float(val.replace('%', ''))
                if v > 100:
                    v = 100
                val = (max-min)*v/100
            val *= self._planFactor
            br = wx.Brush(clr)
            dc.SetBrush(br)
            pen = wx.Pen(clr)
            dc.SetPen(pen)
            
            w = (sx - 2*dx)*(val-old)/(max - min)
            
            if type(clr) in (str, unicode):
                _clr = getattr(wx, clr)
                icheadcell.DrawGradient(dc, w+1, h, _clr, icheadcell.BGR_GRAD_RIGHT, x, y, 2)
            else:
                icheadcell.DrawGradient(dc, w+1, h, wx.Colour(*clr), icheadcell.BGR_GRAD_RIGHT, x, y, 2)

            x += w
            old = val
        
        # --- Рисуем текущее значение индикатора
        clr_cur = (220, 220, 220)
        br = wx.Brush(clr_cur)
        dc.SetBrush(br)
        pen = wx.Pen(clr_cur)
        dc.SetPen(pen)
        
        if cursor > max:
            cursor = max
        
        if cursor > min and min != max:
            w = (sx - 2*dx)*(cursor-min)/(max - min)+1
            icheadcell.DrawGradient(dc, w, h, wx.Colour(clr_cur[0], clr_cur[1], clr_cur[2]),
                                    icheadcell.BGR_GRAD_LEFT, dx, dy-h, 0.2)

        pen = wx.Pen((0, 0, 0))
        dc.SetPen(pen)
        br = wx.Brush((255, 255, 255), wx.TRANSPARENT)
        dc.SetBrush(br)
        w = (sx - 2*dx)
        dc.DrawRectangle(dx, dy-h, w+1, h+1)
        
        # --- Рисуем основную ось
        dc.SetTextForeground((0, 0, 0))
        br = wx.Brush(self.indicatorColor)
        dc.SetBrush(br)
        dc.DrawLine(dx, dy, sx - dx, dy)
        
        # --- Рисуем мажорную сетку
        dp = float((sx - 2.0*dx)/(len(majorLst)-1.0))
        w, h = self.GetTextExtent('o')
        
        for indx, val in enumerate(majorLst):
            dc.DrawLine(dx+dp*indx, dy-H_MAJOR/2, dx+dp*indx, dy+H_MAJOR/2)
            
            if indx < len(labelLst):
                l = str(labelLst[indx])
                dc.DrawText(l, dx+dp*indx-w*len(l)/2, dy+H_MAJOR/2)

        # --- Рисуем минорную сетку
        dp = float((sx - 2.0*dx)/(len(minorLst)-1.0))
        for indx, val in enumerate(minorLst):
            dc.DrawLine(dx+dp*indx, dy-H_MINOR/2, dx+dp*indx, dy)
            
        # --- Рисуем заголовок
        dx = (sx - w*len(label))/2
        dc.SetTextForeground(self.foregroundColor)
        dc.DrawText(label, dx, SHIFT_Y_LABEL)
        
        # --- Рисуем светофор
        clr_pen = (0, 0, 0)
        clr = self.GetValColor()
        pen = wx.Pen(clr_pen)
        dc.SetPen(pen)
        br = wx.Brush(clr)
        dc.SetBrush(br)
        
        dc.DrawRectangle(sx - WIDTH_BTN - 18, SHIFT_Y_LABEL+2, WIDTH_BTN, HEIGHT_BTN)
        
        # ---  Рисуем указатель на график
        br = wx.Brush(self.backgroundColor)
        dc.SetBrush(br)
        dc.DrawRectangle(sx - WIDTH_BTN+4, SHIFT_Y_LABEL+2, WIDTH_GRPH_BTN, HEIGHT_GRPH_BTN)

        dc.DrawRectangle(sx - WIDTH_BTN+4+2, SHIFT_Y_LABEL+2 + 6, 2, 3)
        dc.DrawRectangle(sx - WIDTH_BTN+4+5, SHIFT_Y_LABEL+2+ 4, 2, 5)
        dc.DrawRectangle(sx - WIDTH_BTN+4+8, SHIFT_Y_LABEL+2+ 2, 2, 7)
        dc.EndDrawing()

    def DrawBriethMode(self, dc):
        """
        """
        if self._blockEvtPoint:
            return
        
        # --- Рисуем светофор
        dc.BeginDrawing()

        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        
        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1) # 1 == kThemeBrushDialogBackgroundActive

        dc.SetBackground(backBrush)
        dc.SetTextForeground(self.GetForegroundColour())
        dc.Clear()

        sx, sy = self.GetSize()
        clr_pen = (0, 0, 0)
        clr = self.GetValColor()
        pen = wx.Pen(clr_pen)
        dc.SetPen(pen)
        br = wx.Brush(clr)
        dc.SetBrush(br)
        
        dc.DrawRectangle(sx - WIDTH_BTN - 5, SHIFT_Y_LABEL, WIDTH_BTN, HEIGHT_BTN)
        dc.EndDrawing()

    def DrawTextMode(self, dc):
        """
        """
        if self._blockEvtPoint:
            return
            
        dc.BeginDrawing()
        clr = self.GetBackgroundColour()
        backBrush = wx.Brush(clr, wx.SOLID)
        
        if wx.Platform == '__WXMAC__' and clr == self.defBackClr:
            # if colour is still the default then use the striped background on Mac
            backBrush.SetMacTheme(1) # 1 == kThemeBrushDialogBackgroundActive

        dc.SetBackground(backBrush)
        dc.Clear()
        
        sx, sy = self.GetSize()
        w, h = self.GetTextExtent('o')
        label = self.GetLabel()
        
        # --- Рисуем заголовок
        dx = 10
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(self.foregroundColor)
        dc.DrawText(label, dx, SHIFT_Y_LABEL)
        
        # --- Рисуем светофор
        clr_pen = (0, 0, 0)
        clr = self.GetValColor()
        pen = wx.Pen(clr_pen)
        dc.SetPen(pen)
        br = wx.Brush(clr)
        dc.SetBrush(br)
        
        dc.DrawRectangle(sx - WIDTH_BTN - 18, SHIFT_Y_LABEL+2, WIDTH_BTN, HEIGHT_BTN)
        
        # ---  Рисуем указатель на график
        br = wx.Brush(self.backgroundColor)
        dc.SetBrush(br)
        dc.DrawRectangle(sx - WIDTH_BTN+4, SHIFT_Y_LABEL+2, WIDTH_GRPH_BTN, HEIGHT_GRPH_BTN)

        dc.DrawRectangle(sx - WIDTH_BTN+4+2, SHIFT_Y_LABEL+2 + 6, 2, 3)
        dc.DrawRectangle(sx - WIDTH_BTN+4+5, SHIFT_Y_LABEL+2+ 4, 2, 5)
        dc.DrawRectangle(sx - WIDTH_BTN+4+8, SHIFT_Y_LABEL+2+ 2, 2, 7)

        dc.EndDrawing()
   
    def GetAggregationType(self):
        """
        Возвращает тип агрегации данных.
        """
        if self.aggregationType in aggregationTypeDict:
            ret = aggregationTypeDict[self.aggregationType]
        else:
            ret = self.aggregationType = AGR_TYPE_USUAL
            
        return ret

    def GetAggregationTypeDict(self):
        """
        Возвращает тип агрегации данных.
        """
        return aggregationTypeDict

    def GetAggregationFunc(self):
        """
        Возвращает тип функции агрегации данных.
        """
        if self.aggregationFunc in aggregationFuncDict:
            ret = aggregationFuncDict[self.aggregationFunc]
        else:
            ret = self.aggregationFunc = AGR_FUNC_SUM

        return ret

    def GetAggregationFuncDict(self):
        """
        Возвращает тип агрегации данных.
        """
        return aggregationFuncDict
    
    def GetDayPlanFunc(self):
        """
        Возвращает ссылку на функцию дневных планов.
        """
        return self._dayPlanFunc
        
    def GetPeriodIzm(self):
        """
        Возвращет время измерерния.
        """
        return self.periodIzm
    
    def GetIDataclass(self):
        """
        Возвращает интерфейс на класс данных.
        """
        if self.source in (None, '', 'None'):
            return None
            
        if self.dataset:
            return self.dataset.dataclassInterface
        elif self._dataclassI:
            return self._dataclassI
        else:
            log.debug(u'\tCreateDataclass <%s>' % self.source)
            self._dataclassI = icsqlalchemy.icSQLAlchemyTabClass(self.source)
            return self._dataclassI
        
    def GetMaxValue(self):
        """
        Возвращает максимальное значение шкалы индикатора.
        """
        if self.majorValues:
            max = self.majorValues[-1]
        else:
            max = None

        return max

    def GetMinValue(self):
        """
        Возвращает максимальное значение шкалы индикатора.
        """
        if self.majorValues:
            min = self.majorValues[0]
        else:
            min = None

        return min
        
    def GetRecordset(self, t1=None, t2=None):
        """
        Возвращает набор записей отобранных из класса данных по заданному периоду.
        
        @rtype: C{SQLObject.main.SelectResults}
        @return: Возвращаем список отобранных записей.
        """
        cls = self.GetIDataclass()
        
        if cls:
            rs = None
            tfld = self.attrTime
            
            if tfld in ('', None, 'None'):
                log.warning(u'INDICATOR ERROR; NOT DEFINE DATE ATTRIBUTE')
                return None
                
            if not t1 or not t2:
                aggr_typ = self.GetAggregationType()
                
                #   Определяем период запроса
                ret = self.getQueryPeriod()
                if ret:
                    t1, t2 = ret
                else:
                    return None

            if t1 == t2:
                s = 'cls.q.%s==\'%s\',' % (tfld, t1)
            else:
                s = 'cls.q.%s>=\'%s\',cls.q.%s<=\'%s\',' % (tfld, t1, tfld, t2)
            
            if self.structQuery:
                s = ''
                for key, val in self.structQuery.items():
                    s = '%scls.q.%s==%s,' % (s, key, val)
                
                #   Делаем запрос
                rs = eval('cls.select(AND(%s), orderBy=cls.q.%s)' % (s[:-1], self.attrTime))
            else:
                if t1 == t2:
                    log.debug(u'Indicator QUERY cls.select(%s), <%s>' % (s[:-1], t1))
                    rs = eval('cls.select(%s, orderBy=cls.q.%s)' % (s[:-1], self.attrTime))
                else:
                    log.debug(u'Indicator QUERY cls.select(AND(%s)), <%s>' % (s[:-1], t1))
                    rs = eval('cls.select(AND(%s), orderBy=cls.q.%s)' % (s[:-1], self.attrTime))

            return rs
            
    def GetValColor(self):
        """
        Возвращает цвет зоны значения индикатора.
        """
        max = self.GetMaxValue()
        min = self.GetMinValue()

        if self.colorRegions and max is not None and min is not None and self.GetValue():
            val = self.GetValue()/self.factor
            return GetValColor(val, min, max, self.colorRegions, self._planFactor)
        else:
            return self.backgroundColor

    def GetValue(self):
        """
        Возвращает значение индикатора.
        """
        return self._value
        
    def GetTimeField(self):
        """
        Возвращает имя поля для хранения временного параметра.
        """
        return self.attrTime
        
    def GetTypePredst(self):
        """
        Возвращает тип представления.
        """
        return self._typePredst

    def getQueryPeriod(self):
        """
        """
        per = beg, end = self.GetPeriodIzm()
        aggr_typ = self.GetAggregationType()
        t1, t2 = None, None
        
        if aggr_typ in (AGR_TYPE_DAY, AGR_TYPE_USUAL):
            if end:
                t1 = t2 = end
            elif not end and beg:
                t1 = t2 = beg
            else:
                log.warning(u'INVALID PERIOD %s in RefreshState' % str(per))
                return None
                
        elif aggr_typ == AGR_TYPE_PERIOD:
            t1, t2 = beg, end
            
        elif aggr_typ == AGR_TYPE_MONTH:
            year = end[:4]
            mnth = end[5:7]
            t1 = '%s.%s.%s' % (year, mnth, '01')
            t2 = end
            
        elif aggr_typ == AGR_TYPE_QUARTER:
            year = end[:4]
            mnth = end[5:7]
            
            #   I квартал
            if int(mnth) in (1, 2, 3):
                t1 = '%s.%s.%s' % (year, '01', '01')
                t2 = end
            #   II квартал
            elif int(mnth) in (4, 5, 6):
                t1 = '%s.%s.%s' % (year, '04', '01')
                t2 = end
            #   III квартал
            elif int(mnth) in (7, 8, 9):
                t1 = '%s.%s.%s' % (year, '07', '01')
                t2 = end
            #   IV квартал
            elif int(mnth) in (10, 11, 12):
                t1 = '%s.%s.%s' % (year, '10', '01')
                t2 = end

        elif aggr_typ == AGR_TYPE_YEAR:
            year = end[:4]
            t1 = '%s.%s.%s' % (year, '01', '01')
            t2 = end
            
        return t1, t2
        
    # --- Обработчики событий
    def OnInit(self, evt):
        """
        Обрабатываем сообщение <icEvents.EVT_POST_INIT>.
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('onInit')
        evt.Skip()
        self._blockEvtPoint = False
        
    def OnMove(self, evt):
        """
        Обработка сообщения <wx.EVT_MOTION>.
        """
        x, y = self.GetPosition()
        sx, sy = self.GetSize()
        
        px,py = p = evt.GetPosition()
        d = 5
        r = wx.Rect(d, d, sx-2*d, sy-2*d)

        #   Создаем окно подсказки
        if r.Inside(p):
            if self.GetValue() is None:
                msg = u'На текущий момент нет информации'
            elif self.shortHelpString in ['', None, 'None']:
                msg = '%s (%s)' % (str(self.GetValue()), self.ei)
            else:
                msg = '%s (%s)\r\n%s' % (str(self.GetValue()), self.ei, self.shortHelpString)
                
            if self._helpWin is None:
                self._helpWin = icwidget.icShortHelpString(self.parent, msg,
                                                           (x + px+15, y+20), 2000)
            else:
                self._helpWin.bNextPeriod = True
        elif self._helpWin:
            self._helpWin.Show(False)
            self._helpWin.Destroy()
        else:
            self._helpWin = None
            
        r_clr = wx.Rect(sx - WIDTH_BTN - 23, SHIFT_Y_LABEL+2, WIDTH_BTN, HEIGHT_BTN)
        r_grph = wx.Rect(sx - WIDTH_BTN-4, SHIFT_Y_LABEL+2, WIDTH_GRPH_BTN, HEIGHT_GRPH_BTN)
        
        if r_grph.Inside(p) or r_clr.Inside(p):
            cursor = wx.StockCursor(wx.CURSOR_HAND)
        else:
            cursor = wx.StockCursor(wx.CURSOR_DEFAULT)

        self.SetCursor(cursor)
        evt.Skip()
    
    def OnLeftDown(self, evt):
        """
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        sx, sy = self.GetSize()
        p = evt.GetPosition()
        r = wx.Rect(sx - WIDTH_BTN-4, SHIFT_Y_LABEL+2, WIDTH_GRPH_BTN, HEIGHT_GRPH_BTN)
        
        if r.Inside(p):
            if self.evalSpace['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
                
                #   Рисуем динамику изменений наблюдаемого параметра
                self.CreateIndicatorTrend()
                
                #   Отрабатываем пользовательский функционал
                self.eval_attr('onGraph')
                
        r_clr = wx.Rect(sx - WIDTH_BTN - 23, SHIFT_Y_LABEL+2, WIDTH_BTN, HEIGHT_BTN)
        if r_clr.Inside(p):
            typ = self.GetTypePredst()
            
            if typ == TEXT_TYPE_PREDST:
                self.SetTypePredst(LINE_TYPE_PREDST)
            else:
                self.SetTypePredst(TEXT_TYPE_PREDST)
                
            self.eval_attr('onColor')
            
        evt.Skip()

    def OnLeftDblClick(self, evt):
        """
        Обработчик события wx.EVT_DCLICK, атрибут=onLeftDblClick
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('onLeftDblClick')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()

    def OnLeftUp(self, evt):
        """
        """
        pass

    def OnPaint(self, evt):
        """
        """
        if self._blockEvtPoint:
            return

        dc = wx.BufferedPaintDC(self)
        width, height = self.GetClientSize()

        if not width or not height:
            return

        typ = self.GetTypePredst()
        
        if typ == TEXT_TYPE_PREDST:
            if self.skin:
                self.skin.DrawTextMode(dc, self)
            else:
                self.DrawTextMode(dc)
        else:
            if self.skin:
                self.skin.Draw(dc, self)
            else:
                self.Draw(dc)
    
    def OnRightDown(self, evt):
        """
        Обрабатываем нажатие правой кнопки мыши.
        """
        return
        
    def OnSize(self, evt):
        self.Refresh()

    def RecountScalePar(self, min=None, max=None, majorStep=None, minorStep=None, factor=None, bChangeTitles=True):
        """
        Изменяет параметры шкалы индикатора.
        
        @type min: C{float}
        @param min: Минимальное значение шкалы индикатора.
        @type max: C{float}
        @param max: Максимальное значение шкалы индикатора.
        @type majorStep: C{float}
        @param majorStep: Шаг мажорной сетки шкалы индикатора.
        @type minorStep: C{float}
        @param minorStep: Шаг минорной сетки шкалы индикатора.
        @type factor: C{float}
        @param factor: Коэфициент умножения (отношение между реальным отображаемым
            значением и значением показываемым идикатором).
        @type bChangeTitle: C{bool}
        @param bChangeTitle: Признак изменения подписей маждорной сетки.
        """
        if self.majorValues:
            if min is None:
                min = self.majorValues[0]
            if max is None:
                max = self.majorValues[-1]
                
            if max == min:
                max += 1
                
            if majorStep is None:
                majorStep = float((max - min)/(len(self.majorValues)-1.0))
            if minorStep is None:
                minorStep = float((max - min)/(len(self.minorValues)-1.0))
                
        if factor is not None:
            self.factor = factor
        
        log.debug(u'RecountScalePar: %s, %s, %s, %s' % (min, max, majorStep, minorStep))

        self.majorValues = []
        s = 0.0
        i = 0
        
        #   Признаки целочисленных значений шагов мажорной и минорной сетки
        bMajorInt, bMinorInt = False, False

        if majorStep == 0:
            majorStep = 1

        while s <= max:
            if round(s) == s:
                self.majorValues.append(s)
            else:
                self.majorValues.append(s)
            i += 1
            s += majorStep

        self.minorValues = []
        s = 0.0
        i = 0

        if minorStep == 0:
            minorStep = majorStep
        
        while s <= max:
            if round(s) == s:
                self.minorValues.append(int(s))
            else:
                self.minorValues.append(s)
            i += 1
            s += minorStep
            
        if bChangeTitles:
            self.majorLabels = self.majorValues
            log.debug(u'LABELS - %s' % self.majorLabels)
    
    def RefreshState(self):
        """
        Индикатор обновляет свое представление - обращается к нужному классу данных
        и считывает значение индикатора.
        """
        rs = self.GetRecordset()
        if rs and rs.count() > 0:
            value, plan = self.aggregatePar(rs)
            log.debug(u'VALUE, PLAN: %s, %s' % (value, plan))
            
            if plan is not None:
                val = int(plan * 2 / self.factor)
                
                if val > 10:
                    val = int(round(val, -(len(str(val)) - 1)))
                    
                log.debug(u'MAX VAL = %s %s' % (val, int(plan * 2 / self.factor)))
                self.RecountScalePar(max=val)
                
            self.SetValue(value)
        else:
            self.SetValue(None)
            
        return True

    def SetState(self, value, plan=None,
                 min=None, majorStep=None, minorStep=None, factor=None,
                 bChangeTitles=True):
        """
        Функция устанавливает состояние индикатора относительного планового значения.
        
        @type value: C{float}
        @param value: Значвение индикатора.
        @type plan: C{float}
        @param plan: Плановое значвение индикатора (примерно соответствует середине).
        @type min: C{float}
        @param min: Минимальное значение шкалы индикатора.
        @type majorStep: C{float}
        @param majorStep: Шаг мажорной сетки шкалы индикатора.
        @type minorStep: C{float}
        @param minorStep: Шаг минорной сетки шкалы индикатора.
        @type factor: C{float}
        @param factor: Коэфициент умножения (отношение между реальным отображаемым
            значением и значением показываемым идикатором).
        @type bChangeTitle: C{bool}
        @param bChangeTitle: Признак изменения подписей маждорной сетки.
        """
        if plan is not None:
            if factor is None:
                factor = self.factor
                
            max = int(plan * 2 / factor)

            if max > 10:
                max = int(round(max, -(len(str(max)) - 1)))
            elif max == 0:
                max = 1
                
            self._planFactor = float((2*plan)/(max*factor))
            log.debug(u'SET STATE MAX VAL, planFactor = %s, %s' % (max, self._planFactor))
            self.RecountScalePar(min, max, majorStep, minorStep, factor, bChangeTitles)

        self.SetValue(value)
        return True
            
    def SetAggregationType(self, type):
        """
        """
        self.aggregationType = type
        
    def SetAggregationFunc(self, func):
        """
        """
        self.aggregationFunc = func

    def SetDayPlanFunc(self, func):
        """
        Сохраняет ссылку на функцию дневных планов.
        """
        self._dayPlanFunc = func
        
    def SetLabel(self, label):
        """
        Sets the static text label and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.
        """
        label = label.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\r\n', '\n')
        wx.PyControl.SetLabel(self, label)
        style = self.GetWindowStyleFlag()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()
        
    def SetFont(self, font):
        """
        Sets the static text font and updates the control's size to exactly
        fit the label unless the control has wx.ST_NO_AUTORESIZE flag.
        """
        wx.PyControl.SetFont(self, font)
        style = self.GetWindowStyleFlag()
        if not style & wx.ST_NO_AUTORESIZE:
            self.SetSize(self.GetBestSize())
        self.Refresh()

    def SetPeriodIzm(self, tm):
        """
        Устанавливает время измерерния.
        """
        self.periodIzm = tm

    def SetSkin(self, skin):
        """
        Устанвливает скин для индикатора.
        """
        self.skin = skin
        
    def SetTimeField(self, fld):
        """
        Устанавливает имя поля для хранения временного параметра.
        """
        self.attrTime = fld

    def SetTypePredst(self, typ=LINE_TYPE_PREDST):
        """
        Возвращает тип представления.
        """
        if typ != LINE_TYPE_PREDST:
            self.SetSize((self.size[0], 23))
        else:
            self.SetSize(self.size)
            
        self.Refresh()
        self._typePredst = typ

    def SetStatisticBuff(self, data):
        """
        Устанавливает указатель на буфер статистических данных. Используется
        для отображение динамики на графике.
        """
        self._statistic = data

    def SetStatisticFuncPar(self, f, *arg, **kwarg):
        """
        Устанавливаем функцию по сбору статистики.
        """
        self._statisticFuncPar = (f, arg, kwarg)
        
    def SetValue(self, val):
        """
        Устанавливает значение индикатора.
        """
        self._value = val
        self.Refresh()
    
    def UpdateViewFromDB(self, db_name=None, bFromBuff=True):
        """
        Обновляет представление индикатора (если компонент привязан к объекту
        icGridDataset).
        
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        @type bFromBuff: C{bool}
        @param bFromBuff: Признак, который указывает, что значения можно брать из
            буфера измененных значений.
        @rtype: C{bool}
        @return: Возвращает признак успешного обновления.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name
            
        if (self.dataset is not None and self.IsShown() and self.bStatusVisible and
           self.dataset.name == db_name):
            
            val = self.dataset.getNameValue(self.attrVal, bFromBuff=bFromBuff)
            self.SetValue(val)
            return True


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
    skin = icClassicSkin()
    
    ctrl_1 = icArrowIndicator(win, -1, {'position': (20, 20),
                                        'size': (255, 70),
                                        'label': u'Реализация',
                                        'dateIzm': '20/05/05',
                                        'value': '15',
                                        'ei': u'кг.',
                                        'onGraph': 'print(\'OnGraph\')',
                                        'onSaveProperty': 'print(\'onSaveProperty\')',
                                        'onLeftDblClick': 'print(\'onLeftDblClick\')',
                                        'shortHelpString': u' Индикатор \r\n Проверка',
                                        'colorRegions': '((20, \'BLUE\'), (32, \'GREEN\'), (50, (230, 160, 0)))',
                                        'majorValues': '(0, 10, 20, 30, 40, 50)',
                                        'majorLabels': '(\'A\', 10, 20, 30, 40, \'C\')',
                                        'minorValues': '(0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50)',
                                        'backgroundColor': (250, 250, 250),
                                        'foregroundColor': (0, 0, 200)})

    ctrl_2 = icArrowIndicator(win, -1, {'position': (20, 90),
                                        'size': (255, 70),
                                        'label': u'Реализация (x 1000)',
                                        'dateIzm': '20/05/05',
                                        'value': '35000',
                                        'factor': 1000,
                                        'ei': u'кг.',
                                        'source': 'table1',
                                        'attrVal': 'value',
                                        'attrPlan': 'plan',
                                        'onGraph': 'print(\'OnGraph\')',
                                        'onSaveProperty': 'print(\'onSaveProperty\')',
                                        'shortHelpString': u' Индикатор \r\n Проверка',
                                        'colorRegions': '((20, \'BLUE\'), (32, \'GREEN\'), (50, (255, 0, 0)))',
                                        'majorValues': '(0, 10, 20, 30, 40, 50)',
                                        'majorLabels': '(\'A\', 10, 20, 30, 40, \'C\')',
                                        'minorValues': '(0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50)',
                                        'backgroundColor': (250, 250, 250),
                                        'foregroundColor': (0, 0, 200)})
                    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
