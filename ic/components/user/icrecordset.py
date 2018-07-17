#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Построчный доступ к данным.
Класс пользовательского визуального компонента.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx
import ic.components.icwidget as icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
import ic.db.icsqlalchemydataset as parentModule
import ic.imglib.syscomp_img as syscomp_img
from ic.utils import coderror
from ic.dlg import ic_dlg

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icRecordset'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'Recordset',
                'name': 'default',

                'sourcePsp': None,
                'filter': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_USER_PROPERTY: ['sourcePsp'],
                                   },
                '__parent__': icwidget.SPC_IC_SIMPLE,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = syscomp_img.recordset
ic_class_pic2 = syscomp_img.recordset

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    if attr in ('sourcePsp',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('sourcePsp',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Table',):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является таблицей.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return ret


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('sourcePsp',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icRecordset(icwidget.icSimple, parentModule.icSQLAlchemyDataSet):
    """
    Описание пользовательского компонента.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='Recordset'}: Тип объекта.
        - B{name='default'}: Имя объекта.
        - B{sourcePsp=None}: Паспорт методанных таблицы (Table).
        - B{filter=None}: Паспорт фильтр.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        @param evalSpace: Контекст ресурса.
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])

        # Создаем класс таблицы
        self._table = None
        if self.sourcePsp:
            self._table = self.GetKernel().Create(self.sourcePsp)

        # Рекодсет имеет такое же ресурсное описание, что и таблица
        if self._table:
            name = self.name
            parentModule.icSQLAlchemyDataSet.__init__(self, id, self._table.resource,
                                                      logType, evalSpace, preCreateDataclass=self._table)
            # Регестрируемся в контексте
            self.GetContext()['_sources'][name] = self
            self.GetContext()['_dict_obj'][name] = self


def test(par=0):
    """
    Тестируем пользовательский класс.
    @type par: C{int}
    @param par: Тип консоли.
    """
    import ic.components.ictestapp as ictestapp
    app = ictestapp.TestApp(par)
    common.img_init()
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
