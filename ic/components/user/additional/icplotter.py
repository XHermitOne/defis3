#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Построение временных графиков.
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

import ic.PropertyEditor.icMatplotlibPanel as parentModule
import matplotlib.numerix as numerix
#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icPloter'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT':0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {},
                'type': 'Trend',
                'onDrawCursor':None,
                'onMouseLeftDown':None,
                'name': 'default',
                'wxAgg':0,
                '__parent__':icwidget.SPC_IC_WIDGET,
                '__events__':{'onDrawCursor':('DRAW_CURSOR','draw_cursor',False),
                              'onMouseLeftDown':('MOUSE_LEFT_DOWN','onMouseLeftDown',False)},
                '__attr_types__': {0: ['name', 'type'],
                                    icDefInf.EDT_CHECK_BOX:['wxAgg']}}
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTrend'
ic_class_pic2 = '@common.imgEdtTrend'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0,0,0,2)

class icPloter(icwidget.icWidget, parentModule.icPlotPanel):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
        - B{wxAgg=0}: Признак использования FigureCanvasWxAgg, что дает более
            высокое качество графика. В этом режиме проблемы с русскими шрифтами.
        - B{onDrawCursor=None}: Выражение, выполняемое при перерисовки курсора.
            Если выражение не определено, курсор не рисуется.
        - B{onMouseLeftDown=None}: Выражение, выполняемое при нажатии левой
            кнопки мыши на графике.
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') <> 0]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.icPlotPanel.__init__(self, parent, id, self.position, self.size,
                                        self.style, bWxAgg=self.wxAgg)
        #img = common.imgEdtImage
        #parentModule.GenBitmapTextButton.__init__(self, parent, id, img, self.label, self.position, self.size, style = self.style, name = self.name)

        #   Регистрация обработчиков событий
        

        self.BindICEvt()
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def draw_cursor(self, evt):
        """
        """
        if self.resource['onDrawCursor']:
            self.evalSpace['evt'] = evt
            self.evalSpace['self'] = self
            
            parentModule.icPlotPanel.draw_cursor(self, evt)
            self.eval_attr('onDrawCursor')
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace = self.evalSpace,
                                bCounter = bCounter, progressDlg = progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace,
                                bCounter = bCounter, progressDlg = progressDlg)
      
    #   Обработчики событий
    def OnMouseLeftDown(self, evt):
        """
        Обрабатываем нажатие правой кнопки мыши.
        """
        parentModule.icPlotPanel.draw_cursor(self, evt)
        parentModule.icPlotPanel.OnMouseLeftDown(self, evt)
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('onMouseLeftDown')

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
    win = icPloter(frame, -1, {})

    N = 5
    menMeans   = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd     = (2, 3, 4, 1, 2)
    womenStd   = (3, 5, 2, 3, 3)
    ind = numerix.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    
    p1 = win.subplot.bar(ind, menMeans,   width, color='r', yerr=womenStd)
    p2 = win.subplot.bar(ind, womenMeans, width, color='y',
             bottom=menMeans, yerr=menStd)
    win.subplot.set_xticks(ind+width)
    win.subplot.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    """
    Тестируем пользовательский класс.
    """
    test()

