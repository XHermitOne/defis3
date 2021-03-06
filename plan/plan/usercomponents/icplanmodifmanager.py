#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс пользовательского визуального компонента.

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
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import ic.utils.coderror as coderror

from ic.bitmap import bmpfunc
from ic.log import log

from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icPlanModifManager'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ModPlanManager',
                'name': 'default',
                'metaclass': None,
                'child': [],

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type'],
                                   icDefInf.EDT_USER_PROPERTY: ['metaclass'],
                                   },
                '__parent__': icwidget.SPC_IC_SIMPLE}
                    

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('chart_organisation.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('chart_organisation.png')

#   Путь до файла документации
ic_class_doc = 'plan/doc/_build/html/plan.usercomponents.icplanmodifmanager.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['PlanModif']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


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
    :type metaclass: C{tuple}
    :param metaclass: Паспорт объекта, описывающего метадерево базового плана.
    :type propEdt: C{ic.components.user.objects.PropNotebookEdt}
    :param propEdt: Указатель на редактор свойств.
    """
    if attr == 'metaclass':
        return pspEdt.get_user_property_editor(value, pos, size, style, propEdt)


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr == 'metaclass':
        return pspEdt.property_editor_ctrl(value, propEdt)

    return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    # Превращаем текс в картеж (представление паспорта)
    if attr == 'metaclass':
        return pspEdt.str_to_val_user_property(text, propEdt)

    return None


class icPlanModifManager(icwidget.icSimple):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{child=[]}:
        - B{type='ModPlanManager'}: Тип.
        - B{name='default'}: Имя.
        - B{metaclass=None}: Ссылка (паспорт) на метокласса, описывающего элементы базового плана.
            Пример: ((None, IMetaplan, None, metadata/planProdaj.py, 'STIS'), <uuid>)

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
        self.createAttributes(component)

        #   Создаем дочерние компоненты
        self.createChildren(bCounter=bCounter, progressDlg=progressDlg)

    def getCanContainLst(self, modifId, metatype):
        """
        Возвращает список типов компонентов, которые могут содержатся в
        определенном компоненте - разрешающее правило. Список генерится по
        объекту описания модификации плана.
        """
        lst = self.getModifLst(modifId)
        if lst and metatype in lst:
            i = lst.index(metatype)
            if i + 1 < len(lst):
                return [lst[i+1]]
        return list()

    def getDescrDct(self):
        """
        Возвращает словарь описаний модификаций. Ключ - идентификатор модификации,
            значение - описание модификации.
        """
        dct = {}
        for obj in self.components.values():
            dct[obj.name] = obj.description
        
        return dct
        
    def getModifLst(self, modifId):
        """
        Возвращает структуру описывающую модификацию плана.
        """
        for obj in self.components.values():
            if obj.name == modifId:
                return obj.metaplan


def test(par=0):
    """
    Тестируем пользовательский класс.
    
    :type par: C{int}
    :param par: Тип консоли.
    """
    
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
