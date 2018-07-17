#!/usr/bin/env python
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
import imp
from ic.kernel import ickernel
from ic.log import log
from ic.kernel import icexceptions

from . import glob
from ic.utils import ic_file

__version__ = (0, 0, 3, 2)


def getKernel():
    """
    Ядро системы. Он же движок.
    """
    return glob.get_glob_var('KERNEL')


def getMetadata():
    """
    Метаданные системы.
    """
    return glob.get_glob_var('metadata')


def getSchemas():
    """
    Схемы системы.
    """
    return glob.get_glob_var('schemas')


def getSettings():
    """
    Настройки системы.
    """
    return glob.get_glob_var('settings')


def icLet(Name_, Data_, Security_='*rw'):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Функция добавляет переменную/объект в хранилище.
    @param Name_: Имя переменной/объекта.
    @param Data_: Непосредственно данные.
    @param Security_: Строка защиты.
    """
    try:
        return getKernel().GetContext().Set(Name_, Data_)
    except:
        log.fatal()


def icRef(Name_):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Получить ссыылку на объект по его имени.
    @param Name_: Имя объекта.
    @return: Возвращает ссылку на объект или None, если нет такого объекта.
    """
    try:
        return getKernel().GetContext().Get(Name_)
    except:
        log.fatal()


def icGet(Name_, LockKey_=None):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Получить копию объекта.
    @param Name_: Имя объекта.
    @param LockKey_: Ключ блокировки.
    @return: Возвращает копию объекта не связанную с оригиналом
        или None, если нет такого объекта.
    """
    try:
        kernel = getKernel()
        if kernel:
            return kernel.GetContext().Get(Name_)
        else:
            log.warning(u'Не определено ядро системы для получения объекта <%s>' % Name_)
    except:
        log.fatal(u'Ошибка ic_user.icGet NAME: <%s> KERNEL: <%s>' % (Name_, getKernel()))
    return None


def icPut(Name_, Data_, LockKey_=None):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Сохранить объект.
    @param Name_: Имя объекта.
    @param Data_: Данные.
    @param LockKey_: Ключ блокировки.
    @return: Возвращает результат выполнения операции (False или True).
    """
    try:
        return getKernel().GetContext().Set(Name_, Data_)
    except:
        log.fatal()


def icDel(Name_):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Удалить объект.
    @param Name_: Имя объекта.
    @return: Возвращает удаленный из хранилища объект.
    """
    try:
        return getKernel().GetContext().Del(Name_)
    except:
        log.fatal()


def icIs(Name_):
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Функция проверяет усть ли объект в хранилище.
    @param Name_: Имя объекта.
    @return: Результат поиска (0/1).
    """
    try:
        return getKernel().GetContext().Is(Name_)
    except:
        log.fatal()


def icPrintStore():
    """
    ФУНКЦИИ ХРАНИЛИЩА ПЕРЕМЕННЫХ И ОБЪЕКТОВ.
    Вывести на консоль содержимое ХРАНИЛИЩА.
    """
    try:
        return getKernel().GetContext().Print()
    except:
        log.fatal(u'Ошибка ic_user.icPrintStore <%s>' % getKernel().GetContext().__class__)

printEnvironmentTable = icPrintStore

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


def InitEnv(PrjDir_, **environ):
    """
    Инициализация окружения по папке проекта.
    @param PrjDir_: Папке проекта.
    """
    try:
        # Подгрузить дополнительные атрибуты проекта
        from ic.prj import PrjRes
        prj_res_manager = PrjRes.icPrjRes()
        prj_dir = ic_file.NormPathUnix(PrjDir_)
        prj_res_file_name = os.path.join(prj_dir, ic_file.BaseName(prj_dir)+'.pro')
        if os.path.exists(prj_res_file_name):
            prj_res_manager.openPrj(prj_res_file_name)
            env_dict = prj_res_manager.getPrjEnv()
            environ.update(env_dict)
            log.info(u'Чтение дополнительных атрибутов проекта <%s> ... ОК' % prj_res_file_name)
        else:
            log.warning(u'Не найден файл проекта <%s>' % prj_res_file_name)
        return getKernel().GetContext().initEnv(PrjDir_, **environ)
    except:
        log.fatal(u'Ошибка ic_user.InitEnv')


def icLogin(User_=None, Password_=None, DBMode_='-s', **kwargs):
    """
    Основная запускаемая функция.
    """
    from . import icUser

    kernel = ickernel.createKernel()
    glob.set_glob_var('KERNEL', kernel)
    InitEnv(**kwargs)

    # Полное имя файла ресурса доступа к ресурсам
    users_file = icUser.DEFAULT_USERS_RES_FILE
    icLet('UserAccessFile', users_file)

    # Имя проекта
    icLet('PrjName', ic_file.Split(icGet('SYS_RES'))[1])

    # Установить операционный год
    setOperateYear()

    # залогиниться
    login_ok = kernel.Login(User_, Password_, DBMode_)
    if not login_ok:
        kernel.Logout()
    else:
        metadata = glob.set_glob_var('metadata', kernel.GetContext()['metadata'])
        schemas = glob.set_glob_var('schemas',  kernel.GetContext()['schemas'])
        settings = glob.set_glob_var('settings', kernel.GetContext()['settings'])

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


def icEditorLogin(User_=None, Password_=None, DBMode_='-s', **kwargs):
    """
    Основная запускаемая функция.
    """
    from ic.engine import icApp
    from . import icUser

    app = icApp.icApp()

    kernel = ickernel.createEditorKernel()
    glob.set_glob_var('KERNEL', kernel)
    InitEnv(**kwargs)
    # Полное имя файла ресурса доступа к ресурсам
    users_file = icUser.DEFAULT_USERS_RES_FILE
    icLet('UserAccessFile', users_file)
    # Имя проекта
    icLet('PrjName', ic_file.Split(icGet('SYS_RES'))[1])
    login_result = kernel.Login(User_, Password_, DBMode_)

    metadata = glob.set_glob_var('metadata', kernel.GetContext()['metadata'])
    schemas = glob.set_glob_var('schemas', kernel.GetContext()['schemas'])
    settings = glob.set_glob_var('settings', kernel.GetContext()['settings'])
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
    kernel = glob.get_glob_var('KERNEL')
    if kernel:
        # Закрыть главное окно
        kernel.Stop()
        glob.set_glob_var('KERNEL', None)
    else:
        log.warning(u'Не определено ядро системы при останове. Принудительное закрытие главного окна.')

    glob.set_glob_var('metadata', None)
    glob.set_glob_var('schemas', None)
    glob.set_glob_var('settings', None)

    return True


def getMainWin():
    """
    Определить главное окно системы.
    """
    try:
        return getKernel().GetContext().getMainWin()
    except:
        log.fatal()


icGetMainWin = getMainWin


def icGetMainOrg():
    """
    Определить главный органайзер.
    """
    try:
        return getKernel().GetContext().getMainOrg()
    except:
        log.fatal()


def icGetRunner():
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
                log.info(u'KERNEL: <%s>\tPROJECT: <%s>' % (kernel, kernel_prj_root))
                return kernel_prj_root
            else:
                log.warning(u'Не инициализирован проект в контексте ядра системы')
            # Берем из глобального контекста
            prj_root = icGet('PRJ_ROOT')
            if prj_root:
                return prj_root
            else:
                log.warning(u'Не инициализирован проек в хранилище/окружении системы')
        return None
    except:
        log.fatal(u'Ошибка определения корневого элемента дерева')


def addMainNotebookPage(Page_, Title_, OpenExists_=False, Image_=None,
                        CanClose_=True, OpenScript_=None, CloseScript_=None, DefaultPage_=-1):
    """
    Добавить в органайзер страницу.
    @param Page_: Страница (Наследник wxScrolledWindow).
    @param Title_: Строка-заголовок страницы.
    @param OpenExists_: Если такая страница уже существует, тогда открыть ее.
    @param DefaultPage_: Индекс страницы,  открываемой по умолчанию. Если -1,
        то открывается текущая добавляемая страница.
    """
    try:
        return getKernel().GetContext().getMainWin().AddOrgPage(Page_, Title_, OpenExists_, Image_,
                                                                CanClose_, OpenScript_, CloseScript_, DefaultPage_)
    except:
        log.fatal()
    

icAddMainOrgPage = addMainNotebookPage


def icDelMainOrgPage(Index_):
    """
    Удалить из органайзера страницу.
    @param Index_: Индекс стриницы.
    """
    try:
        return getKernel().GetContext().getMainWin().DelOrgPage(Index_)
    except:
        log.fatal()


def StartDRPython(Param_=None):
    """
    Запуск drPython отдельной задачей.
    @param Param_: Параметры коммандной строки.
    """
    # Очистить параметры командной строки
    del sys.argv[1:]
    # Запуск приложения drPython
    import drpython
    app = drpython.DrApp(0)
    app.MainLoop()


def icGetDBResFile():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Функция возвращает путь к ресурсному файлу описания классов данных.
    """
    return icGet('DBResFile')


def icGetUserAccessFile():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Функция возвращает путь к ресурсному файлу доступа к ресурсам системы.
    """
    return icGet('UserAccessFile')


def getCurUserName():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Имя текущего зарегистрированного пользователя в системе.
    """
    return icGet('UserName')


def getCurUser():
    """
    ФУНКЦИИ РАБОТЫ С ДАННЫМИ.
    Текущий зарегистрированный пользователь в системе.
    """
    return getKernel().GetAuthUser()


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
    return icGet('PrjName')


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
    return icGet('PRJ_DIR')


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
        return imp.load_package(prj_name, prj_dir)
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
    icLet('OperateYEAR', year)
    if is_save:
        saveOperateYear(year)


def getOperateYear():
    """
    Получить операционный год.
    """
    return icGet('OperateYEAR')


def setSysYearAsOperate():
    """
    Установить системный год как операционный.
    """
    import datetime
    today = datetime.date.today()
    sys_year = today.year
    icLet('OperateYEAR', sys_year)
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
