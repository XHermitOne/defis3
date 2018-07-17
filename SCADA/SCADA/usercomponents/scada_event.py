#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент события SCADA системы.

При сканировании события выполняется блок кода experssion,
который должен возвращать True/False.
В случае expression == True выполняется блок кода onAction.

Сканирование события можно отключить переключателем enable.
"""

from ic.components import icwidget
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import ic_bmp
from ic.utils import coderror
from ic.dlg import ic_dlg

# --- Спецификация ---
SPC_IC_SCADA_EVENT = {'enable': True,
                      'expression': None,
                      'onAction': None,

                      'scan_class': None,

                      '__parent__': icwidget.SPC_IC_SIMPLE,

                      '__attr_hlp__': {'scan_class': u'Класс сканирования',
                                       'enable': u'Вкл./Выкл. проверки события',
                                       'expression': u'Выражение проверки появления события',
                                       'onAction': u'Блок кода обработки события',
                                       },
                      }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSCADAEvent'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'SCADAEvent',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {'onAction': (None, 'OnAction', False)},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid'],
                                   icDefInf.EDT_CHECK_BOX: ['enable'],
                                   icDefInf.EDT_USER_PROPERTY: ['scan_class'],
                                   icDefInf.EDT_PY_SCRIPT: ['expression'],
                                   },
                '__parent__': SPC_IC_SCADA_EVENT,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('flag.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('flag.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('scan_class',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

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
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является КЛАССОМ СКАНИРОВАНИЯ.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('scan_class',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icSCADAEvent(icwidget.icSimple):
    """
    Компонент события SCADA системы.

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]

        for key in lst_keys:
            setattr(self, key, component[key])

        # Объект класса сканирования данных SCADA.
        self._scan_class = None

    def OnAction(self, event=None):
        """
        Выполнения блока кода - обработчика события.
        """
        context = self.GetContext()
        context['SCADA_ENGINE'] = self.parent
        return self.eval_attr('onAction')

    def doExpression(self):
        """
        Выполнить и проверить выполнение условия возникновения события.
        @return: True/False.
        """
        context = self.GetContext()
        context['SCADA_ENGINE'] = self.parent

        if self.isICAttrValue('expression'):
            result = self.eval_attr('expression')
            if result[0] == coderror.IC_EVAL_OK:
                return result[1]
            else:
                log.warning(u'Ошибка обработки условия возникновения события ОБЪЕКТА <%s>. Результат: %s' % (self.name,
                                                                                                             result))
        else:
            log.warning(u'Не определено выражение проверки условия возникновения события ОБЪЕКТА <%s>.' % self.name)
        return False

    def Enable(self, enable=True):
        """
        Вкл./ Выкл. обработки события.
        @param enable: Признак Вкл./ Выкл. обработки события.
        """
        self.enable = enable

    def do(self):
        """
        Проверить и обработать событие.
        @return: True/False.
        """
        if not self.enable:
            # Обработка события выключена.
            return False

        exp_result = self.doExpression()
        if exp_result:
            # Да событие возникло
            # Обрабатываем
            self.OnAction()
            return True
        return False

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
