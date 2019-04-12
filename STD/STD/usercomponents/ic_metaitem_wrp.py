#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Метакомпонент.
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
    
@type SPC_IC_METAITEM: C{dict}
@var SPC_IC_METAITEM: Спецификация на ресурсное описание метакласса. Описание ключей:

    - B{name = 'default'): Имя.
    - B{metatype = None): Указание имени метатипа, из которого порожден метаобъект, Если None, то сам является метатипом.
    - B{description = None): Описание.
    - B{spc = {}): Значение спецификации метакомпонента.
    - B{const_spc = {}): Постоянные значения спецификации метакомпонента.
    - B{view_form = None): Форма чтения/просмотра.
    - B{edit_form = None): Форма редактирования/записи.
    - B{report = None): Форма печати/отчет.
    - B{storage_type = 'DirStorage'): Тип хранилища метакомпонента.
    - B{container = True): Признак контейнера.
    - B{pic = None): Образ метакомпонента.
    - B{pic2 = None): Дополнительный образ метакомпонента.
    - B{doc = None): Файл документации компонента.
    - B{can_contain = None): Разрешающее правило вкличения.
    - B{can_not_contain = None): Запрещающее/bc правило - список типов компонентов,
        #которые не могут содержаться в данном компоненте. Запрещающее правило
        #начинает работать если разрешающее правило разрешает добавлять любой
        #компонент (can_contain = -1).
    - B{init = None): Блок кода, выполняемый при создании метаобъекта
    - B{del = None): Блок кода, выполняемый при удалении метаобъекта
"""

import wx

from ic.components import icwidget
import ic.components.icResourceParser as prs
from ic.imglib import common
from ic.PropertyEditor import icDefInf

from STD.metastruct import metaitem

# --- Спецификация ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMetaItem'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaItem',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                'child': [],
                '_uuid': None,

                '__styles__': ic_class_styles,
                '__events__': {'on_init': (None, 'onInit', False),
                               'on_del': (None, 'onDel', False),
                               'on_edit': (None, 'onEdit', False),
                               'on_view': (None, 'onView', False),},
                '__lists__': {'storage_type': [metaitem.FILE_NODE_STORAGE_TYPE,
                                               metaitem.FILE_STORAGE_TYPE,
                                               metaitem.DIR_STORAGE_TYPE],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', 'doc'],
                                   icDefInf.EDT_CHECK_BOX: ['container'],
                                   icDefInf.EDT_CHOICE: ['storage_type'],
                                   icDefInf.EDT_TEXTDICT: ['spc', 'const_spc'],
                                   },
                '__parent__': metaitem.SPC_IC_METAITEM,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMetaItem'
ic_class_pic2 = '@common.imgEdtMetaItem'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_metaitem_wrp.icMetaItem-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['MetaConst', 'MetaAttr']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icMetaItem(icwidget.icSimple, metaitem.icMetaItemEngine):
    """
    Метакомпонент.
    """
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace, bGenUUID=False)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        metaitem.icMetaItemEngine.__init__(self, parent, component)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def onInit(self, event=None):
        """
        Выполнения блока кода - обработчика события.
        Блок кода, выполняемый при создании метаобъекта.
        """
        context = self.GetContext()
        context['self'] = self
        context['evt'] = event
        context['event'] = event
        return self.eval_attr('on_init')

    def onDel(self, event=None):
        """
        Выполнения блока кода - обработчика события.
        Блок кода, выполняемый при удалении метаобъекта.
        """
        context = self.GetContext()
        context['self'] = self
        context['evt'] = event
        context['event'] = event
        return self.eval_attr('on_del')

    def onEdit(self, event=None):
        """
        Выполнения блока кода - обработчика события.
        Блок кода, выполняемый при редактировании метаобъекта.
        """
        context = self.GetContext()
        context['self'] = self
        context['evt'] = event
        context['event'] = event
        return self.eval_attr('on_edit')

    def onView(self, event=None):
        """
        Выполнения блока кода - обработчика события.
        Блок кода, выполняемый при просмотре метаобъекта.
        """
        context = self.GetContext()
        context['self'] = self
        context['evt'] = event
        context['event'] = event
        return self.eval_attr('on_edit')
