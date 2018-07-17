#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент выбора ДАТЫ-ВРЕМЯ.
"""


import wx
import datetime
from ic.utils import util
from ic.kernel import io_prnt
from ic.bitmap import ic_bmp
from ic.components import icwidget as parentModule
from ic.PropertyEditor import icDefInf
from STD.controls import datetime_ctrl


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icDateTimeCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'DateTimeCtrl',
                'is_now': False,    # Установить по умолчанию на текущее ДАТУ-ВРЕМЯ?
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_CHECK_BOX: ['is_now'],
                                   },
                '__parent__': parentModule.SPC_IC_WIDGET,
                '__attr_hlp__': {'is_now': u'Установить по умолчанию на текущее ДАТУ-ВРЕМЯ?',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('calendar-property.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('calendar-property.png')

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


class icDateTimeCtrl(datetime_ctrl.icDateTimeControl,
                     parentModule.icWidget):
    """
    Компонент выбора ДАТЫ-ВРЕМЕНИ.
    ВНИМАНИЕ! Наследование от icWidget д.б. на последнем месте,
    чтобы переопределить методы setValue/getValue. Они необходимы для
    заполнения значениями в формах-карточках с помощью icFormDataManger.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)

        parentModule.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        datetime_ctrl.icDateTimeControl.__init__(self, parent=parent, id=id)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        if self.is_now:
            dt_now = self.get_now()
            self.setDateTime(dt_now)

    def get_now(self):
        """
        Текущий системное ДАТА-ВРЕМЯ.
        """
        return datetime.datetime.now()


def test(par=0):
    """
    Test class.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = icDateTimeCtrl(frame, -1, {})
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
