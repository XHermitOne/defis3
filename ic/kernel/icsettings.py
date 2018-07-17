#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Поддержка доступа к настройке проекта системы через точку.
Внешние настройки проекта храняться в *.ini файле проекта:
../<Project Dir>/<Project Name>/<Project Name>.ini
"""

# Подключение библиотек
from ic.utils import ic_mode
from ic.utils import ini
from ic.utils import ic_file
from ic.utils import ic_exec
from ic.engine import ic_user
from . import io_prnt

__version__ = (0, 0, 1, 2)


def setProjectSettingsToEnvironment(ProjectName_=None, ReDefine_=False):
    """
    Добавить все переменные из *.ini файла в окружение системы.
    @param ProjectName_: Имя проекта. Если None, то берется
    текущий проект.
    @param ReDefine_: Переопределять переменные в окружении?
    @return: True/False.
    """
    prj_settings = None
    if ic_user.getSettings() is None:
        if ic_mode.isDebugMode():
            io_prnt.outLog(u'Не определена переменная настроек проекта.')
        prj_dir = ic_user.icGet('PRJ_DIR')
        prj_name = ic_user.icGet('PrjName')
        if prj_dir and prj_name:
            prj_ini_file_name = prj_dir+'/'+prj_name+'.ini'
            prj_settings = ini.INI2Dict(prj_ini_file_name)
    else:    
        if ProjectName_ is None:
            prj_settings = ic_user.getSettings().THIS.get()
        else:
            prj_settings = getattr(ic_user.getSettings(), ProjectName_).get()
            
    if prj_settings:
        for section_name, section in prj_settings.items():
            for param, value in section.items():
                if ic_user.icIs(param):
                    io_prnt.outLog(u'Переменная %s уже определена в окружении' % param)
                    if ReDefine_:
                        ic_user.icLet(param, value)
                        io_prnt.outLog(u'Переменная %s переопределена в окружении' % param)
                else:
                    ic_user.icLet(param, value)
        if ic_mode.isDebugMode():
            ic_user.icPrintStore()            
        return True
    return False
    

class icSettingsDotUsePrototype(object):
    """
    Класс поддержки доступа к настройкам проекта.
    """

    def __init__(self, DefaultSettingsList_=None):
        """
        Консруктор.
        @param DefaultSettingsList_: Передающийся по точке список указания 
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
        prj_dir = ic_user.icGet('PRJ_DIR')
        if prj_dir:
            ini_file_name = prj_dir+'/'+self._cur_settings_list[0]+'.ini'
        else:
            prj_name = self._cur_settings_list[0]
            ini_file_name = ic_file.DirName(ic_file.DirName(ic_file.DirName(__file__)))+'/%s/%s/%s.ini' % (prj_name, prj_name, prj_name)
        return ini_file_name
    
    def get(self):
        """
        Функция получения значения.
        """
        return None
    
    def set(self, value):
        """
        Функция сохранения значения.
        @param value: Сохраняемое значение.
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
            prj._cur_settings_list[0] = ic_user.icGet('PrjName')
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
        return ini.INI2Dict(ini_file_name)
    
    def set(self, value):
        """
        Функция сохранения значения.
        @param value: Сохраняемое значение.
        """
        if isinstance(value, dict):
            ini_file_name = self._get_ini_file_name()
            return ini.Dict2INI(value, ini_file_name, True)
        return None

    def edit(self):
        """
        Запуск редактирования INI файла настроек
        """
        ini_file_name = self._get_ini_file_name()
        if ic_file.Exists(ini_file_name):
            cmd = 'gedit %s &' % ini_file_name
            ic_exec.icSysCmd(cmd)
        else:
            io_prnt.outWarning(u'INI файл <%s> не найден' % ini_file_name)


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
        settings_dict = ini.INI2Dict(ini_file_name)
        if self._cur_settings_list[1] in settings_dict:
            return settings_dict[self._cur_settings_list[1]]
        return None
    
    def set(self, value):
        """
        Функция сохранения значения.
        @param value: Сохраняемое значение.
        """
        if isinstance(value, dict):
            ini_file_name = self._get_ini_file_name()
            settings_dict = ini.INI2Dict(ini_file_name)
            settings_dict[self._cur_settings_list[1]] = value
            return ini.Dict2INI(settings_dict, ini_file_name, True)
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
        value = ini.loadParamINI(ini_file_name, self._cur_settings_list[1], self._cur_settings_list[2])
        value = u'' if value is None else value
        value = unicode(value, ini.DEFAULT_ENCODE) if isinstance(value, str) else value
        return value
    
    def set(self, value):
        """
        Функция сохранения значения.
        @param value: Сохраняемое значение.
        """
        ini_file_name = self._get_ini_file_name()
        return ini.saveParamINI(ini_file_name, self._cur_settings_list[1], self._cur_settings_list[2], value)
