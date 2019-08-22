#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Модуль прикладной системы.
    Организация поступления входной информации от филиалов/офисов предприятия.
    Информация обофисах находится в НСИ справочник Office.
    cod - 2-х символьный код офиса.
    s1 - Маска/шаблон загружаемых файлов.
    s2 - Функция загрузки. Например in_data.loadDataDBFStandart.
    s3 - Папка архиваю, если определена, тогда после удачной загрузки
        файлы будут переносится в нее. Если не определена,
        то файлы просто будут переименовываться в BAK файлы.
Автор(ы): Шурик Колчанов.
"""

#--- Подключение библиотек ---
import wx
#import datetime

import ic.db.dbf as dbf
import ic.log.ic_log as ic_log
import ic.dlg.dlgfunc as ic_dlg
#import ic.dlg.threaded_progress as progress
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg

import ic.engine.glob_functions as ic_user
import ic.utils.filefunc as ic_file
import ic.utils.toolfunc as ic_util
import ic.utils.datetimefunc as ic_time
import ic.utils.ic_ini as ic_ini
#import ic.db.ic_sqlobjtab as ic_sqlobjtab
#from ic.db import ic_tabview
import ic.utils.resource as resource
#import NSI.spravfunc as nsi
import ic.components.icResourceParser as prs

import analitic.in_data as input_data
from STD import std_dialogs

# Версия
__version__ = (0, 0, 0, 1)


#--- Функции (Устаревшие) данных ---
def loadInputData(input_data_dir=None):
    """
    Загрузить входные данные в БД.
    @param input_data_dir: Папка в которой лежат дбфники.
    """
    if input_data_dir is None:
        input_data_dir=input_data.getInputDataDir()

    #   Загружаем файлы по реализации
    dbf_files=ic_file.getFilenamesByExt(input_data_dir, '.olp')
    dbf_files.sort()
    # print '--->>>loadInputData -> <analiticIC>',dbf_files,input_data_dir #,ic_file.ListDir(input_data_dir)
    for dbf_file in dbf_files:
        # print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file,'analitic')
        #Поменять расширение
        #ic_file.changeExt(dbf_file,'_rlz.bak')

    #   Загружаем файлы по заявкам
    dbf_files=ic_file.getFilenamesByExt(input_data_dir, '.olp')
    dbf_files.sort()
    # print '--->>>loadInputData -> <zayavkiIC>',dbf_files,input_data_dir
    for dbf_file in dbf_files:
        # print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file, 'zayavki')
        #Поменять расширение
        ic_file.changeExt(dbf_file, '.bak')
        #Отметить в логе
        _logInputData(dbf_file)

    #   Загружаем файлы по оплате
#    dbf_files=ic_file.getFilenamesByExt(input_data_dir,'.grp')
#    print '--->>>loadInputData -> <pay>', dbf_files,input_data_dir
#    for dbf_file in dbf_files:
#        print 'LOAD DATA FROM',dbf_file
#        loadInputDataDBF(dbf_file, 'pay')
#        #Поменять расширение
#        ic_file.changeExt(dbf_file,'_grp.bak')

    #print 'Refresh All Views'
    #refreshAllTabView()

def loadInputDataDBF(DBFFileName_, className='analitic'):
    """
    Загрузка входных данных из dbf файла.
    """
    ### Изменил Оконешников А.
    #Было
    #res=resource.icGetRes('analitic',nameRes='analitic')
    res = resource.icGetRes(className, nameRes=className)
    ###

    tab = ic_sqlobjtab.icSQLObjDataClass(res)
    #Удалить данные перед загрузкой
    ok=_delLoadData(DBFFileName_,tab)
    if not ok:
        return

    #
    dbf_office_cod=ic_file.BaseName(DBFFileName_)[:2].lower()
    #print '~~~>>>',tab.dataclass._SO_columnDict

    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()
    #print 'DBF isOpen:', bOpen
    #print 'DBF RecCount',DBFFileName_,dbf_f.getRecCount()
    i=0
    while not dbf_f.EOF():
        #Прочитать все данные из записи
        try:
            dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
                '%Y.%m.%d')
            grp_cod='%03d'%(int(dbf_f.getFieldByName('GRUP').strip()))
            grp_name=ic_util.recodeText(dbf_f.getFieldByName('NAMGRUP'),
                'CP866','CP1251')
            t_cod_str='0000' #dbf_f.getFieldByName('CODT').strip()
            if t_cod_str and grp_cod:
                try:
                    t_cod='%03d%04d'%(int(grp_cod),int(t_cod_str))
                except:
                    # print '### ValueError GROUP,CODT=', grp_cod, t_cod_str
                    grp_cod='000'
                    t_cod='0000'
            else:
                grp_cod='000'
                t_cod='0000'
            t_name=ic_util.recodeText(dbf_f.getFieldByName('NAMS'),
                'CP866','CP1251')
            ei_name=ic_util.recodeText(dbf_f.getFieldByName('EI'),
                'CP866','CP1251')
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

            reg_str=dbf_f.getFieldByName('REG').strip()
            reg_cod='%04d'%(int(reg_str))
            reg_name=ic_util.recodeText(dbf_f.getFieldByName('NAMREG'),
                'CP866','CP1251')

            men_str=dbf_f.getFieldByName('MENS').strip()
            men_cod='%04d'%(int(men_str))
            men_name=ic_util.recodeText(dbf_f.getFieldByName('NAMMENS'),
                'CP866','CP1251')

            #Загрузка данных
            i+=1
            #recs=tab.select(ic_sqlobjtab.AND(tab.q.dtoper==dt_oper,
            #    tab.q.grup==grp_cod,tab.q.summa==sum,
            #    tab.q.reg==reg_cod,tab.q.mens==men_cod))
            #print idx,recs
            #if recs.count():
            #    for rec in recs:
            #        tab.update(rec.id,dtoper=dt_oper,grup=grp_cod,codt=t_cod,
            #            ei=ei_name,kolf=kol,cena=cen,summa=sum,
            #            reg=reg_cod,mens=men_cod,
            #            plan_kol=None,plan_sum=None)
            #else:
            print i
            tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
                ei=ei_name,kolf=kol,cena=cen,summa=sum,
                reg=reg_cod,mens=men_cod,
                plan_kol=None,plan_sum=None,
                office_cod=dbf_office_cod)

            #Синхронизация справочников
            _syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
            _syncSpravRegions(reg_cod,reg_name)
            _syncSpravMenagers(men_cod,men_name)

        except:
            print 'ERROR'
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
        grp_name=ic_util.recodeText(dbf_f.getFieldByName('NAMGRUP'), 'CP866', 'CP1251')
        t_cod=int(dbf_f.getFieldByName('CODT'))
        t_name=ic_util.recodeText(dbf_f.getFieldByName('NAMS'), 'CP866', 'CP1251')
        ei_name=ic_util.recodeText(dbf_f.getFieldByName('EI'), 'CP866', 'CP1251')
        kol=float(dbf_f.getFieldByName('KOLF'))
        cen=float(dbf_f.getFieldByName('CENA'))
        sum=float(dbf_f.getFieldByName('SUMMA'))
        reg_cod=int(dbf_f.getFieldByName('REG'))
        reg_name=ic_util.recodeText(dbf_f.getFieldByName('NAMREG'), 'CP866', 'CP1251')
        men_cod=int(dbf_f.getFieldByName('MENS'))
        men_name=ic_util.recodeText(dbf_f.getFieldByName('NAMMENS'), 'CP866', 'CP1251')

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


def _delLoadData(DBFFileName_,DataTab_):
    """
    Удалить из целевой таблицы данные, соответствующие загружаемым.
    """
    try:
        #Опреджелить дату, за которую происходит загрузка данных
        day_count=getLoadDayCount()
        if day_count:
            day_count=datetime.timedelta(int(day_count))
        else:
            return
        dbf_file_name=ic_file.BaseName(DBFFileName_)

        dbf_office_cod=dbf_file_name[:2].lower()
        cur_year=2000+int(dbf_file_name[2:4])
        cur_month=int(dbf_file_name[4:6])
        cur_day=int(dbf_file_name[6:8])

        end_date=datetime.datetime(cur_year,cur_month,cur_day)
        begin_date=end_date-day_count
        limit_date=datetime.datetime(cur_year,01,01)
        if begin_date<limit_date:
            begin_date=limit_date

        del_sql="""DELETE FROM %s
        WHERE (dtoper BETWEEN '%s' AND '%s')
            AND office_cod='%s';"""%(DataTab_.getDBTableName(),
            begin_date.strftime('%Y.%m.%d'),end_date.strftime('%Y.%m.%d'),
            dbf_office_cod)
        print 'SQL STRING:',del_sql
        print DataTab_.executeSQL(del_sql)
        #date_lst=map(lambda cur_day: cur_day.strftime('%Y.%m.%d'),
        #    map(lambda day_delta: end_date-datetime.timedelta(day_delta),
        #    range(int(day_count))))
        #date_lst=[]
        #cur_day=end_date
        #while cur_day>=begin_date:
        #    cur_date_str=cur_day.strftime('%Y.%m.%d')
        #    cur_day-=datetime.timedelta(1)
        #    date_lst.append(cur_date_str)
        #date_lst.sort()

        #for cur_date in date_lst:
        #    DataTab_.del_where(ic_sqlobjtab.AND(DataTab_.q.office_cod==dbf_office_cod,
        #        DataTab_.q.dtoper==cur_date))
        #or_lst=map(lambda cur_date: DataTab_.q.dtoper==cur_date,date_lst)
        #DataTab_.del_where(ic_sqlobjtab.OR(*or_lst))
        return True
    except:
        ic_log.icLogErr()
        return False

#--- Функции синхронизации справочников ---
def _syncSprav(Type_,Cod_,Name_):
    """
    Синхронизация данных справочника.
    @param Type: Тип справочника.
    @param Cod_: Код.
    @param Name_: Название.
    """
    s_name=nsi.FSpravBuffRepl(Type_,Cod_)
    if s_name is None:
        #Такой вид продукции не найден
        #Надо добавить его в справочник
        name_=Name_.strip()
        ic_log.icToLog('NSI %s ADD %s %s'%(Type_,Cod_,name_))
        tab=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
            nameRes='NsiStd'))
        tab.add(type=Type_,
            cod=Cod_,
            name=name_,
            id_nsi_list=nsi.getSpravId(Type_),
            access='',
            count=1,
            n1=0,n2=0,n3=0, #n4=0,n5=0,
            f1=0.0,f2=0.0,f3=0.0,
            s1='',s2='',s3='') #,s4='',s5='')
        nsi.refreshSpravBuffRepl(Type_)
#    else:
#        s_name=s_name.strip()
#        name_=name.strip()
#        if s_name<>name_ and name_:
#            #Изменилось название
#            #Надо синхронизировать со справочником
#            ic_log.icToLog('NSI %s CHANGE %s %s <> %s'%(res_type,Cod_,name_,s_name))
#            id=nsi.getSpravCodeId(res_type,Cod_)
#            if id<>None:
#                tab=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
#                    nameRes='NsiStd'))
#                tab.update(id,type=res_type,cod=Cod_,name=name_,id_nsi_list=nsi.getSpravId(res_type))

def _syncSpravProducts(GroupCod_,GroupName_,ProductCod_,ProductName_):
    """
    Синхронизация данных справочника продуктов.
    """
    #Сначала синхронизировать виды продукции
    cod='%03d'%(int(GroupCod_))
    _syncSprav('Product',cod,GroupName_)
    #Затем сами продукты
    #cod='%03d%04d'%(int(GroupCod_),int(ProductCod_))
    #_syncSprav('Product',cod,ProductName_)

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

#--- Функции загрузки ----
def getDateRange(DBFFileName_,DateFieldName_='DTOPER'):
    """
    Определение загружаемого диапазона дат из DBF файла.
    @return: Возвращает кортеж начальной и конечной даты.
        Или None в случае ошибки.
    """
    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()
    if not bOpen:
        ic_log.icToLog('Ошибка открытия файла %s'%(DBFFileName_))
        return None
    #Инициализация минимальной и максимальной даты по первой записи
    try:
        date_value=dbf_f.getDateFieldFmtByName(DateFieldName_,'%Y.%m.%d')
    except:
        ic_log.icLogErr()
        dbf_f.Close()
        return None

    min_date=date_value
    max_date=date_value

    while not dbf_f.EOF():
        try:
            date_value=dbf_f.getDateFieldFmtByName(DateFieldName_,'%Y.%m.%d')
            if min_date>date_value:
                min_date=date_value
            if max_date<date_value:
                max_date=date_value
        except:
            ic_log.icLogErr()
        dbf_f.Next()
    dbf_f.Close()
    return (min_date,max_date)

def delDateRangeInDB(DataTab_,BeginDate_,EndDate_,OfficeCode_):
    """
    Удалить временной диапазон из БД с указанием источника.
    """
    try:
        del_sql="""DELETE FROM %s
        WHERE (dtoper BETWEEN '%s' AND '%s')
            AND office_cod='%s';"""%(DataTab_.getDBTableName(),
            BeginDate_,EndDate_,
            OfficeCode_)
        # print 'SQL STRING:',del_sql
        DataTab_.executeSQL(del_sql)
        return True
    except:
        ic_log.icLogErr()
        return False


def loadDataDBFStandart(DBFFileName_,ToTabName_,OfficeCod_):
    """
    Стандартная загрузка DBF файла в БД.
    """
    #res=resource.icGetRes(ToTabName_, nameRes=ToTabName_)

    tab=ic_sqlobjtab.icSQLObjTabClass(ToTabName_)

    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()

    #ic_proccess_dlg.setProccessBoxLabel(DBFFileName_, 0,label2='Загрузка данных', value2=10)
    #progress.icOpenThreadedProgressDlg('Загрузка данных',
    #    DBFFileName_,0,dbf_f.getRecCount())
    i=0
    #try:
    #    count_100=float(100/dbf_f.getRecCount())
    #except:
    #    count_100=0
    while not dbf_f.EOF():
        #Прочитать все данные из записи
        try:
            dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
                '%Y.%m.%d')
            grp_cod='%03d'%(int(dbf_f.getFieldByName('GRUP').strip()))
            grp_name=ic_util.recodeText(dbf_f.getFieldByName('NAMGRUP'),
                'CP866','CP1251')
            t_cod_str='0000' #dbf_f.getFieldByName('CODT').strip()
            if t_cod_str and grp_cod:
                try:
                    t_cod='%03d%04d'%(int(grp_cod),int(t_cod_str))
                except:
                    # print '### ValueError GROUP,CODT=', grp_cod, t_cod_str
                    grp_cod='000'
                    t_cod='0000'
            else:
                grp_cod='000'
                t_cod='0000'
            t_name=ic_util.recodeText(dbf_f.getFieldByName('NAMS'),
                'CP866','CP1251')
            ei_name=ic_util.recodeText(dbf_f.getFieldByName('EI'),
                'CP866','CP1251')
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

            reg_str=dbf_f.getFieldByName('REG').strip()
            reg_cod='%04d'%(int(reg_str))
            reg_name=ic_util.recodeText(dbf_f.getFieldByName('NAMREG'),
                'CP866','CP1251')

            men_str=dbf_f.getFieldByName('MENS').strip()
            men_cod='%04d'%(int(men_str))
            men_name=ic_util.recodeText(dbf_f.getFieldByName('NAMMENS'),
                'CP866','CP1251')

            #Загрузка данных
            i+=1
            #print idx
            tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
                ei=ei_name,kolf=kol,cena=cen,summa=sum,
                reg=reg_cod,mens=men_cod,
                plan_kol=None,plan_sum=None,
                office_cod=OfficeCod_)

            #Синхронизация справочников
            _syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
            _syncSpravRegions(reg_cod,reg_name)
            _syncSpravMenagers(men_cod,men_name)

        except:
            ic_log.icLogErr('ОШИБКА загрузки DBF %s файда в БД'%(DBFFileName_))

        ic_proccess_dlg.setProccessBoxLabel(value=float(100.0 / dbf_f.getRecCount()) * i)
        i+=1
        #progress.icStepThreadedProgressDlg()

        dbf_f.Next()

    #progress.icCloseThreadedProgressDlg()

    print 'OK'
    dbf_f.Close()

def preloadDataDBFStandart(DBFFileName_,ToTabName_,OfficeCod_):
    """
    Подготовка к загрузке.
    """
    #Определить начальную и конечную даты загрузки
    begin_end_date=getDateRange(DBFFileName_)
    if begin_end_date is None:
        return None
    begin_date,end_date=begin_end_date

    tab=ic_sqlobjtab.icSQLObjTabClass(ToTabName_)

    #Удалить данные перед загрузкой
    ok=delDateRangeInDB(tab,begin_date,end_date,OfficeCod_)
    if not ok:
        return None
    return (begin_date,end_date)

def postloadDataDBFStandart(DBFFileName_,BeginDate_,EndDate_,LogTab_):
    """
    Действия после загрузки.
    """
    if LogTab_:
        LogTab_.add(date_log=ic_time.TodayFmt('%Y.%m.%d'),
            begin_date=BeginDate_,end_date=EndDate_,
            office_cod=cod,office_name=rec['name'],
            file=cur_file)

@ic_proccess_dlg.proccess2_noparent_deco
def loadDataStandart():
    """
    Стандартная загрузка входных данных по всем офисам.
    """
    #Сначала определить все данны справочника.
    sprav=nsi.getSpravDictSimple('Office')
    if sprav is None:
        return

    #Таблица лога
    log=ic_sqlobjtab.icSQLObjTabClass('load_log')
    for cod,rec in sprav.items():
        try:
            imp_lst=rec['s2'].split('.')
            exec 'from %s import %s as load_func'%('.'.join(imp_lst[:-1]),imp_lst[-1])
        except:
            ic_log.icLogErr('Ошибка импорта функции загрузки %s'%(rec['s2']))
            return
        #Взять все файлы по маске
        files=ic_file.getFilesByMask(rec['s1'])
        files.sort()
        if files:
            begin_date,end_date=ic_time.MaxDayFmt('%Y.%m.%d'),ic_time.MinDayFmt('%Y.%m.%d')

            i=0
            try:
                count_100=float(100.0/len(files))
            except:
                count_100=0
            for cur_file in files:

                #Процесс бар
                ic_proccess_dlg.setProccessBoxLabel(cur_file, 0, label2='Загрузка данных', value2=count_100 * i)
                i+=1

                #Вызов функции загрузки данных
                load_date=load_func(cur_file,rec)

                #Архивация
                if rec['s3']:
                    ic_file.copyToDir(cur_file,rec['s3'])
                    ic_file.Remove(cur_file)
                else:
                    #Поменять расширение
                    ic_file.changeExt(cur_file, '.bak')
                #Прописать в логе
                if load_date:
                    log.add(date_log=ic_time.TodayFmt('%Y.%m.%d'),
                        begin_date=load_date[0],end_date=load_date[1],
                        office_cod=cod,office_name=rec['name'],
                        file=cur_file)
                #Зафиксировать диапазон изменений
                if load_date[0]:
                    begin_date=min(begin_date,load_date[0])
                if load_date[1]:
                    end_date=max(end_date,load_date[1])
            #Возвратить диапазон дат изменения для последующего разноса сумм
            if begin_date==ic_time.MaxDayFmt('%Y.%m.%d') or end_date==ic_time.MinDayFmt('%Y.%m.%d'):
                #Загрузка не прошла должным образом
                return None
            return (begin_date,end_date)
    return None

def refreshData(date_range=None):
    """
    Обновление данных в деревьях планов.
    """
    if date_range is None:
        date_range=std_dialogs.icDateRangeSTDDlg(glob_functions.getMainWin())

    if date_range:
        import analitic.planUtils as planUtils
        from analitic.metadatainterfaces import IMetaplan
        import plan.browsers as brws

        metaclass = IMetaplan.IMetaplan()
        plan_manager=brws.icPlanMenager(metaclass)
        #metaTree=IMetaplan.IMetaplan()

        #1. Сначала необходимо разнести базовый план
        begin_dt=ic_time.MonthDT(date_range[0],'%Y.%m.%d')
        end_dt=ic_time.MonthDT(date_range[1],'%Y.%m.%d')

        while begin_dt<=end_dt:
            year=begin_dt.year
            month=begin_dt.month
            planUtils.refreshSumm(metaclass.getObject(),year,month)
            begin_dt=ic_time.setDayDT(begin_dt+ic_time.OneMonthDelta(),1)

        #2. Затем произвести разнос сумм по модификациям
        begin_dt=ic_time.MonthDT(date_range[0],'%Y.%m.%d')
        end_dt=ic_time.MonthDT(date_range[1],'%Y.%m.%d')

        while begin_dt<=end_dt:
            year=begin_dt.year
            month=begin_dt.month
            planUtils.loadDataPlanModif(metaclass,year,month)
            begin_dt=ic_time.setDayDT(begin_dt+ic_time.OneMonthDelta(),1)

def loadData():
    """
    Загрузка данных.
    """
    date_range=loadDataStandart()
    if date_range<>None:
        if ic_dlg.getAskDlg('Разнос сумм', 'Были приняты данные с %s по %s. Разнести суммы за данный период?' % (date_range[0],
                                                                                                                 date_range[1]))==wx.YES:

            return refreshData(date_range)

#--- Функции специфические для каждого предприятия ---
def loadDataIC(DBFFileName_,SpravRecDict_):
    """
    Загрузка данных для ИнфоЦентра.
        У всех функций загрузки д.б. единый интерфейс!!!
    @return: Возвращает загруженный диапазон дат.
    """

    begin_end_date_analitic=preloadDataDBFStandart(DBFFileName_,'analitic',SpravRecDict_['cod'])
    if begin_end_date_analitic<>None:
        loadDataDBFStandart(DBFFileName_,'analitic',SpravRecDict_['cod'])
        begin_date_analitic,end_date_analitic=begin_end_date_analitic
    else:
        begin_date_analitic,end_date_analitic=None,None

    if preloadDataDBFStandart(DBFFileName_,'zayavki',SpravRecDict_['cod'])<>None:
        loadDataDBFStandart(DBFFileName_,'zayavki',SpravRecDict_['cod'])
    return (begin_date_analitic,end_date_analitic)

#--- Настроечные функции ---
def saveLoadDayCount(self):
    """
    Выбрать и сохранить диапазон загружаемых дат.
    """
    days=prs.ResultForm('day_count_dlg',
        parent=glob_functions.getMainWin())
    if days<>None:
        #load_day_count='0000.00.%02i'%(int(days))
        setLoadDayCount(days)

def getLoadDayCount():
    """
    Определить диапазон загружаемых дат.
    """
    prj_path=glob_functions.getVar('SYS_RES')
    ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
    return ic_ini.IniLoadParam(ini_file,
            'SETTINGS','load_day_count')

def setLoadDayCount(LoadDayCount_):
    """
    Сохранить в настроечном файле диапазон загружаемых дат.
    """
    #Заносить только проверенные значния
    if LoadDayCount_:
        prj_path=glob_functions.getVar('SYS_RES')
        ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
        return ic_ini.IniSaveParam(ini_file,
            'SETTINGS','load_day_count',LoadDayCount_)

def receiveDataAll():
    """
    Прием фактов.
    """
    loadData()

