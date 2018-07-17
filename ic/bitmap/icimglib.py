#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер работы с библиотекой образов.
"""

# --- Подключение библиотек ---
import types
from ic.log import log
from ic.dlg import ic_dlg
from ic.utils import ic_file
from ic.kernel import io_prnt
from ic.utils import util
from ic.utils import ic_mode
from ic.bitmap import icimg2py

# --- Константы ---
# Шаблон файла библиотеки образов
_ImageLibraryFileTemplate = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Библиотека образов.
\"\"\"

# --- Imports ---
from wx import ImageFromStream, BitmapFromImage
from wx import EmptyIcon
import cStringIO

'''

_ImageBlockTemplate = '''# --- BEGIN %s
def get%sData():
    return %s


def get%sBitmap():
    return BitmapFromImage(get%sImage())


def get%sImage():
    stream = cStringIO.StringIO(get%sData())
    return ImageFromStream(stream)


def get%sIcon():
    icon = EmptyIcon()
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
    
    def __init__(self, sImgLibFileName=None):
        """
        Крструктор.
        @param sImgLibFileName: Файл библиотеки образов *.py.
        """
        # Файл библиотеки образов
        self._img_lib_file_name = sImgLibFileName
        self._img_lib_file = None
        self._img_lib_text = None

    def getImgLibFileName(self):
        return self._img_lib_file_name
        
    def loadImgLib(self, sImgLibFileName=None):
        """
        Загрузить текст библиотеки образов.
        @param sImgLibFileName: Файл библиотеки образов *.py.
        """
        if not sImgLibFileName:
            sImgLibFileName = self._img_lib_file_name
            
        if sImgLibFileName and sImgLibFileName != self._img_lib_file_name:
            self._img_lib_file_name = sImgLibFileName
            
        self._img_lib_file = None
        try:
            self._img_lib_file = open(sImgLibFileName, 'r')
            self._img_lib_text = self._img_lib_file.read()
            self._img_lib_file.close()
            self._img_lib_file = None

            if ic_mode.isDebugMode():
                io_prnt.outLog(u'Загрузка библиотеки образов <%s>' % sImgLibFileName)
            return self._img_lib_text
        except:
            io_prnt.outErr(u'Ошибка загрузки файла библиотеки образов <%s>' % sImgLibFileName)
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
        
    def createImgBlock(self, ImgName_, ImgData_):
        """
        Создать блок образа.
        @param ImgName_: Имя добавляемого объекта.
        @param ImgData_: Сериализованные данные файла образа.
        """
        if isinstance(ImgName_, unicode):
            ImgName_ = ImgName_.encode()
        
        # Заменить <-> в именах образа на <_>
        ImgName_ = ImgName_.replace('-', '_')
        
        n = ImgName_
        d = ImgData_
        return _ImageBlockTemplate % (n, n, d, n, n, n, n, n, n, n, n, n)
        
    def getImgData(self, ImgFileName_):
        """
        Получить данные образа из файла образа.
        @param ImgFileName_: Имя файла образа.
        """
        return icimg2py.getImgFileData(ImgFileName_)
        
    def addImgBlock(self, ImgBlock_):
        """
        Добавить блок образа к библиотеке.
        @param ImgBlock_: Блок образа.
        """
        if not self._img_lib_text:
            self.createNewImgLib()
        self._img_lib_text += ImgBlock_
        return self._img_lib_text

    def addImg(self, ImgFileName_):
        """
        Добавить образ в библиотеку образов из файла.
        @param ImgFileName_: Имя файла образа.
        """
        img_name = ic_file.SplitExt(ic_file.BaseName(ImgFileName_))[0]
        img_data = self.getImgData(ImgFileName_)
        if img_data:
            img_block = self.createImgBlock(img_name, img_data)
            self.addImgBlock(img_block)
        
    def saveImgLib(self, sImgLibFileName=None):
        """
        Сохранить изменения в библиотеку образов.
        @param sImgLibFileName: Файл библиотеки образов *.py.
        @return: Возвращает результат выполнения операции True/False.
        """
        if not sImgLibFileName:
            sImgLibFileName = self._img_lib_file_name
            
        if sImgLibFileName and sImgLibFileName != self._img_lib_file_name:
            self._img_lib_file_name = sImgLibFileName
            
        self._img_lib_file = None
        try:
            self._img_lib_file = open(sImgLibFileName, 'w')
            self._img_lib_file.write(self._img_lib_text)
            self._img_lib_file.close()
            self._img_lib_file = None
            return True
        except:
            io_prnt.outErr(u'Ошибка сохранения файла библиотеки образов <%s>' % sImgLibFileName)
            if self._img_lib_file:
                self._img_lib_file.close()
                self._img_lib_file = None
            return False

    def findImgBlock(self, ImgName_):
        """
        Найти блок образа в библиотеке образов.
        @param ImgName_: Имя объекта.
        @return: Возвращает кортеж позиции начала и конца или None, если блок не найден.
        """
        if isinstance(ImgName_, unicode):
            ImageName_ = ImgName_.encode()
        try:
            begin = self._img_lib_text.find(BEGIN_IMG_SIGNATURE % ImgName_)
            end = self._img_lib_text.find(END_IMG_SIGNATURE % ImgName_)
            if begin == -1 or end == -1:
                return None
            if end >= 0:
                while self._img_lib_text[end] != '\n':
                    end += 1
            return begin, end
        except:
            io_prnt.outErr(u'Ошибка поиска блока образа <%s>.' % ImgName_)
            return None
          
    def delImgBlock(self, ImgName_):
        """
        Удалить блок образа по имени.
        @param ImgName_: Имя объекта.
        @return: Возвращает результат выполнения операции True/False.
        """
        if isinstance(ImgName_, unicode):
            ImgName_ = ImgName_.encode()

        begin_end = self.findImgBlock(ImgName_)
        if begin_end:
            begin, end = begin_end
            self._img_lib_text = self._img_lib_text[:begin]+self._img_lib_text[end:]
            return True
        return False
   
    def findImgData(self, ImgName_):
        """
        Получить из библиотеки образов данные образов по имени образа.
        @param ImgName_: Имя объекта.
        @return: Возвращает строку данных образа или 
            None, если образ с таким именем не найден.
        """
        if isinstance(ImgName_, unicode):
            ImgName_ = ImgName_.encode()

        module = util.icLoadSource('img_lib_module', self._img_lib_file_name)
        img_data_func_name = 'get%sData' % ImgName_
        if img_data_func_name in dir(module):
            img_data = icimg2py.crunchImgData(module.__dict__[img_data_func_name]())
            return img_data
        else:
            return None        
        
    def renameImgBlock(self, ImgName_, NewImgName_):
        """
        Переименовать блок.
        @param ImgName_: Имя объекта.
        @param NewImgName_: Новое имя объекта.
        @return: True/False.
        """
        if isinstance(ImgName_, unicode):
            ImgName_ = ImgName_.encode()
        if isinstance(NewImgName_, unicode):
            NewImgName_ = NewImgName_.encode()
            
        img_data = self.findImgData(ImgName_)
        if img_data:
            new_img_block = self.createImgBlock(NewImgName_, img_data)
            self.delImgBlock(ImgName_)
            self.addImgBlock(new_img_block)
            return True
        return False
            
    def getImages(self, sImgLibFileName=None):
        """
        Получить словарь оборазов из библиотеки образов.
        @param sImgLibFileName: Файл библиотека образов.
        """
        # Импорт модуля библиотеки образов
        if sImgLibFileName is None:
            sImgLibFileName = self._img_lib_file_name
        
        img_dict = None
        if sImgLibFileName:
            module = util.icReLoadSource('img_lib_module', sImgLibFileName)
            # Заполенение словаря образов
            img_dict = dict([(var_name, module.__dict__[var_name]) for var_name in [var for var in dir(module) if type(module.__dict__[var]).__name__ == 'Bitmap']])
            log.debug('IMAGES: %s' % img_dict.keys())
        return img_dict
    
    def isEmpty(self):
        """
        НЕ определена библиотека образов?
        """
        return not self._img_lib_text
