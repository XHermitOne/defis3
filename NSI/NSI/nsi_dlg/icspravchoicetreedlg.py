#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Диалоговая форма выбора элемента/код справочника.
Все данные представлены в древовидном представлении.
"""

import operator
import wx

from . import nsi_dialogs_proto
from ic.log import log
from ic.bitmap import ic_bmp
from ic.dlg import ic_dlg
from . import icspraveditdlg
from ic.utils import ic_str
from ic.utils import wxfunc
from ic.engine import form_manager

# Версия
__version__ = (0, 0, 8, 4)

# Текст фиктивного элемента дерева
TREE_ITEM_LABEL = u'...'

# Кеш диалоговых окон для оптимизации вызова выбора из справочника
CHOICE_DLG_CACHE = dict()

SORT_REVERSE_SIGN = '-'


class icSpravChoiceTreeDlg(nsi_dialogs_proto.icSpravChoiceTreeDlgProto,
                           form_manager.icFormManager):
    """
    Диалоговая форма выбора элемента/код справочника.
    """
    
    def __init__(self, nsi_sprav=None, default_selected_code=None,
                 *args, **kwargs):
        """
        Конструктор.
        @param nsi_sprav: Объект справочника.
        @param default_selected_code: Выбираемый по умолчанию код.
        """
        nsi_dialogs_proto.icSpravChoiceTreeDlgProto.__init__(self, *args, **kwargs)

        # Объект справочника
        self.sprav = nsi_sprav
        # Список имен полей таблицы справочника, отображающихся в
        # контроле дерева справочника в виде колонок
        self.sprav_field_names = ['cod', 'name']

        # Список имен полей таблицы справочника, по которым
        # можно производить поиск
        self.sprav_search_field_names = ['name', 'cod']

        # Найденые коды, соответствующие строке поиска
        self.search_codes = list()
        # Текущий найденный код в списке найденных кодов
        self.search_code_idx = 0
        # Признак необходимости обновить список искомых кодов
        self.not_actual_search = False

        # Имя колонки для сортировки
        self.sort_column = None

        # Индексы картинок указания сортировки
        self.sort_ascending_img = -1
        self.sort_descending_img = -1

        # ВНИМАНИЕ! Необходимо запоминать объект библиотеки образов
        # Иначе при использовании будет возникать <Segmentation fault>
        self.sprav_treeListCtrl_img_list = None

        # self.init()

        self.default_selected_code = default_selected_code

        # Всплывающее окно для отображения доп информации
        self.popup_win = None

        # self.sprav_treeCtrl.Bind( wx.EVT_TREE_ITEM_COLLAPSED, self.onSpravTreeItemCollapsed )
        # self.sprav_treeListCtrl.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onSpravTreeItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onSpravTreeItemExpanded)
        # self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onSpravTreeItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)

        # Клик мыши на заголовочной части
        header_list_ctrl = self.sprav_treeListCtrl.GetHeaderWindow()
        header_list_ctrl.Bind(wx.EVT_LEFT_DOWN, self.onHeaderMouseLeftClick)

    def onInitDlg(self, event):
        """
        Инициализация диалогового окна.
        """
        # log.debug(u'onInit')
        if self.default_selected_code:
            log.info(u'По умолчанию выбираем код <%s> в справочнике [%s]' % (self.default_selected_code,
                                                                             self.sprav.getName()))
            if self.sprav.isCod(self.default_selected_code):
                self.select_sprav_tree_item(self.default_selected_code)
            else:
                log.warning(u'Код <%s> не найден в справочнике [%s]' % (self.default_selected_code,
                                                                        self.sprav.getName()))
        event.Skip()

    def onCloseDlg(self, event):
        """
        Закрытие диалогового окна.
        """
        self.hidePopupInfo()
        event.Skip()

    def init(self, fields, search_fields):
        """
        Функция инициализации диалогового окна.
        @param fields: Список имен полей справочника, которые
            необходимо отобразить в контроле дерева.
            Если поля не указываются, то отображаются только
            <Код> и <Наименование>.
        @param search_fields: Поля по которым производиться поиск.
        """
        self.init_images()

        self.init_columns(*fields)
        self.init_search(*search_fields)
        self.set_sprav_tree()

        # Проверка разрешения у пользователя на редактирование справочника
        can_edit = self.sprav.canEdit()
        self.edit_button.Enable(can_edit)

    def init_images(self):
        """
        Инициализация образов контролов.
        """
        # Используем штатную картинку wx.ArtProvider
        #   V
        if False:
            # <wx.Tool>
            bmp = ic_bmp.createLibraryBitmap('magnifier-left.png')
            tool_id = self.search_tool.GetId()
            # ВНИМАНИЕ! Для смены образа инструмента не надо использовать
            # метод инструмента <tool.SetNormalBitmap(bmp)> т.к. НЕ РАБОТАЕТ!
            # Для этого вызываем метод панели инструметнтов
            # <toolbar.SetToolNormalBitmap(tool_id, bmp)>
            self.search_toolBar.SetToolNormalBitmap(tool_id, bmp)
            # Внимание! После изменения образов инструментов
            # у панели инструментов надо вызвать <Realize>
            self.search_toolBar.Realize()

        # Образы контрола списка справочника
        if self.sprav_treeListCtrl_img_list is None:
            img_list = wx.ImageList(ic_bmp.DEFAULT_LIB_BMP_SIZE[0],
                                    ic_bmp.DEFAULT_LIB_BMP_SIZE[1])
            # log.debug(u'Создана библиотека образов')

            self.sort_ascending_img = img_list.Add(ic_bmp.createLibraryBitmap('bullet_arrow_up.png'))
            self.sort_descending_img = img_list.Add(ic_bmp.createLibraryBitmap('bullet_arrow_down.png'))

            self.sprav_treeListCtrl.SetImageList(img_list)
            # ВНИМАНИЕ! Необходимо запоминать объект библиотеки образов
            # Иначе при использовании будет возникать <Segmentation fault>
            self.sprav_treeListCtrl_img_list = img_list
            # log.debug(u'Библиотека образов прикреплена к контролу списка спраавочника')

    def get_field_label(self, field):
        """
        Определить надпись соответствующую полю по его описанию.
        @param field: Описание поля.
        @return: Строка надписи в юникоде.
        """
        if field is None:
            return TREE_ITEM_LABEL
        label = field['label'] if field.get('label', None) else \
            (field['description'] if field.get('description', None) else field['name'])
        return ic_str.toUnicode(label)

    def init_columns(self, *fields):
        """
        Инициализация колонок контрола дерева справочника.
        @param fields: Список имен полей справочника, которые
            необходимо отобразить в контроле дерева.
            Если поля не указываются, то отображаются только 
            <Код> и <Наименование>.
        """
        field_names = ['cod', 'name']
        if fields:
            field_names += fields
        self.sprav_field_names = field_names
            
        if self.sprav is None:
            log.warning(u'Не определен справочник для выбора кода')
            return
        
        tab = self.sprav.getTable()
        # Словарь спецификаций полей таблицы справочника
        field_dict = dict([(field['name'], field) for field in tab.getResource()['child']])
        
        for field_name in field_names:
            field = field_dict.get(field_name, None)
            if field:
                column_label = self.get_field_label(field)
                self.sprav_treeListCtrl.AddColumn(column_label)
            else:
                log.warning(u'Не найдено поле <%s> в описании таблицы <%s>' % (field_name, tab.name))

        # Обновить отсортированные колонки
        self.refreshSortColumn(self.sort_column)

    def init_search(self, *search_fields):
        """
        Инициализация контролов выбора поиска по полям справочника.
        @param search_fields: Поля по которым производиться поиск.
        """
        # По умолчанию делаем поиск по наименованию
        field_names = ['name', 'cod']
        if search_fields:
            field_names += search_fields
        self.sprav_search_field_names = field_names

        if self.sprav is None:
            log.warning(u'Не определен справочник для выбора кода')
            return

        tab = self.sprav.getTable()
        # Словарь спецификаций полей таблицы справочника
        field_dict = dict([(field['name'], field) for field in tab.getResource()['child']])

        choices = list()
        for field_name in field_names:
            field = field_dict.get(field_name, None)
            if field:
                choice_label = self.get_field_label(field)
                choices.append(choice_label)
            else:
                log.warning(u'Не найдено поле <%s> в описании таблицы <%s>' % (field_name, tab.name))
        self.search_field_choice.Clear()
        self.search_field_choice.AppendItems(choices)
        self.search_field_choice.Select(0)

    def set_sprav_tree(self, is_progress=True, sort_column=None):
        """
        Установить данные дерева справочника.
        @param is_progress: Вывести прогрессбар построения дерева справочника?
        @param sort_column: Наименования колонки сортировки.
        """
        # Добавить корневой элемент дерева справочника
        sprav_res = self.sprav.GetResource() 
        sprav_title = sprav_res['description'] if sprav_res['description'] else sprav_res['name']
        # В случае многострочных наименования выделять только первую строку
        sprav_title = [line.strip() for line in sprav_title.split(u'\n')][0]

        self.root = self.sprav_treeListCtrl.AddRoot(sprav_title)
        
        if self.sprav.isEmpty():
            # Справочник пустой. Заполнять не надо
            return

        if sort_column is None:
            sort_column = self.sort_column
        self.set_sprav_level_tree(self.root, is_progress=is_progress, sort_column=sort_column)

        # Развернуть корневой элемент
        self.sprav_treeListCtrl.Expand(self.root)

    def refresh_sprav_tree(self, is_progress=True, sort_column=None):
        """
        Обновить данные дерева справочника.
        @param is_progress: Вывести прогрессбар построения дерева справочника?
        @param sort_column: Наименования колонки сортировки.
        """
        # Запомнить выделенный элемент дерева
        selected_code = self.getSelectedCode()

        # Сначала удалить все элементы дерева
        self.sprav_treeListCtrl.DeleteAllItems()

        # Добавить корневой элемент дерева справочника
        sprav_res = self.sprav.GetResource()
        sprav_title = sprav_res['description'] if sprav_res['description'] else sprav_res['name']
        # В случае многострочных наименования выделять только первую строку
        sprav_title = [line.strip() for line in sprav_title.split(u'\n')][0]

        self.root = self.sprav_treeListCtrl.AddRoot(sprav_title)

        if self.sprav.isEmpty():
            # Справочник пустой. Заполнять не надо
            return

        if sort_column is None:
            sort_column = self.sort_column
        self.set_sprav_level_tree(self.root, is_progress=is_progress, sort_column=sort_column)

        # Выделить запомненный элемент
        if selected_code is not None:
            self.select_sprav_tree_item(selected_code)
        else:
            self.sprav_treeListCtrl.Expand(self.root)

    def set_sprav_level_tree(self, parent_item, sprav_code=None,
                             is_progress=True, sort_column=None):
        """
        Добавить уровень дерева справочника.
        @param parent_item: Элемент дерева, в который происходит добавление.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @param sort_column: Наименования колонки сортировки.
        """
        # Добавить первый уровень дерева справочника
        sprav_storage = self.sprav.getStorage()
        level_data = sprav_storage.getLevelTable(sprav_code)
        # Отсортировать
        if sort_column is not None:
            log.debug(u'Установлена сортировка по колонке <%s>' % sort_column)
            level_data = self.sort_sprav_recordset(level_data, sort_column=sort_column)

        if level_data is None:
            log.warning(u'Нет данных справочника')
            return

        sprav_res = self.sprav.GetResource()
        sprav_title = sprav_res['description'] if sprav_res['description'] else sprav_res['name']
        label = u'Открытие справочника <%s>' % sprav_title
        len_level_data = len(level_data) if isinstance(level_data, list) else level_data.rowcount
        if is_progress:
            ic_dlg.icOpenProgressDlg(self, u'Справочник', label, 0, len_level_data)

        try:
            for i, record in enumerate(level_data):
                self.set_sprav_tree_item(parent_item, record)

                if is_progress:
                    ic_dlg.icUpdateProgressDlg(i + 1, label)

            # Установить авто ширину колонок
            for i, field_name in enumerate(self.sprav_field_names):
                self.sprav_treeListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        except:
            log.fatal(u'Ошибка построения дерева справочника')

        if is_progress:
            ic_dlg.icCloseProgressDlg()

    def get_sort_field(self, sort_column='name'):
        """
        Определить имя поля сортировки по указанию имени/индексу 
        колонки сортировки.
        @param sort_column: Указание имени/индекса колонки сортировки.
        @return: Имя поля сортировки.
            Или None в случае ошибки.
        """
        sort_field = None
        if isinstance(sort_column, int):
            # ВНИМАНИЕ! Увеличение на 1 сделано для того чтобы учесть
            # первую колонку с индексом 0. Т.к. -0 нет.
            #                      V
            i = abs(sort_column) - 1
            sort_field = self.sprav_field_names[i]
        elif isinstance(sort_column, str) or isinstance(sort_column, unicode):
            if sort_column.startswith(SORT_REVERSE_SIGN):
                sort_field = sort_column[1:]
            else:
                sort_field = sort_column
            if sort_field not in self.sprav_field_names:
                log.warning(u'Сортировка.Поле <%s> не найдено среди %s.' % (sort_field, self.sprav_field_names))
                sort_field = None
        else:
            log.warning(u'Ошибка типа поля/колонки сортировки <%s>' % type(sort_column))
        return sort_field

    def get_sort_field_idx(self, sort_column='name'):
        """
        Определить индекс поля сортировки по указанию имени/индексу 
        колонки сортировки.
        @param sort_column: Указание имени/индекса колонки сортировки.
        @return: Индекс поля сортировки.
            Или None в случае ошибки.
        """
        sort_field_idx = None
        if isinstance(sort_column, int):
            # ВНИМАНИЕ! Увеличение на 1 сделано для того чтобы учесть
            # первую колонку с индексом 0. Т.к. -0 нет.
            #                         V
            return abs(sort_column) - 1
        elif isinstance(sort_column, str) or isinstance(sort_column, unicode):
            if sort_column.startswith(SORT_REVERSE_SIGN):
                sort_field = sort_column[1:]
            else:
                sort_field = sort_column
            if sort_field in self.sprav_field_names:
                sort_field_idx = self.sprav_field_names.index(sort_field)
            else:
                log.warning(u'Сортировка.Поле <%s> не найдено среди %s.' % (sort_field, self.sprav_field_names))
                sort_field_idx = None
        else:
            log.warning(u'Ошибка типа поля/колонки сортировки <%s>' % type(sort_column))
        return sort_field_idx

    def is_reverse_sort(self, sort_column='name'):
        """
        Проверка на обратную сортировку.
        @param sort_column: Указание имени/индекса колонки сортировки.
        @return: True - Обратная сортировка / False - Обычная сортировка по возрастанию. 
        """
        if isinstance(sort_column, int):
            return sort_column < 0
        elif isinstance(sort_column, str) or isinstance(sort_column, unicode):
            return sort_column.startswith(SORT_REVERSE_SIGN)
        # По умолчанию обычная сортировка по возрастанию
        return False

    def sort_sprav_recordset(self, recordset, sort_column='name'):
        """
        Отсортировать список записей по колонке.
        @param recordset: Список записей.
        @param sort_column: Поле сортировки.
            Поле может задаваться по имени или по индексу.
            Если перед именем стоит <-> или индекс отрицательный, 
            то считается что сортировка в обратном порядке.
            Например:
            'name' - сортировка по полю 'name'
            '-name' - сортировка по полю 'name' в обратном порядке
            1 - сортировка по полю с индексом 0
            -1 -  сортировка по полю с индексом 0 в обратном порядке.
            Соответственно если запись задается словарем, 
            то в качестве поля указываем имя поля.
            Если запись задается списком, то поле указываем индексом.
        @return: Отсортированный список записей.
        """
        if not isinstance(recordset, list):
            # Не списки мы не можем отсортировать
            log.warning(u'Ошибка типа сортируемых записей <%s>' % type(recordset))
            return recordset

        if not recordset:
            # Если список записей пустой, то и сортировать нет смысла
            return recordset

        sort_field = self.get_sort_field(sort_column)
        log.debug(u'Поле сортировки <%s>' % sort_field)

        # Непосренственно сама сортировка
        if sort_field is not None:
            # Анализ производим по первой записи
            first_record = recordset[0]
            # log.debug(u'Анализ первой строки %s\tПоля: %s\tТип записи: %s' % (str(first_record),
            #                                                                   self.sprav_field_names, type(first_record)))
            if isinstance(first_record, dict):
                # Сортировка происходит сразу по нескольким полям
                # Определим последовательность полей сортировки
                # (исключаем поле кода только если явно по нему сортируем)
                field_sequence = [sort_field] + [fld for fld in self.sprav_field_names if fld not in ('cod', sort_field)]
                is_reverse = self.is_reverse_sort(sort_column)
                # log.debug(u'Sort columns: %s\tis reverse: %s' % (field_sequence, is_reverse))
                # ВНИМАНИЕ! Здесь используется operator.itemgetter
                # для определения порядка группировки сортировки
                # operator.itemgetter('a', 'b', 'c') аналог
                # lambda rec: (rec['a'], rec['b'], rec['c'])
                # но выполняется быстрее
                new_recordset = sorted(recordset,
                                       key=operator.itemgetter(*field_sequence),
                                       reverse=is_reverse)
            elif isinstance(first_record, list) or isinstance(first_record, tuple):
                # ВНИМАНИЕ! Получить индексы полей рекордсета.
                # Рекордсет получаем из справочника и порядок полей может не
                # соответствовать порядку отображаемых полей
                sort_field_idx = self.get_sort_field_idx(sort_column)
                # Сортировка происходит сразу по нескольким полям
                # Определим последовательность полей сортировки
                # (исключаем поле кода только если явно по нему сортируем)
                field_sequence_idx = [sort_field_idx] + [i for i in range(len(self.sprav_field_names)) if i not in (0, sort_field_idx)]
                field_names = self.sprav.getStorage().getSpravFieldNames()
                new_field_sequence_idx = [field_names.index(self.sprav_field_names[i]) for i in field_sequence_idx]
                is_reverse = self.is_reverse_sort(sort_column)
                # log.debug(u'Sort columns: %s\tis reverse: %s' % (new_field_sequence_idx, is_reverse))
                new_recordset = sorted(recordset,
                                       key=operator.itemgetter(*new_field_sequence_idx),
                                       reverse=is_reverse)
            else:
                log.warning(u'Сортировка. Не поддерживаемый тип записей <%s>' % type(first_record))
                new_recordset = recordset

            return new_recordset
        # При возникновении какой-либо ошибки возвращаем
        # не отсортированный набор записей
        return recordset

    def set_sprav_tree_item(self, parent_item, record):
        """
        Установить элемент дерева справочника.
        @param parent_item: Родительский элемент дерева.
        @param record: Запись справочника, ассоциируемая с элементом.
        """
        # Запись в виде словаря
        rec_dict = self.sprav.getStorage()._getSpravFieldDict(record)
        code = rec_dict['cod']
        item = self.sprav_treeListCtrl.AppendItem(parent_item, code)
        self.sprav_treeListCtrl.SetPyData(item, rec_dict)
        # Заполнение колонок
        for i, field_name in enumerate(self.sprav_field_names[1:]):
            value = rec_dict.get(field_name, u'')
            # Проверка типов
            if value is None:
                value = u''
            elif type(value) not in (str, unicode):
                value = str(value)
            self.sprav_treeListCtrl.SetItemText(item, value, i+1)            
        
        if self.sprav.isSubCodes(code):
            # Есть подкоды. Для отображения + в контроле дерева
            # необходиом добавить фиктивный элемент
            self.sprav_treeListCtrl.AppendItem(item, TREE_ITEM_LABEL)

        # !!! ВАЛИТЬСЯ! Не испльзовать этот код !!!!
        # Если текущий код находится в списке найденных, то подсветить его
        # if self.search_codes and code in self.search_codes:
        #     self.sprav_treeListCtrl.SetItemBackgroundColour(item, wx.SYS_COLOUR_GRAYTEXT)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def find_tree_child_item(self, item_text, cur_item=None):
        """
        Поиск дочернего элемента дерева по тексту.
        @param item_text: Текст элемента дерева.
        """
        if cur_item is None:
            cur_item = self.root
            
        find_item = None
        child_item, cookie = self.sprav_treeListCtrl.GetFirstChild(cur_item)
        while child_item.IsOk():
            if item_text == self.sprav_treeListCtrl.GetItemText(child_item):
                find_item = child_item
                break
            child_item, cookie = self.sprav_treeListCtrl.GetNextChild(cur_item, cookie)
        return find_item

    def init_level_tree(self, item):
        """
        Проинициализировать ветку элемента дерева.
        @param item: Элемент дерева.
        """
        find_item = self.find_tree_child_item(TREE_ITEM_LABEL, item)
        if find_item:
            self.sprav_treeListCtrl.Delete(find_item)

        # Заполнение пустого уровня
        if not self.sprav_treeListCtrl.ItemHasChildren(item):
            record = self.sprav_treeListCtrl.GetPyData(item)
            code = record['cod']
            self.set_sprav_level_tree(item, code)
  
    def find_sprav_tree_item(self, parent_item, sprav_code=None):
        """
        Поиск элемента дерева справочника по коду справочника.
        @param parent_item: Родительский элемент дерева.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @return: Найденный элемент дерева или None, если элемент не найден. 
        """
        # Поискать код в текущем элементе
        record = self.sprav_treeListCtrl.GetPyData(parent_item)
        if record:
            if sprav_code == record['cod']:
                return parent_item
        
        # Поиск в дочерних элементах
        find_result = None
        child_item, cookie = self.sprav_treeListCtrl.GetFirstChild(parent_item)
        while child_item.IsOk():
            record = self.sprav_treeListCtrl.GetPyData(child_item)
            if record:
                if sprav_code == record['cod']:
                    find_result = child_item
                    break
            child_item, cookie = self.sprav_treeListCtrl.GetNextChild(parent_item, cookie)
        
        # На этом уровне ничего не нашли
        # необходимо спуститься на уровень ниже
        if not find_result:
            child_item, cookie = self.sprav_treeListCtrl.GetFirstChild(parent_item)
            while child_item.IsOk():
                self.init_level_tree(child_item)
                find_result = self.find_sprav_tree_item(child_item, sprav_code)
                if find_result:
                    break
                child_item, cookie = self.sprav_treeListCtrl.GetNextChild(parent_item, cookie)

        if find_result:
            # Если найти в этой ветке то распахнуть ее
            self.sprav_treeListCtrl.Expand(parent_item)
            
        return find_result
  
    def select_sprav_tree_item(self, sprav_code, parent_item=None):
        """
        Найти и выбрать элемент дерева справочника по коду справочника.
        @param sprav_code: Код справочнка, ассоциируемый с элементом дерева.
        @return: Найденный элемент дерева или None, если элемент не найден. 
        """
        if parent_item is None:
            parent_item = self.root
        
        item = self.find_sprav_tree_item(parent_item, sprav_code)
        if item:
            # Выбрать элемент дерева
            self.sprav_treeListCtrl.SelectItem(item)
            # Прокрутить скролинг до выбранного элемента дерева
            self.sprav_treeListCtrl.ScrollTo(item)
            return item
        return None        

    def getSelectedCode(self):
        """
        Выбранный код справочника.
        """
        item = self.sprav_treeListCtrl.GetSelection()
        if item and item.IsOk():
            record = self.sprav_treeListCtrl.GetPyData(item)
            return record.get('cod', None) if record is not None else None
        return None
    
    def edit_sprav(self):
        """
        Запуск редактирования справочника.
        """
        return icspraveditdlg.edit_sprav_dlg(parent=self, nsi_sprav=self.sprav)
        
    def onEditButtonClick(self, event):
        """
        Обработчик кнопки <Редактирование...>
        """
        ok_edit = self.edit_sprav()
        if ok_edit:
            # Если редактирование пршло успешно, тогда обновить 
            # дерево справочника
            self.sprav_treeListCtrl.DeleteAllItems()
            self.set_sprav_tree()
            # Удалить текст поиска
            self.search_textCtrl.SetValue(u'')            
            
        self.hidePopupInfo()
        event.Skip()
        
    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>
        """
        self.EndModal(wx.ID_CANCEL)
        self.hidePopupInfo()
        event.Skip()
        
    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>
        """
        self.EndModal(wx.ID_OK)
        self.hidePopupInfo()
        event.Skip()
        
    def onSpravTreeItemExpanded(self, event):
        """
        Обработчик разворачивания элемента дерева справочника.
        """
        item = event.GetItem()
        self.init_level_tree(item)
            
        event.Skip()

    def getSearchFieldname(self):
        """
        Определить выбранное имя поля, по которому производим поиск.
        """
        idx = self.search_field_choice.GetSelection()
        return self.sprav_search_field_names[idx] if 0 <= idx < len(self.sprav_search_field_names) else 'name'

    def clearSearch(self):
        """
        Очистка параметров поиска. Используется при кешировании формы.
        """
        # Найденые коды, соответствующие строке поиска
        self.search_codes = list()
        # Текущий найденный код в списке найденных кодов
        self.search_code_idx = 0
        # Признак необходимости обновить список искомых кодов
        self.not_actual_search = False

        # self.select_sprav_tree_item(self.default_selected_code)

        self.search_field_choice.Select(0)
        self.search_textCtrl.SetValue(u'')

    def getSearchCodes(self, search_txt, search_fieldname=None):
        """
        Обновить найденные коды соответствующие параметрам поиска.
        @param search_txt: Текст поиска.
        @param search_fieldname: Поле поиска. 
            Поле по которому производим поиск.
        @return: Список кодов справочника соответствующих параметрам поиска.
        """
        # Запуск поиска по справочнику
        if search_fieldname is None:
            search_fieldname = self.getSearchFieldname()

        # --- Обработка параметров сортировки ---
        order_by = None
        is_desc = False
        if self.sort_column:
            sort_field = self.get_sort_field(self.sort_column)
            is_desc = self.is_reverse_sort(self.sort_column)
            order_by = [sort_field] + [fld for fld in self.sprav_field_names if fld not in ('cod', sort_field)]
        # ----------------------------------------

        search_codes = self.sprav.getStorage().search(search_txt, search_fieldname,
                                                      order_by=order_by, is_desc=is_desc)
        # log.debug(u'Search codes: %s Order by: %s Is desc: %s' % (search_codes, order_by, is_desc))
        if search_codes:
            # Запомнить найденные коды в буфере
            self.search_codes = search_codes
            self.search_code_idx = 0
        return search_codes

    def onSearchToolClicked(self, event):
        """
        Обработчик инструмента поиска по наименованию записи справочника.
        """
        search_txt = self.search_textCtrl.GetValue()
        if search_txt:
            do_find = True
            if self.not_actual_search:
                search_codes = self.getSearchCodes(search_txt)
                if not search_codes:
                    ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ', u'Не найдены записи, соответствующие строке поиска')
                    do_find = False
                self.not_actual_search = False
            else:
                # Если не надо обновлять список найденных кодов, то просто
                # искать следующий код в списке
                self.search_code_idx += 1
                if self.search_code_idx >= len(self.search_codes):
                    self.search_code_idx = 0
                    
            if do_find and self.search_codes:
                find_code = self.search_codes[self.search_code_idx]
                self.select_sprav_tree_item(find_code)
        else:
            ic_dlg.icWarningBox(u'ПРЕДУПРЕЖДЕНИЕ', u'Не выбрана строка поиска')
            
        event.Skip()        
        
    def onSearchText(self, event):
        """
        Обработчик изменения строки поиска.
        """
        search_txt = event.GetString()
        # log.debug(u'Change search text <%s>' % search_txt)
        self.not_actual_search = True
        event.Skip()

    def onItemSelectChanged(self, event):
        """
        Обработчик выбора элемента дерева.
        """
        item = event.GetItem()
        if item:
            record = self.sprav_treeListCtrl.GetPyData(item)
            if record and ic_str.isMultiLineTxt(record['name']):
                # Если текст многостроковый, то выводить
                # дополнительное всплывающее окно
                self.hidePopupInfo()
                self.showPopupInfo(item, record['name'])
            else:
                self.hidePopupInfo()
        event.Skip()

    def calcPopupInfoPos(self, item=None):
        """
        Расчет позиции всплывающего окна по выделенному элементу дерева.
        @param item: Элемент дерева, к которому относиться отображаемй текст.
        @return: x, y - Расчетные значения позиции. 
        """
        if item is None:
            # Если пункт не определен, то всплывающее окно не привязано к нему
            r_x, r_y, r_w, r_h = 0, 0, 0, 0
        else:
            r_x, r_y, r_w, r_h = self.sprav_treeListCtrl.GetBoundingRect(item, False)

        if r_x == 0 and r_y == 0:
            # Скорее всего просто не можем определить координаты
            return -1, -1

        scr_x, scr_y = self.sprav_treeListCtrl.GetScreenPosition()
        pos_x, pos_y = self.sprav_treeListCtrl.GetPosition()
        col_w = sum(
            [self.sprav_treeListCtrl.GetColumnWidth(col) for col in range(self.sprav_treeListCtrl.GetColumnCount())])
        x = scr_x + pos_x + col_w
        y = scr_y + pos_y + r_y
        return x, y

    def showPopupInfo(self, item=None, txt=u'', position=None):
        """
        Отображение много-строкового текста для возможности просмотра 
            сложного наименования. Используется например для отображения простых
            схем.  
        @param item: Элемент дерева, к которому относиться отображаемй текст.
        @param txt: Многостроковый текст.
        @param position: Координаты отображения всплываемого окна.
        @return: True/False.
        """
        if position is None:
            x, y = self.calcPopupInfoPos(item)
        else:
            x, y = position

        if x == -1 and y == -1:
            # Скорее всего просто не можем определить координаты
            return

        if self.popup_win is None:
            self.popup_win = wx.PopupWindow(self, wx.SIMPLE_BORDER)
            panel = wx.Panel(self.popup_win)
            panel.SetBackgroundColour('CORNSILK')

            static_txt = wx.StaticText(panel, -1, txt, pos=(10, 10))
            font = wx.Font(pointSize=10,
                           family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL,
                           faceName='Courier New')
            static_txt.SetFont(font)

            size = static_txt.GetBestSize()
            self.popup_win.SetSize((size.width+20, size.height+20))
            panel.SetSize((size.width+20, size.height+20))

            self.popup_win.Position(wx.Point(x, y), (0, 0))
            self.popup_win.Show()

    def hidePopupInfo(self):
        """
        Скрыть дополнительные данные в всплывающем окне.
        """
        if self.popup_win:
            self.popup_win.Show(False)
            self.popup_win = None

    def getSelectedColIdx(self, mouse_x):
        """
        Определить индекс выбранной колонки.
        @param mouse_x: Координата мыши в заголовке списка справочника.
        @return: Индекс колонки, на которой кликнули мышкой.
            Если колонка не найдена, то возвращает -1.
        """
        i = 0
        column_areas = list()
        for i_col in range(self.sprav_treeListCtrl.GetColumnCount()):
            width = self.sprav_treeListCtrl.GetColumnWidth(i_col)
            column_areas.append((i, i + width))
            i += width
        find_col = [i for i, area in enumerate(column_areas) if area[0] < mouse_x < area[1]]
        find_col = find_col[0] if find_col else -1
        return find_col

    def refreshSortColumn(self, sort_column=None):
        """
        Обновить отсортированную колонку контрола списка справочника.
        @param sort_column: Колонка сортировки
        @return: True/False. 
        """
        if sort_column is None:
            sort_column = self.sort_column

        if sort_column is None:
            # Убрать все знаки
            for i_col in range(self.sprav_treeListCtrl.GetColumnCount()):
                self.sprav_treeListCtrl.SetColumnImage(i_col, -1)
        elif isinstance(sort_column, int) and sort_column > 0:
            i_col = self.get_sort_field_idx(sort_column)
            self.sprav_treeListCtrl.SetColumnImage(i_col, self.sort_ascending_img)
        elif isinstance(sort_column, int) and sort_column < 0:
            i_col = self.get_sort_field_idx(sort_column)
            self.sprav_treeListCtrl.SetColumnImage(i_col, self.sort_descending_img)
        elif type(sort_column) in (str, unicode) and not sort_column.startswith(SORT_REVERSE_SIGN):
            i_col = self.get_sort_field_idx(sort_column)
            self.sprav_treeListCtrl.SetColumnImage(i_col, self.sort_ascending_img)
        elif type(sort_column) in (str, unicode) and sort_column.startswith(SORT_REVERSE_SIGN):
            i_col = self.get_sort_field_idx(sort_column)
            self.sprav_treeListCtrl.SetColumnImage(i_col, self.sort_descending_img)
        return True

    def onHeaderMouseLeftClick(self, event):
        """
        Обработчик клика мыши на заголовочной части списка справочника.
        """
        find_col = self.getSelectedColIdx(event.GetX())

        if find_col >= 0:
            # ВНИМАНИЕ! Увеличение на 1 сделано для того чтобы учесть
            # первую колонку с индексом 0. Т.к. -0 нет.
            find_col_name = self.get_sort_field(find_col + 1)
            if self.sort_column is None:
                # Сортировка не была включена
                # Установить сортировку по возрастанию
                self.sprav_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            elif self.sort_column > 0 and self.sort_column == find_col_name:
                # Сортировка по возрастанию для этой колонки уже была включена
                # Установить сортировку по убыванию
                self.sprav_treeListCtrl.SetColumnImage(find_col, self.sort_descending_img)
                self.sort_column = SORT_REVERSE_SIGN + find_col_name
            elif self.sort_column < 0 and self.sort_column == find_col_name:
                # Сортировка по убыванию для этой колонки уже была включена
                # Установить сортировку по возрастанию
                self.sprav_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            elif self.sort_column != find_col_name:
                # Сортировка по другой колонке
                # Отключить сортировку предыдущей колонки
                prev_col = -1
                if type(self.sort_column) in (str, unicode):
                    prev_col_name = self.sort_column if not self.sort_column.startswith(SORT_REVERSE_SIGN) else self.sort_column[1:]
                    prev_col = self.sprav_field_names.index(prev_col_name)
                elif isinstance(self.sort_column, int):
                    prev_col = abs(self.sort_column) - 1
                self.sprav_treeListCtrl.SetColumnImage(prev_col, -1)
                # Включить сортировку по возрастанию для новой колонки
                self.sprav_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            else:
                log.warning(u'Ошибка определения колонки сортировки <%s>. Предыдущее значние <%s>' % (find_col,
                                                                                                      self.sort_column))
                self.sort_column = None

            if self.sort_column is not None:
                self.refresh_sprav_tree(is_progress=False, sort_column=self.sort_column)
                # Поменяли сортировку -> порядок поиска озменился
                self.not_actual_search = True

        event.Skip()


def choice_sprav_dlg(parent=None, nsi_sprav=None, fields=None,
                     default_selected_code=None, search_fields=None):
    """
    Функция вызова диалогового окна выбора кода справочника.
    ВНИМАНИЕ! Диалоговые окна кешируются в словаре кеша CHOICE_DLG_CACHE.
        Диалоги создаются только первый раз затем происходит только их вызов.
    @param parent: Родительское окно.
    @param nsi_sprav: Объект справочника.
    @param fields: Список имен полей справочника, которые
        необходимо отобразить в контроле дерева.
        Если поля не указываются, то отображаются только 
        <Код> и <Наименование>.
    @param default_selected_code: Выбранный код по умолчанию.
        Если None, то ничего не выбирается.
    @param search_fields: Поля по которым производиться поиск.
        Если не указаны, то берутся отображаемые поля.
    """
    if nsi_sprav is None:
        log.warning(u'Не определен справочник для вызова диалогового окна выбора')
        return None

    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    global CHOICE_DLG_CACHE

    sprav_name = nsi_sprav.getName()

    dlg = None
    if sprav_name not in CHOICE_DLG_CACHE or wxfunc.isWxDeadObject(CHOICE_DLG_CACHE[sprav_name]):
        dlg = icSpravChoiceTreeDlg(nsi_sprav=nsi_sprav,
                                   default_selected_code=default_selected_code,
                                   parent=parent)
        # Загрузка дополнительных данных
        ext_data = dlg.load_ext_data(nsi_sprav.getName()+'_choice_dlg')
        dlg.sort_column = ext_data.get('sort_column', None)

        fields = list() if fields is None else fields
        search_fields = fields if search_fields is None else search_fields
        dlg.init(fields, search_fields)

        CHOICE_DLG_CACHE[sprav_name] = dlg
    elif sprav_name in CHOICE_DLG_CACHE and not wxfunc.isWxDeadObject(CHOICE_DLG_CACHE[sprav_name]):
        dlg = CHOICE_DLG_CACHE[sprav_name]
        dlg.clearSearch()

    result = None
    if dlg:
        result = dlg.ShowModal()
        dlg.save_ext_data(nsi_sprav.getName()+'_choice_dlg', sort_column=dlg.sort_column)

    code = None
    if result == wx.ID_OK:
        code = dlg.getSelectedCode()
        
    # dlg.Destroy()
    return code


def del_cached_choice_sprav_dlg(nsi_sprav=None):
    """
    Удалить из кеша диалоговую форму выбора из справочника.
    @param nsi_sprav: Объект справочника.
    @return: True - форма удалена из кеша/False - форма не удалена из кеша по какойто причине.
    """
    if nsi_sprav is None:
        log.warning(u'Не определен справочник для удаления диалогового окна выбора из кеша')
        return False

    global CHOICE_DLG_CACHE

    sprav_name = nsi_sprav.getName()
    if sprav_name in CHOICE_DLG_CACHE:
        dlg = CHOICE_DLG_CACHE[sprav_name]
        dlg.Destroy()

        del CHOICE_DLG_CACHE[sprav_name]
        return True
    return False


def test():
    """
    Функция тестирования.
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    dlg = icSpravChoiceTreeDlg(parent=None)
    dlg.init_columns()
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    test()
