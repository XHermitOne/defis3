#!/usr/bin/env python
# -*- coding: utf-8 -*-

#<< Типовой шаблон пользовательского компонента >>

# -----------------------------------------------------------------------------
# Name:         $module_name: icuserbase.py $
# Purpose:      $purpose: Назначение $
#
# Author:       <$author: .$>
#
# Created:      $created: 2003/10/06 $
# RCS-ID:       $Id: icuserbase.py $
# Copyright:    $copyright: (c) Company$
# Licence:      $licence:<your licence>$
# -----------------------------------------------------------------------------
"""
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

import $import: <ic.components.parentModule> $ as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = '$class_name:<icUserBase>$'

#   Описание стилей компонента
ic_class_styles = $styles: <стили компонента>$

#   Спецификация на ресурсное описание класса
ic_class_spc = $spc: <{'type':'UserBase',
                       'name':'default',
                       'doc_file':None}> $
                    
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '$icon: <>$'
ic_class_pic2 = '$icon: <>$'

#   Путь до файла документации
ic_class_doc = $doc: <файл с документацией на класс>$
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = $contain: <[]> $

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = $not_contain:<None>$

#   Версия компонента
__version__ = (0, 0, 0, 1)


class $class_name:<icUserBase>$(icwidget.icWidget, parentModule.$parent_class:<pclass>$):
    """
    Описание пользовательского компонента.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        $spc_description: $
    """
    component_spc = ic_class_spc
   
    def __init__(self, parent, id, component, logType = 0, evalSpace = None,
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
        parentModule.$parent_class:<pclass>$.__init__(self, $init_arg: <self.parent, id, ... >$)
        #img = common.imgEdtImage
        #parentModule.GenBitmapTextButton.__init__(self, parent, id, img, self.label, self.position, self.size, style = self.style, name = self.name)
        
        #   Регистрация обработчиков событий
        $bind_events: <Описание обработчиков сообщений>$
        self.BindICEvt()
        #   Создаем дочерние компоненты
        if component.has_key('child'):
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.IsSizer() and self.child:
            prs.icResourceParser(self.parent, self.child, self, evalSpace = self.evalSpace,
                                 bCounter = bCounter, progressDlg = progressDlg)
        elif self.child:
            prs.icResourceParser(self, self.child, None, evalSpace = self.evalSpace,
                                 bCounter = bCounter, progressDlg = progressDlg)
      
    #   Обработчики событий
    $events_function: <Функции-обработчики сообщений>$


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
