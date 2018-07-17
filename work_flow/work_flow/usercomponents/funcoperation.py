#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского компонента ФУНКЦИОНАЛЬНАЯ ОПЕРАЦИЯ.

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
from ic.utils import coderror
from ic.kernel import io_prnt
import ic.components.icResourceParser as prs
from ic.bitmap import ic_bmp
# from work_flow.work_sys import work_img
import ic.PropertyEditor.icDefInf as icDefInf

import work_flow.doc_sys.icoperation as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icFuncOperation'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'FuncOperation',
                     'name': 'default',
                     'child': [],
                     'activate': True,
                     'init_expr': None,
                     '_uuid': None,

                     'prev_do': None,  # Скрипт, запускаемый перед выполнением операции
                     'post_do': None,  # Скрипт, запускаемый после выполнения операции
                     'prev_undo': None,  # Скрипт, запускаемый перед выполнением отмены операции
                     'post_undo': None,  # Скрипт, запускаемый после выполнения отмены операции

                     'do_func': None,  # Функция выполнения операции
                     'undo_func': None,  # Функция выполнения отмены операции

                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'operation_table'],
                                        },
                     '__events__': {},
                     '__parent__': parentModule.SPC_IC_FUNCOPERATION,
                     '__attr_hlp__': {'prev_do': u'Скрипт, запускаемый перед выполнением операции',
                                      'post_do': u'Скрипт, запускаемый после выполнения операции',
                                      'prev_undo': u'Скрипт, запускаемый перед выполнением отмены операции',
                                      'post_undo': u'Скрипт, запускаемый после выполнения отмены операции',
                                      'do_func': u'Функция выполнения операции',
                                      'undo_func': u'Функция выполнения отмены операции',
                                      },
                     })
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('gear.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('gear.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


class icFuncOperation(icwidget.icSimple, parentModule.icFuncOperationProto):
    """
    Функциональная операция.
    Методы выполнения и отмены задаются функциями пользователя.
    Атрибуты спецификации:
        do_func - Функция выполнения операции
        undo_func - Функция выполнения отмены операции

        operation_table - Имя таблицы операций движения
        prev_do - Скрипт, запускаемый перед выполнением операции
        post_do - Скрипт, запускаемый после выполнения операции
        prev_undo - Скрипт, запускаемый перед выполнением отмены операции
        post_undo - Скрипт, запускаемый после выполнения отмены операции

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        
        - B{type='defaultType'}:
        - B{name='default'}:

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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        parentModule.icFuncOperationProto.__init__(self, parent)
        
        # --- Свойства компонента ---
        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getName(self):
        """
        Имя объекта
        """
        return self.name

    #   Обработчики событий

    def is_do_func(self):
        """
        Определена функция <do_func>?
        @return: True/False.
        """
        return self.isICAttrValue('do_func')

    def do(self):
        """
        Запуск выполнения операции.
        @return: True/False.
        """
        # Если функция не определена, то и не выполнять
        if not self.is_do_func():
            return True
        else:
            io_prnt.outLog(u'Выполнение ОПЕРАЦИИ <%s>' % self.name)

        context = self.GetContext()
        context['OBJ'] = self.parent
        context['UUID'] = self.parent.getUUID()

        # Пред обработка
        if self.isICAttrValue('prev_do'):
            self.eval_attr('prev_do')

        result = self.eval_attr('do_func')

        # Пост обработка
        if self.isICAttrValue('post_do'):
            self.eval_attr('post_do')

        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            io_prnt.outWarning(u'Ошибка выполнения ОПЕРАЦИИ <%s>.' % self.name)
        return False

    def is_undo_func(self):
        """
        Определена функция <undo_func>?
        @return: True/False.
        """
        return self.isICAttrValue('undo_func')

    def undo(self):
        """
        Запуск выполнения отмены операции.
        @return: True/False.
        """
        # Если функция не определена, то и не выполнять
        if not self.is_do_func():
            return True
        else:
            io_prnt.outLog(u'Отмена ОПЕРАЦИИ <%s>' % self.name)

        context = self.GetContext()
        context['OBJ'] = self.parent
        context['UUID'] = self.parent.getUUID()

        # Пред обработка
        if self.isICAttrValue('prev_undo'):
            self.eval_attr('prev_undo')

        result = self.eval_attr('undo_func')

        # Пост обработка
        if self.isICAttrValue('post_undo'):
            self.eval_attr('post_undo')

        if result[0] == coderror.IC_EVAL_OK:
            return result[1]
        else:
            io_prnt.outWarning(u'Ошибка отмены ОПЕРАЦИИ <%s>.' % self.name)
        return False
