#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс Главное окно системы. Технология AUI.

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

import wx,wx.aui
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

from ic.engine import icAUImainwin

from ic.utils import coderror
from ic.dlg import ic_dlg
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

# --- Константы и переменные ---
# Флаги управлния AUI панелями
ICAUIFlags = {'AUI_MGR_ALLOW_FLOATING': wx.aui.AUI_MGR_ALLOW_FLOATING,
              'AUI_MGR_ALLOW_ACTIVE_PANE': wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE,
              'AUI_MGR_TRANSPARENT_DRAG': wx.aui.AUI_MGR_TRANSPARENT_DRAG,
              'AUI_MGR_TRANSPARENT_HINT': wx.aui.AUI_MGR_TRANSPARENT_HINT,
              'AUI_MGR_VENETIAN_BLINDS_HINT': wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT,
              'AUI_MGR_RECTANGLE_HINT': wx.aui.AUI_MGR_RECTANGLE_HINT,
              'AUI_MGR_HINT_FADE': wx.aui.AUI_MGR_HINT_FADE,
              'AUI_MGR_NO_VENETIAN_BLINDS_FADE': wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE,
              }

# --- Спецификация компонента ---
#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icAUIMainWindow'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
ic_class_spc = {'type': 'AUIMainWindow',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                'child': [],
                '_uuid': None,

                'is_main_notebook': True,  # Присутствует в главном окне нотебук?
                'is_menubar': True,    # Присутствует в главном окне меню?
                'is_statusbar': True,  # Присутствует в главном окне статусная строка?
                'content': None,       # Заполнить фрейм главного окна объектом ...

                # Флаги AUI менеджера
                'allow_floating': True,      # Разрешать плавающие панели
                'allow_active_pane': False,  # Есть активная панель
                'transparent_drag': False,
                'transparent_hint': True,       # Прозрачная подсказка прикрепления
                'venetian_blinds_hint': False,  # Полупрозрачная подсказка прикрепления
                'rectangle_hint': False,        # Прямоугольная подсказка прикрепления
                'hint_fade': True,
                'no_venetian_blinds_fade': True,  # Отключить эффект заполнения подсказки
    
                # Градиент заголовков AUI панелей
                'pane_gradient': 'Horizontal',

                'on_close_page': None,    # Обработчик закрытия страницы
                'on_closed_page': None,    # Обработчик закрытой страницы

                '__events__': {},
                '__lists__': {'pane_gradient': [name for name in icAUImainwin.AUI_PANE_GRADIENTS.keys() if name is not None],
                              },
                '__styles__': ic_class_styles,
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'title_label',
                                                            'icon', 'splash'],
                                   icDefInf.EDT_CHECK_BOX: ['title_readonly', 'sys_menu',
                                                            'min_button', 'max_button', 'area_split',
                                                            'allow_floating',
                                                            'allow_active_pane',
                                                            'transparent_drag',
                                                            'transparent_hint',
                                                            'venetian_blinds_hint',
                                                            'rectangle_hint',
                                                            'hint_fade',
                                                            'no_venetian_blinds_fade',
                                                            'is_main_notebook', 'is_menubar', 'is_statusbar',
                                                            ],
                                   icDefInf.EDT_NUMBER: ['border'],
                                   icDefInf.EDT_POINT: ['pos'],
                                   icDefInf.EDT_SIZE: ['size'],
                                   icDefInf.EDT_COMBINE: ['style'],
                                   icDefInf.EDT_COLOR: ['title_color', 'phone_color'],
                                   icDefInf.EDT_CHOICE: ['pane_gradient'],
                                   icDefInf.EDT_RO_TEXTFIELD: ['res_module', '_uuid', 'obj_module'],
                                   icDefInf.EDT_USER_PROPERTY: ['content'],
                                   },
                '__parent__': icAUImainwin.SPC_IC_AUIMAINWIN,
                '__attr_hlp__': {'is_main_notebook': u'Присутствует в главном окне нотебук?',
                                 'is_menubar': u'Присутствует в главном окне меню?',
                                 'is_statusbar': u'Присутствует в главном окне статусная строка?',
                                 'content': u'Заполнить фрейм главного окна объектом ...',
                                 'allow_floating': u'Разрешать плавающие панели',
                                 'allow_active_pane': u'Есть активная панель',
                                 'transparent_drag': u'',
                                 'transparent_hint': u'Прозрачная подсказка прикрепления',
                                 'venetian_blinds_hint': u'Полупрозрачная подсказка прикрепления',
                                 'rectangle_hint': u'Прямоугольная подсказка прикрепления',
                                 'hint_fade': u'',
                                 'no_venetian_blinds_fade': u'Отключить эффект заполнения подсказки',
                                 'pane_gradient': u'Градиент заголовков AUI панелей',
                                 'on_close_page': u'Обработчик закрытия страницы',
                                 'on_closed_page': u'Обработчик закрытой страницы',
                                 },
                }
                    
#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMainWin'
ic_class_pic2 = '@common.imgEdtMainWin'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_auimainwin_wrp.icAUIMainWindow-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['AUIPane']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 1, 1)

# Функции редактирования


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('content',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('content',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt.GetPropertyGrid().GetView()
            if not ret[0][0] in ('Panel', 'ScrolledWindow', 'Notebook', 'SplitterWindow'):
                ic_dlg.icMsgBox(u'ОШИБКА РЕДАКТИРОВАНИЯ', u'Выбранный объект не является главным окном.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('content',):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icAUIMainWindow(icwidget.icSimple, icAUImainwin.icAUIMainWinPrototype):
    """
    Главное окно приложения. Технология AUI.
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
        icwidget.icSimple.__init__(self,parent, id, component, logType, evalSpace)
        icAUImainwin.icAUIMainWinPrototype.__init__(self, component)

        #   Создаем дочерние компоненты
        if 'child' in component:
            for child in component['child']:
                if child['activate'] not in ('0', 'False', 'false'):
                    pane = self.childCreator(child)
                    self.aui_manager.addPane(pane)
                    if not pane.visible:
                        self.aui_manager.GetPane(pane.name).Show(False)  
            
        self.aui_manager.Update()
        
        # Дополнительный функционал инициализации
        if component.get('init_expr', None):
            self.eval_attr('init_expr')        

    def _childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], 
                                    None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def childCreator(self, Child_):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icBuildObject(self, Child_,
                                 evalSpace=self.evalSpace,
                                 bIndicator=False)

    def onClosePage(self, event):
        """
        Обработчик закрытия страницы главного нотебука.
        """
        event.Skip()

        #   Формируем пространство имен
        self.evalSpace['evt'] = event
        self.evalSpace['event'] = event

        self.eval_attr('on_close_page')

    def onClosedPage(self, event):
        """
        Обработчик закрытой страницы главного нотебука.
        """
        event.Skip()

        #   Формируем пространство имен
        self.evalSpace['evt'] = event
        self.evalSpace['event'] = event

        self.eval_attr('on_closed_page')
