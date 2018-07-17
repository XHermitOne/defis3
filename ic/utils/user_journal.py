#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Библиотека функций работы с журанлом пользователей.
"""

# --- Подключение пакетов ---
import wx
import time
import os
import os.path
from . import ic_file
from . import lock
from . import ini
from . import ic_mode
from ic.kernel import io_prnt

_ = wx.GetTranslation

__version__ = (0, 0, 0, 2)

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
        self._journal_file_name = ic_file.AbsolutePath(RegJrnFileName_)
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
        return lock.ComputerName()
        
    def getRegLastUserName(self):
        """
        Последний зарегестрированный пользователь.
        """
        return ini.loadParamINI(self._journal_file_name, 'REG_LAST_USER',
                                self.getComputerName())
            
    def getRegUserList(self):
        """
        Зарегестированные на текущей машине полизовательские имена.
        """
        param = ini.loadParamINI(self._journal_file_name, 'REG_USER_LIST',
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
            ini.saveParamINI(self._journal_file_name, 'REG_USER_LIST',
                             host_name, str(user_list))
            # Прописать текущего пользователя как последнего зарегестрированного
            ini.saveParamINI(self._journal_file_name, 'REG_LAST_USER',
                             host_name, str(UserName_))
            
            # Прописать машину,  юзеря и время входа в систему
            result = ini.saveParamINI(self._journal_file_name, 'CURRENT_USERS',
                                      UserName_, str(tuple(full_start_param)))
                
            # Указать в журнале текущего пользователя
            self.setCurUser(UserName_)

            if ic_mode.isDebugMode():
                io_prnt.outLog(u'Register user %s' % UserName_)
            return result
        except:
            io_prnt.outErr(u'Journal registration user error: %s.' % UserName_)
            return False    
            
    def unregister(self):
        """
        Вычеркнуть из журнала регистрации пользователей.
        """
        try:
            if self._del_reg_user:
                cur_username = self.getCurUser()
                if cur_username is None:
                    if ic_mode.isDebugMode():
                        io_prnt.outWarning(u'Not define current user')
                    return False
                else:
                    if ic_mode.isDebugMode():
                        io_prnt.outLog(u'Unregister user %s.' % cur_username)
                return ini.delParamINI(self._journal_file_name, 'CURRENT_USERS',
                                       cur_username)
            return True
        except:
            io_prnt.outErr(u'Journal delete user error: %s.' % self._journal_file_name)
            return False
            
    def getCurrentUsersCount(self):
        """
        Количество текущих пользователей системы.
        """
        try:
            if os.path.exists(self._journal_file_name):
                return ini.getParamCountINI(self._journal_file_name, 'CURRENT_USERS')
            return 0
        except:
            io_prnt.outErr(u'Journal define number of current users error: %s.' % self._journal_file_name)
            return None

    def getCurrentUserNames(self):
        """
        Имена текущих зарегистрированных пользователей.
        """
        try:
            return ini.getParamNamesINI(self._journal_file_name, 'CURRENT_USERS')
        except:
            io_prnt.outErr(u'Journal define current users names error: %s.' % self._journal_file_name)
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
            return eval(ini.loadParamINI(self._journal_file_name,
                                         'CURRENT_USERS', UserName_))
        except:
            io_prnt.outErr(u'Journal define user run parameters error: user=%s, journal=%s.' % (UserName_,
                                                                                                self._journal_file_name))
            return None
