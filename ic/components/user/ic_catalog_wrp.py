#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Object catalog.
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
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf
import ic.imglib.newstyle_img as newstyle_img
import ic.db.icdbcatalog as parentModule
from ic.db import iccatalog
from ic.utils import coderror
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.multichoiceeditor import icMultiChoiceUserEdt as multiChoiceEdt
from ic.db import icsqlalchemy
_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'Catalog'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT':0}

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
ic_class_pic = '@ic.imglib.newstyle_img.folder'
ic_class_pic2 = '@ic.imglib.newstyle_img.folderOpen'

#   Путь до файла документации
ic_class_doc = 'doc/public/catalog.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None   # ['ObjectCatalogItem', 'FolderCatalogItem']

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
    elif attr in ('catalog_types',):
        lst = iccatalog.catalog_type_dct.keys()
        lst.sort()
        ret = multiChoiceEdt.get_user_property_editor(value, pos, size, style, propEdt,
            title=_('Catalog types'), edt_txt=_('Select types:'),choice=lst)        

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
                msgbox.MsgBox(parent, _('Object is not DB source (*.src).'))
                return coderror.IC_CTRL_FAILED_IGNORE
            return ret
    elif attr in ('catalog_types',):
        tps = str_to_val_user_property(attr, value, propEdt)
        if tps is None:
            return tps

        if type(tps) in (type([]), type((0,))):
            lst = iccatalog.catalog_type_dct.keys()
            for el in tps:
                if not el in lst:
                    msgbox.MsgBox(parent, _('Type <%s> is not registered catalog item.' % el))
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
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
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
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icWidget.__init__(self, parent, id, component, logType, evalSpace)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        
        for key in lst_keys:
            setattr(self, key, component[key])
        
        #   !!! Конструктор наследуемого класса !!!
        #   Необходимо вставить реальные параметры конструкора.
        #   На этапе генерации их не всегда можно определить.
        parentModule.icDBCatalog.__init__(self, src=component['sourcePsp'], table=component['table'])
        
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                                 bCounter=bCounter, progressDlg=progressDlg)
      
    #   Обработчики событий


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
