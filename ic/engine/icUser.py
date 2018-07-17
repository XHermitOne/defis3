#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль пользователя.

@type SPC_IC_USER: C{dictionary}
@var SPC_IC_USER: Спецификация на ресурсное описание компонента icAccessManager.
Описание ключей SPC_IC_USER:
    - B{name = 'password'}: Зашифрованный пароль пользователя.
    - B{name = 'group'}: Имя группы-родителя, у которой наследуются права доступа.
    - B{name = 'lock_time'}: Временной график  доступа к системе за неделю.
    - B{name = 'local_dir'}: Папка локальных настроек.
    - B{name = 'on_login'}: Cкрипт, выполняемый после успешного логина.
    - B{name = 'on_logout'}: Cкрипт, выполняемый после успешного логаута.
    - B{name = 'main_win'}: Паспорт-идентификатор главного окна пользователя.
    - B{name = 'menubars'}: Список меню.
    - B{name = 'roles'}: Список имен ролей.
"""

# --- Подключение библиотек ---
import copy
import re
import os.path
import os
import wx

from ic.utils import ic_mode

from ic.utils import util

from ic.log import log
from ic.dlg import ic_dlg
from ic.utils import ic_file
from ic.utils import ic_exec
from ic.utils import ic_util
from ic.utils import user_journal

from ic.kernel import icexceptions
from ic.kernel import icbaseuser
from ic.utils import coderror
from . import ic_user

_ = wx.GetTranslation

# --- Константы подсистемы ---
# Осуществлять проверку от копирования?
COPY_DEFENDER_ON = False

# Файл ресурсов описаний ограничений доступа для всех пользователей системы
# ЗАКРИПТОВАННЫЙ!!!
DEFAULT_USERS_RES_FILE = 'users.acc'

# Имя системного администратора по умолчанию
SYS_ADMIN_NAME = 'admin'

# Имя папки локальных настроек по умолчанию
LOCALDIR_DEFAULT = '.defis/wrk/'

# Типы ресурсов системы
ACC_NONE = -1       # Тип ресурса не определен
ACC_DATA = 0        # Тип данных
ACC_MENUITEM = 200  # Тип пункта главного меню.
ACC_TOOLITEM = 201  # Тип инструмента на панели инструментов.

# Символы кодировки ограничений
FULL_ACCESS_PERMIT = '--vudawr'     # Полный доступ

ACCESS_LOCK = '-'   # Блокировка ресурса системы

ACCESS_USE = 'u'        # использование
ACCESS_VIEW = 'v'       # отображение
ACCESS_READ = 'r'       # чтение
ACCESS_EDIT = 'w'       # редактирование
ACCESS_APPEND = 'a'     # добавление
ACCESS_DELETE = 'd'     # удаление

# Поля(Индексы) в таблице описаний прав доступа
ACC_IDX_RESTYPE = 0
ACC_IDX_TEMPLAT = 1
ACC_IDX_DESCRIPT = 2
ACC_IDX_PERMIT = 2  # После удаления описательной части из таблицы

# --- Спецификации ---
# Специяфикация группы пользователей
SPC_IC_USERGROUP = {'type': 'UserGroup',
                    'group': None,  # имя группы-родителя, у которого наследуются права доступа,
                    'lock_time': None,  # временной график  доступа к системе  за неделю
                    'menubars': [],     # Список меню.
                    'on_login': None,   # скрипт, выполняемый после успешного логина
                    'on_logout': None,  # скрипт, выполняемый после успешного логаута
                    }

# Спецификация пользователя системы
SPC_IC_USER = {'type': 'User',
               'password': None,  # зашифрованный пароль пользователя
               'group': None,  # имя группы-родителя, у которого наследуются права доступа,
               'lock_time': [[], [], [], [], [], [], []],  # временной график  доступа к системе  за неделю
               'local_dir': '.defis/wrk/',  # папка локальных настроек
               'main_win': None,   # Паспорт-идентификатор главного окна
               'menubars': [],     # Список меню.
               'on_login': None,   # скрипт, выполняемый после успешного логина
               'on_logout': None,  # скрипт, выполняемый после успешного логаута
               'roles': [],    # Список ролей
               }


__version__ = (0, 0, 1, 2)


# --- ФУНКЦИИ СИСТЕМЫ ОГРАНИЧЕНИЯ ДОСТУПА ---
def getUserRequisit(UserName_):
    """
    Получить реквизиты пользователя.
    @param UserName_: Имя пользователя.
        Если UserName_ не определено, тогда возвращается
        описание прав доступа текущего пользователя.
        Если UserName определен, тогда возвращается
        описание прав доступа указанного пользователя.
    @return: Функция возвращает реквизиты текущего пользователя.
    """
    if ic_mode.isRuntimeMode():
        # Режим исполнения
        app = ic_user.icGetRunner()
        return app.getUser().GetUserRequisit(UserName_)
    else:
        # Режим редактирования
        return copy.deepcopy(SPC_IC_USER)


def getAuthent(ResName_, ResType_, ShowMsg_=True):
    """
    Функция возвращает права доступа к ресурсу для текущего пользователя в виде 8-символьной строки.
    @param ResName_: имя ресурса.
    @param ResType_: тип ресурса.
    @param ShowMsg_: флаг, описывающий разрешение на отображение
        сообщения о заблокированном ресурсе для данного пользователя.
        Параметр необязателен. По умолчанию сообщение показывается.
    @return: Возвращает права доступа к ресурсу для текущего пользователя
        в виде 8-символьной строки. Например '----dawr'
    """
    if ic_mode.isRuntimeMode():
        # Режим исполнения
        app = ic_user.icGetRunner()
        return app.getUser().GetAuthent(ResName_, ResType_, ShowMsg_)
    else:
        # Режим редактирования
        return FULL_ACCESS_PERMIT


def canAuthent(Permit_, ResName_, ResType_, ShowMsg_=True):
    """
    Функция определяет ограничения на запрашиваемый ресурс.
    @param Permit_: символ или группа символов,
        определяющий право доступа на действие.
        'u' - использование (ACCESS_USE).
        'v' - отображение  (ACCESS_VIEW).
        'r' - чтение (ACCESS_READ).
        'w' - редактирование (ACCESS_EDIT).
        'a' - добавление (ACCESS_APPEND).
        'd' - удаление (ACCESS_DELETE).
    @param ResName_: имя ресурса.
    @param ResType_: тип ресурса.
    @param ShowMsg_: флаг, описывающий разрешение на отображения
        сообщения о заблокированном ресурсе для данного пользователя.
        Параметр необязателен. По умолчанию сообщение показывается.
    @return: Возвращает True, если ресурс не ограничен,
        запрашиваемыми правами доступа, False - ресурс ограничен.
    """
    # ВНИМАНИЕ!!! Проверка осуществляется только в режиме выполнения
    if ic_mode.isRuntimeMode():
        app = ic_user.icGetRunner()
        if app:
            return app.getUser().CanAuthent(Permit_, ResName_, ResType_, ShowMsg_)
    return True


class icUserPrototype(icbaseuser.icRootUser):
    """
    Класс пользователя системы.
    """
    
    def __init__(self, ResFileName_=DEFAULT_USERS_RES_FILE, LoginManager_=None):
        """
        Конструктор класса.
        """
        # Базовый пользователь, получающий доступ к ядру
        # и управляющий объектами системы
        icbaseuser.icRootUser.__init__(self)

        # --- Атрибуты класса ---
        # Ресурсный файл
        self._ResFile = ResFileName_
        # Имя текущего пользователя
        self._UserName = ''
        # Реквизиты текущего пользователя:
        self._UserRequisit = {}
        # Режим работы с БД.
        self._DBMode = ic_mode.DB_SHARE
        
        self._login_manager = LoginManager_

    def setLoginManager(self, LoginManager_):
        """
        Установить менеджер входа в систему.
        """
        self._login_manager = LoginManager_
        
    def getUserResFileName(self):
        """
        Имя ресурсного файла пользователей.
        """
        return self._ResFile
    
    def getUsersResource(self):
        """
        Полностью структура ресурса файла пользователей.
        """
        return util.readAndEvalFile(self.getUserResFileName())
            
    def _getRolesIdList(self):
        """
        Список идентификаторов ролей.
        """
        if self._UserRequisit and 'roles' in self._UserRequisit:
            return self._UserRequisit['roles']
        return []
        
    def _createRoles(self, RolesId_=None):
        """
        Создание списка ролей по идентификаторам.
        @return: Список объектов ролей.
        """
        if RolesId_ is None:
            RolesId_ = self._getRolesIdList()
            
        role_obj_list = []
        for role_id in RolesId_:
            new_role_psp = (('Role', role_id, None, role_id+'.rol', None),)
            new_role_obj = ic_user.getKernel().createResObjByPsp(new_role_psp, context=self.GetContext())
            role_obj_list.append(new_role_obj)
        return tuple(role_obj_list)
        
    def _getRoles(self):
        """
        Список ролей.
        """
        if self.__class__.roles is None:
            return []
        return list(self.__class__.roles)

    def getRolesIdList(self):
        """
        Список идентификаторов ролей.
        """
        return self._getRolesIdList()

    def isRole(self, role_name):
        """
        Обладает пользователь ролью?
        @param role_name: Наименование роли.
            Например: administrators.
        @return: True/False
        """
        user_roles_names = self.getRolesIdList()
        return role_name in user_roles_names

    def getRolesObjList(self):
        """
        Список объектов ролей.
        """
        return self._getRoles()

    def Load(self, UserName_, ResFile_=None):
        """
        Загузить все реквизиты из ресурсного файла.
        @param UserName_: Имя пользователя в ресурсном файле.
        @param ResFile_: Имя ресурсного файла.
        """
        try:
            if ResFile_ is not None:
                self._ResFile = ResFile_
            access_dict = util.readAndEvalFile(self._ResFile, bRefresh=True)

            # Запомнить имя ...
            self._UserName = UserName_

            if UserName_ in access_dict:
                # Собрать данные из словаря по одному пользователю.
                self._UserRequisit = self.CutUserRequisit(access_dict, UserName_, self._UserRequisit)
                if self._UserRequisit != {}:
                    pass
                else:
                    self._UserName = ''
            else:
                self._UserName = ''
                self._UserRequisit = {}

            return self._UserRequisit
        except:
            log.fatal(u'Ошибка загрузки реквизитов пользователя.')
            self._UserName = ''
            self._UserRequisit = {}

    def _cutGroupRequisite(self, AccessDict_, GroupName_, Requisit_=None):
        """
        Собрать данные по группам.
        @param AccessDict_: Словарь описаний ограничений доступа
            пользователей системы.
        @param GroupName_: Имя группы пользователей в ресурсном файле.
        @param Requisit_: Текущий реквизит пользователя.
            При первом вызове функции д.б. {}
        """
        if Requisit_ is None:
            Requisit_ = {}
        group_data = AccessDict_[GroupName_]
        
        # временной график  доступа к системе  за неделю
        if (('lock_time' not in Requisit_) or (not Requisit_['lock_time'])) and \
           'lock_time' in group_data:
            Requisit_['lock_time'] = group_data['lock_time']
        # Список меню
        if (('menubars' not in Requisit_) or (not Requisit_['menubars'])) and \
           'menubars' in group_data:
            Requisit_['menubars'] = group_data['menubars']
        # скрипт, выполняемый после успешного логина
        if (('on_login' not in Requisit_) or (not Requisit_['on_login'])) and \
           'on_login' in group_data:
            Requisit_['on_login'] = group_data['on_login']
        # скрипт, выполняемый после успешного логаута
        if (('on_logout' not in Requisit_) or (not Requisit_['on_logout'])) and \
           'on_logout' in group_data:
            Requisit_['on_logout'] = group_data['on_logout']
        
        if 'group' in group_data and group_data['group']:
            Requisit_ = self._cutGroupRequisit(AccessDict_, group_data['group'], Requisit_)
            
        return Requisit_
        
    def CutUserRequisit(self, AccessDict_, UserName_, Requisit_=None):
        """
        Собрать данные из словаря по одному пользователю.
        @param AccessDict_: Словарь описаний ограничений доступа
            пользователей системы.
        @param UserName_: Имя пользователя в ресурсном файле.
        @param Requisit_: Текущий реквизит пользователя.
            При первом вызове функции д.б. {}
        """
        try:
            if Requisit_ is None:
                Requisit_ = {}

            user_data = AccessDict_[UserName_]
            user_data = copy.deepcopy(ic_util.SpcDefStruct(SPC_IC_USER, user_data))

            if 'group' in user_data and user_data['group']:
                requisites = self._cutGroupRequisite(AccessDict_, user_data['group'])
                # временной график  доступа к системе  за неделю
                if (('lock_time' not in user_data) or (not user_data['lock_time'])) and \
                   'lock_time' in requisites:
                    Requisit_['lock_time'] = requisites['lock_time']
                # Список меню
                if (('menubars' not in user_data) or (not user_data['menubars'])) and \
                   'menubars' in requisites:
                    Requisit_['menubars'] = requisites['menubars']
                # скрипт, выполняемый после успешного логина
                if (('on_login' not in user_data) or (not user_data['on_login'])) and \
                   'on_login' in requisites:
                    Requisit_['on_login'] = requisites['on_login']
                # скрипт, выполняемый после успешного логаута
                if (('on_logout' not in user_data) or (not user_data['on_logout'])) and \
                   'on_logout' in requisites:
                    Requisit_['on_logout'] = requisites['on_logout']
                
            if Requisit_:
                user_data.update(Requisit_)

            return user_data
        except:
            # Ошибка сбора данных доступа для регистрируемого пользователя')
            log.fatal(u'User Requisite Error')
            return None
        
    def LoadUser(self, UserName_, ResFile_=DEFAULT_USERS_RES_FILE):
        """
        Загузить данные из ресурсного файла по одному пользователю.
        @param UserName_: Имя пользователя в ресурсном файле.
        @param ResFile_: Имя ресурсного файла.
        """
        try:
            access_dict = util.readAndEvalFile(ResFile_)
            return access_dict[UserName_]
        except:
            log.fatal(u'Load User Requisite Error')

    def _checkLoginUser(self, UserName_):
        """
        Проверка зарегистрированного пользователя.
        @param UserName_: Имя пользователя.
        """
        if not ic_mode.isRuntimeMode():
            # Если режим конфигурирования, то обязательно
            # проверять уникальность регистрации
            # чтобы проблем с блокировками не было
            if self._login_manager:
                return self._login_manager.isRegUserName(UserName_)
        return False
      
    def _password_compare(self, UserPassword_, LoginPassword_, LoginPasswordMD5_):
        """
        Функция сравнения паролей.
        @param UserPassword_: Пароль определенный для пользователя в ресурсе.
        @param LoginPassword_: Введенный пароль при логине.
        @param LoginPasswordMD5_: Контрольная сумма md5 введенного пароля при логине.
        @return: Возвращает True если пароли совпадают и False если не совпадают.
        """
        if UserPassword_ is None or UserPassword_ == '':
            # Пароль для пользователя не определен
            # Можно в систему входить без пароля
            return True
        elif len(UserPassword_) < 32:
            # Пароль для пользователя определен просто строкой
            return UserPassword_ == LoginPassword_
        elif len(UserPassword_) == 32:
            # Пароль для пользователя в ресурсе задан как контрольная сумма md5
            return UserPassword_ == LoginPasswordMD5_
        return False
        
    def login_ok(self, UserName_=SYS_ADMIN_NAME, Password_=None, PasswordMD5_=None,
                 DBMode_=ic_mode.DB_SHARE, RuntimeMode_=True):
        """
        Залогинить пользователя.
        @param UserName_: Имя пользователя.
        @param Password_: Если задан пароль по умолчанию,
            то происходит автологин.
        @param PasswordMD5_: Контрольная сумма логина.
        @param DBMode_: Режим использования БД.
        @param RuntimeMode_: Признак режима исполнения.
        @return: Возвращает True, если вход в систему успешный.
        """
        try:
            sys_enter = False  # Флаг входа в систему

            if self._checkLoginUser(UserName_):
                if UserName_:
                    err_txt = 'User %s registered in system yet' % self._UserName
                    log.warning(err_txt)
                    raise icexceptions.LoginErrorException((coderror.IC_LOGIN_ERROR, err_txt))
        
            if UserName_:
                self.Load(UserName_)
                if self._UserName and \
                   self._password_compare(self._UserRequisit['password'], Password_, PasswordMD5_):
                    # Проверка входа в систему в нерабочее время
                    if self.CanWorkTime():
                        if self.CanDBMode(DBMode_):
                            sys_enter = True
                            # Если в систему вошли,
                            # Установить режим работы с БД.
                            self._DBMode = DBMode_
                            ic_user.icLet('DBMode', self._DBMode)
                            # то прописать в журнале регистрации
                            if self._login_manager:
                                self._login_manager.RegisterJournal(self._UserName, self._DBMode)
                            # Сохранить имя юзверя в хранилище переменных
                            ic_user.icLet('UserName', self._UserName)
                            # Выполнить скрипт прикладного программиста
                            if 'on_login' in self._UserRequisit:
                                self._exec_on_login(self._UserRequisit['on_login'])
                        else:
                            err_txt = u'''БД открыта в монопольном режиме другим пользователем.
                            Нельзя работать с БД в режиме <%s>''' % DBMode_
                            log.warning(err_txt)
                            raise icexceptions.LoginDBExclusiveException((coderror.IC_LOGIN_DBEXCLUSIVE_ERROR, err_txt))
                    else:
                        err_txt = u'Попытка входа в систему в нерабочее время: <%s>' % self._UserName
                        log.warning(err_txt)
                        raise icexceptions.LoginDBExclusiveException((coderror.IC_LOGIN_WORKTIME_ERROR, err_txt))
                else:
                    self._UserName = ''
                    self._UserRequisit = {}
                    err_txt = _('Invalid user login or password')
                    log.warning(err_txt)
                    raise icexceptions.LoginInvalidException((coderror.IC_LOGIN_ERROR, err_txt))
        except:
            log.fatal(u'User registration Error <%s>' % UserName_)
            raise
        
        ok = ['FAILED', 'OK'][int(sys_enter)]
        log.info(u'Enter to system: %s ... %s' % (self._UserName, ok))
        return sys_enter
        
    def _password_md5(self, Password_):
        """
        Получить из обычного пароля зашифрованный пароль.
        """
        import md5
        md5_password = md5.new(Password_).hexdigest()
        return md5_password
       
    def Login(self, DefaultUserName_=SYS_ADMIN_NAME,
              DefaultPassword_=None, DBMode_=ic_mode.DB_SHARE,
              RuntimeMode_=True, bAutoLogin=False):
        """
        Сделать заполнение формы логина пользователя и в случае удачного входа в систему загрузить реквизиты пользователя.
        @param DefaultUserName_: Имя пользователя по умолчанию.
        @param DefaultPassword_: Если задан пароль по умолчанию,
            то происходит автологин.
        @param DBMode_: Режим использования БД.
        @param RuntimeMode_: Признак режима исполнения.
        @return: Возвращает True, если вход в систему успешный.
        """
        user_login = None
        # Если файла ресурсов нет, тогда вход в систему не возможен
        if not os.path.isfile(self._ResFile):
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!', u'Файл прав пользователей не найден.')
            return False
        sys_enter = False   # Флаг входа в систему
        
        if self._login_manager:
            user_login = self._login_manager.Login(DefaultUserName_,
                                                   DefaultPassword_, DBMode_, RuntimeMode_)

        if DefaultPassword_ is not None:
            md5_password = self._password_md5(DefaultPassword_)
            # Автологин
            user_login = (DefaultUserName_, DefaultPassword_, md5_password)
        else:
            user_login = (DefaultUserName_, DefaultPassword_, None)
            
        # Если нажата кнопка Отмена, тогда прекратить логин
        if user_login is None:
            sys_enter = False
            return sys_enter
            
        # Проверка на вход в систему под рутом
        if user_login[ic_dlg.LOGIN_USER_IDX] == 'root':
            icbaseuser.icRootUser.Login(self,
                                        user_login[ic_dlg.LOGIN_USER_IDX],
                                        user_login[ic_dlg.LOGIN_PASSWORD_IDX])
            log.info(u'ROOT SYSTEM ENTER...OK')
            return True

        # Переопределить пользователя по умолчани.
        DefaultUserName_ = user_login[ic_dlg.LOGIN_USER_IDX]
            
        try:
            sys_enter = self.login_ok(user_login[ic_dlg.LOGIN_USER_IDX],
                                      user_login[ic_dlg.LOGIN_PASSWORD_IDX],
                                      user_login[ic_dlg.LOGIN_PASSWORD_MD5_IDX],
                                      DBMode_, RuntimeMode_)
        except icexceptions.LoginInvalidException:
            if bAutoLogin:
                raise
            else:
                ic_dlg.icMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
        except icexceptions.LoginErrorException:
            ic_dlg.icMsgBox(u'Вход в систему', u'Пользователь %s уже зарегистрирован в системе. Вход в систему запрещен.' % user_login[0])
        except icexceptions.LoginDBExclusiveException:
            ic_dlg.icMsgBox(u'Вход в систему', u'БД открыта в монопольном режиме другим пользователем. Вход в систему запрещен.')
        except icexceptions.LoginWorkTimeException:
            ic_dlg.icMsgBox(u'Вход в систему', u'Попытка входа в систему в не регламентированное время пользователем %s. Вход в систему запрещен.' % user_login[0])
        except:
            log.fatal(u'ERROR USER LOGIN RECORD: <%s> ' % user_login)
            raise
                
        return sys_enter

    def _exec_on_login(self, Code_):
        """
        Выполнить при успешном логине.
        """
        if ic_mode.isRuntimeMode():
            ic_exec.ExecuteMethod(Code_, self)
        
    def logout_ok(self):
        """
        Выход из системы.
        """
        if self._login_manager:
            self._login_manager.UnRegisterJournal()
        # Выполнить скрипт прикладного программиста
        if 'on_logout' in self._UserRequisit:
            self._exec_on_logout(self._UserRequisit['on_logout'])
        return True
    
    def Logout(self):
        """
        Выход из системы.
        """
        logout_result = self.logout_ok()

        ic_mode.setRuntimeMode(False)
        return logout_result

    def _exec_on_logout(self, Code_):
        """
        Выполнить при успешном логауте.
        """
        if ic_mode.isRuntimeMode():
            ic_exec.ExecuteMethod(Code_, self)

    def GetUserRequisit(self, UserName_=''):
        """
        Получить реквизиты пользователя.
        @param UserName_: Имя пользователя.
            Если UserName_ не определено, тогда возвращается
            описание прав доступа текущего пользователя.
            Если UserName определен, тогда возвращается
            описание прав доступа указанного пользователя.
        @return: Функция возвращает реквизиты текущего пользователя.
        """
        try:
            if UserName_ == '' or UserName_ is None or UserName_ == self._UserName:
                return self._UserRequisit
            else:
                access_dict = util.readAndEvalFile(self._ResFile)
                return self.CutUserRequisit(access_dict, UserName_)
        except:
            log.fatal(u'Ошибка опеределения реквизитов доступа к системным ресурсам пользователя')
            return None

    def GetAuthent(self, ResName_, ResType_=ACC_NONE, ShowMsg_=True):
        """
        Функция возвращает права доступа к ресурсу для текущего пользователя в виде 8-символьной строки.
        @param ResName_: имя ресурса.
        @param ResType_: тип ресурса, необязательный параметр.
            Если он не определен, ресурс ищется среди всех типов ресурсов.
        @param ShowMsg_: флаг, описывающий разрешение на отображение
            сообщения о заблокированном ресурсе для данного пользователя.
            Параметр необязателен. По умолчанию сообщение показывается.
        @return: Возвращает права доступа к ресурсу для текущего пользователя
            в виде 8-символьной строки. Например '----dawr'
        """
        try:
            # Если определен тип ресурса, ...
            if ResType_ != ACC_NONE:
                # ... тогда проверять только ресурсы этого типа
                for i_access in self._UserRequisit:
                    if i_access[ACC_IDX_RESTYPE] == ResType_:
                        if re.match(i_access[ACC_IDX_TEMPLAT], ResName_):
                            return i_access[ACC_IDX_PERMIT]
            else:
                # Иначе проверять все ресурсы
                for i_access in self._UserRequisit:
                    if re.match(i_access[ACC_IDX_TEMPLAT], ResName_):
                        return i_access[ACC_IDX_PERMIT]
            return FULL_ACCESS_PERMIT
        except:
            log.fatal(u'Ошибка определения прав доступа для ресурса')

    def CanAuthent(self, Permit_, ResName_, ResType_=ACC_NONE, ShowMsg_=True):
        """
        Функция определяет ограничения на запрашиваемый ресурс.
        @param Permit_: символ или группа символов,
            определяющий право доступа на действие.
            'u' - использование (ACCESS_USE).
            'v' - отображение  (ACCESS_VIEW).
            'r' - чтение (ACCESS_READ).
            'w' - редактирование (ACCESS_EDIT).
            'a' - добавление (ACCESS_APPEND).
            'd' - удаление (ACCESS_DELETE).
        @param ResName_: имя ресурса.
        @param ResType_: тип ресурса, необязательный параметр.
            Если он не определен, ресурс ищется среди всех типов ресурсов.
        @param ShowMsg_: флаг, описывающий разрешение на отображения
            сообщения о заблокированном ресурсе для данного пользователя.
            Параметр необязателен. По умолчанию сообщение показывается.
        @return: Возвращает True, если ресурс не ограничен,
            запрашиваемыми правами доступа, False - ресурс ограничен.
        """
        try:
            can = True
            # Если определен тип ресурса, ...
            # Вывести сообщение
            if (not can) and ShowMsg_:
                ic_dlg.icMsgBox(u'Ошибка!',
                                u'Доступ к ресурсу <%s> заблокирован.' % ResName_)
            return can
        except:
            log.fatal(u'Ошибка проверки прав доступа для ресурса')

    def CanAccess(self, AccessPermit_, AskPermit_):
        """
        Проверка на разрешение всех запрашиваемых прав.
        @param AccessPermit_: права доступа, строка 8 символов.
        @param AskPermit_: символ или группа символов,
            определяющий право доступа на действие.
        """
        for i_symb in AskPermit_:
            # Как только найден первый запрет, то возвратить ложь
            if AccessPermit_.find(i_symb) == -1:
                return False
        return True

    def CanWorkTime(self):
        """
        Проверить текущее время удовлетворяет временному графику доступа к системе.
        @return: Возвращает True если текущее время удовлетворяет временному графику.
            Иначе False.
        """
        return True

    def CanDBMode(self, DBMode_=ic_mode.DB_SHARE):
        """
        Можно залогиниться с таким режимом работы с БД?
        @param DBMode_: Режим использования БД.
        @return: Возвращает True, если вход разрешен.
        """
        if self._login_manager:
            return self._login_manager.CanDBMode(DBMode_)
        return True
    
    # --- Функции-свойства ---
    
    # def GetResources(self):
    #     """
    #     Функция возвращает список движков текущего пользователя.
    #     """
    #     try:
    #         if self._UserName and self._UserRequisit:
    #             return self._UserRequisit[RES_ACC_RUNRES]
    #         return []
    #     except:
    #         return []
    #
    # def GetRunners(self):
    #     """
    #     Функция возвращает список движков текущего пользователя.
    #     """
    #     try:
    #         if self._UserName and self._UserRequisit:
    #             if type(self._UserRequisit[RES_ACC_RUNNAME]) in (str, unicode):
    #                 return ic.utils.util.ic_eval(self._UserRequisit[RES_ACC_RUNNAME])
    #             else:
    #                 return self._UserRequisit[RES_ACC_RUNNAME]
    #         return []
    #     except:
    #         return []

    def getMenubarsPsp(self):
        """
        Список паспортов горизонтальных меню.
        """
        try:
            if self._UserName and self._UserRequisit:
                return self._UserRequisit['menubars']
            return []
        except:
            return []

    def getMainWinPsp(self):
        """
        Паспорт главного окна.
        """
        try:
            if self._UserName and self._UserRequisit:
                return self._UserRequisit['main_win']
            return None
        except:
            return None

    def SetResFile(self, ResFile_):
        """
        Установить ресурсный файл.
        """
        self._ResFile = ResFile_


class icUserGroup(icUserPrototype):
    """
    Группа пользователей.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icUserPrototype.__init__(self, *args, **kwargs)

        
class icUser(icUserPrototype):
    """
    Пользователь системы.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        icUserPrototype.__init__(self, *args, **kwargs)


class icLoginManager(object):        
    """
    Менеджер управления входа в систему.
    """

    def __init__(self, RegUserJrnFileName_=user_journal.DEFAULT_REG_JRN_FILE_NAME,
                 UsersResFileName_=DEFAULT_USERS_RES_FILE, loader_=None):
        """
        Конструктор.
        """
        from . import loader

        # Журнал регистрации пользователей
        self._reg_user_journal = user_journal.icRegUserJournal(RegUserJrnFileName_)
        # Инициализируем менеджера загрузки ресурса
        self._loader = loader_ or loader.icLoader()
        self._users_resource = None
        ic_user.icLet('LOADER', self._loader)
        users_res_file_name = ic_file.PathFile(ic_user.icGet('SYS_RES'), UsersResFileName_)
        self._users_resource = self._loader.load_res(users_res_file_name, bRefresh=True)

    def GetResource(self):
        return self._users_resource
    
    def GetUserResource(self, name):
        return self._users_resource.get(name, None)
    
    def _getAutoLogin(self, UserName_=None, Password_=None):
        """
        Определить имя пользователя и пароль для автологина если они гдето указаны.
        Автологин может задаваться как из коммандной строки, так и через
        дополнительные атрибуты проекта, которые затем попадают в хранилище переменных.
        @return: Функция возвращает кортеж (Логин,Пароль) используемый для автологина.
        """
        if UserName_:
            return UserName_, Password_
        store_auto_login = ic_user.icGet('AutoLogin')
        store_auto_psswd = ic_user.icGet('AutoPassword')
        if store_auto_login:
            return store_auto_login, store_auto_psswd
        return UserName_, Password_

    def IsAutoAuth(self):
        """
        Возвращает признак автоматической авторизации.
        """
        if ic_user.icGet('AutoLogin') in (None, 'None', ''):
            return False
        return True
        
    def Login(self, DefaultUserName_=SYS_ADMIN_NAME,
              DefaultPassword_=None, DBMode_=ic_mode.DB_SHARE,
              RuntimeMode_=True, ResFileName_=None):
        """
        Сделать заполнение формы логина пользователя и в случае удачного входа в систему загрузить реквизиты пользователя.
        @param DefaultUserName_: Имя пользователя по умолчанию.
        @param DefaultPassword_: Если задан пароль по умолчанию,
            то происходит автологин.
        @param DBMode_: Режим использования БД.
        @param RuntimeMode_: Признак режима исполнения.
        @return: Заполненную структуру ввода.
        """
        # Установить режим работы системы
        ic_mode.setRuntimeMode(RuntimeMode_)
        
        # Сначала проверить защиту от копирования
        if not self.CopyDefender():
            log.warning(u'Защита от копирования!')
            return False
        
        user_login = None
        if DefaultPassword_ is None:
            # Вызов диалога логина
            user_name = self.getRegLastUser()
            user_login = ic_dlg.icLoginDlg(None, u' Вход в систему',
                                           user_name, self.getRegUserList())
        else:
            import md5
            md5_password = md5.new(DefaultPassword_).hexdigest()
            # Автологин
            user_login = (DefaultUserName_, DefaultPassword_, md5_password)

        return user_login
    
    def CopyDefender(self):
        """
        Функция проверки защиты от копирования.
        """
        # Если проверка защиты отключена, тогда все ок и не проверять
        if not COPY_DEFENDER_ON:
            return True

        hdd_sn = ic_util.GetHDDSerialNo()
        reg_hdd_sn = ic_util.GetRegValue('Software\\DEFIS\\HDD', 'SerialNo')
        if hdd_sn == reg_hdd_sn:
            return True
        ic_dlg.icMsgBox(u'Вход в систему', u'Не зарегестрированная копия. Вход в систему не возможен.')
        return False
    
    def CanDBMode(self, DBMode_=ic_mode.DB_SHARE):
        """
        Можно залогиниться с таким режимом работы с БД?
        @param DBMode_: Режим использования БД.
        @return: Возвращает True, если вход разрешен.
        """
        # Посмотреть колтчество пользователей системы
        param_count = self._reg_user_journal.getCurrentUsersCount()
        # Если польхователей нет, тогда можно войти в системы с любым режимом
        if param_count == 0:
            return True
        # Если в системе 1 пользователь то посмотреть в каком режиме работает он
        elif param_count == 1:
            param_names = self._reg_user_journal.getCurrentUserNames()
            if param_names:
                param = self._reg_user_journal.getCurrentUserStartParam(param_names[0])
                if param[4] == ic_mode.DB_MONOPOLY:
                    return False
                elif param[4] == ic_mode.DB_SHARE:
                    return True
        # Если несколько пользователей то смотря какой режим нужен
        elif param_count > 1:
            if DBMode_ == ic_mode.DB_MONOPOLY:
                return False
            elif DBMode_ == ic_mode.DB_SHARE:
                return True
        return False
    
    def RegisterJournal(self, UserName_, DBMode_):
        """
        Прописать юзеря в журнале регистрации.
        @param UserName_: Имя пользователя.
        """
        prj_name = ic_user.icGet('PrjName')
        return self._reg_user_journal.register(UserName_, prj_name, DBMode_, ic_mode.isRuntimeMode())
    
    def getRegUserList(self):
        """
        Зарегестированные на текущей машине полизовательские имена.
        """
        reg_user_list = self._reg_user_journal.getRegUserList()
        for i, reg_user in enumerate(reg_user_list):
            if self._users_resource and \
               reg_user in self._users_resource and \
               'description' in self._users_resource[reg_user]:
                description = self._users_resource[reg_user]['description']
                if description:
                    reg_user_list[i] = u'%s (%s)' % (reg_user, description)
            
        return reg_user_list
        
    def getRegLastUser(self):
        """
        Последний зарегестрированный пользователь.
        """
        reg_last_user = self._reg_user_journal.getRegLastUserName()
        if self._users_resource and \
           reg_last_user in self._users_resource and \
           'description' in self._users_resource[reg_last_user]:
            description = self._users_resource[reg_last_user]['description']
            if description:
                reg_last_user += u' (%s)' % description

        return reg_last_user
        
    def UnRegisterJournal(self):
        """
        Вычеркнуть из журнала регистрации пользователей.
        """
        return self._reg_user_journal.unregister()

    def isRegUserName(self, UserName_):
        """
        Есть в журнале регистрации такой пользователь.
        """
        return self._reg_user_journal.isRegUserName(UserName_)
