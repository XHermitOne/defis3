#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Поддержка доступа к настройке проекта системы через точку.
Внешние настройки проекта храняться в *.ini файле проекта:
../<Project Dir>/<Project Name>/<Project Name>.ini
"""

# Подключение библиотек
import os
import os.path

from ic.utils import modefunc
from ic.utils import inifunc
from ic.utils import execfunc
from ic.engine import glob_functions
from ic.log import log

__version__ = (0, 1, 2, 1)


def setProjectSettingsToEnvironment(ProjectName_=None, ReDefine_=False):
    """
    Добавить все переменные из *.ini файла в окружение системы.

    :param ProjectName_: Имя проекта. Если None, то берется
    текущий проект.
    :param ReDefine_: Переопределять переменные в окружении?
    :return: True/False.
    """
    prj_settings = None
    if glob_functions.getSettings() is None:
        if modefunc.isDebugMode():
            log.info(u'Не определена переменная настроек проекта.')
        prj_dir = glob_functions.getVar('PRJ_DIR')
        prj_name = glob_functions.getVar('PrjName')
        if prj_dir and prj_name:
            prj_ini_file_name = os.path.join(prj_dir, prj_name+'.ini')
            prj_settings = inifunc.INI2Dict(prj_ini_file_name)
    else:    
        if ProjectName_ is None:
            prj_settings = glob_functions.getSettings().THIS.get()
        else:
            prj_settings = getattr(glob_functions.getSettings(), ProjectName_).get()
            
    if prj_settings:
        for section_name, section in prj_settings.items():
            for param, value in section.items():
                if glob_functions.isVar(param):
                    log.info(u'Переменная %s уже определена в окружении' % param)
                    if ReDefine_:
                        glob_functions.letVar(param, value)
                        log.info(u'Переменная %s переопределена в окружении' % param)
                else:
                    glob_functions.letVar(param, value)
        if modefunc.isDebugMode():
            glob_functions.printVarStorage()
        return True
    return False
    

class icSettingsDotUsePrototype(object):
    """
    Класс поддержки доступа к настройкам проекта.
    """
    def __init__(self, DefaultSettingsList_=None):
        """
        Консруктор.

        :param DefaultSettingsList_: Передающийся по точке список указания 
        параметра настройки. Список состоит из 3-х элементов:
        где,
        0 - имя проекта.
        1 - имя секции.
        2 - имя параметра в секции.
        """
        if DefaultSettingsList_:
            self._cur_settings_list = DefaultSettingsList_
        else:
            self._cur_settings_list = [None, None, None]
        
    def _get_ini_file_name(self):
        """
        Определить полное имя файла настроек из имени проекта.
        """
        prj_dir = glob_functions.getVar('PRJ_DIR')
        if prj_dir:
            ini_file_name = os.path.join(prj_dir, self._cur_settings_list[0]+'.ini')
        else:
            prj_name = self._cur_settings_list[0]
            ini_file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                         prj_name, prj_name, '%s.ini' % prj_name)
        return ini_file_name
    
    def get(self):
        """
        Функция получения значения.
        """
        return None
    
    def set(self, value):
        """
        Функция сохранения значения.

        :param value: Сохраняемое значение.
        """
        return None


class icSettingsDotUse(icSettingsDotUsePrototype):
    """
    Класс описания настроек проекта. Для доступа к настройкам проекта через точку.
    """
    THIS_PRJ = 'THIS'

    def __init__(self, DefaultSettingsList_=None):
        """
        Конструктор.
        """
        icSettingsDotUsePrototype.__init__(self, DefaultSettingsList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к настройкам проекта через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            

        prj = icPrjDotUse(object.__getattribute__(self, '_cur_settings_list'))

        if AttrName_ == object.__getattribute__(self, 'THIS_PRJ'):
            prj._cur_settings_list[0] = glob_functions.getVar('PrjName')
        else:
            prj._cur_settings_list[-1] = AttrName_
            
        return prj


class icPrjDotUse(icSettingsDotUsePrototype):
    """
    Класс проекта. Для доступа к настройки проекта через точку.
    """
    def __init__(self, DefaultSettingsList_=None):
        """
        Конструктор.
        """
        icSettingsDotUsePrototype.__init__(self, DefaultSettingsList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к секциям файла настройки через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        section = icSectionDotUse(object.__getattribute__(self, '_cur_settings_list'))
        section._cur_settings_list[1] = AttrName_
        return section

    def get(self):
        """
        Функция получения значения.
        """
        ini_file_name = self._get_ini_file_name()
        return inifunc.INI2Dict(ini_file_name)
    
    def set(self, value):
        """
        Функция сохранения значения.

        :param value: Сохраняемое значение.
        """
        if isinstance(value, dict):
            ini_file_name = self._get_ini_file_name()
            return inifunc.Dict2INI(value, ini_file_name, True)
        return None

    def edit(self):
        """
        Запуск редактирования INI файла настроек
        """
        ini_file_name = self._get_ini_file_name()
        if os.path.exists(ini_file_name):
            cmd = 'gedit %s &' % ini_file_name
            execfunc.doSysCmd(cmd)
        else:
            log.warning(u'INI файл <%s> не найден' % ini_file_name)


class icSectionDotUse(icSettingsDotUsePrototype):
    """
    Класс секции файла настройки проекта. Для доступа к настройкам проекта через точку.
    """
    def __init__(self, DefaultSettingsList_=None):
        """
        Конструктор.
        """
        icSettingsDotUsePrototype.__init__(self, DefaultSettingsList_)

    def __getattribute__(self, AttrName_):
        """
        Поддержка доступа к параметрам файла настройки через точку.
        """
        try:
            return object.__getattribute__(self, AttrName_)
        except AttributeError:
            pass            
            
        param = icParamDotUse(object.__getattribute__(self, '_cur_settings_list'))
        param._cur_settings_list[2] = AttrName_
        return param

    def get(self):
        """
        Функция получения значения.
        """
        ini_file_name = self._get_ini_file_name()
        settings_dict = inifunc.INI2Dict(ini_file_name)
        if self._cur_settings_list[1] in settings_dict:
            return settings_dict[self._cur_settings_list[1]]
        return None
    
    def set(self, value):
        """
        Функция сохранения значения.

        :param value: Сохраняемое значение.
        """
        if isinstance(value, dict):
            ini_file_name = self._get_ini_file_name()
            settings_dict = inifunc.INI2Dict(ini_file_name)
            settings_dict[self._cur_settings_list[1]] = value
            return inifunc.Dict2INI(settings_dict, ini_file_name, True)
        return None


class icParamDotUse(icSettingsDotUsePrototype):
    """
    Класс параметра файла настройки проекта. Для доступа к настройкам проекта через точку.
    """
    def __init__(self, DefaultSettingsList_=None):
        """
        Конструктор.
        """
        icSettingsDotUsePrototype.__init__(self, DefaultSettingsList_)

    def get(self):
        """
        Функция получения значения.
        ВНИМАНИЕ! Считается что внутри программы по умолчанию мы пользуемся
        юникодными строками, поэтому все строки автоматически приводим к юникоду.
        """
        ini_file_name = self._get_ini_file_name()
        value = inifunc.loadParamINI(ini_file_name, self._cur_settings_list[1], self._cur_settings_list[2])
        value = u'' if value is None else value
        # value = unicode(value, ini.DEFAULT_ENCODE) if isinstance(value, str) else value
        return value
    
    def set(self, value):
        """
        Функция сохранения значения.

        :param value: Сохраняемое значение.
        """
        ini_file_name = self._get_ini_file_name()
        return inifunc.saveParamINI(ini_file_name, self._cur_settings_list[1], self._cur_settings_list[2], value)

    def value(self):
        """
        Получить значение.
        ВНИМАНИЕ! Производиться попытка преобразования типа.

        :return:
        """
        str_value = self.get()
        # Пытаемся преобразовать тип
        try:
            value = eval(str_value)
        except:
            # log.fatal(u'Ошибка преобразования строки <%s> к типу' % str_value)
            value = str_value
        return value
