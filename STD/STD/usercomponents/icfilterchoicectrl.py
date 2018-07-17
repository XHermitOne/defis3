#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Компонент выбора фильтров.
"""


import wx
import datetime
from ic.utils import util
from ic.kernel import io_prnt
from ic.bitmap import ic_bmp
from ic.utils import ic_file
from ic.utils import ic_uuid
from ic.components import icwidget
from STD.queries import filter_choicectrl as parentModule
from ic.PropertyEditor import icDefInf

# Регистрация прав использования
from ic.kernel import icpermission
from ic.kernel.icaccesscontrol import ClassSecurityInfo

prm = icpermission.icPermission(id='filter_edit', title='ObjFilterEdit',
                                description=u'Редактирование фильтров',
                                component_type='STD')
icpermission.registerPermission(prm)


DEFAULT_FILTER_SAVE_FILENAME = ic_file.getHomePath()+'/.defis/filters.save'

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icFilterChoiceCtrl'

# Спецификация компонента
ic_class_spc = {'name': 'default',
                'type': 'FilterChoiceCtrl',

                'save_filename': None,  # Имя файла хранения фильтров
                'get_env': None,        # Метод получения окружения
                'limit': None,          # Ограничение количества строк

                'onChange': None,  # Код смены фильтра

                '__events__': {'onChange': (None, 'OnChange', False)},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['save_filename'],
                                   icDefInf.EDT_PY_SCRIPT: ['get_env', 'onChange'],
                                   icDefInf.EDT_NUMBER: ['limit'],
                                   },
                '__parent__': icwidget.SPC_IC_WIDGET,
                '__attr_hlp__': {'save_filename': u'Имя файла хранения фильтров',
                                 'get_env': u'Метод получения окружения',
                                 'onChange': u'Код смены фильтра',
                                 'limit': u'Ограничение количества строк',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('funnel--pencil.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('funnel--pencil.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = []

#   Версия компонента
__version__ = (0, 0, 1, 3)


class icFilterChoiceCtrl(icwidget.icWidget, parentModule.icFilterChoiceCtrlProto):
    """
    Компонент выбора фильтра.
    @type component_spc: C{dictionary}
    @cvar component_spc: Specification.
    """
    security = ClassSecurityInfo()

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.
        """
        self._widget_psp_uuid = None

        # Append for specification
        component = util.icSpcDefStruct(ic_class_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icFilterChoiceCtrlProto.__init__(self, parent, id)
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        for key in [x for x in component.keys() if not x.startswith('__')]:
            setattr(self, key, component[key])

        self._filter_filename = self.getICAttr('save_filename')
        self._environment = self.getICAttr('get_env')
        self._limit = self.getICAttr('limit')

        # После того как определили окружение и
        # имя файла хранения фильтров можно загрузить фильтры
        self.loadFilter()
        self.SetValue(self.getStrFilter())

    # Установка ограничения редактирования фильтров
    # Для этого в родительском классе заведены
    # функции <addFilter> и <delFilter>
    security.declareProtected('filter_edit', 'addFilter')
    security.declareProtected('filter_edit', 'delFilter')

    def getUUID(self):
        """
        Это уникальный идентификатор паспорта компонента.
        Не изменяемый в зависимости от редактирования т.к.
        паспорт не меняется.
        @return: UUID строка контрольной суммы паспорта.
        """
        if self._widget_psp_uuid:
            return self._widget_psp_uuid

        psp = self.GetPassport()
        if psp:
            psp = tuple(psp)[0]
        self._widget_psp_uuid = ic_uuid.get_passport_check_sum(psp, True)
        return self._widget_psp_uuid

    def _canEditFilter(self):
        return self.security.is_permission('filter_edit', self.GetKernel().GetAuthUser().getPermissions())

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        ВНИМАНИЕ! Здесь нельзя писать код как:
        def OnButtonClick(self):
            ok = self.doDlgChoiceFilter(self)
            if ok:
                self.eval_attr('onChange')
            self.SetFocus()
        Иначе wxPython валиться по <Segmentation fault>
        (проверено на версии wxPython 3.0.0).
        """
        self._dlg = parentModule.icFilterChoiceDlg(self)
        # Заблокировать кнопки если необходимо
        can_edit_filter = self._canEditFilter()
        self._dlg.addButton.Enable(can_edit_filter)
        self._dlg.delButton.Enable(can_edit_filter)

        self._dlg.setEnvironment(self._environment)
        self._dlg.setFilters(self._filter)
        self._dlg.setLimitLabel(self._limit, self._over_limit)

        if self._dlg.ShowModal() == wx.ID_OK:
            self._filter = self._dlg.getFilter()
            self.saveFilter()
            str_filter = self.getStrFilter()
            self.SetValue(str_filter)
            # Здесь необходимо выполнить обработчик изменения фильтра
            self.OnChange(None)
        self._dlg.Destroy()
        self._dlg = None
        self.SetFocus()

    def OnChange(self, event):
        """
        Смена фильтра.
        """
        return self.eval_attr('onChange')


def test(par=0):
    """
    Test class.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = icFilterChoiceCtrl(frame, -1, {})
    btn = wx.Button(frame, -1, 'test', pos=wx.Point(100, 50))

    def on_test_btn_click(event):
        print('RESULT:', win.getFilter())
        event.Skip()

    btn.Bind(wx.EVT_BUTTON, on_test_btn_click)

    #
    # Test code
    #
        
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
