#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Тестируем функции безопасности."""
import unittest
from ic.kernel import icpermission
from ic.kernel import icaccesscontrol
from ic.kernel import icobject
from ic.kernel import icbaseuser
from ic.kernel import icbasekernel
from ic.kernel import icexceptions

class TestPermission(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_std_permission(self):
        """ test std permission."""
        dct = icpermission.getPermissionDct()
        self.failUnlessEqual('view' in dct.keys(), True)
        self.failUnlessEqual('edit' in dct.keys(), True)
        self.failUnlessEqual('add' in dct.keys(), True)

    def test_reg_permission(self):
        """ test reg permission."""
        icpermission.registerPermission(icpermission.icPermission('test','can test', 'can test', '__TEST__'))
        dct = icpermission.getPermissionDct()
        self.failUnlessEqual('test' in dct.keys(), True)
        prm = dct['test']
        self.failUnlessEqual(prm.id, 'test')
        self.failUnlessEqual(prm.title, 'can test')
        self.failUnlessEqual(prm.description, 'can test')
        self.failUnlessEqual(prm.type, '__TEST__')

class TestClassSecurityInfo(unittest.TestCase):
    """ Test ClassSecurityInfo"""
    def setUp(self):
        self.security = icaccesscontrol.ClassSecurityInfo()

    def test_declare(self):
        """ test declare method."""
        security = self.security
        security.declarePublic('meth1')
        self.failUnlessEqual('meth1' in security.names.keys(), True)
        self.failUnlessEqual(security.names['meth1'], 0)
        security.declarePrivate('meth2')
        self.failUnlessEqual(security.names['meth2'], 1)
        security.declareProtected('view', 'meth3')
        self.failUnlessEqual(security.names['meth3'], 'view')
    
    def test_access(self):
        """ test access."""
        class TestObject(icobject.icObject):
            #security = self.security
            security = icaccesscontrol.ClassSecurityInfo()
            security.declareProtected('view', 'ViewObject')
            def ViewObject(self):
                pass
            security.declareProtected('view2', 'ViewObject2')
            def ViewObject2(self):
                pass
            security.declarePrivate('ViewObject3')
            def ViewObject3(self):
                pass

        obj = TestObject()
        obj.ViewObject()
        
        kernel = icbasekernel.icBaseKernel()
        kernel.Login('root', None)
        obj.context.kernel = kernel
        obj.ViewObject()
        
        try:
            obj.ViewObject2()
            raise AttributeError('Proected attribute error') 
        except icexceptions.MethodAccessDeniedException:
            pass

        try:
            obj.ViewObject3()
            raise AttributeError('Private attribute error') 
        except icexceptions.MethodAccessDeniedException:
            pass
            
        kernel.Logout()
        
class TestUser(unittest.TestCase):
    def test_create_user_root(self):
        """ Test to create root user."""
        root = icbaseuser.icRootUser()
        try:
            root.Login('user')
        except icexceptions.LoginInvalidException:
            pass
        except:
            self.failUnlessEqual('Root login', False)
            
        root.Login('root')
        self.failUnlessEqual(root.getRoles()[0].id, 'Admin')
        # Проверяем, что роли readonly атрибут
        try:
            root.roles = []
            raise NotImplementedError('Readonly Attribute Error')
        except AttributeError:
            pass
        # Проверяем, что разрешения readonly атрибут
        try:
            root.getRoles()[0].permissions = []
            raise NotImplementedError('Readonly Attribute Error')
        except AttributeError:
            pass
            
        lst = [el.id for el in root.getPermissions()]
        self.failUnlessEqual('view' in lst, True)
        self.failUnlessEqual('edit' in lst, True)
        self.failUnlessEqual('add' in lst, True)
        self.failUnlessEqual('delete' in lst, True)
        self.failUnlessEqual('view2' in lst, False)
                
class TestBaseKernel(unittest.TestCase):
    def test_base_kernel(self):
        """ Test base kernel."""
        kernel = icbasekernel.icBaseKernel()
        try:
            kernel.Login('user', None)
        except icexceptions.LoginInvalidException:
            pass
        
        kernel.Login('root', None)
        root = kernel.getUser()
        self.failUnlessEqual(root.getRoles()[0].id, 'Admin')
        #print '>>> context=', kernel.context.get_kernel()
        kernel.Logout()
        user = kernel.getUser()
        self.failUnlessEqual(user, None)
    
def start_unitest(par=0):
    if par == 0:
        unittest.main()
        return
        
    lst = [
        TestPermission, 
        TestClassSecurityInfo,
        TestUser,
        TestBaseKernel,
    ]
    
    for cls in lst:
        print('--- %s tests:' % cls.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    start_unitest(0)
    
