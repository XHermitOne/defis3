#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Контрол управления деревом запросов к OLAP кубам OLAP сервера.
"""

import wx

from ic.log import log
from ic.bitmap import bmpfunc
from ic.utils import util
from ic.utils import uuidfunc
from ic.dlg import dlgfunc
from ic.utils import coderror

from ic.components import icwidget
from ic.PropertyEditor import icDefInf
from ic.components import icResourceParser as prs

from ..olap.ctrl import olap_query_tree_ctrl

# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

# Регистрация прав использования
from ic.kernel import icpermission
from ic.kernel.icaccesscontrol import ClassSecurityInfo

prm = icpermission.icPermission(id='tree_olap_request_edit', title='TreeObjOLAPRequestEdit',
                                description=u'Редактирование запросов к OLAPT серверу',
                                component_type='analitic')
icpermission.registerPermission(prm)

#   Описание стилей компонента
ic_class_styles = {'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
                   'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
                   'TR_NO_LINES': wx.TR_NO_LINES,
                   'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
                   'TR_SINGLE': wx.TR_SINGLE,
                   'TR_MULTIPLE': wx.TR_MULTIPLE,
                   # 'TR_EXTENDED': wx.TR_EXTENDED,
                   'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
                   'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
                   'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
                   'TR_ROW_LINES': wx.TR_ROW_LINES,
                   'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
                   'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
                   'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
                   # 'TR_MAC_BUTTONS': wx.TR_MAC_BUTTONS
                   }

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icOLAPQueryTreeCtrl'

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'OLAPQueryTreeCtrl',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],

                'save_filename': None,  # Имя файла хранения запросов
                'onChange': None,  # Код смены запроса
                'olap_server': None,  # OLAP сервер

                '__styles__': ic_class_styles,
                '__events__': {'onChange': (None, 'OnChange', False),
                               },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 'save_filename'],
                                   icDefInf.EDT_PY_SCRIPT: ['onChange'],
                                   icDefInf.EDT_USER_PROPERTY: ['olap_server']
                                   },
                '__parent__': olap_query_tree_ctrl.SPC_IC_OLAPQUERYTREECTRL,
                '__lists__': {},
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('wxtreectrl.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('wxtreectrl.png')

#   Путь до файла документации
ic_class_doc = 'analitic/doc/_build/html/analitic.usercomponents.icolapquerytreectrl.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('olap_server',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    # Проверка нажатия кнопки <Отмена>
    if ret in (None, 'None'):
        # log.debug(u'Нажата <отмена>')
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('olap_server',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            # parent = propEdt
            if not ret[0][0] in ('CubesOLAPServer',):
                dlgfunc.openWarningBox(u'ОШИБКА',
                                       u'Выбранный объект не является OLAP СЕРВЕРОМ.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('olap_server',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icOLAPQueryTreeCtrl(icwidget.icWidget,
                          olap_query_tree_ctrl.icOLAPQueryTreeCtrlProto):
    """
    Контрол управления деревом запросов к OLAP кубам OLAP сервера.
    """
    component_spc = ic_class_spc
    security = ClassSecurityInfo()

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
        self._widget_psp_uuid = None

        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        olap_query_tree_ctrl.icOLAPQueryTreeCtrlProto.__init__(self, parent=parent, id=id)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        self._save_filename = self.getSaveFilename()

        # После того как определили окружение и
        # имя файла хранения фильтров можно загрузить фильтры
        self.loadRequests()

    # Установка ограничения редактирования фильтров
    # Для этого в родительском классе заведены
    # функции <addFilterItem>, <delFilterItem>, <editFilterItem>, <editIndicatorItem>
    security.declareProtected('tree_olap_request_edit', 'addRequestItem')
    security.declareProtected('tree_olap_request_edit', 'delRequestItem')
    security.declareProtected('tree_olap_request_edit', 'editRequestItem')
    security.declareProtected('tree_olap_request_edit', 'editRequestIndicatorItem')

    def _canEditOLAPRequest(self):
        return self.security.is_permission('tree_olap_request_edit', self.GetKernel().GetAuthUser().getPermissions())

    def getUUID(self):
        """
        Это уникальный идентификатор паспорта компонента.
        Не изменяемый в зависимости от редактирования т.к.
        паспорт не меняется.

        :return: UUID строка контрольной суммы паспорта.
        """
        if self._widget_psp_uuid:
            return self._widget_psp_uuid

        psp = self.GetPassport()
        if psp:
            psp = tuple(psp)[0]
        self._widget_psp_uuid = uuidfunc.get_passport_check_sum(psp, True)
        return self._widget_psp_uuid

    def getSaveFilename(self):
        """
        Имя файла хранения содержимого дерева запросов.
        """
        return self.getICAttr('save_filename')

    def getOLAPServerPsp(self):
        """
        Паспорт объекта OLAP сервера.
        """
        return self.getICAttr('olap_server')

    def getOLAPServer(self):
        """
        Объект OLAP сервера.
        """
        if self._OLAP_server is None:
            olap_srv_psp = self.getOLAPServerPsp()
            kernel = self.GetKernel()
            self._OLAP_server = kernel.Create(olap_srv_psp)

        return self._OLAP_server

    def OnChange(self, event):
        """
        Смена фильтра.
        """
        return self.eval_attr('onChange')
