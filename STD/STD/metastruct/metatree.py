#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дерево метакомпонентов.
Класс пользовательского визуального компонента.
"""

from ic.log import log

import ic.utils.resource as resource
import ic.storage.objstore as objstore

try:
    from . import metaitem
except ImportError:
    import metaitem

# --- Спецификация ---
SPC_IC_METATREE = {'source': None,  # Хранилище дерева метакомпонентов
                   '__parent__': metaitem.SPC_IC_METAITEM,
                   '__attr_hlp__': {'source': u'Хранилище дерева метакомпонентов',
                                    },
                   }

#   Версия компонента
__version__ = (0, 1, 1, 1)


# --- Классы ---
class icMetaTreeEngine(metaitem.icMetaItemEngine):
    """
    Дерево метакомпонентов. Управление.
    """
    def __init__(self, Resource_):
        """
        Конструктор.
        @param Resource_: Ресурс описания дерева метакомпонентов.
        """
        metaitem.icMetaItemEngine.__init__(self, None, Resource_)
        # Определить хранилище данных
        self._object_storage_name = None
        self._storage = None
  
    def getStorage(self):
        """
        Определить хранилище данных.
        """
        if self._storage is None:
            object_storage = self.getICAttr('source')
            return self.setStorage(object_storage)
        return self._storage

    def setStorage(self, ObjectStorage_):
        """
        Установка хранилища данных.
        @param ObjectStorage_: Объект хранилища данных. Может передаваться
            по имени и в виде готового объекта.
        """
        if isinstance(ObjectStorage_, str):
            return self.setStorageByName(ObjectStorage_)
        else:
            if self._object_storage_name != ObjectStorage_.name:
                self._storage = ObjectStorage_
                self._object_storage_name = ObjectStorage_.name
                # Убить все дочерние объекты
                self.clearBuffChildren()
        return self._storage

    def setStorageByName(self, ObjectStorageName_):
        """
        Установка хранилища данных по имени.
        """
        if self._object_storage_name != ObjectStorageName_:
            # Нужно создать новое хранилище
            object_storage_res = resource.icGetRes(ObjectStorageName_,
                                                   'odb', nameRes=ObjectStorageName_)
            self._storage = None
            if object_storage_res:
                self._storage = objstore.icObjectStorage(object_storage_res)
                self._object_storage_name = ObjectStorageName_
            log.info(u'MetaTree %s STORAGE: %s' % (self.name, self._storage))
            # Убить все дочерние объекты
            self.clearBuffChildren()
        return self._storage
        
    def getContainerMetaItems(self):
        """
        Список компонент, которые могут быть узлами дерева.
        """
        try:
            return dict([child for child in self.components.items() if issubclass(child[1].__class__, metaitem.icMetaItemEngine)])
        except:
            log.error(u'Ошибка определения списка метаклассов в метадереве %s' % self.name)
            return {}
        
    def getContainerMetaItem(self, MetaComponentName_):
        """
        Взять метакомпонент, который может быть узлом дерева по имени.
        @param MetaComponentName_: Имя мета компонента-типа.
        """
        if self.name == MetaComponentName_:
            return self
        container_metacomponents = self.getContainerMetaItems()
        if MetaComponentName_ in container_metacomponents:
            return container_metacomponents[MetaComponentName_]
        else:
            log.info(u'ВНИМАНИЕ!!! Метакомпонент %s в метадереве %s не найден!' % (MetaComponentName_, self.name))
        return None

    def Save(self, MetaObject_=None):
        """
        Сохранить данные метакомпонента.
        @param MetaObject_: Сохраняемый метакомпонент.
            Если None, то значит надо сохранить себя.
        """
        if MetaObject_ is None:
            MetaObject_ = self
        metaobj_path = MetaObject_.getPath()
        if metaobj_path:
            parent_path = metaobj_path[:-1]
            self.setPath(parent_path, None, **{MetaObject_.name: MetaObject_})
        self.saveStoreNodeLevel(metaobj_path, MetaObject_, self.getStorage())
        # Сбросить признаки изменения значений и структуры мотаобъекта
        MetaObject_.setValueChanged(False)
        MetaObject_.setStructChanged(False)
        
    def Load(self, MetaObject_=None):
        """
        Загрузить данные компонента.
        @param MetaObject_: Загружаемый метакомпонент.
            Если None, то значит надо загрузить себя.
        """
        if MetaObject_ is None:
            MetaObject_ = self
        metaobj_path = MetaObject_.getPath()
        return self.LoadPath(metaobj_path, MetaObject_)
        
    def setPath(self, Path_, CurStoreLevel_, **MetaObjects_):
        """
        Установить данные метаобъектов по указанной ветке/пути в хранилище.
        @param Path_: Список имен метаобъектов/ветки.
        @param CurStoreLevel_: Текущий уровень хранилища. Если None, то корень.
        @param MetaObjects_: Сохраняемые метаобъекты.
        """
        if CurStoreLevel_ is None:
            CurStoreLevel_ = self.getStorage()
        if CurStoreLevel_ is not None:
            if len(Path_) > 0:
                return self.setPath(Path_[1:], CurStoreLevel_[Path_[0]], **MetaObjects_)
            else:
                # Подготовить данные для записи в хранилище
                data = {}
                for meta_obj in MetaObjects_.items():
                    if meta_obj[0] not in CurStoreLevel_:
                        data[meta_obj[0]] = meta_obj[1].createValueStorage(CurStoreLevel_)
                    else:
                        data[meta_obj[0]] = meta_obj[1].getStoreNodeLevel()
                        meta_obj[1].setValueStorage(data[meta_obj[0]])
                CurStoreLevel_.update(data)
                return True
        return False
        
    def LoadPath(self, Path_, MetaObject_, CurStoreLevel_=None):
        """
        Загрузить данные метаобъекта по указанной ветке/пути.
        @param Path_: Список имен метаобъектов/ветки.
        @param MetaObject_: Сохраняемый метаобъект
        """
        if CurStoreLevel_ is None:
            CurStoreLevel_ = self.getStorage()
        if CurStoreLevel_ is not None:
            if len(Path_) > 1:
                return self.LoadPath(Path_[1:],
                                     MetaObject_, CurStoreLevel_[Path_[0]])
            else:
                MetaObject_.setValue(CurStoreLevel_[Path_[0]])
                return True
        return False

    def getStoreNodeLevel(self, Path_=None, CurStoreLevel_=None):
        """
        Получить узел хранилища по пути.
        @param Path_: Путь.
        """
        if Path_ is None:
            Path_ = self.getPath()
        if CurStoreLevel_ is None:
            CurStoreLevel_ = self.getStorage()
        if CurStoreLevel_ is not None:
            if len(Path_) > 0:
                try:
                    return self.getStoreNodeLevel(Path_[1:], CurStoreLevel_[Path_[0]])
                except:
                    log.error(u'Ошибка определения узла хранилища метаобъекта %s %s %s' % (Path_,
                                                                                                CurStoreLevel_.getName(),
                                                                                                CurStoreLevel_.keys()))
                    return None
            else:
                return CurStoreLevel_
        return None
       
    def isStoreNodeLevel(self, Path_=None, CurStoreLevel_=None):
        """
        Проверить существует ли узел хранилища с таким путем.
        @param Path_: Путь.
        @return: True/False.
        """
        if Path_ is None:
            Path_ = self.getPath()
        if CurStoreLevel_ is None:
            CurStoreLevel_ = self.getStorage()
        if CurStoreLevel_ is not None:
            if len(Path_) > 0:
                return (Path_[0] in CurStoreLevel_ and \
                        self.isStoreNodeLevel(Path_[1:], CurStoreLevel_[Path_[0]]))
            else:
                return True
        return False
        
    def saveStoreNodeLevel(self, Path_=None, MetaObject_=None, CurStoreLevel_=None):
        """
        Сохранить узел хранилища по пути.
        @param Path_: Путь.
        @param MetaObject_: Сохраняемый метаобъект.
        """
        if MetaObject_ is None:
            MetaObject_ = self
        if Path_ is None:
            Path_ = self.getPath()
        if CurStoreLevel_ is None:
            CurStoreLevel_ = self.getStorage()
        if CurStoreLevel_ is not None:
            if len(Path_) > 1:
                try:
                    return self.saveStoreNodeLevel(Path_[1:], MetaObject_, CurStoreLevel_[Path_[0]])
                except:
                    log.error(u'Ошибка сохранения узла хранилища метаобъекта %s %s %s' % (Path_,
                                                                                               CurStoreLevel_.getName(),
                                                                                               CurStoreLevel_.keys()))
                    return None
            elif len(Path_) == 1:
                try:
                    CurStoreLevel_[Path_[0]].save()
                    return CurStoreLevel_[Path_[0]]
                except:
                    log.error(u'!Ошибка сохранения узла хранилища метаобъекта %s %s %s' % (Path_,
                                                                                                CurStoreLevel_.getName(),
                                                                                                CurStoreLevel_.keys()))
                    return None
            elif Path_ == []:
                CurStoreLevel_.save()
                return CurStoreLevel_
        return None
        
    def ReLoad(self):
        """
        Перечитать все объекты из хранилища.
        """
        if self.getStorage() is not None:
            self.getStorage().ReLoad()
        self.Build()

    def unLockAll(self):
        """
        Разблокировать все мои блокировки.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.unLockAllMy()
        return False
        
    def closeStorage(self):
        """
        Закрыть все файлы хранилища.
        """
        if self.getStorage():
            self.getStorage().closeAllFiles()
         
    def clearStorage(self):
        """
        Очистка хранилища. Удаляет содержимое папки хранилища.
        """
        storage = self.getStorage()
        if storage:
            storage.clearStorageDir()
        
    def setCache(self, Cache_=True):
        """
        Установить кэширование хранилища.
        """
        storage = self.getStorage()
        if storage:
            storage.setCache(Cache_)
        
    # --- Транзакционный механизм ---

    # --- Поддержка интерфейса словаря ---
