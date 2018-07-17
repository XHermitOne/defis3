#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.SpinCtrl

@type SPC_IC_SPINNER: C{dictionary}
@var SPC_IC_SPINNER: Спецификация на ресурсное описание панели инструментов.
Описание ключей SPC_IC_SPINNER:

    - B{type='Spinner'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{style=wx.SP_WRAP | wx.SIMPLE_BORDER}: Стиль окна.
    - B{value=0}: Значение после создания объекта.
    - B{min=0}: Минимальное значение поля.
    - B{max=10}: Максимальное значение поля.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры поля.
    - B{init=None}: Выражение, вычисляющее значение компонента.
    - B{attr=None}: Аттрибут поля.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{font={}}: Шрифт текста.
    - B{loseFocus=None}: Выражение, выполняемое после потери фокуса.
    - B{setFocus=None}: Выражение, выполняемое после установки фокуса.
    - B{onSpin=None}: Выражение, выполняемое после нажатия на одну из кнопок
        <Up> и <Down>(сообщение EVT_SPIN).
    - B{source=None}: Описание или ссылка на источник данных.
    - B{refresh=[]}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - вычисление представления поля (по атрибуту 'getvalue')
            - отрабатывает контроль значения поля(по атрибуту 'ctrl')
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue')
            - обновление представления поля (по атрибуту 'getvalue')
    - B{keyDown=None}: Выражение, выполняемое при получении сообщения от клавиатуры.
    
@type ICSpinnerStyle: C{dictionary}
@var ICSpinnerStyle: Словарь специальных стилей компонента. Описание ключей ICSpinnerStyle:

    - C{wx.SP_ARROW_KEYS} - Пользователь может использовать стрелки для изменения значения.
    - C{wx.SP_WRAP} - Значение компонента лежит в заданных пределах (min,max).

"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
from ic.utils import util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
from ic.components.icfont import *
import ic.PropertyEditor.icDefInf as icDefInf
from ic.utils import coderror

ICSpinnerStyle = {'SP_ARROW_KEYS': wx.SP_ARROW_KEYS,
                  'SP_WRAP': wx.SP_WRAP}

SPC_IC_SPINNER = {'type': 'Spinner',
                  'name': 'default',

                  'field_name': None,
                  'style': 0,
                  'position': (-1, -1),
                  'size': (-1, -1),
                  'init': None,
                  'value': 0,
                  'min': 0,
                  'max': 10,
                  'foregroundColor': None,
                  'backgroundColor': None,
                  'font': {},
                  'loseFocus': None,
                  'setFocus': None,
                  'onSpin': None,
                  'keyDown': None,
                  'refresh': [],
                  'source': None,

                  '__attr_types__': {icDefInf.EDT_NUMBER: ['min', 'max', 'value'],
                                     },
                  '__events__': {'onSpin': ('wx.EVT_SPIN', 'OnSpin', True),
                                 'setFocus': ('wx.EVT_SET_FOCUS', 'OnSetFocus', False),
                                 'loseFocus': ('wx.EVT_KILL_FOCUS', 'OnKillFocus', False),
                                 },
                  '__parent__': SPC_IC_WIDGET,
                  }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------
#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icControlsType

#   Имя пользовательского класса
ic_class_name = 'icSpinner'

#   Описание стилей компонента
ic_class_styles = ICSpinnerStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_SPINNER
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtSpinner'
ic_class_pic2 = '@common.imgEdtSpinner'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icspinner.icSpinner-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 6)


class icSpinner(icWidget, wx.SpinCtrl):
    """
    Класс icSpinner реализует интерфейс для обработки компонента wx.SpinCtrl.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icSpinner

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        self.bChanged = 0

        component = util.icSpcDefStruct(SPC_IC_SPINNER, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        for key in lst_keys:
            setattr(self, key, component[key])

        if component['field_name'] is None:
            self.field_name = self.name
        else:
            self.field_name = component['field_name']
   
        min = util.getICAttr(component['min'], evalSpace,
                             'Error in getICAttr in icspinner. name=%s <min>=%s' % (self.name, component['min']))
        max = util.getICAttr(component['max'], evalSpace,
                             'Error in getICAttr in icspinner. name=%s <max>=%s' % (self.name, component['max']))
        val = util.getICAttr(component['value'], evalSpace,
                             'Error in getICAttr in icspinner. name=%s <value>=%s' % (self.name, component['value']))
        
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']
        pos = component['position']
        size = component['size']
        size = (int(size[0]), int(size[1]))
        font = component['font']
        
        #   Номер последней заблокированной записи
        self._oldLockReck = -1

        wx.SpinCtrl.__init__(self, parent, id, str(val), pos, size, style,
                             min=min, max=max, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))
            
        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        try:
            self.SetValue(str(self.dataset.getNameValue(self.field_name)))
        except:
            pass
        
        obj = icFont(font)
        self.SetFont(obj)
        
        self.Bind(wx.EVT_SPIN, self.OnSpin, id=id)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.BindICEvt()

    def OnSetFocus(self, evt):
        """
        Обрабатывает установку фокуса.
        """
        #   Блокируем запись для редактирования, если позволяет объект данных
        if self.dataset and not self.evalSpace['__block_lock_rec']:
            err = self.dataset.Lock()
                
            if err in [1, 2] and rec != self._oldLockReck:
                MsgBox(None, u'Запись (%d) заблокирована err=%s' % (rec, str(err)))
                self._oldLockReck = rec

        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.eval_attr('setFocus')
        evt.Skip()

    def OnKillFocus(self, evt):
        """
        Обрабатывает потерю фокуса.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.eval_attr('loseFocus')
        evt.Skip()
        
        if self.IsModified() and self.dataset is not None:
            value = self.GetValue()
            ret = self.dataset.setNameValue(self.field_name, value)
            
            #   Обновляем предсавления других объектов
            if ret in [coderror.IC_CTRL_OK, coderror.IC_CTRL_REPL]:
                self.UpdateRelObj()
                
        #   Разблокируем запись для редактирования, если объект данных поддерживает блокировки
        try:
            self.dataset.Unlock()
        except:
            pass
        
    def IsModified(self):
        """
        Возвращает признак изменения выбора
        """

        return self.bChanged

    def OnSpin(self, evt):
        """
        Обрабатывает сообщение о изменении выбора.
        Флаг изменения объекта устанавливается в true
        """

        self.bChanged = 1
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        
        self.eval_attr('onSpin')
        evt.Skip()
            
    def UpdateViewFromDB(self, db_name=None):
        """
        Обновляет данные в текстовом поле после изменения курсора в источнике данных.
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name
            
        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            try:
                val = int(self.dataset.getNameValue(self.field_name))
            except:
                val = 0
                
            self.SetValue(val)

    def getValue(self):
        """
        Получить значение редактора.
        """
        return self.GetValue()

    def setValue(self, Value_):
        """
        Установить значение редактора.
        """
        if type(Value_) in (str, unicode) and Value_.strip().isdigit():
            Value_ = int(Value_.strip())
        elif type(Value_) in (int, float):
            Value_ = int(Value_)
        else:
            self.SetValue(0)
            return
        self.SetValue(Value_)


def test(par=0):
    """
    Тестируем класс icSpinner.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icSpinner Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icSpinner(win, -1, {'position': (30, 10),
                                 'keyDown': 'print \'keyDown in Spinner\'',
                                 'style': 0})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
