#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Библиотека функций работы с журанлом пользователей.
"""

# --- Подключение пакетов ---
import wx
import time
import os
import os.path

from . import filefunc
from . import lockfunc
from . import inifunc
from . import modefunc
from ic.log import log

__version__ = (0, 1, 1, 1)

_ = wx.GetTranslation

# --- Constants ---
# Имя журнала регистрации пользователей по умолчанию
DEFAULT_REG_JRN_FILE_NAME = './log/reg_user_journal.ini'


class icRegUserJournal:
    """
    Журнал пользователей.
    """

    def __init__(self, RegJrnFileName_=DEFAULT_REG_JRN_FILE_NAME):
        """
        Конструктор.
        @param RegJrnFileName_: Файл журнала регистрации пользователей.
        """
        # Имя файла журнала регистрации
        self._journal_file_name = filefunc.get_absolute_path(RegJrnFileName_)
        # Имя текущего ползователя
        self._current_user = None
        # Удалить регистрацию о пользователе из журнала?
        self._del_reg_user = True
    
    def getCurUser(self):
        """
        Текущий пользователь.
        """
        return self._current_user
        
    def setCurUser(self, UserName_):
        """
        Текущий пользователь.
        """
        self._current_user = UserName_
        
    def getComputerName(self):
        """
        Имя компьютера.
        """
        return lockfunc.ComputerName()
        
    def getRegLastUserName(self):
        """
        Последний зарегестрированный пользователь.
        """
        return inifunc.loadParamINI(self._journal_file_name, 'REG_LAST_USER',
                                    self.getComputerName())
            
    def getRegUserList(self):
        """
        Зарегестированные на текущей машине полизовательские имена.
        """
        param = inifunc.loadParamINI(self._journal_file_name, 'REG_USER_LIST',
                                     self.getComputerName())
        if isinstance(param, str) and bool(param):
            return eval(param)
        return []
   
    def isRegUserName(self, UserName_):
        """
        Пользователь уже зарегистрирован?
        @param UserName_: Имя пользователя.
        """
        user_list = self.getCurrentUserNames()
        if user_list:
            return UserName_ in user_list
        return False
        
    def register(self, UserName_, *StartParam_):
        """
        Зарегистрировать пользователя в журнале.
        @param UserName_: Имя пользователя.
        @param StartParam_: Параметры запуска.
        """
        try:
            if self.isRegUserName(UserName_):
                self._del_reg_user = False
                
            # Текущее время
            str_time = time.asctime(time.localtime(time.time()))
            # Имя компьютера
            host_name = self.getComputerName()
            full_start_param = [str_time, host_name, UserName_]+list(StartParam_)
            # Прописать в списке зарегестрированных пользователей текущего юзера
            user_list = self.getRegUserList()

            if UserName_ not in user_list:
                user_list.append(UserName_)
            inifunc.saveParamINI(self._journal_file_name, 'REG_USER_LIST',
                                 host_name, str(user_list))
            # Прописать текущего пользователя как последнего зарегестрированного
            inifunc.saveParamINI(self._journal_file_name, 'REG_LAST_USER',
                                 host_name, str(UserName_))
            
            # Прописать машину,  юзеря и время входа в систему
            result = inifunc.saveParamINI(self._journal_file_name, 'CURRENT_USERS',
                                          UserName_, str(tuple(full_start_param)))
                
            # Указать в журнале текущего пользователя
            self.setCurUser(UserName_)

            if modefunc.isDebugMode():
                log.info(u'Регистрация пользователя <%s>' % UserName_)
            return result
        except:
            log.fatal(u'Ошибка регистрации пользователя <%s> в журнале' % UserName_)
            return False    
            
    def unregister(self):
        """
        Вычеркнуть из журнала регистрации пользователей.
        """
        try:
            if self._del_reg_user:
                cur_username = self.getCurUser()
                if cur_username is None:
                    if modefunc.isDebugMode():
                        log.warning(u'Не определен текущий пользователь')
                    return False
                else:
                    if modefunc.isDebugMode():
                        log.info(u'Снятие регистрации пользовтеля %s.' % cur_username)
                return inifunc.delParamINI(self._journal_file_name, 'CURRENT_USERS',
                                           cur_username)
            return True
        except:
            log.fatal(u'Ошибка удаления пользователя из журнала <%s>' % self._journal_file_name)
            return False
            
    def getCurrentUsersCount(self):
        """
        Количество текущих пользователей системы.
        """
        try:
            if os.path.exists(self._journal_file_name):
                return inifunc.getParamCountINI(self._journal_file_name, 'CURRENT_USERS')
            return 0
        except:
            log.fatal(u'Ошибка определения количества текущих пользователей системы. Журанал <%s>' % self._journal_file_name)
            return None

    def getCurrentUserNames(self):
        """
        Имена текущих зарегистрированных пользователей.
        """
        try:
            return inifunc.getParamNamesINI(self._journal_file_name, 'CURRENT_USERS')
        except:
            log.fatal(u'Ошибка определения имен текущих пользователей системы. Журнал <%s>' % self._journal_file_name)
            return None
        
    def getCurrentRegComputers(self):
        """
        Имена текущих зарегистрированных хостов.
        """
        return []

    def getCurrentUserStartParam(self, UserName_):
        """
        Параметры запуска пользователя.
        @param UserName_: Имя пользователя.
        """
        try:
            return eval(inifunc.loadParamINI(self._journal_file_name,
                                         'CURRENT_USERS', UserName_))
        except:
            log.fatal(u'Ошибка определения параметров запуска пользователя <%s>. Журнал <%s>' % (UserName_,
                                                                                                 self._journal_file_name))
            return None
