#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Уровень иерархии справочников.
Класс пользовательского компонента УРОВНЯ ИЕРАРХИИ СПРАВОЧНИКОВ.

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
from ic.bitmap import ic_bmp
import ic.PropertyEditor.icDefInf as icDefInf

import NSI.nsi_sys.icspravlevel as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icSpravLevel'

#   Описание стилей компонента
ic_class_styles = None

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = dict({'type': 'SpravLevel',
                     'name': 'default',
                     'child': [],
                     'activate': True,
                     'init_expr': None,
                     '_uuid': None,
                     '__brief_attrs__': ['name', 'description'],
    
                     'hlp_form': None,   # Форма для выбора кода на текушем уровне
                     'edit_form': None,  # Форма для редактирования записей справоника текушего уровня
                     'access': '',       # Права доступа
                     'len': 2,    # Длина кода уровня
                     'cod_type': 'string',  # Тип значения субкода (число/строка)
                     'description': '',   # Описание
                     'notice': {},  # Словарь описания семантики дополнительных полей данных справочника
                     'pic': None,   # Картинка-образ
                     'pic2': None,  # Картинка-образ
                     'ref_sprav': None,     # Справочник, на который ссылается текущий уровень
                     'ref_level': 0,
                     'add_ctrl': None,  # Функция дополнительного контроля на добавление записи в справочник
                     'update_ctrl': None,   # Функция дополнительного контроля на обновление/изменение записи в справочник
                     'del_ctrl': None,  # Функция дополнительного контроля на удаление записи из справочника

                     '__events__': {},
                     '__lists__': {'cod_type': ['number', 'string']},
                     '__attr_types__': {0: ['name', 'type'],
                                        icDefInf.EDT_TEXTFIELD: ['description', 'access', 'hlp_form', 'edit_form'],
                                        icDefInf.EDT_CHOICE: ['cod_type'],
                                        icDefInf.EDT_NUMBER: ['len', 'ref_level'],
                                        icDefInf.EDT_TEXTDICT: ['notice'],
                                        },
                     '__parent__': parentModule.SPC_IC_SPRAVLEVEL,
                     '__attr_hlp__': {'hlp_form': u'Форма для выбора кода на текушем уровне',
                                      'edit_form': u'Форма для редактирования записей справоника текушего уровня',
                                      'access': u'Права доступа',
                                      'len': u'Длина кода уровня',
                                      'cod_type': u'Тип значения субкода (число/строка)',
                                      'notice': u'Словарь описания семантики дополнительных полей данных справочника',
                                      'pic': u'Картинка-образ',
                                      'pic2': u'Картинка-образ',
                                      'ref_sprav': u'Справочник, на который ссылается текущий уровень',
                                      'add_ctrl': u'Функция дополнительного контроля на добавление записи в справочник',
                                      'update_ctrl': u'Функция дополнительного контроля на обновление/изменение записи в справочник',
                                      'del_ctrl': u'Функция дополнительного контроля на удаление записи из справочника',
                                      },
                     })

ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = ic_bmp.createLibraryBitmap('book-open-bookmark.png')
ic_class_pic2 = ic_bmp.createLibraryBitmap('book-open-bookmark.png')

#   Путь до файла документации
ic_class_doc = ''
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 3)


class icSpravLevel(icwidget.icSimple, parentModule.icSpravLevelPrototype):
    """
    Описание пользовательского компонента.

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
        parentModule.icSpravLevelPrototype.__init__(self, parent, parent.getLevelCount())
        self.ref_sprav = self.getICAttr('ref_sprav')
        self.ref_level = component['ref_level']
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

    def getCodLen(self):
        """
        Длина кода уровня.
        """
        return self.len

    def getEditFormName(self):
        """
        Форма для редактирования данных текущего уровня.
        """
        return self.getICAttr('edit_form')

    def getHelpFormName(self):
        """
        Форма для выбора данных текущего уровня.
        """
        return self.getICAttr('hlp_form')

    def getEditFormPsp(self):
        """
        Форма для редактирования данных текущего уровня.
        """
        return None

    def getHelpFormPsp(self):
        """
        Форма для выбора данных текущего уровня.
        """
        return None

    def getNoticeDict(self):
        """
        Словарь замен имен полей-реквизитов справочника.
        """
        return self.getICAttr('notice')

    def getPic(self):
        """
        Картинка.
        """
        pic = self.getICAttr('pic')
        if pic:
            return pic
        return ic_bmp.createLibraryBitmap('folder.png')

    def getPic2(self):
        """
        Картинка.
        """
        pic = self.getICAttr('pic2')
        if pic:
            return pic
        return ic_bmp.createLibraryBitmap('folder-open.png')

    def getRefSprav(self):
        """
        Получить ссылку на справочник.
        """
        return self.ref_sprav

    def getRefLevel(self):
        """
        Получить ссылку на номер уровня связанного справочника, на который ссылается уровень.
        """
        return self.ref_level

    def getAddCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на добавление записи в справочник.
        """
        self.evalSpace.update(kwargs)
        self.evalSpace['args'] = args
        
        result = self.eval_attr('add_ctrl')
        if result[0]:
            return result[1]
        return None
    
    def getUpdateCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на обновление/изменение записи в справочник.
        """
        self.evalSpace.update(kwargs)
        self.evalSpace['args'] = args
        
        result = self.eval_attr('update_ctrl')
        if result[0]:
            return result[1]
        return None
    
    def getDelCtrl(self, *args, **kwargs):
        """
        Функция дополнительного контроля на удаление записи из справочника.
        """
        self.evalSpace.update(kwargs)
        self.evalSpace['args'] = args
        
        result = self.eval_attr('del_ctrl')
        if result[0]:
            return result[1]
        return None
    
    #   Обработчики событий
