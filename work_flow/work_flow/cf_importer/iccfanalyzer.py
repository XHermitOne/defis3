#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс анализитора конфигураци.
"""

from . import iccfdirmanager
from .cf_obj import iccfobject

from ic.log import log

__version__ = (0, 0, 0, 3)


class icCFAnalyzer:
    """
    Класс анализитора конфигураци.
    """
    def __init__(self, cf_dirname=None):
        """
        Конструктор.
        @param cf_dirname: Имя папки конфигурации 1с.
        """
        self.cf_dir_manager = iccfdirmanager.icCFDirManager(cf_dirname)

        # Список объектов конфигурации
        self.cf_list = None
        
    def createCFList(self, cf_dirname=None):
        """
        Создать список объектов конфигурации 1с.
        @param cf_dirname: Имя папки конфигурации 1с.
        """
        if cf_dirname:
            self.cf_dir_manager.buildMetaObjects(cf_dirname)
        else:
            self.cf_dir_manager.buildMetaObjects()
        
        self.cf_list = self._createCFList(self.cf_dir_manager.cf_root)
        return self.cf_list
        
    def _createCFList(self, root):
        """
        Создать список объектов конфигурации 1с.
        """
        result = list()

        # log.debug(u'Создание списка объектов <%s> конфигурации 1С' % root.name)
        if root:
            for child in root.children:
                obj = dict()
                name = unicode(str(child.name), 'utf-8') if not isinstance(child.name, unicode) else child.name
                obj['name'] = name
                obj['img'] = child.getImage()
                obj['img_exp'] = child.getImageExpand()
                obj['checkable'] = True
                obj['check'] = True
                obj['__record__'] = (child.uid, name)
                obj['children'] = self._createCFList(child)
            
                result.append(obj)
                
        return result
    
    def getMetaobjects(self, cf_list):
        """
        Получить список метаобъектов по списку описаний объектов конфигурации 1с.
        """
        metaobjects = list()
        for cf_child in cf_list:
            checked = cf_child.get('check', False)
            uid = cf_child['__record__'][0]
            if checked:
                if uid != iccfobject.NONE_UID:
                    metaobject = self.cf_dir_manager.cf_root.findByUID(uid)
                    if metaobject:
                        metaobjects.append(metaobject)
                
            if 'children' in cf_child and cf_child['children']:
                metaobjects += self.getMetaobjects(cf_child['children'])
        return metaobjects

    def getRootMetaobject(self):
        """
        Корневой метаобъект.
        """
        return self.cf_dir_manager.cf_root
