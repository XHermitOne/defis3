#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Интерфейс к однофайловой объектной справочной системе.

@type sprav_file_name: C{string}
@var sprav_file_name: Имя файла, где хранится основной справочник.
@type sprav_log_file_name: C{string}
@var sprav_log_file_name: Имя файла, где хранятся все изменения справочника.
"""
import wx
import ic.components.icResourceParser as prs
import ic.utils.util as util
import ic.interfaces.icobjectinterface as icobjectinterface
import ic.utils.ic_cache as ic_cache
import time

### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'pic': None, 'report': None, 'storage_type': u'DirStorage', 'spc': {}, 'description': u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0430\u043f\u043a\u0438 \u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'source': u'odb_sprav', 'init': None, 'can_not_contain': None, 'type': u'MetaTree', 'const_spc': {}, '_uuid': u'1d01016c8e6ea9da7af385629f37746e', 'child': [{'activate': 1, 'pic': None, 'report': None, 'storage_type': u'FileStorage', 'spc': {}, 'description': u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u0438\u043f\u0430 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430\r\n{'data': <\u043e\u0431\u044a\u0435\u043a\u0442 \u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f>}\r\n", 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {}, '_uuid': u'bf8003a8f2897989b29024ee64436140', 'child': [], 'can_contain': u"['spravListItem', 'spravLogItem']", 'edit_form': None, 'name': u'spravType', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'report': None, 'storage_type': u'FileNodeStorage', 'spc': {'data': []}, 'description': u'\u041e\u0431\u044a\u0435\u043a\u0442 \u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f \u0434\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043d\u043e\u0433\u043e \u0442\u0438\u043f\u0430. \u0414\u0430\u043d\u043d\u044b\u0435\r\n\u0445\u0440\u0430\u043d\u044f\u0442\u0441\u044f \u0432 \u0432\u0438\u0434\u0435 \u0441\u043f\u0438\u0441\u043a\u0430 \u043a\u043e\u0440\u0442\u0435\u0436\u0435\u0439.\r\n', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {}, '_uuid': u'50a7a0065b1bfaf676f10c2e7dea3249', 'child': [], 'can_contain': None, 'edit_form': None, 'name': u'spravListItem', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}, {'activate': 1, 'pic': None, 'can_contain': None, 'storage_type': u'FileNodeStorage', 'spc': {'data': [], 'log': {}}, 'description': u'\u041e\u0431\u044a\u0435\u043a\u0442 \u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f \u0434\u0430\u043d\u043d\u044b\u0445 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0430 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043d\u043e\u0433\u043e \u0442\u0438\u043f\u0430. \u0414\u0430\u043d\u043d\u044b\u0435\r\n\u0445\u0440\u0430\u043d\u044f\u0442\u0441\u044f \u0432 \u0432\u0438\u0434\u0435 \u0441\u043b\u043e\u0432\u0430\u0440\u044f. \u041a\u043b\u044e\u0447\u0438 - \u043a\u043e\u0434\u044b, \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0441\u043f\u0438\u0441\u043e\u043a, \u043a\u0430\u0440\u0442\u0435\u0436\u0435\u0439.\r\n\u041a\u0430\u0440\u0442\u0435\u0436 \u0445\u0440\u0430\u043d\u0438\u0442 \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u0430 \u043e\u043f\u0440\u0434\u0435\u043b\u0435\u043d\u043d\u044b\u0439 \u043f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u043a \u0432\u0440\u0435\u043c\u0435\u043d\u0438.\r\n\u0412\u0440\u0435\u043c\u044f \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u0441\u0442\u0440\u043e\u043a\u0438 \u0445\u0440\u0430\u043d\u0438\u0442\u0441\u044f \u0432 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u043c \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0435 \u043a\u0430\u0440\u0442\u0435\u0436\u0430.\r\n\r\n\r\n', 'style': 0, 'container': True, 'component_module': None, 'pic2': None, 'init': None, 'can_not_contain': None, 'type': u'MetaItem', 'const_spc': {}, '_uuid': u'24edcb627ee7961072cf7abdcffeafee', 'child': [], 'report': None, 'edit_form': None, 'name': u'spravLogItem', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}], 'can_contain': None, 'edit_form': None, 'name': u'NsiTree', 'doc': None, 'alias': None, 'del': None, 'init_expr': None, 'view_form': None}

#   Версия объекта
__version__ = (1, 0, 2, 8)
###END SPECIAL BLOCK

#   Имя класса
ic_class_name = 'IODBNsi'

#   Имя файла, где хранится основной справочник
sprav_file_name = 'sprav'
sprav_item_type = 'spravType'
data_item_type = 'spravListItem'
log_item_type = 'spravLogItem'

#   Имя файла изменений
sprav_log_file_name = 'spravLog'
log_item_type = 'spravLogItem'

class IODBNsi(icobjectinterface.icObjectInterface):
    def __init__(self, parent, spravObj=None, DBName_=None,TabName_=None):
        """
        Конструктор интерфейса.
        
        @param SpravObj: Объект справочника.
        """
        # Имя источника
        self.db = DBName_
        # Имя таблицы
        self.table = TabName_
        # Объект справочника
        self.sprav = spravObj
        
        if self.sprav:
            self.spravName = self.sprav.name
        else:
            self.spravName = 'Default'
            
        self.metaSprav = None
        self.metaSpravLog = None
        #   Вызываем конструктор базового класса
        icobjectinterface.icObjectInterface.__init__(self, parent, resource)

        #   Указатель на NSI
        self.nsi = self.getObject()
        self.init_sprav()
        #self.close()
        
    def init_sprav(self):
        """
        """
        
#        print ' CREATE IODBSpravObject', obj
        if sprav_file_name not in self.nsi:
            obj = self.nsi.Add(sprav_file_name, sprav_item_type)
            log_obj = self.nsi.Add(sprav_file_name+'_log', sprav_item_type)
            self.metaSprav = obj.Add(self.spravName, data_item_type)
            self.metaSpravLog = log_obj.Add(self.spravName, log_item_type)
        else:
            #print '*** keys=', self.nsi[sprav_file_name].keys()
            t1 = time.clock()
            self.metaSpravLog = self.nsi[sprav_file_name+'_log'][self.spravName]
            self.metaSprav = self.nsi[sprav_file_name][self.spravName]
            t2 = time.clock()
            print('Init Sprav time=%f сек.' % (t2-t1))
            #print 'data=', self.metaSprav.value.data
 
    def close(self):
        """
        Закрывает хранилище справочника.
        """
        if self.metaSprav:
            self.metaSprav.closeStorage()
#
#        obj['sprav1'].value.data = {'AAAA':[1,2,7]}
#        obj['sprav1'].setValueChanged(True)
#        obj['sprav1'].Save()
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

    
def test(par=0):
    """
    Тестируем класс new_form.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()