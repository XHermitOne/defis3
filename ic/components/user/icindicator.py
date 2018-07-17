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

import wx, sys
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import os
import ic.bitmap.icbitmap as icbitmap

import ic.components.custom.icheadcell as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'IndicatorState'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'IndicatorState',
                'name': 'default',

                'states': [],
                'mouseClick': None,
                'alignmentImg': '(\'left\', \'middle\')',
                'child': [],
                'images': [],
                'path': '',

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   12: ['path', 'mouseClick'],
                                   20: ['images', 'states'],
                                   icDefInf.EDT_CHOICE: ['alignmentImg', 'alignment'],
                                   },
                '__events__': {'mouseClick': ('wx.EVT_LEFT_UP', 'OnMouseClick', False),
                               },
                '__lists__': {'alignmentImg': ['(\'left\', \'middle\')',
                                               '(\'left\', \'top\')',
                                               '(\'left\', \'bottom\')',
                                               '(\'centred\', \'middle\')',
                                               '(\'centred\', \'top\')',
                                               '(\'centred\', \'bottom\')',
                                               '(\'right\', \'middle\')',
                                               '(\'right\', \'top\')',
                                               '(\'right\', \'bottom\')'],
                              'alignment': ['(\'left\', \'middle\')',
                                            '(\'left\', \'top\')',
                                            '(\'left\', \'bottom\')',
                                            '(\'centred\', \'middle\')',
                                            '(\'centred\', \'top\')',
                                            '(\'centred\', \'bottom\')',
                                            '(\'right\', \'middle\')',
                                            '(\'right\', \'top\')',
                                            '(\'right\', \'bottom\')']                                            
                              },
                '__parent__': parentModule.ic_class_spc,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtGauge'
ic_class_pic2 = '@common.imgEdtGauge'

#   Путь до файла документации
ic_class_doc = 'public/icurindicator.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'DatasetNavigator', 'GridCell']

#   Версия компонента
__version__ = (0, 0, 0, 2)


class IndicatorState(parentModule.icHeadCell):
    """
    Описание пользовательского компонента.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{name='default'}:
        - B{states=[]}:
        - B{mouseClick=None}:
        - B{child=[]}:
        - B{images=[]}:
        - B{path=''}:
        - B{type='IndicatorState'}:
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

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])
            
        parentModule.icHeadCell.__init__(self, parent, id, component, logType, evalSpace)
        
        if not self.path:
            self.path = os.getcwd()
        else:
            self.path = util.getICAttr(component['path'], self.evalSpace, msg='ERROR')
            
        self.path = self.path.replace('\\', '/')
        if self.path[-1] != '/':
            self.path += '/'

        #   Создаем список картинок. Каждому состоянию соответствует картинка
        self._alignmentImg = eval(self.alignmentImg)
        
        self.imageList = []
        self.statesDict = {}
        
        for indx, nm in enumerate(self.images):
            if not type(nm) in (str, unicode):
                img = nm
                self.imageList.append(img)
            else:
                file = self.path+nm
                bmptype = icbitmap.icBitmapType(file)
                if bmptype is not None and os.path.isfile(file):
                    image_file = wx.Image(file, bmptype)
                    img = image_file.ConvertToBitmap()
                    self.imageList.append(img)
                
            if indx < len(self.states):
                st = self.states[indx]
            else:
                st = None
                
            self.statesDict[indx] = (img, st)

        self.imageState = None
        self._oldState = -1
        self.SetState(0)
        
        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseClick)
        self.BindICEvt()

        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)
        
    def SetState(self, state):
        """
        Устанавливает нужное состояние компонента.
        @type state: C{int}
        @param state: Нужное состояние.
        @rtype: C{bool}
        @return: Признак успешного завершения.
        """
        if state in self.statesDict.keys():
            img, val = self.statesDict[state]
            pw, ph = img.GetWidth(), img.GetHeight()
            sx, sy = self.GetSize()
            
            ah, av = self._alignmentImg
            
            if ah == 'left':
                x = 2
            elif ah == 'right':
                x = (sx - pw) - 2
            else:
                x = (sx - pw)/2
                
            if av == 'top':
                y = 2
            elif av == 'bottom':
                y = (sy - ph) - 2
            else:
                y = (sy - ph)/2
                        
            if not self.imageState:
                self.imageState = wx.StaticBitmap(self, -1, img,
                                                  pos=(x, y), size=(pw, ph))
            else:
                self.imageState.SetBitmap(img)
                self.imageState.SetPosition((x, y))
                if wx.Platform == '__WXMSW__':
                    self.imageState.Enable(False)

            self._oldState = state
            return True
        
        return False
            
    def SetNextState(self):
        """
        Устанавливает следующее состояние.
        @rtype: C{bool}
        @return: Признак успешного завершения.
        """
        st = self.GetState()
        
        if st+1 < len(self.images):
            return self.SetState(st+1)
        else:
            return self.SetState(0)

    def SetStateValue(self, value):
        """
        Устанавливавет состояние по значению.
        @type value: C{float}
        @param value: Значение по которому определяется состояние.
        @rtype: C{bool}
        @return: Признак успешного завершения.
        """
        for key in self.statesDict.keys():
            st = self.statesDict[key][1]
            
            if st:
                min, max = st
                
                if value >= min and value <= max:
                    return self.SetState(key)
                    
        return False
        
    def GetState(self):
        """
        Возвращает номер текущего состояния.
        """
        return self._oldState
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий
    
    def OnMouseClick(self, evt):
        """
        Обработчик события wx.EVT_LEFT_UP, атрибут=mouseClick.
        """
        self.eval_event('mouseClick', evt, True)


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
    
    ctrl_1 = IndicatorState(win, -1, {'position': (100, 35), 'size': (100, 30)})
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
