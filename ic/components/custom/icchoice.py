#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.Choice.

@type SPC_IC_CHOICE: C{dictionary}
@var SPC_IC_CHOICE: Спецификация на ресурсное описание текстового поля с выбором из списка:

    - B{type='Choice'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{field_name='default'}: Имя поля базы данных, которое отображает компонент.
    - B{style=wx.SIMPLE_BORDER | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB}: Стиль компонента (стили icWindow/wx.Window).
    - B{position=(-1, -1)}: Расположение компонента на родительском окне.
    - B{size=(-1,-1)}: Размер компонента.
    - B{items=None}: Выражение вычисляющее список выбора. Если выражение возвращает словарь,
        то он используется как словарь замен при записи в объект данных.
    - B{foregroundColor=(0, 0, 0)}:  Цвет текста.
    - B{backgroundColor=(255, 255, 255)}: Цвет фона.
    - B{choice=None}: Выражение, выполняющаяся при выборе пункта меню.
    - B{loseFocus=None}: Выражение, выполняющееся при потери фокуса.
    - B{setFocus=None}: Выражение, выполняющееся при установки фокуса.
    - B{source=None}: Описание или ссылка на источник данных.
    - B{refresh=None}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
        Если атрибут равен None, то обновляются все объекты работающие с классами данных.
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных. Стадии пересчета вычисляемого поля:
            - вычисление представления поля (по атрибуту 'getvalue').
            - отрабатывает контроль значения поля(по атрибуту 'ctrl').
            - Если контроль проходит запись в базу вычисленного значения (по атрибуту 'setvalue').
"""

import wx
import ic.utils.util as util
from ic.utils import ic_util
from ic.components.icwidget import icWidget, SPC_IC_WIDGET
from ic.utils import coderror
from ic.components import icwindow
from ic.kernel import io_prnt
from ic.dlg import ic_dlg
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf


LOG_TYPE = 0
SPC_IC_CHOICE = {'type': 'Choice',
                 'name': 'default',

                 'field_name': None,
                 'style': wx.SIMPLE_BORDER | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB,
                 'position': (-1, -1),
                 'size': (-1, -1),
                 'items': None,
                 'foregroundColor': (0, 0, 0),
                 'backgroundColor': (255, 255, 255),
                 'loseFocus': None,
                 'setFocus': None,
                 'choice': None,
                 'refresh': [],
                 'recount': [],
                 'source': None,

                 '__events__': {'choice': ('wx.EVT_CHOICE', 'OnChoice', False),
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
ic_class_name = 'icChoice'

#   Описание стилей компонента
ic_class_styles = icwindow.ic_class_styles

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_CHOICE
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtChoice'
ic_class_pic2 = '@common.imgEdtChoice'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.custom.icchoice.icChoice-class.html'
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 0, 7)


class icChoice(icWidget, wx.Choice):
    """
    Класс icChoice реализует интерфейс для поля ввода с возможностью выбора из списка
        - обкладка над компонентом wx.Choice.
    """

    def setDictRepl(self, dictRepl):
        """
        Устанавливает словарь замен значений в списке и значений в объекте данных.
        @type dictRepl: C{}
        @param dictRepl: Словарь замен.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """

        if not isinstance(dictRepl, dict):
            return False
        else:
            self._dictRepl = dictRepl

            #   Чистим список
            self.Clear()

            #   Заполняем список в алфавитном порядке (исключение Ё)
            lst = dictRepl.values()
            lst.sort()
            
            for val in lst:
                self.Append(str(val))

        return True
    
    def setChoiceList(self, items):
        """
        Устанавливает список выбора.
        
        @type items: C{list | tuple}
        @param items: Список выбора.
        @rtype: C{bool}
        @return: Признак успешного выполнения.
        """
        if not type(items) in (list, tuple):
            return False
        
        #   Чистим список
        self.Clear()
        self._dictRepl = None
        
        #   Заполняем список новыми значениями
        for item in items:
            self.Append(ic_util.toUnicode(item))

        return True
    
    def setItems(self, items, sel=-1):
        """
        Устанавливаем список выбора - элементы картежи из ключа и значения.
        """
        self.Clear()
        self._itemsLst = items
        self._dictRepl = None
        #   Заполняем список новыми значениями
        for item in items:
            self.Append(item[1])
        
        self.SetSelection(sel)
        
    def getDictRepl(self):
        """
        Возвращает указатель на словарь замен.
        """
        return self._dictRepl
    
    def __init__(self, parent, id, component, logType=0, evalSpace={},
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icChoice.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        self.bChanged = 0

        util.icSpcDefStruct(SPC_IC_CHOICE, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        size = component['size']
        pos = component['position']
        style = component['style']
        
        if component['field_name'] is None:
            self.field_name = self.name
        else:
            self.field_name = component['field_name']
        
        self.losefocus = component['loseFocus']
        self.setfocus = component['setFocus']
        self.choice = component['choice']

        #   Номер последней заблокированной записи
        self._oldLockReck = -1

        #   Словарь замен. Ключи - соответствующие значения в объекте данных, значения  формируют список выбора
        self._dictRepl = None
        self._itemsLst = None
        
        # Обрабатываем аттрибут инициализации списка
        if not component['items']:
            self.items = []
        elif type(component['items']) in (list, tuple):
            self.items = component['items']
        elif isinstance(component['items'], dict):
            self._dictRepl = component['items']
            self.items = self._dictRepl.values()
            self.items.sort()
        else:
            ret = util.getICAttr('@'+component['items'], self.evalSpace, 'getICAttr() Error in icchoice.__init__(...) <items> name=%s' % self.name)

            if type(ret) in (list, tuple):
                self.items = ret
            elif isinstance(ret, dict):
                self._dictRepl = ret
                self.items = self._dictRepl.values()
                self.items.sort()
            else:
                self.items = []
            
        # Создаем объект
        wx.Choice.__init__(self, parent, id, pos, size, self.items, style, name=self.name)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        try:
            self.SetValue(self.dataset.getNameValue(self.field_name))
        except:
            pass

        self.Bind(wx.EVT_CHOICE, self.OnChoice, id=id)
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
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Запись (%d) заблокирована err=%s' % (rec, str(err)), self.parent)
                self._oldLockReck = rec

        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.eval_attr('setFocus')
        evt.Skip()

    def OnKillFocus(self, evt):
        """
        Обрабатывает потерю фокуса.
        """
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
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
        Возвращает признак изменения выбора.
        """
        return self.bChanged

    def OnChoice(self, evt):
        """
        Обрабатывает сообщение о изменении выбора. Флаг изменения объекта устанавливается в True.
        """
        self.bChanged = 1
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt

        # Обрабатываем выбор пункта из списка
        self.eval_attr('choice')
        evt.Skip()

    def GetValue(self):
        """
        Функция возвращает реальное значение, которое получается через словарь замен.
        """
        value = self.GetRealValue()
        
        if value is None:
            # Ничего не выбрано
            return value
        
        if self._itemsLst:
            indx = self.GetSelection()
            return self._itemsLst[indx][0]

        elif self._dictRepl:
            for key, val in self._dictRepl.items():
                if value == val:
                    value = key
                    break

        return value
    
    def GetRealValue(self):
        """
        Возвращается текущий выбор из списка.
        """
        # Определяем текущий выбор
        indx = self.GetSelection()
        if indx >= 0:
            value = self.GetString(indx)
            return value

        return None

    def SetValue(self, value):
        """
        Функция преобразует входное значение в одно из значений списка (если это возможно)
        и установит его в качестве текущего. Преобразование производится через словарь
        замен _dictRepl.

        @type value: C{string}
        @param value: Устанавливаемое значение.
        """
        ret = False
        if self._itemsLst:
            for i, el in enumerate(self._itemsLst):
                if el[0] == value:
                    self.SetSelection(i)
                    return True
        elif self._dictRepl:
            try:
                val = self._dictRepl[value]
                ret = self.SetRealValue(val)
            except:
                self.SetSelection(-1)
                io_prnt.outLastErr('KeyError in icchoice.SetValue(val), val=%s' % value)
        else:
            ret = self.SetRealValue(value)
            
        return ret
    
    def SetRealValue(self, value):
        """
        Устанавливает определенное значение в качестве текущего. Значение сравнивается со списком
        выбора, находится самое подходящее, которое и выбирается в качестве текущего значения.

        @param value: Значение которое надо поставить в качестве текущего
        @rtype: C{bool}
        @return: Возвращает признак успешного выполнения
        """
        val = str(value)

        for i in xrange(self.GetCount()):
            str_item = self.GetString(i)

            if str_item.find(val) == 0:
                self.SetSelection(i)
                return True
            
        self.SetSelection(-1)
        return False
    
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
        @rtype: C{bool}
        @return: Возвращает признак успешного обновления.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name
            
        if self.dataset is not None and self.dataset.name == db_name and self.bStatusVisible:
            self.SetValue(self.dataset.getNameValue(self.field_name))
            return True
    
        return False


def test(par=0):
    """
    Тестируем класс icChoice
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    frame = wx.Frame(None, -1, 'icChoice Test', size=(100,100))
    win = wx.Panel(frame, -1)
    ctrl_1 = icChoice(win, -1, {'items': {u'a': u'а', u'b': u'б', u'c': u'ц', u'd': u'д'},
                                'position': (20, 0),
                                'choice': 'print \'choice\''})
    ctrl_1.SetSelection(0)

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
