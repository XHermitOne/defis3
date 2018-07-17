#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ссылка/связь с объектом.
Компонент имеет следующие атрибуты:
    object - Паспорт объекта-источника сборки
    res_replace - Словарь изменения ресурса объекта-источника
        Ресурс объекта источника изменяется методом словаря update.
        В качестве ключей этого словаря м.б. имена атрибутов непосредственно самого
        связываемого объекта...
        Например:
        {
            'size': (10, 20),
            ...
        }
        ...так и имена дочерних объектов.
        В этом случае в качестве значения
        должен быть словарь изменяемых атрибутов дочернего объекта.
        Например:
        {
            'object1': {'size': (20, 30),
                        'pos': (100, 200),
                        ...},
            ...
        }

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
from . import icwidget
import ic.utils.util as util
from ic.log import log
from ic.utils import coderror
from ic.utils import resource
import ic.PropertyEditor.icDefInf as icDefInf
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

parentModule = icwidget

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icObjectLink'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'ObjectLink',
                'name': 'default',
                'object': None,         # Паспорт объекта-источника
                'res_replace': None,    # Словарь изменения ресурса объекта-источника
                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_USER_PROPERTY: ['object'],
                                   icDefInf.EDT_DICT: ['res_replace'],
                                   },
                '__parent__': icwidget.SPC_IC_BASE,
                }


#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtObjLink'
ic_class_pic2 = '@common.imgEdtObjLink'

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('object',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('object',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            # В качестве объекта-источника может выступать любой объект
            return coderror.IC_CTRL_OK
        return coderror.IC_CTRL_FAILED


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('object',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icObjectLink(parentModule.icBase):
    """
    Описание пользовательского компонента.
    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc
   
    def __init__(self, parent, id, component, logType=0, evalSpace=None, *arg, **kwarg):
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
        """
        component = util.icSpcDefStruct(self.component_spc, component)

        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if not x.startswith('__')]
        for key in lst_keys:
            setattr(self, key, component[key])
        
        parentModule.icBase.__init__(self, parent, id, component, logType, evalSpace)
        # !!! Компонент создается в своем контексте

        # Получаем ресурс-оригинал
        res = self.GetKernel().getResByPsp(self.object)
        # Подготавливаем словарь замен
        dct = self.get_replacement_dct(component)
        # Производим замену
        res = self.do_replacement(res, dct)
                
        # Создаем связанный объект
        self._object = self.GetKernel().createObjBySpc(parent, res, context=self.context)

        # Регистрируемся в контексте
        self.context['_dict_obj'][self.name] = self
        self.context['_list_obj'].append(self)

    def do_replacement(self, res, replacement_dct=None):
        """
        Произвести замены в ресурсе.
        @param res: Ресурс объекта.
        @param replacement_dct: Словарь замен.
        @return: Ресурс с произведенными заменами
        """
        if not res:
            log.warning(u'Не определен ресурс')
            return res

        if replacement_dct is None:
            # Если словарь замен не определен, то замены производить не надо
            return res

        # Если определен словарь замен используем его
        for attr_name, value in replacement_dct.items():
            # ВНИМАНИЕ! Типы объектов подменять нельзя
            if attr_name != 'type' and not attr_name.startswith('_'):
                if attr_name in res:
                    res[attr_name] = value
                else:
                    # Если нет такого атрибута, значит это замена атрибутов дочернего объекта
                    if isinstance(value, dict):
                        res = resource.update_child_resource(attr_name, res, value)
                    else:
                        log.warning(u'Не поддерживаемый тип %s замены ресурса дочернего объекта <%s>' % (type(value),
                                                                                                         attr_name))
        return res

    def get_replacement_dct(self, res=None):
        """
        Получить словарь замен ресурса перед сборкой связанного объекта.
        @param res: Ресурс.
        @return: Словарь замен.
        """
        if res is None:
            res = self.GetResource()

        replacement_dct = dict()
        # ВНИМАНИЕ! Самое главное надо подменить имя ссылаемого объекта
        replacement_dct['name'] = self.name

        for key, val in res.items():
            if key in ('border', 'flag', 'position', 'proportion', 'size', 'span'):
                replacement_dct[key] = val
        # Словарь замен может быть расширен
        # при помощи атрибута res_replace
        if self.isICAttrValue('res_replace'):
            res_replace = self.getICAttr('res_replace')
            if isinstance(res_replace, dict):
                replacement_dct.update(res_replace)
            else:
                log.warning(u'Не поддерживаемый тип %s замены значений ресурса при сборке объекта <%s> ' % (type(res_replace),
                                                                                                            self.getName()))
        return replacement_dct

    def get_replace_object(self):
        """
        Возвращает указатель на объект, который встраивается в создаваемый компонент
        парсером.
        """
        return self._object


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
