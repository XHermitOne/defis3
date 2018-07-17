#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс поддержки словаря ассоциаций.
Модуль поддержки словаря ассоциаций. Ассоциативный словарь содержит наиболее
часто используемые ассоциации. В качестве ключей используются картежи со
значениями полей, которые являются естественными ключами, например, название
улицы и номер дома являются такими ключами для объектов недвижимости. По
этому ключу можно всегда востановит этажность, материал, типы планировок и.т.д.
Задавая такие ассоциации в классе данных можно значительно снизить трудоемкость
ввода первичной информации об объектах класса данных, поскольку некоторое
количество атрибутов будут заполняться автоматически.
"""

from . import persistant
from . import ic_file

from ic.engine import ic_user
from ic.log import log

__version__ = (1, 0, 1, 2)

#   Размер словаря ассоциаций
accDictBuffSize = 100


def cmpRows(x, y):
    """
    Функция сравнения записей в частотном словаре.
    """
    if x[1] > y[1]:
        return -1
    elif x[1] < y[1]:
        return 1
    else:
        return 0


class icAssociationDict(persistant.icPersistant):
    """
    Класс ассоциативнового словаря.
    """
    
    def __init__(self, uniq_name, assc_key, assc_val,
                 res_path=None, subsys='', buffSize=accDictBuffSize):
        """
        Конструктор частотного словаря.
        
        @type uniq_name: C{string}
        @param uniq_name: Уникальное имя словаря.
        @type assc_key: C{tuple}
        @param assc_key: Картеж, задающий ассоциативный ключ. Элементами картежа
            являются имена ключевых полей.
        @type assc_val: C{tuple}
        @param assc_val: Картеж, задающий значение ассоциации.
        @type res_path: C{string}
        @param res_path: Путь до папки где хранится словрь <res_path/resource.var>.
        @type subsys: C{string}
        @param subsys: Имя подсистемы.
        @type buffSize: C{int}
        @param buffSize: Размер буфера по определенному ключу.
        """
        self.assc_key = assc_key
        self.assc_val = assc_val
        self.buffSize = buffSize

        persistant.icPersistant.__init__(self, uniq_name, 'adt', res_path, subsys)

        local_dir = ic_user.icGet('LOCAL_DIR')
        if not self.res_path and local_dir:
            self.res_path = ic_file.NormPathUnix(local_dir+'/')

        #   Читаем словарь
        self._model = {}
        self._model = self.LoadDict()
        
        #   Если он не создан еще - создаем его
        if not self._model:
            self._model = {}

    def GetKeyTuple(self):
        """
        Возвращает ключевой картеж.
        """
        return self.assc_key
        
    def GetValueTuple(self):
        """
        Возвращает картеж, задающий значения ассоциации.
        """
        return self.assc_val
        
    def LoadDict(self):
        """
        Читает словарь.
        
        @rtype: C{...}
        @return: Возвращает сохраненный объект.
        """
        self._model = self.Load()
        return self._model
        
    def SaveDict(self):
        """
        Сохраняет словарь в хранилище пользователя.

        @rtype: C{bool}
        @return: Признак успешного завершения операции.
        """
        return self.Save()

    def GetAssociateObj(self, key):
        """
        Возвращает значение по ключу. В случае если заданного ключа нет возвращает None.

        @type key: C{tuple}
        @param key: Ключ объекта в словаре.
        """
        if key in self._model:
            return self._model[key]
        
        return None
        
    def GetAssociateFld(self, key, fld_name):
        """
        Возвращает значение определенного поля ассоциации.
        
        @type key: C{tuple}
        @param key: Ключ объекта в словаре.
        @type fld_name: C{string}
        @param fld_name: Имя поля.
        """
        if key in self._model:
            vals = self._model[key][0]
            
            #   Определяем индекс поля
            try:
                indx = list(self.assc_val).index(fld_name)
                value = vals[indx]
                log.debug(u'>>> IN GetAssociateFld FIND FIELD Value = %s' % value)
                return value
            except:
                log.error(u'>>> fld_name value ERROR in GetAssociateFld fld_name: %s' % fld_name)
                log.fatal(u'>>> asscDict = %s' % self._model)
            
        return None
        
    def DelAssociation(self, key):
        """
        Удаляет ассоциацию из словаря.
        
        @type key: C{tuple}
        @param key: Ключ объекта в словаре.
        @rtype: C{bool}
        @return: Признак успешного удаления.
        """
        if key in self._model:
            self._model.pop(key)
            return True
            
        return False
        
    def Update(self, obj, *args, **kwargs):
        """
        Объединяет два ассоциативных словаря в один.

        @type obj: C{icAssociationDict}
        @param obj: Другой ассоциативный словарь.
        @return: Дополненную метомодель словаря.
        """
        #   Список новых ключей
        addkey = []

        if obj is None:
            model = None
        else:
            model = obj.GetModel()

        if model is None:
            return self._model
        
        for key, val in model.items():
        
            if key not in self._model.keys():
                self._model[key] = val
                addkey.append(key)
            else:
                self._model[key][1] = self._model[key][1] + val[1]
                        
        #   Упорядочиваем буфер и по необходимости чистим
        self.AddInAsscDict()
        
        return self._model
        
    def AddInAsscDict(self, key=None, val=None):
        """
        Добавляет вариант в словарь, упорядочивает его и по необходимости чистит.

        @type key: C{tuple}
        @param key: Ключ объекта в словаре.
        @type val: C{dictionary}
        @param val: Добавляемый вариант.
        """
        if val and key in self._model:
            self._model[key][0] = val
            self._model[key][1] += 1
        else:
            #   Сортируем в порядке уменьшения частоты использования ассоциации
            lst = [((x, self._model[x][0]), self._model[x][1]) for x in self._model.keys()]
            lst.sort(cmpRows)
            new_buff = {}

            #   По необходимости чистим буфер - выкидываем наименее
            #   используемые варианты
            if len(self._model) > self.buffSize*2:

                ######################################################################
                #   Нормируем показания счетчиков, чтобы у новых вариантов была возможность
                #   задержаться в буфере, в противном случае начиная с некоторого момента
                #   в буффере будут оставатся варианты с большим показанием счетчика, превысить
                #   которое новый вариант в принципе не сможет.
                ######################################################################
                        
                factor = float(self.buffSize)/lst[0][1]
                if factor > 1:
                    factor = 1
                            
                log.debug(u'>>> real norma factor = %s' % factor)
                for x in lst[:self.buffSize]:
                    new_buff[x[0][0]] = [x[0][1], x[1]*factor]
            else:
                for x in lst:
                    new_buff[x[0][0]] = [x[0][1], x[1]]
            
            self._model = new_buff
            
            #   Добавляем новый вариант
            if key and val:
                log.debug(u'>>> AddInAsscDict: key,val= %s, %s\t%s' % (key, [val, 1], new_buff))
                self._model[key] = [val, 1]
        
        return self._model
