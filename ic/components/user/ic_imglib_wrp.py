#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Библиотека образов.
Класс пользовательского компонента БИБЛИОТЕКА ОБРАЗОВ.

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

from ic.bitmap import icimagelibrary as parentModule

_ = wx.GetTranslation

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icImageLibrary'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'ImageLibrary',
                'name': 'default',
                'activate': True,
                'child': [],
                'init_expr': None,
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description'],
                                   },
                '__lists__': {},
                '__parent__': icwidget.SPC_IC_SIMPLE,
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtImgLib'
ic_class_pic2 = '@common.imgEdtImgLib'

#   Путь до файла документации
ic_class_doc = None
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['Bitmap']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)

DEFAULT_IMAGE_SIZE = (16, 16)


class icImageLibrary(icwidget.icSimple, parentModule.icImageLibraryPrototype):
    """
    Библиотека образов.
    """

    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
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
        parentModule.icImageLibraryPrototype.__init__(self)
        self.childCreator(bCounter, progressDlg)
        
        for idx, el in enumerate(self.resource['child']):
            img = self.GetChildByName(el['name']).getBitmap()
            if not img:
                # Если образ не определен, то все равно надо добавить
                # картинку чтобы индексы не сбивались
                img = common.imgEdtImage
            self.Add(img)

    def Add(self, img):
        """
        Абстрактный метод. Переопределяется в icImageList.
        Заменяется на метод wx.ImageList.
        """
        pass

    def GetBitmap(self, idx):
        """
        Абстрактный метод. Переопределяется в icImageList.
        Заменяется на метод wx.ImageList.
        """
        return None

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.child, None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
