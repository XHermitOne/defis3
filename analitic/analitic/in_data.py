# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Модуль прикладной системы.
    Организация поступления входной информации.
Автор(ы): Шурик Колчанов.
"""

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---
import ic.db.dbf as dbf
import ic.log.ic_log as ic_log
import ic.dlg.ic_dlg as ic_dlg
import ic.engine.ic_user as ic_user
import ic.utils.ic_file as ic_file
import ic.utils.ic_util as ic_util
import ic.utils.ic_ini as ic_ini
import ic.db.ic_sqlobjtab as ic_sqlobjtab
from ic.db import ic_tabview
import ic.utils.resource as resource
#import NSI.spravfunc as nsi

#--- Функции ---
def saveInputDataDir():
    """
    Выбрать и сохранить папку входных данных.
    """
    input_data_dir=ic_dlg.icDirDlg(None,
        'Выберите папку входных данных')
    if ic_file.IsDir(input_data_dir):
        setInputDataDir(input_data_dir)
    
def getInputDataDir():
    """
    Определить папку входных данных.
    """
    prj_path=ic_user.icGet('SYS_RES')
    ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
    return ic_ini.IniLoadParam(ini_file,
            'SETTINGS','input_data_dir')

def setInputDataDir(InputDataDir_):
    """
    Сохранить в настроечном файле папку входных данных.
    @param InputDataDir_: Папка в которой лежат дбфники.
    """
    #Заносить только проверенные значния
    if InputDataDir_ and ic_file.IsDir(InputDataDir_):
        prj_path=ic_user.icGet('SYS_RES')
        ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
        return ic_ini.IniSaveParam(ini_file,
            'SETTINGS','input_data_dir',InputDataDir_)

def loadInputData(InputDataDir_=None):
    """
    Загрузить входные данные в БД.
    @param InputDataDir_: Папка в которой лежат дбфники.
    """
    if InputDataDir_ is None:
        InputDataDir_=getInputDataDir()
    
    #   Загружаем файлы по реализации
    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.grf')
    print '--->>>loadInputData -> <analitik>',dbf_files,InputDataDir_ #,ic_file.ListDir(InputDataDir_)
    for dbf_file in dbf_files:
        print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file)
        #Поменять расширение
        ic_file.icChangeExt(dbf_file,'.bak')
        
    #   Загружаем файлы по заявкам
    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.grz')
    print '--->>>loadInputData -> <zayavki>',dbf_files,InputDataDir_
    for dbf_file in dbf_files:
        print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file, 'zayavki')
        #Поменять расширение
        ic_file.icChangeExt(dbf_file,'_grz.bak')
    
    #   Загружаем файлы по оплате
    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.grp')
    print '--->>>loadInputData -> <pay>', dbf_files,InputDataDir_
    for dbf_file in dbf_files:
        print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file, 'pay')
        #Поменять расширение
        ic_file.icChangeExt(dbf_file,'_grp.bak')
    
    print 'Refresh All Views'
    refreshAllTabView()
        
def loadInputDataDBF(DBFFileName_, className='analitic'):
    """
    Загрузка входных данных из dbf файла.
    """
    ### Изменил Оконешников А.
    #Было
    #res=resource.icGetRes('analitic',nameRes='analitic')
    res=resource.icGetRes(className, nameRes=className)
    ###
    
    tab=ic_sqlobjtab.icSQLObjDataClass(res)
    #print '~~~>>>',tab.dataclass._SO_columnDict
    
    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()
    #print 'DBF isOpen:', bOpen
    #print 'DBF RecCount',DBFFileName_,dbf_f.getRecCount()
    while not dbf_f.EOF():
        #Прочитать все данные из записи
        dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
            '%Y.%m.%d')
        grp_cod=dbf_f.getFieldByName('GRUP').strip()
        grp_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMGRUP'),'CP866','CP1251')
        t_cod_str=dbf_f.getFieldByName('CODT').strip()
        if t_cod_str and grp_cod:
            try:
                t_cod='%03d%04d'%(int(grp_cod),int(t_cod_str))
            except:
                print '### ValueError GROUP,CODT=', grp_cod, t_cod_str
                grp_cod='000'
                t_cod='0000'
        else:
            grp_cod='000'
            t_cod='0000'
        t_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMS'),'CP866','CP1251')
        ei_name=ic_util.ReCodeString(dbf_f.getFieldByName('EI'),'CP866','CP1251')
        kol_str=dbf_f.getFieldByName('KOLF').strip()
        if kol_str:
            kol=float(kol_str)
        else:
            kol=0.0
        cen_str=dbf_f.getFieldByName('CENA').strip()
        if cen_str:
            cen=float(cen_str)
        else:
            cen=0.0
        sum_str=dbf_f.getFieldByName('SUMMA').strip()
        if sum_str:
            sum=float(sum_str)
        else:
            sum=0.0
        reg_cod='0'*(max(0,4-len(dbf_f.getFieldByName('REG').strip())))+dbf_f.getFieldByName('REG').strip()
        reg_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMREG'),'CP866','CP1251')
        men_cod='0'*(max(0,4-len(dbf_f.getFieldByName('MENS').strip())))+dbf_f.getFieldByName('MENS').strip()
        men_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMMENS'),'CP866','CP1251')

        #Синхронизация справочников
        #_syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
        #_syncSpravRegions(reg_cod,reg_name)
        #_syncSpravMenagers(men_cod,men_name)
        
        #Загрузка данных
        print '.',
        tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
            ei=ei_name,kolf=kol,cena=cen,summa=sum,
            reg=reg_cod,mens=men_cod,
            plan_kol=None,plan_sum=None)
        
        dbf_f.Next()
    print 'OK'
    dbf_f.Close()

def syncInputDataDBF(DBFFileName_):
    """
    Синхронизация справочников входных данных из dbf файла.
    """
    #res=resource.icGetRes('analitic',nameRes='analitic')
    #tab=ic_sqlobjtab.icSQLObjDataClass(res)
    
    dbf_f=dbf.icDBFFile(DBFFileName_)
    dbf_f.Open()
    while not dbf_f.EOF():
        #Прочитать все данные из записи
        dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
            '%d/%m/%Y %H:%M:%S')
        grp_cod=int(dbf_f.getFieldByName('GRUP'))
        grp_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMGRUP'),'CP866','CP1251')
        t_cod=int(dbf_f.getFieldByName('CODT'))
        t_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMS'),'CP866','CP1251')
        ei_name=ic_util.ReCodeString(dbf_f.getFieldByName('EI'),'CP866','CP1251')
        kol=float(dbf_f.getFieldByName('KOLF'))
        cen=float(dbf_f.getFieldByName('CENA'))
        sum=float(dbf_f.getFieldByName('SUMMA'))
        reg_cod=int(dbf_f.getFieldByName('REG'))
        reg_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMREG'),'CP866','CP1251')
        men_cod=int(dbf_f.getFieldByName('MENS'))
        men_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMMENS'),'CP866','CP1251')

        #Синхронизация справочников
        _syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
        _syncSpravRegions(reg_cod,reg_name)
        _syncSpravMenagers(men_cod,men_name)
        
        #Загрузка данных
        #print '.',
        #tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
        #    ei=ei_name,kolf=kol,cena=cen,summa=sum,
        #    reg=reg_cod,mens=men_cod)
        
        dbf_f.Next()
    dbf_f.Close()

def refreshAllTabView():
    """
    Обновить все представления.
    """
    #realize_group_sum=ic_tabview.icSQLObjTabView('realize_group_sum')
    realize_sum=ic_tabview.icSQLObjTabView('realize_sum')
    zayavki_sum=ic_tabview.icSQLObjTabView('zayavki_sum')
    pay_sum=ic_tabview.icSQLObjTabView('pay_sum')
    
    #realize_group_sum.refreshView()
    realize_sum.refreshView()
    print ' >> refreshView <realize_sum>'
    zayavki_sum.refreshView()
    print ' >> refreshView <zayavki_sum>'
    pay_sum.refreshView()
    print ' >> refreshView <pay_sum>'
    
def _syncSprav(Type_,Cod_,Name_):
    """
    Синхронизация данных справочника.
    @param Type: Тип справочника.
    @param Cod_: Код.
    @param Name_: Название.
    """
    s_name=nsi.FSprav(Type_,Cod_)
    if s_name is None:
        #Такой вид продукции не найден
        #Надо добавить его в справочник
        name_=Name_.strip()
        ic_log.icToLog('NSI %s ADD %s %s'%(Type_,Cod_,name_))
        tab=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
            nameRes='NsiStd'))
        tab.add(type=Type_,cod=Cod_,name=name_,id_nsi_list=nsi.getSpravId(Type_))
    else:
        s_name=s_name.strip()
        name_=Name_.strip()
        if s_name<>name_ and name_:
            #Изменилось название
            #Надо синхронизировать со справочником
            ic_log.icToLog('NSI %s CHANGE %s %s <> %s'%(Type_,Cod_,name_,s_name))
            id=nsi.getSpravCodeId(Type_,Cod_)
            if id<>None:
                tab=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
                    nameRes='NsiStd'))
                tab.update(id,type=Type_,cod=Cod_,name=name_,id_nsi_list=nsi.getSpravId(Type_))
    
def _syncSpravProducts(GroupCod_,GroupName_,ProductCod_,ProductName_):
    """
    Синхронизация данных справочника продуктов.
    """
    #Сначала синхронизировать виды продукции
    cod='%03d'%(int(GroupCod_))
    _syncSprav('Product',cod,GroupName_)
    #Затем сами продукты
    cod='%03d%04d'%(int(GroupCod_),int(ProductCod_))
    _syncSprav('Product',cod,ProductName_)

def _syncSpravRegions(RegCod_,RegName_):
    """
    Синхронизация данных справочника регионов.
    """
    #Сначала синхронизировать виды продукции
    cod='%04d'%(int(RegCod_))
    _syncSprav('Region',cod,RegName_)
    
def _syncSpravMenagers(MenCod_,MenName_):
    """
    Синхронизация данных справочника менеджеров.
    """
    #Сначала синхронизировать виды продукции
    cod='%03d'%(int(MenCod_))
    _syncSprav('Menager',cod,MenName_)
