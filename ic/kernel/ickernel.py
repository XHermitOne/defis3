#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Описание ядра системы.
"""

import _thread
import threading
import time

import ic.utils.impfunc
from . import icexceptions
from ic.log import log
from . import decorators
from . import icContext
from . import io_prnt
from .icbasekernel import icBaseKernel
from ic.utils import util

__version__ = (0, 2, 2, 1)

prs = None
resource = None


def import_sys_mod():
    global prs
    global resource

    if prs is None:
        import ic.components.icResourceParser as prs
        import ic.utils.resource as resource
        globals()['prs'] = prs
        globals()['resource'] = resource


# Функции
def get_res_interface(resName, className, extName, parent=None, subsys=None,
                      context=None, *arg, **kwarg):
    """
    Возвращает интерфейс ресурса.
    """
    if subsys:
        mod = '%s.%s' % (subsys, resName.replace('\\', '/').replace('/', '.'))
    else:
        mod = '%s' % resName.replace('\\', '/').replace('/', '.')

    exec('import %s' % mod)
    if className is None:
        className = eval('%s.ic_class_name' % (mod,))
    iclass = eval('%s.%s' % (mod, className))

    return iclass(parent, *arg, **kwarg)


def createEditorKernel():
    """
    Создание и регистрация ядра в режиме радактирования.
    """
    from ic.engine import glob_variables
    # Определить ядро
    kernel = glob_variables.set_glob_var('KERNEL', icKernel())
    log.info(u'[KERNEL] Создание ядра в режиме редактора <%s>' % kernel.context.__class__)
    return kernel


def createRuntimeKernel():
    """
    Создание и регистрация ядра в режиме ИСПОЛНЕНИЕ В СРЕДЕ GUI.
    """
    from ic.engine import icapplication
    from ic.engine import glob_variables
    # Определить ядро
    kernel = glob_variables.set_glob_var('KERNEL', icapplication.icApp())
    log.info(u'[KERNEL] Создание ядра в режиме ИСПОЛНЕНИЕ В СРЕДЕ GUI')
    return kernel


def createConsoleKernel():
    """
    Создание и регистрация ядра в режиме ИСПОЛНЕНИЕ В КОНСОЛЬНОЙ СРЕДЕ.
    """
    from ic.engine import glob_variables
    # Определить ядро
    kernel = glob_variables.set_glob_var('KERNEL', icKernel())
    log.info(u'[KERNEL] Создание ядра в режиме ИСПОЛНЕНИЕ В КОНСОЛЬНОЙ СРЕДЕ')
    return kernel


def createKernel(is_runtime_mode=None, is_console_mode=None, is_editor_mode=None):
    """
    Создать объект ядра.

    :param is_runtime_mode: Запуск ядра в режиме ИСПОЛНЕНИЕ В СРЕДЕ GUI?
        Если не определено, то берется из параметров коммандной строки <-run>
    :param is_console_mode: Запуск ядра в режиме ИСПОЛНЕНИЕ В КОНСОЛЬНОЙ СРЕДЕ?
        Если не определено, то берется из параметров коммандной строки <-cui>
    :param is_console_mode: Запуск ядра в режиме РЕДАКТОРА?
        Если не определено, то берется из параметров коммандной строки <-cfg>
    :return: Объект ядра системы.
    """
    from ic.utils import modefunc

    if is_runtime_mode is None:
        is_runtime_mode = modefunc.isRuntimeMode()

    if is_console_mode is None:
        is_console_mode = modefunc.isConsoleMode()

    if is_editor_mode is None:
        is_editor_mode = modefunc.isEditorMode()

    if is_runtime_mode:
        return createRuntimeKernel()
    elif is_console_mode:
        return createConsoleKernel()
    elif is_editor_mode:
        return createEditorKernel()
    else:
        log.error(u'[KERNEl] Ошибка создания объекта ядра. Не определен режим запуска.')
    return None


def getKernel():
    """
    Текущее ядро.
    """
    from ic.engine import glob_functions
    return glob_functions.getKernel()


# Классы ядра
DEFAULT_USER = 'admin'


class icKernel(icBaseKernel):
    """
    Класс ядра для работы с ресурсными объектами.
    """
    def __init__(self, context=None, *arg, **kwarg):
        """
        Конструктор.

        :param context: Контекст ядра.
        """
        # Текущий пользователь
        self._User = None
        icBaseKernel.__init__(self, context, *arg, **kwarg)

        # Объект управления ресурсами проекта
        self._prj_res_controller = None

    def add_connection_lst(self, lst):
        """
        Добавляет в список сигнальных соединений соединения.
        """
        if self.__connectionLst is None:
            self.__connectionLst = []

        self.__connectionLst += lst

    def parse_resource(self, parent, res, sizer=None, logType=0,
                       context=None, bCounter=True, progressDlg=None, **kwargs):
        """
        Низкоуровневый парсинг ресурса.
        """
        prs.icResourceParser(parent, res, sizer, logType, context,
                             bCounter=bCounter, progressDlg=progressDlg, **kwargs)

    @decorators.to_passport
    def getResByPsp(self, passport):
        """
        Возвращает ресурс объекта по его паспорту.

        :type passport: C{icObjectPassport}
        :param passport: идентификатор описания (паспорт) объекта.
        """
        return resource.getResByPsp(tuple(passport))

    @decorators.init_context
    @decorators.to_passport
    def createResObjByPsp(self, passport, context=None, parent=None, id=None, **kwarg):
        """
        Создает объект по ресурсa по паспорту.
        """
        res = self.getResByPsp(passport)
        if res:
            obj = prs.icBuildObject(parent, res, evalSpace=context, id=id)
        else:
            obj = None

        # Регистрируем объект
        if obj:
            resName, extName = passport.getDescrMod().split('.')
            self._reg_object(obj, resName)

        return obj

    @decorators.init_context
    def createObjByRes(self, resName, className, extName, parent=None, subsys=None,
                       context=None, **kwarg):
        """
        Создает объект по ресурсу. Depricated.

        :type resName: C{string}
        :param resName: Имя ресурса, по которому создается объект.
        :type className: C{string}
        :param className: Имя объекта.
        :type extName: C{string}
        :param extName: Расширения ресурсного файла для данного ресурса.
        :param parent: Родитель объекта (если необходим).
        :param context: Контекст.
        :return: Возвращает объект или None в случае ошибки.
        """
        if context is None:
            context = self.init_new_context()

        context.resFileName = '%s.%s' % (resName, extName)
        obj = prs.icCreateObject(resName, extName, parent=parent,
                                 context=context, className=className, **kwarg)
        # Регистрируем объект
        if obj:
            self._reg_object(obj, resName)
        return obj

    @decorators.init_context
    def createObjBySpc(self, parent, res, context=None, id=None):
        """
        Создает объект по ресурсному описанию.
        """
        if not res:
            log.error(u'ЯДРО. Не определен ресурс для создания объекта')
            return None

        obj = prs.icBuildObject(parent, res, evalSpace=context, id=id)
        if obj:
            resName = res['name']
            self._reg_object(obj, resName)
        return obj

    def createObjByClass(self, resName, className, extName, parent=None, subsys=None,
                         context=None, **kwarg):
        """
        Создает объект по питоновскому классу.
        """
        if subsys:
            mod = '%s.%s.py' % (subsys, resName.replace('\\', '/').replace('/', '.'))
        else:
            mod = '%s.py' % resName.replace('\\', '/').replace('/', '.')
        # Импортируем модуль
        exec(open(mod).read(), globals())
        # Создаем объект
        iclass = globals()[className]
        obj = iclass(parent, **kwarg).getObject()
        if obj:
            self._reg_object(obj, resName)
        return obj

    def CreateObj(self, resName, className, extName, subsys=None, parent=None,
                  context=None, *arg, **kwarg):
        """
        Функция создания объекта системы. Объекты системы делятся на два типа:
        1) объекты, создаваемые по ресурсному описанию.
        2) объекты, создаваемые по на основе Python класса.
        Если расширение файла ресурса 'py', то объект относится ко второму типу;
        все файлы с другими расширениями описывают объекты первого типа. Depricated.

        :type resName: C{string}
        :param resName: Имя файла ресурса.
        :type className: C{string}
        :param className: Имя ресурса(класса).
        :type extName: C{string}
        :param extName: Расширение файла ресурса (frm, tab, acc, mtd, py).
            Расширение задает тип ресурса.
        :rtype: C{icObject}
        :return: Возвращает созданный объект.
        """
        if extName == 'py':
            return self.createObjByClass(resName, className, extName, parent, subsys, context=context, **kwarg)
        else:
            return self.createObjByRes(resName, className, extName, parent, subsys, context=context, **kwarg)

    @decorators.init_context
    @decorators.to_passport
    def Create(self, passport, parent=None, context=None, *arg, **kwarg):
        """
        Функция создания объекта системы. Объекты системы делятся на два типа:
        1) объекты, создаваемые по ресурсному описанию.
        2) объекты, создаваемые на основе Python класса.
        Если расширение файла ресурса 'py', то объект относится ко второму типу;
        все файлы с другими расширениями описывают объекты первого типа.

        :type passport: C{icObjectPassport}
        :param passport: идентификатор описания (паспорт) объекта.
        :type parent: C{wx.Window}
        :param parent: Родительское окно.
            Расширение задает тип ресурса.
        :rtype: C{icObject}
        :return: Возвращает созданный объект.
        """
        objType = passport.getDescrType()
        className = passport.getDescrName()
        resName, extName = passport.getDescrMod().split('.')
        subsys = passport.getDescrSubsys()

        #   Картинки создаются отдельно
        if extName == 'py' and objType in ('wx.StaticBitmap', 'wxStaticBitmap'):
            path = resource.icGetSysPath()
            path = '%s/%s/%s' % (path, subsys, passport.getDescrMod())
            # Импортируем модуль
            mod = self.load_source(resName, path)
            # Создаем объект
            if hasattr(mod, className):
                log.info(u'Изображение <%s> загружено из библиотеке образов <%s>' %
                         (className, passport.getDescrMod()))
                return getattr(mod, className)
            else:
                log.warning(u'Изображение <%s> в библиотеке образов <%s> не найдено' %
                            (className, passport.getDescrMod()))
        elif extName == 'py':
            return self.createObjByClass(resName, className, extName, parent, subsys, context=context, **kwarg)
        # Ставим жесткое условие - объект по куску ресурса можно получить только у метаданных
        elif objType and className and extName == 'mtd':
            return self.createResObjByPsp(passport, context, parent)
        else:
            return self.createObjByRes(resName, className, extName, parent, subsys, context=context, **kwarg)

    def findSlotLstBySignal(self, signal):
        """
        Ищем в списке соединений по сигналу список соответствующих слотов.
        """
        pass

    def GetConnectionLst(self):
        """
        Возвращает список активированных соединений.
        """
        return self.__connectionLst

    def getConnectionByObject(self, obj):
        """
        Возвращает списки соединение, в которых объект выступает в качестве
        источнока, в качестве приемника.

        :type obj: C{icObject}
        :param obj: Объект.
        :rtype: C{tuple}
        :return: (srcLst, slotLst). srcLst - список соединений где объект прописан
        как источник; slotLst - список соединений где объект прописан как приемник.
        """
        srcConLst = []
        slotConLst = []
        lst = self.GetConnectionLst()
        if lst:
            for con in lst:
                # Проверяем источники
                if con.src.passport == obj.GetPassport():
                    srcConLst.append(con)
                # Проверяем слоты
                for slot in con.slotLst:
                    if slot.passport == obj.GetPassport():
                        slotConLst.append(con)
        return srcConLst, slotConLst

    def getProjectResController(self):
        """
        Возвращает указатель на объект управления ресурсами проекта.
        """
        if self._prj_res_controller is None:
            from ic.prj import ctrlPrj
            self._prj_res_controller = ctrlPrj.icProjectResManager()
        return self._prj_res_controller

    # Другое название метода
    getProjectResManager = getProjectResController

    def GetMetadata(self):
        """
        Возвращает указатель на объект метоописания.
        """
        return self.context.GetObject('metadata')

    def init_object(self):
        """
        Инициализируем ядро.
        """
        #   Список соединений сигналов
        self.__connectionLst = None
        # Устанавливаем указатель на ядро
        self.context.kernel = self
        # Добавляем функцию
        # Грузим компоненты
        import_sys_mod()
        #   Запускаем цикл обработки сигналов
        # количеств обрабатываемых сигналов за один раз
        self.num_parse_signal = 10
        self.start_signal_loop()

    def init_connection_lst(self, lst=None):
        """
        Инициализация списка сигнальных соединений.
        """
        if lst:
            self.__connectionLst = lst
        else:
            self.__connectionLst = []

    def init_new_context(self, prnt_context=None):
        """
        Создает новый контекст объекта.

        :type prnt_context: C{icContext.Context}
        :param prnt_context: Родитнльский контекст.
        """
        context = icContext.Context(self)
        if prnt_context:
            context.SetParentContext(prnt_context)
        else:
            context.SetParentContext(self.GetContext())

        return context

    def Login(self, username, password, *arg, **kwarg):
        """
        Функция регистрации пользователя.
        """
        try:
            login_result = self._login_loop(username, password, *arg, **kwarg)
        except:
            self.Logout()
            raise

        io_prnt.SetUserLog(username, self)
        return login_result

    def _login_loop(self, username=None, password=None, db_mode='-s'):
        """
        Цикл входа в систему.

        :param username: Имя пользователя.
        :param password: Пароль.
        :param db_mode: Режим использования БД.
        """
        from ic.dlg import dlgfunc
        from ic.engine import user_manager

        login_ok = False
        login_manager = user_manager.icLoginManager()
        username, password = login_manager._getAutoLogin(username, password)
        bAuto = login_manager.isAutoAuth()
        while not login_ok:
            user_data = login_manager.Login(username, password, db_mode,
                                            bRuntimeMode=False)
            if user_data is None:
                break
            user_name = user_data[dlgfunc.LOGIN_USER_IDX]
            user_password = user_data[dlgfunc.LOGIN_PASSWORD_IDX]
            user_password_md5 = user_data[dlgfunc.LOGIN_PASSWORD_MD5_IDX]
            res = login_manager.getUserResource(user_name)

            if res is None:
                username, password = None, None
                dlgfunc.openMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
            else:
                self._User = self.createObjBySpc(None, res)
                self._User.setLoginManager(login_manager)
                passwd_crc = self._User._get_password_crc(user_password)
                try:
                    login_ok = self._User.login_ok(user_name, user_password, passwd_crc,
                                                   db_mode, bRuntimeMode=False)
                except icexceptions.LoginInvalidException:
                    if bAuto:
                        bAuto = False
                        username, password = None, None
                        dlgfunc.openMsgBox(u'Вход в систему', u'Неправильный пользователь или пароль. Доступ запрещен.')
                    else:
                        raise

        return login_ok

    def GetAuthUser(self):
        """
        Возвращает текущего авторизированного пользователя.
        """
        return self._User

    def Logout(self):
        """
        Выход.
        """
        logout_result = False
        if self.context:
            self.context._destroyEnv()
        if self._User:
            logout_result = self._User.logout_ok()
            self._User = None

        return logout_result

    def Stop(self):
        """
        Остановка.
        """
        self.stop()
        return self.Logout()

    def load_source(self, name, path):
        """
        Возвращает загруженный модуль.

        :type name: C{string}
        :param name: Имя модуля.
        :type path: C{string}
        :param path: Полный путь до модуля.
        """
        return ic.utils.impfunc.loadSource(name=name, path=path)

    def post_signal(self, signal, slotLst=None):
        """
        Сигнал ставится в очередь сигналов.
        """
        for slot in slotLst:
            if slot and slot.isValidSignal(signal):
                self._append_loop_lst(signal, slot)
            else:
                log.warning(u'Сигнал  <%s> не соответствует слоту <%s>.' % (signal, slot))
        return True

    def send_signal(self, signal, slotLst=None):
        """
        Обработка сигнала в обход очереди.
        """
        # По слоту находим реальный объект
        for slot in slotLst:
            if slot and slot.isValidSignal(signal):
                slot.parse_signal(signal)
        return True

    def _append_loop_lst(self, signal, slot):
        """
        Добавляем сигнал в очередь.
        """
        if not self._eventLoopLst.isSet():
            self._eventLoopLst.wait(0.5)
        if not self._eventLoopLst.isSet():
            log.warning(u'Очередь сигналов заблокирована. сигнал: %s' % signal)
            return False
        else:
            # Блокируем список
            self._eventLoopLst.clear()
            self.loopLst.append((signal, slot))
            # Снимаем блокировку
            self._eventLoopLst.set()

        return True

    def _parse_signal_lst(self):
        """
        Разбираем очередь сообщений.
        """
        try:
            # Блокируем очередь
            num = min(len(self.loopLst), self.num_parse_signal)
            for i in range(num):
                sign, slot = self.loopLst[i]
                if slot and slot.isValidSignal(sign):
                    if sign.isSkip():
                        slot.parse_signal(sign)
            # Блокируем очередь
            self._eventLoopLst.clear()
            self.loopLst = self.loopLst[num:]
            # Снимаем блокировку с очереди
            self._eventLoopLst.set()
        except:
            log.fatal(u'Ошибка парсинга очереди сообщений')
            pass

    def run(self, mainwin_psp=None, menubars_psp=None):
        """
        Запуск движка.

        :param mainwin_psp: Паспорт главного окна.
        :param menubars_psp: Список паспортов горизонтальных меню.
        :return: Возвращает True, если все OK иначе - False.
        """
        pass

    def stop(self):
        """
        Функция останавливает второй поток.
        """
        log.info(u'*** STOP KERNEL EVENT LOOP ****')
        if self._eventLoopLst:
            while 1:
                if self._eventLoopLst.isSet():
                    # Блокируем очередь
                    self._eventLoopLst.clear()
                    self.__stop = True
                    # Снимаем блокировку с очереди
                    self._eventLoopLst.set()
                    break
                else:
                    self._eventLoopLst.wait(0.5)

    def signal_loop(self, *warg):
        """
        Диспетчер сигналов.
        """
        try:
            return self._signal_loop(*warg)
        except:
            log.fatal(u'Ошибка диспетчера сигналов')

    def _signal_loop(self, *warg):
        """
        Диспетчер сигналов.
        """
        while True:
            # Обрабатываем очередь
            if not self._eventLoopLst.isSet():
                # Ждем 5 сек, если очередь занята
                self._eventLoopLst.wait(0.5)
                if not self._eventLoopLst.isSet():
                    log.warning(u'Диспетчер ядра не может получить доступ к очереди сигналов.')
                else:
                    #   Если установлен признак остановки, то выходим из цикла
                    if self.__stop:
                        break
                    self._parse_signal_lst()
            else:
                #   Если установлен признак остановки, то выходим из цикла
                if self.__stop:
                    break
                self._parse_signal_lst()
            try:
                time.sleep(0.001)
            except:
                log.error(u'*** EXCEPTION time.sleep(0.001) ***')
                break

    def start_signal_loop(self):
        """
        Start.
        """
        self.loopLst = []
        # isSet = True - очередь свободна; False - занята
        self._eventLoopLst = threading.Event()
        self._eventLoopLst.set()
        self.__stop = False
        self._loopThread = _thread.start_new(self.signal_loop, (0,))

    def setBehaviour(self, behaviour_res_filename):
        """
        Установить поведение системы.

        :param behaviour_res_filename: Имя файла ресурса со связями.
        """
        pass

    def getObjectByPsp(self, psp):
        """
        Получить зарегистрированный объект по паспорту.

        :param psp: Паспорт объекта.
        :return: Искомый объект или None, если не найден.
        """
        name = psp[0][1]
        obj = self.getObject(name)
        if obj is None:
            # Объект не найден, можно пропробовать создать
            try:
                obj = self.Create(psp)
            except:
                log.fatal(u'Ошибка создания объекта по паспорту %s' % str(psp))
        return obj
