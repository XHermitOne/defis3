#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource module </mnt/defis/defis3/archive/archive/nsi_body_type.tab>
File            </mnt/defis/defis3/archive/archive/nsi_body_type_tab.py>
Description     <Resource module>
"""

from ic.interfaces import icmanagerinterface

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/nsi_body_type.tab

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 0, 1)

# ВНИМАНИЕ! В s2 записываем команду Linux для получения
# Из файла документа текста этого документа
# Далее запускаем ее с помощью popen и получаем результат
DEFAULT_TAB_DATA = (dict(cod='PDF-', name=u'PDF документ', s1='pdf', s2='convert {{ FILENAME }}[0] {{ PROFILE_DIR }}/out.jpg; tesseract -l rus {{ PROFILE_DIR }}/out.jpg stdout'),
                    dict(cod='JPG-', name=u'JPG документ', s1='jpg', s2='cp {{ FILENAME }} {{ PROFILE_DIR }}/out.jpg; tesseract -l rus {{ PROFILE_DIR }}/out.jpg stdout'),
                    dict(cod='TIFF', name=u'TIFF документ', s1='tiff', s2='convert {{ FILENAME }} {{ PROFILE_DIR }}/out.jpg; tesseract -l rus {{ PROFILE_DIR }}/out.jpg stdout'),
                    dict(cod='DOC-', name=u'Windows Word документ', s1='doc', s2='unoconv --format=pdf --output={{ PROFILE_DIR }}/out.pdf {{ FILENAME }}; convert {{ PROFILE_DIR }}/out.pdf[0] {{ PROFILE_DIR }}/out.jpg; tesseract -l rus {{ PROFILE_DIR }}/out.jpg stdout'),
                    dict(cod='ODT-', name=u'LibreOffice Writer документ', s1='odt', s2='unoconv --format=pdf --output={{ PROFILE_DIR }}/out.pdf {{ FILENAME }}; convert {{ PROFILE_DIR }}/out.pdf[0] {{ PROFILE_DIR }}/out.jpg; tesseract -l rus {{ PROFILE_DIR }}/out.jpg stdout'),
                    )


class icNSIBodyTypeTabManager(icmanagerinterface.icWidgetManager):
    """
    Менеджер таблицы справочника типов 
    содержания отсканированных документов.
    """

    def onInit(self, event):
        pass

    def set_default_data(self):
        """
        Установка значений справочника по умолчанию.
        """
        tab = self.get_object()
        
        # Очистить таблицу
        tab.clear()
        
        for record in DEFAULT_TAB_DATA:
            record['type'] = 'nsi_body_type'
            tab.add(**record)            
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icNSIBodyTypeTabManager
