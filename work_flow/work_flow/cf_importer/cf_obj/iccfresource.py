#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс работы с ресурсом элемента конфигурации 1с, разобранной V8Unpack v2.0.
"""

import os
import os.path
import re

# try:
#     from utils import util
# except:
#     pass
from ic.log import log

RE_UID_PATTERN = r'........-....-....-....-............'
RE_DATE_PATTERN = r',([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]),'
RE_BINARY_PATTERN = r',([0-9a-zA-Z+!?/=\s]*)=]'
RE_BASE64_PATTERN = r'#base64:([0-9a-zA-Z+!?/=\s]*)]'

RESOURCE_PREFIX = '\xef\xbb\xbf'


class icCFResource:
    """
    Класс менеджера управления ресурсом объекта конфигурации.
    """
    def __init__(self, cf_res_filename=None):
        """
        Конструктор.
        @param cf_res_filename: Полное имя ресурса объекта конфигурации.
        """
        self.cf_res_filename = None
        if cf_res_filename:
            self.cf_res_filename = os.path.abspath(cf_res_filename)
        
        # Непосредственно данные ресурса
        self.data = None
        
    def loadData(self, cf_res_filename=None):
        """
        Загрузить данные из ресурсного файла.
        @param cf_res_filename: Полное имя ресурса объекта конфигурации.
        """
        if cf_res_filename:
            self.cf_res_filename = os.path.abspath(cf_res_filename)
        
        if os.path.exists(self.cf_res_filename):
            f_res = None            
            try:
                f_res = open(self.cf_res_filename)
                txt_data = f_res.read()
                f_res.close()
            except:
                if f_res:
                    f_res.close()
                f_res = None
                log.fatal()
            
            try:    
                self.data = self._parseTxt2Data(txt_data)
            except:
                log.fatal(u'ERROR: Parse resource file: <%s>' % self.cf_res_filename)
        else:
            log.warning(u'ERROR: CF resource file <%s> not found!' % self.cf_res_filename)
        
    def _parseTxt2Data(self, txt_data):
        """
        Пропарсить текстовые данные.
        """
        txt_data = txt_data.replace('{', '[').replace('}', ']').replace('"', '"""')
        txt_data = txt_data.replace('\r', '')        
        txt_data.strip()
   
        # Обрамить бинарные данные кавычками
        re_binary_list = re.findall(RE_BINARY_PATTERN, txt_data)
        binary_lst = []
        for binary in re_binary_list:
            if binary not in binary_lst:
                binary_lst.append(binary)
        for binary in binary_lst:
            txt_data = txt_data.replace(binary + '=', '\'\'\'' + binary + '=\'\'\'')
        re_binary_list = re.findall(RE_BASE64_PATTERN, txt_data)
        binary_lst = []
        for binary in re_binary_list:
            if binary not in binary_lst:
                binary_lst.append(binary)
        for binary in binary_lst:
            txt_data = txt_data.replace('#base64:' + binary + ']', '\'\'\'#base64:' + binary + '\'\'\']')
        
        # Обрамление всех UIDов кавычками
        re_uid_list = re.findall(RE_UID_PATTERN, txt_data)
        uid_lst = []
        for uid in re_uid_list:
            if uid not in uid_lst:
                uid_lst.append(uid)
        for uid in uid_lst:
            txt_data = txt_data.replace(uid, '\'' + uid + '\'')

        # Обрамление всех дат кавычками
        re_date_list = re.findall(RE_DATE_PATTERN, txt_data)
        date_lst = []
        for date in re_date_list:
            if date not in date_lst:
                date_lst.append(date)
        for date in date_lst:
            txt_data = txt_data.replace(date, ',\'' + date + '\',')

        # Убрать все двойные запятые из текста
        while (',,' in txt_data) or (', ,' in txt_data):
            txt_data = txt_data.replace(',,', ',').replace(', ,', ',')

        try:
            data = eval(txt_data)
        except:
            log.fatal(u'ERROR! Resource syntax error: <%s>' % unicode(txt_data, 'utf-8'))
            data = None
        
        return data

    def _str(self, data):
        if isinstance(data, str):
            if data[:8] == '#base64:':
                return data.replace('\n', '\r\r\n').replace('\\n', '\r\r\n')
            else:
                return '"' + data.replace('\n', '\r\n') + '"'
        elif isinstance(data, unicode):
            return '"' + data.encode('utf-8') + '"'
        else:
            return str(data)
        
    def _data2txt(self, data):
        """
        Преобразовать данные в текст в формате необходимым для конвертации.
        """
        result_txt = ''
        if isinstance(data, list):
            result_txt += '{'
            count = len(data) - 1
            for i, value in enumerate(data):
                if isinstance(value, list):
                    result_txt += '\r\n'
                    result_txt += self._data2txt(value)
                    if i == count:
                        result_txt += '\r\n'
                else:
                    result_txt += self._str(value)
                # Если элемент не последний, то добавить запятую
                if i < count:
                    result_txt += ','
            result_txt += '}'
        return result_txt
        
    def _parseData2Txt(self, data):
        """
        Преобразовать данные в текст.
        """
        data = util.structStrRecode(data, 'unicode', 'utf-8')
        txt_data = self._data2txt(data)
        txt_data = RESOURCE_PREFIX + txt_data
        
        # все UIDы
        uid_list = re.findall(RE_UID_PATTERN, txt_data)
        uid_lst = []
        for uid in uid_list:
            if uid not in uid_lst:
                uid_lst.append(uid)
        for uid in uid_lst:
            txt_data = txt_data.replace('"' + uid + '"', uid)

        # все даты
        date_list = re.findall(RE_DATE_PATTERN, txt_data)
        date_lst = []
        for date in date_list:
            if date not in date_lst:
                date_lst.append(date)
        for date in date_lst:
            txt_data = txt_data.replace('"' + date + '"', date)

        txt_data = txt_data.replace('\\n', '\r\n')
        txt_data = txt_data.replace('\\t', '\t')

        return txt_data

    def saveData(self, cf_res_filename=None):
        """
        Записать данные в ресурсный файл.
        @param cf_res_filename: Полное имя ресурса объекта конфигурации.
        """
        if cf_res_filename:
            self.cf_res_filename = os.path.abspath(cf_res_filename)

        txt_data = self._parseData2Txt(self.data)
        
        f = None
        try:
            f = open(self.cf_res_filename, 'w')
            f.write(txt_data)
            f.close()
            return True
        except:
            if f:
                f.close()
                f = None
            log.fatal(u'Ошибка записи данных')
        return False
    
    def getByIdxList(self, idx_list, res=None):
        """
        Получить часть ресурса по списку индексов.
        """
        if res is None:
            res = self.data
        if len(idx_list) > 1:
            return self.getByIdxList(idx_list[1:], res[idx_list[0]])
        else:
            return res[idx_list[0]]        
        
        
def test():
    """
    Функция тестирования.
    """
    import sys
    
    dir_path = os.path.dirname(__file__)
    if not dir_path:
        dir_path = os.getcwd()
        
    sys.path.append(os.path.dirname(dir_path))
    
    res_filename = os.path.abspath(dir_path + '/test/root')
    print('RES FILE:', res_filename)
    if os.path.exists(res_filename):
        res = icCFResource(res_filename)
        res.loadData()
        print('RES:', res.data)


def test1():
    """
    Функция тестирования.
    """
    dir_path = os.path.dirname(__file__)
    if not dir_path:
        dir_path = os.getcwd()
        
    res_filename = os.path.dirname(os.path.dirname(dir_path)) + '/example/form'
    print('RES FILE:', res_filename)
    if os.path.exists(res_filename):
        res = icCFResource(res_filename)
        res.loadData()
        print('RES:', res.data[2])


if __name__ == '__main__':
    test()
