#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс поддержки частотного словаря.
Функции частотного словаря.
Частотный словарь хранит по определенному ключу (имя поля/тескстового поля) список ранее
вводимых вариантов значений с счетчиком вводов. При достяжении определенного размера списка
некоторое количество наименее используемых вариантов удаляются.
"""

import os
import os.path
import wx

try:
    from . import persistant
except ImportError:
    import persistant
except ValueError:
    import persistant

from ic.utils import ic_file
from ic.utils import ic_str


__version__ = (1, 0, 2, 1)

#   Размер буфера по определенному ключу
freqDictBuffSize = 50

#   Размер текста после которого функция OnAutoTextFill начинает предоставлять
#   варианты ввода
fillStartPosition = 3

DEFAULT_FREQUENCYDICT_NAME = 'frequencydict'
DEFAULT_KEY_NAME = 'frequencykey'

DEFAULT_ENCODING = 'utf-8'
ALTERNATIVE_ENCODING = 'cp1251'


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
    

class icFrequencyDict(persistant.icPersistant):
    """
    Частотный словарь.
    """

    def __init__(self, uniq_name, res_path=None, subsys='',
                 start_pos=fillStartPosition, buffSize=freqDictBuffSize):
        """
        Конструктор частотного словаря.
        @type uniq_name: C{string}
        @param uniq_name: Уникальное имя словаря.
        @type res_path: C{string}
        @param res_path: Путь до папки где хранится словрь <res_path/resource.var>.
        @type subsys: C{string}
        @param subsys: Имя подсистемы.
        @type start_pos: C{int}
        @param start_pos: Позиция курсора текста после которой функция OnAutoTextFill
            начинает генерировать варианты продолжения слов.
        @type buffSize: C{int}
        @param buffSize: Размер буфера по определенному ключу.
        """
        persistant.icPersistant.__init__(self, uniq_name, 'fdt', res_path=res_path, subsys=subsys)
        self.start_pos = start_pos
        self.buffSize = buffSize
        local_dir = ic_file.getPrjProfilePath()
        if not self.res_path and local_dir:
            self.res_path = os.path.normpath(local_dir)
        
        #   Читаем словарь
        self._model = {}
        self._model = self.LoadDict()
        
        #   Если он не создан еще - создаем его
        if not self._model:
            self._model = {}
        
    def SetStartPos(self, start_pos):
        """
        Устанавливает значение позиций курсора текста после которой функция OnAutoTextFill
        начинает генерировать варианты продолжения слов.
        @type start_pos: C{int}
        @param start_pos: Позиция курсора текста после которой функция OnAutoTextFill
            начинает генерировать варианты продолжения слов.
        """
        self.start_pos = start_pos

    def GetStartPos(self):
        """
        Возвращает значение позиций курсора текста после которой функция
        OnAutoTextFill начинает генерировать варианты продолжения слов.
        """
        return self.start_pos
                
    def LoadDict(self):
        """
        Читает словарь.
        @rtype: C{...}
        @return: Возвращает сохраненный объект.
        """
        self._model = self.LoadPersistent()
        return self._model
        
    def SaveDict(self):
        """
        Сохраняет словарь в хранилище пользователя.
        @rtype: C{bool}
        @return: Признак успешного завершения операции.
        """
        return self.SavePersistent()

    def UpdateDict(self, obj, *args, **kwargs):
        """
        Объединяет два частотных словаря в один.
        @type obj: C{icFrequencydict}
        @param obj: Частотный словарь информация из которого добавляется в текущий словарь.
        @return: Дополненную метомодель частотного словаря.
        """
        #   Список новых ключей
        addkey = []
        if obj is None:
            model = None
        else:
            model = obj
        
        if model is None:
            return self._model
            
        for key, val in model.items():
            if key not in self._model.keys():
                self._model[key] = val
                addkey.append(key)
            else:
                #   Определяем списки слов в разных словарях
                lst_self = [x[0] for x in self._model[key]]
                lst_obj = [x[0] for x in val]
                for indx, word in enumerate(lst_obj):
                    if word not in lst_self:
                        self._model[key].append(val[indx])
                    else:
                        #   Обновляем счетчик
                        i = lst_self.index(word)
                        self._model[key][i][1] += val[indx][1]
                        
        #   Упорядочиваем буфер и по необходимости чистим
        for key in self._model:
            if key not in addkey:
                self.AddWordInFreqDict(key)
        
        return self._model

    def gen_words(self, *value_list):
        """
        Разбивка списка предложенных значений на слова и их сортировка.
        В новом варианте используем сортировку по тексту в нижнем регистре
        @param value_list: Список часто используемых значений.
        @return: Список часто используемых значений отсортированных и с выделенными словами.
            Например:
            Список ['Договор поставки оборудования'] разобъется на
            ['договор', 'договор поставки', 'договор поставки оборудования']
        """
        result = list()
        for value in value_list:
            if not isinstance(value, unicode):
                value = ic_str.toUnicode(value, DEFAULT_ENCODING)
            words = value.split(u' ')

            sub_value = u''
            for word in words:
                sub_value = sub_value + u' ' + word
                sub_value = sub_value.strip()
                if sub_value not in result:
                    result.append(sub_value)

        result = sorted(result, key=lambda item: item[0].lower())
        return result

    def gen_words_with_count(self, *frecuency_value_list):
        """
        Сгенерировать список часто используемых слов с коэффициентом использивания.
        @param frecuency_value_list: Список элементов часто используемых слов:
            Элемент списка: (u'Часто используемое слово или фраза',
                               коэффициент/счетчик использования).
        @return: Откорректированный список. См.метод gen_words.
        """
        values = [txt_value for txt_value, n_count in frecuency_value_list]
        word_values = self.gen_words(*values)
        word_count = len(word_values)
        return [[word_value, word_count - i] for i, word_value in enumerate(word_values)]

    def FindBestVar(self, key, txt):
        """
        Возвращает наиболее часто повоторяющийся вариант слова.
        @type key: C{string}
        @param key: Ключ объекта (имя поля) в частотном словаре.
        @type txt: C{string}
        @param txt: Слово по которому ищем.
        """
        freqDict = self._model
        #   Получаем все варианты
        if freqDict and key in freqDict:
            col_var = self.gen_words_with_count(*freqDict[key])
        else:
            col_var = []

        #   Берем первый попавшийся подходящий вариант
        var = None
        for v in col_var:
            w = v[0]
            if not isinstance(w, unicode):
                try:
                    w = unicode(w, DEFAULT_ENCODING)
                except UnicodeDecodeError:
                    w = unicode(w, ALTERNATIVE_ENCODING)
            if w.find(txt) == 0:
                var = w
                break
            
        return var
        
    def AutoTextFill(self, text_ctrl, key=None):
        """
        Обрабатывает сообщение <icEvents.EVT_TEXT_TEMPL>. Используется для того,
        чтобы предаставить пользователю вариант текста, который он уже вводил.
        @type text_ctrl: C{wx.TextCtrl}
        @param text_ctrl: Указатель на объект ввода.
        @type key: C{string}
        @param key: Ключ объекта (имя поля) в частотном словаре.
        """
        if key is None:
            key = str(text_ctrl.name) if hasattr(text_ctrl, 'name') else DEFAULT_KEY_NAME

        freqDict = self._model
        #   Проверяем, что редактор еще открыт
        if text_ctrl.IsShown():
            txt = text_ctrl.GetValue()
            if len(txt) >= self.start_pos:
                #   Ищем лучший вариант продолжения
                var = self.FindBestVar(key, txt)
                # print(u'Найдено <%s>' % var)
                if var and len(var) > len(txt):
                    txt = txt + var[len(txt):]
                    pt = text_ctrl.GetInsertionPoint()
                    wx.TextCtrl.SetValue(text_ctrl, txt)
                    text_ctrl.SetInsertionPoint(pt)
                    # Текст от курсора до конца выделяем
                    text_ctrl.SetSelection(pt, -1)
    
    def AddTextFill(self, text_ctrl, key=None):
        """
        Добавляем введеный в контроле текст в частотный словарь.
        @type text_ctrl: C{wx.TextCtrl}
        @param text_ctrl: Указатель на объект ввода.
        @type key: C{string}
        @param key: Ключ объекта (имя поля) в частотном словаре.
        @return: True/False. 
        """
        if key is None:
            key = str(text_ctrl.name) if hasattr(text_ctrl, 'name') else DEFAULT_KEY_NAME

        if text_ctrl:
            value = text_ctrl.GetValue()
            if not isinstance(value, unicode):
                try:
                    value = unicode(value, DEFAULT_ENCODING)
                except UnicodeDecodeError:
                    value = unicode(value, ALTERNATIVE_ENCODING)
            self.AddWordInFreqDict(key, val=value)
            return True
        return False

    def AddWordInFreqDict(self, key, val=None):
        """
        Упорядочивает список слов и вобавляет слово в частотный словарь ввода.
        Если значение слова не передается, то буфер только упорядочивается по 
        убыванию частоты обращений к слову.
        @type key: C{string}
        @param key: Ключ объекта (имя поля) в частотном словаре.
        @type val: C{string}
        @param val: Добавляемое слово.
        """
        if not key:
            return
        if key in self._model:
            bFind = False
            #   Проверяем на наличие данного слова в словаре
            for v in self._model[key]:
                if v[0] == val:
                    v[1] += 1
                    bFind = True
                    break
            #   Сортируем в порядке уменьшения частоты ввода опреде-
            #   ленного слова
            # self._model[key].sort(cmpRows)

            self._model[key] = self.gen_words_with_count(*self._model[key])

            #   Если слово впервые вводится
            if not bFind:
                buff_size = self.buffSize
                #   По необходимости чистим буфер - выкидываем наименее
                #   используемые слова
                if len(self._model[key]) > buff_size*2:
                    self._model[key] = self._model[key][:buff_size]
                    ######################################################################
                    #   Нормируем показания счетчиков, чтобы у новых вариантов была возможность
                    #   задержаться в буфере, в противном случае начиная с некоторого момента
                    #   в буффере будут оставатся варианты с большим показанием счетчика, превысить
                    #   которое новый вариант в принципе не сможет.
                    ######################################################################
                    factor = float(buff_size)/self._model[key][0][1]
                    if factor > 1:
                        factor = 1
                    self._model[key] = [[x[0], int(x[1]*factor+1)]+x[2:] for x in self._model[key]]
                #   Добавляем новое слово
                if val:
                    self._model[key].append([val, 1])
        elif val:
            self._model[key] = [[val, 1]]
        
        return self._model

    def saveTextFillControls(self, **controls):
        """
        Сохранить автозаполнения заполнения контролов. 
        @param controls: Словарь контролов заполнения.
            Ключи словаря используются как ключи частотного словаря.
        @return: True/False. 
        """
        for ctrl_name, ctrl in controls.items():
            self.AddTextFill(ctrl, ctrl_name)
        self.SaveDict()  # Сохранить частотные словари для авто заполнений
        return True


def test_cmp_rows():
    """
    Тестовая функция.
    """
    words = [
             u'Договор поставки чайников',
             u'Договор подряда по мебели',
             u'Договор поставки',
             u'договор подряда',
             u'договор',
             ]
    for word in words:
        print(word)
    # words.sort(cmpRows)
    # words.sort()
    words = sorted(words, key=lambda item: item.lower())
    print()
    for word in words:
        print(word)


if __name__ == '__main__':
    test_cmp_rows()