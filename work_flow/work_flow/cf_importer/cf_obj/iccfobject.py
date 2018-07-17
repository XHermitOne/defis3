#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс абстрактного элемента конфигурации.
"""


import os
import os.path
import re
import wx

from ic.utils import util1c
from ic.dlg import ic_dlg


__version__ = (0, 0, 0, 3)

NONE_UID = '00000000-0000-0000-0000-000000000000'
ANY_UID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

# Признак ссылки
REF_SIGNATURE_1C = '#'


class icCFObject:
    """
    Класс абстрактного элемента конфигурации.
    """
    def __init__(self, parent=None, uid=None, cf_dirname=None):
        """
        Конструктор.
        @param parent: Родительский объект.
        @param uid: Униакльный идентификатор объекта.
        @param cf_dirname: Папка конфигурации 1с.
        """
        self.parent = parent
        
        self.uid = uid
        if self.uid is None:
            self.uid = NONE_UID
            
        self.cf_dir = cf_dirname
        if self.cf_dir is None:
            self.cf_dir = self.getCFDir()
            
        # Человекопонятное имя объекта
        self.name = u''
        
        # Список дочерних элементов
        self.children = []
        
        # Образ объекта
        self.img_filename = ''
        self.img = None
        self.img_exp_filename = ''
        self.img_exp = None

    def getUnicodeName(self):
        """
        Имя объекта в представлении Unicode.
        """
        if isinstance(self.name, unicode):
            return self.name
        else:
            return util1c.encodeText(str(self.name), 'utf-8', 'unicode')

    def getStructUnicodeName(self):
        """
        Имя объекта в Unicode со всей иерархией метаданных.
        """
        name = self.getUnicodeName()
        if self.parent:
            name = self.parent.getStructUnicodeName() + u'.' + name
        return name

    def getImage(self):
        """
        Образ.
        """
        if self.img is None:
            if os.path.exists(self.img_filename):
                self.img = wx.Image(self.img_filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        return self.img

    def getImageExpand(self):
        """
        Образ раскрытого узла.
        """
        if self.img_exp is None:
            if os.path.exists(self.img_exp_filename):
                self.img_exp = wx.Image(self.img_exp_filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            # else:
            #     self.img_exp = wx.Image(self.img_filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        return self.img_exp
    
    def getCFDir(self):
        """
        Получить имя папки конфигурации.
        """
        if self.cf_dir:
            return self.cf_dir
        else:
            if self.parent:
                return self.parent.getCFDir()
        return self.cf_dir
    
    def build(self):
        """
        Переопределяемый метод инициализации  построения всех дочерних оъектов.
        """
        ic_dlg.icUpdateProgressDlg(NewMsg_=u'Метаобъект: ' + self.getStructUnicodeName())        
  
    def findByUID(self, uid):
        """
        Найти объект по UID.
        @param uid: Униакльный идентификатор объекта.
        @return: Возвращает объект в дереве объектов с заданным UID или None,
        если такой объект не найден.
        """
        if self.uid == uid:
            return self
        if self.children:
            for child in self.children:
                find_obj = child.findByUID(uid)
                if find_obj:
                    return find_obj
        return None

    def getChildrenByUID(self, uid):
        """
        Получить все дочерние объекты с указанным UID.
        @param uid: Униакльный идентификатор объекта.
        @return: Возвращает список дочерних элементов искомого объекта.
        """
        obj = self.findByUID(uid)
        if obj:
            return obj.getAllChildren()
        return None
        
    def getAllChildren(self):
        """
        Получить все дочерние объекты списком.
        """
        children = []
        children += self.children
        for child in self.children:
            children += child.getAllChildren()
        return children
    
    def getAllChildrenByFilter(self, Filter_, IsMetaobject_=True):
        """
        Получить все дочерние объекты списком по фильтру.
        @param Filter_: Строка фильтра в формате:
        ...<Регулярное выражение>.Имя узла.Имя подузла
        Например:
        ...<\A(?!иц*)>.Формы.ФормаСписка
        @param IsMetaobject_: Получить только метаобъекты.
        """
        # Подготовка фильтра
        re_filters = re.findall(r'(<.*?>)', Filter_)
        for i, re_filter in enumerate(re_filters):
            Filter_ = Filter_.replace(re_filter, '<%d>' % i)
            # Стереть в фильтре <>
            re_filter = re_filter[1:-1]
            re_filters[i] = re_filter            
        
        my_filters = Filter_.split('.')        
        for i, my_filter in enumerate(my_filters):
            if my_filter and (my_filter[0] == '<') and (my_filter[-1] == '>'):
                my_filters[i] = re.compile(re_filters[int(my_filter[1:-1])])
        
        children = self.getChildrenByFilter(my_filters[0], my_filters[1:])
        
        if IsMetaobject_:
            children = [child for child in children if child.uid != NONE_UID]
           
        return children
    
    def getChildrenByFilter(self, Filter_, SubFilters_=None):
        """
        Получить все дочерние объекты списком по фильтру.
        @param Filter_: Строка фильтра.
        @param SubFilters_: Подфильтр дочерних элементов для рекурсивного выбора.
        """
        if not Filter_:
            # Если фильтр не определен, то все дочерние элементы.
            children = self.children
        elif type(Filter_) in (str, unicode):
            children = [child for child in self.children if Filter_ == child.name]
        else:
            children = [child for child in self.children if bool(re.search(Filter_, child.name))]
        
        if SubFilters_:
            sub_children = []
            for child in children:
                sub_children += child.getChildrenByFilter(SubFilters_[0], SubFilters_[1:])
            return sub_children
        
        return children
        
    # --- Функции изменения метаобъекта в конфигурации ---
    def addInModule(self, Txt_):
        """
        Добавить в модуль объекта текст.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        return False

    def delInModule(self, Txt_):
        """
        Удалить из модуля объекта текст.
        @param Txt_: Удаляемый текст.
        @return: True - удаление прошло успешно, False - удаления не произошло.
        """
        return False
        
    def replaceInModule(self, SrcTxt_, DstTxt_):
        """
        Заменить текст в модуле объекта.
        @param SrcTxt_: Заменяемый текст.
        @param DstTxt_: Заменяющий текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        return False

    def gen_resource(self):
        """
        Генерация ресурса, соответстствующего объеку 1С.
        @return: True/False.
        """
        return False

    def _get_db_psp(self, prj_res_ctrl=None):
        """
        Определить паспорт БД проекта.
        @param prj_res_ctrl: Контроллер управления ресурсом проекта.
        @return:
        """
        return self.parent._get_db_psp(prj_res_ctrl) if self.parent else None


class icCFFolder(icCFObject):
    """
    Папка объектов конфигурации.
    """        
    def __init__(self, parent=None, cf_dirname=None, name=None, children=None,
                 img_filename='', img_exp_filename=''):
        """
        Конструктор.
        @param parent: Родительский объект.
        @param cf_dirname: Папка конфигурации 1с.
        @param name: Имя папки.
        @param children: Список дочерних элементов.
        @param img_filename: Имя файла образа элемента папки.
        @param img_exp_filename: Имя файла образа элемента раскрытой папки.
        """
        # ВНИМАНИЕ!
        # Для папок UID - NONE_UID
        # Если это просто объект у которого не предусмотрен UID, то
        # у него должен быть ANY_UID
        icCFObject.__init__(self, parent, None, cf_dirname)
        
        self.name = name
        self.children = children

        # Образ объекта
        self.img_filename = img_filename
        self.img_exp_filename = img_exp_filename
        
    def setChildren(self, name=None, children=None):
        """
        Установить дочерние объекты папки.
        @param name: Наименование папки.
        @param children: Список дочерних объектов папки.
        """
        if name is not None:
            self.name = name
        if children is not None:
            self.children = children
