#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент выбора года.
"""


import wx
import datetime
from ic.utils import util
from ic.kernel import io_prnt
from ic.bitmap import ic_bmp
from ic.components.custom import icchoice as parentModule
from ic.PropertyEditor import icDefInf


DEFAULT_MIN_YEAR = 1950
DEFAULT_MAX_YEAR = 2050

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icYearChoiceCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'YearChoiceCtrl',
                'min': DEFAULT_MIN_YEAR,
                'max': DEFAULT_MAX_YEAR,
                'is_now': True,    # Установить по умалчанию на текущий год?
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_CHECK_BOX: ['is_now'],
                                   },
                '__parent__': parentModule.ic_class_spc,
                '__attr_hlp__': {'min': u'Минимальный возможный год',
                                 'max': u'Максимальный возможный год',
                                 'is_now': u'Установить по умалчанию на текущий год?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('calendar-share.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('calendar-share.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 0, 0, 4)


class icYearChoiceCtrl(parentModule.icChoice):
    """
    Компонент выбора года.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        self.min_year = component.get('min', DEFAULT_MIN_YEAR)
        self.max_year = component.get('max', DEFAULT_MAX_YEAR)
        self.year_list = None
        component['items'] = self.get_years()

        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)

        parentModule.icChoice.__init__(self, parent, id, component, logType, evalSpace,
                                       bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        if self.is_now:
            now_year = str(self.get_now_year())
            self.SetValue(now_year)

    def get_years(self):
        """
        Список лет.
        """
        if self.year_list:
            # Если список уже заполнен то просто вернуть его
            return self.year_list

        # Заполнить список месяцев
        self.year_list = [str(i) for i in range(self.min_year, self.max_year)]
        return self.year_list

    def get_now_year(self):
        """
        Текущий системный год.
        """
        return datetime.datetime.now().year

    def get_selected_year(self):
        """
        Выбранный год.
        """
        value = self.GetValue()
        return int(value) if value.isdigit() else self.get_now_year()


def test(par=0):
    """
    Test class.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = icYearChoiceCtrl(frame, -1, {})
    btn = wx.Button(frame, -1, 'test', pos=wx.Point(100, 50))

    def on_test_btn_click(event):
        print('RESULT:', win.get_selected_year())
        event.Skip()

    btn.Bind(wx.EVT_BUTTON, on_test_btn_click)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
