#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Индикатор состояний.
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

import wx.lib.buttons as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'Indicator'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'__events__': {'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False)}, 'type': 'defaultType', 'name': 'default', 'label': ''}
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImage'
ic_class_pic2 = '@common.imgEdtImage'

#   Путь до файла документации
ic_class_doc = 'public/icurindicator.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class Indicator(icwidget.icWidget, parentModule.GenBitmapTextButton):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:
        - B{label=''}:

    """

    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace={},
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
        img = common.imgEdtImage
        parentModule.GenBitmapTextButton.__init__(self, parent, id, img, self.label, self.position, self.size,
                                                  style=self.style, name=self.name)
        
        #   Регистрация обработчиков событий
        
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.BindICEvt()
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, self.evalSpace, 
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, self.evalSpace, 
                                 bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий
    
    def OnKeyDown(self, evt):
        """
        Обработчик события wx.EVT_KEY_DOWN, атрибут=keyDown
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        ret, val = self.eval_attr('keyDown')
        if ret and val:
            evt.Skip()
        elif not ret:
            evt.Skip()


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
    
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()
