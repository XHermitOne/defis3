#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Object catalog.
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

from ic.components import icwidget
from ic.utils import util
from ic.dlg import dlgfunc
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf
import ic.db.icdbcatalog as parentModule
from ic.db import iccatalog
from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.multichoiceeditor import icMultiChoiceUserEdt as multiChoiceEdt
from ic.db import icsqlalchemy
from ic.bitmap import bmpfunc

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'Catalog'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ObjectCatalog',
                'name': 'default',

                'sourcePsp': None,
                'catalog_types': [],
                'child': [],
                'table': None,

                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_USER_PROPERTY: ['sourcePsp', 'catalog_types'],
                                   },
                '__events__': {},
                '__parent__': icwidget.SPC_IC_SIMPLE,
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('folder.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('folder-open.png')

#   Путь до файла документации
ic_class_doc = 'ic/doc/_build/html/ic.components.user.ic_catalog_wrp.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None   # ['ObjectCatalogItem', 'FolderCatalogItem']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('sourcePsp',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr in ('catalog_types',):
        lst = iccatalog.catalog_type_dct.keys()
        lst.sort()
        ret = multiChoiceEdt.get_user_property_editor(value, pos, size, style, propEdt,
                                                      title=u'Типы каталогов', edt_txt=u'Выберите тип:', choice=lst)

    if not ret:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    from ic.dlg import msgbox
    parent = propEdt.GetPropertyGrid().GetView()
    if attr in ('sourcePsp',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            if not ret[0][0] in icsqlalchemy.DB_TYPES:
                dlgfunc.openWarningBox(u'ОШИБКА', u'Объект не является БД', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return ret
    elif attr in ('catalog_types',):
        tps = str_to_val_user_property(attr, value, propEdt)
        if tps is None:
            return tps

        if type(tps) in (type([]), type((0,))):
            lst = iccatalog.catalog_type_dct.keys()
            for el in tps:
                if el not in lst:
                    dlgfunc.openWarningBox(u'ОШИБКА', u'Тип <%s> не зарегистрирован как элемент каталога' % el, parent)
                    return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        else:
            return coderror.IC_CTRL_FAILED
            
        return coderror.IC_CTRL_OK        


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('sourcePsp',):
        return pspEdt.str_to_val_user_property(text, propEdt)
    elif attr in ('catalog_types',):
        return multiChoiceEdt.str_to_val_user_property(text, propEdt)


class Catalog(icwidget.icWidget, parentModule.icDBCatalog):
    """
    Описание пользовательского компонента.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.
        
        - B{name='default'}:
        - B{child=[]}:
        - B{type='ObjectCatalog'}: Тип компонента.
        - B{sourcePsp=None}: Источник данных.
        - B{catalog_types=[]}: Типы элементов каталога.
        - B{table=None}: Имя таблицы хранения каталога.

    """
    component_spc = ic_class_spc
   
    def __init__(self, parent, id, component, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор пользовательского компонента.

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
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        self.createAttributes(component)

        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.icDBCatalog.__init__(self, src=component['sourcePsp'], table=component['table'])
        
        #   Создаем дочерние компоненты
        self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if 'child' in self.resource:
            if self.IsSizer():
                prs.icResourceParser(self.parent, self.resource['child'], self, evalSpace=self.evalSpace,
                                     bCounter=bCounter, progressDlg=progressDlg)
            elif self.child:
                prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                     bCounter=bCounter, progressDlg=progressDlg)
      

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

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    test()
