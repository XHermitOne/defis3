#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Каталог объектов в реляционной базе.
"""

from . import iccatalog
from ic.db.resources import iccatalogtable
from . import icdbpassport
from ic.kernel.icobject import icObjectPassport

# Шаблон описание источника данных 
src_tmpl = {}

# Разделитель элементов паспорта при хранении в базе
PSP_EL_DIV = ':'

__version__ = (0, 0, 1, 2)


def toNone(t):
    if t in (u'None', 'None'):
        return None
    return t
    

class icDBCatalog(iccatalog.icCatalog):

    def __init__(self, src, *arg, **kwarg):
        """ 
        Конструктор.
        @param src: Паспорт источника данных.
        """
        iccatalog.icCatalog.__init__(self)
        self.table = iccatalogtable.CatalogTable(None, src).getObject()
        self.ctg_refresh()
        
    def ctg_refresh(self, path=''):
        """ 
        Обновляем представление каталога
        """
        self._catalog = []
        rs = self.table.queryAll()
        for r in rs:
            cls = iccatalog.catalog_type_dct.get(r[3] or iccatalog.DEFAULT_OTYPE, None)
            if cls:
                pobj = self.val_to_psp(r[2])
                item = cls(r[1], pobj, r[4], r[5], r[5], r[6], id=r[0], catalog=self)
                self._catalog.append(item)

    def add_item(self, parent_item, name, item):
        """ 
        Добавление элемента в родительскую папку.
        @param parent_item: Родительский элемент. Если None, то элемент добавляется
            в корень каталога.
        """
        item = super(icDBCatalog, self).add_item(parent_item, name, item)        
        if item:
            # Прописываем в базе
            Tab = self.table.dataclass
            pobj = self.psp_to_val(item.pobj)
            c = Tab.insert().execute(path=item.path, pobj=pobj, 
                                     otype=item.catalog_type,
                                     title=item.title,
                                     description=item.description,
                                     reg_time=item.reg_time,
                                     act_time=item.act_time)
            return item
            
    @iccatalog.norm_path
    def remove(self, path):
        """ 
        Удалить объект из каталога.
        """
        item = self.get_item(path)
        if item and item.id:
            # Удаляем из базы
            tab = self.table.dataclass
            tab.delete(tab.c.id == item.id).execute()
            # Удаляем из буфера
            self._catalog.remove(item)
            
    @icdbpassport.to_db_passport
    def psp_to_val(self, psp):
        """ 
        Преобразования паспорта в значение поля. Значение вида:
            (('Document','doc1',None,'doc1.mtd','workflow'), id, uuid) пробразуется к виду
            <Document,doc1,None,doc1.mtd,workflow:[id]:[uuid]>
        @type psp: C{ic.kernrl.icobject.icObjectPassport}
        @param psp: Паспорт.
        """
        tt = psp[0]
        if len(psp) > 1:
            idt = str(psp[1])
        else:
            idt = ''
            
        if len(psp) > 2:
            uuidt = psp[2]
        else:
            uuidt = ''
            
        val = '%s,%s,%s,%s,%s:%s:%s' % (tt[0], tt[1], tt[2], tt[3], tt[4], idt, uuidt)
        return val

    def val_to_psp(self, val):
        """ 
        Преобразования значения поля в паспорт.
        @param val: Занчение поля.
        """
        lst = val.split(':')
        tt = [None, None, None, None, None]
        el = lst[0].split(',')
        try:
            tt[0] = el[0]
            tt[1] = el[1]
            tt[2] = el[2]
            tt[3] = el[3]
            tt[4] = el[4]
        except IndexError:
            pass
        tt = [toNone(t) for t in tt]
        lst[0] = tt
        try:
            lst[1] = lst[1]
        except IndexError:
            lst.append(None)
            
        if len(lst) == 2:
            lst.append(None)
            
        if lst[2] == '':
            lst[2] = None
            
        return icObjectPassport(*lst)
