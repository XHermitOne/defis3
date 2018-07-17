#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Дерево метакомпонентов.
Класс пользовательского визуального компонента.

@type ic_user_name: C{string}
@var ic_user_name: Имя пользовательского класса.
@type ic_can_contain: C{list | int}
@var ic_can_contain: Разрешающее правило - список типов компонентов, которые
    могут содержаться в данном компоненте. -1 - означает, что любой компонент
    может содержатся в данном компоненте. Вместе с переменной ic_can_not_contain
    задает полное правило по которому определяется возможность добавления других 
    компонентов в данный комопнент. 
@type ic_can_not_contain: C{list}
@var ic_can_not_contain: Запрещающее правило - список типов компонентов, 
    которые не могут содержаться в данном компоненте. Запрещающее правило
    начинает работать если разрешающее правило разрешает добавлять любой 
    компонент (ic_can_contain = -1).
"""

import wx
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.utils.resource as resource
from ic.kernel import io_prnt
from . import ic_metaitem_wrp
import ic.storage.objstore as objstore

# --- Спецификация ---
SPC_IC_METATREE = {'source': None,  # Хранилище дерева метакомпонентов
                   '__parent__': ic_metaitem_wrp.SPC_IC_METAITEM,
                   '__attr_hlp__': {'source': u'Хранилище дерева метакомпонентов',
                                    },
                   }

# --- Описание компонента для редактора ресурса ---
#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMetaTree'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaTree',
                'name': 'default', 
                'activate': True,
                'init_expr': None,
                '_uuid': None,
                'child': [],
                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'storage_type': [ic_metaitem_wrp.FILE_NODE_STORAGE_TYPE,
                                               ic_metaitem_wrp.FILE_STORAGE_TYPE,
                                               ic_metaitem_wrp.DIR_STORAGE_TYPE],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', 
                                                            'view_form', 'edit_form', 'print_report'],
                                    icDefInf.EDT_CHECK_BOX: ['container'],
                                    icDefInf.EDT_TEXTDICT: ['spc', 'const_spc'],
                                    icDefInf.EDT_CHOICE: ['storage_type'],
                                   }, 
                '__parent__': SPC_IC_METATREE,
                }

#   Имя иконки класса, которые располагаются в директории 
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMetaTree'
ic_class_pic2 = '@common.imgEdtMetaTree'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_metatree_wrp.icMetaTree-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['MetaItem', 'MetaConst', 'MetaAttr']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен 
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# --- Классы ---
class icMetaTreeEngine(ic_metaitem_wrp.icMetaItemEngine):
    """
    Дерево метакомпонентов. Управление.
    """
    def __init__(self, Resource_):
        """
        Конструктор.
        @param Resource_: Ресурс описания дерева метакомпонентов.
        """
        ic_metaitem_wrp.icMetaItemEngine.__init__(self, None, Resource_)
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
        if type(ObjectStorage_) in (str, unicode):
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
            io_prnt.outLog(u'MetaTree %s STORAGE: %s' % (self.name, self._storage))
            # Убить все дочерние объекты
            self.clearBuffChildren()
        return self._storage
        
    def getContainerMetaItems(self):
        """
        Список компонент, которые могут быть узлами дерева.
        """
        try:
            return dict([child for child in self.components.items() if issubclass(child[1].__class__, ic_metaitem_wrp.icMetaItemEngine)])
        except:
            io_prnt.outErr(u'Ошибка определения списка метаклассов в метадереве %s' % self.name)
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
            io_prnt.outLog(u'ВНИМАНИЕ!!! Метакомпонент %s в метадереве %s не найден!' % (MetaComponentName_, self.name))
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
                    io_prnt.outErr(u'Ошибка определения узла хранилища метаобъекта %s %s %s' % (Path_,
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
                    io_prnt.outErr(u'Ошибка сохранения узла хранилища метаобъекта %s %s %s' % (Path_,
                                                                                               CurStoreLevel_.getName(),
                                                                                               CurStoreLevel_.keys()))
                    return None
            elif len(Path_) == 1:
                try:
                    CurStoreLevel_[Path_[0]].save()
                    return CurStoreLevel_[Path_[0]]
                except:
                    io_prnt.outErr(u'!Ошибка сохранения узла хранилища метаобъекта %s %s %s' % (Path_,
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


class icMetaTree(icwidget.icSimple, icMetaTreeEngine):
    """
    Дерево метакомпонентов.
    """
    # Спецификаци компонента
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор.

        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        @type bCounter: C{bool}
        @param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        @type progressDlg: C{wx.ProgressDialog}
        @param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)
        icMetaTreeEngine.__init__(self, component)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)
