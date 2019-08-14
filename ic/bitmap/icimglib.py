#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Менеджер работы с библиотекой образов.
"""

# --- Подключение библиотек ---
import os
import os.path

import ic.utils.impfunc
from ic.log import log
from ic.utils import util
from ic.utils import ic_mode
from ic.bitmap import icimg2py

__version__ = (0, 1, 1, 2)

# --- Константы ---
# Шаблон файла библиотеки образов
_ImageLibraryFileTemplate = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Библиотека образов.
\"\"\"

# --- Imports ---
import wx
import io

'''

_ImageBlockTemplate = '''# --- BEGIN %s
def get%sData():
    return %s


def get%sBitmap():
    return wx.Bitmap(get%sImage())


def get%sImage():
    stream = io.BytesIO(get%sData())
    return wx.Image(stream)


def get%sIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(get%sBitmap())
    return icon


%s = get%sBitmap()
# --- END %s
'''

# Сигнатуры начал аи конца определения образа
BEGIN_IMG_SIGNATURE = '# --- BEGIN %s'
END_IMG_SIGNATURE = '# --- END %s'


class icImgLibResource:
    """
    Менеджер работы с библиотекой образов.
    """
    
    def __init__(self, img_lib_filename=None):
        """
        Крструктор.
        @param img_lib_filename: Файл библиотеки образов *.py.
        """
        # Файл библиотеки образов
        self._img_lib_file_name = img_lib_filename
        self._img_lib_file = None
        self._img_lib_text = None

    def getImgLibFileName(self):
        return self._img_lib_file_name
        
    def loadImgLib(self, img_lib_filename=None):
        """
        Загрузить текст библиотеки образов.
        @param img_lib_filename: Файл библиотеки образов *.py.
        """
        if not img_lib_filename:
            img_lib_filename = self._img_lib_file_name
            
        if img_lib_filename and img_lib_filename != self._img_lib_file_name:
            self._img_lib_file_name = img_lib_filename
            
        self._img_lib_file = None
        try:
            self._img_lib_file = open(img_lib_filename, 'r')
            self._img_lib_text = self._img_lib_file.read()
            self._img_lib_file.close()
            self._img_lib_file = None

            if ic_mode.isDebugMode():
                log.info(u'Загрузка библиотеки образов <%s>' % img_lib_filename)
            return self._img_lib_text
        except:
            log.error(u'Ошибка загрузки файла библиотеки образов <%s>' % img_lib_filename)
            if self._img_lib_file:
                self._img_lib_file.close()
                self._img_lib_file = None
            return None
        
    def createNewImgLib(self):
        """
        Создание новой библиотеки образов.
        """
        self._img_lib_file_name = None
        self._img_lib_file = None
        self._img_lib_text = _ImageLibraryFileTemplate
        
    def createImgBlock(self, img_name, img_data):
        """
        Создать блок образа.
        @param img_name: Имя добавляемого объекта.
        @param img_data: Сериализованные данные файла образа.
        """
        # if isinstance(img_name, str):
        #    img_name = img_name.encode()
        
        # Заменить <-> в именах образа на <_>
        img_name = img_name.replace('-', '_')
        
        n = img_name
        d = img_data
        return _ImageBlockTemplate % (n, n, d, n, n, n, n, n, n, n, n, n)
        
    def getImgData(self, img_filename):
        """
        Получить данные образа из файла образа.
        @param img_filename: Имя файла образа.
        """
        return icimg2py.getImgFileData(img_filename)
        
    def addImgBlock(self, img_block):
        """
        Добавить блок образа к библиотеке.
        @param img_block: Блок образа.
        """
        if not self._img_lib_text:
            self.createNewImgLib()
        self._img_lib_text += img_block
        return self._img_lib_text

    def addImg(self, img_filename):
        """
        Добавить образ в библиотеку образов из файла.
        @param img_filename: Имя файла образа.
        """
        img_name = os.path.splitext(os.path.basename(img_filename))[0]
        img_data = self.getImgData(img_filename)
        if img_data:
            img_block = self.createImgBlock(img_name, img_data)
            self.addImgBlock(img_block)
        
    def saveImgLib(self, img_lib_filename=None):
        """
        Сохранить изменения в библиотеку образов.
        @param img_lib_filename: Файл библиотеки образов *.py.
        @return: Возвращает результат выполнения операции True/False.
        """
        if not img_lib_filename:
            img_lib_filename = self._img_lib_file_name
            
        if img_lib_filename and img_lib_filename != self._img_lib_file_name:
            self._img_lib_file_name = img_lib_filename
            
        self._img_lib_file = None
        try:
            self._img_lib_file = open(img_lib_filename, 'wt')
            self._img_lib_file.write(self._img_lib_text)
            self._img_lib_file.close()
            self._img_lib_file = None
            return True
        except:
            log.fatal(u'Ошибка сохранения файла библиотеки образов <%s>' % img_lib_filename)
            if self._img_lib_file:
                self._img_lib_file.close()
                self._img_lib_file = None
            return False

    def findImgBlock(self, img_name):
        """
        Найти блок образа в библиотеке образов.
        @param img_name: Имя объекта.
        @return: Возвращает кортеж позиции начала и конца или None, если блок не найден.
        """
        # if isinstance(img_name, unicode):
        #    ImageName_ = img_name.encode()
        try:
            begin = self._img_lib_text.find(BEGIN_IMG_SIGNATURE % img_name)
            end = self._img_lib_text.find(END_IMG_SIGNATURE % img_name)
            if begin == -1 or end == -1:
                return None
            if end >= 0:
                while self._img_lib_text[end] != '\n':
                    end += 1
            return begin, end
        except:
            log.fatal(u'Ошибка поиска блока образа <%s>.' % img_name)
            return None
          
    def delImgBlock(self, img_name):
        """
        Удалить блок образа по имени.
        @param img_name: Имя объекта.
        @return: Возвращает результат выполнения операции True/False.
        """
        # if isinstance(img_name, unicode):
        #    img_name = img_name.encode()

        begin_end = self.findImgBlock(img_name)
        if begin_end:
            begin, end = begin_end
            self._img_lib_text = self._img_lib_text[:begin]+self._img_lib_text[end:]
            return True
        return False
   
    def findImgData(self, img_name):
        """
        Получить из библиотеки образов данные образов по имени образа.
        @param img_name: Имя объекта.
        @return: Возвращает строку данных образа или 
            None, если образ с таким именем не найден.
        """
        # if isinstance(img_name, unicode):
        #     img_name = img_name.encode()

        module = ic.utils.impfunc.loadSource('img_lib_module', self._img_lib_file_name)
        img_data_func_name = 'get%sData' % img_name
        if img_data_func_name in dir(module):
            img_data = icimg2py.crunchImgData(module.__dict__[img_data_func_name]())
            return img_data
        else:
            return None        
        
    def renameImgBlock(self, img_name, new_img_name):
        """
        Переименовать блок.
        @param img_name: Имя объекта.
        @param new_img_name: Новое имя объекта.
        @return: True/False.
        """
        # if isinstance(img_name, unicode):
        #    img_name = img_name.encode()
        # if isinstance(new_img_name, unicode):
        #    new_img_name = new_img_name.encode()
            
        img_data = self.findImgData(img_name)
        if img_data:
            new_img_block = self.createImgBlock(new_img_name, img_data)
            self.delImgBlock(img_name)
            self.addImgBlock(new_img_block)
            return True
        return False
            
    def getImages(self, img_lib_filename=None):
        """
        Получить словарь оборазов из библиотеки образов.
        @param img_lib_filename: Файл библиотека образов.
        """
        # Импорт модуля библиотеки образов
        if img_lib_filename is None:
            img_lib_filename = self._img_lib_file_name
        
        img_dict = None
        if img_lib_filename:
            module = ic.utils.impfunc.reloadSource('img_lib_module', img_lib_filename)
            # Заполенение словаря образов
            img_dict = dict([(var_name, module.__dict__[var_name]) for var_name in [var for var in dir(module) if type(module.__dict__[var]).__name__ == 'Bitmap']])
            log.debug('IMAGES: %s' % img_dict.keys())
        return img_dict
    
    def isEmpty(self):
        """
        НЕ определена библиотека образов?
        """
        return not self._img_lib_text
