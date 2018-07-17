#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент логического тега SCADA системы.
"""

from ic.components import icwidget
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

from ic.utils import util
from ic.PropertyEditor import icDefInf

from ic.log import log

from ic.bitmap import ic_bmp
from ic.utils import coderror
from ic.dlg import ic_dlg

from . import scada_tag

# --- Спецификация ---
SPC_IC_BOOL_SCADA_TAG = {'units': '',

                         '__parent__': scada_tag.SPC_IC_SCADA_TAG,

                         '__attr_hlp__': {'units': u'Единицы измерения',
                                          },
                         }


#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icBoolSCADATag'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'BoolSCADATag',
                'name': 'default',
                'child': [],
                'activate': True,
                '_uuid': None,

                '__events__': {},
                '__lists__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', '_uuid', 'units'],
                                   icDefInf.EDT_USER_PROPERTY: ['node', 'scan_class'],
                                   icDefInf.EDT_PY_SCRIPT: ['address'],
                                   },
                '__parent__': SPC_IC_BOOL_SCADA_TAG,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('tag_yellow.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('tag_yellow.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 4)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('node', 'scan_class'):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('node',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('OPCNode', 'MemoryNode'):
                ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                                u'Выбранный объект не является узлом/контроллером SCADA.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        elif ret in (None, ''):
            return coderror.IC_CTRL_OK
    elif attr in ('scan_class',):
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
    if attr in ('node', 'scan_class'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icBoolSCADATag(scada_tag.icSCADATagProto, icwidget.icSimple):
    """
    Компонент логического тега SCADA системы.

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

        scada_tag.icSCADATagProto.__init__(self)

    def getNodePsp(self):
        """
        Паспорт узла-источника данных SCADA.
        @return: Паспорт или None в случае ошибки.
        """
        return self.getICAttr('node')

    def getNode(self, node_psp=None):
        """
        Объект узла-источника данных SCADA.
        @param node_psp: Паспорт узла-источника данных SCADA.
            Если не определено, то задается функцией self.getNodePsp.
        @return: Объект узла-источника данных SCADA или
            None в случае ошибки.
        """
        if node_psp is None and self._node is not None:
            # Если объект таблицы уже определен, то просто вернуть его
            return self._node

        psp = self.getNodePsp() if node_psp is None else node_psp
        if psp is not None:
            # Получить зарегистрированный объект. Если его нет, то он создасться
            self._node = self.GetKernel().getObjectByPsp(psp)
        else:
            log.warning(u'Не определен паспрот при получении объекта УЗЛА-ИСТОЧНИКА ДАННЫХ SCADA')
            self._node = None
        return self._node

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

    def getAddress(self):
        """
        Адрес в источнике данных/контроллере/узле SCADA.
        """
        address = self.getICAttr('address')
        if not address:
            log.warning(u'Не определен адрес тега <%s>' % self.name)
        return address

    def normValueInto(self, value):
        """
        Преобразование типа значения для установки внутреннего значения.
        @param value: Текущее значение тега.
        @return: Преобразованное значение.
        """
        if type(value) in (str, unicode):
            return value in ('True', '1', )
        elif isinstance(value, bool):
            return value
        return bool(value)

    def normValueOut(self, value):
        """
        Преобразование типа значения для получения из внутреннего значения.
        @param value: Текущее значение тега.
        @return: Преобразованное значение.
        """
        return value
