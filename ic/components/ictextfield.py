#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Обкладка для компонента wx.TextCtrl.

@type SPC_IC_TEXTFIELD: C{dictionary}
@var SPC_IC_TEXTFIELD: Спецификация на ресурсное описание компонента:

    - B{type='TextField'}: Тип компонента.
    - B{name='default'}: Имя компонента.
    - B{field_name=None}: Имя поля базы данных, которое отображает компонент.
    - B{style=wx.SIMPLE_BORDER | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB}: Стиль компонента.
    - B{position=(-1, -1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размеры поля.
    - B{value= ''}: Значение поля после создания компонента, если компонент не привязан к атрибуту класса данных.
    - B{attr=None}: Аттрибут поля.
    - B{font={}}: Шрифт текста.
    - B{pic='S'}: Шаблон ввода. Если определен атрибут getvalue, то сначала вычисляется выражение, а затем
        накладывается шаблон. Если определен атрибут setvalue, то сначала убираются символы шаблона, а затем
        вычисляется выражение.
    - B{valid=None}: Не используется.
    - B{use_fdict=None}: Признак включения частотного словаря.
    - B{foregroundColor=(0, 0, 0)}: Цвет текста.
    - B{backgroundColor=(255, 255, 255)}: Цвет фона.
    - B{getvalue=None}: Выражение, вычисляющее значение поля для вывода на форму (выражение вычисляется в функции
        SetValue() объекта TextCtrl). Для выражения доступна переменная value, которая передается в параметрах
        функции SetValue(). Например, для того, чтобы поле отображало символ '$' в конце суммы выражение может быть
        следующего вида: C{str(value).replace(' $', '')+' $'}.
    - B{setvalue=None}: Выражение, вычисляющее значение для записи в базу данных (выражение вычисляется в функции
        GetValue() объекта TextCtrl). Для выражения доступна переменная value, которая передается в параметрах
        функции GetValue(). Например, для того, чтобы  хранить сумму в долларах без символа '$' выражение может
        быть следующего вида: C{float(value.replace(' $', ''))}.
    - B{init=None}: Выражение, вычисляющее первоначальное значение поля при создании нового объекта данных.
    - B{hlp=None}: Выражение, выполняемое после нажатия F1 либо спец. кнопки. Если выражение возвращает None,
        то значение поле не изменяется, в другом случае текстовое поле принимает возвращаемое значение.
    - B{ctrl=None}: Выражение контроля ввода (см. описания кодов контроля в модуле coderror.py).
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки.
    - B{changed=None}: Выражение, выполняемое после изменения текста.
    - B{setFocus=None}: Выражение, выполняемое после установки фокуса.
    - B{source=None}: Описание или ссылка на источник данных.
    - B{refresh=[]}: Выражение, возвращающее список обновляемых компонентов. Под обновлением понимается обновление
        представлений компонентов (для вычисляемых полей это соответствует вычислению выражения аттрибута 'getvalue').
    - B{recount=None}: Выражение, возвращающее список пересчитываемых компонентов. Под этим понимается пересчет
        значений хранимых в базе данных.

@type ICTextFieldStyle: C{dictionary}
@var ICTextFieldStyle: Словарь специальных стилей компонента. Описание ключей ICTextFieldStyle:

    - C{wx.TE_PROCESS_ENTER}:  Компонент будет генерировать сообщение wx.EVENT_TYPE_TEXT_ENTER_COMMAND.
    - C{wx.TE_PROCESS_TAB}:  Компонент будет получать сообщение EVT_CHAR при нажатии TAB.
    - C{wx.TE_MULTILINE}: Многострочное поле ввода.
    - C{wx.TE_PASSWORD}: Поле ввода пароля.
    - C{wx.TE_READONLY}: Нередактируемый текст.
    - C{wx.TE_RICH}: Использует Rich control под Win32, позволяет редактировать текст размером > 64Kb
        Стиль игнорируется под другими платформами.
    - C{wx.TE_RICH2}  Использует Rich control версии 2.0 или 3.0 под Win32.Стиль игнорируется под другими платформами.
    - C{wx.TE_AUTO_URL}:  Подсвечивает URLы и генерирует wx.TextUrlEvents при наведении мышкой курсора.
        Стиль поддерживается только под Win32 и требует стиля wx.TE_RICH.
    - C{wx.TE_NOHIDESEL}:  По умолчанию Windows компонент не отмечает выбранный блок когда
        компонент не имеет фокуса - используя этот стиль можно заставить компонет всегда показывать
        выбранный блок. Стиль игнорируется под другими платформами.
    - C{wx.HSCROLL}:  Создает горизонтальную прокурутку. Не используется под GTK+.
    - C{wx.TE_LEFT}:  Выравнивание по левому краю (по умолчанию).
    - C{wx.TE_CENTRE}:  Выравнивание по центру.
    - C{wx.TE_RIGHT}:  Выравнивание по правому краю.
    - C{wx.TE_DONTWRAP}:  Аналог wx.HSCROLL.
    - C{wx.TE_LINEWRAP}:  Разворачивает так, чтобы текст был виден полностью. (wx.Unix only currently).
    - C{wx.TE_WORDWRAP}:  Разворачивает так, чтобы слово было видно полностью (wx.Unix only currently).
"""
import wx
from ic.dlg.msgbox import MsgBox
from .icFieldTempl import *
from ic.log.iclog import *
import ic.utils.util as util
from ic.utils.coderror import *
from .icfont import icFont
from .icwidget import icWidget, SPC_IC_WIDGET
from . import icEvents
import ic.utils.frequencydict as frequencydict
from ic.kernel import io_prnt
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

ICTextFieldStyle = {'TE_PROCESS_ENTER': wx.TE_PROCESS_ENTER,
                    'TE_PROCESS_TAB': wx.TE_PROCESS_TAB,
                    'TE_MULTILINE': wx.TE_MULTILINE,
                    'TE_PASSWORD': wx.TE_PASSWORD,
                    'TE_READONLY': wx.TE_READONLY,
                    'TE_RICH': wx.TE_RICH,
                    'TE_RICH2': wx.TE_RICH2,
                    'TE_AUTO_URL': wx.TE_AUTO_URL,
                    'TE_NOHIDESEL': wx.TE_NOHIDESEL,
                    'HSCROLL': wx.HSCROLL,
                    'TE_LEFT': wx.TE_LEFT,
                    'TE_CENTRE': wx.TE_CENTRE,
                    'TE_RIGHT': wx.TE_RIGHT,
                    'TE_DONTWRAP': wx.TE_DONTWRAP,
                    'TE_LINEWRAP': wx.TE_LINEWRAP,
                    'TE_WORDWRAP': wx.TE_WORDWRAP,
                    'SIMPLE_BORDER': wx.SIMPLE_BORDER}

SPC_IC_TEXTFIELD = {'type': 'TextField',
                    'name': 'default',
                    'activate': True,

                    'field_name': None,
                    'data_name': None,
                    'style': 0,
                    'position': (-1, -1),
                    'size': (-1, -1),
                    'value': '',

                    'pic': 'S',
                    'font': {},
                    'foregroundColor': (0, 0, 0),
                    'backgroundColor': (255, 255, 255),
                    'getvalue': None,
                    'setvalue': None,
                    'use_fdict': False,
                    'hlp': None,
                    'ctrl': None,
                    'init': None,
                    'valid': None,
                    'source': None,
                    'refresh': [],
                    'recount': [],
                    'keyDown': None,
                    'changed': None,
                    'setFocus': None,

                    '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['pic', 'valid', 'data_name'],
                                       icDefInf.EDT_CHECK_BOX: ['use_fdict'],
                                       },
                    '__events__': {'changed': ('wx.EVT_TEXT', 'OnTextChanged', False),
                                   'setFocus': ('wx.EVT_SET_FOCUS', 'OnSetFocus', False),
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
ic_class_name = 'icTextField'

#   Описание стилей компонента
ic_class_styles = ICTextFieldStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_TEXTFIELD
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtTextField'
ic_class_pic2 = '@common.imgEdtTextField'

#   Путь до файла документации
ic_class_doc = None

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 1, 4)

#   Код спец. кнопок, которые не обрабатываются при форматировании теста по шаблону
KEYTEMPLATE = [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_BACK, wx.WXK_HOME, wx.WXK_DELETE, wx.WXK_END,
               wx.WXK_SHIFT, wx.WXK_F1, wx.WXK_TAB, wx.WXK_RETURN]


class icTextField(icWidget, wx.TextCtrl):
    """
    Класс icTextField реализует объект ввода текста. Данный объект может
    быть привязан к определенному источнику данных через аттрибут 'source'.
    """
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор для создания icTextField.
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
        self.bkillfocus = True
        #   Признак временной потери фокуса
        self.bTimeLosefocus = False
        self.counter = 0
        self.id = id
        self.bChanged = False
        #   Номер последней заблокированной записи
        self._oldLockReck = -1
        #   Старое значение
        self._oldValue = None

        util.icSpcDefStruct(SPC_IC_TEXTFIELD, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        if self.refresh in [None, []]:
            self.refresh = self.recount

        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        text = component['value']

        #   Вычисляем текст поля после создания объекта#
        if text.find('@') == -1:
            val = util.getICAttr('@'+text, self.evalSpace, None)
        else:
            val = util.getICAttr('@'+text, self.evalSpace, 'Error in ictextfield.__init__()<text>. Name:' + self.name)

        if not val:
            val = text

        if component['field_name'] in ('', None, 'None'):
            self.field_name = self.name
        else:
            self.field_name = component['field_name']

        size = component['size']
        pos = component['position']
        font = component['font']

        #   Преобразователи предстваления
        self.getvalue = component['getvalue']
        self.setvalue = component['setvalue']
        #   Шаблон ввода и служебные атрибуты
        self.pic = component['pic']
        self.pictype, self.typeFld = defPicType(self.pic, '')
        #   Обработчики событий
        self.hlp = component['hlp']
        self.ctrl = component['ctrl']
        self.keydown = component['keyDown']
        self.setfocus = component['setFocus']
        self.use_fdict = component['use_fdict']

        if not type(val) in (str, unicode):
            val = str(val)

        wx.TextCtrl.__init__(self, parent, id, val, pos, size, self.style, name=self.name)

        obj = icFont(font)
        self.SetFont(obj)

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        try:
            self.SetValue(str(self.dataset.getNameValue(self.field_name)))
        except:
            pass

        #   Читаем частотный словарь ввода
        self._freqDict = None
        self.SetFreqDict(self.use_fdict)

        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_TEXT, self.OnTextChanged, id=id)
        self.Bind(icEvents.EVT_TEXT_TEMPL, self.OnTempl)
        self.Bind(icEvents.EVT_AUTO_TEXT_FILL, self.OnAutoTextFill)
        self.BindICEvt()
        self.bBlockChangeEvt = False

    def SetFreqDict(self, flag):
        """
        Включаем/Выключаем частотный словарь.
        """
        self.use_fdict = flag
        if self.use_fdict and not self._freqDict:
            if self.GetDataset():
                freqDictName = 'dataclass_frequency_dict:' + self.GetDataset().name
                self._freqDict = frequencydict.icFrequencyDict(freqDictName)
            #   Если объект не привязан к классу данных, то используем
            #   стандартный словарь для текстовых полей
            else:
                freqDictName = 'textfield_frequency_dict:' + self.name
                self._freqDict = frequencydict.icFrequencyDict(freqDictName)

    def ObjDestroy(self):
        """
        Вызывается перед уничтожением.
        """
        #   Сохраняем частотный словарь ввода
        if self.use_fdict and self._freqDict:
            self._freqDict.SaveDict()

    def PostTempl(self):
        event = icEvents.icTextTemplEvent(icEvents.icEVT_TEXT_TEMPL, self.GetId())
        self.GetEventHandler().AddPendingEvent(event)

    def OnTempl(self, evt):
        """
        Преобразуем к шаблонному виду.
        """
        pt = self.GetInsertionPoint()
        text = self.GetValue()
        #   Заносим в текстовое поле так, чтобы признак изменентя текста не
        #   изменился
        self.SetValue(text, 1)
        self.SetInsertionPoint(pt)

    def OnAutoTextFill(self, evt):
        """
        Функция отрабатывает после.
        """
        if self.use_fdict and self._freqDict and self.pictype in (IC_N_STRING_FORMAT, IC_STRING_FORMAT):
            self._freqDict.AutoTextFill(self, evt.GetData())

    #   Используется для вызова справки по F1
    def OnKeyDown(self, evt):
        """
        Обработка нажатия клавиши (событие EVT_KEY_DOWN).
        Порядок действий:
        - обработка выражениия, записанного в аттрибуте keydown
        - обработка выражениия, записанного в аттрибуте hlp
        - обработка шаблонов
        - действия компонента по умолчанию на данное событие (evt.Skip())
        """
        kcod = evt.m_keyCode
        if self.GetInsertionPoint() == self.GetLastPosition():
            evt.bTabUse = 1

        #   Формируем пространство имен
        value = self.GetValue()
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['value'] = value
        # --- Запускаем внешний обработчик нажатия клавиш. Если он вернет дальнейшая
        #   обработка будет прекращена
        result = True
        if not self.keydown in [None, 'None', '']:
            ret, result = self.eval_attr('keyDown')
            if ret and result is not None:
                result = bool(result)
            else:
                result = True
        if not result:
            return
        #   Запускаем внешний обработчик нажатия клавиши F1. Контроль ввода временно
        #   отключаем посколку при выполнении выражения фокус может теряться, что будет приводить
        #   к запуску контроля ввода.
        if evt.m_keyCode == wx.WXK_F1 and self.hlp:
            self.bkillfocus = False
            ret, val = self.eval_attr('hlp')
            #   Записываем выбранное значение в поле. Признак изменения устанавливаем.
            if ret and val is not None:
                #   Если возвращаемое значение картеж, то первый элемент
                #   код выбора, второй значение выбора
                if isinstance(val, tuple):
                    if len(val) >= 4:
                        codHlp, ret_val, flds_vals, strval = val
                        ret_val = strval.rstrip()
                    else:
                        codHlp, ret_val, flds_vals = val

                    if codHlp == IC_HLP_OK or (codHlp == IC_HLP_REPL and MsgBox(self.parent,
                                                                                _('Do you really want choose value: %s?') % ret_val,
                                                                                style=wx.YES_NO | wx.ICON_QUESTION) == wx.ID_YES):
                        bChoose = True
                    else:
                        bChoose = False
                else:
                    ret_val = val
                    flds_vals = {}
                    bChoose = True

                #   Если возвращено значение для заполнения
                if bChoose:
                    #   Если возвращаемое значение картеж, то собираем из
                    #   него строку
                    if isinstance(ret_val, tuple):
                        ret_val = ''.join([str(x) for x in ret_val])
                    else:
                        ret_val = str(ret_val)

                    self.SetValue(ret_val, 1, False)
                    if 1:
                        #   Если указан словарь дополнительных значений, то
                        #   устанавливаем их
                        if flds_vals and self.dataset:
                            for fld in flds_vals.keys():
                                self.dataset.setNameValue(fld, flds_vals[fld])

            #   Фокус надо вернуть в любом случае
            self.SetFocus()
            self.bkillfocus = True
            return

        #   Перемещаемся на следующий компонент в порядке очереди
        elif evt.m_keyCode == wx.WXK_TAB:
            self.Navigate()
            return
        elif evt.m_keyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and not self.style & wx.TE_MULTILINE:
            self.Navigate()
            return

        # --- Обработка шаблона
        try:
            text = wx.TextCtrl.GetValue(self)
            templ = self.pic
            if evt.ShiftDown() and kcod == wx.WXK_INSERT:
                self.PostTempl()
            elif evt.ControlDown() or evt.ShiftDown():
                pass
            elif kcod in (wx.WXK_DELETE, wx.WXK_BACK):
                self.PostTempl()
                evt.Skip()
                return
            elif kcod not in KEYTEMPLATE:
                #   Проверяем соответствут ли вводимый символ шаблону вывода
                #   При необходимости вставляет символы форматирования
                if not PrepareTextByTempl(self, self.pictype, templ, text, kcod):
                    return
            ############################################################
            #   Генерируем сообщение на автоматическое заполнене тескста
            event = icEvents.icAutoTextFillEvent(icEvents.icEVT_AUTO_TEXT_FILL, self.GetId())
            event.SetData(self.field_name)
            self.GetEventHandler().AddPendingEvent(event)
            ############################################################
        except:
            LogLastError('Exception')

        evt.Skip()

    def IsModified(self):
        """
        Признак того, что значение изменилось.
        """
        return self.bChanged

    def ClearChangedPrz(self):
        """
        Сброс признака изменения значения.
        """
        self.bChanged = False

    def Ctrl(self, evt=None, bAsk=True, value=None):
        """
        Функция контроля введенного текста.
        """
        #   Готовим пространство имен
        if value is None:
            value = self.GetValue()
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['self'] = self
        self.evalSpace['value'] = value
        ctrl_val = IC_CTRL_OK
        #   Проводим контроль, введенного текста
        ret, ctrl_ret = self.eval_attr('ctrl')
        if ret:
            try:
                #   Если тип выражения картеж, то первый
                #   элемент код контроля, второй словарь значений
                if isinstance(ctrl_ret, tuple):
                    return ctrl_ret
                else:
                    ctrl_val = int(ctrl_ret)
            except:
                io_prnt.outErr('INVALID RETURN CODE=%s in Ctrl' % str(ctrl_ret))
                ctrl_val = IC_CTRL_OK
        return ctrl_val

    def CtrlValue(self, value=None):
        """
        Контроль значения.
        @rtype: C{bool}
        @return: Возращает признак, разрещающий или запрещающий установить значение.
        """
        codCtrl = IC_CTRL_OK
        if value is None:
            value = self.GetValue()

        if value is not None:
            #   Проводим контроль, введенного текста, если компонент работает с
            #   классом данных
            if self.IsModified() and self.dataset is not None:
                codCtrl = self.UpdateDataDB()
            #   Если компонент не связан с классом данных
            elif self.IsModified():
                codCtrl = self.Ctrl(bAsk=False, value=value)
                if isinstance(codCtrl, tuple):
                    codCtrl = codCtrl[0]
            ################################################################
            #   Добавляем слово в частотный словарь
            if codCtrl in [IC_CTRL_OK, IC_CTRL_REPL] and self._freqDict and self.pictype in (IC_N_STRING_FORMAT,
                                                                                             IC_STRING_FORMAT):
                dct = self._freqDict.AddWordInFreqDict(self.field_name, value)
            ################################################################

            #   Если контролем требуется подтверждение
            if codCtrl == IC_CTRL_REPL:
                if MsgBox(self.parent, _('Do you really want change value: %s?') % value,
                          style=wx.YES_NO | wx.NO_DEFAULT) != wx.ID_YES:
                    codCtrl = IC_CTRL_FAILED_IGNORE

            #   Если один из контролей не прошел, восстанавливаем старое значение и
            #   сообщаем пользователю
            if codCtrl in [IC_CTRL_FAILED, IC_CTRL_FAILED_IGNORE]:
                if codCtrl == IC_CTRL_FAILED:
                    MsgBox(self.parent, _('Invalid field value. value: <%s>, field: <%s>') % (value, self.name))
                    self.bChanged = True
                    self.SetValue(self._oldValue or '')
                    self.SetFocus()
                #   В случае если не удается востановить значение штатным методом
                if codCtrl == IC_CTRL_FAILED_IGNORE or not self.UpdateViewFromDB():
                    self.SetValue(self._oldValue)
                    self.SetFocus()

                return False
        return True

    def OnKillFocus(self, evt):
        """
        Обрабатывает потерю фокуса (событие EVT_KILL_FOCUS).
        Порядок действий:
        - обработка выражениия, записанного в аттрибуте losefocus
        - обработка выражениия, записанного в аттрибуте ctrl
        - действия компонента по умолчканию на данное событие (evt.Skip())
        """
        #   Если не стоит признак обработи сообщения потери фокуса, устанавливаем
        #   признак временной потери фокуса. Для того, чтобы функция OnSetFocus
        #   правильно обработала возврат фокуса.
        if not self.bkillfocus:
            self.bTimeLosefocus = True
            evt.Skip()
            return

        self.CtrlValue()
        #   Разблокируем запись для редактирования, если объект данных поддерживает блокировки
        try:
            self.dataset.Unlock()
            io_prnt.outLog('>>> TextField Unlock rec=%s' % str(self.dataset.Recno()))
        except:
            pass

    def OnTextChanged(self, evt):
        """
        Обрабатывает сообщение об изменении текста (сообщение EVT_TEXT).
        """
        if self.bBlockChangeEvt:
            return

        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.eval_attr('changed')
        self.bChanged = True
        evt.Skip()

    def GetValue(self):
        """
        Функция читает значение поля и удаляет символы форматирования
        шаблона вывода.
        @return: Возвращает значение поля без символов форматирования.
        @rtype: C{string}
        """
        value = wx.TextCtrl.GetValue(self)
        #   Убираем форматирование по шаблону
        try:
            value = delTempl(self.pic, value)
        except Exception:
            pass

        #   Если аттрибут описания 'setvalue' определен, то вычисляем значение для хранения
        if self.setvalue not in [None, 'None', '']:
            self.evalSpace['value'] = value
            ret, val = self.eval_attr('setvalue')
            if ret:
                value = val

        return value

    def Restore(self):
        """
        Устанавливает старое значение.
        """
        if self._oldValue != self.GetValue():
            self.SetValue(self._oldValue)

    def SetValue(self, value, prz=1, bFix=True):
        """
        Устанавливает значение поля, признак изменения, а также форматирует
        текст по шаблону вывода.
        @type value:
        @param value:
        @type prz:  C{int}
        @param prz: Устанавливает признак изменения поля
        """
        #   Если аттрибут описания 'getvalue' определен, то вычисляем выводимое значение поля
        if self.getvalue not in (None, 'None', ''):
            self.evalSpace['value'] = value
            ret, val = self.eval_attr('getvalue')
            if ret:
                value = val

        if value in (None, 'None'):
            value = u''

        #   Преобразуем к шаблонному представлению
        try:
            value, point = setTempl(self.pic, value, -1)
        except Exception:
            MsgLastError(self.parent, 'Exception in setTempl()')

        # if self.IsDebugMode():
        #     io_prnt.outLog(u'TEXT SET VALUE=%s' % value)

        wx.TextCtrl.SetValue(self, value)
        #   Обнуляем признак изменения при необходимости (prz == 0), поскольку SetValue
        #   возбудит EVT_TEXT и установит его в 1.
        if prz == 0:
            self.bChanged = False

        if bFix:
            #   Запоминаем старое значение
            self._oldValue = value

    def SetValueCtrl(self, value):
        """
        Проводит контроль значения и устанавливает его.
        """
        if self._oldValue != value:
            old = self._oldValue
            self.SetValue(value)
            if not self.CtrlValue():
                self.SetValue(old, 0)
            else:
                return True
        return False

    def OnSetFocus(self, evt):
        """
        Обрабатывает установку фокуса (сообщение EVT_SET_FOCUS).
        """
        if self.bTimeLosefocus:
            self.bTimeLosefocus = False
            evt.Skip()
            return
        #   Формируем пространство имен
        value = self.GetValue()
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        self.evalSpace['value'] = value
        evt.Skip()
        #   Блокируем запись для редактирования, если позволяет объект данных
        if self.dataset and not self.evalSpace['__block_lock_rec']:
            rec = self.dataset.Recno()
            result = self.dataset.Lock(rec)
            if not result and rec != self._oldLockReck:
                self.bkillfocus = False
                MsgBox(self.parent, _('Record (%d) is locked. <TextField=%s>, err=%s') % (rec, self.name, str(result)))
                self._oldLockReck = rec
                self.bkillfocus = True
            else:
                io_prnt.outLog('TEXTFIELD LOCK RECORD: %s' % str(rec))

        self.eval_attr('setFocus')
        self.bChanged = False

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
        #   Проводим контроль поля
        ret = self.Ctrl()
        values = None
        if isinstance(ret, tuple):
            codCtrl, values = ret
        else:
            codCtrl = int(ret)

        if self.dataset is not None and self.dataset.name == db_name and codCtrl in [IC_CTRL_OK, IC_CTRL_REPL]:
            #   Если контролем требуется подтверждение
            if codCtrl == IC_CTRL_REPL:
                if MsgBox(self.parent, _('Do you really want change value: %s?') % self.name,
                          style=wx.YES_NO | wx.NO_DEFAULT) != wx.ID_YES:
                    codCtrl = IC_CTRL_FAILED_IGNORE
                else:
                    codCtrl = IC_CTRL_OK
            if codCtrl == IC_CTRL_OK:
                value = self.GetValue()
                codCtrl = self.dataset.setNameValue(self.field_name, value)
            if codCtrl == IC_CTRL_OK and isinstance(values, dict):
                for fld in values:
                    val = values[fld]
                    ctrlFld = self.dataset.setNameValue(fld, val)
                    if ctrlFld == IC_CTRL_FAILED:
                        MsgBox(self.parent, _('Invalid field value. value: <%s>, field: <%s>') % (val, fld))
                        codCtrl = ctrlFld
                        break
        return codCtrl

    def UpdateViewFromDB(self, db_name=None, bFromBuff=True):
        """
        Обновляет данные в текстовом поле (если компонент привязан к
        источнику данных).
        @type db_name: C{String}
        @param db_name: Имя источника данных.
        @type bFromBuff: C{bool}
        @param bFromBuff: Признак, который указывает, что значения можно брать из
            буфера измененных значений.
        @rtype: C{bool}
        @return: Возвращает признак успешного обновления.
        """
        #   Если класс данных не задан, то считаем, что объект необходимо обновить
        if db_name is None:
            db_name = self.dataset.name
        if self.dataset is not None and self.IsShown() and self.bStatusVisible and self.dataset.name == db_name:
            val = self.dataset.getNameValue(self.field_name, bFromBuff=bFromBuff)
            self.SetValue(val)
            io_prnt.outLog('REFRESH name = %s, value = %s' % (self.name, val))
            return True
        return False

    def setValue(self, Data_):
        """
        Установить данные в виджет.
        """
        return self.SetValue(Data_)

    def getValue(self):
        """
        Получить данные из виджета.
        """
        return self.GetValue()


def test(par=0):
    """
    Тестируем класс icTextField.
    """
    from ic.components.ictestapp import TestApp
    import ic.components.icwxpanel as panel
    import ic.components.icframe as frame

    app = TestApp(par)
    frame = frame.icFrame(None, -1, {'keyDown': 'print(\'Frame ####-@@@\')'})
    win = panel.icWXPanel(frame)
    ctrl = icTextField(win, -1, {'pic': '999,999.99', 'position': (20, 20),
                                 'changed': 'print(\'CHANGED\')'})

    win.Bind(icEvents.EVT_KEY_DOWN_IC, win.BackPropKeyDownEvt, ctrl)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
