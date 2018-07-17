#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Метакомпонент.
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
    
@type SPC_IC_METAITEM: C{dict}
@var SPC_IC_METAITEM: Спецификация на ресурсное описание метакласса. Описание ключей:

    - B{name = 'default'): Имя.
    - B{metatype = None): Указание имени метатипа, из которого порожден метаобъект, Если None, то сам является метатипом.
    - B{description = None): Описание.
    - B{spc = {}): Значение спецификации метакомпонента.
    - B{const_spc = {}): Постоянные значения спецификации метакомпонента.
    - B{view_form = None): Форма чтения/просмотра.
    - B{edit_form = None): Форма редактирования/записи.
    - B{report = None): Форма печати/отчет.
    - B{storage_type = 'DirStorage'): Тип хранилища метакомпонента.
    - B{container = True): Признак контейнера.
    - B{pic = None): Образ метакомпонента.
    - B{pic2 = None): Дополнительный образ метакомпонента.
    - B{doc = None): Файл документации компонента.
    - B{can_contain = None): Разрешающее правило вкличения.
    - B{can_not_contain = None): Запрещающее/bc правило - список типов компонентов,
        #которые не могут содержаться в данном компоненте. Запрещающее правило
        #начинает работать если разрешающее правило разрешает добавлять любой
        #компонент (can_contain = -1).
    - B{init = None): Блок кода, выполняемый при создании метаобъекта
    - B{del = None): Блок кода, выполняемый при удалении метаобъекта
"""

import wx
import copy
import ic.components.icwidget as icwidget
import ic.utils.util as util
import ic.components.icResourceParser as prs
import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

import ic.dlg.ic_dlg as ic_dlg
from ic.kernel import io_prnt
import ic.interfaces.Persistent as persistent
import ic.storage.storesrc as storesrc
import ic.utils.clipboard as clipboard
from . import ic_metaconst_wrp
from . import ic_metaattr_wrp

# --- Спецификация ---
FILE_NODE_STORAGE_TYPE = 'FileNodeStorage'
FILE_STORAGE_TYPE = 'FileStorage'
DIR_STORAGE_TYPE = 'DirStorage'

SPC_IC_METAITEM = {'name': 'default',       # Имя
                   'description': None,     # Описание
                   'spc': {},               # Значение спецификации метакомпонента
                   'const_spc': {},         # Постоянные значения спецификации метакомпонента
                   'view_form': None,       # Форма чтения/просмотра
                   'edit_form': None,       # Форма редактирования/записи
                   'report': None,          # Форма печати/отчет
                   'storage_type': DIR_STORAGE_TYPE,    # Тип хранилища метакомпонента
                   'container': True,       # Признак контейнера
                   'pic': None,             # Образ метакомпонента
                   'pic2': None,            # Дополнительный образ метакомпонента
                   'doc': None,             # Файл документации компонента
                   'can_contain': None,     # Разрешающее правило - список типов компонентов, которые
                                            # могут содержаться в данном компоненте. -1 - означает, что любой компонент
                                            # может содержатся в данном компоненте. Вместе с переменной can_not_contain
                                            # задает полное правило по которому определяется возможность добавления других
                                            # компонентов в данный комопнент.
                   'can_not_contain': None,     # Запрещающее правило - список типов компонентов,
                                                # которые не могут содержаться в данном компоненте. Запрещающее правило
                                                # начинает работать если разрешающее правило разрешает добавлять любой
                                                # компонент (can_contain = -1).
                    'init': None,   # Блок кода, выполняемый при создании метаобъекта
                    'del': None,    # Блок кода, выполняемый при удалении метаобъекта

                    'gen_new_name': None,   # Блок генерации нового имени метаобъекта
                    '__parent__': icwidget.SPC_IC_SIMPLE,
                    '__attr_hlp__': {'name': u'Имя',
                                     'description': u'Описание',
                                     'spc': u'Значение спецификации метакомпонента',
                                     'const_spc': u'Постоянные значения спецификации метакомпонента',
                                     'view_form': u'Форма чтения/просмотра',
                                     'edit_form': u'Форма редактирования/записи',
                                     'report': u'Форма печати/отчет',
                                     'storage_type': u'Тип хранилища метакомпонента',
                                     'container': u'Признак контейнера',
                                     'pic': u'Образ метакомпонента',
                                     'pic2': u'Дополнительный образ метакомпонента',
                                     'doc': u'Файл документации компонента',
                                     'can_contain': u'Разрешающее правило - список типов компонентов, которые могут содержаться в данном компоненте',
                                     'can_not_contain': u'Запрещающее правило - список типов компонентов, которые не могут содержаться в данном компоненте',
                                     'init': u'Блок кода, выполняемый при создании метаобъекта',
                                     'del': u'Блок кода, выполняемый при удалении метаобъекта',
                                     'gen_new_name': u'Блок генерации нового имени метаобъекта',
                                     },
                   }

# --- Описание компонента для редактора ресурса ---

#   Тип компонента
ic_class_type = icDefInf._icServiceType

#   Имя класса
ic_class_name = 'icMetaItem'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT':0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'MetaItem',
                'name': 'default',
                'activate': True,
                'init_expr': None,
                'child': [],
                '_uuid': None,
                '__styles__': ic_class_styles,
                '__events__': {},
                '__lists__': {'storage_type': [FILE_NODE_STORAGE_TYPE,
                                               FILE_STORAGE_TYPE,
                                               DIR_STORAGE_TYPE],
                              },
                '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['description', 'doc'],
                                   icDefInf.EDT_CHECK_BOX:['container'],
                                   icDefInf.EDT_CHOICE:['storage_type'],
                                   icDefInf.EDT_TEXTDICT:['spc','const_spc'],
                                   },
                '__parent__':SPC_IC_METAITEM,
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtMetaItem'
ic_class_pic2 = '@common.imgEdtMetaItem'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.user.ic_metaitem_wrp.icMetaItem-class.html'
ic_class_spc['__doc__'] = ic_class_doc
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = ['MetaConst', 'MetaAttr']

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 0, 0, 2)


# --- Классы ---
class icMetaProperty:
    """
    Свойства метакомпонента.
    """
    def __init__(self, MetaObj_, Property_=None, Const_=None):
        """
        Конструктор.
        @param MetaObj_: Метаобъект, свойства которого является.
        @param Property_: Словарь изменяемых свойств.
        @param Const_: Словарь неизменяемых свойств.
        """
        if Property_ is None:
            Property_ = {}
        self.__dict__['property'] = Property_
        if Const_ is None:
            Const_ = {}
        self.__dict__['const'] = Const_

        # !!! ОСТАЛЬНЫЕ СВОЙСТВА ДОЛЖНЫ НАХОДИТСЯ ПОСЛЕ ОПРЕДЕЛЕНИЯ property и const!!!
        # Метаобъект
        self._meta_obj = MetaObj_
        # Признак изменения какого-либо свойства
        self._propertyChanged = False

    def __nonzero__(self):
        """
        Провера на не 0.
        """
        return not isinstance(self, None)
        
    def __getattr__(self,name):
        if name in self.__dict__['const']:
            return self.__dict__['const'][name]
        elif name in self.__dict__['property']:
            return self.__dict__['property'][name]
        try:
            return self.__dict__[name]
        except KeyError:
            io_prnt.outWarning(u'Нет ключа %s в спецификации объекта %s компонента %s среди имен %s %s' % (name,
                                                                                                           self.__dict__['property']['name'],
                                                                                                           self.__dict__['property']['metatype'],
                                                                                                           self.__dict__['property'].keys(),
                                                                                                           self.__dict__['const'].keys()))
            raise KeyError
        
    def __setattr__(self, name, value):
        if name in self.__dict__['const']:
            self.__dict__['const'][name] = value
        elif name in self.__dict__['property']:
            if self.__dict__['property'][name] != value:
                self._propertyChanged = True
            self.__dict__['property'][name] = value
        elif name in self.__dict__['const']:
            self.__dict__['const'][name] = value
        else:
            self.__dict__[name] = value
        
    def getProperty(self):
        return self.__dict__['property']
        
    def setProperty(self, **Property_):
        self.__dict__['property'].update(Property_)
        self._propertyChanged = True

    def getConst(self):
        return self.__dict__['const']

    def isPropertyChanged(self):
        """
        Произошло изменение свойств?
        """
        return self._propertyChanged
        
    def resetPropertyChanged(self):
        """
        Сброс признака изменения свойств.
        """
        self._propertyChanged = False
        
    def setPropertyChanged(self, PropertyChanged_=True):
        """
        Установка признака изменения свойств.
        """
        self._propertyChanged = PropertyChanged_
        
    def getParentProperty(self, PropertyName_):
        """
        Значение свойств родительского узла (рекурсивно).
        @param PropertyName_: Имя искомого свойства.
        """
        if PropertyName_ in self.__dict__['property']:
            return self.__dict__['property'][PropertyName_]
        if PropertyName_ in self.__dict__['const']:
            return self.__dict__['const'][PropertyName_]
        if self._meta_obj._Parent:
            return self._meta_obj._Parent.value.getParentProperty(PropertyName_)
        return None


class icMetaItemEngine(persistent.icMetaComponentInterface, object):
    """
    Метакомпонент. Управление.
    """
    def __init__(self, Parent_, Resource_):
        """
        Конструктор.
        @param Parent_: Родительский метакомпонент.
        @param Resource_: Ресурс описания мета компонента.
        """
        # Расширить спецификацию
        Resource_ = util.icSpcDefStruct(SPC_IC_METAITEM, Resource_, False)
        
        persistent.icMetaComponentInterface.__init__(self)

        # Признак построенной ветки
        self._is_build = False
        
        self._Parent = Parent_
        self._name = Resource_['name']

        # Заполненение внутренних атрибутов метакомпонента
        self._value_spc = None
        if isinstance(Resource_['spc'], dict):
            self._value_spc = Resource_['spc']
        elif type(Resource_['spc']) in (str, unicode):
            self._value_spc = self.eval_attr('spc')[1]
        if not self._value_spc:
            self._value_spc = dict()
        self._value_spc['metatype'] = Resource_['name']
        self._value_spc['name'] = Resource_['name']
        self._value_spc['uuid'] = self.GetObjectUUID()
        
        self._const_spc = Resource_['const_spc']
        if self.components:
            attributes = [attr for attr in self.components.values() if issubclass(attr.__class__, ic_metaattr_wrp.icMetaAttr)]
            attribute_dict = dict([(attr.name, attr.defaultValue()) for attr in attributes])
            self._value_spc.update(attribute_dict)
            constants = [attr for attr in self.components.values() if issubclass(attr.__class__, ic_metaconst_wrp.icMetaConst)]
            constant_dict = dict([(const.name, const.defaultValue()) for const in constants])
            self._const_spc.update(constant_dict)

        self._value = icMetaProperty(self, util.icSpcDefStruct(self._value_spc, {}), self._const_spc)

        self._storage_type = Resource_['storage_type']

        self._container = Resource_['container']

        # Связанные с узлом дерева данные
        self._user_data = None
        
        # Документация метакомпонента
        self._doc = Resource_['doc']

        # События
        self._on_init = Resource_['init']
        self._on_del = Resource_['del']
        
        # Блок генерации имени метаобъекта
        self._is_gen_new_name = bool(not (Resource_['gen_new_name'] in [None, 'None']))

        # Дочерние метакомпоненты-объекты
        self._children = {}
        
        # Признак изменения структуры узла
        self._structChanged = False
        
        # Количество изменений в ветке
        self._changedCount = 0
     
    def getValue(self):
        """
        Свойства метакомпонента.
        """
        return self._value
    
    def setUserData(self, UserData_):
        """
        Привязать пользовательские данные к узлу дерева.
        """
        self._user_data = UserData_
        
    def getUserData(self):
        """
        Пользовательские данные привязанные к узлу.
        """
        return self._user_data

    def getRoot(self, MetaItem_=None):
        """
        Возвращает корневой элемент дерева.
        """
        if not MetaItem_:
            MetaItem_ = self
        
        if MetaItem_.isRoot():
            return MetaItem_
        else:
            return self.getRoot(MetaItem_.getItemParent())
    
    def findObject(self, Path_):
        """
        Ищет узел по заданному пути.
        """
        if not Path_:
            return self
            
        key = Path_[0]
        if key in self:
            return self[key].findObject(Path_[1:])
        
    def setValue(self, NewValue_, NewConst_=None):
        """
        Свойства метакомпонента.
        """
        if NewConst_ is None:
            NewConst_ = self._const_spc
        self._value = icMetaProperty(self, util.icSpcDefStruct(self._value_spc, NewValue_), NewConst_)
        
    value = property(getValue)
        
    def addChangedCount(self):
        """
        Увеличить счетчик изменений ветки.
        """
        self._changedCount += 1
        
        if self._Parent:
            self._Parent.addChangedCount()
        
    def subChangedCount(self):
        """
        Уменньшить счетчик изменений ветки.
        """
        if self._changedCount > 0:
            self._changedCount -= 1

            if self._Parent:
                self._Parent.subChangedCount()
            
    def getChangedCount(self):
        """
        Счетчик изменений ветки.
        """
        return self._changedCount
        
    def isValueChanged(self):
        """
        Признак изменения значения узла.
        """
        return self.value.isPropertyChanged()
        
    def setValueChanged(self, ValueChanged_=True):
        """
        Установить признак изменения значения узла.
        """
        self.value.setPropertyChanged(ValueChanged_)
        
        # Установить у всех родительских узлов счетчик изменения значения для
        # определения события сохранения
        if ValueChanged_:
            self.addChangedCount()
        else:
            self.subChangedCount()

    def isStructChanged(self):
        """
        Признак изменения структуры узла.
        """
        return self._structChanged
        
    def setStructChanged(self, StructChanged_=True):
        """
        Установить признак изменения структуры узла.
        """
        self._structChanged = StructChanged_
        
        # Установить у всех родительских узлов признак изменения структуры для
        # определения события сохранения
        if StructChanged_:
            self.addChangedCount()
        else:
            self.subChangedCount()
                
    def setName(self, NewName_):
        self.name = NewName_
        self.value.name = self.name
        self._name = self.name
        
    def rename(self, NewName_):
        """
        Переименование.
        """
        # Если имя не поменялось, то и напрягаться не надо!!!
        if self.name == NewName_:
            return
        
        if self._Parent:
            if self.name in self._Parent._children:
                del self._Parent._children[self.name]
            self._Parent._children[NewName_] = self

        self.name = NewName_
        
        # Только после переименования всех свойств метаобъекта
        # необходимо пререименовать узел хранилища для синхронности!!!
        self.renameStoreNode(NewName_)

        self.value.name = self.name
        self._name = self.name
        
        self.BuildAll()

    def renameStoreNode(self, NewName_):
        """
        Переименовать узел хранилища метаобъекта.
        @param NewName_: Новое имя.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            node.setName(NewName_)
            # Сразу сохранить
            node.save()

    def createValueStorage(self, ParentStoreNode_):
        """
        Функция возвращает хранилище метаобъекта.
        @param ParentStoreNode_: Родительский узел хранилища.
        """
        storage_node = None
        if self._storage_type == DIR_STORAGE_TYPE:
            # Папочное хранилище
            storage_node = storesrc.icDirStorage()
            storage_node.setParentNode(ParentStoreNode_, self.name)
        elif self._storage_type == FILE_STORAGE_TYPE:
            # Файловое хранилище
            storage_node = storesrc.icFileStorage()
            storage_node.setParentNode(ParentStoreNode_, self.name)
        elif self._storage_type == FILE_NODE_STORAGE_TYPE or (self._storage_type is None):
            # Файловое хранилище
            storage_node = storesrc.icFileNodeStorage()
            storage_node.setParentNode(ParentStoreNode_, self.name)

        if storage_node is not None:
            storage_node.setProperty(self.getValue().getProperty())

        return storage_node
    
    def setValueStorage(self, StorageNode_):
        """
        Функция устанавливает значения метаобъекта в хранилище метаобъекта.
        @param StorageNode_: Узел хранилища, соответствующий метаобъекту.
        """
        storage_node = StorageNode_

        if storage_node is not None:
            storage_node.setProperty(self.value.getProperty())
            
        return storage_node
        
    def readPropertyStorage(self, ReLoad_=False):
        """
        Прочитать свойство из хранилища.
        @param ReLoad_: Признак необходимости обновления свойств узлоа из
            хранилища.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            if ReLoad_:
                return node.loadProperty()
            else:
                return node.getProperty()
        return None
       
    def savePropertyStorage(self):
        """
        Сохранить свойства в хранилище.
        """
        if self._Parent:
            # Сбросить свойства в дерево хранилища
            parent_path = self._Parent.getPath()
            self.setPath(parent_path, None, **{self.name: self})
            
        # Выполнить сохранение
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.saveProperty()
        return None
        
    def getPic(self):
        """
        Образ узла метаобъекта.
        """
        self.evalSpace['self'] = self
        pic = self.eval_attr('pic')[1]
        if pic is None:
            pic = common.imgFolder
        return pic
    
    def getPic2(self):
        """
        Образ узла метаобъекта (развернут).
        """
        self.evalSpace['self'] = self
        pic = self.eval_attr('pic2')[1]
        if pic is None:
            pic = common.imgFolderOpen
        return pic

    def getCanContain(self):
        """
        Список включения.
        """
        self.evalSpace['self'] = self
        return self.countAttr('can_contain')
        
    def getCanNotContain(self):
        """
        Список включения.
        """
        self.evalSpace['self'] = self
        return self.countAttr('can_not_contain')
        
    def getDoc(self):
        return self._doc
        
    def View(self, *args, **kwargs):
        """
        Открыть форму просмотра метакомпонента.
        """
        self.evalSpace['self'] = self
        view_form = self.getICAttr('view_form', bExpectedExpr=True, bReUse=False)
        if view_form:
            if '.' in view_form:
                import_str = 'import %s' % ('.'.join(view_form.split('.')[:-1]))
                exec import_str
                form_class = view_form.split('.')[-1]
                form_mod = eval('.'.join(view_form.split('.')[:-1]))
                
                return getattr(form_mod, form_class)(*args, **kwargs).getObject()
            else:
                return prs.CreateForm(view_form, *args, **kwargs)

    def __View(self, *args, **kwargs):
        """
        Открыть форму просмотра метакомпонента.
        """
        if self._view_form:
            if '.' in self._view_form:
                import_str = 'import %s' % ('.'.join(self._view_form.split('.')[:-1]))
                exec import_str
                form_class = self._view_form.split('.')[-1]
                form_mod = eval('.'.join(self._view_form.split('.')[:-1]))
                
                return getattr(form_mod, form_class)(*args, **kwargs).getObject()
            else:
                return prs.CreateForm(self._view_form, *args, **kwargs)

    def getItemParent(self):
        return self._Parent
        
    def Edit(self, *args, **kwargs):
        """
        Открыть форму редактирования метакомпонента.
        """
        self.evalSpace['self'] = self
        edit_form = self.getICAttr('edit_form', bExpectedExpr=True, bReUse=False)
        if edit_form:
            if '.' in edit_form:
                import_str = 'import %s' % ('.'.join(edit_form.split('.')[:-1]))
                exec import_str
                form_class = edit_form.split('.')[-1]
                form_mod = eval('.'.join(edit_form.split('.')[:-1]))
                
                return getattr(form_mod, form_class)(*args, **kwargs).getObject()
            else:
                return prs.CreateForm(edit_form, *args, **kwargs)
        
    def __Edit(self, *args, **kwargs):
        """
        Открыть форму редактирования метакомпонента.
        """
        if self._edit_form:
            if '.' in self._edit_form:
                import_str = 'import %s' % ('.'.join(self._edit_form.split('.')[:-1]))
                exec import_str
                form_class = self._edit_form.split('.')[-1]
                form_mod = eval('.'.join(self._edit_form.split('.')[:-1]))
                
                return getattr(form_mod, form_class)(*args, **kwargs).getObject()
            else:
                return prs.CreateForm(self._edit_form, *args, **kwargs)

    def Print(self, *args, **kwargs):
        """
        Запустить печать отчета метакомпонента.
        """
        self.evalSpace['self'] = self
        report = self.getICAttr('report', bExpectedExpr=True, bReUse=False)
        return DoReport(report, *args, **kwargs)

    def __Print(self, *args, **kwargs):
        """
        Запустить печать отчета метакомпонента.
        """
        if self._report:
            return DoReport(self._report, *args, **kwargs)
    
    def Module(self):
        """
        Импортировать модуль метакомпонента.
        """
        pass
           
    def Add(self, Name_=None, Type_=None):
        """
        Добавить дочерний метакомпонент.
        @param Name_: Имя добавляемого объекта,
            если None, то имя генерируется.
        @param Type_: Имя компонента, объект которого
            будет добавлен в дерево.
            Если None, то будет сделан запрос имени.
        @return: Созданный объект метакомпонента.
        """
        new_metaobj = self._add(Name_, Type_)
        
        # После создания объекта необходимо выполнить специфическую
        # инициализацию
        if new_metaobj is not None:
            if new_metaobj._on_init and (new_metaobj._on_init != 'None'):
                new_metaobj.evalSpace['self'] = new_metaobj
                ok = util.ic_eval(new_metaobj._on_init, evalSpace=self.evalSpace)
                if (not ok[1]) or (not ok[0]):
                    # Если инициализация не прошла, тогда не сохранять!!!
                    return None

            new_metaobj.setStructChanged(True)
            new_metaobj.Save()
                
        return new_metaobj
        
    def _add(self, Name_=None, Type_=None):
        """
        Добавить дочерний метакомпонент.
        @param Name_: Имя добавляемого объекта,
            если None, то имя генерируется.
        @param Type_: Имя компонента, объект которого
            будет добавлен в дерево.
            Если None, то будет сделан запрос имени.
        @return: Созданный объект метакомпонента.
        """
        new_metaobj = None
        # Имя не определено
        if Type_ is None:
            container_meta_components = self.getContainerMetaItems()
            if container_meta_components:
                Type_ = ic_dlg.icSingleChoiceDlg(None,
                                                 u'Возможные типы>', u'Выбирите тип объекта:',
                                                 container_meta_components.keys())
            else:
                return None
        if Type_:
            # Объект можно добавить в этот узел
            lst = [x.name for x in self.getMyContainerMetaItems()]

            if Type_ in lst:
                meta_type_obj = self.getContainerMetaItem(Type_)
                if meta_type_obj:
                    # Создать новое имя если это нужно
                    if Name_ is None:
                        Name_ = meta_type_obj.genNewName()
                    io_prnt.outLog(u'Создание метаобъекта %s метакомпонента %s родитель: %s' % (Name_, Type_,
                                                                                                self.name))
                    new_metaobj = meta_type_obj.createMetaObj(self, Name_)
                    if new_metaobj:
                        self._children[Name_] = new_metaobj

        return new_metaobj
   
    def genNewName(self):
        """
        Генерация имени метаобъекта.
        """
        if not self._is_gen_new_name:
            return 'default' + str(wx.NewId())
        else:
            return self.eval_attr('gen_new_name')[1]
        
    def createMetaObj(self, Parent_, NewName_, ReLoadProperty_=False):
        """
        Создать объект метаобъект.
        @param Parent_: Родитель.
        @param NewName_: Имя метаобъекта.
        @param ReLoadProperty_: Признак перезагрузки свойств метаобъекта из хранилища.
        @return: Возвращает метаобъект.
        """
        res = copy.deepcopy(self.resource)
        res['name'] = NewName_

        obj = self.__class__(Parent_, component=res, evalSpace=self.evalSpace)
        
        # Определить метатип метаобъекта, как имя метаитема
        obj.value.metatype = self.resource['name']
        # При создании метаобъекта необходимо прочитать его свойства
        # из хранилища
        if obj.isStoreNodeLevel():
            property = obj.readPropertyStorage(ReLoadProperty_)
            if property is not None:
                obj.setValue(property)
            
        return obj
        
    def DelChild(self, Name_=None):
        """
        Удалить дочерний метакомпонент.
        @param Name_: Имя удаляемого объекта,
            если None, то имя запрашивается.
        """
        if Name_ is None:
            child_meta_objects = self._children
            if child_meta_objects:
                Name_ = ic_dlg.icSingleChoiceDlg(None,
                                                 u'Возможные объекты>', u'Выбирите объект:',
                                                 child_meta_objects.keys())
            else:
                return False

        if Name_:
            if Name_ in self._children:
                node = self.getStoreNodeLevel()
                if node is not None:
                    del node[Name_]
                    del self._children[Name_]
                    # Сохранить
                    ok = node.save()
                    self.setStructChanged(False)
                    return ok
        return False
        
    def Del(self):
        """
        Удалить метакомпонент.
        """
        if self._Parent:
            ok = (True, True)
            # Перед удалением выполнить блок кода на удаление
            if self._on_del and (self._on_del != 'None'):
                self.evalSpace['self'] = self
                ok = util.ic_eval(self._on_del, evalSpace=self.evalSpace)
            # Получается что корень удалить нельзя!!!
            if ok[0] and ok[1]:
                self._Parent.setStructChanged(True)
                return self._Parent.DelChild(self.name)
        return False
        
    def getContainerMetaItems(self):
        """
        Список компонент, которые могут быть узлами дерева.
        """
        if self._Parent:
            return self._Parent.getContainerMetaItems()
        return None
        
    def getContainerMetaItem(self, MetaItemName_):
        """
        Взять метакомпонент, который может быть узлом дерева по имени.
        @param MetaItemName_: Имя мета компонента-типа.
        """
        if self._Parent:
            return self._Parent.getContainerMetaItem(MetaItemName_)
        return None
     
    def Save(self, MetaObject_=None):
        """
        Сохранить данные метаобъекта.
        @param MetaObject_: Сохраняемый метаобъект.
            Если None, то значит надо сохранить себя.
        """
        if MetaObject_ is None:
            MetaObject_ = self
            io_prnt.outLog(u'METAITEM Save <%s> <%s>' % (MetaObject_.isValueChanged(), MetaObject_.isStructChanged()))

        # Если не было никаких изменений, то сохранять не надо
        if (not MetaObject_.isValueChanged()) and \
           (not MetaObject_.isStructChanged()):
            return None
        
        if self._Parent:
            return self._Parent.Save(MetaObject_)
        return None

    def Load(self, MetaObject_=None):
        """
        Загрузить данные метаобъекта.
        @param MetaObject_: Загружаемый метаобъект.
            Если None, то значит надо загрузить себя.
        """
        if MetaObject_ is None:
            MetaObject_ = self
        if self._Parent:
            return self._Parent.Load(MetaObject_)
        return None
    
    def setPath(self, Path_, CurStoreLevel_, **MetaObjects_):
        """
        Установить данные метаобъектов по указанной ветке/пути.
        @param Path_: Список имен метаобъектов/ветки.
        @param CurStoreLevel_: Текущий уровень хранилища. Если None, то корень.
        @param MetaObjects_: Сохраняемые метаобъекты.
        """
        if self._Parent:
            return self._Parent.setPath(Path_, CurStoreLevel_, **MetaObjects_)
        return None
        
    def SaveAllChildren(self, ParentMetaObject_=None):
        """
        Сохранить себя и все дочерние узлы.
        @param ParentMetaObject_: Сохраняемый метаобъект.
        """
        if ParentMetaObject_ is None:
            ParentMetaObject_ = self
            
        if ParentMetaObject_ == self:
            # Перед сохранением надо прочитать всю ветку дерева метаобъектов
            self.BuildAll()
            
        # Сохранение состояния всех дочерних метаобъектов
        self.setPath(self.getPath(), None, **self._children)
        
        for child in self._children.values():
            child.SaveAllChildren(ParentMetaObject_)
        if ParentMetaObject_ == self:
            # Принудительно сохранить рутовый объект
            self.setValueChanged(True)
            self.Save()
        else:
            # Сбросить признаки изменения значений и структуры
            # дочерних метаобъектов
            self.setValueChanged(False)
            self.setStructChanged(False)
        
    def getPath(self, CurPath_=None):
        """
        Получить список имен узлов пути метаобъекта в дереве.
        """
        if CurPath_ is None:
            CurPath_ = []
        if self._Parent:
            # Вставить имя метаобъека первым в списке пути
            CurPath_.insert(0, self._name)
            return self._Parent.getPath(CurPath_)
        return CurPath_

    def getMyContainerMetaItems(self, CanContain_=-1, CanNotContain_=-1):
        """
        Получить список метакомпонентов, которые могут быть вставлены в
        текущий метаобъект.
        @param CanContain_: Разрешающее правило включения. Список имен метакомпонент.
        @param CanNotContain_: Запрещающее правило включения. Список имен метакомпонент.
        @return: Список метакомпонент.
        """
        if CanContain_ == -1:
            CanContain_ = self.getCanContain()
        if CanNotContain_ == -1:
            CanNotContain_ = self.getCanNotContain()
        if self._Parent:
            return self._Parent.getMyContainerMetaItems(CanContain_, CanNotContain_)

        if CanContain_ is not None:
            return [metaitem for metaitem in self.getContainerMetaItems().values() if metaitem.name in CanContain_]
        elif CanNotContain_ is not None:
            return [metaitem for metaitem in self.getContainerMetaItems().values() if not(metaitem.name in CanContain_)]
        else:
            return self.getContainerMetaItems().values()
        
    def ReLoad(self):
        """
        Перечитать все объекты из хранилища.
        """
        self.clearBuffChildren()
        self.Build()
        
    def isBuild(self):
        """
        Построен уровень?
        """
        return self._is_build

    def _buildMetaObj(self, Name_, StoreNode_, ReBuild_=False):
        """
        Низкоуровневая функция построения узла.
        @param Name_: Имя дочернего узла.
        @param StoreNode_: Узел родителя в хранилище.
        @param ReBuild_: Флаг установки пересоздания узлов.
        """
        new_metaobj = None
        if issubclass(StoreNode_[Name_].__class__, storesrc.icFileStorage):
            metatype = StoreNode_[Name_]['property']['metatype']
        elif issubclass(StoreNode_[Name_].__class__, storesrc.icDirStorage):
            if StoreNode_[Name_].property is not None:
                metatype = StoreNode_[Name_].property['metatype']
            else:
                return None
        elif issubclass(StoreNode_[Name_].__class__, storesrc.icFileNodeStorage):
            metatype = StoreNode_[Name_]['property']['metatype']
        else:
            return None
        meta_item = self.getContainerMetaItem(metatype)
        name = StoreNode_[Name_].getName()
        if ReBuild_:
            # Создавать узлы по любому
            new_metaobj = meta_item.createMetaObj(self, name, True)
            if new_metaobj:
                self._children[name] = new_metaobj
        else:
            # Создавать узлы, только при условии что их нет
            if name not in self._children:
                new_metaobj = meta_item.createMetaObj(self, name, False)
                if new_metaobj:
                    self._children[name] = new_metaobj
        return new_metaobj
        
    def BuildBranch(self, Path_, ReBuild_=False, BuildAll_=True):
        """
        Построить только ветку.
        @param Path_: Путь до узла.
        @param ReBuild_: Флаг установки пересоздания узлов.
        @param BuildAll_: Вызвать у созданного узла BuildAll автоматически?
        """
        metaobj_path = self.getPath()
        store_node = self.getStoreNodeLevel(metaobj_path)
        
        # Разбор узла хранилища
        if store_node is not None:
            if Path_:
                store_subnode_name = Path_[0]
                if store_subnode_name in store_node.keys():
                    new_metaobj = self._buildMetaObj(store_subnode_name, store_node, ReBuild_)
                    if new_metaobj:
                        return new_metaobj.BuildBranch(Path_[1:], ReBuild_, BuildAll_)
            else:
                if BuildAll_:
                    return self.BuildAll()
        
    def Build(self, ReBuild_=False):
        """
        Построить дерево объектов по данным хранилища.
        @param ReBuild_: Флаг установки пересоздания узлов.
        """
        metaobj_path = self.getPath()
        store_node = self.getStoreNodeLevel(metaobj_path)
        
        # Разбор узла хранилища
        if store_node is not None:
            for store_subnode_name in store_node.keys():
                new_metaobj = self._buildMetaObj(store_subnode_name, store_node, ReBuild_)
                if new_metaobj is None:
                    continue
        self._is_build = True

    def BuildAll(self):
        """
        Построить рекурсивно всю ветку метаобъектов.
        """
        self.Build()
        for child in self._children.values():
            child.BuildAll()

    def syncBuildAll(self):
        """
        Построить ветку метаобъектов, только если ее нет в памяти.
        """
        metaobj_path = self.getPath()
        store_node = self.getStoreNodeLevel(metaobj_path)
        if store_node is not None and len(store_node.keys()) > len(self._children.keys()):
            self.Build()
        for child in self._children.values():
            child.syncBuildAll()
        
    def getStoreNodeLevel(self, Path_=None):
        """
        Получить узел хранилища по пути.
        @param Path_: Путь.
        """
        if Path_ is None:
            # Если определен узел, тогда просто вернуть его
            Path_ = self.getPath()
        if self._Parent:
            return self._Parent.getStoreNodeLevel(Path_)
        return None
    
    def isStoreNodeLevel(self, Path_=None):
        """
        Проверить существует ли узел хранилища с таким путем.
        @param Path_: Путь.
        @return: True/False.
        """
        if Path_ is None:
            # Если определен узел, тогда просто вернуть его
            Path_ = self.getPath()
        if self._Parent:
            return self._Parent.isStoreNodeLevel(Path_)
        return False
        
    def saveStoreNodeLevel(self, Path_=None, MetaObject_=None):
        """
        Сохранить узел хранилища по пути.
        @param Path_: Путь.
        @param MetaObject_: Сохраняемый метаобъект.
        """
        if MetaObject_ is None:
            MetaObject_ = self
        if Path_ is None:
            # Если определен узел, тогда просто вернуть его
            Path_ = self.getPath()
        if self._Parent:
            return self._Parent.saveStoreNodeLevel(Path_, MetaObject_)
        return False
       
    def closeStorage(self):
        """
        Закрыть все файлы хранилища.
        """
        if self._Parent:
            self._Parent.closeStorage()

    # --- Методы поддержки блокировок ---
    def lock(self):
        """
        Заблокировать.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.lock()
        return False
        
    def unLock(self):
        """
        Разблокировать.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.unLock()
        return False
        
    def isLock(self):
        """
        Проверить блокировку.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.isLock()
        return False
        
    def ownerLock(self):
        """
        Владелец блокировки.
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.ownerLock()
        return None

    def isMyLock(self):
        """
        Моя блокировка?
        """
        node = self.getStoreNodeLevel()
        if node is not None:
            return node.isMyLock()
        return False
        
    def isRoot(self):
        """
        Является ли метаобъект главным/рутовым?
        """
        return self._Parent is None
      
    def Clone(self, CloneName_=None):
        """
        Создать клон метаобъекта.
        @param CloneName_: Имя клона, если None,то имя генерируется.
        @return: Возвращает объект клона или None в случае неудачи.
        """
        if CloneName_ is None:
            CloneName_ = self.genNewName()

        if self._storage_type == DIR_STORAGE_TYPE:
            node = self.getStoreNodeLevel()
            if node is not None and self._Parent:
                node.Clone(CloneName_)
                return None
        elif self._storage_type == FILE_STORAGE_TYPE:
            node = self.getStoreNodeLevel()
            if node is not None and self._Parent:
                node.Clone(CloneName_)
                return None
        elif self._storage_type == FILE_NODE_STORAGE_TYPE:
            return self._clone(CloneName_)
        else:
            return self._clone(CloneName_)
        return None
        
    def _clone(self, CloneName_, doCopyChildren_=True):
        """
        Создать клон метаобъекта.
        @param CloneName_: Имя клона, если None,то имя генерируется.
        @param doCopyChildren_: Признак копирования дочерних узлов.
        @return: Возвращает объект клона или None в случае неудачи.
        """
        try:
            io_prnt.outLog(u'Создание клона %s метаобъекта %s родитель: %s' % (CloneName_, self.name,
                                                                               self._Parent.name))
            clone = self._Parent._add(CloneName_, self.value.metatype)
            clone.Save()
            clone_property = copy.deepcopy(self.value.getProperty())
            clone_property['name'] = CloneName_
            clone_const = copy.deepcopy(self.value.getConst())
            clone.setValue(clone_property, clone_const)

            if doCopyChildren_:
                self.copyChildren()
                clone.pastChildren()
            clone.Save()
            return clone
        except:
            io_prnt.outErr(u'Ошибка создания клона метаобъекта %s' % self.name)
            return None

    def copyChildren(self):
        """
        Копировать все дочерние метаобъекты в клипбоард.
        """
        return clipboard.toClipboard(self)
        
    def pastChildren(self):
        """
        Вставить все дочерние метаобъекты из клипбоарда.
        @return: None - ошибка. False - не могу вставить в текущий объект.
            True - все ок.
        """
        if not clipboard.emptyClipboard():
            from_metaobj = clipboard.fromClipboard(False)
            if issubclass(from_metaobj.__class__, icMetaItem):
                # Сделать полную копию ветки дочерних метаобъектов.
                from_metaobj.syncBuildAll()
                self.savePropertyStorage()
                ok = self._deepcopyChildren(from_metaobj._children)
                return ok
        return None
    
    def canMyChild(self, MetaObject_):
        """
        Может ли метаобъект быть дочерним метаобъектом текущего метаобъекта?
        @param MetaObject_: Метаобъект, претендующий на роль дочернего.
        @return: Возвращает True/False.
        """
        try:
            my_container_metaitems = [metaitem.name for metaitem in self.getMyContainerMetaItems()]
            return MetaObject_.value.metatype in my_container_metaitems
        except:
            io_prnt.outErr()
            return False
        
    def canPastChildren(self):
        """
        Можно ли вставить в текущий узел объекты из клипборда?
        @return: True/False.
        """
        if clipboard.emptyClipboard():
            return False
        from_metaobj = clipboard.fromClipboard(False)
        if issubclass(from_metaobj.__class__, icMetaItem):
            if from_metaobj._children:
                ok = self.canMyChild(from_metaobj._children.values()[0])
                return ok
            else:
                return False
        return False
        
    def _deepcopyChildren(self, Children_):
        """
        Сделать полную копию ветки дочерних метаобъектов.
        @param Children_: Список дочерних метаобъектов, копии которых необходимо получить.
        """
        for child in Children_.items():
            try:
                # Создать и инициализировать новый дочерний метаобъект
                new_child_name = child[1].value.name
                new_child = self._add(new_child_name, child[1].value.metatype)
                new_child.Save()
                child_property = copy.deepcopy(child[1].value.getProperty())
                child_const = copy.deepcopy(child[1].value.getConst())
                new_child.setValue(child_property, child_const)
                # Сделать полную копию ветки дочерних метаобъектов.
                new_child._deepcopyChildren(child[1]._children)
                new_child.savePropertyStorage()
            except:
                io_prnt.outErr(u'Ошибка создания и инициализации копии %s метаобъекта %s' % (new_child_name, child[0]))
                return False
        return True

    def getBuffChildren(self):
        """
        Дочерние метаобъекты.
        """
        return self._children
        
    def clearBuffChildren(self):
        """
        Очистить словарь/буффер дочерних метаобъектов.
        """
        self._children = {}
        storage = self.getStorage()
        if storage:
            storage.Close()
        
    def getStorage(self):
        if self._Parent:
            return self._Parent.getStorage()
        return None
        
    # --- Транзакционный механизм ---
    def transact(self):
        """
        Начать транзакцию.
        """
        node = self.getStoreNodeLevel()
        if node:
            node.transact()
        
    def _savePropertyStorageParent(self):
        """
        Сохранить свойства у всех родительских узлов до рута.
        """
        if self._Parent:
            self.savePropertyStorage()
            return self._Parent._savePropertyStorageParent()
        return True
        
    def commit(self):
        """
        Подтвердить изменения.
        """
        node = self.getStoreNodeLevel()
        if node:
            node.commit()
        self.SaveAllChildren()
        if self._Parent:
            self._Parent._savePropertyStorageParent()
        
    def rollback(self):
        """
        Откат изменений.
        """
        node = self.getStoreNodeLevel()
        if node:
            node.rollback()

    # --- Поддержка атрибутов спецификации ---
            
    # --- Поддержка интерфейса словаря ---
    def __getitem__(self, key):
        if not self.isBuild():
            self.Build()
        return self._children.__getitem__(key)
        
    def __setitem__(self, key, item):
        if not self.isBuild():
            self.Build()
        return self._children.__setitem__(key,item)
        
    def __delitem__(self, key):
        if not self.isBuild():
            self.Build()
        return self._children.__delitem__(key)
        
    def has_key(self, key):
        if not self.isBuild():
            self.Build()
        return key in self._children

    def __contains__(self, item):
        """
        ВНИМАНИЕ! Это функция - замена has_key для Python3.
        """
        return item in self

    def keys(self):
        if not self.isBuild():
            self.Build()
        return self._children.keys()

    def items(self):
        if not self.isBuild():
            self.Build()
        return self._children.items()
        
    def values(self):
        if not self.isBuild():
            self.Build()
        return self._children.values()
        
    def setdefault(self, key, default=None):
        if not self.isBuild():
            self.Build()
        return self._children.setdefault(key, default)
        
    def get(self, key, default=None):
        if not self.isBuild():
            self.Build()
        return self._children.get(key, default)


class icMetaItem(icwidget.icSimple, icMetaItemEngine):
    """
    Метакомпонент.
    """
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
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace, bGenUUID=False)

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        icMetaItemEngine.__init__(self, parent, component)
        
    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                             bCounter=bCounter, progressDlg=progressDlg)

