#!/usr/bin/env python3
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
import hashlib

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
from . import glob_functions
import ic.config

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
LOCALDIR_DEFAULT = os.path.join(ic.config.PROFILE_PATH, 'wrk')

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
               'local_dir': LOCALDIR_DEFAULT,  # папка локальных настроек
               'main_win': None,   # Паспорт-идентификатор главного окна
               'menubars': [],     # Список меню.
               'on_login': None,   # скрипт, выполняемый после успешного логина
               'on_logout': None,  # скрипт, выполняемый после успешного логаута
               'roles': [],    # Список ролей
               }


__version__ = (0, 1, 1, 2)


# --- ФУНКЦИИ СИСТЕМЫ ОГРАНИЧЕНИЯ ДОСТУПА ---
def getUserRequisit(username):
    """
    Получить реквизиты пользователя.
    @param username: Имя пользователя.
        Если username не определено, тогда возвращается
        описание прав доступа текущего пользователя.
        Если UserName определен, тогда возвращается
        описание прав доступа указанного пользователя.
    @return: Функция возвращает реквизиты текущего пользователя.
    """
    if ic_mode.isRuntimeMode():
        # Режим исполнения
        app = glob_functions.getEngine()
        return app.getUser().getUserRequisit(username)
    else:
        # Режим редактирования
        return copy.deepcopy(SPC_IC_USER)


def getAuthent(res_name, res_type, bShowMsg=True):
    """
    Функция возвращает права доступа к ресурсу для текущего пользователя в виде 8-символьной строки.
    @param res_name: имя ресурса.
    @param res_type: тип ресурса.
    @param bShowMsg: флаг, описывающий разрешение на отображение
        сообщения о заблокированном ресурсе для данного пользователя.
        Параметр необязателен. По умолчанию сообщение показывается.
    @return: Возвращает права доступа к ресурсу для текущего пользователя
        в виде 8-символьной строки. Например '----dawr'
    """
    if ic_mode.isRuntimeMode():
        # Режим исполнения
        app = glob_functions.getEngine()
        return app.getUser().getAuthent(res_name, res_type, bShowMsg)
    else:
        # Режим редактирования
        return FULL_ACCESS_PERMIT


def canAuthent(permit, res_name, res_type, bShowMsg=True):
    """
    Функция определяет ограничения на запрашиваемый ресурс.
    @param permit: символ или группа символов,
        определяющий право доступа на действие.
        'u' - использование (ACCESS_USE).
        'v' - отображение  (ACCESS_VIEW).
        'r' - чтение (ACCESS_READ).
        'w' - редактирование (ACCESS_EDIT).
        'a' - добавление (ACCESS_APPEND).
        'd' - удаление (ACCESS_DELETE).
    @param res_name: имя ресурса.
    @param res_type: тип ресурса.
    @param bShowMsg: флаг, описывающий разрешение на отображения
        сообщения о заблокированном ресурсе для данного пользователя.
        Параметр необязателен. По умолчанию сообщение показывается.
    @return: Возвращает True, если ресурс не ограничен,
        запрашиваемыми правами доступа, False - ресурс ограничен.
    """
    # ВНИМАНИЕ!!! Проверка осуществляется только в режиме выполнения
    if ic_mode.isRuntimeMode():
        app = glob_functions.getEngine()
        if app:
            return app.getUser().canAuthent(permit, res_name, res_type, bShowMsg)
    return True


class icUserPrototype(icbaseuser.icRootUser):
    """
    Класс пользователя системы.
    """
    
    def __init__(self, res_filename=DEFAULT_USERS_RES_FILE, login_manager=None):
        """
        Конструктор класса.
        """
        # Базовый пользователь, получающий доступ к ядру
        # и управляющий объектами системы
        icbaseuser.icRootUser.__init__(self)

        # --- Атрибуты класса ---
        # Ресурсный файл
        self._ResFile = res_filename
        # Имя текущего пользователя
        self._UserName = ''
        # Реквизиты текущего пользователя:
        self._UserRequisit = {}
        # Режим работы с БД.
        self._DBMode = ic_mode.DB_SHARE
        
        self._login_manager = login_manager

    def setLoginManager(self, login_manager):
        """
        Установить менеджер входа в систему.
        """
        self._login_manager = login_manager
        
    def getUserResFileName(self):
        """
        Имя ресурсного файла пользователей.
        """
        if self._ResFile:
            return ic_file.getAbsolutePath(self._ResFile)
        return self._ResFile
    
    def setUserResFileName(self, res_filename):
        """
        Установить ресурсный файл.
        """
        self._ResFile = res_filename

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
        
    def _createRoles(self, reles_id=None):
        """
        Создание списка ролей по идентификаторам.
        @return: Список объектов ролей.
        """
        if reles_id is None:
            reles_id = self._getRolesIdList()
            
        role_obj_list = []
        for role_id in reles_id:
            new_role_psp = (('Role', role_id, None, role_id+'.rol', None),)
            new_role_obj = glob_functions.getKernel().createResObjByPsp(new_role_psp, context=self.GetContext())
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

    def Load(self, username, res_filename=None):
        """
        Загузить все реквизиты из ресурсного файла.
        @param username: Имя пользователя в ресурсном файле.
        @param res_filename: Имя ресурсного файла.
        """
        try:
            if res_filename is not None:
                self.setUserResFileName(res_filename)
            res_filename = self.getUserResFileName()
            access_dict = util.readAndEvalFile(res_filename, bRefresh=True)

            # Запомнить имя ...
            self._UserName = username

            if username in access_dict:
                # Собрать данные из словаря по одному пользователю.
                self._UserRequisit = self.cutUserRequisit(access_dict, username, self._UserRequisit)
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

    def _cutGroupRequisite(self, access_dict, user_group_name, user_requisit=None):
        """
        Собрать данные по группам.
        @param access_dict: Словарь описаний ограничений доступа
            пользователей системы.
        @param user_group_name: Имя группы пользователей в ресурсном файле.
        @param user_requisit: Текущий реквизит пользователя.
            При первом вызове функции д.б. {}
        """
        if user_requisit is None:
            user_requisit = {}
        group_data = access_dict[user_group_name]
        
        # временной график  доступа к системе  за неделю
        if (('lock_time' not in user_requisit) or (not user_requisit['lock_time'])) and \
           'lock_time' in group_data:
            user_requisit['lock_time'] = group_data['lock_time']
        # Список меню
        if (('menubars' not in user_requisit) or (not user_requisit['menubars'])) and \
           'menubars' in group_data:
            user_requisit['menubars'] = group_data['menubars']
        # скрипт, выполняемый после успешного логина
        if (('on_login' not in user_requisit) or (not user_requisit['on_login'])) and \
           'on_login' in group_data:
            user_requisit['on_login'] = group_data['on_login']
        # скрипт, выполняемый после успешного логаута
        if (('on_logout' not in user_requisit) or (not user_requisit['on_logout'])) and \
           'on_logout' in group_data:
            user_requisit['on_logout'] = group_data['on_logout']
        
        if 'group' in group_data and group_data['group']:
            user_requisit = self._cutGroupRequisit(access_dict, group_data['group'], user_requisit)
            
        return user_requisit
        
    def cutUserRequisit(self, access_dict, username, user_requisit=None):
        """
        Собрать данные из словаря по одному пользователю.
        @param access_dict: Словарь описаний ограничений доступа
            пользователей системы.
        @param username: Имя пользователя в ресурсном файле.
        @param user_requisit: Текущий реквизит пользователя.
            При первом вызове функции д.б. {}
        """
        try:
            if user_requisit is None:
                user_requisit = {}

            user_data = access_dict[username]
            user_data = copy.deepcopy(ic_util.SpcDefStruct(SPC_IC_USER, user_data))

            if 'group' in user_data and user_data['group']:
                requisites = self._cutGroupRequisite(access_dict, user_data['group'])
                # временной график  доступа к системе  за неделю
                if (('lock_time' not in user_data) or (not user_data['lock_time'])) and \
                   'lock_time' in requisites:
                    user_requisit['lock_time'] = requisites['lock_time']
                # Список меню
                if (('menubars' not in user_data) or (not user_data['menubars'])) and \
                   'menubars' in requisites:
                    user_requisit['menubars'] = requisites['menubars']
                # скрипт, выполняемый после успешного логина
                if (('on_login' not in user_data) or (not user_data['on_login'])) and \
                   'on_login' in requisites:
                    user_requisit['on_login'] = requisites['on_login']
                # скрипт, выполняемый после успешного логаута
                if (('on_logout' not in user_data) or (not user_data['on_logout'])) and \
                   'on_logout' in requisites:
                    user_requisit['on_logout'] = requisites['on_logout']
                
            if user_requisit:
                user_data.update(user_requisit)

            return user_data
        except:
            # Ошибка сбора данных доступа для регистрируемого пользователя')
            log.fatal(u'User Requisite Error')
            return None
        
    def loadUser(self, username, res_filename=DEFAULT_USERS_RES_FILE):
        """
        Загузить данные из ресурсного файла по одному пользователю.
        @param username: Имя пользователя в ресурсном файле.
        @param res_filename: Имя ресурсного файла.
        """
        try:
            access_dict = util.readAndEvalFile(res_filename)
            return access_dict[username]
        except:
            log.fatal(u'Load User Requisite Error')

    def _checkLoginUser(self, username):
        """
        Проверка зарегистрированного пользователя.
        @param username: Имя пользователя.
        """
        if not ic_mode.isRuntimeMode():
            # Если режим конфигурирования, то обязательно
            # проверять уникальность регистрации
            # чтобы проблем с блокировками не было
            if self._login_manager:
                return self._login_manager.isRegUserName(username)
        return False
      
    def _password_compare(self, user_password, login_password, login_password_crc):
        """
        Функция сравнения паролей.
        @param user_password: Пароль определенный для пользователя в ресурсе.
        @param login_password: Введенный пароль при логине.
        @param login_password_crc: Контрольная сумма md5 введенного пароля при логине.
        @return: Возвращает True если пароли совпадают и False если не совпадают.
        """
        if user_password is None or user_password == '':
            # Пароль для пользователя не определен
            # Можно в систему входить без пароля
            return True
        elif len(user_password) < 32:
            # Пароль для пользователя определен просто строкой
            return user_password == login_password
        elif len(user_password) == 32:
            # Пароль для пользователя в ресурсе задан как контрольная сумма md5
            return user_password == login_password_crc
        return False
        
    def login_ok(self, username=SYS_ADMIN_NAME, password=None, password_crc=None,
                 db_mode=ic_mode.DB_SHARE, bRuntimeMode=True):
        """
        Залогинить пользователя.
        @param username: Имя пользователя.
        @param password: Если задан пароль по умолчанию,
            то происходит автологин.
        @param password_crc: Контрольная сумма логина.
        @param db_mode: Режим использования БД.
        @param bRuntimeMode: Признак режима исполнения.
        @return: Возвращает True, если вход в систему успешный.
        """
        try:
            sys_enter = False  # Флаг входа в систему

            if self._checkLoginUser(username):
                if username:
                    err_txt = 'Пользователь <%s> уже зарегистрирован в системе' % self._UserName
                    log.warning(err_txt)
                    raise icexceptions.LoginErrorException((coderror.IC_LOGIN_ERROR, err_txt))
        
            if username:
                self.Load(username)
                if self._UserName and \
                   self._password_compare(self._UserRequisit['password'], password, password_crc):
                    # Проверка входа в систему в нерабочее время
                    if self.canWorkTime():
                        if self.canDBMode(db_mode):
                            sys_enter = True
                            # Если в систему вошли,
                            # Установить режим работы с БД.
                            self._DBMode = db_mode
                            glob_functions.letVar('DBMode', self._DBMode)
                            # то прописать в журнале регистрации
                            if self._login_manager:
                                self._login_manager.registerJournal(self._UserName, self._DBMode)
                            # Сохранить имя юзверя в хранилище переменных
                            glob_functions.letVar('UserName', self._UserName)
                            # Выполнить скрипт прикладного программиста
                            if 'on_login' in self._UserRequisit:
                                self._exec_on_login(self._UserRequisit['on_login'])
                        else:
                            err_txt = u'''БД открыта в монопольном режиме другим пользователем.
                            Нельзя работать с БД в режиме <%s>''' % db_mode
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
            log.fatal(u'Ошибка регистрации пользователя <%s>' % username)
            raise
        
        ok = ['FAILED', 'OK'][int(sys_enter)]
        log.info(u'Вход в систему <%s> ... %s' % (self._UserName, ok))
        return sys_enter
        
    def _get_password_crc(self, password):
        """
        Получить из обычного пароля зашифрованный пароль.
        """
        crc_password = hashlib.md5(password.encode()).hexdigest()
        return crc_password
       
    def Login(self, default_username=SYS_ADMIN_NAME,
              default_password=None, db_name=ic_mode.DB_SHARE,
              bRuntimeMode=True, bAutoLogin=False):
        """
        Сделать заполнение формы логина пользователя и в случае удачного входа в систему загрузить реквизиты пользователя.
        @param default_username: Имя пользователя по умолчанию.
        @param default_password: Если задан пароль по умолчанию,
            то происходит автологин.
        @param db_name: Режим использования БД.
        @param bRuntimeMode: Признак режима исполнения.
        @return: Возвращает True, если вход в систему успешный.
        """
        user_login = None
        res_filename = self.getUserResFileName()

        # Если файла ресурсов нет, тогда вход в систему не возможен
        if not os.path.exists(res_filename):
            err_msg = u'Файл прав пользователей <%s> не найден.' % res_filename
            log.warning(err_msg)
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', err_msg)
            return False
        sys_enter = False   # Флаг входа в систему
        
        if self._login_manager:
            user_login = self._login_manager.Login(default_username,
                                                   default_password, db_name, bRuntimeMode)

        if default_password is not None:
            md5_password = self._get_password_crc(default_password)
            # Автологин
            user_login = (default_username, default_password, md5_password)
        else:
            user_login = (default_username, default_password, None)
            
        # Если нажата кнопка Отмена, тогда прекратить логин
        if user_login is None:
            sys_enter = False
            return sys_enter
            
        # Проверка на вход в систему под рутом
        if user_login[ic_dlg.LOGIN_USER_IDX] == 'root':
            icbaseuser.icRootUser.Login(self,
                                        user_login[ic_dlg.LOGIN_USER_IDX],
                                        user_login[ic_dlg.LOGIN_PASSWORD_IDX])
            log.info(u'Вход в систему с правами Администратора...OK')
            return True

        # Переопределить пользователя по умолчани.
        default_username = user_login[ic_dlg.LOGIN_USER_IDX]
            
        try:
            sys_enter = self.login_ok(user_login[ic_dlg.LOGIN_USER_IDX],
                                      user_login[ic_dlg.LOGIN_PASSWORD_IDX],
                                      user_login[ic_dlg.LOGIN_PASSWORD_MD5_IDX],
                                      db_name, bRuntimeMode)
        except icexceptions.LoginInvalidException:
            if bAutoLogin:
                raise
            else:
                ic_dlg.icMsgBox(u'Вход в систему',
                                u'Неправильный пользователь или пароль. Доступ запрещен.')
        except icexceptions.LoginErrorException:
            ic_dlg.icMsgBox(u'Вход в систему',
                            u'Пользователь %s уже зарегистрирован в системе. Вход в систему запрещен.' % user_login[0])
        except icexceptions.LoginDBExclusiveException:
            ic_dlg.icMsgBox(u'Вход в систему',
                            u'БД открыта в монопольном режиме другим пользователем. Вход в систему запрещен.')
        except icexceptions.LoginWorkTimeException:
            ic_dlg.icMsgBox(u'Вход в систему',
                            u'Попытка входа в систему в не регламентированное время пользователем %s. Вход в систему запрещен.' % user_login[0])
        except:
            log.fatal(u'Ошибка входа пользователя в систему. Параметры входа <%s> ' % user_login)
            raise
                
        return sys_enter

    def _exec_on_login(self, exec_code):
        """
        Выполнить при успешном логине.
        """
        if ic_mode.isRuntimeMode():
            ic_exec.execute_method(exec_code, self)
        
    def logout_ok(self):
        """
        Выход из системы.
        """
        if self._login_manager:
            self._login_manager.unregisterJournal()
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

    def _exec_on_logout(self, exec_code):
        """
        Выполнить при успешном логауте.
        """
        if ic_mode.isRuntimeMode():
            ic_exec.execute_method(exec_code, self)

    def getUserRequisit(self, username=''):
        """
        Получить реквизиты пользователя.
        @param username: Имя пользователя.
            Если username не определено, тогда возвращается
            описание прав доступа текущего пользователя.
            Если UserName определен, тогда возвращается
            описание прав доступа указанного пользователя.
        @return: Функция возвращает реквизиты текущего пользователя.
        """
        try:
            if username == '' or username is None or username == self._UserName:
                return self._UserRequisit
            else:
                res_filename = self.getUserResFileName()
                access_dict = util.readAndEvalFile(res_filename)
                return self.cutUserRequisit(access_dict, username)
        except:
            log.fatal(u'Ошибка опеределения реквизитов доступа к системным ресурсам пользователя')
            return None

    def getAuthent(self, res_name, res_type=ACC_NONE, bShowMsg=True):
        """
        Функция возвращает права доступа к ресурсу для текущего пользователя в виде 8-символьной строки.
        @param res_name: имя ресурса.
        @param res_type: тип ресурса, необязательный параметр.
            Если он не определен, ресурс ищется среди всех типов ресурсов.
        @param bShowMsg: флаг, описывающий разрешение на отображение
            сообщения о заблокированном ресурсе для данного пользователя.
            Параметр необязателен. По умолчанию сообщение показывается.
        @return: Возвращает права доступа к ресурсу для текущего пользователя
            в виде 8-символьной строки. Например '----dawr'
        """
        try:
            # Если определен тип ресурса, ...
            if res_type != ACC_NONE:
                # ... тогда проверять только ресурсы этого типа
                for i_access in self._UserRequisit:
                    if i_access[ACC_IDX_RESTYPE] == res_type:
                        if re.match(i_access[ACC_IDX_TEMPLAT], res_name):
                            return i_access[ACC_IDX_PERMIT]
            else:
                # Иначе проверять все ресурсы
                for i_access in self._UserRequisit:
                    if re.match(i_access[ACC_IDX_TEMPLAT], res_name):
                        return i_access[ACC_IDX_PERMIT]
            return FULL_ACCESS_PERMIT
        except:
            log.fatal(u'Ошибка определения прав доступа для ресурса')

    def canAuthent(self, permit, res_name, res_type=ACC_NONE, bShowMsg=True):
        """
        Функция определяет ограничения на запрашиваемый ресурс.
        @param permit: символ или группа символов,
            определяющий право доступа на действие.
            'u' - использование (ACCESS_USE).
            'v' - отображение  (ACCESS_VIEW).
            'r' - чтение (ACCESS_READ).
            'w' - редактирование (ACCESS_EDIT).
            'a' - добавление (ACCESS_APPEND).
            'd' - удаление (ACCESS_DELETE).
        @param res_name: имя ресурса.
        @param res_type: тип ресурса, необязательный параметр.
            Если он не определен, ресурс ищется среди всех типов ресурсов.
        @param bShowMsg: флаг, описывающий разрешение на отображения
            сообщения о заблокированном ресурсе для данного пользователя.
            Параметр необязателен. По умолчанию сообщение показывается.
        @return: Возвращает True, если ресурс не ограничен,
            запрашиваемыми правами доступа, False - ресурс ограничен.
        """
        try:
            can = True
            # Если определен тип ресурса, ...
            # Вывести сообщение
            if (not can) and bShowMsg:
                ic_dlg.icMsgBox(u'Ошибка!',
                                u'Доступ к ресурсу <%s> заблокирован.' % res_name)
            return can
        except:
            log.fatal(u'Ошибка проверки прав доступа для ресурса')

    def canAccess(self, access_permit, ask_permit):
        """
        Проверка на разрешение всех запрашиваемых прав.
        @param access_permit: права доступа, строка 8 символов.
        @param ask_permit: символ или группа символов,
            определяющий право доступа на действие.
        """
        for i_symb in ask_permit:
            # Как только найден первый запрет, то возвратить ложь
            if access_permit.find(i_symb) == -1:
                return False
        return True

    def canWorkTime(self):
        """
        Проверить текущее время удовлетворяет временному графику доступа к системе.
        @return: Возвращает True если текущее время удовлетворяет временному графику.
            Иначе False.
        """
        return True

    def canDBMode(self, db_mode=ic_mode.DB_SHARE):
        """
        Можно залогиниться с таким режимом работы с БД?
        @param db_mode: Режим использования БД.
        @return: Возвращает True, если вход разрешен.
        """
        if self._login_manager:
            return self._login_manager.canDBMode(db_mode)
        return True
    
    # --- Функции-свойства ---
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

    def __init__(self, reg_user_jrn_filename=user_journal.DEFAULT_REG_JRN_FILE_NAME,
                 users_res_filename=DEFAULT_USERS_RES_FILE, loader=None):
        """
        Конструктор.
        """
        from . import db_res_load_manager

        # Журнал регистрации пользователей
        self._reg_user_journal = user_journal.icRegUserJournal(reg_user_jrn_filename)
        # Инициализируем менеджера загрузки ресурса
        self._loader = loader or db_res_load_manager.icDBResLoadManager()
        self._users_resource = None
        glob_functions.letVar('LOADER', self._loader)
        users_res_file_name = ic_file.PathFile(glob_functions.getVar('SYS_RES'), users_res_filename)
        self._users_resource = self._loader.load_res(users_res_file_name, bRefresh=True)

    def getResource(self):
        return self._users_resource
    
    def getUserResource(self, name):
        try:
            return self._users_resource.get(name, None)
        except:
            log.fatal(u'Ошибка определения ресурса пользователя')
        return None
    
    def _getAutoLogin(self, username=None, password=None):
        """
        Определить имя пользователя и пароль для автологина если они гдето указаны.
        Автологин может задаваться как из коммандной строки, так и через
        дополнительные атрибуты проекта, которые затем попадают в хранилище переменных.
        @return: Функция возвращает кортеж (Логин,Пароль) используемый для автологина.
        """
        if username:
            return username, password
        store_auto_login = glob_functions.getVar('AutoLogin')
        store_auto_psswd = glob_functions.getVar('AutoPassword')
        if store_auto_login:
            return store_auto_login, store_auto_psswd
        return username, password

    def isAutoAuth(self):
        """
        Возвращает признак автоматической авторизации.
        """
        if glob_functions.getVar('AutoLogin') in (None, 'None', ''):
            return False
        return True
        
    def Login(self, default_username=SYS_ADMIN_NAME,
              default_password=None, db_mode=ic_mode.DB_SHARE,
              bRuntimeMode=True, res_filename=None):
        """
        Сделать заполнение формы логина пользователя и в случае удачного входа в систему загрузить реквизиты пользователя.
        @param default_username: Имя пользователя по умолчанию.
        @param default_password: Если задан пароль по умолчанию,
            то происходит автологин.
        @param db_mode: Режим использования БД.
        @param bRuntimeMode: Признак режима исполнения.
        @return: Заполненную структуру ввода.
        """
        # Установить режим работы системы
        ic_mode.setRuntimeMode(bRuntimeMode)
        
        # Сначала проверить защиту от копирования
        if not self.CopyDefender():
            log.warning(u'Защита от копирования!')
            return False
        
        user_login = None
        if default_password is None:
            # Вызов диалога логина
            user_name = self.getRegLastUser()
            user_login = ic_dlg.icLoginDlg(None, u' Вход в систему',
                                           user_name, self.getRegUserList())
        else:
            md5_password = hashlib.md5(default_password.encode()).hexdigest()
            # Автологин
            user_login = (default_username, default_password, md5_password)

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
    
    def canDBMode(self, db_mode=ic_mode.DB_SHARE):
        """
        Можно залогиниться с таким режимом работы с БД?
        @param db_mode: Режим использования БД.
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
            if db_mode == ic_mode.DB_MONOPOLY:
                return False
            elif db_mode == ic_mode.DB_SHARE:
                return True
        return False
    
    def registerJournal(self, username, db_mode):
        """
        Прописать юзеря в журнале регистрации.
        @param username: Имя пользователя.
        """
        prj_name = glob_functions.getVar('PrjName')
        return self._reg_user_journal.register(username, prj_name, db_mode, ic_mode.isRuntimeMode())
    
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
        
    def unregisterJournal(self):
        """
        Вычеркнуть из журнала регистрации пользователей.
        """
        return self._reg_user_journal.unregister()

    def isRegUserName(self, username):
        """
        Есть в журнале регистрации такой пользователь.
        """
        return self._reg_user_journal.isRegUserName(username)
