#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Стилизованный notebook.
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

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import random
import wx.lib.agw.flatnotebook as fnb

_ = wx.GetTranslation
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icFlatNotebook'

#   Описание стилей компонента
ic_class_styles = {'FNB_ALLOW_FOREIGN_DND': fnb.FNB_ALLOW_FOREIGN_DND,
                   'FNB_HEIGHT_SPACER': fnb.FNB_HEIGHT_SPACER,
                   # Use Visual Studio 2003 (VC7.1) style for tabs
                   'FNB_VC71': fnb.FNB_VC71,
                   # Use fancy style - square tabs filled with gradient coloring
                   'FNB_FANCY_TABS': fnb.FNB_FANCY_TABS,
                   # Draw thin border around the page
                   'FNB_TABS_BORDER_SIMPLE': fnb.FNB_TABS_BORDER_SIMPLE,
                   # Do not display the 'X' button
                   'FNB_NO_X_BUTTON': fnb.FNB_NO_X_BUTTON,
                   # Do not display the Right / Left arrows
                   'FNB_NO_NAV_BUTTONS': fnb.FNB_NO_NAV_BUTTONS,
                   # Use the mouse middle button for cloing tabs
                   'FNB_MOUSE_MIDDLE_CLOSES_TABS': fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS,
                   # Place tabs at bottom - the default is to place them
                   # at top
                   'FNB_BOTTOM': fnb.FNB_BOTTOM,
                   # Disable dragging of tabs
                   'FNB_NODRAG': fnb.FNB_NODRAG,
                   # Use Visual Studio 2005 (VC8) style for tabs
                   'FNB_VC8': fnb.FNB_VC8,
                   # Place 'X' on a tab
                   'FNB_X_ON_TAB': fnb.FNB_X_ON_TAB,
                   'FNB_BACKGROUND_GRADIENT': fnb.FNB_BACKGROUND_GRADIENT,
                   # Style to close tab using double click - styles 1024, 2048 are reserved
                   'FNB_DCLICK_CLOSES_TABS': fnb.FNB_DCLICK_CLOSES_TABS,
                   # Use Smart Tabbing, like Alt+Tab on Windows
                   'FNB_SMART_TABS': fnb.FNB_SMART_TABS,
                   # Use a dropdown menu on the left in place of the arrows
                   'FNB_DROPDOWN_TABS_LIST': fnb.FNB_DROPDOWN_TABS_LIST,
                   # Hides the Page Container when there is one or fewer tabs
                   'FNB_HIDE_ON_SINGLE_TAB': fnb.FNB_HIDE_ON_SINGLE_TAB,
                   'FNB_ALLOW_FOREIGN_DND': fnb.FNB_ALLOW_FOREIGN_DND,
                   }

if wx.VERSION < (2, 8, 11, 0, ''):
    ic_class_styles['FNB_COLORFUL_TABS'] = fnb.FNB_COLORFUL_TABS
else:
    ic_class_styles['FNB_COLORFUL_TABS'] = fnb.FNB_COLOURFUL_TABS
    
#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'FlatNotebook',
                'name': 'default',
                'child': [],

                'titles': [],
                'images': [],
                'tab_area_color': None,
                'grad_color_border': None,
                'active_tab_color': None,
                'non_active_tabtxt_color': None,
                'active_tabtxt_color': None,

                'colorFrom': (200, 200, 200),
                'colorTo': (200, 200, 200),
                'style': fnb.FNB_NODRAG,
                'onPageChanged': None,
                'onPageChanging': None,
                'onPageClosing': None,
                'page_selection': -1,

                '__styles__': ic_class_styles,
                '__events__': {'onPageChanged': ('fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED', 'OnPageChanged', False),
                               'onPageChanging': ('fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING', 'OnPageChanging', False),
                               'onPageClosing': ('fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING', 'OnPageClosing', False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   icDefInf.EDT_TEXTLIST: ['titles'],
                                   icDefInf.EDT_COLOR: ['colorFrom', 'colorTo',
                                                        'active_tab_color',
                                                        'tab_area_color',
                                                        'active_tabtxt_color',
                                                        'non_active_tabtxt_color',
                                                        'grad_color_border'],
                                   icDefInf.EDT_NUMBER: ['page_selection'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtNotebook'
ic_class_pic2 = '@common.imgEdtNotebook'

#   Путь до файла документации
ic_class_doc = 'doc/public/icflatnotebook.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Window', 'Panel', 'ScrolledWindow', 'SplitterWindow', 'Notebook', 'DataLink']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icFlatNotebook(icwidget.icWidget, fnb.FlatNotebook):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{child=[]}:
        - B{type='FlatNotebook'}:
        - B{name='default'}:
        - B{titles=[]}:
        - B{images=[]}:
        - B{colorFrom=(200,200,200)}: Цвет1 градиентной заливки активной страницы.
        - B{colorTo=(200,200,200)}: Цвет2 градиентной заливки активной страницы.
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

        #
        self._newPageCounter = 0
        self._bShowImages = []
        
        #   Определяем список картинок
        self.images = self.countAttr('images')
        if self.images is None:
            self.images = []
            
        self._ImageList = wx.ImageList(16, 16)
        for img in self.images:
            self._ImageList.Add(img)
        
        if wx.VERSION < (2, 8, 11, 0, ''):
            fnb.FlatNotebook.__init__(self, parent, wx.ID_ANY, style=self.style)
        else:
            fnb.FlatNotebook.__init__(self, parent, wx.ID_ANY, agwStyle=self.style)
            
        if self.images:
            self.SetImageList(self._ImageList)
        
        if self.colorFrom:
            wx.CallAfter(self.SetGradientColourFrom, wx.Colour(*self.colorFrom))
        if self.colorTo:
            wx.CallAfter(self.SetGradientColourTo, wx.Colour(*self.colorTo))
        if self.active_tab_color:
            self.SetActiveTabColour(wx.Colour(*self.active_tab_color))
        if self.tab_area_color:
            self.SetTabAreaColour(wx.Colour(*self.tab_area_color))
        if self.grad_color_border:
            self.SetGradientColourBorder(wx.Colour(*self.grad_color_border))
        if self.active_tabtxt_color:
            self.SetActiveTabTextColour(wx.Colour(*self.active_tabtxt_color))
        if self.non_active_tabtxt_color:
            self.SetNonActiveTabTextColour(wx.Colour(*self.non_active_tabtxt_color))
        #   Регистрация обработчиков событий
        self.BindICEvt()

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
        #   Добавляем компоненты в книгу
        self.addChildsToNotebook()
        
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        
        self.__init_clr = False
        wx.CallAfter(self.OnPageChanged, None)

        if self.page_selection >= 0:
            self.SetSelection(int(self.page_selection))
  
    def init_clr(self):
        if not self.__init_clr:
            self.__init_clr = True
            if self.colorFrom:
                self.SetGradientColourFrom(wx.Colour(*self.colorFrom))
            if self.colorTo:
                self.SetGradientColourTo(wx.Colour(*self.colorTo))
            self.Refresh()
        
    def OnPageChanged(self, evt):
        self.init_clr()
        self.eval_event('onPageChanged', evt, True)
        
    def OnPageChanging(self, evt):
        self.eval_event('onPageChanging', evt, True)
        
    def OnPageClosing(self, evt):
        self.eval_event('onPageClosing', evt, True)
        
    def addChildsToNotebook(self):
        """
        Добавляем дочерние элементы в книгу.
        """
        for i, el in enumerate(self.component_lst):
            if i >= len(self.titles):
                title = _('Page ') + str(i)
            else:
                title = self.titles[i]
                
            if self.images and i < len(self.images):
                self.AddPage(el, title, True, i)
            else:
                self.AddPage(el, title, True, -1)
        
    def addPage2(self, win=None, caption=None, sel=0, image=-1):
        """
        Добавление страницы.
        """
        if not caption:
            caption = _('New Page Added #') + str(self._newPageCounter)
        
        self.Freeze()
        
        if image is None or (not isinstance(image, int) and wx.NullBitmap == image):
            image = -1
            
        if self.images:
            image = random.randint(0, self._ImageList.GetImageCount()-1)
        
        if not win:
            win = self.CreatePage(caption)
            
        self.AddPage(win, caption, True, image)
        self.Thaw()
        self._newPageCounter = self._newPageCounter + 1

    def addPage(self, win=None, caption=None, sel=0, image=-1):
        """
        Добавление страницы.
        """
        if not isinstance(image, int):
            image = 0
        
        self.AddPage(win, caption, True, image)
        self._newPageCounter = self._newPageCounter + 1
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)

    def CreatePage(self, caption):
        """
        Создает пустую страницу.
        """
        p = wx.Panel(self)
        wx.StaticText(p, -1, caption, (20, 20))
        return p

    def deleteAllPages(self, bDestroy=True):
        """
        Deletes all the pages.
        """
        for page in range(self.GetPageCount()):
            self.DeletePage(page)
        self.DeleteAllPages()
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
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    win.SetSizer(mainSizer)
    
    scr = '''
import ic.imglib.collection1C as lib
return [ic.imglib.collection1C.schema, ic.imglib.collection1C.addRec]
'''
    book = icFlatNotebook(win, -1, {'images': scr, 'style': fnb.FNB_VC8, 'colorFrom': (250, 100, 100)})
    book.Freeze()
    for x in range(5):
        book.addPage2()

    mainSizer.Add(book, 6, wx.EXPAND)
    mainSizer.Layout()
    win.SendSizeEvent()
    
    book.Thaw()
    book.Refresh()
    print(u'>>> style: %s ' % book.GetWindowStyleFlag())
    frame.Show(True)
    
    app.MainLoop()
    
if __name__ == '__main__':
    test()

