#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Заполнение классификатора адресов РФ <KLADR>.
"""

import os
import os.path
import wx

from ic import ic_dlg
from ic import log
from ic.db import dbf
from ic.utils import ic_str

from . import config

# Version
__version__ = (0, 0, 0, 1)

# Constants

DEFAULT_KLADR_DBF_FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          'NSI', 'db', 'KLADR.dbf')

DEFAULT_DBF_ENCODE = 'cp866'

# Functions


def addKLADRSpravRecord(sprav, code, name, socr):
    """
    Добавить запись в справочник населенных пунктов
    @param sprav: Объект справочника.
    @param code: Структурный код.
    @param name: Наименование.
    @param socr: Сокращение.
    """
    rec = dict()
    cod = ''.join(code)
    rec['name'] = name
    rec['s1'] = socr
                
    if not sprav.isCod(cod):
        sprav.addRec(cod, rec)
                    
    if len(code) == 1:
        # При заполнении региона сразу установить прочее
        rrr_cod = cod+'000'
        if not sprav.isCod(rrr_cod):
            sprav.addRec(rrr_cod, {'name': u'----'})
            ggg_cod = rrr_cod+'000'
            if not sprav.isCod(ggg_cod):
                sprav.addRec(ggg_cod, {'name': u'----'})
    if len(code) == 2:
        # При заполнении района сразу установить прочее
        ggg_cod = cod+'000'
        if not sprav.isCod(ggg_cod):
            sprav.addRec(ggg_cod, {'name': u'----'})
    return sprav
    

def setKLADRData(sprav_manager, is_progress=False):
    """
    Основная функция заполнения.
    @param sprav_manager: Менеджер справочников.
    """
    log.debug('Set default data. Sprav manager <%s>' % sprav_manager)
    log.debug('KLADR dbf file name <%s>' % DEFAULT_KLADR_DBF_FILENAME)

    if not os.path.exists(DEFAULT_KLADR_DBF_FILENAME):
        log.warnnig('KLADR DBF file <%s> not found' % DEFAULT_KLADR_DBF_FILENAME)
        return
        
    if sprav_manager:
        
        if is_progress:
            ic_dlg.icOpenProgressDlg(wx.GetApp().GetTopWindow(), 
                                     u'Загрузка данных KLADR', 
                                     u'Загрузка данных о населенных пунктах', 
                                     0, 100)
        else:
            log.debug('Start set KLADR data')
        
        try:
            sprav = sprav_manager.getSpravByName('nas_punkts')
            # Сначала очистить справочник
            sprav.Clear(True)
            
            kladr_dbf = dbf.icDBFFileDBFPY(DEFAULT_KLADR_DBF_FILENAME)
            kladr_dbf.Open()
            i = 0
            while not kladr_dbf.EOF():
                str_code = kladr_dbf.getFieldByName('CODE')
                code = splitKLADRCode(str_code)[:4]
                str_socr = unicode(kladr_dbf.getFieldByName('SOCR'), DEFAULT_DBF_ENCODE)
                name = unicode(kladr_dbf.getFieldByName('NAME'), DEFAULT_DBF_ENCODE)
                log.info('[%d] %s\t%s\t%s\t%s' % (i, str_code, name, str_socr, code))
                kladr_dbf.Next()
                
                addKLADRSpravRecord(sprav, code, name, str_socr)
                
                i += 1 
            
            kladr_dbf.Close()
        except:
            kladr_dbf.Close()
            log.error('Set KLADR data')
            raise

        if is_progress:
            ic_dlg.icCloseProgressDlg()
        else:
            log.debug('Stop set KLADR data')


def splitKLADRCode(str_code):
    """
    Разделить код KLADR (СС РРР ГГГ ППП АА) на составляющие:
    СС – код субъекта Российской Федерации (региона);
    РРР – код района;
    ГГГ – код города;      
    ППП – код населенного пункта,
    АА – признак актуальности адресного объекта.
    """
    code = list()
    cc = str_code[:2]
    code.append(cc)
    if not ic_str.is_serial_zero(str_code[2:]):
        rrr = str_code[2:5]
        code.append(rrr)
        if not ic_str.is_serial_zero(str_code[5:]):
            ggg = str_code[5:8]
            code.append(ggg)
            if not ic_str.is_serial_zero(str_code[8:]):
                ppp = str_code[8:11]
                code.append(ppp)
                if not ic_str.is_serial_zero(str_code[11:]):
                    aa = str_code[11:]
                    code.append(aa)
    return tuple(code)
    
    
def printKLADRData():
    """
    Просмотр данных классификатора.
    """
    global DEFAULT_KLADR_DBF_FILENAME
    
    if not os.path.exists(DEFAULT_KLADR_DBF_FILENAME):
        DEFAULT_KLADR_DBF_FILENAME = os.path.join(os.path.dirname(os.getcwd()), 'db', 'KLADR.dbf')
    if not os.path.exists(DEFAULT_KLADR_DBF_FILENAME):
        log.warning('DBF file <%s> not found' % DEFAULT_KLADR_DBF_FILENAME)
        
    log.debug('--- Print KLADR data ---')
    log.debug('KLADR dbf file name <%s>' % DEFAULT_KLADR_DBF_FILENAME)
    log.debug('Start print KLADR data')
        
    try:
        # sprav = sprav_manager.getSpravByName('nas_punkts')
        kladr_dbf = dbf.icDBFFileDBFPY(DEFAULT_KLADR_DBF_FILENAME)
        kladr_dbf.Open()
        i = 0
        while not kladr_dbf.EOF():
            str_code = kladr_dbf.getFieldByName('CODE')
            code = splitKLADRCode(str_code)
            str_socr = unicode(kladr_dbf.getFieldByName('SOCR'), DEFAULT_DBF_ENCODE)
            name = unicode(kladr_dbf.getFieldByName('NAME'), DEFAULT_DBF_ENCODE)
            log.info('[%d] %s\t%s\t%s\t%s' % (i, str_code, name, str_socr, code))
            kladr_dbf.Next()
            i += 1 
            
        kladr_dbf.Close()
    except:
        kladr_dbf.Close()
        log.error('Print KLADR data')
        raise

    log.debug('Stop print KLADR data')


def test():
    """
    Функция тестирования.
    """
    log.init(config)
    
    printKLADRData()
    
    
if __name__ == '__main__':
    test()