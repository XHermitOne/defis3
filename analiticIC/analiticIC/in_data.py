#!/usr/bin/env python3
#  -*- coding: cp1251 -*-
"""
������ ���������� �������.
    ����������� ����������� ������� ���������� �� ��������/������ �����������.
    ���������� �������� ��������� � ��� ���������� Office.
    cod - 2-� ���������� ��� �����.
    s1 - �����/������ ����������� ������.
    s2 - ������� ��������. �������� in_data.loadDataDBFStandart.
    s3 - ����� �������, ���� ����������, ����� ����� ������� ��������
        ����� ����� ����������� � ���. ���� �� ����������, 
        �� ����� ������ ����� ����������������� � BAK �����.
�����(�): ����� ��������.
"""

# ������
__version__ = (0, 0, 0, 1)

#--- ����������� ��������� ---
import wx
#import datetime

import ic.db.dbf as dbf
import ic.log.ic_log as ic_log
import ic.dlg.ic_dlg as ic_dlg
#import ic.dlg.threaded_progress as progress
import ic.dlg.ic_proccess_dlg as ic_proccess_dlg

import ic.engine.ic_user as ic_user
import ic.utils.ic_file as ic_file
import ic.utils.ic_util as ic_util
import ic.utils.ic_time as ic_time
import ic.utils.ic_ini as ic_ini
#import ic.db.ic_sqlobjtab as ic_sqlobjtab
#from ic.db import ic_tabview
import ic.utils.resource as resource
#import NSI.spravfunc as nsi
import ic.components.icResourceParser as prs

import analitic.in_data as input_data
from STD import std_dialogs

#--- ������� (����������) ������ ---
def loadInputData(InputDataDir_=None):
    """
    ��������� ������� ������ � ��.
    @param InputDataDir_: ����� � ������� ����� �������.
    """
    if InputDataDir_ is None:
        InputDataDir_=input_data.getInputDataDir()
    
    #   ��������� ����� �� ����������
    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.olp')
    dbf_files.sort()
    print '--->>>loadInputData -> <analiticIC>',dbf_files,InputDataDir_ #,ic_file.ListDir(InputDataDir_)
    for dbf_file in dbf_files:
        print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file,'analitic')
        #�������� ����������
        #ic_file.icChangeExt(dbf_file,'_rlz.bak')
        
    #   ��������� ����� �� �������
    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.olp')
    dbf_files.sort()
    print '--->>>loadInputData -> <zayavkiIC>',dbf_files,InputDataDir_
    for dbf_file in dbf_files:
        print 'LOAD DATA FROM',dbf_file
        loadInputDataDBF(dbf_file, 'zayavki')
        #�������� ����������
        ic_file.icChangeExt(dbf_file,'.bak')
        #�������� � ����
        _logInputData(dbf_file)
    
    #   ��������� ����� �� ������
#    dbf_files=ic_file.GetFilesByExt(InputDataDir_,'.grp')
#    print '--->>>loadInputData -> <pay>', dbf_files,InputDataDir_
#    for dbf_file in dbf_files:
#        print 'LOAD DATA FROM',dbf_file
#        loadInputDataDBF(dbf_file, 'pay')
#        #�������� ����������
#        ic_file.icChangeExt(dbf_file,'_grp.bak')
    
    #print 'Refresh All Views'
    #refreshAllTabView()
        
def loadInputDataDBF(DBFFileName_, className='analitic'):
    """
    �������� ������� ������ �� dbf �����.
    """
    ### ������� ����������� �.
    #����
    #res=resource.icGetRes('analitic',nameRes='analitic')
    res=resource.icGetRes(className, nameRes=className)
    ###
    
    tab=ic_sqlobjtab.icSQLObjDataClass(res)
    #������� ������ ����� ���������
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
        #��������� ��� ������ �� ������
        try:
            dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
                '%Y.%m.%d')
            grp_cod='%03d'%(int(dbf_f.getFieldByName('GRUP').strip()))
            grp_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMGRUP'),
                'CP866','CP1251')
            t_cod_str='0000' #dbf_f.getFieldByName('CODT').strip()
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
            t_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMS'),
                'CP866','CP1251')
            ei_name=ic_util.ReCodeString(dbf_f.getFieldByName('EI'),
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
            reg_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMREG'),
                'CP866','CP1251')

            men_str=dbf_f.getFieldByName('MENS').strip()
            men_cod='%04d'%(int(men_str))
            men_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMMENS'),
                'CP866','CP1251')

            #�������� ������
            i+=1
            #recs=tab.select(ic_sqlobjtab.AND(tab.q.dtoper==dt_oper,
            #    tab.q.grup==grp_cod,tab.q.summa==sum,
            #    tab.q.reg==reg_cod,tab.q.mens==men_cod))
            #print i,recs
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

            #������������� ������������
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
    ������������� ������������ ������� ������ �� dbf �����.
    """
    #res=resource.icGetRes('analitic',nameRes='analitic')
    #tab=ic_sqlobjtab.icSQLObjDataClass(res)
    
    dbf_f=dbf.icDBFFile(DBFFileName_)
    dbf_f.Open()
    while not dbf_f.EOF():
        #��������� ��� ������ �� ������
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

        #������������� ������������
        _syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
        _syncSpravRegions(reg_cod,reg_name)
        _syncSpravMenagers(men_cod,men_name)
        
        #�������� ������
        #print '.',
        #tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
        #    ei=ei_name,kolf=kol,cena=cen,summa=sum,
        #    reg=reg_cod,mens=men_cod)
        
        dbf_f.Next()
    dbf_f.Close()


def _delLoadData(DBFFileName_,DataTab_):
    """
    ������� �� ������� ������� ������, ��������������� �����������.
    """
    try:
        #����������� ����, �� ������� ���������� �������� ������
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

#--- ������� ������������� ������������ ---
def _syncSprav(Type_,Cod_,Name_):
    """
    ������������� ������ �����������.
    @param Type: ��� �����������.
    @param Cod_: ���.
    @param Name_: ��������.
    """
    s_name=nsi.FSpravBuffRepl(Type_,Cod_)
    if s_name is None:
        #����� ��� ��������� �� ������
        #���� �������� ��� � ����������
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
#        name_=Name_.strip()
#        if s_name<>name_ and name_:
#            #���������� ��������
#            #���� ���������������� �� ������������
#            ic_log.icToLog('NSI %s CHANGE %s %s <> %s'%(Type_,Cod_,name_,s_name))
#            id=nsi.getSpravCodeId(Type_,Cod_)
#            if id<>None:
#                tab=ic_sqlobjtab.icSQLObjDataClass(resource.icGetRes('NsiStd',
#                    nameRes='NsiStd'))
#                tab.update(id,type=Type_,cod=Cod_,name=name_,id_nsi_list=nsi.getSpravId(Type_))
    
def _syncSpravProducts(GroupCod_,GroupName_,ProductCod_,ProductName_):
    """
    ������������� ������ ����������� ���������.
    """
    #������� ���������������� ���� ���������
    cod='%03d'%(int(GroupCod_))
    _syncSprav('Product',cod,GroupName_)
    #����� ���� ��������
    #cod='%03d%04d'%(int(GroupCod_),int(ProductCod_))
    #_syncSprav('Product',cod,ProductName_)

def _syncSpravRegions(RegCod_,RegName_):
    """
    ������������� ������ ����������� ��������.
    """
    #������� ���������������� ���� ���������
    cod='%04d'%(int(RegCod_))
    _syncSprav('Region',cod,RegName_)
    
def _syncSpravMenagers(MenCod_,MenName_):
    """
    ������������� ������ ����������� ����������.
    """
    #������� ���������������� ���� ���������
    cod='%03d'%(int(MenCod_))
    _syncSprav('Menager',cod,MenName_)

#--- ������� �������� ----
def getDateRange(DBFFileName_,DateFieldName_='DTOPER'):
    """
    ����������� ������������ ��������� ��� �� DBF �����. 
    @return: ���������� ������ ��������� � �������� ����. 
        ��� None � ������ ������.
    """
    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()
    if not bOpen:
        ic_log.icToLog('������ �������� ����� %s'%(DBFFileName_))
        return None
    #������������� ����������� � ������������ ���� �� ������ ������
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
    ������� ��������� �������� �� �� � ��������� ���������.
    """
    try:
        del_sql="""DELETE FROM %s
        WHERE (dtoper BETWEEN '%s' AND '%s') 
            AND office_cod='%s';"""%(DataTab_.getDBTableName(),
            BeginDate_,EndDate_,
            OfficeCode_)
        print 'SQL STRING:',del_sql
        DataTab_.executeSQL(del_sql)
        return True
    except:
        ic_log.icLogErr()
        return False


def loadDataDBFStandart(DBFFileName_,ToTabName_,OfficeCod_):
    """
    ����������� �������� DBF ����� � ��.
    """
    #res=resource.icGetRes(ToTabName_, nameRes=ToTabName_)
    
    tab=ic_sqlobjtab.icSQLObjTabClass(ToTabName_)
    
    dbf_f=dbf.icDBFFile(DBFFileName_)
    bOpen = dbf_f.Open()
    
    #ic_proccess_dlg.SetProccessBoxLabel(DBFFileName_, 0,label2='�������� ������', value2=10)
    #progress.icOpenThreadedProgressDlg('�������� ������',
    #    DBFFileName_,0,dbf_f.getRecCount())
    i=0
    #try:
    #    count_100=float(100/dbf_f.getRecCount())
    #except:
    #    count_100=0
    while not dbf_f.EOF():
        #��������� ��� ������ �� ������
        try:
            dt_oper=dbf_f.getDateFieldFmtByName('DTOPER',
                '%Y.%m.%d')
            grp_cod='%03d'%(int(dbf_f.getFieldByName('GRUP').strip()))
            grp_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMGRUP'),
                'CP866','CP1251')
            t_cod_str='0000' #dbf_f.getFieldByName('CODT').strip()
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
            t_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMS'),
                'CP866','CP1251')
            ei_name=ic_util.ReCodeString(dbf_f.getFieldByName('EI'),
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
            reg_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMREG'),
                'CP866','CP1251')

            men_str=dbf_f.getFieldByName('MENS').strip()
            men_cod='%04d'%(int(men_str))
            men_name=ic_util.ReCodeString(dbf_f.getFieldByName('NAMMENS'),
                'CP866','CP1251')

            #�������� ������
            i+=1
            #print i
            tab.add(dtoper=dt_oper,grup=grp_cod,codt=t_cod,
                ei=ei_name,kolf=kol,cena=cen,summa=sum,
                reg=reg_cod,mens=men_cod,
                plan_kol=None,plan_sum=None,
                office_cod=OfficeCod_)

            #������������� ������������
            _syncSpravProducts(grp_cod,grp_name,t_cod,t_name)
            _syncSpravRegions(reg_cod,reg_name)
            _syncSpravMenagers(men_cod,men_name)
        
        except:
            ic_log.icLogErr('������ �������� DBF %s ����� � ��'%(DBFFileName_))

        ic_proccess_dlg.SetProccessBoxLabel(value=float(100.0/dbf_f.getRecCount())*i)
        i+=1
        #progress.icStepThreadedProgressDlg()
        
        dbf_f.Next()

    #progress.icCloseThreadedProgressDlg()
    
    print 'OK'
    dbf_f.Close()

def preloadDataDBFStandart(DBFFileName_,ToTabName_,OfficeCod_):
    """
    ���������� � ��������.
    """
    #���������� ��������� � �������� ���� ��������
    begin_end_date=getDateRange(DBFFileName_)
    if begin_end_date is None:
        return None
    begin_date,end_date=begin_end_date

    tab=ic_sqlobjtab.icSQLObjTabClass(ToTabName_)
    
    #������� ������ ����� ���������
    ok=delDateRangeInDB(tab,begin_date,end_date,OfficeCod_)
    if not ok:
        return None
    return (begin_date,end_date)

def postloadDataDBFStandart(DBFFileName_,BeginDate_,EndDate_,LogTab_):
    """
    �������� ����� ��������.
    """
    if LogTab_:
        LogTab_.add(date_log=ic_time.TodayFmt('%Y.%m.%d'),
            begin_date=BeginDate_,end_date=EndDate_,
            office_cod=cod,office_name=rec['name'],
            file=cur_file)
    
@ic_proccess_dlg.proccess2_noparent_deco
def loadDataStandart():
    """
    ����������� �������� ������� ������ �� ���� ������.
    """
    #������� ���������� ��� ����� �����������.
    sprav=nsi.getSpravDictSimple('Office')
    if sprav is None:
        return
    
    #������� ����
    log=ic_sqlobjtab.icSQLObjTabClass('load_log')
    for cod,rec in sprav.items():
        try:
            imp_lst=rec['s2'].split('.')
            exec 'from %s import %s as load_func'%('.'.join(imp_lst[:-1]),imp_lst[-1])
        except:
            ic_log.icLogErr('������ ������� ������� �������� %s'%(rec['s2']))
            return
        #����� ��� ����� �� �����
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
                
                #������� ���
                ic_proccess_dlg.SetProccessBoxLabel(cur_file,0,label2='�������� ������', value2=count_100*i)
                i+=1

                #����� ������� �������� ������
                load_date=load_func(cur_file,rec)
                
                #���������
                if rec['s3']:
                    ic_file.copyToDir(cur_file,rec['s3'])
                    ic_file.Remove(cur_file)
                else:
                    #�������� ����������
                    ic_file.icChangeExt(cur_file,'.bak')
                #��������� � ����
                if load_date:
                    log.add(date_log=ic_time.TodayFmt('%Y.%m.%d'),
                        begin_date=load_date[0],end_date=load_date[1],
                        office_cod=cod,office_name=rec['name'],
                        file=cur_file)
                #������������� �������� ���������
                if load_date[0]:
                    begin_date=min(begin_date,load_date[0])
                if load_date[1]:
                    end_date=max(end_date,load_date[1])
            #���������� �������� ��� ��������� ��� ������������ ������� ����
            if begin_date==ic_time.MaxDayFmt('%Y.%m.%d') or end_date==ic_time.MinDayFmt('%Y.%m.%d'):
                #�������� �� ������ ������� �������
                return None
            return (begin_date,end_date)
    return None

def refreshData(date_range=None):
    """
    ���������� ������ � �������� ������.
    """
    if date_range is None:
        date_range=std_dialogs.icDateRangeSTDDlg(ic_user.icGetMainWin())
    
    if date_range:
        import analitic.planUtils as planUtils
        from analitic.metadatainterfaces import IMetaplan
        import plan.browsers as brws

        metaclass = IMetaplan.IMetaplan()
        plan_manager=brws.icPlanMenager(metaclass)
        #metaTree=IMetaplan.IMetaplan()
    
        #1. ������� ���������� �������� ������� ����
        begin_dt=ic_time.MonthDT(date_range[0],'%Y.%m.%d')
        end_dt=ic_time.MonthDT(date_range[1],'%Y.%m.%d')
        
        while begin_dt<=end_dt:
            year=begin_dt.year
            month=begin_dt.month
            planUtils.refreshSumm(metaclass.getObject(),year,month)
            begin_dt=ic_time.setDayDT(begin_dt+ic_time.OneMonthDelta(),1)
            
        #2. ����� ���������� ������ ���� �� ������������
        begin_dt=ic_time.MonthDT(date_range[0],'%Y.%m.%d')
        end_dt=ic_time.MonthDT(date_range[1],'%Y.%m.%d')
        
        while begin_dt<=end_dt:
            year=begin_dt.year
            month=begin_dt.month
            planUtils.loadDataPlanModif(metaclass,year,month)
            begin_dt=ic_time.setDayDT(begin_dt+ic_time.OneMonthDelta(),1)
    
def loadData():
    """
    �������� ������.
    """
    date_range=loadDataStandart()
    if date_range<>None:
        if ic_dlg.icAskDlg('������ ����','���� ������� ������ � %s �� %s. �������� ����� �� ������ ������?'%(date_range[0],
            date_range[1]))==wx.YES:

            return refreshData(date_range)
            
#--- ������� ������������� ��� ������� ����������� ---
def loadDataIC(DBFFileName_,SpravRecDict_):
    """
    �������� ������ ��� ����������.
        � ���� ������� �������� �.�. ������ ���������!!!
    @return: ���������� ����������� �������� ���.
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
    
#--- ����������� ������� ---
def saveLoadDayCount(self):
    """
    ������� � ��������� �������� ����������� ���.
    """
    days=prs.ResultForm('day_count_dlg',
        parent=ic_user.icGetMainWin())
    if days<>None:
        #load_day_count='0000.00.%02i'%(int(days))
        setLoadDayCount(days)
    
def getLoadDayCount():
    """
    ���������� �������� ����������� ���.
    """
    prj_path=ic_user.icGet('SYS_RES')
    ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
    return ic_ini.IniLoadParam(ini_file,
            'SETTINGS','load_day_count')

def setLoadDayCount(LoadDayCount_):
    """
    ��������� � ����������� ����� �������� ����������� ���.
    """
    #�������� ������ ����������� �������
    if LoadDayCount_:
        prj_path=ic_user.icGet('SYS_RES')
        ini_file=prj_path+'/'+ic_file.BaseName(prj_path)+'.ini'
        return ic_ini.IniSaveParam(ini_file,
            'SETTINGS','load_day_count',LoadDayCount_)

def receiveDataAll():
    """
    ����� ������.
    """
    loadData()
    
