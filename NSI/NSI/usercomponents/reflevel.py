#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Уровень иерархии объекта-ссылка/справочника.
Класс пользовательского компонента УРОВНЯ ИЕРАРХИИ ОБЪЕКТА-ССЫЛКА/СПРАВОЧНИКА.
"""

import copy
import wx
from ic.components import icwidget
from ic.utils import util
import ic.components.icResourceParser as prs
from ic.bitmap import bmpfunc
from ic.PropertyEditor import icDefInf

import NSI.nsi_sys.ref_level as parentModule
from . import refrequisite

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icRefLevel'

#   Описание стилей компонента
ic_class_styles = None

# ВНИМАНИЕ! При создании уровня автоматически создаются системные реквизиты.
# Имена реквизитов изменять нельзя!

# Спецификация реквизита кода объекта
ic_code_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_code_requisite_spc['name'] = 'cod'
ic_code_requisite_spc['description'] = u'Код'
ic_code_requisite_spc['label'] = u'Код'

# Спецификация реквизита наименования объекта
ic_name_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_name_requisite_spc['name'] = 'name'
ic_name_requisite_spc['description'] = u'Наименование'
ic_name_requisite_spc['label'] = u'Наименование'

# Спецификация реквизита вкл/выкл объекта
ic_activate_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_activate_requisite_spc['name'] = 'activate'
ic_activate_requisite_spc['type_val'] = 'Boolean'
ic_activate_requisite_spc['description'] = u'Вкл/Выкл'
ic_activate_requisite_spc['label'] = u'Вкл/Выкл'
ic_activate_requisite_spc['default'] = u'@True'

# Спецификация реквизита даты даты последнего редактирования
ic_dt_edit_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_dt_edit_requisite_spc['name'] = 'dt_edit'
ic_dt_edit_requisite_spc['type_val'] = 'DateTime'
ic_dt_edit_requisite_spc['description'] = u'Дата-время последнего редактирования'
ic_dt_edit_requisite_spc['label'] = u'Дата-время последнего редактирования'
ic_dt_edit_requisite_spc['default'] = u'@datetime.datetime.now()'

# Спецификация реквизита имени компьютера
ic_comp_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_comp_requisite_spc['name'] = 'computer'
ic_comp_requisite_spc['description'] = u'Компьютер'
ic_comp_requisite_spc['label'] = u'Компьютер'
ic_comp_requisite_spc['default'] = u'@ic.utils.system.getComputerName()'

# Спецификация реквизита имени пользователя
ic_user_requisite_spc = copy.deepcopy(refrequisite.ic_class_spc)
ic_user_requisite_spc['name'] = 'username'
ic_user_requisite_spc['description'] = u'Пользователь'
ic_user_requisite_spc['label'] = u'Пользователь'
ic_user_requisite_spc['default'] = u'@ic.engine.glob_functions.getCurUserName()'

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'RefLevel',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'description': '',  # Описание
                '__brief_attrs__': ['name', 'description'],
                'child': [ic_code_requisite_spc,
                          ic_name_requisite_spc,
                          ic_activate_requisite_spc,
                          ic_dt_edit_requisite_spc,
                          ic_comp_requisite_spc,
                          ic_user_requisite_spc],

                'len': 2,  # Длина кода уровня
                'pic': None,  # Картинка-образ
                'pic2': None,  # Картинка-образ

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_NUMBER: ['len'],
                                   icDefInf.EDT_IMG: ['pic', 'pic2'],
                                   },
                '__parent__': parentModule.SPC_IC_REFLEVEL,
                '__attr_hlp__': {'len': u'Длина кода уровня',
                                 'pic': u'Картинка-образ',
                                 'pic2': u'Дополнительная картинка-образ',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('book-open-bookmark.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('book-open-bookmark.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['RefRequisite', 'RefNSIRequisite']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 1, 1)


class icRefLevel(icwidget.icSimple, parentModule.icRefLevelProto):
    """
    Класс пользовательского компонента УРОВНЯ ИЕРАРХИИ ОБЪЕКТА-ССЫЛКА/СПРАВОЧНИКА.

    :type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
    """
    component_spc = ic_class_spc

    def __init__(self, parent, id, component, logType=0, evalSpace=None,
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
        parentModule.icRefLevelProto.__init__(self, parent, parent.getLevelCount())

        self.len = self.getICAttr('len')

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

    def getStorage(self):
        """
        Хранилище.
        """
        return self.getSprav().getStorage()

    def getDBPsp(self):
        """
        Паспорт БД.
        """
        return self.getSprav().getDBPsp()

    def getChildrenRequisites(self):
        """
        Все реквизиты объекта в виде списка.
        """
        return self.GetComponentsList()

    def getCodLen(self):
        """
        Длина кода уровня.
        """
        return self.len

    def getPic(self):
        """
        Картинка.
        """
        pic = self.getICAttr('pic')
        if pic:
            return pic
        return bmpfunc.createLibraryBitmap('folder.png')

    def getPic2(self):
        """
        Картинка.
        """
        pic = self.getICAttr('pic2')
        if pic:
            return pic
        return bmpfunc.createLibraryBitmap('folder-open.png')

    #   Обработчики событий
