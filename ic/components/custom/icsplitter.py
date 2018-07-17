#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wxSplitterWindow. Генерирут объект по ресурсному описанию. Данный
объект состоит из двух областей размеры которых можно менять перетаскиванием разделителя.
ВНИМАНИЕ! Добавление дочерних компонентов в этот компонент
происходит не как у остальных компонентов.
В Компонент можно добавить только 2 панели например.
При этом спецификация первой панели добавляется в атрибут 'win1',
а второй панели в атрибут 'win2'.

@type SPC_IC_SPLITTER: C{dictionary}
@var SPC_IC_SPLITTER: Спецификация на ресурсное описание компонента. Описание ключей SPC_IC_SPLITTER:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'SplitterWindow'}: Тип объекта.
    - B{position = (-1,-1)}: Расположение компонента на родительском окне.
    - B{size = (-1,-1)}: Размер картинки.
    - B{style=wx.SP_3D}: Стили:
        - C{wx.SP_3D} - 3D вид бордюр и разделителя;
        - C{wx.SP_3DSASH} - 3D вид разделителя.
        - C{wx.SP_3DBORDER} - 3D вид бордюр.
        - C{wx.SP_FULLSASH} - разделитель прорисовывается полностью так, что можно испольозовать окна без бордюр.
        - C{wx.SP_BORDER} - тонкая черная бордюра вокруг окна.
        - C{wx.SP_NOBORDER} - нет бордюр и черный разделитель.
        - C{wx.SP_PERMIT_UNSPLIT} - позволяет свернуть одно из окон даже если установлен минимальный размер панели больший нуля.
        - C{wx.SP_LIVE_UPDATE} - линия нового положения не рисуется, а размеры окон сразу изменяются.
 
    - B{win1=None}: Описание первой панели.
    - B{win2=None}: Описание второй панели.
    - B{layout='horizontal'}: Способ разделения ('vertical' | 'horizontal').
    - B{sash_pos=100}: Расположение разделителя.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на окне.
    - B{min_panelsize=20}: Минимальный размер свернутой панели.
    
@type ICSplitterStyle: C{dictionary}
@var ICSplitterStyle: Словарь специальных стилей компонента. Описание ключей ICSplitterStyle:

    - C{wx.SP_3D} - 3D вид бордюр и разделителя;
    - C{wx.SP_3DSASH} - 3D вид разделителя.
    - C{wx.SP_3DBORDER} - 3D вид бордюр.
    - C{wx.SP_BORDER} - тонкая черная бордюра вокруг окна.
    - C{wx.SP_NOBORDER} - нет бордюр и черный разделитель.
    - C{wx.SP_PERMIT_UNSPLIT} - позволяет свернуть одно из окон даже если установлен минимальный размер панели больший нуля.
    - C{wx.SP_LIVE_UPDATE} - линия нового положения не рисуется, а размеры окон сразу изменяются.
 
"""

import wx
import ic.utils.util as util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
import ic.utils.resource as resource
import ic.PropertyEditor.icDefInf as icDefInf
from ic.kernel import io_prnt
import ic.imglib.common as common

_ = wx.GetTranslation

ICSplitterStyle = {'SP_3D': wx.SP_3D,
                   'SP_3DSASH': wx.SP_3DSASH,
                   'SP_3DBORDER': wx.SP_3DBORDER,
                   'SP_BORDER': wx.SP_BORDER,
                   'SP_NOBORDER': wx.SP_NOBORDER,
                   'SP_PERMIT_UNSPLIT': wx.SP_PERMIT_UNSPLIT,
                   'SP_LIVE_UPDATE': wx.SP_LIVE_UPDATE}

SPC_IC_SPLITTER = {'name': 'defaultName',
                   'type': 'SplitterWindow',
                    
                   'position': (-1, -1),
                   'size': (-1, -1),
                   'sash_pos': 100,
                   'sash_size': -1,
                   'min_panelsize': 20,
                   'layout': 'horizontal',
                    
                   'win1': None,    # Имя первого окна в сплиттере
                   'win2': None,    # Имя второго окно в сплиттере
                    
                   'style': wx.SP_3D,
                   'keyDown': None,
                    
                   '__attr_types__': {icDefInf.EDT_NUMBER: ['sash_pos',
                                                            'sash_size', 'min_panelsize'],
                                      icDefInf.EDT_CHOICE: ['layout'],
                                      },
                   '__lists__': {'layout': ['vertical', 'horizontal'],
                                 },
                   '__parent__': SPC_IC_WIDGET,
                   '__attr_hlp__': {'win1': u'Имя первого окна в сплиттере',
                                    'win2': u'Имя второго окно в сплиттере',
                                    },
                   }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icSplitter'

#   Описание стилей компонента
ic_class_styles = ICSplitterStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_SPLITTER
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtSplitter'
ic_class_pic2 = '@common.imgEdtSplitter'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icsplitter.icSplitter-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Window', 'Panel', 'FlatNotebook',
                  'ScrolledWindow', 'SplitterWindow',
                  'Notebook', 'DataLink', 'Import', 'ObjectLink']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = -1

#   Версия компонента
__version__ = (1, 0, 0, 6)


class icSplitter(icWidget, wx.SplitterWindow):
    """
    Класс реализует интерфейс к классу wx.SplitterWindow
    через ресурсное описание.
    """
    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        import ic.components.icResourceParser as prs
        testObj = prs.CreateForm('Test', formRes=res,
                                 evalSpace=context, parent=parent, bIndicator=True)
        #   Для оконных компонентов надо вызвать метод Show
        try:
            testObj.context['_root_obj'].Show(True)
            testObj.context['_root_obj'].SetFocus()
        except: 
            io_prnt.outErr()
    
    def __init__(self, parent, id=-1, component={}, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания объекта icSplitterWindow.
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
        util.icSpcDefStruct(SPC_IC_SPLITTER, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace, bPrepareProp=True)

        size = component['size']
        pos = component['position']
        self.sash_size = component['sash_size']
        #   Флаг, указывающий, что необходимо сохранять изменяющиеся
        #   параметры окна (позицию и размеры).
        self.saveChangeProperty = True

        #   Читаем расположение сплиттера из файла настроек пользователя
        _pos = self.LoadUserProperty('sash_pos')

        if _pos:
            self.sash_pos = _pos
        # Последняя позиция разделителя
        self._last_sash_pos = _pos

        wx.SplitterWindow.__init__(self, parent, id, pos, size, component['style'], name=self.name )
        self.SetMinimumPaneSize(component['min_panelsize'])
        self.SetSashSize(self.sash_size)

        self.BindICEvt()

        #   Создаем дочерние компоненты
        self.child = []
        if component['win1']:
            self.child.append(component['win1'])
        if component['win2']:
            self.child.append(component['win2'])
        
        self.childCreator(bCounter, progressDlg)
        
        # Вспомогательные атрибуты
        self._toggle_win1 = False
        self._toggle_win2 = False

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self
                
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
                                
        if not self.resource['win1']:
            win1 = wx.Window(self, -1)
        else:
            win1 = self.components[self.resource['win1']['name']]

        if not self.resource['win2']:
            win2 = wx.Window(self, -1)
        else:
            win2 = self.components[self.resource['win2']['name']]

        if self.layout == 'vertical':
            self.SplitVertically(win1, win2, self.sash_pos)
        else:
            self.SplitHorizontally(win1, win2, self.sash_pos)

    def ObjDestroy(self):
        self.SaveUserProperty('sash_pos', self.GetSashPosition())
        
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
        
    def hideWindow1(self):
        """
        Скрыть первую панель.
        """
        self._last_sash_pos = self.GetSashPosition()
        min_panel_size = self.GetMinimumPaneSize()
        self.SetSashPosition(min_panel_size)
        
    def showWindow1(self):
        """
        Показать первую панель.
        """
        restore_pos = self._last_sash_pos
        self._last_sash_pos = self.GetSashPosition()
        self.SetSashPosition(restore_pos)
        
    def hideWindow2(self):
        """
        Скрыть вторую панель.
        """
        self._last_sash_pos = self.GetSashPosition()
        new_pos = self.GetMinimumPaneSize()
        self.SetSashPosition(new_pos)
        
    def showWindow2(self):
        """
        Показать вторую панель.
        """
        restore_pos = self._last_sash_pos
        self._last_sash_pos = self.GetSashPosition()
        self.SetSashPosition(restore_pos)

    def toggleWindow1(self):
        """
        Переключить просмотр первой панели.
        """
        if self._toggle_win1:
            self.showWindow1()
            self._toggle_win1 = False
        else:
            self.hideWindow1()
            self._toggle_win1 = True
        
    def toggleWindow2(self):
        """
        Переключить просмотр второй панели.
        """
        if self._toggle_win2:
            self.showWindow2()
            self._toggle_win2 = False
        else:
            self.hideWindow2()
            self._toggle_win2 = True


def test(par=0):
    """
    Тестируем класс icSplitter.
    """
    from ic.components.ictestapp import TestApp
    import ic.components.icwxpanel as panel
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icSplitterWindow Test')
    win = icSplitter(frame, -1, {'layout': 'horizontal',
                                 'keyDown': 'print \'KeyDown in Splitter\''})

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
