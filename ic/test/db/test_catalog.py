#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Тестируем каталог."""
import unittest
from ic.kernel import icexceptions
from ic.db import iccatalog, icdbcatalog
import ic
prj_dir = '../testprj/testprj/'

#TODO: get_pobject(psp) - привести в правильный вид - функция должна возвращать объект
#TODO: Разобратся с функциональностью схем и источников данных - нужно объеты схем создавать
#      при первом обращении.

class TestCatalog(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        ic.Logout()

    def test_dbpassport(self):
        """ test dbpassport."""
        import ic.db.icdbpassport as dbp
        p1 = dbp.icDBPassport(('people', 1840, 'myPrj'), ('asdf12233566af00',))
        p2 = dbp.icDBPassport(('people', 1840, None))
        p3 = dbp.icDBPassport(('people', 1840))
        p4 = dbp.icDBPassport(('people', 1840, 'Err'))
        self.failUnlessEqual(p1, p2)
        self.failUnlessEqual(p2, p1)
        self.failUnlessEqual(p1, p3)
        self.failUnlessEqual(p3, p1)
        self.failUnlessEqual(p4 == p1, False)

    def test_get_object_psp(self):
        """ Тестируем функцию доступа к объекту данных по паспорту."""
        import ic.db.icdbpassport as dbp
        if ic.Login('user',None, prj_dir):
            psp = dbp.icDBPassport(('catalog', 1, None))
            r = dbp.get_object(psp)
            print('**** obj:', r, r.id, r.path, r.pobj)
            ic.Logout()

    def test_base_catalog(self):
        """ test std permission."""
        ct = iccatalog.icCatalog()
        ct.add('key', {'obj':None})
        ct.add('key/fld', {'obj':None})
        ct.add('key/fld1', {'obj':None})
        ct.add('key/fld/1', {'obj':None})
        ct.add('key/fld/2', {'obj':None})
        ct.add('key/fld/3', {'obj':None})
        ct.add('key/fld/4', {'obj':None})
        ct.add('key/fld1/1', {'obj':None})
        ct.add('key/fld1/2', {'obj':None})
        ct.add('key/fld1/3', {'obj':None})
        
        self.failUnlessEqual(len(ct.get_path_lst('/')), 10)
        self.failUnlessEqual(len(ct.get_path_lst('key')), 9)
        self.failUnlessEqual(len(ct.get_path_lst('key/')), 9)
        self.failUnlessEqual(len(ct.get_path_lst('/key')), 9)
        self.failUnlessEqual(len(ct.get_path_lst('/key/')), 9)
        self.failUnlessEqual(len(ct.get_path_lst('key/f')), 0)
        self.failUnlessEqual(len(ct.get_path_lst('key/fld')), 4)
        self.failUnlessEqual(len(ct.get_path_lst('key/fld1')), 3)
        self.failUnlessEqual(len(ct.get_path_lst('key/fld1/')), 3)
        
        # Список дочерних элементов
        self.failUnlessEqual('key' in ct.get_child_path_lst('/'), True)
        self.failUnlessEqual(len(ct.get_child_path_lst('key')), 2)
        self.failUnlessEqual(len(ct.get_child_path_lst('key2')), 0)
        self.failUnlessEqual('key/fld' in ct.get_child_path_lst('key'), True)
        self.failUnlessEqual('key/fld1' in ct.get_child_path_lst('key'), True)
        self.failUnlessEqual('key/fld1' in ct.get_child_path_lst('key/'), True)
        #print '****', ct.get_child_path_lst('/')
        
        self.failUnlessEqual(ct.get_parent_path('key'), '')
#        self.failUnlessEqual('add' in dct.keys(), True)

    def test_result_search(self):
        """ test icResultSearch."""
        lst = iccatalog.icListResultSearch([1,2,3,4,5])
        self.failUnlessEqual(lst[:], [1,2,3,4,5])
        ct = iccatalog.icCatalog()
        ct.add('key', {'obj':None})
        ct.add('key/fld', {'obj':None})
        ct.add('key/fld1', {'obj':None})
        ct.add('key/fld/1', {'obj':None})
        for i, el in enumerate(ct):
            if i==0:
                self.failUnlessEqual(el.path, 'key')
            elif i==1:
                self.failUnlessEqual(el.path, 'key/fld')
            elif i==2:
                self.failUnlessEqual(el.path, 'key/fld1')
            elif i==3:
                self.failUnlessEqual(el.path, 'key/fld/1')

    def test_filter(self):
        """ test search functions."""
        ct = iccatalog.icCatalog()
        ct.add('key', {'obj':None}, 'Folder')
        ct.add('key/fld', {'obj':None}, 'Folder')
        ct.add('key/fld1', {'obj':None}, 'Folder')
        ct.add('key/fld/1', {'obj':None}, 'Folder')
        ct.add('key/fld/2', {'obj':None}, 'object')
        ct.add('key/fld/3', {'obj':None}, 'object')
        ct.add('key/fld/4', {'obj':None})
        ct.add('key/fld1/1', {'obj':None})
        ct.add('key/fld1/2', {'obj':None})
        ct.add('key/fld1/3', {'obj':None})
        res = ct.filter_type('Folder')
        self.failUnlessEqual(type(res), iccatalog.icListResultSearch)
        self.failUnlessEqual(len(res), 4)
        res = ct.filter_type() # None type
        self.failUnlessEqual(len(res), 6)
        res = ct.filter_type('object')
        self.failUnlessEqual(len(res), 6)
                
        dct = ct.get_type_dct()
        self.failUnlessEqual(len(dct['Folder']), 4)
        self.failUnlessEqual(len(dct['object']), 6)
        #self.failUnlessEqual(len(dct[None]), 4)
        
        dct = ct.get_type_dct(['Folder', 'object', 'type3'])
        self.failUnlessEqual('Folder' in dct.keys(), True)
        self.failUnlessEqual('object' in dct.keys(), True)
        self.failUnlessEqual('type3' in dct.keys(), False)
        self.failUnlessEqual(None in dct.keys(), False)
        
    def test_db_catalog(self):
        """ Тестируем каталог, хранящийся в реляционной базе."""
        #prj_dir = '../testprj/testprj/'
        print('- prj_dir = ', prj_dir)
        if ic.Login('user',None, prj_dir):
            from ic.db.resources import iccatalogtable
            from sqlalchemy.sql import select

            src = (('SQLiteDB', 'testsrc', None, 'testsrc.src', 'testprj'),)
            tab = iccatalogtable.CatalogTable(None, src).getObject()
            cat = icdbcatalog.icDBCatalog(src)
            if not 'path' in cat.keys():
                #print '***** keys=', cat.keys()
                cat.add('path', (('Document', 'doc1', None, 'doc1.mtd', 'workflow'),'1'), 'Folder', 'title', 'description')
                
            cat.ctg_refresh()
            #print '***** keys=', cat.keys()
            self.failUnlessEqual('path' in cat.keys(), True)
            item = cat['path']
            self.failUnlessEqual(item.pobj.type, 'Document')
            self.failUnlessEqual(item.pobj.name, 'doc1')
            self.failUnlessEqual(item.pobj.interface, None)
            self.failUnlessEqual(item.pobj.mod, 'doc1.mtd')
            self.failUnlessEqual(item.pobj.subsys, 'workflow')
            self.failUnlessEqual(item.pobj.id, '1')
            self.failUnlessEqual(item.pobj.uuid, None)
                
            # Проверяем удаление
            cat.remove('path')
            self.failUnlessEqual('path' in cat.keys(), False)
            cat.ctg_refresh()
            self.failUnlessEqual('path' in cat.keys(), False)
            ic.Logout()

    def test_component_catalog(self):
        """ Тестируем компонент каталога."""
        if ic.Login('user',None, prj_dir):
            cat = ic.metadata.THIS.mtd.testcatalog.ObjectCatalog.create()
            print('--- cat=', cat.ctg_refresh)
            cat.table
            ic.Logout()
    
def start_unitest(par=0):
    if par == 0:
        unittest.main()
        return
        
    lst = [
        TestCatalog, 
    ]
    
    for cls in lst:
        print('--- %s tests:' % cls.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest(0)
    
