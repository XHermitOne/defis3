#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Окно редактирования/просмотра окружения/контекста проекта.
"""

import wx
from . import environment_edit_dlg_proto

from ic.engine import glob_functions
from ic.engine import form_manager

from ic.log import log
from ic.dlg import dlgfunc


__version__ = (0, 1, 1, 1)


class icEnvironmentEditDlg(environment_edit_dlg_proto.icEditEnvironmentDlgProto,
                           form_manager.icFormManager):
    """
    Окно редактирования/просмотра окружения/контекста проекта.
    """
    def __init__(self, context=None, project_root=None, *args, **kwargs):
        """
        Конструктор.
        """
        environment_edit_dlg_proto.icEditEnvironmentDlgProto.__init__(self, *args, **kwargs)

        self. init()

        if context is None:
            context = glob_functions.getKernel().GetContext()
        self.context = context

        self.set_base_variables()

        self._project_root = project_root
        if self._project_root:
            self.set_ext_variables()

    def init(self):
        """
        Инициализация формы.
        """
        self.init_ctrl()

    def init_ctrl(self):
        """
        Инициализация контролов формы.
        """
        self.setColumns_list_ctrl(ctrl=self.base_listCtrl, cols=(dict(label=u'Наименование', width=200),
                                                                 dict(label=u'Значение', width=500),
                                                                 dict(label=u'Доступ', width=100),
                                                                 dict(label=u'Ключ блокировки', width=100)))

        self.setColumns_list_ctrl(ctrl=self.ext_listCtrl, cols=(dict(label=u'Наименование', width=200),
                                                                dict(label=u'Значение', width=500)))

    def set_base_variables(self, variables=None):
        """
        Установить в списке основные переменные окружения для просмотра.
        :param variables: Список переменных окружения.
            Если не определен, то получается автоматически из контекста.
        """
        if variables is None:
            variables = self._convert_context(self.context)

        rows = [(var['__record__'][0],
                 var['__record__'][1],
                 var['__record__'][2],
                 var['__record__'][3]) for var in variables]
        rows.sort()
        self.setRows_list_ctrl(ctrl=self.base_listCtrl, rows=rows)

    def set_ext_variables(self, variables=None):
        """
        Установить в списке дополнительные переменные окружения проекта.
        :param variables: Список дополнительных переменных окружения.
            Если не определен, то получается автоматически из окружения проекта.
        """
        if variables is None:
            variables = self._project_root.prj_res_manager.getPrjEnv()
        rows = list(variables.items())
        rows.sort()
        self.setRows_list_ctrl(ctrl=self.ext_listCtrl, rows=rows)

    def _convert_context(self, context):
        """
        Переконвертировать контекст в формат дерева.
        """
        result = []
        for name in context.keys():
            tree_item = {}
            context_item = context[name]
            tree_item['name'] = name
            tree_item['__record__'] = [name, str(context_item), '', '']
            result.append(tree_item)
        return result

    def design(self):
        """
        Открыть диалоговое окно для редактирования.
        """
        self.ShowModal()

    def onAddToolClicked(self, event):
        """
        Обработчик добавления новой записи в гриде дополнительных атрибутов проекта.
        """
        name = dlgfunc.getTextEntryDlg(parent=self.ext_listCtrl,
                                       prompt_text=u'Новая переменная окружения',
                                       title=u'ОКРУЖЕНИЕ')
        if name:
            value = dlgfunc.getTextEntryDlg(parent=self.ext_listCtrl,
                                            prompt_text=u'Значение переменной',
                                            title=u'ОКРУЖЕНИЕ')
            if value is not None:
                self.appendRow_list_ctrl(ctrl=self.ext_listCtrl, row=(name, value))
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Обработчик удаления выбранной записи в гриде дополнительных атрибутов проекта.
        """
        del_idx = self.getItemSelectedIdx(obj=self.ext_listCtrl)
        if del_idx > 0:
            row = self.getRow_list_ctrl(ctrl=self.ext_listCtrl)
            if row:
                name, value = row
                if dlgfunc.openAskBox(title=u'УДАЛЕНИЕ',
                                      prompt_text=u'Удалить переменную <%s> из окружения проекта?' % name):
                    self.removeRow_list_ctrl(ctrl=self.ext_listCtrl, item=del_idx)
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        Обработчик сохранения отредактированных значений.
        """
        rows = self.getRows_list_ctrl(ctrl=self.ext_listCtrl)

        env_dict = None
        if rows:
            env_dict = dict([(str(name), val) for name, val in rows if name])
        if self._project_root and env_dict:
            self._project_root.prj_res_manager.setPrjEnv(env_dict)
            self._project_root.save()
        event.Skip()
        
    def onCloseButtonClick(self, event):
        """
        Обработчик кнопки закрытия диалогового окна.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()
