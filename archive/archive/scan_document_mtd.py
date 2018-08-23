#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Менеджер документов сканирования.

Перенос каталога отсканированных документов в другое место (сервер NFS):
1. Создаем папку монтирования. Например /mnt/zipdoc
2. Устанавливаем права 777
    sudo chmod -R 777 /mnt/zipdoc
3. Автомонтирование в /etc/fstab
    10.0.0.30:/zipdoc   /mnt/zipdoc     nfs     defaults    0   0
    Для того чтобы монтировались NFS разделы надо 
    устанавливать следующие пакеты:
    sudo apt-get install nfs-kernel-server nfs-common
4. Копируем туда каталог doc_catalog из старого места
5. Копируем этот же каталог в папку бекапа
6. Устанавливаем путь до новой папки каталога документов 
    /mnt/zipdoc/doc_catalog в атрибуте <folder> 
    каталогизатора <doc_cataloger>
7. Бекапим БД архива документов <library>.
8. В менеджере PostgreSQL PgadminIII выполняем т.к.в имени файла указывается 
    абсолютный путь до файла
    UPDATE scan_document_tab SET file_name = REPLACE(file_name, '/старый/путь', '/mnt/zipdoc');
9. Все
"""

import os
import os.path
import datetime
import ic
from ic import log
from ic.interfaces import icmanagerinterface
from ic.dlg import ic_dlg

### RESOURCE_MODULE: /mnt/defis/defis3/archive/archive/scan_document.mtd

### ---- Import external modules -----
### RESOURCE_MODULE_IMPORTS

#   Version
__version__ = (0, 0, 1, 3)

BORDER_WIDTH = 40
BORDER_HEIGHT = 40

DATE_FMT = '%Y-%m-%m'
NONE_DATE_FMT = 'XXXX-XX-XX'

# Используемые справочники
ARCHIVE_SPRAV_MANAGER = ic.metadata.archive.mtd.nsi_archive.create()
CONTRAGENT_SPRAV = ARCHIVE_SPRAV_MANAGER.getSpravByName('nsi_c_agent')


class icScanDocumentManager(icmanagerinterface.icWidgetManager):

    def onInit(self, evt):
        pass

    def create(self, doc=None):
        """
        Операция создания документа.
        """
        if doc is None:
            doc = self.get_object()
            
        numerator = ic.metadata.THIS.mtd.scan_doc_numerator.create()
        doc.setRequisiteValue('n_obj', numerator.do_gen())
        doc.setRequisiteValue('dt_create', datetime.datetime.now())        
        doc.setRequisiteValue('dt_state', datetime.datetime.now())        
        
        # ВНИМАНИЕ! При смене состояния любого документа запоминаем 
        # компьютер и пользователя которым были сделаны изменения
        doc.setRequisiteValue('computer', ic.getComputerName())
        doc.setRequisiteValue('username', ic.getCurUserName())
        doc.changeState('00')        
        
    def get_scheme_data(self, doc=None):
        """
        Определить данные схемы для документа.
        """
        if doc is None:
            doc = self.get_object()
            
        shapes = list()
        lines = list()
        
        doc_shape = self._gen_doc_shape(doc)
        # Выделяем отправной документ цветом
        doc_shape['brush'] = 'LIGHT_GREY_BRUSH'
        shapes.append(doc_shape)
        
        shapes, lines = self._gen_to_scheme(doc, doc_shape, shapes, lines)
        shapes, lines = self._gen_from_scheme(doc, doc_shape, shapes, lines)

        # Убрать наложение фигур
        shapes = self._allocate_vert(shapes)
        
        scheme = dict(shapes=shapes, lines=lines)
        return scheme
            
    def _gen_to_scheme(self, doc, doc_shape, shapes, lines):
        """
        Генерация части схемы по ссылкам НА документы.
        """
        to_docs = doc.getRequisiteValue('scan_doc_to')
        
        next_dy = 0
        for to_doc in to_docs:
            # print('to', to_doc['link_to'])
            new_doc = ic.metadata.THIS.mtd.scan_document.create()
            new_doc.load_obj(to_doc['link_to'])
            # ВНИМАНИЕ! Необходимо отсекать фигуры с
            # одинаковым UUID
            shape_uuids = [shape['name'] for shape in shapes]
            if to_doc['link_to'] not in shape_uuids:
                next_pos = (doc_shape['pos'][0]+doc_shape['size'][0]+BORDER_WIDTH,
                            doc_shape['pos'][1]+next_dy)
                new_shape = self._gen_doc_shape(new_doc, pos=next_pos)
                next_dy = new_shape['size'][1]+BORDER_HEIGHT
                shapes.append(new_shape)
            else:
                idx = shape_uuids.index(to_doc['link_to'])
                new_shape = shapes[idx]
            new_line = self._gen_line(doc_shape, new_shape)
            lines.append(new_line)
            self._gen_to_scheme(new_doc, new_shape, shapes, lines)

        return shapes, lines

    def _gen_from_scheme(self, doc, doc_shape, shapes, lines):
        """
        Генерация части схемы по ссылкам К документам.
        """
        from_docs = doc.getRequisiteValue('scan_doc_from')
        
        next_dy = 0
        for from_doc in from_docs:
            # print('from', from_doc['link_from'])
            new_doc = ic.metadata.THIS.mtd.scan_document.create()
            new_doc.load_obj(from_doc['link_from'])
            # ВНИМАНИЕ! Необходимо отсекать фигуры с
            # одинаковым UUID
            shape_uuids = [shape['name'] for shape in shapes]
            if from_doc['link_from'] not in shape_uuids:
                next_pos = (doc_shape['pos'][0]-doc_shape['size'][0]-BORDER_WIDTH,
                            doc_shape['pos'][1]+next_dy)
                next_pos = self._shift_shapes(next_pos, shapes)            
                new_shape = self._gen_doc_shape(new_doc, pos=next_pos)
                next_dy = new_shape['size'][1]+BORDER_HEIGHT
                shapes.append(new_shape)
            else:
                idx = shape_uuids.index(from_doc['link_from'])
                new_shape = shapes[idx]
            new_line = self._gen_line(new_shape, doc_shape)
            lines.append(new_line)
            self._gen_to_scheme(new_doc, new_shape, shapes, lines)
            
        return shapes, lines
        
    def _shift_shapes(self, pos, shapes):
        """
        Сдвинуть все фигуры, для вставки в начало новой.
        """
        x = pos[0]
        y = pos[1]
        dx = 100 - x if x < 100 else 0
        dy = 100 - y if y < 100 else 0
        for i, shape in enumerate(shapes):
            shape['pos'] = (shape['pos'][0] + dx,
                            shape['pos'][1] + dy)
            # shapes[i] = shape
            
        new_pos = (x, y)
        if dx:
            new_pos = (100, new_pos[1])
        if dy:
            new_pos = (new_pos[0], 100)  
        return new_pos
        
    def _allocate_vert(self, shapes):
        """
        Распределить фигуры по вертикали.
        Сделано для того чтобы фигуры не накладывались одна на другую.
        """
        is_shuffle = True
        
        while is_shuffle:
            is_shuffle = False
            for i, shape in enumerate(shapes):
                pos = shape['pos']
                prev_pos = [prev_shape['pos'] for prev_shape in shapes[:i]]
                # print 'Find', pos, prev_pos, pos in prev_pos
                if pos in prev_pos:
                    new_pos = (pos[0], pos[1]+shape['size'][1]+BORDER_HEIGHT)
                    #print 'Pos', pos, new_pos, shape['size'], prev_pos
                    shape['pos'] = new_pos
                    # shapes[i] = shape
                    is_shuffle = True
                    break
            # print is_shuffle
        return shapes

    def _gen_doc_shape(self, doc, pos=None):
        """
        Генерация фигуры текущего документа.
        """
        if pos is None:
            pos = (100, 100)
            
        doc_shape = dict(type='icDividedShape',
                         name=doc.getUUID(),
                         title=doc.getRequisiteValue('doc_name'),
                         text=doc.getRequisiteValue('description'),
                         pen='BLACK_PEN',
                         brush='WHITE_BRUSH',
                         size=(200, 150),
                         pos=pos)
        return doc_shape
        
    def _gen_line(self, src_doc_shape, dst_doc_shape):
        """
        Генерация линии, соединяющей 2 фигуры.
        """
        line= {'from': src_doc_shape['name'],
               'to': dst_doc_shape['name'],
               'pen': 'BLACK_PEN',
               'brush': 'BLACK_BRUSH',
               'arrow': 'ARROW_ARROW',
               'type': 'LineShape'}
        return line       
   
    def _get_doc_links_from(self, doc):
        """
        Получить дерево связей документа указывающих на него.
        """
        from_docs = doc.getRequisiteValue('scan_doc_from')
        if from_docs:
            result = list()
                    
            for from_doc in from_docs:
                new_doc = ic.metadata.THIS.mtd.scan_document.create()
                new_doc.load_obj(from_doc['link_from'])
                
                from_data_links = self.get_doc_links(new_doc)
                result.append(from_data_links)
            
            return result
        return None

    def _get_doc_links_to(self, doc):
        """
        Получить дерево связей документа указывающих на него.
        """
        # Сначала добавить сам объект
        result = doc.getRequisiteData()
        if CONTRAGENT_SPRAV:
            result['contragent'] = CONTRAGENT_SPRAV.Find(result.get('c_agent', None))
        result['doc_date_str'] = result['doc_date'].strftime(DATE_FMT) if result['doc_date'] else NONE_DATE_FMT
        result['obj_date_str'] = result['obj_date'].strftime(DATE_FMT) if result['obj_date'] else NONE_DATE_FMT
        result['__children__'] = list()
            
        to_docs = doc.getRequisiteValue('scan_doc_to')
        if to_docs:
            for to_doc in to_docs:
                new_doc = ic.metadata.THIS.mtd.scan_document.create()
                new_doc.load_obj(to_doc['link_to'])

                to_data_links = self._get_doc_links_to(new_doc) 
                result['__children__'].append(to_data_links)
                
        return result
        
    def get_doc_links(self, doc=None):
        """
        Дерево связей документа.
        """
        if doc is None:
            doc = self.get_object()

        from_docs = doc.getRequisiteValue('scan_doc_from')

        if from_docs:
            return self._get_doc_links_from(doc)
        else:
            return self._get_doc_links_to(doc)
        return dict()

    def view_scan_file(self, scan_filename=None):
        """
        Открыть на просмотр файл.
        @param scan_filename: Имя сканированного файла.
            Если не определено, то пытаемся взять из объекта текущего документа.
        """
        if scan_filename is None:
            scan_filename = self.get_object().getRequisiteValue('file_name')
            
        if not scan_filename:
            msg = u'Файл скана не определен'
            log.warning(msg)
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', msg)
            return
        if not os.path.exists(scan_filename):
            msg = u'Файл <%s> не найден для просмотра' % scan_filename
            log.warning(msg)
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', msg)
            return

        doc_file_ext = os.path.splitext(scan_filename)[1].lower()
        cmd = u''
        if doc_file_ext == '.pdf':
            cmd = u'evince %s&' % scan_filename
        elif doc_file_ext in ('.jpg', '.jpeg', '.tiff', '.bmp'):
            cmd = u'eog %s&' % scan_filename
        else:
            log.warning(u'Не поддерживаемый тип файла <%s>' % doc_file_ext)
        if cmd:
            log.info(u'Выполнение комманды <%s>' % cmd)
            os.system(cmd)
        
    def clear_not_exist_links(self, doc=None):
        """
        Удаление из документа ссылок на не существующие документы.
        Функция выполняется не рекурсивно только в рамках указанного документа.
        """
        if doc is None:
            doc = self.get_object()
        
        from_docs = doc.getRequisiteValue('scan_doc_from')
        to_docs = doc.getRequisiteValue('scan_doc_to')
        
        do_save = False
        if from_docs:
            do_set = False
            for i in range(len(from_docs)-1, -1, -1):
                from_doc = from_docs[i]
                if not doc.is_obj(from_doc['link_from']):
                    log.error(u'Не существующая ссылка от <%s>' % from_doc)
                    del from_docs[i]
                    do_set = True
                    do_save = True
                elif from_doc['link_from'] in [link['link_from'] for link in from_docs[i+1:]]:
                    # Ранее уже зарегисрированный UUID
                    log.error(u'Уже зарегистрированная ссылка от <%s>' % from_doc)
                    del from_docs[i]
                    do_set = True
                    do_save = True
                else:
                    log.debug(u'Ссылка существует от <%s>' % from_doc)

            if do_set:
                doc.setRequisiteValue('scan_doc_from', from_docs)
                
        if to_docs:
            do_set = False
            for i in range(len(to_docs)-1, -1, -1):
                to_doc = to_docs[i]
                if not doc.is_obj(to_doc['link_to']):
                    log.error(u'Не существующая ссылка на <%s>' % to_doc)
                    del to_docs[i]
                    do_set = True
                    do_save = True
                elif to_doc['link_to'] in [link['link_to'] for link in to_docs[i+1:]]:
                    # Ранее уже зарегисрированный UUID
                    log.error(u'Уже зарегистрированная ссылка на <%s>' % to_doc)
                    del to_docs[i]
                    do_set = True
                    do_save = True
                else:
                    log.debug(u'Ссылка существует на <%s>' % to_doc)
                    
            if do_set:
                doc.setRequisiteValue('scan_doc_to', to_docs)
        if do_save:
            ask_ok = ic_dlg.icAskBox(u'ВНИМАНИЕ!', 
                                     u'Найдены и удалены не существующие ссылки документа. Произвести сохранение изменений?')
            if ask_ok:
                doc.update_obj(scan_doc_from=from_docs, scan_doc_to=to_docs)
            return True
        return False
                
    def onShapeDblClick(self, selected_shape):
        """
        Обработчик двойного клика на фигуре схемы.
        """
        doc = ic.metadata.THIS.mtd.scan_document.create()
        doc.load_obj(selected_shape.id)
        doc_filename = doc.getRequisiteValue('file_name')
        
        if not os.path.exists(doc_filename):
            log.warning(u'Файл <%s> не найден для просмотра' % doc_filename)
            return
                        
        doc_file_ext = os.path.splitext(doc_filename)[1].lower()
        cmd = u''
        if doc_file_ext == '.pdf':
            cmd = u'evince %s&' % doc_filename
        elif doc_file_ext in ('.jpg', '.jpeg', '.tiff', '.bmp'):
            cmd = u'eog %s&' % doc_filename
        else:
            log.warning(u'Не поддерживаемый тип файла <%s>' % doc_file_ext)
        if cmd:
            os.system(cmd)
        
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK

manager_class = icScanDocumentManager
