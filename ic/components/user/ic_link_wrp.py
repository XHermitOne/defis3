#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Связь с другой таблицей.
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
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.kernel import icobject

from ic.db import icsqlalchemy

from ic.dlg import ic_dlg
from ic.utils import coderror

from ic.kernel import io_prnt

from ic.engine import ic_user

#   Тип компонента
ic_class_type = icDefInf._icDatasetType

#   Имя класса
ic_class_name = 'icLink'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': icsqlalchemy.LINK_TYPE,
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                
                'description': '',
                'lnk_type': 'phisical',     # Тип связи Жесткая связь/логическая связь
                'table': None,
                'del_cascade': False,
                'field': None,

                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'lnk_type': ['phisical', 'logical'],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type', 
                                                            'description'],
                                   icDefInf.EDT_CHOICE: ['lnk_type'],
                                   icDefInf.EDT_CHECK_BOX: ['del_cascade'],
                                   icDefInf.EDT_USER_PROPERTY: ['table'],
                                   },
                '__parent__': icsqlalchemy.SPC_IC_LNK,
                '__attr_hlp__': {'lnk_type': u'Тип связи Жесткая связь/логическая связь',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtDBLink'
ic_class_pic2 = '@common.imgEdtDBLink'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_link_wrp.icLink-class.html'
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
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('table',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('table',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in (icsqlalchemy.TABLE_TYPE,):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является таблицей.')
                return coderror.IC_CTRL_FAILED_IGNORE
            try:
                kernel = ic_user.getKernel()
                res = propEdt.GetResEditor().GetResource()
                my_db_psp = res['source']
                if my_db_psp:
                    my_db_psp = icobject.icObjectPassport(*my_db_psp)

                res = kernel.getResByPsp(ret)
                link_db_psp = res['source']
                if link_db_psp:
                    link_db_psp = icobject.icObjectPassport(*link_db_psp)

                if my_db_psp != link_db_psp:
                    ic_dlg.icWarningBox(u'ОШИБКА', u'ВНИМАНИЕ! Связанные таблицы должны находиться в одной БД.')
                    return coderror.IC_CTRL_FAILED_IGNORE
            except:
                io_prnt.outErr(u'Ошибка контроля вводимого значения %s : %s' % (attr, value))
            return ret


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('table',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icLink(icwidget.icSimple):
    pass
