#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для класса wx.CheckBox.

@type SPC_IC_CHECKBOX: C{dictionary}
@var SPC_IC_CHECKBOX: Спецификация на ресурсное описание компонента icCheckBox.
Описание ключей SPC_IC_CHECKBOX:

    - B{name = 'DefaultName'}: Имя объекта.
    - B{type = 'CheckBox'}: Тип объекта.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{label=''}: Подпись.
    - B{position=(-1,-1)'}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размер объекта.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{style=wx.SIMPLE_BORDER}: Стиль (все стили icWindow/wx.Window).
    - B{init=None}: Выражение, вычисляющее значение компонента. (depricated) см. checked
    - B{attr=None}: Аттрибут поля:
        - C{'W'}: Разрешено редактировать.
        - C{'R'}: Разрешено только просматривать.
        - C{'C'}: Вычисляемое поле, разрешено редактировать.
        - C{'CR'}: Вычисляемое поле, разрешено только просматривать.
        
    - B{checked=0}: Состояние компонента после создания (1 - отмеченный, 0 - не отмеченный).
    - B{check=None}: Выражение, выполняемое после выбора объекта.
    - B{uncheck=None}: Выражение, выполняемое после отмены выбора объекта.
    - B{loseFocus=None}: Выражение, выполняемое после потери фокуса.
    - B{setFocus=None}: Выражение, выполняемое после установки фокуса.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в компоненте.
    - B{source=None}: Описание или ссылка на источник данных.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - вычисление представления поля (по атрибуту 'getvalue').
            - отрабатывает контроль значения поля(по атрибуту 'ctrl').
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue').
            - обновление представления поля (по атрибуту 'getvalue').
"""

import wx
from ic.dlg.msgbox import MsgBox
from ic.log.iclog import *
import ic.utils.util as util
import ic.utils.coderror as coderror
from ic.components.icwidget import icWidget,  SPC_IC_WIDGET
import ic.PropertyEditor.icDefInf as icDefInf

SPC_IC_CHECKBOX = {'type': 'CheckBox',
                   'name': 'default',

                   'field_name': None,
                   'label': '',
                   'style': wx.SIMPLE_BORDER,
                   'position': (-1, -1),
                   'size': (-1, -1),
                   'attr': None,
                   'foregroundColor': None,
                   'backgroundColor': None,
                   'checked': 0,
                   'check': None,
                   'uncheck': None,
                   'loseFocus': None,
                   'source': None,
                   'refresh': [],
                   'recount': [],
                   'setFocus': None,
                   'keyDown': None,

                   '__events__': {'check': ('wx.EVT_CHECKBOX', 'OnCheckBox', True),
                                  'uncheck': ('wx.EVT_CHECKBOX', 'OnCheckBox', True),
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
ic_class_name = 'icCheckBox'

#   Описание стилей компонента
ic_class_styles = {'CHK_2STATE': wx.CHK_2STATE,
                   'CHK_3STATE': wx.CHK_3STATE,
                   'CHK_ALLOW_3RD_STATE_FOR_USER': wx.CHK_ALLOW_3RD_STATE_FOR_USER,
                   'ALIGN_RIGHT': wx.ALIGN_RIGHT,
                   }

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_CHECKBOX
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtCheckBox'
ic_class_pic2 = '@common.imgEdtCheckBox'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.iccheckbox.icCheckBox-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 6)


class icCheckBox(icWidget, wx.CheckBox):
    """
    Класс icCheckBox реализует интерфейс для обработки помечаемого поля
    как обкладку над компонентом wx.CheckBox.
    """

    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icCheckBox.

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
        """
        self.bChanged = 0
        component = util.icSpcDefStruct(SPC_IC_CHECKBOX, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)
        
        label = component['label']
        pos = component['position']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        style = component['style']

        #   Номер последней заблокированной записи
        self._oldLockReck = -1

        if component['field_name'] is None:
            self.field_name = self.name
        else:
            self.field_name = component['field_name']
   
        self.check = component['check']
        self.uncheck = component['uncheck']
        self.losefocus = component['loseFocus']
        self.setfocus = component['setFocus']
                
        wx.CheckBox.__init__(self, parent, id, label, pos, style=style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        try:
            checked = self.dataset.getNameValue(self.field_name)
        except:
            checked = component['checked']
    
        if checked is not None:
            try:
                val = int(checked)
                self.SetValue(val)
            except:
                pass

        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, id=id)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.BindICEvt()

    def OnSetFocus(self, evt):
        """
        Обрабатывает установку фокуса.
        Обрабатывается потеря фокуса - используется для контроля значения поля.
        """
        #   Блокируем запись для редактирования, если позволяет объект данных
        try:
            err = self.dataset.Lock()
            
            if err in [1, 2] and rec != self._oldLockReck:
                MsgBox(None, u'Запись (%d) заблокирована err=%s' % (rec, str(err)))
                self._oldLockReck = rec
        except:
            pass

        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('setFocus')
        evt.Skip()

    def OnKillFocus(self, evt):
        """
        Обрабатывает потерю фокуса
        Обрабатывается потеря фокуса - используется для контроля значения поля.
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        self.eval_attr('loseFocus')
        evt.Skip()
        
        if self.IsModified() and self.dataset is not None:
            value = self.GetValue()
            bSet = self.dataset.setNameValue(self.field_name, int(value))
            
            #   Обновляем предсавления других объектов
            if bSet in [coderror.IC_CTRL_OK, coderror.IC_CTRL_REPL]:
                self.UpdateRelObj()

        #   Разблокируем запись для редактирования, если объект данных поддерживает блокировки
        try:
            self.dataset.Unlock()
        except:
            pass

    def OnCheckBox(self, evt):
        """
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['self'] = self
        self.bChanged = 1

        if not self.GetValue():
            self.eval_attr('uncheck')
        else:
            self.eval_attr('check')
            
        evt.Skip()

    def IsModified(self):
        """
        Возвращает признак изменения выбора
        """
        return self.bChanged

    def UpdateDataDB(self, db_name=None, bRestore=False):
        """
        Обновляем данные в базе данных.
        
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        @type bRestore: C{bool}
        @param bRestore: Признак обновления представления. Если True, то при
            неудачной попытки записи программа востановит значение поля по базе
        @rtype: C{int}
        @return: Возвращает код контроля на запись.
        """
        #   Если класс данных не задан, то считаем, что данные необходимо обновить
        if db_name is None:
            db_name = self.dataset.name

        codCtrl = coderror.IC_CTRL_FAILED
        
        if self.dataset is not None and self.dataset.name == db_name:

            value = self.GetValue()
            codCtrl = self.dataset.setNameValue(self.field_name, value)
                
            if bRestore and codCtrl in [coderror.IC_CTRL_FAILED, coderror.IC_CTRL_FAILED_IGNORE]:
                self.UpdateViewFromDB()
            
        return codCtrl
    
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
        return self.IsChecked()
    
    def setValue(self, Value_):
        """
        Установить значение редактора.
        """
        self.SetValue(bool(Value_))


def test(par=0):
    """
    Тестируем класс icCheckBox
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icCheckBox Test')
    win = wx.Panel(frame, -1)
    ctrl_1 = icCheckBox(win, -1, {'label': 'CheckBox', 'position': (10, 10),
                                  'keyDown': 'print \'keyDown in CheckBox\'',
                                  'setFocus': 'print \'SetFocus\'',
                                  'loseFocus': 'print \'loseFocus\'',
                                  'check': 'print \'check\'',
                                  'uncheck': 'print \'uncheck\''})
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
