#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль форм просмотра схем документов.
"""

import os
import os.path

from archive.forms import scheme_doc_form_proto
import ic
from ic.log import log
from ic.engine import form_manager
from ic.dlg import dlgfunc

# Version
__version__ = (0, 0, 3, 2)


class icSchemeDocPanel(scheme_doc_form_proto.icSchemeDocPanelProto,
                       form_manager.icFormManager):
    """
    Панель просмотра схем документов.
    """
    
    def init(self):
        """
        Инициализация панели.
        """
        self.init_images()
        
    def init_images(self):
        """
        Инициализация картинок контролов.
        """
        self.setLibImages_ToolBar(tool_bar=self.ctrl_toolBar,
                                  view_tool='eye.png',
                                  edit_tool='document--pencil.png')
    
    def onEditToolClicked(self, event):
        """
        Обработчик инструмента редактирования текущего выбранного документа.
        """
        selected_shape = self.scheme_viewer_ctrl.getSelectedShape()
        if selected_shape:
            doc_uuid = selected_shape.id
            
            doc = ic.metadata.THIS.mtd.scan_document.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Редактирование документа UUID <%s>' % doc_uuid)            
            from archive.forms import edit_doc_form
            result = edit_doc_form.edit_doc_dlg(doc=doc)
            if result:
                doc.save_obj()
                self.refreshDiagram(doc)
                
        event.Skip()
        
    def refreshDiagram(self, doc=None):
        """
        Обновить диаграмму.
        """
        if doc:
            try:
                scheme = doc.GetManager().get_scheme_data()
                self.scheme_viewer_ctrl.setDiagram(scheme)
                self.scheme_viewer_ctrl.Refresh(False)
            except:
                log.fatal(u'Ошибка обновления схемы для документа <%s>' % doc.getRequisiteValue('uuid'))
        else:
            log.warning(u'Не определен документ для обновления схемы')

    def viewScanFile(self, scan_filename):
        """
        Открыть программу просмотра файла скана.
        :param scan_filename: Файл скана.
        """
        if not scan_filename:
            msg = u'Файл скана не определен'
            log.warning(msg)
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', msg, parent=self)
            return
        if not os.path.exists(scan_filename):
            msg = u'Файл <%s> не найден' % scan_filename
            log.warning(msg)
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!', msg, parent=self)
            return
        file_ext = os.path.splitext(scan_filename)[1]
        if file_ext in ('.pdf', '.PDF'):
            # Формат PDF
            cmd = 'evince %s&' % scan_filename
        elif file_ext in ('.jpg', '.jpeg', '.tiff', '.bmp'):
            # Графический формат файла
            cmd = u'eog %s&' % scan_filename
        else:
            log.warning(u'Не поддерживаемый тип файла <%s>' % file_ext)
        if cmd:
            os.system(cmd)        

    def onViewToolClicked(self, event):
        """
        Обработчик инструмента просмотра текущего выбранного документа.
        """
        selected_shape = self.scheme_viewer_ctrl.getSelectedShape()
        if selected_shape:
            doc_uuid = selected_shape.id
            
            doc = ic.metadata.THIS.mtd.scan_document.create()
            doc.load_obj(doc_uuid)
            log.debug(u'Просмотр документа UUID <%s>' % doc_uuid)            
            scan_filename = doc.getRequisiteValue('file_name')
            self.viewScanFile(scan_filename)
                
        event.Skip()
            