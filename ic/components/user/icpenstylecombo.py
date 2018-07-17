#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Комбобокс стиля линии.
Класс пользовательского визуального компонента. КОМБОБОКС СТИЛЯ ЛИНИИ.

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
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icPenStyleComboBox'

#   Описание стилей компонента
ICComboBoxStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                   'CB_DROPDOWN': wx.CB_DROPDOWN,
                   'CB_READONLY': wx.CB_READONLY,
                   'CB_SORT': wx.CB_SORT}

ic_class_styles = ICComboBoxStyle

ICPenStylesDefault = [{u'Solid': wx.SOLID},
                      {u'Transparent': wx.TRANSPARENT},
                      {u'Dot': wx.DOT},
                      {u'Long Dash': wx.LONG_DASH},
                      {u'Short Dash': wx.SHORT_DASH},
                      {u'Dot Dash': wx.DOT_DASH},
                      {u'Backward Diagonal Hatch': wx.BDIAGONAL_HATCH},
                      {u'Cross-diagonal Hatch': wx.CROSSDIAG_HATCH},
                      {u'Forward Diagonal Hatch': wx.FDIAGONAL_HATCH},
                      {u'Cross Hatch': wx.CROSS_HATCH},
                      {u'Horizontal Hatch': wx.HORIZONTAL_HATCH},
                      {u'Vertical Hatch': wx.VERTICAL_HATCH},
                      ]

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'PenStyleComboBox',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'description': '',

                'font': {},
                'position': (-1, -1),
                'size': (-1,-1),
                'items': ICPenStylesDefault,
                'foregroundColor': (0, 0, 0),
                'backgroundColor': (255, 255, 255),

                '__styles__': ic_class_styles,
                '__events__': {},
                '__brief_attrs__': ['name', 'description'],
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtChoice'
ic_class_pic2 = '@common.imgEdtChoice'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.icpenstylecombo.icPenStyleComboBox-class.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icPenStyleComboBox(icwidget.icWidget, wx.combo.OwnerDrawnComboBox):
    """
    КОМБОБОКС СТИЛЯ ЛИНИИ.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='DatePickerCtrl'}:
        - B{name='default'}:
        - B{value=''}:
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
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        items = [item.keys()[0] for item in self.items]

        wx.combo.OwnerDrawnComboBox.__init__(self, parent, 
                                             choices=items,
                                             pos=self.position,
                                             size=self.size,
                                             style=self.style)

        # --- Регистрация обработчиков событий
        self.BindICEvt()

    def OnDrawItem(self, dc, rect, item, flags):
        """
        Overridden from OwnerDrawnComboBox, called to draw each
        item in the list.
        """
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected yet
            return

        r = wx.Rect(*rect)  # make a copy
        r.Deflate(3, 5)

        # Определить стиль штриховки
        penStyle = self.items[item].values()[0]
            
        fgCol = wx.Colour(*tuple(self.foregroundColor))
        pen = wx.Pen(fgCol, 3, penStyle)
        dc.SetPen(pen)

        if flags & wx.combo.ODCB_PAINTING_CONTROL:
           # for painting the control itself
           dc.DrawLine(r.x+5, r.y+r.height/2, r.x+r.width - 5, r.y+r.height/2)

        else:
            # for painting the items in the popup
            dc.DrawText(self.GetString(item),
                        r.x + 3,
                        (r.y + 0) + ((r.height/2) - dc.GetCharHeight())/2
                        )
            dc.DrawLine(r.x+5, r.y+((r.height/4)*3)+1, r.x+r.width - 5, r.y+((r.height/4)*3)+1)
           
    def OnDrawBackground(self, dc, rect, item, flags):
        """
        Overridden from OwnerDrawnComboBox, called for drawing the
        background area of each item.
        """
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering.
        if (item & 1 == 0 or flags & (wx.combo.ODCB_PAINTING_CONTROL |
                                      wx.combo.ODCB_PAINTING_SELECTED)):
            wx.combo.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

        # Otherwise, draw every other background with different colour.
        bgCol = wx.Colour(*tuple(self.backgroundColor))
        dc.SetBrush(wx.Brush(bgCol))
        dc.SetPen(wx.Pen(bgCol))
        dc.DrawRectangleRect(rect)

    def OnMeasureItem(self, item):
        """
        Overridden from OwnerDrawnComboBox, should return the height
        needed to display an item in the popup, or -1 for default.
        """
        # Simply demonstrate the ability to have variable-height items
        if item & 1:
            return 36
        else:
            return 24

    def OnMeasureItemWidth(self, item):
        """
        Overridden from OwnerDrawnComboBox.  Callback for item width, or
        -1 for default/undetermined.
        """
        return -1

    def getSelectedStyle(self):
        """
        Функция возвращает выбранный стиль, например wx.SOLID.
        """
        selected = self.GetSelection()
        if selected >= 0:
            item_values = [item.values()[0] for item in self.items]
            return item_values[selected]
        return -1

    def setSelectedStyle(self, PenStyle_):
        """
        Выбрать в комбобоксе стиль.
        @param PenStyle_: Стиль линии, например wx.SOLID. 
        """
        item_values = [item.values()[0] for item in self.items]
        find_idx = -1
        try:
            find_idx = item_values.index(PenStyle_)
        except:
            pass
        self.SetSelection(find_idx)


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
    
    ctrl = icPenStyleComboBox(win, -1, {'position': (10, 10),
                                        'size': (100, -1),
                                        'style': wx.CB_READONLY})
                                
    frame.Show(True)
    app.MainLoop()
    

if __name__ == '__main__':
    test()
