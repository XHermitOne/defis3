#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент выбора месяца.
"""

import datetime
import wx
from ic.utils import util
from ic.kernel import io_prnt
from ic.bitmap import ic_bmp
from ic.PropertyEditor import icDefInf

from ic.components.custom import icchoice as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icMonthChoiceCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'MonthChoiceCtrl',
                'is_now': True,    # Установить по умолчанию на текущий месяц?
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_CHECK_BOX: ['is_now'],
                                   },
                '__parent__': parentModule.ic_class_spc,
                '__attr_hlp__': {'is_now': u'Установить по умолчанию на текущий месяц?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('calendar-month.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('calendar-month.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 0, 0, 2)

MONTH_LIST = (u'Январь', u'Февраль', u'Март', u'Апрель',
              u'Май', u'Июнь', u'Июль', u'Август',
              u'Сентябрь', u'Октябрь', u'Ноябрь', u'Декабрь',
              )

class icMonthChoiceCtrl(parentModule.icChoice):
    """
    Компонент выбора месяца.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        # Инициализировать список выбора в спецификации
        self.month_list = None
        component['items'] = self.get_months()

        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)

        parentModule.icChoice.__init__(self, parent, id, component, logType, evalSpace,
                                       bCounter, progressDlg)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        if self.is_now:
            now_month = datetime.datetime.now().month-1
            self.SetSelection(now_month)

    def get_months(self):
        """
        Список месяцев.
        """
        if self.month_list:
            # Если список уже заполнен то просто вернуть его
            return self.month_list

        # Заполнить список месяцев
        self.month_list = MONTH_LIST
        return self.month_list

    def get_selected_month_name(self):
        """
        Имя выбранного месяца.
        """
        return self.GetValue()

    def get_selected_month_num(self):
        """
        Номер выбранного месяца.
        """
        return self.GetSelection()+1


def test(par=0):
    """
    Test class.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = icMonthChoiceCtrl(frame, -1, {})
    btn = wx.Button(frame, -1, 'test', pos=wx.Point(100, 50))

    def on_test_btn_click(event):
        print('RESULT:', win.get_selected_month_name(), win.get_selected_month_num())
        event.Skip()

    btn.Bind(wx.EVT_BUTTON, on_test_btn_click)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
