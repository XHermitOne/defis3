#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит класс icNotebook, который по ресурсному описанию создает окно с закладками.

@type SPC_IC_PAGES_BOOK: C{dictionary}
@var SPC_IC_PAGES_BOOK: Спецификация на ресурсное описание компонента. Описание ключей:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'SplitterWindow'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{size = (-1,-1)}: Размер компонента.
    - B{style=0}: Стили:
        - C{NB_LEFT}  - закладки располагаются на левой стороне.
        - C{NB_RIGHT}  - закладки располагаются на правой стороне.
        - C{NB_BOTTOM}  - закладки располагаются внизу.
        - C{NB_FIXEDWIDTH} - (Windows only) закладки имеют фиксированную длину.
        - C{NB_MULTILINE} - (Windows only) закладки могут располагаться в несколько строк.
        
    - B{child=[]}: Описание окон книги.
    - B{titles=[]}: Описание надписаей на закладках.
    - B{images=[]}: Описание картинок прикрепленных к закладкам.
    - B{pageChanged=None}: Выражение, выполняемое после изменения текущей страницы органайзера
        (реакция на сообщение B{wx.EVT_COMMAND_NOTEBOOK_PAGE_CHANGED}).
    - B{imag_size=(16,16)}: Размер картинок.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на окне.
    - B{select=None}: Выражение вычисляющее номер активной страницы.
    
@type ICPagesBookStyle: C{dictionary}
@var ICPagesBookStyle: Словарь специальных стилей компонента. Описание ключей ICPagesBookStyle:

    - C{NB_LEFT}  - закладки располагаются на левой стороне.
    - C{NB_RIGHT}  - закладки располагаются на правой стороне.
    - C{NB_BOTTOM}  - закладки располагаются внизу.
    - C{NB_FIXEDWIDTH} - (Windows only) закладки имеют фиксированную длину.
    - C{NB_MULTILINE} - (Windows only) закладки могут располагаться в несколько строк.
"""
import wx
import ic.utils.util as util
import ic.components.icwidget as icwidget
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

ICPagesBookStyle = {'DEFAULT': 0,
                    'NB_LEFT': wx.NB_LEFT,
                    'NB_RIGHT': wx.NB_RIGHT,
                    'NB_BOTTOM': wx.NB_BOTTOM,
                    'NB_FIXEDWIDTH': wx.NB_FIXEDWIDTH,
                    'NB_MULTILINE': wx.NB_MULTILINE}

SPC_IC_PAGES_BOOK = {'type': 'Notebook',
                     'name': 'Notebook',

                     'style': 0,
                     'position': (-1, -1),
                     'size': (-1, -1),
                     'child': [],
                     'titles': [],
                     'images': [],
                     'image_size': (16, 16),
                     'pageChanged': None,
                     'select': None,
                     'keyDown': None,
                     'onRightMouseClick': None,
                     'onLeftMouseClick': None,

                     '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                        icDefInf.EDT_TEXTLIST: ['titles'],
                                        },
                     '__events__': {'pageChanged': ('wx.EVT_NOTEBOOK_PAGE_CHANGED', 'OnPageChanged', False),
                                    'onLeftMouseClick': ('wx.EVT_LEFT_DOWN', 'OnLeftDown', False),
                                    'onRightMouseClick': ('wx.EVT_RIGHT_DOWN', 'OnRightDown', False),
                                    },
                     '__parent__': icwidget.SPC_IC_WIDGET,
                     }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icNotebook'

#   Описание стилей компонента
ic_class_styles = ICPagesBookStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_PAGES_BOOK
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtNotebook'
ic_class_pic2 = '@common.imgEdtNotebook'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icnotebook.icNotebook-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Window', 'Panel', 'ScrolledPanel',
                  'ScrolledWindow', 'SplitterWindow', 'Notebook', 'DataLink']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = -1

#   Версия компонента
__version__ = (1, 0, 0, 7)


class icNotebook(icwidget.icWidget, wx.Notebook):
    """
    Интерфейс к классу wxNotebook
    через ресурсное описание.
    """
    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None,
                bCounter=False, progressDlg=None):
        """
        Конструктор для создания объекта icNotebook.

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
        util.icSpcDefStruct(SPC_IC_PAGES_BOOK, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.style = component['style']
        
        self.titles = component['titles']
        if self.titles is None:
            self.titles = []
        
        self.images = self.countAttr('images')
        if self.images is None:
            self.images = []

        sel = component['select']
        sx, sy = component['image_size']
        self.pageChanged = component['pageChanged']
        self.keydown = component['keyDown']

        wx.Notebook.__init__(self, parent, id, self.position, self.size, self.style, name=self.name )
        
        #   Создаем контейнер для картинок на закладках
        self.imgList = wx.ImageList(sx, sy)
        for img in self.images:
            self.imgList.Add(img)
        
        if self.images:
            self.SetImageList(self.imgList)

        #   Устанавливаем нужную страницу в качестве активной
        ret, res = self.eval_attr('select')
        page = 0
        
        if ret:
            try:
                page = int(res)
            except:
                page = 0
            
        self.firstSel = page

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, id=id)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.BindICEvt()

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)

        # После создания страниц надо выбрать страницу
        self.SetSelection(self.firstSel)
        
    def addChildsToNotebook(self):
        """
        Добавляем дочерние элементы в книгу.
        """
        for i, child in enumerate(self.resource['child']):
            el = self.components[child['name']]

            if i >= len(self.titles):
                title = u'Страница ' + str(i)
            else:
                title = self.titles[i]
                
            if self.images and i < len(self.images):
                self.AddPage(el, title, True, i)
            else:
                self.AddPage(el, title, True, -1)
            
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
            
            #   Добавляем компоненты в книгу
            self.addChildsToNotebook()

    def DestroyWin(self):
        """
        Обрабатывает закрытие окна.
        """
        #   Посылаем всем уведомление о разрущении родительского окна.
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except:
                    pass
        except:
            pass
    
    def OnLeftDown(self, evt):
        """
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        
        self.eval_attr('onLeftMouseClick')
        evt.Skip()

    def OnRightDown(self, evt):
        """
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        
        self.eval_attr('onRightMouseClick')
        evt.Skip()

    def OnPageChanged(self, evt):
        """
        Обрабатываем изменение текущей страницы органайзера.
        """
        old_id_page = self.GetSelection()
        new_id_page = evt.GetSelection()

        #   Устанавливаем нужную страницу в качестве активной
        evt.Skip()
        self.activePage = new_id_page
        lst = self.SetStatusVisible(True)
        self.UpdateRelObj(lst)
        
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        
        self.eval_attr('pageChanged')

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
            id_page = self.activePage
            win = self.GetPage(id_page)
            
            #   Устанавливаем у дочерних объектов такой же признак видимости
            for child in self.components:
                
                if bVisible:
                    try:
                        if self.components[child] == win:
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
    Тестируем класс icNotebook.
    """
    from ic.components.ictestapp import TestApp
    import ic.components.icwxpanel as panel
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'Notebook Test')
    win = icNotebook(frame, -1, {'keyDown': 'print \'keyDown in Notebook\''})
    win1 = panel.icWXPanel(win, -1)
    win2 = panel.icWXPanel(win, -1)
    win.AddPage(win1, 'Page 1')
    win.AddPage(win2, 'Page 2')
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
