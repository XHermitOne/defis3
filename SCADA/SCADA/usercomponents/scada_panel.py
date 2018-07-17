#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Панель оперативных данных SCADA системы.
"""

import wx
from ic.components import icwxpanel
# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt

from ic.PropertyEditor import icDefInf

from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.utils import util

from . import scada_form_manager

# --- Спецификация ---
SPC_IC_SCADA_PANEL = {'engines': list(),
                      'scan_class': None,
                      'auto_run': False,

                      '__parent__': icwxpanel.SPC_IC_PANEL,

                      '__attr_hlp__': {'engines': u'Список движков SCADA системы',
                                       'scan_class': u'Класс сканирования',
                                       'auto_run': u'Признак автозапуска и автоостанова всех движков при создании/закрытии окна',
                                       },
                      }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSCADAPanel'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SCADAPanel',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_CHECK_BOX: ['auto_run'],
                                   icDefInf.EDT_USER_PROPERTY: ['engines', 'scan_class'],
                                   },
                '__parent__': SPC_IC_SCADA_PANEL,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('control_panel.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('control_panel.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = -1

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (0, 0, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('scan_class',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr in ('engines',):
        ret = pspListEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('scan_class',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('ScanClass',):
                ic_dlg.icWarningBox(u'ОШИБКА',
                                    u'Выбранный объект не является КЛАССОМ СКАНИРОВАНИЯ.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('engines',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            first_menubar_type = ret[0][0][0]
            for cur_psp in ret:
                if not cur_psp[0][0] in ('SCADAEngine',):
                    ic_dlg.icWarningBox(u'ОШИБКА',
                                        u'Выбранный объект [%s] не является ДВИЖКОМ SCADA СИСТЕМЫ.' % cur_psp)
                    return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('scan_class',):
        return pspEdt.str_to_val_user_property(text, propEdt)
    elif attr in ('engines',):
        return pspListEdt.str_to_val_user_property(text, propEdt)


class icSCADAPanel(icwxpanel.icWXPanel, scada_form_manager.icSCADAFormManager):
    """
    Панель оперативных данных SCADA системы.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """

    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
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
        component = util.icSpcDefStruct(self.component_spc, component, True)
        icwxpanel.icWXPanel.__init__(self, parent, id, component, logType, evalSpace)
        scada_form_manager.icSCADAFormManager.__init__(self)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        self.Bind(wx.EVT_CLOSE, self.onClose)

        # Объект класса сканирования данных SCADA.
        self._scan_class = None

        self.init()

    def getScanClassPsp(self):
        """
        Паспорт класса сканирования данных SCADA.
        @return: Паспорт или None в случае ошибки.
        """
        return self.getICAttr('scan_class')

    def getScanClass(self, scan_class_psp=None):
        """
        Объект класса сканирования данных SCADA.
        @param scan_class_psp: Паспорт класса сканирования данных SCADA.
            Если не определено, то задается функцией self.getScanClassPsp.
        @return: Объект класса сканирования данных SCADA или
            None в случае ошибки.
        """
        if scan_class_psp is None and self._scan_class is not None:
            # Если объект таблицы уже определен, то просто вернуть его
            return self._scan_class

        psp = self.getScanClassPsp() if scan_class_psp is None else scan_class_psp
        if psp is not None:
            # Получить зарегистрированный объект. Если его нет, то он создасться
            self._scan_class = self.GetKernel().getObjectByPsp(psp)
        else:
            log.warning(u'Не определен паспрот при получении объекта КЛАССА СКАНИРОВАНИЯ')
            self._scan_class = None
        return self._scan_class

    def initScanTick(self):
        """
        Инициализация периода сканирования по классу сканирования.
        @return: Период сканирования или None в случае ошибки.
        """
        scan_class = self.getScanClass()
        if scan_class:
            self.scan_tick = scan_class.getTick()
        return self.scan_tick

    def createEngines(self):
        """
        Создать список движков.
        @return: Список движков.
        """
        kernel = self.GetKernel()
        self.scada_engines = [kernel.getObjectByPsp(engine_psp) for engine_psp in self.engines]
        return self.scada_engines

    def init(self):
        """
        Полная инициализация объекта.
        @return: True/False.
        """
        # Создать список движков
        self.createEngines()

        self.initScanTick()

        # Запустить таймер
        self.startTimer()

        #
        if self.auto_run:
            self.startEngines()

        # self.updateValues()

    def onClose(self, event):
        """
        Обработчик закрытия панели.
        """
        if self.on_close:
            self.eval_attr('onClose')

        # Останавливать движки в любом случае
        self.stopEngines()

        event.Skip()
