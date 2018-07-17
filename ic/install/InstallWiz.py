#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль классов визарда создания инсталяционного пакета проекта.
"""

# --- Подключение библиотек ---
import os
import os.path
import wx.wizard as wizard

import ic.dlg.ic_dlg as ic_dlg
import ic.utils.ic_file as ic_file
from ic.utils import ini
import ic.utils.ic_util as ic_util
from ic.kernel import io_prnt
import ic.utils.ic_exec as ic_exec
import ic.imglib.common as imglib

__version__ = (0, 0, 1, 2)


class PrjInstallMaker:
    """
    Инсталятор проекта.
    """

    def __init__(self, PrjDir_):
        """
        Конструктор.
        @param PrjDir_: Папка проекта.
        """
        self._prj_dir = None
        # Имя файла настроек/параметров проекта
        self._prj_ini_file_name = None

        self.setPrj(PrjDir_)

    def setPrj(self, PrjDir_):
        """
        Определить проект для создания инсталяционного пакета.
        @param PrjDir_: Папка проекта.
        """
        self._prj_dir = PrjDir_
        # Имя файла настроек/параметров проекта
        if self._prj_dir:
            self._prj_ini_file_name = self._prj_dir+'/%s.ini' % (os.path.basename(self._prj_dir))

    def getPrjName(self):
        """
        Имя проекта/имя папки проекта.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_name')

    def setPrjName(self, PrjName_):
        """
        Имя проекта/имя папки проекта.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_name', PrjName_)

    def readPrjVersion(self):
        """
        Версия проекта.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'version')
        
    def getPrjVersion(self):
        """
        Версия проекта.
        """
        version = self.readPrjVersion()
        if self.getAutoVer():
            ver_lst = str(version).split('.')
            ver_lst = ver_lst[:-1]+[str(int(ver_lst[-1])+1)]
            version = '.'.join(ver_lst)
        return version

    def setPrjVersion(self, Version_):
        """
        Версия проекта.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'version', Version_)

    def getPrjIcon(self):
        """
        Иконка.
        """
        ico_file = ini.loadParamINI(self._prj_ini_file_name,
                                    'INSTALL', 'prj_icon')
        if ico_file:
            return ic_file.NormPathWin(ico_file)
        return ico_file

    def setPrjIcon(self, ICOFileName_):
        """
        Иконка.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_icon', ICOFileName_)

    def getPrjTitle(self):
        """
        Заголовок проекта в инсталяторе.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_title')

    def setPrjTitle(self, PrjTitle_):
        """
        Заголовок проекта в инсталяторе.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_title', PrjTitle_)

    def getPrjAuthor(self):
        """
        Автор.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_author')

    def setPrjAuthor(self, PrjAuthor_):
        """
        Автор.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_author', PrjAuthor_)

    def getPrjCopyright(self):
        """
        Права.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_copyright')

    def setPrjCopyright(self, PrjCopyright_):
        """
        Права.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'prj_copyright', PrjCopyright_)

    def getOpenSource(self):
        """
        Признак добавления в инсталяционный пакет исходников.
        """
        open_src_txt = ini.loadParamINI(self._prj_ini_file_name,
                                        'INSTALL', 'open_src')
        if open_src_txt:
            return eval(open_src_txt)
        return True

    def setOpenSource(self,MakeOpenSource_):
        """
        Признак добавления в инсталяционный пакет исходников.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'open_src', str(MakeOpenSource_))

    def getAutoVer(self):
        """
        Признак автоматического изменения версий.
        """
        auto_ver = ini.loadParamINI(self._prj_ini_file_name,
                                    'INSTALL', 'auto_ver')
        if auto_ver:
            return eval(auto_ver)
        return False

    def setAutoVer(self,MakeAutoVer_):
        """
        Признак автоматического изменения версий.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'auto_ver', str(MakeAutoVer_))
            
    def getPackages(self):
        """
        Список добавляемых пакетов.
        """
        packages = ini.loadParamINI(self._prj_ini_file_name,
                                    'INSTALL', 'packages')
        if packages:
            return eval(packages)
        return []

    def setPackages(self,Packages_):
        """
        Признак добавления в инсталяционный пакет исходников.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'packages', str(Packages_))

    def getInstallMaker(self):
        """
        Программа компиляции скрипта инсталяционного пакета.
        """
        install_maker = ini.loadParamINI(self._prj_ini_file_name,
                                         'INSTALL', 'install_maker')
        if install_maker:
            return ic_file.NormPathWin(install_maker)
        return install_maker

    def setInstallMaker(self,InstallMaker_):
        """
        Программа компиляции скрипта инсталяционного пакета.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'install_maker', InstallMaker_)

    def installScript(self):
        """
        Создание скрипта инсталяционного пакета проекта.
        """
        pass

    def makeInstallPackage(self):
        """
        Создание инсталяционного пакета.
        """
        pass

# Шаблон для скрипта инсталятора Nullsoft Install System
_NSISScriptTemplate = '''; setup.nsi
; Наименование инсталятора
Name '%s %s %s'

;Установить иконку
Icon '%s'

;Файл инсталяции
OutFile 'setup.exe'

; Инсталяционная директория
InstallDir $PROGRAMFILES\\%s

;Ключ реестра для проверки директории (если вы инсталлируете снова,  то
;старые файлы будут заменены новыми автоматически)
InstallDirRegKey HKLM SOFTWARE\\%s 'Install_Dir'

; 
ComponentText 'Инсталяция программы %s на ваш компьютер.'

; Текст для выбора папки инсталяции
DirText 'Выбирите папку для инсталяции:'

; --- Обязательные пакеты ---
  
%s

Section 'Прикладная система %s'
    ;Set output path to the installation directory.
    SetOutPath $INSTDIR
    
    ExecWait '$EXEDIR\\package\\%s.exe'
    
    #Отредактировать run.bat 
    FileOpen $0 '$INSTDIR\\run.bat' 'w'
    FileWrite $0 'run.py -run \'$INSTDIR/%s/%s/\' -s'
    FileClose $0
    
    ;Копировать иконку в инсталляционную папку
    CopyFiles '%s' $INSTDIR
    ;Создать ярлык на рабочем столе 
    CreateShortCut '$DESKTOP\\%s.lnk' '$INSTDIR\\run.bat' '' '$INSTDIR\\%s' 
SectionEnd

;Деинсталятор
UninstallText 'Деинсталяция системы %s. Нажмите Next для продолжения.'

Section 'Uninstall'
    ;remove registry keys
    DeleteRegKey HKLM SOFTWARE\\%s

    ; remove files and uninstaller
    Delete $INSTDIR\\*.*

    ; remove directories used
    RMDir '$INSTDIR'
SectionEnd
'''

_NSISSectionTemplateEXE = '''
Section '%s'
    ExecWait '$EXEDIR\\package\\%s'
SectionEnd
'''

_NSISSectionTemplateMSI = '''
Section '%s'
    ExecWait ''msiexec.exe' /i '$EXEDIR\\package\\%s''
SectionEnd
'''

_NSISSectionTemplateDLL = '''
Section '%s'
    CopyFiles '$EXEDIR\\package\\%s' $SYSDIR
SectionEnd
'''


class NullsoftInstallSystem(PrjInstallMaker):
    """
    Инсталятор проекта.
        Nullsoft InstallSystem.
        В качестве компилятора необходимо выбирать makensis.exe!!!
    """

    def __init__(self, PrjDir_):
        """
        Конструктор.
        @param PrjDir_: Папка проекта.
        """
        PrjInstallMaker.__init__(self, PrjDir_)

    def _copyDLL(self, InstallDir_):
        """
        Копирование необходимых DLL в инсталяционный пакет.
        @param InstallDir_: Инсталяционная папка.
        """
        python_dir = ic_file.getPythonDir()
        dll_name = python_dir+'/msvcp71.dll'
        if os.path.exists(dll_name):
            ic_file.copyToDir(dll_name, InstallDir_)
        dll_name = python_dir+'/msvcr71.dll'
        if os.path.exists(dll_name):
            ic_file.copyToDir(dll_name, InstallDir_)
            
    def _makeNSISSection(self, PackageName_):
        """
        Создание секции скрипта инсталязионного пакета.
        @param PackageName_: Имя файла инсталируемого пакета.
        """
        package_name_split = PackageName_.split('.')
        package_name_title = '.'.join(package_name_split[:-1])
        package_name_ext = package_name_split[-1]
        if package_name_ext == 'exe':
            return _NSISSectionTemplateEXE % (package_name_title, PackageName_)
        elif package_name_ext == 'msi':
            return _NSISSectionTemplateMSI % (package_name_title, PackageName_)
        elif package_name_ext == 'dll':
            return _NSISSectionTemplateDLL % (package_name_title, PackageName_)
        return _NSISSectionTemplateMSI % (PackageName_, PackageName_)
            
    def installScript(self):
        """
        Создание скрипта инсталяционного пакета проекта.
        """
        prj_name = self.getPrjName()
        sub_sys_name = os.path.basename(self._prj_dir)
        package_text = reduce(lambda txt, line: txt+line,
                              [self._makeNSISSection(ic_file.BaseName(package)) for package in self.getPackages()])

        icon_name = os.path.basename(self.getPrjIcon())
        script = _NSISScriptTemplate % (self.getPrjTitle().replace('\"', '\''),
                                        self.getPrjCopyright().replace('\"', '\''),
                                        self.getPrjAuthor().replace('\"', '\''),
                                        icon_name,
                                        prj_name, prj_name, prj_name,
                                        package_text,
                                        prj_name, prj_name, prj_name,
                                        sub_sys_name,
                                        icon_name,
                                        sub_sys_name,
                                        icon_name,
                                        prj_name, prj_name)
        return script
        
    def makeInstallPackage(self):
        """
        Создание инсталяционного пакета.
        """
        install_dir = ic_dlg.icDirDlg(None,
                                      u'Выберите инсталяционную папку',
                                      os.getcwd())
        if os.path.isdir(install_dir):
            try:
                packages = self.getPackages()
                ic_dlg.icOpenProgressDlg(None,
                                         u'Создание инсталяционного пакета проекта',
                                         u'Создание инсталяционного пакета проекта',
                                         0, len(packages)+5)
                i = 0
                # Создать папку пакетов
                os.makedirs(install_dir+'/package')

                # Скопировать иконку
                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Копирование иконки')
                ico_file = self.getPrjIcon()
                if os.path.exists(ico_file):
                    ic_file.icCopyFile(ico_file,
                                       install_dir+'/'+os.path.basename(ico_file))
                else:
                    io_prnt.outLog(u'Файл иконки <%s> не существует' % ico_file)
                
                # Создание пакета прикладной системы
                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Создание пакета прикладной системы')
                arch_file = self._makePrjInstall()
                if os.path.exists(arch_file):
                    ic_file.icCopyFile(arch_file,
                                       install_dir+'/package/'+os.path.basename(arch_file))
                    # Удалить временную папку
                    ic_file.RemoveTreeDir(os.path.dirname(arch_file), 1)
                    
                # Скопировать пакеты
                for package in packages:
                    i += 1
                    ic_dlg.icUpdateProgressDlg(i, u'Копирование пакета <%s>' % package)
                    if os.path.exists(package):
                        ic_file.icCopyFile(package,
                                           install_dir+'/package/'+os.path.basename(package))
                    else:
                        io_prnt.outLog(u'Файл пакета <%s> не существует' % package)

                # Сохранить скрипт инсталятора
                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Создание скрипта инсталятора')
                script = self.installScript()
                try:
                    nsi_file = None
                    nsi_file = open(install_dir+'\setup.nsi', 'w')
                    nsi_file.write(script)
                    nsi_file.close()
                except:
                    io_prnt.outErr(u'Ошибка сохранения скрипта инсталятора')
                    if nsi_file:
                        nsi_file.close()

                # Компилирование скрипта инсталятора
                i += 1
                ic_dlg.icUpdateProgressDlg(i, u'Компилирование скрипта инсталятора')
                nsis_cmd = '%s %s/setup.nsi' % (self.getInstallMaker(), install_dir)
                io_prnt.outLog(u'Компиляция скрипта инсталятора '+nsis_cmd)
                ic_exec.icSysCmd(nsis_cmd)

                ic_dlg.icCloseProgressDlg()
            except:
                io_prnt.outErr(u'Ошибка создания инсталяционного пакета')
                ic_dlg.icCloseProgressDlg()
                
    def _makePrjInstall(self):
        """
        Создание пакета прикладной системы.
        """
        try:
            prj_name = self.getPrjName()
            temp_dir = 'c:/temp/'+prj_name
            if os.path.exists(temp_dir):
                io_prnt.outLog(u'INSTALL WIZARD DELETE TEMP DIR <%s>' % temp_dir)
                ic_file.RemoveTreeDir(temp_dir)
                io_prnt.outLog(u'INSTALL WIZARD DELETE TEMP DIR OK')

            os.makedirs(temp_dir)
            # Скопировать необходимые папки и модули
            # во временную папку
            prj_dir = os.path.dirname(self._prj_dir)
            main_dir = os.path.dirname(prj_dir)
            # Пакет ic
            io_prnt.outLog(u'INSTALL WIZARD COPY ic PACKAGE <%s>' % main_dir)
            ic_tmp_dir = temp_dir+'/ic'
            ic_file.CopyTreeDir(main_dir+'/ic', ic_tmp_dir)
            
            # Условие удаления исходников из ic
            if not self.getOpenSource():
                ic_file.delAllFilesFilter(ic_tmp_dir, '*.py', '*.bak')

            # Пакет прикладной системы
            io_prnt.outLog(u'INSTALL WIZARD COPY %s PACKAGE %s' % (prj_name, prj_dir))
            usr_tmp_dir = temp_dir+'/'+os.path.basename(prj_dir)
            ic_file.CopyTreeDir(prj_dir,
                                temp_dir+'/'+os.path.basename(prj_dir))

            # Все откомпелироавать нехрен
            ic_file.CompileDir(temp_dir)
            
            # Заархивировать пакет прикладной системы
            rar_util = main_dir+'/ic/db/postgresql/Rar.exe'
            arch_file_name = temp_dir+'/'+prj_name+'.exe'
            arch_cmd = '%s a -r -s -ep1 -sfx -df %s %s/*.*' % (rar_util,
                                                               arch_file_name, temp_dir)
            io_prnt.outLog(u'INSTALL WIZARD Команда архивации: <%s>' % arch_cmd)
            ic_exec.icSysCmd(arch_cmd)
            return arch_file_name
        except:
            io_prnt.outErr(u'Ошибка архивации прикладной системы')
    

# Шаблон для скрипта инсталятора py2exe
_py2exeScriptTemplate = '''#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(
    description = '%s',
    name = '%s',

    # targets to build
    windows = [%s],
    console = [%s],
    )
'''


class py2exeInstallSystem(PrjInstallMaker):
    """
    Система инсталляции сделанная на py2exe.
    """

    def __init__(self, PrjDir_):
        """
        Конструктор.
        @param PrjDir_: Папка проекта.
        """
        PrjInstallMaker.__init__(self, PrjDir_)
    
    def makeInstallPackage(self):
        """
        Создание инсталяционного пакета.
        """
        install_dir = ic_dlg.icDirDlg(None,
                                      u'Выберите инсталяционную папку',
                                      os.getcwd())
        if os.path.isdir(install_dir):
            try:
                # Создание setup.py файла
                script = self.setupScript()
                try:
                    setup_file = None
                    setup_file = open(install_dir+'\setup.nsi', 'w')
                    setup_file.write(script)
                    setup_file.close()
                except:
                    io_prnt.outErr(u'Ошибка сохранения скрипта инсталятора')
                    if setup_file:
                        setup_file.close()
            
            except:
                io_prnt.outErr(u'Ошибка создания инсталяционного пакета')

    def setupScript(self):
        """
        Создание setup.py файла.        
        """
        pass
        
    def getConsole(self):
        """
        Признак поддержки консоли.
        """
        return bool(ini.loadParamINI(self._prj_ini_file_name,
                                     'INSTALL', 'console'))

    def setConsole(self,MakeConsole_):
        """
        Признак поддержки консоли.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'open_src', str(MakeConsole_))
            
# --- Визард создания инсталяционного пакета ---
def runInstallWizard(Parent_,PrjResFileName_):
    """
    Запуск визарда создания инсталяционного пакета.
    @param Parent_: Родительское окно.
    @param PrjResFileName_: Имя ресурса проекта.
    """
    install_maker = NullsoftInstallSystem(os.path.dirname(PrjResFileName_))
    
    wiz = wizard.Wizard(Parent_, -1,
                        u'Создание инсталяционного пакета проекта',
                        imglib.imgInstallWizard)
    page1 = PrjAttrPage(wiz,
                        u'Атрибуты инсталяционного пакета проекта', install_maker)
    page2 = PackagePage(wiz, u'Необходимые пакеты', install_maker)
    
    wiz.FitToPage(page1)
    
    page1.SetNext(page2)
    page2.SetPrev(page1)

    if wiz.RunWizard(page1):
        # Сохранить атрибуты проекта
        install_maker.setPrjName(page1.sizer.evalSpace['_dict_obj']['TextPrjName'].GetValue())
        install_maker.setPrjTitle(page1.sizer.evalSpace['_dict_obj']['TextDiscr'].GetValue())
        install_maker.setPrjAuthor(page1.sizer.evalSpace['_dict_obj']['TextAuthor'].GetValue())
        install_maker.setPrjCopyright(page1.sizer.evalSpace['_dict_obj']['TextCopyright'].GetValue())
        install_maker.setPrjIcon(page1.sizer.evalSpace['_dict_obj']['TextIcon'].GetValue())
        install_maker.setInstallMaker(page1.sizer.evalSpace['_dict_obj']['TextInstallSys'].GetValue())
        install_maker.setOpenSource(page1.sizer.evalSpace['_dict_obj']['OpenSourceCheckBox'].GetValue())
        install_maker.setPackages(page2.sizer.evalSpace['_dict_obj']['packageList'].getStringsByCol(0))

        install_maker.makeInstallPackage()

        ic_dlg.icMsgBox(u'ВНИМАНИЕ', u'Создан инсталяционный пакет проекта.')
    else:
        ic_dlg.icMsgBox(u'ВЫХОД', u'Выход из визарда создания инсталяционного пакета проекта')


def makePrjAttrPage(wizPg, title, installMaker):
    """
    Инициализация страницы атрибутов проекта.
    """
    import ic.install.InstallPrjAttrWizPage as page
    obj = page.icInstallPrjAttrWizPage(wizPg)    
    sizer = obj.getObject()
    if installMaker:
        # Инициализация атрибутов проекта
        obj.evalSpace['_dict_obj']['TextPrjName'].SetValue(str(installMaker.getPrjName()))
        obj.evalSpace['_dict_obj']['TextDiscr'].SetValue(str(installMaker.getPrjTitle()))
        obj.evalSpace['_dict_obj']['TextAuthor'].SetValue(str(installMaker.getPrjAuthor()))
        obj.evalSpace['_dict_obj']['TextCopyright'].SetValue(str(installMaker.getPrjCopyright()))
        obj.evalSpace['_dict_obj']['TextIcon'].SetValue(str(installMaker.getPrjIcon()))
        obj.evalSpace['_dict_obj']['TextInstallSys'].SetValue(str(installMaker.getInstallMaker()))
        obj.evalSpace['_dict_obj']['OpenSourceCheckBox'].SetValue(installMaker.getOpenSource())
        
    return sizer


def makePackagePage(wizPg, title, installMaker):
    """
    Инициализация страницы необходимых пакетов.
    """
    import ic.install.InstallPackageWizPage as page
    obj = page.icInstallPackageWizPage(wizPg)    
    sizer = obj.getObject()
    if installMaker:
        # Инициализация атрибутов проекта
        for package in installMaker.getPackages():
            obj.evalSpace['_dict_obj']['packageList'].appendStringRec(str(package))

    return sizer


class PrjAttrPage(wizard.PyWizardPage):
    def __init__(self, parent, title, installMaker=None):
        wizard.PyWizardPage.__init__(self, parent)
        self.sizer = makePrjAttrPage(self, title, installMaker)
        self.next = self.prev = None
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev


class PackagePage(wizard.PyWizardPage):
    def __init__(self, parent, title, installMaker=None):
        wizard.PyWizardPage.__init__(self, parent)
        self.sizer = makePackagePage(self, title, installMaker)
        self.next = self.prev = None
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev
  
# --- Визард создания демо-приложения ---
def runDemoWizard(Parent_, PrjResFileName_):
    """
    Запуск визарда создания инсталяционного пакета.
    @param Parent_: Родительское окно.
    @param PrjResFileName_: Имя ресурса проекта.
    """
    install_maker = py2exeInstallSystem(os.path.dirname(PrjResFileName_))
    
    wiz = wizard.Wizard(Parent_, -1,
                        u'Создание демо-проекта',
                        imglib.imgInstallWizard)
    page = DemoPage(wiz, u'Атрибуты демо-проекта', install_maker)

    wiz.FitToPage(page)
    
    if wiz.RunWizard(page):
        # Сохранить атрибуты проекта
        install_maker.setPrjName(page.sizer.evalSpace['_dict_obj']['TextPrjName'].GetValue())
        install_maker.setPrjTitle(page.sizer.evalSpace['_dict_obj']['TextDiscr'].GetValue())
        install_maker.setPrjAuthor(page.sizer.evalSpace['_dict_obj']['TextAuthor'].GetValue())
        install_maker.setPrjCopyright(page.sizer.evalSpace['_dict_obj']['TextCopyright'].GetValue())
        install_maker.setPrjIcon(page.sizer.evalSpace['_dict_obj']['TextIcon'].GetValue())
        install_maker.setConsole(page.sizer.evalSpace['_dict_obj']['ConsoleCheckBox'].GetValue())

        install_maker.makeInstallPackage()

        ic_dlg.icMsgBox(u'ВНИМАНИЕ', u'Создан демо-проект.')
    else:
        ic_dlg.icMsgBox(u'ВЫХОД', u'Выход из визарда создания демо-проекта')


def makeDemoPrjPage(wizPg, title, installMaker):
    """
    Инициализация страницы атрибутов демо-проекта.
    """
    import ic.install.InstallDemoPrjWizPage as page
    obj = page.icInstallDemoPrjWizPage(wizPg)    
    sizer = obj.getObject()
    if installMaker:
        # Инициализация атрибутов проекта
        obj.evalSpace['_dict_obj']['TextPrjName'].SetValue(str(installMaker.getPrjName()))
        obj.evalSpace['_dict_obj']['TextDiscr'].SetValue(str(installMaker.getPrjTitle()))
        obj.evalSpace['_dict_obj']['TextAuthor'].SetValue(str(installMaker.getPrjAuthor()))
        obj.evalSpace['_dict_obj']['TextCopyright'].SetValue(str(installMaker.getPrjCopyright()))
        obj.evalSpace['_dict_obj']['TextIcon'].SetValue(str(installMaker.getPrjIcon()))
        obj.evalSpace['_dict_obj']['ConsoleCheckBox'].SetValue(installMaker.getConsole())
        
    return sizer


class DemoPage(wizard.PyWizardPage):
    def __init__(self, parent, title, installMaker=None):
        wizard.PyWizardPage.__init__(self, parent)
        self.sizer = makeDemoPrjPage(self, title, installMaker)
        self.next = self.prev = None
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev

# --- Визард создания публикации ---
class zipPublicSystem(PrjInstallMaker):
    """
    Система публикации.
    """

    def __init__(self, PrjDir_):
        """
        Конструктор.
        @param PrjDir_: Папка проекта.
        """
        PrjInstallMaker.__init__(self, PrjDir_)

    def getArchivator(self):
        """
        Архиватор.
        """
        return ini.loadParamINI(self._prj_ini_file_name,
                                'INSTALL', 'archivator')

    def setArchivator(self, Archivator_):
        """
        Архиватор.
        """
        return ini.saveParamINI(self._prj_ini_file_name,
                                'INSTALL', 'archivator', Archivator_)
            
    def makeInstallPackage(self):
        """
        Создание инсталяционного пакета.
        """
        install_dir = ic_dlg.icDirDlg(None,
                                      u'Выберите инсталяционную папку',
                                      os.getcwd())
        if os.path.isdir(install_dir):
            arch_file_name = self._makePrjInstall()
            ic_file.icCopyFile(arch_file_name,
                               install_dir+'/'+os.path.basename(arch_file_name))
            
    def _publicWinRAR(self, InstallDir_):
        """
        Создание публикации архиватором WinRAR.
        """
        pass
    
    def _makePrjInstall(self):
        """
        Создание пакета прикладной системы.
        """
        try:
            prj_name = self.getPrjName()
            temp_dir = os.environ['TMP']+'/'+prj_name
            if os.path.exists(temp_dir):
                io_prnt.outLog(u'PUBLIC WIZARD DELETE TEMP DIR <%s>' % temp_dir)
                ic_file.RemoveTreeDir(temp_dir)
                io_prnt.outLog(u'PUBLIC WIZARD DELETE TEMP DIR OK')

            os.makedirs(temp_dir)
            # Скопировать необходимые папки и модули
            # во временную папку
            prj_dir = os.path.dirname(self._prj_dir)
            main_dir = os.path.dirname(prj_dir)
            # Пакет ic
            io_prnt.outLog(u'PUBLIC WIZARD COPY ic PACKAGE <%s>' % main_dir)
            ic_tmp_dir = temp_dir+'/ic'
            ic_file.CopyDir(main_dir+'/ic', temp_dir)
            
            # Условие удаления исходников из ic
            ic_file.delAllFilesFilter(ic_tmp_dir, '*.bak', '*.pyc')

            # Пакет прикладной системы
            io_prnt.outLog(u'PUBLIC WIZARD COPY %s PACKAGE %s' % (prj_name, prj_dir))
            usr_tmp_dir = temp_dir+'/'+os.path.basename(prj_dir)
            ic_file.CopyDir(prj_dir, temp_dir)
            
            #Условие удаления исходников из ic
            ic_file.delAllFilesFilter(usr_tmp_dir, '*.bak', '*.pyc', '*.lck', '/log/*.ini', '/log/*.log')
            
            ic_file.icCopyFile(main_dir+'/readme.ru',
                               temp_dir+'/readme.ru')
            ic_file.icCopyFile(main_dir+'/license.ru',
                               temp_dir+'/license.ru')

            if ic_util.isOSWindowsPlatform():
                return self._makeArchiveRAR(main_dir, temp_dir, prj_name)
            else:
                return self._makeArchiveZIP(temp_dir, prj_name)
            
        except:
            io_prnt.outErr(u'Ошибка архивации прикладной системы')
        return None
            
    def _makeArchiveRAR(self, MainDir_, TempDir_, PrjName_):
        """
        Заархивировать пакет прикладной системы. Архиватор: RAR.
        """
        # Заархивировать пакет прикладной системы
        arch_util = MainDir_+'/ic/db/postgresql/Rar.exe'
        arch_file_name = TempDir_+'/'+PrjName_+'_'+str(self.readPrjVersion())+'.zip'
        arch_cmd = '%s a -r -s -ep1 -afzip -df %s %s/*.*' % (arch_util,
                                                             arch_file_name, TempDir_)
        io_prnt.outLog(u'PUBLIC WIZARD Команда архивации: '+arch_cmd)
        ic_exec.icSysCmd(arch_cmd)
        return arch_file_name
        
    def _makeArchiveZIP(self, TempDir_, PrjName_):
        """
        Заархивировать пакет прикладной системы. Архиватор: ZIP.
        """
        # Заархивировать пакет прикладной системы
        arch_util = 'zip'
        arch_file_name = TempDir_+'/'+PrjName_+'_'+str(self.readPrjVersion())+'.zip'

        arch_cmd = 'cd %s;%s -r %s *' % (TempDir_, arch_util, arch_file_name)
        io_prnt.outLog(u'PUBLIC WIZARD Команда архивации: '+arch_cmd)
        ic_exec.icSysCmd(arch_cmd)
        return arch_file_name
        
    
def runPublicWizard(Parent_, PrjResFileName_):
    """
    Запуск визарда создания пакета публикации.
    @param Parent_: Родительское окно.
    @param PrjResFileName_: Имя ресурса проекта.
    """
    public_maker = zipPublicSystem(ic_file.DirName(PrjResFileName_))
    
    wiz = wizard.Wizard(Parent_, -1,
                        u'Создание пакета публикации',
                        imglib.imgInstallWizard)
    page = PublicPage(wiz, u'Атрибуты пакета публикации', public_maker)
    
    wiz.FitToPage(page)
    
    if wiz.RunWizard(page):
        # Сохранить атрибуты проекта
        public_maker.setPrjName(page.sizer.evalSpace['_dict_obj']['TextPrjName'].GetValue())
        public_maker.setAutoVer(page.sizer.evalSpace['_dict_obj']['AutoVerCheckBox'].GetValue())
        public_maker.setPrjVersion(page.sizer.evalSpace['_dict_obj']['TextVersion'].GetValue())
        public_maker.setArchivator(page.sizer.evalSpace['_dict_obj']['TextArchiveSys'].GetValue())

        public_maker.makeInstallPackage()

        ic_dlg.icMsgBox(u'ВНИМАНИЕ', u'Создан пакет публикации.')
    else:
        ic_dlg.icMsgBox(u'ВЫХОД', u'Выход из визарда создания пакета публикации')


def makePublicPrjPage(wizPg, title, publicMaker):
    """
    Инициализация страницы атрибутов пакета публикации.
    """
    import ic.install.PublicPrjAttrWizPage as page
    obj = page.icPublicPrjAttrWizPage(wizPg)    
    sizer = obj.getObject()
    if publicMaker:
        # Инициализация атрибутов проекта
        obj.evalSpace['_dict_obj']['TextPrjName'].SetValue(str(publicMaker.getPrjName()))
        obj.evalSpace['_dict_obj']['AutoVerCheckBox'].SetValue(publicMaker.getAutoVer())
        obj.evalSpace['_dict_obj']['TextVersion'].SetValue(str(publicMaker.getPrjVersion()))
        obj.evalSpace['_dict_obj']['TextArchiveSys'].SetValue(str(publicMaker.getArchivator()))
        
    return sizer


class PublicPage(wizard.PyWizardPage):
    def __init__(self, parent, title, publicMaker=None):
        wizard.PyWizardPage.__init__(self, parent)
        self.sizer = makePublicPrjPage(self, title, publicMaker)
        self.next = self.prev = None
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev
