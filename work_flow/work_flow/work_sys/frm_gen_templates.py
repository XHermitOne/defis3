#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль шаблонов генератора форм.
"""

_stdToolbarResModuleFmt = '''
    def onAddTool(Context_):
        \"\"\"
        Обработчик добавления объекта.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        pass
        
    def onDelTool(Context_):
        \"\"\"
        Обработчик удаления объекта.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        pass

    def onEditTool(Context_):
        \"\"\"
        Обработчик редактирования объекта.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        pass
        
    def onModeTool(Context_):
        \"\"\"
        Обработчик изменения режима работы с объектом.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        pass
        
    def onFindTool(Context_):
        \"\"\"
        Обработчик поиска объекта.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        pass
        
'''

_stdTreeBrwsResModuleFmt = '''
    def onInitTreeBrws(Context_):
        \"\"\"
        Обработчик инициализации дерева просмотра объекта.
        @param Context_: Контекст выполнения формы.
        \"\"\"
        try:
            obj = Context_['OBJ']
            storage = obj.getStorage()
            tree_data = storage.getBranchObj()
            tree_ctrl = Context_.GetObject('tree_object_ctrl')
            tree_ctrl.LoadTree(tree_data)
            return True 
        except:
            ic.io_prnt.outErr(u'Ошибка инициализации дерева просмотра объекта')
            return False
        
'''

_choiceDlgResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface

class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"
    
    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass

    def onOkButton(self, event):
        \"\"\"
        Обработчик кнопки <OK>.
        \"\"\"
        try:
            dlg = self.GetObject('choice_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result'] = self.GetObject('view_obj_grid').getSelectedObjUUID()
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        \"\"\"
        Обработчик кнопки <Отмена>.
        \"\"\"
        try:
            dlg = self.GetObject('choice_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()

    def onInit(self, event):
        \"\"\"
        Инициализация всех контролов диалогового окна.
        \"\"\"
        self.GetObject('view_obj_grid').refreshDataset()

    def onSearchTool(self, event):
        \"\"\"
        Запуск поиска объектов, соответствующих фильтру.
        \"\"\"
        obj = self.context['OBJ']
        filter = self.GetObject('filter_constructor_tree').getEditResult()
        query = obj.getFilterSQLAlchemy(filter)
        records = query.execute().fetchall()        
        dataset = obj._resultFilter2Dataset(records)
        self.GetObject('view_obj_grid').setDataset(dataset)
    
    def onClearFilterTool(self, event):
        \"\"\"
        Очистка фильтра.
        \"\"\"
        self.GetObject('filter_constructor_tree').clearTree()
    
    def onHideFilterTool(self, event):
        \"\"\"
        Скрыть дерево фильтра.
        \"\"\"
        self.GetObject('choice_splitter').hideWindow1()
        toolbar = self.GetObject('search_toolbar')
        toolbar.EnableTool(toolbar.getToolId('hide_filter_tool'), False)
        toolbar.EnableTool(toolbar.getToolId('show_filter_tool'), True)
    
    def onShowFilterTool(self, event):
        \"\"\"
        Показать дерево фильтра.
        \"\"\"
        self.GetObject('choice_splitter').showWindow1()
        toolbar = self.GetObject('search_toolbar')
        toolbar.EnableTool(toolbar.getToolId('hide_filter_tool'), True)
        toolbar.EnableTool(toolbar.getToolId('show_filter_tool'), False)
    
    def onViewObjTool(self, event):
        \"\"\"
        Просмотр объекта.
        \"\"\"
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.View(UUID_=obj_uuid)        

    def onEditObjTool(self, event):
        \"\"\"
        Редактирование объекта.
        \"\"\"
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.Edit(UUID_=obj_uuid)        
            obj_list.refreshDataset()

    def onAddObjTool(self, event):
        \"\"\"
        Добавление объекта.
        \"\"\"
        obj_list = self.GetObject('view_obj_grid')
        obj = self.context['OBJ']
        rec = obj.Add()
        if rec:
            obj.addRequisiteData(rec)
            obj_list.refreshDataset()

    def onDelObjTool(self, event):
        \"\"\"
        Удаление объекта.
        \"\"\"
        obj_list = self.GetObject('view_obj_grid')
        obj_uuid = obj_list.getSelectedObjUUID()
        if obj_uuid:
            obj = self.context['OBJ']
            obj.Del(UUID_=obj_uuid)
            obj_list.refreshDataset()

    def getSelectedObjUUID(self):
        \"\"\"
        UUID выбранного объекта.
        \"\"\"
        return self.GetObject('view_obj_grid').getSelectedObjUUID()
        
        
manager_class = %sManager

'''

# Шаблон обработчика кнопки <Отмена> в диалоговых формах
_cancelMouseClickScript = '''def onCancelButtonMouseClick(Context_):
    \"\"\"
    Обработчик нажатия на кнопку <Отмена>.
    \"\"\"
    try:
        dlg = Context_['_root_obj']
        dlg.EndModal(wx.ID_CANCEL)
        Context_['result'] = None
    except:
        ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
    return None
    
'''

# Шаблон обработчика кнопки <OK> в диалоговых формах
_okMouseClickScript = '''def onOkButtonMouseClick(Context_):
    \"\"\"
    Обработчик нажатия на кнопку <OK>.
    \"\"\"
    try:
        dlg = Context_['_root_obj']
        dlg.EndModal(wx.ID_OK)
        Context_['result'] = True
    except:
        ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
    return None
    
'''

# Шаблон модуля ресурса для формы инициализации объекта
_initResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"
    
    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass
    
    def onOkButton(self, event):
        \"\"\"
        Обработчик кнопки <OK>.
        \"\"\"
        try:
            dlg = self.GetObject('init_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result'] = True
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        \"\"\"
        Обработчик кнопки <Отмена>.
        \"\"\"
        try:
            dlg = self.GetObject('init_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()

    def onEditButton(self, event):
        \"\"\"
        Обработчик кнопки <Редактирование>.
        \"\"\"
        try:
            dlg = self.GetObject('init_dlg')
            obj = self.context['OBJ']
            init_data = dlg.GetContext().getValueInCtrl(dlg)
            obj.addRequisiteData(init_data)

            # ВНИМАНИЕ! Окно закрывается без сохранения, но сохранение 
            # все таки делается чтобы не проходило сохранение в функции Init
            # на последнем этапе
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None

            if obj:
                # Создать новый контекст у объекта, т.к. 
                # он будет работать в другом режиме
                obj.Edit(Context_=ic.components.icwidget.icResObjContext())
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Редактирование>.')
        event.Skip()


manager_class = %sManager

'''

# Шаблон модуля ресурса для формы/панели поиска объекта
_searchResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"
    
    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        # Бизнес-объект, в котором ведется поиск
        self.OBJ = self.context['OBJ']

    def onSearchTool(self, event):
        \"\"\"
        Обработчик нахатия на кнопке <Поиск> на панели инструментов.
        \"\"\"
        filter_requisite = self.context.getValueInCtrl(self.GetObject('search_panel'))
        obj_dataset = self.OBJ.filterRequisiteData(filter_requisite)
        self.GetObject('view_obj_grid').setDataset(dataset)

    def onClearTool(self, event):
        \"\"\"
        Обработчик нахатия на кнопке <Очистить> на панели инструментов.
        \"\"\"
        self.context.clearValueInCtrl(self.GetObject('search_panel'))
        event.Skip()
    
    def onShowGridTool(self, event):
        \"\"\"
        Обработчик нахатия на кнопке <Показать/скрыть объекты> на панели инструментов.
        \"\"\"
        self.GetObject('search_splitter').toggleWindow2()
        event.Skip()
    
    def onViewTool(self, event):
        \"\"\"
        Обработчик нахатия на кнопке <Режим просмотра> на панели инструментов.
        \"\"\"
        self.OBJ.View(self.GetObject('search_panel'))
        event.Skip()
    
    def onEditTool(self, event):
        \"\"\"
        Обработчик нахатия на кнопке <Режим редактирования> на панели инструментов.
        \"\"\"
        self.OBJ.Edit(self.GetObject('search_panel'))
        event.Skip()
    
    def getSelectedObjUUID(self):
        \"\"\"
        UUID выбранного объекта.
        \"\"\"
        return self.GetObject('view_obj_grid').getSelectedObjUUID()

        
manager_class = %sManager

'''

# Шаблон модуля ресурса для диалоговой формы поиска объекта
_searchDlgResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"
    
    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass
    
    def onOkButton(self, event):
        \"\"\"
        Обработчик кнопки <OK>.
        \"\"\"
        try:
            dlg = self.GetObject('search_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result'] = True
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        \"\"\"
        Обработчик кнопки <Отмена>.
        \"\"\"
        try:
            dlg = self.GetObject('search_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()


manager_class = %sManager

'''

# Шаблон модуля ресурса для формы редактирования объекта
_editDlgResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"
    
    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass
    
    def onOkButton(self, event):
        \"\"\"
        Обработчик кнопки <OK>.
        \"\"\"
        try:
            dlg = self.GetObject('edit_dlg')

            hist_panel = self.GetObject('edit_panel_link').GetObject('hist_panel_link')
            if hist_panel:
                # Сохранить последние значения реквизитов состояния
                hist_panel.GetContext()['GetManager']().saveStateRequisites()

            dlg.EndModal(wx.ID_OK)
            self.context['result'] = True
            
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        \"\"\"
        Обработчик кнопки <Отмена>.
        \"\"\"
        try:
            dlg = self.GetObject('edit_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()
        
    def onInitDlg(self, event):
        \"\"\"
        Инициализация всех контролов диалогового окна.
        \"\"\"
        obj = self.context['OBJ']
        history = obj.getHistory()
        if history:
            # В контекст объектов прикрепленных с помощью ObjectLink передавать
            # параметры через контекст можно только принудительно
            self.GetObject('edit_panel_link').get_replace_object().GetContext()['OBJ'] = obj
            # Установить редактируемы объект у панели состояний объекта
            self.GetObject('edit_panel_link').GetObject('hist_panel_link').GetContext()['GetManager']().setOBJ(obj)


manager_class = %sManager

'''

# Шаблон модуля ресурса для панели редактирования объекта
_editResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"

    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass


manager_class = %sManager

'''

# Шаблон модуля ресурса для формы просмотра объекта
_viewDlgResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"

    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass
    
    def onOkButton(self, event):
        \"\"\"
        Обработчик кнопки <OK>.
        \"\"\"
        try:
            dlg = self.GetObject('view_dlg')
            dlg.EndModal(wx.ID_OK)
            self.context['result'] = True
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <OK>.')
        event.Skip()

    def onCancelButton(self, event):
        \"\"\"
        Обработчик кнопки <Отмена>.
        \"\"\"
        try:
            dlg = self.GetObject('view_dlg')
            dlg.EndModal(wx.ID_CANCEL)
            self.context['result'] = None
        except:
            ic.io_prnt.outErr(u'Обработчик нажатия на кнопку <Отмена>.')
        event.Skip()


manager_class = %sManager

'''

# Шаблон модуля ресурса для панели просмотра объекта
_viewResModuleFmt = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль ресурса <%s>.
\"\"\"

%s: %s
# -----------------------------------------------------------------------------
# Name:        %s
# Purpose:     Модуль ресурса.
#
# Author:      <Создан генератором форм>
#
# Created:     
# RCS-ID:      $Id: $
# Copyright:   (c) 
# Licence:     <your licence>
# -----------------------------------------------------------------------------

#   Версия модуля
__version__ = (0, 0, 0, 1)

# Imports
import wx
import ic 
from ic.interfaces import icmanagerinterface


class %sManager(icmanagerinterface.icWidgetManager):
    \"\"\"
    Менеджер формы.
    \"\"\"

    def Init(self):
        \"\"\"     
        Функция инициализации менеджера.
        \"\"\"
        wx.CallAfter(self._init)

    def _init(self):
        \"\"\"
        Основная функция инициализации внутренних объектов.
        \"\"\"
        pass


manager_class = %sManager

'''
