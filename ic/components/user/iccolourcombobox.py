#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Комбобокс выбора цвета.
Класс пользовательского визуального компонента. КОМБОБОКС ВЫБОРА ЦВЕТА.

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
import wx.combo
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.dlg import ic_dlg

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icColourComboBox'

#   Описание стилей компонента
ICComboBoxStyle = {'CB_SIMPLE': wx.CB_SIMPLE,
                   'CB_DROPDOWN': wx.CB_DROPDOWN,
                   'CB_READONLY': wx.CB_READONLY,
                   'CB_SORT': wx.CB_SORT}

ic_class_styles = ICComboBoxStyle

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'ColourComboBox',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'description': '',

                'font': {},
                'position': (-1, -1),
                'size': (-1, -1),
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
ic_class_doc = None
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icColourComboBox(icwidget.icWidget,wx.combo.ComboCtrl):
    """
    КОМБОБОКС ВЫБОРА ЦВЕТА.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='ColourComboBox'}:
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
        wx.combo.ComboCtrl.__init__(self, parent, 
                                    pos=self.position,
                                    size=self.size,
                                    style=self.style)

        self._draw_choice_button()
        
        # --- Регистрация обработчиков событий
        self.BindICEvt()

    def _draw_choice_button(self):
        """
        Отрисовать кнопку '...'
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw,bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 254, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = '...'
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw,th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)       
        
    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        colour = wx.BLACK
        if self.GetValue():
            colour = wx.Colour(*eval(self.GetValue()))
        
        colour = ic_dlg.icColorDlg(self, u'Выбор цвета', colour)

        self.SetValue(str(colour))
        self.SetBackgroundColour(colour)
        self.SetFocus()

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass
        
    def getSelectedColour(self):
        """
        Функция возвращает выбранный цвет.
        """
        colour = self.GetValue()
        if colour:
            colour = wx.Colour(*eval(colour))
            return colour        
        return None

    def setSelectedColour(self, Colour_):
        """
        Выбрать в комбобоксе цвет.
        @param Colour_: Цвет. Может задаваться как кортежем (R,G,B) или
            объектом wx.Colour.
        """
        if Colour_ is None:
            self.SetValue('')
            self.SetBackgroundColour(wx.SYS_COLOUR_BACKGROUND)
        else:
            colour = str(Colour_)
            self.SetValue(colour)
            self.SetBackgroundColour(Colour_)


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
    
    ctrl = icColourComboBox(win, -1, {'position': (10, 10),
                                      'size': (300, -1),
                                      'style': wx.CB_READONLY})
                                
    frame.Show(True)
    app.MainLoop()
    
    
if __name__ == '__main__':
    test()
