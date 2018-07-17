#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Абстрактные классы объектов генерирующих ресурсы форм.
Генерация производится по спецификации объекта и специфкациям
атрибутов/реквизитов объекта.
"""

# Imports
import os
import os.path
import wx

from ic.utils import ic_mode

from ic import io_prnt
from ic.utils import ic_str
from ic.utils import util
from ic.utils import ic_file

from ic.engine import ic_user

from . import frm_gen_templates

# Version
__version__ = (0, 0, 0, 3)

# Classes
# Размеры генерируемых диалоговых окон по умолчанию
DEFAULT_DIALOG_WIDTH = 700
DEFAULT_DIALOG_HEIGHT = 500
DEFAULT_DIALOG_SIZE = (DEFAULT_DIALOG_WIDTH, DEFAULT_DIALOG_HEIGHT)


class icObjFormGenerator:
    """
    Базовый класс генератора форм компонента.
        Реализует внутри себя механизм генерации спецификации форм отображения/редактирования.
    """

    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        pass

    def isAutoGroup(self):
        """
        Автоматически создавать компоненты группировки в формах?
        """
        return False

    def getChildrenRequisites(self):
        """
        Все реквизиты объекта в виде списка.
        """
        return []
        
    def _genChoiceFormName(self):
        """
        Генерация имени формы выбора.
        """
        return str(self.name).lower()+'_choice'

    def _genChoicePanelName(self):
        """
        Генерация имени панели выбора.
        """
        return str(self.name).lower()+'_choice_panel'

    def getChoiceFormName(self):
        """
        Имя формы выбора.
        """
        frm_psp = self.getChoiceFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genChoiceFormName()

    def getChoicePanelName(self):
        """
        Имя панели выбора.
        Панель выбора может задаваться атрибутом <choice_form>.
        """
        frm_psp = self.getChoiceFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genChoicePanelName()

    def _genGridRes(self):
        """
        Генерация ресурса грида.
        """
        from ic.components import icgriddataset
        from ic.components import icgrid
        
        grid_spc = util.icSpcDefStruct(util.DeepCopy(icgriddataset.SPC_IC_GRID_DATASET), None)
        
        for requisite in self.getChildrenRequisites():
            grid_col_spc = util.icSpcDefStruct(util.DeepCopy(icgrid.SPC_IC_CELL), None)
            
            grid_spc['child'].append(grid_col_spc)
        return grid_spc

    def _genStdToolbarRes(self, FormName_=None, ResModuleFileName_=None,
                          isAddTool_=False, isDelTool_=False,
                          isViewTool_=False, isEditTool_=False):
        """
        Генерация стандартной панели инструментов для работы с объектами.
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @param isAddTool_: Можно вызывать добавление объекта из панели инструментов?
        @param isDelTool_: Можно вызывать удаление объекта из панели инструментов?
        @param isViewTool_: Можно вызывать просмотр объекта из панели инструментов?
        @param isEditTool_: Можно вызывать редактирование объекта из панели инструментов?
        @return: Возвращает ресурс сгенерированной панели инструментов.
        """
        from ic.components.custom import ictoolbar

        # Панель инструментов
        # Генерация ресурса панели инструментов поиска
        toolbar_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.ic_class_spc), None)
        toolbar_spc['name'] = 'ctrl_toolbar'
        toolbar_spc['image_list'] = (('icImageList', 'search_imglst', None, 'search_imglst.mtd', 'work_flow'),)
        toolbar_spc['flag'] = wx.EXPAND

        if isAddTool_:
            tool_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.SPC_IC_TB_TOOL), None)
            tool_spc['name'] = 'add_obj_tool'
            tool_spc['img_indx'] = 8
            tool_spc['shortHelpString'] = u'Добавить объект'
            tool_spc['onTool'] = 'GetManager(self).onAddObjTool(event)'
            toolbar_spc['child'].append(tool_spc)

        if isDelTool_:
            tool_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.SPC_IC_TB_TOOL), None)
            tool_spc['name'] = 'del_obj_tool'
            tool_spc['img_indx'] = 9
            tool_spc['shortHelpString'] = u'Удалить объект'
            tool_spc['onTool'] = 'GetManager(self).onDelObjTool(event)'
            toolbar_spc['child'].append(tool_spc)

        if isViewTool_ or isEditTool_:
            separator_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.SPC_IC_TB_SEPARATOR), None)
            separator_spc['name'] = 'separator1'
            toolbar_spc['child'].append(separator_spc)
        
        if isViewTool_:
            tool_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.SPC_IC_TB_TOOL), None)
            tool_spc['name'] = 'view_obj_tool'
            tool_spc['img_indx'] = 3
            tool_spc['shortHelpString'] = u'Показать выбранный объект'
            tool_spc['onTool'] = 'GetManager(self).onViewObjTool(event)'
            toolbar_spc['child'].append(tool_spc)
        
        if isEditTool_:
            tool_spc = util.icSpcDefStruct(util.DeepCopy(ictoolbar.SPC_IC_TB_TOOL), None)
            tool_spc['name'] = 'edit_obj_tool'
            tool_spc['img_indx'] = 4
            tool_spc['shortHelpString'] = u'Редактировать выбранный объект'
            tool_spc['onTool'] = 'GetManager(self).onEditObjTool(event)'
            toolbar_spc['child'].append(tool_spc)
        
        return toolbar_spc

    def _genStdTreeBrwsRes(self, FormName_, ResModuleFileName_):
        """
        Генерация стандартного просмотрщика деревянного представления объекта.
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.user import icsimpletreelistctrl
        
        # Дерево выбора
        tree_spc = util.icSpcDefStruct(util.DeepCopy(icsimpletreelistctrl.ic_class_spc), None)
        tree_spc['name'] = 'tree_object_ctrl'
        tree_spc['flag'] = wx.GROW | wx.EXPAND
        tree_spc['proportion'] = 1
        
        # Дополнить модуль ресурса обработчиками событий
        self._genResModule(ResModuleFileName_,
                           frm_gen_templates._stdTreeBrwsResModuleFmt)
        
        return tree_spc

    def _genResModule(self, ResModuleFileName_, Txt_):
        """
        Генерация модуля формы объекта по описанию объекта.
        @param ResModuleName_: Имя модуля генерируемой формы.
        @return: Возвращает True/False.
        """
        res_module = None
        try:
            res_module = open(ResModuleFileName_, 'at')
            res_module.write(Txt_)
            res_module.close()
            return True
        except:
            if res_module:
                res_module.close()
            if ic_mode.isDebugMode():
                io_prnt.outErr(u'Ошибка генерации файла модуля формы %s' % ResModuleFileName_)
            return None
    
    def _genChoicePanelRes(self, name=None):
        """
        Форма выбора объекта.
        Генерация панели выбора объекта по описанию объекта.
        @param name: Имя генерируемого ресурса.
        @return: Возвращает сгенерированный ресурс.
        """
        from ic.components import icwxpanel
        from ic.components.sizers import icboxsizer
        from STD.usercomponents import icfilterchoicectrl

        if name is None:
            name = self.getChoicePanelName()

        spc = util.icSpcDefStruct(util.DeepCopy(icwxpanel.SPC_IC_PANEL), None)
        spc['name'] = 'choice_panel'
        spc['res_module'] = name+'_frm.py'
        spc['title'] = u''+self._getTxtDescription()
        spc['onInit'] = 'GetManager(self).onInit(event)'

        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+spc['res_module'])
        if os.path.exists(res_module_file_name):
            os.remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+name+'.frm')
        txt = frm_gen_templates._choiceDlgResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                          form_file_name, res_module_file_name,
                                                          name+'_ChoicePanel', name+'_ChoicePanel')
        self._genResModule(res_module_file_name, txt)

        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.SPC_IC_BOXSIZER), None)
        box_sizer_spc['name'] = name+'_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        box_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        spc['child'].append(box_sizer_spc)

        # Панель инструментов
        toolbar_spc = self._genStdToolbarRes(name, res_module_file_name,
                                             True, True, True, True)

        box_sizer_spc['child'].append(toolbar_spc)

        # Компонент выбора фильтров
        filter_choice = util.icSpcDefStruct(util.DeepCopy(icfilterchoicectrl.ic_class_spc), None)
        filter_choice['name'] = 'filter_choice'
        filter_choice['flag'] = wx.GROW | wx.EXPAND
        filter_choice['save_filename'] = icfilterchoicectrl.DEFAULT_FILTER_SAVE_FILENAME
        filter_choice['get_env'] = '@return OBJ.getFilterEnv()'
        box_sizer_spc['child'].append(filter_choice)
        # Грид просмотра отфильтрованных объектов
        view_grid_spc = self._genStdViewGridRes(name)
        view_grid_spc['flag'] = wx.GROW | wx.EXPAND
        view_grid_spc['proportion'] = 1

        box_sizer_spc['child'].append(view_grid_spc)

        return spc

    def _genChoiceDialogRes(self, name=None):
        """
        Форма выбора объекта.
        Генерация формы выбора объекта по описанию объекта.
        @param name: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icdialog
        from ic.components.custom import icbutton
        from ic.components.sizers import icboxsizer
        from ic.components.custom import icsplitter
        from ic.components import icmulticolumnlist
        
        if name is None:
            name = self.getChoiceFormName()
        
        frm_spc = util.icSpcDefStruct(util.DeepCopy(icdialog.SPC_IC_DIALOG), None)
        frm_spc['name'] = 'choice_dlg'
        frm_spc['size'] = DEFAULT_DIALOG_SIZE
        frm_spc['style'] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        frm_spc['res_module'] = name+'_frm.py'
        frm_spc['title'] = u'Выбор: '+self._getTxtDescription()
        frm_spc['onInit'] = 'GetManager(self).onInit(event)'
        
        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if os.path.exists(res_module_file_name):
            os.remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+name+'.frm')
        txt = frm_gen_templates._choiceDlgResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                          form_file_name, res_module_file_name,
                                                          name+'_ChoiceForm', name+'_ChoiceForm')
        self._genResModule(res_module_file_name, txt)
        
        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.SPC_IC_BOXSIZER), None)
        box_sizer_spc['name'] = name+'_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)
        
        # Панель инструментов
        toolbar_spc = self._genStdToolbarRes(name, res_module_file_name)
        
        box_sizer_spc['child'].append(toolbar_spc)
        
        # Сплиттер
        splitter_spc = util.icSpcDefStruct(util.DeepCopy(icsplitter.ic_class_spc), None)
        splitter_spc['name'] = 'choice_splitter'
        splitter_spc['flag'] = wx.GROW | wx.EXPAND
        splitter_spc['proportion'] = 1
        splitter_spc['sash_pos'] = DEFAULT_DIALOG_HEIGHT/2
        box_sizer_spc['child'].append(splitter_spc)
        # Генерация ресурса стандартного дерева конструктора фильтра
        filter_list = util.icSpcDefStruct(util.DeepCopy(icmulticolumnlist.ic_class_spc), None)
        filter_list['name'] = 'filter_list'
        filter_list['fields'] = [u'Фильтр', u'Описание']
        splitter_spc['win1'] = filter_list
        # Грид просмотра отфильтрованных объектов
        view_grid_spc = self._genStdViewGridRes(name)
        splitter_spc['win2'] = view_grid_spc
        
        # Кнопки
        btn_box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.SPC_IC_BOXSIZER), None)
        btn_box_sizer_spc['name'] = name+'_sizer_btn'
        btn_box_sizer_spc['layout'] = 'horizontal'
        btn_box_sizer_spc['flag'] = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        btn_box_sizer_spc['border'] = 5
        btn_cancel_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_cancel_spc['name'] = 'cancel_button'
        btn_cancel_spc['label'] = u'Отмена'
        btn_cancel_spc['flag'] = wx.ALL
        btn_cancel_spc['border'] = 5
        btn_cancel_spc['mouseClick'] = 'GetManager(self).onCancelButton(event)'
        btn_box_sizer_spc['child'].append(btn_cancel_spc)
        
        btn_ok_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_ok_spc['name'] = 'ok_button'
        btn_ok_spc['label'] = u'OK'
        btn_ok_spc['flag'] = wx.ALL
        btn_ok_spc['border'] = 5
        btn_ok_spc['mouseClick'] = 'GetManager(self).onOkButton(event)'
        btn_box_sizer_spc['child'].append(btn_ok_spc)
        box_sizer_spc['child'].append(btn_box_sizer_spc)
        
        return frm_spc
        
    def createChoiceFormRes(self):
        """
        Создание, по описанию объекта, ресурса формы выбора.
        @return: Возвращает паспорт сгенерированной формы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()
    
        # Проверка на добавление нового ресурса
        frm_name = self.getChoiceFormName()
        # Если имя определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if frm_name and not prj_res_ctrl.isRes(frm_name, 'frm'):
            frm_res = self._genChoiceDialogRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name, 'frm', frm_res)
        
        frm_psp = (('Dialog', frm_name, None, frm_name+'.frm', None),)
        return frm_psp

    def createChoicePanelRes(self):
        """
        Создание, по описанию объекта, ресурса панели выбора.
        @return: Возвращает паспорт сгенерированной панели.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        panel_name = self.getChoicePanelName()
        # Если имя определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if panel_name and not prj_res_ctrl.isRes(panel_name, 'frm'):
            panel_res = self._genChoicePanelRes(panel_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(panel_name, 'frm', panel_res)

        panel_psp = (('Panel', panel_name, None, panel_name+'.frm', None),)
        return panel_psp

    # Форма инициализации объекта
    def createInitFormRes(self):
        """
        Создание, по описанию объекта, ресурса формы инициализации.
        @return: Возвращает паспорт сгенерированной формы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        frm_name = self.getInitFormName()
        # Если имя определено нет ресурса с таким именем, то запустить
        # создание ресурса
        if frm_name and not prj_res_ctrl.isRes(frm_name, 'frm'):
            frm_res = self._genInitDialogRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name, 'frm', frm_res)
            
        frm_psp = (('Dialog', 'init_dlg', None, frm_name+'.frm', None),)
        return frm_psp

    def createSearchFormRes(self):
        """
        Создание, по описанию объекта, ресурса формы поиска объекта.
        @return: Возвращает паспорт сгенерированной формы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        frm_name = self.getSearchFormName()
        # Если имя определено нет ресурса с таким именем, то запустить
        # создание ресурса
        if frm_name and not prj_res_ctrl.isRes(frm_name, 'frm'):
            frm_res = self._genSearchPanelRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name, 'frm', frm_res)

            frm_res = self._genSearchDialogRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name+'_dlg', 'frm', frm_res)
            
        frm_psp = (('Dialog', 'search_dlg', None, frm_name+'_dlg.frm', None),)
        return frm_psp
    
    def getInitFormName(self):
        """
        Имя формы инициализации/создания.
        """
        frm_psp = self.getInitFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genInitFormName()
        
    def getSearchFormName(self):
        """
        Имя формы поиска.
        """
        frm_psp = self.getSearchFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genSearchFormName()
        
    def _genInitFormName(self):
        """
        Генерация имени формы инициализации/создания.
        """
        return str(self.name).lower()+'_init'

    def _genSearchFormName(self):
        """
        Генерация имени формы поиска.
        """
        return str(self.name).lower()+'_search'
    
    def _getTxtDescription(self):
        """
        Описание объекта в текстовом представлении.
        """
        if type(self.description) in (str, unicode):
            return self.description
        return ''
        
    def _genInitDialogRes(self, FormName_=None):
        """
        Генерация ресурса формы инициализации/создания.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icdialog
        from ic.components.custom import icbutton
        from ic.components.sizers import icboxsizer
        
        if FormName_ is None:
            FormName_ = self.getInitFormName()
        
        frm_spc = util.icSpcDefStruct(util.DeepCopy(icdialog.ic_class_spc), None)
        frm_spc['name'] = 'init_dlg'
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['size'] = DEFAULT_DIALOG_SIZE
        frm_spc['style'] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        frm_spc['title'] = u'Создание: '+self._getTxtDescription()
        
        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._initResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                     form_file_name, res_module_file_name,
                                                     FormName_+'_InitForm', FormName_+'_InitForm')
        self._genResModule(res_module_file_name, txt)
        
        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.SPC_IC_BOXSIZER), None)
        box_sizer_spc['name'] = 'init_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)

        # Генерация ресурса стандартной панели инициализации
        edit_panel_spc = self._genStdInitPanelRes(FormName_)
        box_sizer_spc['child'].append(edit_panel_spc)
        
        btn_box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.SPC_IC_BOXSIZER), None)
        btn_box_sizer_spc['name'] = 'init_sizer_btn'
        btn_box_sizer_spc['layout'] = 'horizontal'
        btn_box_sizer_spc['flag'] = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        btn_box_sizer_spc['border'] = 5
        
        btn_cancel_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_cancel_spc['name'] = 'cancel_button'
        btn_cancel_spc['label'] = u'Отмена'
        btn_cancel_spc['flag'] = wx.ALL
        btn_cancel_spc['border'] = 5
        btn_cancel_spc['mouseClick'] = 'GetManager(self).onCancelButton(event)'
        btn_box_sizer_spc['child'].append(btn_cancel_spc)

        btn_ok_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_ok_spc['name'] = 'ok_button'
        btn_ok_spc['label'] = u'OK'
        btn_ok_spc['flag'] = wx.ALL
        btn_ok_spc['border'] = 5
        btn_ok_spc['mouseClick'] = 'GetManager(self).onOkButton(event)'
        
        btn_box_sizer_spc['child'].append(btn_ok_spc)
        
        box_sizer_spc['child'].append(btn_box_sizer_spc)
        
        return frm_spc
    
    def _genStdInitPanelRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартной панели инициализации. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        if self.isPageGroupInit():
            return self._genStdInitNotebookRes(FormName_, ResModuleFileName_)
        else: 
            return self._genStdInitScrolledwinRes(FormName_, ResModuleFileName_)

    def _genStdInitNotebookRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного нотебука инициализации
        с группировкой реквизитов по страницам. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.custom import icnotebook
        from ic.components.sizers import icgridbagsizer
        
        notebook_spc = util.icSpcDefStruct(util.DeepCopy(icnotebook.ic_class_spc), None)
        notebook_spc['name'] = 'init_notebook'
        notebook_spc['flag'] = wx.GROW | wx.EXPAND
        notebook_spc['proportion'] = 1
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isInit():
                # Определить страницу, если группировка происходит по страницам
                page_title = None
                sizer_spc = None
                if self.isPageGroupInit():
                    page_title = child_requisite.getGroupTitle()
                    # Добавление страницы
                    is_title = bool([title for title in notebook_spc['titles'] if title == page_title])
                    if not is_title:
                        page_spc = self._genStdNotebookPageRes(len(notebook_spc['titles']),
                                                               page_title, FormName_, ResModuleFileName_)
                        notebook_spc['child'].append(page_spc)
                        notebook_spc['titles'].append(page_title)
                    else:
                        page_spc = notebook_spc['child'][notebook_spc['titles'].index(page_title)]
                    sizer_spc = page_spc['child'][0]
                
                if sizer_spc:
                    # Вычисление максимальной позиции y нового контрола на текущей странице
                    max_row = 0
                    if 'child' in sizer_spc and sizer_spc['child']:
                        positions = [pos[0] for pos in [ctrl['position'] for ctrl in sizer_spc['child']]]
                        if positions:
                            max_row = max(positions)
                    
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (max_row+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (max_row+1, 2)

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (max_row+1, 1)
                        box_spc['span'] = (1, 2)
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outLog(u'Ошибка определения типа реквизита %s' % child_requisite.name)
                    sizer_spc['flexCols'] = [2]
        
        return notebook_spc
    
    def _genStdInitScrolledwinRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного скроллируемого окна 
        инициализации без группировки реквизитов. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components import icscrolledpanel
        from ic.components.sizers import icgridbagsizer

        scrolledwin_spc = util.icSpcDefStruct(util.DeepCopy(icscrolledpanel.ic_class_spc), None)
        scrolledwin_spc['name'] = 'init_scrolledwin'
        scrolledwin_spc['flag'] = wx.GROW | wx.EXPAND
        scrolledwin_spc['style'] = wx.TAB_TRAVERSAL
        scrolledwin_spc['proportion'] = 1
        
        win_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icgridbagsizer.ic_class_spc), None)
        win_sizer_spc['name'] = 'win_sizer'
        win_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        win_sizer_spc['vgap'] = 5
        win_sizer_spc['flexCols'] = [2]
        win_sizer_spc['proportion'] = 1
        scrolledwin_spc['child'].append(win_sizer_spc)
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isInit():
                sizer_spc = win_sizer_spc
                if sizer_spc:    
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (i+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (i+1, 2)

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (i+1, 1)
                        box_spc['span'] = (1, 2)
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outWarning(u'Ошибка определения типа реквизита <%s>' % child_requisite.name)
                    sizer_spc['flexCols'] = [2]

        return scrolledwin_spc
        
    # Форма поиска объекта
    def _genSearchDialogRes(self, FormName_=None):
        """
        Генерация ресурса диалоговой формы поиска объекта
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icdialog
        from ic.components.sizers import icboxsizer
        from ic.components import icobjectlink
        
        if FormName_ is None:
            FormName_ = self.getSearchFormName()+'_dlg'

        frm_spc = util.icSpcDefStruct(util.DeepCopy(icdialog.ic_class_spc), None)
        frm_spc['name'] = 'search_dlg'
        frm_spc['size'] = DEFAULT_DIALOG_SIZE
        frm_spc['style'] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['title'] = u'Поиск: '+self._getTxtDescription()

        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._searchDlgResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                          form_file_name, res_module_file_name,
                                                          FormName_+'_SearchDialog', FormName_+'_SearchDialog')
        self._genResModule(res_module_file_name, txt)

        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'search_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)
        
        # Панель в диалог добавляется по ссылке
        search_panel_spc = util.icSpcDefStruct(util.DeepCopy(icobjectlink.ic_class_spc), None)
        search_panel_spc['name'] = 'search_panel_link'
        search_panel_spc['flag'] = wx.GROW | wx.EXPAND
        search_panel_spc['proportion'] = 1
        search_panel_spc['object'] = ((None, None, None, self.getSearchFormName()+'.frm', None),)
        box_sizer_spc['child'].append(search_panel_spc)

        button_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        button_sizer_spc['name'] = 'button_sizer_h'
        button_sizer_spc['layout'] = 'horizontal'
        box_sizer_spc['child'].append(button_sizer_spc)
        
        return frm_spc
        
    def _genSearchPanelRes(self, FormName_=None):
        """
        Генерация ресурса формы/панели поиска.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icwxpanel
        from ic.components.sizers import icboxsizer
        
        if FormName_ is None:
            FormName_ = self.getSearchFormName()
        
        frm_spc = util.icSpcDefStruct(util.DeepCopy(icwxpanel.ic_class_spc), None)
        frm_spc['name'] = 'search_panel'
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['flag'] = wx.GROW | wx.EXPAND
        frm_spc['style'] = wx.TAB_TRAVERSAL
        frm_spc['description'] = u'Поиск: '+self._getTxtDescription()
        
        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._searchResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                       form_file_name, res_module_file_name,
                                                       FormName_+'_SearchPanel', FormName_+'_SearchPanel')
        self._genResModule(res_module_file_name, txt)
        
        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'search_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)

        # Генерация ресурса панели инструментов поиска
        toolbar_spc = self._getStdToolbarRes()
        
        box_sizer_spc['child'].append(toolbar_spc)
        
        # Генерация ресурса стандартной панели поиска
        splitter_spc = self._genStdSearchPanelRes(FormName_)
        box_sizer_spc['child'].append(splitter_spc)
        
        return frm_spc

    def _genStdSearchPanelRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартной панели инициализации. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.custom import icsplitter
        
        splitter_spc = util.icSpcDefStruct(util.DeepCopy(icsplitter.ic_class_spc), None)
        splitter_spc['name'] = 'search_splitter'
        splitter_spc['flag'] = wx.GROW | wx.EXPAND
        splitter_spc['proportion'] = 1
        splitter_spc['layout'] = 'horizontal'
        
        # Генерация
        if self.isPageGroupSearch():
            search_panel_spc = self._genStdSearchNotebookRes(FormName_, ResModuleFileName_)
        else: 
            search_panel_spc = self._genStdSearchScrolledwinRes(FormName_, ResModuleFileName_)
            
        splitter_spc['win1'] = search_panel_spc
        
        # Генерация грида найденных объектов
        search_grid_spc = self._genStdViewGridRes(FormName_, ResModuleFileName_)
        splitter_spc['win2'] = search_grid_spc

        return splitter_spc
        
    def _genStdSearchNotebookRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного нотебука
        с группировкой реквизитов по страницам. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.custom import icnotebook
        from ic.components.sizers import icgridbagsizer
        
        notebook_spc = util.icSpcDefStruct(util.DeepCopy(icnotebook.ic_class_spc), None)
        notebook_spc['name'] = 'search_notebook'
        notebook_spc['flag'] = wx.GROW | wx.EXPAND
        notebook_spc['proportion'] = 1
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isSearch():
                # Определить страницу, если группировка происходит по страницам
                page_title = None
                sizer_spc = None
                if self.isPageGroupSearch():
                    page_title = child_requisite.getGroupTitle()
                    # Добавление страницы
                    is_title = bool([title for title in notebook_spc['titles'] if title == page_title])
                    if not is_title:
                        page_spc = self._genStdNotebookPageRes(len(notebook_spc['titles']),
                                                               page_title, FormName_, ResModuleFileName_)
                        notebook_spc['child'].append(page_spc)
                        notebook_spc['titles'].append(page_title)
                    else:
                        page_spc = notebook_spc['child'][notebook_spc['titles'].index(page_title)]
                    sizer_spc = page_spc['child'][0]
                
                if sizer_spc:
                    # Вычисление максимальной позиции y нового контрола на текущей странице
                    max_row = 0
                    if 'child' in sizer_spc and sizer_spc['child']:
                        positions = [pos[0] for pos in [ctrl['position'] for ctrl in sizer_spc['child']]]
                        if positions:
                            max_row = max(positions)
                        
                    # Надпись
                    label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                    label_spc['position'] = (max_row+1, 1)
                    # Редактор
                    editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                    editor_spc['position'] = (max_row+1, 2)

                    sizer_spc['child'].append(label_spc)
                    sizer_spc['child'].append(editor_spc)
        
        return notebook_spc
    
    def _genStdNotebookPageRes(self, PageIdx_, PageTitle_, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса страницы стандартного нотебука
        с группировкой реквизитов по страницам. 
        @param PageIdx_: Индекс страницы.
        @param PageTitle_: Надпись/заголовок страницы.
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components import icscrolledpanel
        from ic.components.sizers import icgridbagsizer

        page_spc = util.icSpcDefStruct(util.DeepCopy(icscrolledpanel.ic_class_spc), None)
        page_spc['name'] = 'page_'+str(PageIdx_)
        page_spc['flag'] = wx.GROW | wx.EXPAND
        page_spc['style'] = wx.TAB_TRAVERSAL
        page_spc['proportion'] = 1

        page_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icgridbagsizer.ic_class_spc), None)
        page_sizer_spc['name'] = 'page_sizer_'+str(PageIdx_)
        page_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        page_sizer_spc['proportion'] = 1
        page_sizer_spc['border'] = 5
        page_sizer_spc['vgap'] = 5
        page_sizer_spc['flexCols'] = [2]
        page_spc['child'].append(page_sizer_spc)
        
        return page_spc
    
    def _genStdSearchScrolledwinRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного скроллируемого окна 
        поиска без группировки реквизитов. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components import icscrolledpanel
        from ic.components.sizers import icgridbagsizer

        scrolledwin_spc = util.icSpcDefStruct(util.DeepCopy(icscrolledpanel.ic_class_spc), None)
        scrolledwin_spc['name'] = 'search_scrolledwin'
        scrolledwin_spc['flag'] = wx.GROW | wx.EXPAND
        scrolledwin_spc['style'] = wx.TAB_TRAVERSAL
        scrolledwin_spc['proportion'] = 1
        
        win_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icgridbagsizer.ic_class_spc), None)
        win_sizer_spc['name'] = 'win_sizer'
        wiin_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        win_sizer_spc['proportion'] = 1
        win_sizer_spc['vgap'] = 5
        win_sizer_spc['flexCols'] = [2]
        scrolledwin_spc['child'].append(win_sizer_spc)
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isSearch():
                sizer_spc = win_sizer_spc
                if sizer_spc:    
                    # Надпись
                    label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                    label_spc['position'] = (i+1, 1)
                    # Редактор
                    editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                    editor_spc['position'] = (i+1, 2)

                    sizer_spc['child'].append(label_spc)
                    sizer_spc['child'].append(editor_spc)
        
        return scrolledwin_spc
    
    def _genStdViewGridRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного грида 
        предварительного просмотра объекта. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.user import icsimpleobjlistview
        from ic.components.user import icsimplegrplistview
        from ic.components import icgrid

        if self.isAutoGroup():
            grid_spc = util.icSpcDefStruct(util.DeepCopy(icsimplegrplistview.ic_class_spc), None)
        else:
            grid_spc = util.icSpcDefStruct(util.DeepCopy(icsimpleobjlistview.ic_class_spc), None)
        grid_spc['name'] = 'view_obj_grid'
        grid_spc['data_src'] = tuple(self.GetPassport())

        # Заполнение колонок
        requisites = self.getChildrenRequisites()
        if not requisites:
            io_prnt.outWarning(u'Генерация грида объекта. Не определены реквизиты объекта <%s>' % self.__class__.__name__)
        for i, child_requisite in enumerate(requisites):
            if child_requisite._isIDAttr():
                column_spc = util.icSpcDefStruct(util.DeepCopy(icgrid.SPC_IC_CELL), None)
                column_spc['name'] = child_requisite.getFieldName()
                column_spc['label'] = child_requisite.getLabel()
                column_spc['width'] = child_requisite._getDefaultWidth()
                
                grid_spc['child'].append(column_spc)
        return grid_spc
    
    def _genEditDialogRes(self, FormName_=None):
        """
        Форма редактирования объекта.
        Генерация ресурса формы редактирвоания.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icdialog
        from ic.components.sizers import icboxsizer
        from ic.components import icobjectlink
        from ic.components.custom import icbutton
        
        if FormName_ is None:
            FormName_ = self.getEditFormName()+'_dlg'

        frm_spc = util.icSpcDefStruct(util.DeepCopy(icdialog.ic_class_spc), None)
        frm_spc['name'] = 'edit_dlg'
        frm_spc['size'] = DEFAULT_DIALOG_SIZE
        frm_spc['style'] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['title'] = u'Редактирование: '+self._getTxtDescription()
        # frm_spc['onInit'] = 'GetManager(self).onInit(event)'

        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'_dlg.frm')
        txt = frm_gen_templates._editDlgResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                        form_file_name, res_module_file_name,
                                                        FormName_+'_EditDialog', FormName_+'_EditDialog')
        self._genResModule(res_module_file_name, txt)

        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'edit_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)
        
        # Панель в диалог добавляется по ссылке
        search_panel_spc = util.icSpcDefStruct(util.DeepCopy(icobjectlink.ic_class_spc), None)
        search_panel_spc['name'] = 'edit_panel_link'
        search_panel_spc['flag'] = wx.GROW | wx.EXPAND
        search_panel_spc['proportion'] = 1
        search_panel_spc['object'] = ((None, None, None, self.getEditFormName()+'.frm', None),)
        box_sizer_spc['child'].append(search_panel_spc)

        button_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        button_sizer_spc['name'] = 'button_sizer_h'
        button_sizer_spc['layout'] = 'horizontal'
        button_sizer_spc['flag'] = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        button_sizer_spc['border'] = 5
        box_sizer_spc['child'].append(button_sizer_spc)

        btn_cancel_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_cancel_spc['name'] = 'cancel_button'
        btn_cancel_spc['label'] = u'Отмена'
        btn_cancel_spc['flag'] = wx.ALL
        btn_cancel_spc['border'] = 5
        btn_cancel_spc['mouseClick'] = 'GetManager(self).onCancelButton(event)'
        button_sizer_spc['child'].append(btn_cancel_spc)
        
        btn_ok_spc = util.icSpcDefStruct(util.DeepCopy(icbutton.SPC_IC_BUTTON), None)
        btn_ok_spc['name'] = 'ok_button'
        btn_ok_spc['label'] = u'Ok'
        btn_ok_spc['flag'] = wx.ALL
        btn_ok_spc['border'] = 5
        btn_ok_spc['mouseClick'] = 'GetManager(self).onOkButton(event)'
        button_sizer_spc['child'].append(btn_ok_spc)

        return frm_spc

    def _genEditPanelRes(self, FormName_=None):
        """
        Генерация ресурса панели редактирования.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icwxpanel
        from ic.components.sizers import icboxsizer
        from ic.components.custom import icsplitter
        from ic.components import icobjectlink
        
        if FormName_ is None:
            FormName_ = self.getEditFormName()
        
        frm_spc = util.icSpcDefStruct(util.DeepCopy(icwxpanel.ic_class_spc), None)
        frm_spc['name'] = 'edit_panel'
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['flag'] = wx.GROW | wx.EXPAND
        frm_spc['style'] = wx.TAB_TRAVERSAL
        frm_spc['proportion'] = 1
        frm_spc['description'] = u'Редактирование: '+self._getTxtDescription()
        
        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._editResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                     form_file_name, res_module_file_name,
                                                     FormName_+'_EditPanel', FormName_+'_EditPanel')
        self._genResModule(res_module_file_name, txt)
        
        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'edit_sizer_v'
        box_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        box_sizer_spc['proportion'] = 1
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)
        
        if self.getHistory():
            # Если к объекту прикреплена история, то
            # необходимо в панель редактирования вставить панель
            # редактирования периодов истории
            splitter_spc = util.icSpcDefStruct(util.DeepCopy(icsplitter.ic_class_spc), None)
            splitter_spc['name'] = 'edit_splitter'
            splitter_spc['flag'] = wx.GROW | wx.EXPAND
            splitter_spc['proportion'] = 1
            splitter_spc['sash_pos'] = DEFAULT_DIALOG_HEIGHT/2
            box_sizer_spc['child'].append(splitter_spc)
            # Генерация ресурса стандартной панели поиска
            panel_spc = self._genStdEditPanelRes(FormName_)
            splitter_spc['win1'] = panel_spc
            #
            obj_link_spc = util.icSpcDefStruct(util.DeepCopy(icobjectlink.ic_class_spc), None)
            obj_link_spc['name'] = 'hist_panel_link'
            obj_link_spc['object'] = self.getHistory().getEditFormPsp()
            splitter_spc['win2'] = obj_link_spc
        else:
            # Генерация ресурса стандартной панели поиска
            panel_spc = self._genStdEditPanelRes(FormName_)
            box_sizer_spc['child'].append(panel_spc)
        
        return frm_spc
        
    def _genStdEditPanelRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартной панели инициализации. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        if self.isPageGroupEdit():
            return self._genStdEditNotebookRes(FormName_, ResModuleFileName_)
        else: 
            return self._genStdEditScrolledwinRes(FormName_, ResModuleFileName_)
        
    def _genStdEditNotebookRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного нотебука редактирования
        с группировкой реквизитов по страницам. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.custom import icnotebook
        from ic.components.sizers import icgridbagsizer
        
        notebook_spc = util.icSpcDefStruct(util.DeepCopy(icnotebook.ic_class_spc), None)
        notebook_spc['name'] = 'edit_notebook'
        notebook_spc['flag'] = wx.GROW | wx.EXPAND
        notebook_spc['proportion'] = 1
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isEdit():
                # Определить страницу, если группировка происходит по страницам
                page_title = None
                sizer_spc = None
                if self.isPageGroupEdit():
                    page_title = child_requisite.getGroupTitle()
                    # Добавление страницы
                    is_title = bool([title for title in notebook_spc['titles'] if title == page_title])
                    if not is_title:
                        page_spc = self._genStdNotebookPageRes(len(notebook_spc['titles']),
                                                               page_title, FormName_, ResModuleFileName_)
                        notebook_spc['child'].append(page_spc)
                        notebook_spc['titles'].append(page_title)
                    else:
                        page_spc = notebook_spc['child'][notebook_spc['titles'].index(page_title)]
                    sizer_spc = page_spc['child'][0]
                
                if sizer_spc:
                    # Вычисление максимальной позиции y нового контрола на текущей странице
                    max_row = 0
                    if 'child' in sizer_spc and sizer_spc['child']:
                        positions = [pos[0] for pos in [ctrl['position'] for ctrl in sizer_spc['child']]]
                        if positions:
                            max_row = max(positions)
                        
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (max_row+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (max_row+1, 2)

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (max_row+1, 1)
                        box_spc['span'] = (1, 2)
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outLog(u'Ошибка определения типа реквизита %s' % child_requisite.name)
        
        return notebook_spc
    
    def _genStdEditScrolledwinRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного скроллируемого окна 
        редактирования без группировки реквизитов. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components import icscrolledpanel
        from ic.components.sizers import icgridbagsizer

        scrolledwin_spc = util.icSpcDefStruct(util.DeepCopy(icscrolledpanel.ic_class_spc), None)
        scrolledwin_spc['name'] = 'edit_scrolledwin'
        scrolledwin_spc['flag'] = wx.GROW | wx.EXPAND
        scrolledwin_spc['style'] = wx.TAB_TRAVERSAL
        scrolledwin_spc['proportion'] = 1
        
        win_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icgridbagsizer.ic_class_spc), None)
        win_sizer_spc['name'] = 'win_sizer'
        win_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        win_sizer_spc['proportion'] = 1
        win_sizer_spc['vgap'] = 5
        win_sizer_spc['flexCols'] = [2]
        scrolledwin_spc['child'].append(win_sizer_spc)
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isEdit():
                sizer_spc = win_sizer_spc
                if sizer_spc:    
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (i+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (i+1, 2)

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (max_row+1, 1)
                        box_spc['span'] = (1, 2)
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outLog(u'Ошибка определения типа реквизита %s' % child_requisite.name)
        
        return scrolledwin_spc
        
    def createEditFormRes(self):
        """
        Создание, по описанию объекта, ресурса формы редактирования.
        @return: Возвращает паспорт сгенерированной формы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        frm_name = self.getEditFormName()
        # Если имя определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if frm_name and not prj_res_ctrl.isRes(frm_name, 'frm'):

            frm_res = self._genEditPanelRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name, 'frm', frm_res)

            frm_res = self._genEditDialogRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name+'_dlg', 'frm', frm_res)
            
        frm_psp = (('Dialog', 'edit_dlg', None, frm_name+'_dlg.frm', None),)
        return frm_psp

    # Форма просмотра объекта
    def _genViewDialogRes(self, FormName_=None):
        """
        Генерация ресурса формы просмотра.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icdialog
        from ic.components.sizers import icboxsizer
        from ic.components import icobjectlink
        
        if FormName_ is None:
            FormName_ = self.getViewFormName()+'_dlg'

        frm_spc = util.icSpcDefStruct(util.DeepCopy(icdialog.ic_class_spc), None)
        frm_spc['name'] = 'view_dlg'
        frm_spc['size'] = DEFAULT_DIALOG_SIZE
        frm_spc['style'] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['title'] = u'Просмотр: '+self._getTxtDescription()

        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._viewDlgResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                        form_file_name, res_module_file_name,
                                                        FormName_+'_ViewDialog', FormName_+'_ViewDialog')
        self._genResModule(res_module_file_name, txt)

        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'view_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)
        
        # Панель в диалог добавляется по ссылке
        search_panel_spc = util.icSpcDefStruct(util.DeepCopy(icobjectlink.ic_class_spc), None)
        search_panel_spc['name'] = 'view_panel_link'
        search_panel_spc['flag'] = wx.GROW | wx.EXPAND
        search_panel_spc['proportion'] = 1
        search_panel_spc['object'] = ((None, None, None, self.getViewFormName()+'.frm', None),)
        box_sizer_spc['child'].append(search_panel_spc)

        button_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        button_sizer_spc['name'] = 'button_sizer_h'
        button_sizer_spc['layout'] = 'horizontal'
        box_sizer_spc['child'].append(button_sizer_spc)
        
        return frm_spc

    def _genViewPanelRes(self, FormName_=None):
        """
        Генерация ресурса панели просмотра.
        @param FormName_: Имя генерируемой формы.
        @return: Возвращает ресурс сгенерированной формы.
        """
        from ic.components import icwxpanel
        from ic.components.custom import ictoolbar
        from ic.components.sizers import icboxsizer
        
        if FormName_ is None:
            FormName_ = self.getViewFormName()
        
        frm_spc = util.icSpcDefStruct(util.DeepCopy(icwxpanel.ic_class_spc), None)
        frm_spc['name'] = 'view_panel'
        frm_spc['res_module'] = FormName_+'_frm.py'
        frm_spc['flag'] = wx.GROW | wx.EXPAND
        frm_spc['style'] = wx.TAB_TRAVERSAL
        frm_spc['description'] = u'Просмотр: '+self._getTxtDescription()
        
        # Модуль ресурса
        res_module_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+frm_spc['res_module'])
        if ic_file.Exists(res_module_file_name):
            ic_file.Remove(res_module_file_name)
        form_file_name = ic_file.AbsolutePath(ic_user.icGet('PRJ_DIR')+'/'+FormName_+'.frm')
        txt = frm_gen_templates._viewResModuleFmt % (form_file_name, '### RESOURCE_MODULE',
                                                     form_file_name, res_module_file_name,
                                                     FormName_+'_ViewPanel', FormName_+'_ViewPanel')
        self._genResModule(res_module_file_name, txt)
        
        box_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icboxsizer.ic_class_spc), None)
        box_sizer_spc['name'] = 'view_sizer_v'
        box_sizer_spc['layout'] = 'vertical'
        frm_spc['child'].append(box_sizer_spc)

        # Генерация ресурса стандартной панели
        panel_spc = self._genStdViewPanelRes(FormName_)
        box_sizer_spc['child'].append(panel_spc)
        
        return frm_spc
        
    def _genStdViewPanelRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартной панели просмотра. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        if self.isPageGroupView():
            return self._genStdViewNotebookRes(FormName_, ResModuleFileName_)
        else: 
            return self._genStdViewScrolledwinRes(FormName_, ResModuleFileName_)
        
    def _genStdViewNotebookRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного нотебука просмотр
        с группировкой реквизитов по страницам. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components.custom import icnotebook
        from ic.components.sizers import icgridbagsizer
        
        notebook_spc = util.icSpcDefStruct(util.DeepCopy(icnotebook.ic_class_spc), None)
        notebook_spc['name'] = 'view_notebook'
        notebook_spc['flag'] = wx.GROW | wx.EXPAND
        notebook_spc['proportion'] = 1
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isView():
                # Определить страницу, если группировка происходит по страницам
                page_title = None
                sizer_spc = None
                if self.isPageGroupView():
                    page_title = child_requisite.getGroupTitle()
                    # Добавление страницы
                    is_title = bool([title for title in notebook_spc['titles'] if title == page_title])
                    if not is_title:
                        page_spc = self._genStdNotebookPageRes(len(notebook_spc['titles']),
                                                               page_title, FormName_, ResModuleFileName_)
                        notebook_spc['child'].append(page_spc)
                        notebook_spc['titles'].append(page_title)
                    else:
                        page_spc = notebook_spc['child'][notebook_spc['titles'].index(page_title)]
                    sizer_spc = page_spc['child'][0]
                
                if sizer_spc:
                    # Вычисление максимальной позиции y нового контрола на текущей странице
                    max_row = 0
                    if 'child' in sizer_spc and sizer_spc['child']:
                        positions = [pos[0] for pos in [ctrl['position'] for ctrl in sizer_spc['child']]]
                        if positions:
                            max_row = max(positions)
                        
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (max_row+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (max_row+1, 2)
                        editor_spc['style'] = wx.TE_READONLY
                        editor_spc['enable'] = False

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (max_row+1, 1)
                        box_spc['span'] = (1, 2)
                        box_spc['child'][0]['enable'] = False
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outLog(u'Ошибка определения типа реквизита %s' % child_requisite.name)
                    
        return notebook_spc
    
    def _genStdViewScrolledwinRes(self, FormName_, ResModuleFileName_=None):
        """
        Функция генерации ресурса стандартного скроллируемого окна 
        просмотра без группировки реквизитов. 
        @param FormName_: Имя генерируемой формы.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """ 
        from ic.components import icscrolledpanel
        from ic.components.sizers import icgridbagsizer

        scrolledwin_spc = util.icSpcDefStruct(util.DeepCopy(icscrolledpanel.ic_class_spc), None)
        scrolledwin_spc['name'] = 'view_scrolledwin'
        scrolledwin_spc['flag'] = wx.GROW | wx.EXPAND
        scrolledwin_spc['style'] = wx.TAB_TRAVERSAL
        scrolledwin_spc['proportion'] = 1
        
        win_sizer_spc = util.icSpcDefStruct(util.DeepCopy(icgridbagsizer.ic_class_spc), None)
        win_sizer_spc['name'] = 'win_sizer'
        win_sizer_spc['flag'] = wx.GROW | wx.EXPAND
        win_sizer_spc['proportion'] = 1
        win_sizer_spc['vgap'] = 5
        win_sizer_spc['flexCols'] = [2]
        scrolledwin_spc['child'].append(win_sizer_spc)
        
        # Редакторы реквизитов:
        for i, child_requisite in enumerate(self.getChildrenRequisites()):
            if child_requisite._isView():
                sizer_spc = win_sizer_spc
                if sizer_spc:    
                    if issubclass(child_requisite.__class__, icAttrFormGenerator):
                        # Надпись
                        label_spc = child_requisite._genStdLabelRes(ResModuleFileName_)
                        label_spc['position'] = (i+1, 1)
                        # Редактор
                        editor_spc = child_requisite._genStdEditorRes(ResModuleFileName_)
                        editor_spc['position'] = (i+1, 2)
                        editor_spc['style'] = wx.TE_READONLY
                        editor_spc['enable'] = False

                        sizer_spc['child'].append(label_spc)
                        sizer_spc['child'].append(editor_spc)
                    elif issubclass(child_requisite.__class__, icGridFormGenerator):
                        # Грид редактирования табличного реквизита
                        box_spc = child_requisite._genStdGridRes(ResModuleFileName_)
                        box_spc['position'] = (max_row+1, 1)
                        box_spc['span'] = (1, 2)
                        box_spc['child'][0]['enable'] = False
                        sizer_spc['child'].append(box_spc)
                    else:
                        io_prnt.outLog(u'Ошибка определения типа реквизита %s' % child_requisite.name)
        
        return scrolledwin_spc
        
    def createViewFormRes(self):
        """
        Создание, по описанию объекта, ресурса формы просмотра.
        @return: Возвращает паспорт сгенерированной формы.
        """
        # Открыть проект
        prj_res_ctrl = ic_user.getKernel().getProjectResController()
        prj_res_ctrl.openPrj()

        # Проверка на добавление нового ресурса
        frm_name = self.getViewFormName()
        # Если имя определено нет ресурса таблицы с таким именем, то запустить
        # создание ресурса таблицы
        if frm_name and not prj_res_ctrl.isRes(frm_name, 'frm'):
            frm_res = self._genViewPanelRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name, 'frm', frm_res)

            frm_res = self._genViewDialogRes(frm_name)
            # Сохранить ресурс
            prj_res_ctrl.saveRes(frm_name+'_dlg', 'frm', frm_res)
            
        frm_psp = (('Panel', 'view_dlg', None, frm_name+'_dlg.frm', None),)
        return frm_psp

    # Свойства
    def getEditFormName(self):
        """
        Имя формы редактирования.
        """
        frm_psp = self.getEditFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genEditFormName()

    def _genEditFormName(self):
        """
        Генерация имени формы редактирования.
        """
        return str(self.name).lower()+'_edit'

    def getViewFormName(self):
        """
        Имя формы просмотра.
        """
        frm_psp = self.getViewFormPsp()
        if frm_psp:
            return frm_psp[0][1]
        else:
            return self._genViewFormName()

    def _genViewFormName(self):
        """
        Генерация имени формы просмотра.
        """
        return str(self.name).lower()+'_view'

    def getInitFormPsp(self):
        """
        Форма/Визард для создания/инициализации.
        """
        return None
        
    def getEditFormPsp(self):
        """
        Форма для редактирования.
        """
        return None
        
    def getViewFormPsp(self):
        """
        Форма для просмотра.
        """
        return None
        
    def getSearchFormPsp(self):
        """
        Форма поиска объектов по его атрибутам.
        """
        return None

    def getChoiceFormPsp(self):
        """
        Форма выбора объекта.
        """
        return None

# Идентификаторы типов редакторов реквизитов
TEXT_EDIT_TYPE = 'Text'
DATE_EDIT_TYPE = 'Date'
INT_EDIT_TYPE = 'Integer'
FLOAT_EDIT_TYPE = 'Float'
NSI_EDIT_TYPE = 'NSI'
REF_EDIT_TYPE = 'REF'
# Тип редактора по умолчанию
DEFAULT_EDIT_TYPE = TEXT_EDIT_TYPE

# Размеры редактора атрибута по умолчанию
DEFAULT_ATTR_EDIT_WIDTH = 50
DEFAULT_ATTR_EDIT_HEIGHT = -1
DEFAULT_ATTR_EDIT_SIZE = (DEFAULT_ATTR_EDIT_WIDTH, DEFAULT_ATTR_EDIT_HEIGHT)


class icAttrFormGenerator:
    """
    Базовый класс генератора форм атрибута компонента.
        Реализует внутри себя механизм генерации спецификации форм отображения/редактирования.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        pass

    def _getTxtDescription(self):
        """
        Описание объекта в текстовом представлении.
        """
        if type(self.description) in (str, unicode):
            return self.description.strip()
        return ''
        
    def _getTxtLabel(self):
        """
        Надпись атрибута.
        """
        try:
            if self.label and type(self.label) in (str, unicode):
                return self.label
        except AttributeError:
            io_prnt.outLog(u'У атрибута <%s> объекта не определено свойство label' % self.name)
        description = self._getTxtDescription()
        if description[-1] != u':':
            return description+u':'
        return description
    
    def _isInit(self):
        """
        Атрибут объекта располагается на форме инициализации?
        """
        try:
            return self.isInit()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isInit' % self.name)
            return True
        
    def _isEdit(self):
        """
        Атрибут объекта располагается на форме редактирования?
        """
        try:
            return self.isEdit()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isEdit' % self.name)
            return True
        
    def _isView(self):
        """
        Атрибут объекта располагается на форме просмотра?
        """
        try:
            return self.isView()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isView' % self.name)
            return True
        
    def _isSearch(self):
        """
        Атрибут объекта располагается на форме поиска?
        """
        try:
            return self.isSearch()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isSearch' % self.name)
            return True

    def _isIDAttr(self):
        """
        Атрибут объекта является идентификационным для объекта?
        """
        try:
            return self.isIDAttr()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isIDAttr' % self.name)
            return False
        
    def _genEditorName(self):
        """
        Имя редактора реквизита.
        """
        return str(self.name).lower()+'_edit'
        
    def _getEditType(self):
        """
        Определить тип редактора реквизита.
        Тип редактора в случае реквизита определяется по типу хранимого 
        значения. В реквизите этом метод должен переопределяться.
        """
        return DEFAULT_EDIT_TYPE        
        
    def _genStdEditorRes(self, ResModuleFileName_=None):
        """
        Генерация стандартного редактора реквизита объекта.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        edit_type = self._getEditType()
        editor_spc = None
        if edit_type == TEXT_EDIT_TYPE:
            editor_spc = self._genTxtEditorRes(self._genEditorName(), ResModuleFileName_)
        elif edit_type == DATE_EDIT_TYPE:
            editor_spc = self._genDateEditorRes(self._genEditorName(), ResModuleFileName_)
        elif edit_type == INT_EDIT_TYPE:
            editor_spc = self._genIntEditorRes(self._genEditorName(), ResModuleFileName_)
        elif edit_type == FLOAT_EDIT_TYPE:
            editor_spc = self._genFloatEditorRes(self._genEditorName(), ResModuleFileName_)
        elif edit_type == REF_EDIT_TYPE:
            editor_spc = self._genREFEditorRes(self._genEditorName(), ResModuleFileName_)
        elif edit_type == NSI_EDIT_TYPE:
            editor_spc = self._genNSIEditorRes(self._genEditorName(), ResModuleFileName_)
        else:
            io_prnt.outLog(u'Не определен тип редактора реквизита <%s>' % self.name)
            
        return editor_spc

    def _genTxtEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание текстового редакторв реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components import ictextfield
        
        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(ictextfield.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW|wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['style'] |= wx.ALIGN_LEFT
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()
        
        # Дополнить модуль ресурса обработчиками событий

        return editor_spc
        
    def _genDateEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание редакторв дат реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.user import icdatepickerctrl
        
        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(icdatepickerctrl.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW | wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['style'] |= wx.DP_DROPDOWN
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()
        
        # Дополнить модуль ресурса обработчиками событий

        return editor_spc
    
    def _genIntEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание редакторв целых чисел реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.custom import icspinner
        
        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(icspinner.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW | wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['style'] |= wx.ALIGN_LEFT
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()
        
        # Дополнить модуль ресурса обработчиками событий

        return editor_spc

    def _genFloatEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание редакторв чисел с плавающей точкой реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.custom import icspinner
        
        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(icspinner.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW | wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['style'] |= wx.ALIGN_LEFT
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()
        
        # Дополнить модуль ресурса обработчиками событий

        return editor_spc

    def _genNSIEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание редактора ссылки на справочник реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from NSI.usercomponents import spravtreecomboctrl
        
        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(spravtreecomboctrl.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW | wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()
        
        # настройка взаимодействия контрола со справочником
        editor_spc['sprav'] = self.getNSIPsp()
        
        return editor_spc

    def _genREFEditorRes(self, EditorName_, ResModuleFileName_=None):
        """
        Создание редактора ссылки на бизнес объект/документ реквизита объекта.
        @param EditorName_: Имя редактора.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from work_flow.usercomponents import refobjchoicecomboctrl

        # Редактор
        editor_spc = util.icSpcDefStruct(util.DeepCopy(refobjchoicecomboctrl.ic_class_spc), None)
        editor_spc['name'] = EditorName_
        editor_spc['flag'] = wx.GROW | wx.EXPAND
        editor_spc['proportion'] = 1
        editor_spc['size'] = DEFAULT_ATTR_EDIT_SIZE
        editor_spc['border'] = 2
        editor_spc['data_name'] = self.getFieldName()

        # настройка взаимодействия контрола с объектом
        editor_spc['obj_psp'] = self.getRefObjPsp()

        return editor_spc

    def _genStdLabelRes(self, ResModuleFileName_=None):
        """
        Генерация стандартной надписи реквизита объекта.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.custom import icstatictext

        # Надпись
        label_spc = util.icSpcDefStruct(util.DeepCopy(icstatictext.ic_class_spc), None)
        label_spc['name'] = str(self.name).lower()+'_label'
        label_spc['flag'] = wx.GROW | wx.EXPAND
        label_spc['proportion'] = 0
        label_spc['text'] = self._getTxtLabel()+':'
        label_spc['style'] |= wx.ALIGN_RIGHT
        label_spc['size'] = (-1, -1)
        label_spc['border'] = 2
        
        # Дополнить модуль ресурса обработчиками событий

        return label_spc

# Размеры редактора табличного атрибута по умолчанию
DEFAULT_GRID_EDIT_WIDTH = 500
DEFAULT_GRID_EDIT_HEIGHT = 300
DEFAULT_GRID_EDIT_SIZE = (DEFAULT_GRID_EDIT_WIDTH, DEFAULT_GRID_EDIT_HEIGHT)


class icGridFormGenerator:
    """
    Базовый класс генератора форм табличного атрибута компонента.
        Реализует внутри себя механизм генерации спецификации форм отображения/редактирования.
    """
    def __init__(self, Parent_=None):
        """
        Конструктор.
        @param Parent_: Родительский объект.
        """
        pass

    def _isInit(self):
        """
        Атрибут объекта располагается на форме инициализации?
        """
        try:
            return self.isInit()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isInit' % self.name)
            return True
        
    def _isEdit(self):
        """
        Атрибут объекта располагается на форме редактирования?
        """
        try:
            return self.isEdit()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isEdit' % self.name)
            return True
        
    def _isView(self):
        """
        Атрибут объекта располагается на форме просмотра?
        """
        try:
            return self.isView()
        except AttributeError:
            io_prnt.outLog(u'В атрибуте <%s> объекта не определен метод isView' % self.name)
            return True
        
    def _isSearch(self):
        """
        Атрибут объекта располагается на форме поиска?
        """
        return False

    def _isIDAttr(self):
        """
        Атрибут объекта является идентификационным для объекта?
        """
        return False
    
    def _genGridName(self):
        """
        Имя грида табличного реквизита.
        """
        return str(self.name).lower()+'_edit'
    
    def _genStdGridRes(self, ResModuleFileName_=None):
        """
        Генерация стандартного грида табличного реквизита объекта.
        @param ResModuleFileName_: Имя файла ресурсного модуля.
        @return: Возвращает ресурс сгенерированного объекта.
        """
        from ic.components.sizers import icstaticboxsizer
        from ic.components import icgriddataset
        from ic.components import icgrid
        
        # Сайзер
        sizer_spc = util.icSpcDefStruct(util.DeepCopy(icstaticboxsizer.ic_class_spc), None)
        sizer_spc['flag'] = wx.GROW | wx.EXPAND
        sizer_spc['proportion'] = 1
        sizer_spc['label'] = self.getLabel()
        
        # Грид
        grid_spc = util.icSpcDefStruct(util.DeepCopy(icgriddataset.ic_class_spc), None)
        grid_spc['name'] = self._genGridName()
        grid_spc['flag'] = wx.GROW | wx.EXPAND
        grid_spc['proportion'] = 1
        grid_spc['size'] = DEFAULT_GRID_EDIT_SIZE
        grid_spc['data_name'] = self.getTableName()

        # Заполнение колонок
        for child_requisite in self.getChildrenRequisites():
            if child_requisite._isEdit():
                column_spc = util.icSpcDefStruct(util.DeepCopy(icgrid.SPC_IC_CELL), None)
                column_spc['name'] = child_requisite.getFieldName()
                column_spc['label'] = child_requisite.getLabel()
                column_spc['width'] = child_requisite._getDefaultWidth()
                
                if child_requisite._getEditType() == NSI_EDIT_TYPE:
                    # Для реквизитов связи со справочником указать функцию вызова справочника
                    hlp_script = u'return OBJ.findRequisite(\'%s\').getSprav().Hlp(ParentCode=None)\n' % child_requisite.name
                    column_spc['hlp'] = hlp_script
                
                grid_spc['cols'].append(column_spc)            
            
        sizer_spc['child'].append(grid_spc)
        return sizer_spc
