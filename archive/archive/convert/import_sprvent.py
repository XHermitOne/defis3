#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Импорт справочника контрагентов из бекапа БАЛАНС+.

ВНИМАНИЕ! Найден глюк библиотеки smbclient:
В списке файлов могут пропадать файлы большого размера.
Поэтому проверку на существование файла в SMB ресурсе не производим
а сразу пытаемся его загрузить.
"""

import os
import os.path
import smbclient
import urllib.parse

from ic.log import log
import ic
from ic.utils import ic_file
from ic.utils import filefunc

# Version
__version__ = (0, 1, 1, 1)


DEFAULT_WORKGROUP = 'WORKGROUP'

# Имя DBF файла справочника
# SPRVENT_FILENAME = 'SPRVENT.VNT'

PRJ_DIRNAME = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) if os.path.dirname(__file__) else os.path.dirname(os.path.dirname(os.getcwd()))
LOCAL_SPRVENT_FILENAME = os.path.join(PRJ_DIRNAME, 'db', 'SPRVENT.VNT')

# Список путей поиска DBF файла справочника
FIND_SMB_URLS = ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/SPRVENT.VNT',
                 # 'smb://xhermit@TELEMETRIA/share/install/SPRVENT.VNT',
                 )


def smb_download_sprvent(download_urls=None):
    """
    Найти и загрузить DBF справочник контрагентов.
    @param download_urls: Список путей поиска DBF файла справочника.
    @return: True - Произошла загрузка, False - ничего не загружено.
    """
    if download_urls is None:
        download_urls = FIND_SMB_URLS

    result = False
    smb = None
    for download_url in download_urls:
        try:
            url = urllib.parse.urlparse(download_url)
            download_server = url.hostname
            download_share = url.path.split(os.path.sep)[1]
            download_username = url.username
            download_password = url.password
            
            smb = smbclient.SambaClient(server=download_server,
                                        share=download_share,
                                        username=download_username,
                                        password=download_password,
                                        domain=DEFAULT_WORKGROUP)
            
            log.info(u'Установлена связь с SMB ресурсом')
            log.info(u'\tсервер <%s>' % download_server)
            log.info(u'\tпапка <%s>' % download_share)
            log.info(u'\tпользователь <%s>' % download_username)
            
            # Получить имена загружаемых файлов
            download_file = os.path.join(*url.path.split(os.path.sep)[2:])
            
            log.info(u'Загрузка файла <%s>' % download_file)
                
            if os.path.exists(LOCAL_SPRVENT_FILENAME):
                log.info(u'Удаление файла <%s>' % LOCAL_SPRVENT_FILENAME)
                os.remove(LOCAL_SPRVENT_FILENAME)
               
            # ВНИМАНИЕ! Найден глюк библиотеки smbclient:
            # В списке файлов могут пропадать файлы большого размера.
            # Поэтому проверку на существование файла в SMB ресурсе не производим
            # а сразу пытаемся его загрузить.
            try:
                smb.download(download_file, LOCAL_SPRVENT_FILENAME)
                log.info(u'Файл <%s> загружен' % download_file)
                result = True
            except:
                log.warning(u'''При возникновении ошибки в smbclient'e
возможно проблема в самой библиотеке pysmbclient.
Решение:
    В файле /usr/local/lib/python2.7/dist-packages/smbclient.py
    в вызове функции subprocess.Popen() убрать параметр <shell=True> 
    или поставить в False.
                ''')
                log.fatal(u'SMB. Ошибка загрузки SMB файла <%s>' % download_file)
                result = False
               
            smb.close()
            smb = None
            break        
        except:
            if smb:
                smb.close()
            log.fatal(u'Ошибка загрузки DBF файла справочника контрагентов из БАЛАНСА')
            result = False
            
    return result


def import_sprvent():
    """
    Ипортировать справочник контрагентов.
    """
    log.info(u'--- ЗАПУСК ИМПОРТА СПРАВОЧНИКА КОНТРАГЕНТОВ ---')
    # Сначала загрузить справочник из бекапа
    result = smb_download_sprvent()
    if result:
        # Успешно загрузили
        vnt_filename = LOCAL_SPRVENT_FILENAME
        dbf_filename = LOCAL_SPRVENT_FILENAME.replace('.VNT', '.DBF')
        if not filefunc.is_same_file_length(vnt_filename, dbf_filename):
            # Скопировать VNT в DBF
            if os.path.exists(dbf_filename):
                os.remove(dbf_filename)
            ic_file.icCopyFile(vnt_filename, dbf_filename)
            
            # Это другой файл
            tab = ic.metadata.THIS.tab.nsi_c_agent.create()
            tab.GetManager().set_default_data()
    
            # После заполнения справочника сбросить его кеш, 
            # чтобы отобразить изменения в уже запущенной программе
            spravmanager = ic.metadata.THIS.mtd.nsi_archive.create()
            sprav = spravmanager.getSpravByName('nsi_c_agent')
            sprav.clearInCache()
        else:
            log.debug(u'Справочник контрагентов уже загружен')
    else:
        log.warning(u'Ошибка связи с SMB ресурсом бекапа')


def test():
    """
    Тестирование.
    """
    from ic import config
    log.init(config)
    
    smb_download_sprvent()
    
    filefunc.is_same_file_length(LOCAL_SPRVENT_FILENAME, 
                                 LOCAL_SPRVENT_FILENAME.replace('.VNT', '.DBF'))
    
    
if __name__ == '__main__':
    test()