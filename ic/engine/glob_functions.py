#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль глобальных функций пользователя.

@var VAR_STORAGE: Глобальный объект ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
@var RUNNER_NAME: Имя ДВИЖКА по умолчанию.
"""

# Подключение библиотек и модулей
import sys
import os
import os.path
# import imp
import importlib.util

from ic.kernel import ickernel
from ic.log import log
from ic.kernel import icexceptions

from . import glob_variables
from ic.utils import ic_file

__version__ = (0, 1, 1, 2)


def getKernel():
    """
    Ядро системы. Он же движок.
    """
    return glob_variables.get_glob_var('KERNEL')


def getMetadata():
    """
    Метаданные системы.
    """
    return glob_variables.get_glob_var('metadata')


def getSchemas():
    """
    Схемы системы.
    """
    return glob_variables.get_glob_var('schemas')


def getSettings():
    """
    Настройки системы.
    """
    return glob_variables.get_glob_var('settings')


def letVar(name, data, security='*rw'):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Функция добавляет переменную/объект в хранилище.
    @param name: Имя переменной/объекта.
    @param data: Непосредственно данные.
    @param security: Строка защиты.
    """
    try:
        return getKernel().GetContext().Set(name, data)
    except:
        log.fatal()


def refVar(name):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Получить ссыылку на объект по его имени.
    @param name: Имя объекта.
    @return: Возвращает ссылку на объект или None, если нет такого объекта.
    """
    try:
        return getKernel().GetContext().Get(name)
    except:
        log.fatal()


def getVar(name, lock_key=None):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Получить копию объекта.
    @param name: Имя объекта.
    @param lock_key: Ключ блокировки.
    @return: Возвращает копию объекта не связанную с оригиналом
        или None, если нет такого объекта.
    """
    try:
        kernel = getKernel()
        if kernel:
            return kernel.GetContext().Get(name)
        else:
            log.warning(u'Не определено ядро системы для получения объекта <%s>' % name)
    except:
        log.fatal(u'Ошибка glob_functions.getVar NAME: <%s> KERNEL: <%s>' % (name, getKernel()))
    return None


def putVar(name, data, lock_key=None):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Сохранить объект.
    @param name: Имя объекта.
    @param data: Данные.
    @param lock_key: Ключ блокировки.
    @return: Возвращает результат выполнения операции (False или True).
    """
    try:
        return getKernel().GetContext().Set(name, data)
    except:
        log.fatal()


def delVar(name):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Удалить объект.
    @param name: Имя объекта.
    @return: Возвращает удаленный из хранилища объект.
    """
    try:
        return getKernel().GetContext().Del(name)
    except:
        log.fatal()


def isVar(name):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Функция проверяет усть ли объект в хранилище.
    @param name: Имя объекта.
    @return: Результат поиска (0/1).
    """
    try:
        return getKernel().GetContext().Is(name)
    except:
        log.fatal()


def printVarStorage():
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Вывести на консоль содержимое ХРАНИЛИЩА.
    """
    try:
        return getKernel().GetContext().Print()
    except:
        log.fatal(u'Ошибка glob_functions.printVarStorage <%s>' % getKernel().GetContext().__class__)

printEnvironmentTable = printVarStorage

# ФУНКЦИИ ДВИЖКА


def saveImports():
    """
    Сохранение имен импортированных модулей.
    """
    try:
        return getKernel().GetContext().saveImports()
    except:
        log.fatal()


def clearImports():
    """
    Удалить импортируемые во время работы модули из пространства имен.
    """
    try:
        return getKernel().GetContext().clearImports()
    except:
        log.fatal()


def refreshImports():
    """
    Обновить импортируемы модули.
    """
    try:
        return getKernel().GetContext().refreshImports()
    except:
        log.fatal()


def initEnv(prj_dirname, **environ):
    """
    Инициализация окружения по папке проекта.
    @param prj_dirname: Папка проекта.
    """
    try:
        # Подгрузить дополнительные атрибуты проекта
        from ic.prj import PrjRes
        prj_res_manager = PrjRes.icPrjRes()
        prj_dir = os.path.normpath(prj_dirname)
        prj_res_file_name = os.path.join(prj_dir, os.path.basename(prj_dir)+'.pro')
        if os.path.exists(prj_res_file_name):
            prj_res_manager.openPrj(prj_res_file_name)
            env_dict = prj_res_manager.getPrjEnv()
            environ.update(env_dict)
            log.info(u'Чтение дополнительных атрибутов проекта <%s> ... ОК' % prj_res_file_name)
        else:
            log.warning(u'Не найден файл проекта <%s>' % prj_res_file_name)
        return getKernel().GetContext().initEnv(prj_dirname, **environ)
    except:
        log.fatal(u'Ошибка glob_functions.initEnv')


def icLogin(username=None, password=None, db_mode='-s', **kwargs):
    """
    Основная запускаемая функция.
    """
    from . import icUser

    kernel = ickernel.createKernel()
    glob_variables.set_glob_var('KERNEL', kernel)
    initEnv(**kwargs)

    # Полное имя файла ресурса доступа к ресурсам
    users_file = icUser.DEFAULT_USERS_RES_FILE
    letVar('UserAccessFile', users_file)

    # Имя проекта
    letVar('PrjName', os.path.split(getVar('SYS_RES'))[1])

    # Установить операционный год
    setOperateYear()

    # залогиниться
    login_ok = kernel.Login(username, password, db_mode)
    if not login_ok:
        kernel.Logout()
    else:
        metadata = glob_variables.set_glob_var('metadata', kernel.GetContext()['metadata'])
        schemas = glob_variables.set_glob_var('schemas', kernel.GetContext()['schemas'])
        settings = glob_variables.set_glob_var('settings', kernel.GetContext()['settings'])

        import ic
        ic.metadata = metadata
        ic.schemas = schemas
        ic.settings = settings
        
        from ic.kernel import icsettings
        icsettings.setProjectSettingsToEnvironment()
    
        # Создать основные компоненты и ...
        kernel.run()

        # Запустить основной цикл
        kernel.MainLoop()
    return login_ok


def icEditorLogin(username=None, password=None, db_mode='-s', **kwargs):
    """
    Основная запускаемая функция.
    """
    from ic.engine import icapplication
    from . import icUser

    app = icapplication.icApp()

    kernel = ickernel.createEditorKernel()
    glob_variables.set_glob_var('KERNEL', kernel)
    initEnv(**kwargs)
    # Полное имя файла ресурса доступа к ресурсам
    users_file = icUser.DEFAULT_USERS_RES_FILE
    letVar('UserAccessFile', users_file)
    # Имя проекта
    letVar('PrjName', os.path.split(getVar('SYS_RES'))[1])
    login_result = kernel.Login(username, password, db_mode)

    metadata = glob_variables.set_glob_var('metadata', kernel.GetContext()['metadata'])
    schemas = glob_variables.set_glob_var('schemas', kernel.GetContext()['schemas'])
    settings = glob_variables.set_glob_var('settings', kernel.GetContext()['settings'])
    import ic
    ic.metadata = metadata
    ic.schemas = schemas
    ic.settings = settings

    from ic.kernel import icsettings
    icsettings.setProjectSettingsToEnvironment()
    
    return login_result


def closeMainWinForce():
    """
    Принудительное закрытие главного окна программы.
    ВНИМАНИЕ! Использовать только в начале обработчика
        инициализации главного окна.
        Иначе последствия могут быть не предсказуемыми.
    @return: True/False.
    """
    log.info(u'Принудительное закрытие главного окна программы')
    try:
        import wx

        app = wx.GetApp()
        main_win = app.GetTopWindow()
        main_win.Close(force=True)
        app.ExitMainLoop()
        return True
    except:
        log.fatal(u'Ошибка принудительного закрытия главного окна')
    return False


def closeAppForce():
    """
    Принудительное закрытие приложения.
    ВНИМАНИЕ! Использовать только в начале обработчика
        инициализации главного окна.
        Иначе последствия могут быть не предсказуемыми.
    @return: True/False.
    """
    log.info(u'Принудительное закрытие приложения')
    try:
        import wx

        app = wx.GetApp()
        app.ExitMainLoop()
        app.Destroy()
        return True
    except:
        log.fatal(u'Ошибка принудительного закрытия приложения')
    return False


def icLogout():
    """
    Останов.
    """
    kernel = glob_variables.get_glob_var('KERNEL')
    if kernel:
        # Закрыть главное окно
        kernel.Stop()
        glob_variables.set_glob_var('KERNEL', None)
    else:
        log.warning(u'Не определено ядро системы при останове. Принудительное закрытие главного окна.')

    glob_variables.set_glob_var('metadata', None)
    glob_variables.set_glob_var('schemas', None)
    glob_variables.set_glob_var('settings', None)

    return True


def getMainWin():
    """
    Определить главное окно системы.
    """
    try:
        return getKernel().GetContext().getMainWin()
    except:
        log.fatal()


def getMainOrg():
    """
    Определить главный органайзер.
    """
    try:
        return getKernel().GetContext().getMainOrg()
    except:
        log.fatal()


def getEngine():
    """
    Определить запущенный движок системы.
    """
    try:
        return getKernel()
    except:
        log.fatal()


def getPrjRoot():
    """
    Корневой объект дерева проекта.
    """
    try:
        kernel = getKernel()
        if kernel:
            kernel_prj_root = kernel.GetContext().getPrjRoot()
            if kernel_prj_root:
                log.info(u'Ядро <%s>\tПроект <%s>' % (kernel, kernel_prj_root))
                return kernel_prj_root
            else:
                log.warning(u'Не инициализирован проект в контексте ядра системы')
            # Берем из глобального контекста
            prj_root = getVar('PRJ_ROOT')
            if prj_root:
                return prj_root
            else:
                log.warning(u'Не инициализирован проек в хранилище/окружении системы')
        return None
    except:
        log.fatal(u'Ошибка определения корневого элемента дерева')


def addMainNotebookPage(page, title, bOpenExists=False, image=None, bCanClose=True,
                        open_script=None, close_script=None, default_page=-1):
    """
    Добавить в органайзер страницу.
    @param page: Страница (Наследник wxScrolledWindow).
    @param title: Строка-заголовок страницы.
    @param bOpenExists: Если такая страница уже существует, тогда открыть ее.
    @param default_page: Индекс страницы,  открываемой по умолчанию. Если -1,
        то открывается текущая добавляемая страница.
    """
    try:
        return getKernel().GetContext().getMainWin().addOrgPage(page, title, bOpenExists, image,
                                                                bCanClose, open_script, close_script, default_page)
    except:
        log.fatal()
    

addMainOrgPage = addMainNotebookPage


def delMainOrgPage(page_index):
    """
    Удалить из органайзера страницу.
    @param page_index: Индекс стриницы.
    """
    try:
        return getKernel().GetContext().getMainWin().delOrgPage(page_index)
    except:
        log.fatal()


def startDRPythonIDE(param=None):
    """
    Запуск drPython отдельной задачей.
    @param param: Параметры коммандной строки.
    """
    # Очистить параметры командной строки
    del sys.argv[1:]
    # Запуск приложения drPython
    import drpython
    app = drpython.DrApp(0)
    app.MainLoop()


def getDBResFile():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Функция возвращает путь к ресурсному файлу описания классов данных.
    """
    return getVar('DBResFile')


def getUserAccessFile():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Функция возвращает путь к ресурсному файлу доступа к ресурсам системы.
    """
    return getVar('UserAccessFile')


def getCurUserName():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Имя текущего зарегистрированного пользователя в системе.
    """
    return getVar('UserName')


def getCurUser():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Текущий зарегистрированный пользователь в системе.
    """
    return getKernel().GetAuthUser()


# Имена ролей администратооров
ADMINISTRATOR_ROLE_NAMES = ('admins', 'administrators', 'Admins', 'Administrators')


def isAdministrator(user=None, admin_role_names=ADMINISTRATOR_ROLE_NAMES):
    """
    Проверка является ли пользователь администратором.
    @param user: Проверяемый пользователь. Если None, то берется текущий пользователь.
    @param admin_role_names: Список имен ролей администраторов.
    @return: True/False. None - в случае ошибки.
    """
    if user is None:
        user = getCurUser()
    try:
        is_admin = [user.isRole(role_name) for role_name in admin_role_names]
        return any(is_admin)
    except:
        log.fatal(u'Ошибка проверки является ли пользователь <%s> администратором' % str(user))
    return None


def isAdministratorCurUser(admin_role_names=ADMINISTRATOR_ROLE_NAMES):
    """
    Проверка является ли текущий пользователь администратором системы.
    @param admin_role_names: Список имен ролей администраторов.
    @return: True/False.
    """
    return isAdministrator(admin_role_names=admin_role_names)


def get_res_name_list(*arg, **kwarg):
    """
    ФУНКЦИИ РАБОТЫ С ПРОЕКТОМ.
    Возвращает список ресурсов с заданным расширением.
    Подробнкее см. описание ф-ии getResNamesByTypes.
    """
    root = getPrjRoot()
    if root:
        return root.getResNamesByTypes(*arg, **kwarg)
    else:
        return []


def get_names_in_res(*arg, **kwarg):
    """
    ФУНКЦИИ РАБОТЫ С ПРОЕКТОМ.
    Возвращает список имен заданного типа в файлах с заданным расширение.
    Подробнкее см. описание ф-ии getObjNamesInResources.
    """
    root = getPrjRoot()
    if root:
        return root.getObjNamesInResources(*arg, **kwarg)
    else:
        return []


def get_names_in_res_by_types(*arg, **kwarg):
    """
    ФУНКЦИИ РАБОТЫ С ПРОЕКТОМ.
    Возвращает список имен заданного типа в файлах с заданным расширение.
    Подробнкее см. описание ф-ии getObjNamesInResourcesByTypes.
    """
    root = getPrjRoot()
    if root:
        return root.getObjNamesInResourcesByTypes(*arg, **kwarg)
    else:
        return []


def getPrjName():
    """
    Имя текущего проекта.
    Имя берем из окружения.
    """
    return getVar('PrjName')


def getObjManager(obj):
    """
    Менеджер объекта.
    @param obj: Объект.
    @return: Объект менеджера.
    """
    return obj.GetManager()


def getPrjDir():
    """
    Папка проекта. Берем из окружения.
    @return:  Путь до папки проекта.
    """
    return getVar('PRJ_DIR')


def getPrjPackage():
    """
    Так как папка проекта является пакетом Python,
    то можно получить объект пакета.
    @return: Объект пакета прикладного проекта.
    """
    prj_dir = getPrjDir()
    prj_name = getPrjName()

    if not prj_dir:
        log.warning(u'Не определена папка проекта для получения объекта пакета Python')
        return None
    if not prj_name:
        log.warning(u'Не определено имя проекта для получения объекта пакета Python')
        return None

    try:
        # return imp.load_package(prj_name, prj_dir)
        init_filename = os.path.join(prj_dir, '__init__.py')
        module_spec = importlib.util.spec_from_file_location(prj_name, init_filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
    except:
        log.fatal(u'Ошибка создания объекта пакета Python <%s> : <%s>' % (prj_name, prj_dir))
    return None


def saveOperateYear(year=None):
    """
    Сохранить значение операционного года в INI файле.
    @param year: Год.
    """
    if year is None:
        year = getOperateYear()

    from ic.utils import ini
    prj_path = ic_file.getPrjProfilePath()
    ini_basename = getPrjName() + '.ini'
    ini_filename = os.path.join(prj_path, ini_basename)
    ini.saveParamINI(ini_filename, 'SETTINGS', 'operate_year', year)


def setOperateYear(year=None):
    """
    Установить операционный год.
    @param year: Год.
        Если год не указан, то производится попытка
        прочитать его в INI файле проекта.
        Если в INI файле он не найде, то берется системный.
    """
    is_save = True
    if year is None:
        from ic.utils import ini
        prj_path = ic_file.getPrjProfilePath()
        ini_basename = getPrjName() + '.ini'
        ini_filename = os.path.join(prj_path, ini_basename)
        operate_year = ini.loadParamINI(ini_filename, 'SETTINGS', 'operate_year')
        if not operate_year:
            import datetime
            today = datetime.date.today()
            year = today.year
        else:
            year = int(operate_year)
            is_save = False
    letVar('OperateYEAR', year)
    if is_save:
        saveOperateYear(year)


def getOperateYear():
    """
    Получить операционный год.
    """
    return getVar('OperateYEAR')


def setSysYearAsOperate():
    """
    Установить системный год как операционный.
    """
    import datetime
    today = datetime.date.today()
    sys_year = today.year
    letVar('OperateYEAR', sys_year)
    saveOperateYear(sys_year)


def getReportManager():
    """
    Объект менеджера системы отчетов.
    @return: Объект менеджера системы отчетов.
    """
    from ic import report
    return report.REPORT_MANAGER


def getScanManager():
    """
    Объект менеджера системы сканирования.
    @return: Объект менеджера системы сканирования.
    """
    from ic import scanner
    return scanner.SCANNER_MANAGER
