#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс корневого элемента конфигурации.
"""

import os
import os.path

from . import iccfobject
from . import iccfresource
from . import iccfconfiguration

from ic.dlg import wait_box
from ic.log import log
from ic.dlg import ic_dlg
import ic

__version__ = (0, 0, 1, 1)


class icCFRoot(iccfobject.icCFObject):
    """
    Класс корневого элемента конфигурации.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)

        self.img_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                         'img', '1c.png')

    @wait_box.wait_noparentdeco
    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        try:
            cf_root_filename = os.path.join(os.path.abspath(self.cf_dir), 'metadata', 'root')
            if not os.path.exists(cf_root_filename):
                cf_root_filename = os.path.join(os.path.abspath(self.cf_dir), 'root')
            if not os.path.exists(cf_root_filename):
                log.warning(u'Не найден файл <%s>' % cf_root_filename)
                return

            cf_root_res = iccfresource.icCFResource(cf_root_filename)
            cf_root_res.loadData(cf_root_filename)
        
            # Построение конфигурации
            uid_cfg = cf_root_res.data[1] if cf_root_res.data else None

            cfg = iccfconfiguration.icCFConfiguration(self, uid_cfg)
            cfg.build()
        
            self.children = [cfg]
        except:
            log.fatal(u'Ошибка постороения дерева метаобъектов')

    def getConfiguration(self):
        """
        Объект конфигурации.
        """
        if self.children:
            return self.children[0]
        return None

    DEFAULT_DB_PSP = None

    def _get_db_psp(self, prj_res_ctrl=None):
        """
        Определить паспорт БД проекта.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return:
        """
        if prj_res_ctrl:
            db_resources = prj_res_ctrl.getResourcesByType('src')
            if not db_resources:
                log.warning(u'Не обнаружены ресурсы описания БД для генерации таблицы')
            elif len(db_resources) == 1:
                # У нас 1 ресурс описания БД надо сгенерировать его паспорт
                res = db_resources[0]
                db_psp = ((res['type'], res['name'], None, '%s.src' % res['name'], ic.getPrjName()), )
                return db_psp
            else:
                # Несколько ресусов БД, определить у выше стоящего объекта
                if self.DEFAULT_DB_PSP:
                    return self.DEFAULT_DB_PSP
                else:
                    choices = [u'%s (%s)' % (db_res['name'], db_res['description']) for db_res in db_resources]
                    idx = ic_dlg.icSingleChoiceDlg(Title_=u'БД',
                                                   Text_=u'Выбор БД для генерации ресусов таблиц',
                                                   Choice_=choices)
                    res = db_resources[idx] if idx >= 0 else None
                    db_psp = ((res['type'], res['name'], None, '%s.src' % res['name'], ic.getPrjName()),) if res else None
                    self.DEFAULT_DB_PSP = db_psp
                    return self.DEFAULT_DB_PSP
        return None
