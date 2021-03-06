#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент для выбора дат.
Класс пользовательского визуального компонента.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import wx.adv

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icDatePickerCtrl'

#   Описание стилей компонента
ic_class_styles = {'DP_SPIN': wx.adv.DP_SPIN,
                   'DP_DROPDOWN': wx.adv.DP_DROPDOWN,
                   'DP_DEFAULT': wx.adv.DP_DEFAULT,
                   'DP_ALLOWNONE': wx.adv.DP_ALLOWNONE,
                   'DP_SHOWCENTURY': wx.adv.DP_SHOWCENTURY}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'DatePickerCtrl',
                'activate': True,
                'name': 'default',
                'description': None,
                'data_name': None,
                'style': 0,

                'position': (-1, -1),
                'size': (-1, 18),
                'value': '',
                'show': 1,
                'enable': True,
                'source': None,

                'onDateChanged': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type', 'value']},
                '__events__': {'onDateChanged': ('wx.EVT_DATE_CHANGED', 'OnDateChanged', False),
                               },
                '__parent__': icwidget.SPC_IC_WIDGET,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtCalendar'
ic_class_pic2 = '@common.imgEdtCalendar'

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.icdatepickerctrl.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


class icDatePickerCtrl(icwidget.icWidget, wx.adv.DatePickerCtrl):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        - B{type='DatePickerCtrl'}:
        - B{name='default'}:
        - B{value=''}:
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        if self.value:
            value = self.value.replace(':', '.').replace('/', '.').replace('\\', '.')
            day, month, year = [int(s) for s in value.split('.')]
            tm = wx.DateTimeFromDMY(day, month, year)
        else:
            tm = wx.DefaultDateTime
            
        wx.adv.DatePickerCtrl.__init__(self, parent, dt=tm, pos=self.position, size=self.size, style=self.style)
        
        # --- Регистрация обработчиков событий
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged)
        self.BindICEvt()
      
    # --- Обработчики событий
    def OnDateChanged(self, event):
        """
        Изменение даты.
        """
        self.eval_event('onDateChanged', event, True)
        
    # --- Функции
    def GetStrDate(self):
        """
        Возвращает выбранную дату в виде строки yyyy.mm.dd.
        """
        dt = self.GetValue()
        if dt.IsValid():
            return '%s.%s.%s' % (str(dt.GetYear()), ('00'+str(dt.GetMonth()+1))[-2:], ('00'+str(dt.GetDay()))[-2:])
        return None
   
    def SetStrDate(self, StrDate_):
        """
        Установить дату. Дата - строка в формате yyyy.mm.dd.

        :return: True - значение установилось, False - значение не установилось.
        """
        if (not isinstance(StrDate_, str)) or (not StrDate_):
            return False
        
        value = StrDate_.replace(':', '.').replace('/', '.').replace('\\', '.')
        year, month, day = [int(s) for s in value.split('.')]
        
        dt = wx.DateTimeFromDMY(day, month, year)
        self.SetValue(dt)
        
    def isChecked(self):
        """
        Помечена дата?
        """
        dt = self.GetValue()
        return dt.IsValid()
    
    def checkOff(self):
        """
        Снять метку.
        """
        self.SetValue(wx.DefaultDateTime)        
        
    def setValue(self, Data_):
        """
        Установить данные в виджет.
        """
        return self.SetStrDate(Data_)

    def getValue(self):
        """
        Получить данные из виджета.
        """
        return self.GetStrDate()
        
        
def test(par=0):
    """
    Тестируем пользовательский класс.
    
    :type par: C{int}
    :param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    
    app = ictestapp.TestApp(par)

    common.init_img()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    style = wx.adv.DP_DEFAULT | wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY
    dpc = icDatePickerCtrl(win, -1, {'position': (10, 10), 'size': (120, -1),
                                     'value': '12.05.2003',
                                     'style': style})

    frame.Show(True)
    print(dpc.GetStrDate())
    app.MainLoop()


if __name__ == '__main__':
    test()
