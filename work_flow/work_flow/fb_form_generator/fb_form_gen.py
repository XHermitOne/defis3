#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль генератора проекта wxFormBuilder (*.fbp)
по ресурсу метаданных.
В качестве метаданных м.б.:
    Бизнес объекты
    Объекты состояния
    Документы
"""

import os
import os.path
import wx
from ic.log import log
from ic.utils import ic_extend
from . import fb_form_template
from ic.dlg import ic_dlg


# Версия
__version__ = (0, 0, 0, 2)


PARSED_TYPES = ('BusinesObj', 'StateObj', 'Document')
REQUISITE_TYPES = ('Requisite', 'NSIRequisite', 'REFRequisite', 'TABRequisite')


class icWxFBPrjGenerator(object):
    """
    Класс генератора проекта wxFormBuilder (*.fbp).
    """

    def __init__(self):
        """
        Конструктор.
        """
        # Имя файла проекта
        self.fbp_filename = None
        # Текст-содержание проекта
        self.fbp_txt = u''

        # Ресурс объекта по которому производиться генерация
        self.resource = None

    def setGenFilename(self, filename, is_rewrite=True):
        """
        Установить файл проекта для генерации.
        @param is_rewrite: Перезаписать если уже существует?
        """
        if os.path.exists(filename) and is_rewrite:
            os.remove(filename)

        self.fbp_filename = filename

    def isParsed(self, resource):
        """
        Проверка на поддерживаемый тип ресурса.
        @param resource: Ресурс генерации.
        @return: True - генератор сможет обработать этот вид ресурса.
            False - генератор не поддерживает этот тип ресурса.
        """
        if not resource:
            log.warning(u'Указан пустой ресурс для генерации проекта wxFormBuilder')
            return False

        res_key = resource.keys()[0]
        res_type = resource[res_key]['type']
        return res_type in PARSED_TYPES

    def setResource(self, resource):
        """
        Установить ресурс объекта, по которому производиться генерация.
        @param resource: Ресурс генерации.
        """
        if self.isParsed(resource):
            self.resource = resource
        else:
            self.resource = None

    def genPrjName(self):
        """
        Генерация имени проекта.
        @return: Имя проекта.
        """
        name = os.path.basename(self.resource.keys()[0])
        prj_name = name.lower() + '_frm_proto'
        return prj_name

    def savePrj(self, txt=None, prj_filename=None):
        """
        Сохранить текст проекта в файл.
        @param txt:
        @param prj_filename:
        @return: True/False.
        """
        if txt is None:
            txt = self.fbp_txt

        if prj_filename is None:
            prj_filename = self.fbp_filename

        return ic_extend.save_file_text(prj_filename, txt)

    def genPrj(self, resource=None):
        """
        Генерация проекта.
        @param resource: Ресурс генерации.
        @return: Текст сгенерированного проекта файла *.fbp.
            Либо None в случае какой либо ошибки.
        """
        if resource:
            self.setResource(resource)

        if self.resource is None:
            return None

        prj_name = self.genPrjName()
        # Генерация самих форм
        content = u''
        content += self.genInitPanel(self.resource.values()[0])
        content += self.genInitDlg(self.resource.values()[0])
        content += self.genEditPanel(self.resource.values()[0])
        content += self.genEditDlg(self.resource.values()[0])
        content += self.genViewPanel(self.resource.values()[0])
        content += self.genViewDlg(self.resource.values()[0])

        content += self.genChoicePanel(self.resource.values()[0])
        content += self.genChoiceDlg(self.resource.values()[0])

        content += self.genBrowsePanel(self.resource.values()[0])

        txt = fb_form_template.FBP_PRJ_TEMPLATE % (prj_name, prj_name, content)
        self.fbp_txt = txt
        return self.fbp_txt

    def genBoxSizerName(self):
        """
        Генерация имени wx.BoxSizer.
        @return: Имя wx.BoxSizer.
        """
        return u'boxSizer%d' % wx.NewId()

    def genStaticTextName(self, res, prefix=u''):
        """
        Генерация имени компонента wx.StaticText.
        @param res: Ресурс генерации.
        @param prefix: Префикс имени.
        @return: Имя компонента wx.StaticText.
        """
        return prefix + res['name'].lower() + '_staticText'

    def genStaticTextLabel(self, res):
        """
        Генерация надписи компонента wx.StaticText.
        @param res: Ресурс генерации.
        @return: Строка надписи компонента wx.StaticText.
        """
        label = res.get('label', u'')
        description = res.get('description', u'')
        return label if label else description

    def genTextCtrlName(self, res):
        """
        Генерация имени компонента wx.TextCtrl.
        Компонент является редактируемым компонентом,
        поэтому его имя привязывается напрямую к имени
        редактируемого объекта.
        @param res: Ресурс генерации.
        @return: Имя компонента wx.TextCtrl.
        """
        return res['name']

    def genRadioBoxName(self, res):
        """
        Генерация имени компонента wx.RadioBox.
        @param res: Ресурс генерации.
        @return: Имя компонента wx.TextCtrl.
        """
        return res['name'] + '_radioBox'

    def genCheckBoxName(self, res, prefix=u''):
        """
        Генерация имени компонента wx.RadioBox.
        @param res: Ресурс генерации.
        @param prefix: Префикс имени.
        @return: Имя компонента wx.TextCtrl.
        """
        return prefix + res['name'] + '_checkBox'

    def genSpinCtrlName(self, res, prefix=u''):
        """
        Генерация имени компонента wx.SpinCtrl.
        Компонент является редактируемым компонентом,
        поэтому его имя привязывается напрямую к имени
        редактируемого объекта.
        @param res: Ресурс генерации.
        @param prefix: Префикс имени.
        @return: Имя компонента wx.SpinCtrl.
        """
        return prefix + res['name']

    def genDatePickerCtrlName(self, res, prefix=u''):
        """
        Генерация имени компонента wx.DatePickerCtrl.
        Компонент является редактируемым компонентом,
        поэтому его имя привязывается напрямую к имени
        редактируемого объекта.
        @param res: Ресурс генерации.
        @param prefix: Префикс имени.
        @return: Имя компонента wx.DatePickerCtrl.
        """
        return prefix + res['name']

    def genRequisiteEditBlock(self, requisite_res, is_editable=True):
        """
        Генерировать блок компонентов для редактирования реквизита.
        @param requisite_res: Ресурс реквизита.
        @param is_editable: Вкл. редактирование?
        @return: Текст блока.
        """
        txt = u''
        if requisite_res['type_val'] == 'T':
            label_name = self.genStaticTextName(requisite_res)
            label = self.genStaticTextLabel(requisite_res)
            edit_name = self.genTextCtrlName(requisite_res)
            txt = fb_form_template.FBP_TEXT_REQUISITE_CTRL_TEMPLATE % (self.genBoxSizerName(),
                                                                       label,
                                                                       label_name,
                                                                       edit_name)
        elif requisite_res['type_val'] == 'I':
            label_name = self.genStaticTextName(requisite_res)
            label = self.genStaticTextLabel(requisite_res)
            edit_name = self.genSpinCtrlName(requisite_res)
            txt = fb_form_template.FBP_INT_REQUISITE_CTRL_TEMPLATE % (self.genBoxSizerName(),
                                                                      label,
                                                                      label_name,
                                                                      edit_name)
        elif requisite_res['type_val'] == 'F':
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])

        elif requisite_res['type_val'] == 'DateTime':
            label_name = self.genStaticTextName(requisite_res)
            label = self.genStaticTextLabel(requisite_res)
            edit_name = self.genDatePickerCtrlName(requisite_res)
            txt = fb_form_template.FBP_DATE_REQUISITE_CTRL_TEMPLATE % (self.genBoxSizerName(),
                                                                       label,
                                                                       label_name,
                                                                       edit_name)
        else:
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        return txt

    def genNSICtrlConstructionTxt(self, requisite_res):
        """
        Генерация текста атрибута <construction> контрола справочника.
        @param requisite_res: Ресурс реквизита.
        @return: Текст <construction>.
        """
        psp_txt = str(requisite_res['nsi_psp'])
        psp_txt = psp_txt.replace('\'',  '& apos;')
        name = requisite_res['name']
        txt = u'self.%s = spravchoicecomboctrl.icSpravChoiceComboCtrl(parent=self.attr_scrollWin, id=wx.NewId(), component={ & apos; sprav & apos;: %s})' % (name, psp_txt)
        return txt

    def genNSIRequisiteEditBlock(self, requisite_res):
        """
        Генерировать блок компонентов для редактирования реквизита справочника.
        @param requisite_res: Ресурс реквизита.
        @return: Текст блока.
        """
        check_name = self.genCheckBoxName(requisite_res)
        label = self.genStaticTextLabel(requisite_res)
        edit_name = requisite_res['name']
        construction = self.genNSICtrlConstructionTxt(requisite_res)
        txt = fb_form_template.FBP_NSI_REQUISITE_CTRL_TEMPLATE % (self.genBoxSizerName(),
                                                                  label,
                                                                  check_name,
                                                                  construction,
                                                                  edit_name)
        return txt

    def genRequisiteBlock(self, requisite_res, is_editable=True):
        """
        Генерировать блок компонентов реквизита.
        @param requisite_res: Ресурс реквизита.
        @param is_editable: Вкл. редактирование?
        @return: Текст блока.
        """
        txt = u''
        if requisite_res['type'] == 'Requisite':
            # Обычный реквизит
            txt = self.genRequisiteEditBlock(requisite_res, is_editable)

        elif requisite_res['type'] == 'NSIRequisite':
            # Реквизит справочника
            txt = self.genNSIRequisiteEditBlock(requisite_res)
        elif requisite_res['type'] == 'REFRequisite':
            # Реквизит связи с бизнес объектом/документом.
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        elif requisite_res['type'] == 'TABRequisite':
            # Реквизит табличной части
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        else:
            # Не обрабатываем такие типы
            log.warning(u'Генерация форм не поддержиет реквизиты типа <%s>' % requisite_res['type'])
        return txt

    def genInitPanelName(self, obj_res):
        """
        Инициализация имени панели инициализации.
        @param obj_res: Ресурс объекта генерации.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icInit%sPanelProto' % name_txt

    def isResRequisite(self, requisite_res):
        """
        Проверка является ли ресурс ресурсом реквизита.
        @param requisite_res: Ресурс генерации
        @return: True/False.
        """
        return requisite_res['type'] in REQUISITE_TYPES

    def genInitPanel(self, obj_res):
        """
        Генерация панели инициализации объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        txt = u''
        for requisite in obj_res['child']:
            if not self.isResRequisite(requisite):
                log.debug(u'Ресурс объекта <%s> не является реквизитом' % requisite['name'])
                continue
            if not requisite['is_init']:
                log.debug(u'Реквизит <%s> не является инициализируемым. Пропуск генерации' % requisite['name'])
                continue
            txt += self.genRequisiteBlock(requisite, True)

        return fb_form_template.FBP_INIT_PANEL_TEMPLATE % (self.genInitPanelName(obj_res),
                                                           self.genBoxSizerName(),
                                                           txt)

    def genEditPanelName(self, obj_res):
        """
        Инициализация имени панели редактирования.
        @param obj_res: Ресурс объекта генерации.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icEdit%sPanelProto' % name_txt

    def genEditPanel(self, obj_res):
        """
        Генерация панели редактирования объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        txt = u''
        for requisite in obj_res['child']:
            if not self.isResRequisite(requisite):
                log.debug(u'Ресурс объекта <%s> не является реквизитом' % requisite['name'])
                continue
            if not requisite['is_edit']:
                log.debug(u'Реквизит <%s> не является редактируемым. Пропуск генерации' % requisite['name'])
                continue
            txt += self.genRequisiteBlock(requisite, True)

        return fb_form_template.FBP_EDIT_PANEL_TEMPLATE % (self.genEditPanelName(obj_res),
                                                           self.genBoxSizerName(),
                                                           txt)

    def genViewPanelName(self, obj_res):
        """
        Инициализация имени панели просмотра.
        @param obj_res: Ресурс объекта генерации.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icView%sPanelProto' % name_txt

    def genViewPanel(self, obj_res):
        """
        Генерация панели просмотра объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        txt = u''
        for requisite in obj_res['child']:
            if not self.isResRequisite(requisite):
                log.debug(u'Ресурс объекта <%s> не является реквизитом' % requisite['name'])
                continue
            if not requisite['is_view']:
                log.debug(u'Реквизит <%s> не является просматриваемым. Пропуск генерации' % requisite['name'])
                continue
            txt += self.genRequisiteBlock(requisite, False)

        return fb_form_template.FBP_VIEW_PANEL_TEMPLATE % (self.genViewPanelName(obj_res),
                                                           self.genBoxSizerName(),
                                                           txt)

    def genInitDlgName(self, obj_res):
        """
        Генерация имени диалогового окна инициализации.
        @param obj_res: Ресурс объекта генерации.
        @return: Имя диалогового окна.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icInit%sDlgProto' % name_txt

    def genInitDlgTitle(self, obj_res):
        """
        Генерация текста заголовка диалогового окна инициализации.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['description']

    def genInitPanelObjName(self, obj_res):
        """
        Генерация имени объекта панели инициализации в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'].lower() + u'_panel'

    def genInitPanelObjConstructionTxt(self, obj_res):
        """
        Генерация текста атрибута <construction> панели инициализации
        в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        panel_name = self.genInitPanelObjName(obj_res)
        panel_class_name = self.genInitPanelName(obj_res)
        return u'self.%s = %s(self)' % (panel_name, panel_class_name)

    def genInitDlg(self, obj_res):
        """
        Генерация диалогового окна инициализации объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        name = self.genInitDlgName(obj_res)
        title = self.genInitDlgTitle(obj_res)
        panel_name = self.genInitPanelObjName(obj_res)
        construction = self.genInitPanelObjConstructionTxt(obj_res)
        txt = fb_form_template.FBP_INIT_DLG_TEMPLATE % (name,
                                                        title,
                                                        construction,
                                                        panel_name)
        return txt

    def genEditDlgName(self, obj_res):
        """
        Генерация имени диалогового окна редактирования.
        @param obj_res: Ресурс объекта генерации.
        @return: Имя диалогового окна.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icInit%sDlgProto' % name_txt

    def genEditDlgTitle(self, obj_res):
        """
        Генерация текста заголовка диалогового окна редактирования.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['description']

    def genEditPanelObjName(self, obj_res):
        """
        Генерация имени объекта панели редактирования в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'].lower() + u'_panel'

    def genEditPanelObjConstructionTxt(self, obj_res):
        """
        Генерация текста атрибута <construction> панели редактирования
        в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        panel_name = self.genEditPanelObjName(obj_res)
        panel_class_name = self.genEditPanelName(obj_res)
        return u'self.%s = %s(self)' % (panel_name, panel_class_name)

    def genEditDlg(self, obj_res):
        """
        Генерация диалогового окна редактирования объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        name = self.genEditDlgName(obj_res)
        title = self.genEditDlgTitle(obj_res)
        panel_name = self.genEditPanelObjName(obj_res)
        construction = self.genEditPanelObjConstructionTxt(obj_res)
        txt = fb_form_template.FBP_EDIT_DLG_TEMPLATE % (name,
                                                        title,
                                                        construction,
                                                        panel_name)
        return txt

    def genViewDlgName(self, obj_res):
        """
        Генерация имени диалогового окна просмотра.
        @param obj_res: Ресурс объекта генерации.
        @return: Имя диалогового окна.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icInit%sDlgProto' % name_txt

    def genViewDlgTitle(self, obj_res):
        """
        Генерация текста заголовка диалогового окна просмотра.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['description']

    def genViewPanelObjName(self, obj_res):
        """
        Генерация имени объекта панели просмотра в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'].lower() + u'_panel'

    def genViewPanelObjConstructionTxt(self, obj_res):
        """
        Генерация текста атрибута <construction> панели просмотра
        в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        panel_name = self.genViewPanelObjName(obj_res)
        panel_class_name = self.genViewPanelName(obj_res)
        return u'self.%s = %s(self)' % (panel_name, panel_class_name)

    def genViewDlg(self, obj_res):
        """
        Генерация диалогового окна просмотра объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        name = self.genViewDlgName(obj_res)
        title = self.genViewDlgTitle(obj_res)
        panel_name = self.genViewPanelObjName(obj_res)
        construction = self.genViewPanelObjConstructionTxt(obj_res)
        txt = fb_form_template.FBP_VIEW_DLG_TEMPLATE % (name,
                                                        title,
                                                        construction,
                                                        panel_name)
        return txt

    def genRequisiteEditSearchBlock(self, requisite_res, is_editable=True):
        """
        Генерировать блок компонентов для редактирования реквизита для поиска.
        @param requisite_res: Ресурс реквизита.
        @param is_editable: Вкл. редактирование?
        @return: Текст блока.
        """
        txt = u''
        if requisite_res['type_val'] == 'T':
            label_name = self.genStaticTextName(requisite_res)
            label = self.genStaticTextLabel(requisite_res)
            edit_name = self.genTextCtrlName(requisite_res)
            radio_name = self.genRadioBoxName(requisite_res)
            txt = fb_form_template.FBP_TEXT_REQUISITE_SEARCH_TEMPLATE % (self.genBoxSizerName(),
                                                                         label,
                                                                         label_name,
                                                                         edit_name,
                                                                         radio_name)
        elif requisite_res['type_val'] == 'I':
            on_name = self.genCheckBoxName(requisite_res, u'on_')
            label = self.genStaticTextLabel(requisite_res)
            label1_name = self.genStaticTextName(requisite_res, u'start_')
            label2_name = self.genStaticTextName(requisite_res, u'end_')
            start_name = self.genSpinCtrlName(requisite_res, u'start_')
            end_name = self.genSpinCtrlName(requisite_res, u'end_')
            equal_name = self.genCheckBoxName(requisite_res, u'equal_')
            txt = fb_form_template.FBP_INT_REQUISITE_SEARCH_TEMPLATE % (self.genBoxSizerName(),
                                                                        label,
                                                                        on_name,
                                                                        label1_name,
                                                                        start_name,
                                                                        label2_name,
                                                                        end_name,
                                                                        equal_name)
        elif requisite_res['type_val'] == 'F':
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])

        elif requisite_res['type_val'] == 'DateTime':
            on_name = self.genCheckBoxName(requisite_res, u'on_')
            label = self.genStaticTextLabel(requisite_res)
            label1_name = self.genStaticTextName(requisite_res, u'start_')
            label2_name = self.genStaticTextName(requisite_res, u'end_')
            start_name = self.genDatePickerCtrlName(requisite_res, u'start_')
            end_name = self.genDatePickerCtrlName(requisite_res, u'end_')
            equal_name = self.genCheckBoxName(requisite_res, u'equal_')
            txt = fb_form_template.FBP_DATE_REQUISITE_SEARCH_TEMPLATE % (self.genBoxSizerName(),
                                                                         label,
                                                                         on_name,
                                                                         label1_name,
                                                                         start_name,
                                                                         label2_name,
                                                                         end_name,
                                                                         equal_name)
        else:
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        return txt

    def genNSIRequisiteEditSearchBlock(self, requisite_res):
        """
        Генерировать блок компонентов для редактирования реквизита справочника для поиска.
        @param requisite_res: Ресурс реквизита.
        @return: Текст блока.
        """
        return self.genNSIRequisiteEditBlock(requisite_res)

    def genRequisiteSearchBlock(self, requisite_res, is_editable=True):
        """
        Генерировать блок компонентов реквизита для поиска.
        @param requisite_res: Ресурс реквизита.
        @param is_editable: Вкл. редактирование?
        @return: Текст блока.
        """
        txt = u''
        if requisite_res['type'] == 'Requisite':
            # Обычный реквизит
            txt = self.genRequisiteEditSearchBlock(requisite_res, is_editable)

        elif requisite_res['type'] == 'NSIRequisite':
            # Реквизит справочника
            txt = self.genNSIRequisiteEditSearchBlock(requisite_res)
        elif requisite_res['type'] == 'REFRequisite':
            # Реквизит связи с бизнес объектом/документом.
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        elif requisite_res['type'] == 'TABRequisite':
            # Реквизит табличной части
            log.warning(u'Генерация не реализована для реквизита типа <%s>' % requisite_res['type'])
        else:
            # Не обрабатываем такие типы
            log.warning(u'Генерация форм не поддержиет реквизиты типа <%s>' % requisite_res['type'])
        return txt

    def genChoicePanelName(self, obj_res):
        """
        Инициализация имени панели поиска/выбора.
        @param obj_res: Ресурс объекта генерации.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icChoice%sPanelProto' % name_txt

    def genChoicePanel(self, obj_res):
        """
        Генерация панели поиска и выбора объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        txt = u''
        for requisite in obj_res['child']:
            if not self.isResRequisite(requisite):
                log.debug(u'Ресурс объекта <%s> не является реквизитом' % requisite['name'])
                continue
            if not requisite['is_search']:
                log.debug(u'Реквизит <%s> не является критерием поиска. Пропуск генерации' % requisite['name'])
                continue
            txt += self.genRequisiteSearchBlock(requisite, True)

        return fb_form_template.FBP_CHOICE_PANEL_TEMPLATE % (self.genChoicePanelName(obj_res),
                                                             self.genBoxSizerName(),
                                                             txt)

    def genChoiceDlgName(self, obj_res):
        """
        Генерация имени диалогового окна поиска/выбора.
        @param obj_res: Ресурс объекта генерации.
        @return: Имя диалогового окна.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icChoice%sDlgProto' % name_txt

    def genChoiceDlgTitle(self, obj_res):
        """
        Генерация текста заголовка диалогового окна поиска/выбора.
        @param obj_res: Ресурс объекта генерации.
        """
        return u'Выбор. ' + obj_res['description']

    def genChoicePanelObjName(self, obj_res):
        """
        Генерация имени объекта панели поиска/выбора в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'].lower() + u'_panel'

    def genChoicePanelObjConstructionTxt(self, obj_res):
        """
        Генерация текста атрибута <construction> панели поиска/выбора
        в диалоговом окне.
        @param obj_res: Ресурс объекта генерации.
        """
        panel_name = self.genChoicePanelObjName(obj_res)
        panel_class_name = self.genChoicePanelName(obj_res)
        return u'self.%s = %s(self)' % (panel_name, panel_class_name)

    def genChoiceDlg(self, obj_res):
        """
        Генерация диалогового окна поиска и выбора объекта.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        name = self.genChoiceDlgName(obj_res)
        title = self.genChoiceDlgTitle(obj_res)
        panel_name = self.genChoicePanelObjName(obj_res)
        construction = self.genChoicePanelObjConstructionTxt(obj_res)
        txt = fb_form_template.FBP_CHOICE_DLG_TEMPLATE % (name,
                                                          title,
                                                          construction,
                                                          panel_name)
        return txt

    def genBrowsePanelName(self, obj_res):
        """
        Генерация имени панели просмотра/фильтрации/управления списком объектов.
        @param obj_res: Ресурс объекта генерации.
        """
        name = obj_res['name']
        name_txt = u''.join([word.capitalize() for word in name.split(u'_')])
        return u'icBrowse%sPanelProto' % name_txt

    def genFilterCtrlName(self, obj_res):
        """
        Генерация имени контрола фильтра объектов.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'] + '_filter_ctrl'

    def genFilterCtrlConstructionTxt(self, obj_res):
        """
        Генерация атрибута <construction> контрола фильтра объектов.
        @param obj_res: Ресурс объекта генерации.
        """
        name = self.genFilterCtrlName(obj_res)
        return u'self.%s = icfilterchoicectrl.icFilterChoiceCtrl(parent=self)' % name

    def genObjListCtrlName(self, obj_res):
        """
        Генерация имени контрола списка объектов.
        @param obj_res: Ресурс объекта генерации.
        """
        return obj_res['name'] + '_list'

    def genObjListCtrlConstructionTxt(self, obj_res):
        """
        Генерация атрибута <construction> контрола списка объектов.
        @param obj_res: Ресурс объекта генерации.
        """
        name = self.genObjListCtrlName(obj_res)
        return u'self.%s = icsimplegrplistview.icSimpleGroupListView(parent=self)' % name

    def genBrowsePanel(self, obj_res):
        """
        Генерация панели просмотра/фильтрации/управления списком объектов.
        @param obj_res: Ресурс объекта генерации.
        @return: Сгенерированный текст.
        """
        panel_name = self.genBrowsePanelName(obj_res)
        filter_name = self.genFilterCtrlName(obj_res)
        filter_construction = self.genFilterCtrlConstructionTxt(obj_res)
        obj_list_name = self.genObjListCtrlName(obj_res)
        obj_list_construction = self.genObjListCtrlConstructionTxt(obj_res)
        return fb_form_template.FBP_BROWSE_PANEL_TEMPLATE % (panel_name,
                                                             filter_construction,
                                                             filter_name,
                                                             obj_list_construction,
                                                             obj_list_name)


def gen_wxfb_prj(parent=None, resource=None, fbp_filename=None):
    """
    Функция запуска генерации форм wxFormBuilder бизнес объекта/документа.
    @param parent: Родительское окно.
    @param resource: Ресурс, по которому происходит генерация
    @param fbp_filename: Файл проекта wxFormBuilder для сохранения.
    @return: True - генерация прошла успешно.
        False - Возникла какая-то ошибка.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    if resource is None:
        log.warning(u'Не определен ресурс генерации форм wxFormBuilder')
        return False

    if fbp_filename is None:
        fbp_filename = ic_dlg.icFileDlg(parent,
                                        u'Выбор файла проекта wxFormBuilder для генерации',
                                        u'wxFormBuilder project (*.fbp)|*.fbp')

    if not fbp_filename:
        log.warning(u'Не определен файл проекта wxFormBuilder для генерации форм')
        return False

    if os.path.exists(fbp_filename):
        if not ic_dlg.icAskBox(u'ВНИМАНИЕ', u'Файл <%s> уже существует. Перезаписать его?' % fbp_filename):
            # Не надо перезаписывать,
            # тогда нет смысла и генерировать его
            return False

    generator = icWxFBPrjGenerator()
    if not generator.isParsed(resource):
        ic_dlg.icWarningBox(u'ОШИБКА', u'Тип ресурса не поддерживается генератором форм wxFormBuilder')
        return False

    generator.setResource(resource)
    generator.setGenFilename(fbp_filename)
    txt = generator.genPrj()
    return generator.savePrj(txt)
