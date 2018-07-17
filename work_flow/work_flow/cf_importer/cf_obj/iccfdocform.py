#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс элемента формы документа конфигурации 1с.
"""

import os
import os.path
import copy

from . import iccfresource
from . import iccfobject

from ic.utils import util1c
from ic.log import log

try:
    from work_flow.cf_importer import types1c
except:
    import types1c

__version__ = (0, 0, 0, 2)

# Шаблоны
CTRL_FORM_REQUISITE_TEMPLATE = [9, [2], 0,
                                'ДеревоКолонки', [1, 1, ['ru', 'Дерево колонки']],
                                ['Pattern', ['#', 'e603c0f2-92fb-4d47-8f38-a44a381cf235']],
                                [0, [0, ['B', 1], 0]], [0, [0, ['B', 1], 0]],
                                [0, 0], [0, 0], 0, 0, 0, 0, [0, 0], [0, 0]]

STD_FORM_REQUISITE_TEMPLATE = [[3], 0, 1, 'Реквизит',
                               ['Pattern', ['#', 'e603c0f2-92fb-4d47-8f38-a44a381cf235']]]

CTRL_BEFORE_ADD_START_EVENT_TEMPLATE = [1, '2391e7b8-7235-45d7-ab7e-6ff3dc086396', 'СписокПередНачаломДобавления']

STD_BEFORE_ADD_START_EVENT_TEMPLATE = [40, 'e1692cc2-605b-4535-84dd-28440238746c',
                                       [3, 'ДокументСписокПередНачаломДобавления',
                                        [1, 'ДокументСписокПередНачаломДобавления',
                                         [1, 1, ['ru', 'Документ список перед началом добавления']],
                                         [1, 1, ['ru', 'Документ список перед началом добавления']],
                                         [1, 1, ['ru', 'Документ список перед началом добавления']],
                                         [3, 0, [0], '', -1, -1, 1, 0], [0, 0, 0]]]]


class icCFDocForm(iccfobject.icCFObject):
    """
    Класс элемента формы документа конфигурации 1с.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        iccfobject.icCFObject.__init__(self, *args, **kwargs)
        
        self.img_filename_requisite = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                   'img', 'application-form.png')

    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_cfg_filename_requisite = os.path.join(os.path.abspath(self.cf_dir), 'metadata', self.uid)
        if not os.path.exists(cf_cfg_filename_requisite):
            cf_cfg_filename_requisite = os.path.join(os.path.abspath(self.cf_dir), self.uid)
        if not os.path.exists(cf_cfg_filename_requisite):
            log.warning(u'Не найден файл <%s>' % cf_cfg_filename_requisite)
            return

        cf_cfg_res = iccfresource.icCFResource(cf_cfg_filename_requisite)
        cf_cfg_res.loadData()
        
        self.name = cf_cfg_res.data[1][1][1][2]
        
        self.description = ''
        try:
            self.description = cf_cfg_res.data[1][1][1][3][2]
        except IndexError:
            pass
        
    def getResFileName(self):
        """
        Имя файла ресурса формы.
        """
        res_filename_requisite = os.path.join(self.getCFDir(), self.uid+'.0')
        if not os.path.exists(res_filename_requisite) or not os.path.isfile(res_filename_requisite):
            res_filename_requisite = os.path.join(res_filename_requisite, 'form')
            if not os.path.exists(res_filename_requisite) or not os.path.isfile(res_filename_requisite):
                return None            
        return res_filename_requisite
        
    def addInFormModule(self, txt):
        """
        Добавить в модуль формы текст.
        @param txt: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        res_filename_requisite = os.path.join(self.getCFDir(), self.uid+'.0')
        if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
            return self._addInFormModuleCtrl(res_filename_requisite, txt)
        else:
            mod_filename_requisite = os.path.join(res_filename_requisite, 'module')
            if os.path.exists(mod_filename_requisite) and os.path.isfile(mod_filename_requisite):
                return self._addInFormModuleStd(mod_filename_requisite, txt)
        log.warning(u'ERROR! Form %s (UID: %s) module file not found!' % (self.name, self.uid))
        return None
        
    def _addInFormModuleStd(self, mod_filename_requisite,txt):
        """
        Добавить в модуль формы текст. Обычная форма.
        @param mod_filename_requisite: Имя файла модуля формы.
        @param txt: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        prg_txt = util1c.encodeText(txt, 'unicode', 'utf-8')
        
        f = None
        try:
            f = open(mod_filename_requisite, 'r')
            txt = f.read()
            f.close()
            f = None
            if prg_txt not in txt:
                try:
                    f = open(mod_filename_requisite, 'a')
                    f.write(prg_txt)
                    f.close()
                except:
                    if f:
                        f.close()
                        f = None
                    raise
            return True
        except:
            if f:
                f.close()
                f = None
            raise
        return False
        
    def _addInFormModuleCtrl(self, res_filename_requisite, txt):
        """
        Добавить в модуль формы текст. Управляемая форма.
        @param res_filename_requisite: Имя файла ресурса формы.
        @param txt: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        res = iccfresource.icCFResource(res_filename_requisite)
        res.loadData()

        txt = util1c.encodeText(txt, 'unicode', 'utf-8')
        if txt not in res.data[2]:
            prg_txt = res.data[2] + txt
            res.data[2] = prg_txt
        
        return res.saveData()
    
    def delInFormModule(self, txt):
        """
        Удалить из модуля формы текст.
        @param txt: Удаляемый текст.
        @return: True - удаление прошло успешно, False - удаления не произошло.
        """
        pass
    
    def replaceInFormModule(self, srctxt, dsttxt):
        """
        Заменить текст в модуле формы.
        @param srctxt: Заменяемый текст.
        @param dsttxt: Заменяющий текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        pass
    
    def updateInFormModule(self, txt, *args, **kwargs):
        """
        Заменить текст всех процедур и функций.
        @param txt: Заменяемый текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        res_filename_requisite = os.path.join(self.getCFDir(), self.uid+'.0')
        if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
            pass
        else:
            mod_filename_requisite = os.path.join(res_filename_requisite, 'module')
            if os.path.exists(mod_filename_requisite) and os.path.isfile(mod_filename_requisite):
                return self._updateInFormModuleStd(mod_filename_requisite, txt, *args, **kwargs)
        log.warning(u'ERROR! Form %s (UID: %s) resource file not found!' % (self.name, self.uid))
        return None    

    def _splitModuleProcBlock(self, txt):
        """
        Разбить текст модуля на блоки процедур и функций.
        @param txt: Текст модуля.
        """
        txt_lines = txt.split('\n')
        
        blocks = []
        cur_block = [None, '']
        end_block = False
        first_proc = False
        for line in txt_lines:
            if ('Процедура' in line) or ('Функция' in line):
                new_block = [line.strip(), line+'\n']
                if not first_proc:
                    first_proc = True
                end_block = True               
            elif ('КонецПроцедуры' in line) or ('КонецФункции' in line):
                cur_block[1] += line+'\n'
                new_block = [None, '']
                end_block = True
            else:
                cur_block[1] += line + '\n'

            if end_block:
                blocks.append(cur_block)
                cur_block = new_block
                end_block = False
                
        blocks.append(cur_block)
        
        # Если первый блок пустой, то удалить его
        if blocks[0] == [None, '']:
            del blocks[0]
            
        return blocks
    
    def _appendInModuleBlocks(self, module_blocks, prg_block):
        """
        Добавить блок процедуры/функции в блоки модуля.
        @param module_blocks:Список блоков модуля.
        @param prg_block: Добавляемый блок.
        @return: Обновленный module_blocks
        """
        max_i = 0
        for i, block in enumerate(module_blocks):
            if ('КонецПроцедуры' in block[1]) or ('КонецФункции' in block[1]):
               max_i = max(i, max_i)
        module_blocks.insert(max_i+1, prg_block)
        return module_blocks
    
    def _updateInFormModuleStd(self, mod_filename_requisite, txt, *args, **kwargs):
        """
        Заменить текст всех процедур и функций.
        @param mod_filename_requisite: Имя файла модуля формы.
        @param txt: Заменяемый текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        txt = util1c.encodeText(txt, 'unicode', 'utf-8')
        
        f = None
        try:
            f = open(mod_filename_requisite, 'r')
            mod_txt = f.read()
            f.close()
            f = None
        except:
            if f:
                f.close()
                f = None
            raise
        # Обновить блоки процедур/функций
        mod_blocks = self._splitModuleProcBlock(mod_txt)
        update_blocks = self._splitModuleProcBlock(txt)
        for update_block in update_blocks:
            if update_block[0]:
                is_add = True
                for i, mod_block in enumerate(mod_blocks):
                    if update_block[0] == mod_block[0]:
                        # Заменить блок
                        mod_blocks[i] = update_block
                        is_add = False
                        break
                # Если такой процедуры нет в тексте модуля, то добавить ее
                if is_add:
                    mod_blocks = self._appendInModuleBlocks(mod_blocks, update_block)

        # Собрать текст модуля из обновленных блоков
        mod_txt = ''
        for mod_block in mod_blocks:
            mod_txt += mod_block[1]+'\n'
        mod_txt = mod_txt.replace('\r\n', '\n').replace('\n', '\r\n')
        try:
            f = open(mod_filename_requisite, 'w')
            f.write(mod_txt)
            f.close()
            f = None
        except:
            if f:
                f.close()
                f = None
            raise
        return True
        
    def addFormRequisite(self, name_requisite, type_requisite, *args, **kwargs):
        """
        Добавить реквизит формы. Обычная форма.
        @param name_requisite: Имя реквизита формы.
        @param type_requisite: Тип реквизита формы.
        """
        res_filename_requisite = os.path.join(self.getCFDir(), self.uid+'.0')
        if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
            return self._addFormRequisiteCtrl(res_filename_requisite, name_requisite, type_requisite, *args, **kwargs)
        else:
            res_filename_requisite = os.path.join(res_filename_requisite, 'form')
            if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
                return self._addFormRequisiteStd(res_filename_requisite, name_requisite, type_requisite, *args, **kwargs)
        log.warning(u'ERROR! Form %s (UID: %s) resource file not found!' % (self.name, self.uid))
        return None
        
    def _addFormRequisiteStd(self, res_filename_requisite, name_requisite, type_requisite, *args, **kwargs):
        """
        Добавить реквизит формы. Обычная форма.
        @param res_filename_requisite: Имя файла ресурса формы.
        @param name_requisite: Имя реквизита формы.
        @param type_requisite: Тип реквизита формы.
        """
        res = iccfresource.icCFResource(res_filename_requisite)
        res.loadData()
        
        requisite_template = copy.deepcopy(STD_FORM_REQUISITE_TEMPLATE)
        requisite_template[3] = name_requisite
        typ = types1c.types[type_requisite]
        requisite_template[4][1] = typ
        prev_idx = res.data[2][2][-1][0][0] 
        requisite_template[0][0] = prev_idx+1
        if res.data[-2:] == [1, 1] and res.data[0] == 27:
            requisite_template.insert(1, 0)
        
        res.data[2][2].append(requisite_template)
        
        # Увеличить счетчик реквизитов формы
        res.data[2][2][0] += 1
        
        return res.saveData()
        
    def _addFormRequisiteCtrl(self, res_filename_requisite, name_requisite, type_requisite, *args, **kwargs):
        """
        Добавить реквизит формы. Управляемая форма.
        @param res_filename_requisite: Имя файла ресурса формы.
        @param name_requisite: Имя реквизита формы.
        @param type_requisite: Тип реквизита формы.
        """
        res = iccfresource.icCFResource(res_filename_requisite)
        res.loadData()
        
        requisite_template = copy.deepcopy(CTRL_FORM_REQUISITE_TEMPLATE)
        requisite_template[3] = name_requisite
        description = ''
        if 'description' in kwargs:
            description = kwargs['description']
        requisite_template[4][2][1] = description
        typ = types1c.types[type_requisite]
        requisite_template[5][1] = typ 
        
        res.data[3] = res.data[3][:-3] + [requisite_template] + res.data[3][-3:]
        
        # Увеличить счетчик реквизитов формы
        res.data[3][1] += 1
        
        return res.saveData()
    
    def delFormRequisite(self, name_requisite):
        """
        Удалить реквизит формы по имени.
        @param name_requisite: Имя реквизита формы.
        """
        pass

    def _findObjResIdx(self, res_data, obj_name):
        """
        Найти индекс ресурса объекта в ресурсе формы по его имени.
        """
        idx = util1c.ValueIndexPath(res_data, obj_name)
        if idx:
            return idx[:-1]
        return None
        
    def addFormObjEvent(self, name_requisite, value, *args, **kwargs):
        """
        Добавить событие в объект формы.
        @param name_requisite: Имя объекта формы и события в формате
            <Имя объекта>.<Имя события>
        @param value: Значение которое необходимо прописать в событии.
        """
        res_filename_requisite = os.path.join(self.getCFDir(), self.uid+'.0')
        if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
            log.debug(u'CTRL FORM! %s' % res_filename_requisite)
        else:
            res_filename_requisite = os.path.join(res_filename_requisite, 'form')
            if os.path.exists(res_filename_requisite) and os.path.isfile(res_filename_requisite):
                return self._addFormObjEventStd(res_filename_requisite, name_requisite, value, *args, **kwargs)
        log.warning(u'ERROR! Form %s (UID: %s) resource file not found!' % (self.name, self.uid))
        return None

    def _addFormObjEventCtrl(self, res_filename_requisite, name_requisite, value):
        """
        Добавить событие в объект формы. Управляемая форма.
        @param res_filename_requisite: Имя файла ресурса формы.
        @param name_requisite: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        @param value: Значение которое необходимо прописать в событии.
        """
        res = iccfresource.icCFResource(res_filename_requisite)
        res.loadData()

        name_requisites = name_requisite.split('.')
        if len(name_requisites) != 2:
            log.warning(u'Object name_requisite and event name_requisite <%s> not define!' % name_requisites)
            return

        obj_name_requisite = util1c.encodeText(name_requisites[0], 'unicode', 'utf-8')
        evt_name_requisite = util1c.encodeText(name_requisites[1], 'unicode', 'utf-8')        
        obj_idx = self._findObjResIdx(res.data, obj_name_requisite)
        
        if evt_name_requisite == 'ПередНачаломДобавления':
            if obj_idx:
                evt_idx = (1, 27, 73)
                evt_res = res.getByIdxList(evt_idx)
                if evt_res == [0]:
                    # Если событие не определено
                    evt_template = copy.deepcopy(CTRL_BEFORE_ADD_START_EVENT_TEMPLATE)
                    evt_template[-1] = util1c.encodeText(value, 'unicode', 'utf-8')
                    res.data[1][27][73] = evt_template
        else:
            log.warning(u'Event \'%s\' not support' % evt_name_requisite)
            return
        
        return res.saveData()

    _evtID = {'ПередНачаломДобавления': 40,
              'ПриПовторномОткрытии': 70008,
              'ПередОткрытием': 70000,
              'ПриОткрытии': 70001,
              }
    
    def _createFormObjEventResStd(self, event_name, value, id):
        """
        """
        evt_template = copy.deepcopy(STD_BEFORE_ADD_START_EVENT_TEMPLATE)
        evt_template[0] = id
        evt_template[2][1] = event_name
        evt_template[2][2][1] = value
        description = util1c.splitName1CWord(event_name)
        evt_template[2][2][2][2][1] = description
        evt_template[2][2][3][2][1] = description
        evt_template[2][2][4][2][1] = description
        return evt_template
        
    _SupportEventNames = ('ПередНачаломДобавления', 'ПередОткрытием')

    def _addFormObjEventStd(self, res_filename_requisite, name_requisite, value):
        """
        Добавить событие в объект формы. Обычная форма.
        @param res_filename_requisite: Имя файла ресурса формы.
        @param name_requisite: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        @param value: Значение которое необходимо прописать в событии.
        """
        res = iccfresource.icCFResource(res_filename_requisite)
        res.loadData()

        name_requisites = name_requisite.split('.')
        if len(name_requisites) != 2:
            log.warning(u'Object name_requisite and event name_requisite <%s> not define!' % name_requisites)
            return

        obj_name_requisite = util1c.encodeText(name_requisites[0], 'unicode', 'utf-8')
        evt_name_requisite = util1c.encodeText(name_requisites[1], 'unicode', 'utf-8')
        value = util1c.encodeText(value, 'unicode', 'utf-8')
        
        if evt_name_requisite in self._SupportEventNames:
            if obj_name_requisite:
                # Если имя объекта указано, то это объект формы
                for obj_res in res.data[1][2][2][1:]:
                    if obj_res[4][1] == obj_name_requisite:
                        full_evt_name_requisite = obj_name_requisite + evt_name_requisite
                        res_evt_name_requisites = [evt[2][1] for evt in obj_res[2][4][1:]]
                        if full_evt_name_requisite not in res_evt_name_requisites:
                            evt_template = self._createFormObjEventResStd(full_evt_name_requisite,
                                                                          value, self._evtID[evt_name_requisite])
                            obj_res[2][4].append(evt_template)
                            # Увеличить счетчик событий формы
                            obj_res[2][4][0] += 1
                        break
            else:
                res_evt_name_requisites = [evt[2][1] for evt in res.data[4][1:]]
                if evt_name_requisite not in res_evt_name_requisites:
                    # Если имя объекта не указано, то это сама форма
                    evt_template = self._createFormObjEventResStd(evt_name_requisite, value,
                                                                  self._evtID[evt_name_requisite])
                    res.data[4].append(evt_template)
                    # Увеличить счетчик событий формы
                    res.data[4][0] += 1
        else:
            log.warning(u'Event \'%s\' not support' % evt_name_requisite)
            return
        
        return res.saveData()
        
    def delFormObjEvent(self, name_requisite):
        """
        Удалить событие из объекта формы.
        @param name_requisite: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        """
        pass
