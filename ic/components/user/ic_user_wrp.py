#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пользователь системы.

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
from ic.utils import util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

# Расширенные редакторы
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportListUserEdt as pspListEdt
from ic.PropertyEditor.ExternalEditors.passwordeditor import icPasswordExternalEdt as passwordEdt
from ic.PropertyEditor.ExternalEditors.multichoiceeditor import icMultiChoiceUserEdt as multiChoiceEdt

from ic.dlg import ic_dlg
from ic.utils import coderror
from ic.utils import ic_file
from ic.utils import icprotector
from ic.engine import ic_user

import ic.engine.icUser as icuser

#   Тип компонента
ic_class_type = icDefInf._icMenuType

#   Имя класса
ic_class_name = 'icUser'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

# --- Спецификация на ресурсное описание класса ---
icuser.SPC_IC_USER['__parent__'] = icwidget.SPC_IC_SIMPLE

ic_class_spc = {'type': 'User',
                'name': 'default',
                '_uuid': None,

                'password': None,  # зашифрованный пароль пользователя
                'group': None,     # имя группы-родителя, у которой наследуются права доступа,
                'lock_time': [[], [], [], [], [], [], []],  # временной график  доступа к системе  за неделю
                'local_dir': '.defis/wrk/',  # папка локальных настроек
                'main_win': None,  # Паспорт-идентификатор главного окна
                'menubars': [],    # Список меню.
                'on_login': None,   # скрипт, выполняемый после успешного логина
                'on_logout': None,  # скрипт, выполняемый после успешного логаута
                'roles': [],        # Список ролей

                '__styles__': ic_class_styles,
                '__events__': {},
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['name', 'type',
                                                            'description', 'local_dir'],
                                   icDefInf.EDT_TEXTLIST: ['lock_time'],
                                   icDefInf.EDT_USER_PROPERTY: ['main_win', 'menubars', 'password', 'roles'],
                                   },
                '__parent__': icuser.SPC_IC_USER,
                '__attr_hlp__': {'password': u'Зашифрованный пароль пользователя',
                                 'group': u'Имя группы-родителя, у которой наследуются права доступа',
                                 'lock_time': u'Временной график  доступа к системе  за неделю',
                                 'local_dir': u'Папка локальных настроек',
                                 'main_win': u'Паспорт-идентификатор главного окна',
                                 'menubars': u'Список меню',
                                 'on_login': u'Скрипт, выполняемый после успешного логина',
                                 'on_logout': u'Скрипт, выполняемый после успешного логаута',
                                 'roles': u'Список ролей',
                                 },
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtUser'
ic_class_pic2 = '@common.imgEdtUser'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_user_wrp.icUser-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 4)

# Функции редактирования


def getRolesChoiceList():
    """
    Функция получения списка ролей, определенных в проекте.
    """
    prj_dir = ic_user.icGet('PRJ_DIR')
    role_files = ic_file.GetFilesByExt(prj_dir, '.rol')
    # Сразу отфильтровать Pkl файлы
    role_files = [role_file for role_file in role_files if '_pkl.rol' not in role_file.lower()]
    # Получить только базовые имена файлов
    role_files = [ic_file.SplitExt(ic_file.BaseName(role_file))[0] for role_file in role_files]
    return role_files


def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('main_win',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr in ('menubars',):
        ret = pspListEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr in ('password',):
        ret = passwordEdt.get_user_property_editor(value, pos, size, style, propEdt)
    elif attr in ('roles',):
        choice = getRolesChoiceList()
        ret = multiChoiceEdt.get_user_property_editor(value, pos, size, style, propEdt, title=u'РОЛИ',
                                                      edt_txt=u'Виберите роли из списка:', choice=choice)

    if ret is None:
        return value
    
    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('main_win',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('MainWindow', 'AUIMainWindow'):
                ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект не является главным окном.')
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('menubars',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            first_menubar_type = ret[0][0][0]
            for cur_psp in ret:
                if not cur_psp[0][0] in ('MenuBar', 'FlatMenuBar'):
                    ic_dlg.icWarningBox(u'ОШИБКА', u'Выбранный объект [%s] не является главным меню.' % cur_psp)
                    return coderror.IC_CTRL_FAILED_IGNORE
                # Все горизонтальные  меню должны быть одного типа
                if cur_psp[0][0] != first_menubar_type:
                    ic_dlg.icWarningBox(u'ОШИБКА', u'Ошибка типа. Обект [%s].' % cur_psp)
                    return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
    elif attr in ('password',):
        return passwordEdt.property_editor_ctrl(value, propEdt)
    elif attr in ('roles',):
        return multiChoiceEdt.property_editor_ctrl(value, propEdt)


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('main_win',):
        return pspEdt.str_to_val_user_property(text, propEdt)
    elif attr in ('menubars',):
        return pspListEdt.str_to_val_user_property(text, propEdt)
    elif attr in ('password',):
        return passwordEdt.str_to_val_user_property(text, propEdt)
    elif attr in ('roles',):
        return multiChoiceEdt.str_to_val_user_property(text, propEdt)


class icUser(icwidget.icSimple, icuser.icUser):
    """
    Пользователь системы.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    # Роли пользователя
    roles = None
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родителя
        @type id: C{int}
        @param id: Идентификатор
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
        icuser.icUser.__init__(self, ic_file.PathFile(ic_user.icGet('SYS_RES'),
                               icuser.DEFAULT_USERS_RES_FILE))
            
        icUser.roles = icprotector.readonly(self._createRoles())
        
    def _getRolesIdList(self):
        """
        Список идентификаторов ролей.
        """
        return self.getICAttr('roles')

    def _exec_on_login(self,Code_):
        """
        Выполнить при успешном логине.
        """
        return self.eval_expr(Code_, 'on_login')
        
    def _exec_on_logout(self,Code_):
        """
        Выполнить при успешном логауте.
        """
        return self.eval_expr(Code_, 'on_logout')
