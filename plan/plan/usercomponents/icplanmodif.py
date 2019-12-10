#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Структурная модификация плана.

:type ic_user_name: C{string}
:var ic_user_name: Имя пользовательского класса.
:type ic_can_contain: C{list | int}
:var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других
    компонентов в данный комопнент.
:type ic_can_not_contain: C{list}
:var ic_can_not_contain: Запрещающее правило - список типов компонентов,
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой
    компонент (ic_can_contain = -1).
"""

import wx

from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.PropertyEditor import icDefInf
from ic.kernel import ickernel
from ic.utils import coderror

from ic.bitmap import bmpfunc
from ic.log import log

try:
    from STD import igetlistdlg
except ImportError:
    log.error('Ошибка импортирования <from STD import igetlistdlg>')

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icPlanModif'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'PlanModif',
                'name': 'default',
                'metaplan': [],
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   icDefInf.EDT_USER_PROPERTY: ['metaplan'],
                                   },
                '__parent__': icwidget.SPC_IC_SIMPLE}

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart-up.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart-up.png')

#   Путь до файла документации
ic_class_doc = 'doc/public/icplanmodifmanager.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


# EDITOR_FUNCS_BLOCK
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).

    :type attr: C{string}
    :param attr: Имя текущего атрибута.
    :type value: C{string}
    :param value: Текущее значение цвета в виде "wx.Colour(r,g,b)".
    :type pos: C{wx.Point}
    :param pos: Позиция окна.
    :type size: C{wx.Size}
    :param size: Размер диалогового окна.
    :type style: C{int}
    :param style: Стиль диалога.
    :type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    :param propEdt: Указатель на редактор свойств.
    """
    if attr == 'metaplan':
        tree = propEdt.GetResTree()
        item = tree.GetSelection()
        prnt = tree.GetItemParent(item)
        prnt_res = tree.GetPyData(prnt)
        mt = prnt_res['metaclass']

        if isinstance(mt, str):
            mt = str_to_val_user_property(attr, mt, propEdt, *arg, **kwarg)

        typ, className, ifs, modl, subsys = mt[0]
        resName, extName= modl.split('.')
        cls = ickernel.get_res_interface(resName, className, extName, subsys=subsys)
        result = []

        if cls:
            parent = propEdt.GetPropertyGrid().GetView()

            if value:
                chLst = str_to_val_user_property(attr, value, propEdt, *arg, **kwarg)
                if chLst is None:
                    chLst = []
            else:
                chLst = []

            lst = [key for key, obj in cls.getObject().components.items() if (obj.type == 'MetaItem' and not obj.type in chLst)]

            # from STD import igetlistdlg
            dlgcls = igetlistdlg.IGetListDlg(parent)
            dlgcls.set_base_list(lst)
            dlgcls.set_choice_list(chLst[1:])

            dlg = dlgcls.getObject()
            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                result = dlgcls.get_result()
                result = [cls.getObject().name] + result
            else:
                result = chLst

            dlg.Destroy()
        return result


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr == 'metaplan':
        #   Преобразем строку к значению
        value = str_to_val_user_property(attr, value, propEdt)
        if value is None:
            return value

        if isinstance(value, list):
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED

    return coderror.IC_CTRLKEY_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    # Превращаем текс в картеж (представление паспорта)
    try:
        value = eval(text)
    except:
        log.fatal(u'Ошибка определения значения по выражению <%s>' % text)
        return None

    return value
# END_EDITOR_FUNCS_BLOCK


class icPlanModif(icwidget.icSimple):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

        - B{child=[]}:
        - B{type='PlanModif'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType = 0, evalSpace = None,
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = filter(lambda x: x.find('__') != 0, component.keys())

        for key in lst_keys:
            setattr(self, key, component[key])

        #   Регистрация обработчиков событий
        # self.BindICEvt()

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)

    #   Обработчики событий


def test(par=0):
    """
    Тестируем пользовательский класс.

    :type par: C{int}
    :param par: Тип консоли.
    """
    from ic.imglib import common
    import ic.components.ictestapp as ictestapp

    app = ictestapp.TestApp(par)
    common.init_img()

    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    #   win = icButton(-1, win, {})
    # ctrl_1 = StateIndicator(win, -1, {'position':(100,35), 'size':(100,30)})

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
