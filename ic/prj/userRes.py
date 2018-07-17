#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса управления ресурсом прав и пользователей.
"""

# --- Подключение библиотек ---
import wx
import copy
import os
import os.path
import ic.interfaces.resManager as resManager
from ic.kernel import io_prnt
import ic.utils.ic_res as ic_res
import ic.utils.ic_file as ic_file
import ic.dlg.ic_dlg as ic_dlg
from ic.engine import icUser 

_ = wx.GetTranslation

__version__ = (0, 0, 1, 2)


class UserResource(resManager.ResourceManagerInterface):
    """
    Класс управления ресурсом проекта.
    """

    def __init__(self):
        """
        Конструктор.
        """
        resManager.ResourceManagerInterface.__init__(self)
        # Дерево ресурса
        self._user_res = None
        # Файл
        self._user_res_file_name = None
        # Время последней модификации ресурса
        self._res_maker_time = 0

    def setResFileName(self, ResFileName_=None):
        self._user_res_file_name = ResFileName_

    def defaultRes(self):
        """
        Значение ресурса по умолчанию.
        """
        usr = self.newDefaultUser('new_user')
        return {'new_user': usr}

    def HasItemInDict(self, p, ResName, tp):
        """
        Функция проверки наличия элемента в словаре.
        @param  p: путь к элементу в виде '' для ресурса типа TAB,VAR,WIN,MNU,SVB,FRM
            в виде '['tab1']['shema'][0]['group']' для ресурса типа TAB-SHEMA.
        @param ResName: имя ресурса.
        @param tp: тип ресурса ('tab','var','win','mnu','svb','frm').
        """
        flag = ResName
        t_lst = []
        if p == '':
            lst = tp.keys()
            for i in range(len(lst)):
                for key in lst:
                    if key == flag:
                        flag = 'copy('+str(i+1)+')_'+ResName
                        break
        else:
            lst = tp+p
            for i in range(len(lst)):
                for dic in lst:
                    if dic['name'] == flag:
                        flag = 'copy('+str(i+1)+')_'+ResName
                        break
        return flag

    def newDefault(self, UserName_='new_user'):
        """
        Создание ресурса по умолччанию. Для одного пользователя!!!.
        @param UserName_: Имя пользрвателя по умолчанию.
        """
        usr = {'_uuid': None,
               'name': UserName_,
               'type': 'User',
               'description': None,
               'password': None,
               'group': None,
               'lock_time': ([], [], [], [], [], [], []),
               'access': [],
               'run_res': [],
               'runner': [],
               'local_dir': None,
               'on_login': None,
               'on_logout': None}
        return usr

    def newDefaultUser(self, UserName_='new_user'):
        """
        Создание ресурса по умолччанию. Для одного пользователя!!!.
        @param UserName_: Имя пользрвателя по умолчанию.
        """
        usr = copy.deepcopy(icUser.SPC_IC_USER)
        usr['_uuid'] = None
        usr['name'] = UserName_
        return usr
        
    def newDefaultUserGroup(self, UserGrpName_='new_user_grp'):
        """
        Спецификация группы пользователей по умолчанию.
        @param UserGrpName_: Имя группы пользрвателей.
        """
        usr_grp = copy.deepcopy(icUser.SPC_IC_USERGROUP)
        usr_grp['_uuid'] = None
        usr_grp['name'] = UserGrpName_
        return usr_grp
        
    def Add(self, parent=None):
        """
        Добавить элемент.
        @param parent: родительский.
        """
        # получить новое имя
        nm = self.HasItemInDict('', 'new_user', 'acc')
        if nm == 'new_user':
            self._user_res['new_user'] = self.newDefaultUser()
            if parent is not None:
                self._user_res['new_user']['group'] = parent
            return 1
        else:
            return 0

    def renameUser(self, OldUserName_, NewUserName_):
        """
        Переименовать пользователя.
        @param OldUserName_: Старое имя пользователя.
        @param NewUserName_: Новое имя пользователя.
        @return: Функция возвращает результат выполнения операции True/False.
        """
        try:
            usr = self._user_res[OldUserName_]
            del self._user_res[OldUserName_]    
            self._user_res[NewUserName_] = usr
            self._user_res[NewUserName_]['name'] = NewUserName_
            return True
        except:
            io_prnt.outErr(u'renameUser ERROR')
            return False

    def Copy(self, struct, parent=None):
        """
        Копирует данные.
        @param struct: Дерево.
        @param parent: Родительский.
        @return: Возвращает struct с новыми именами.
        """
        # получить новое имя
        nm = self.HasItemInDict('', struct.keys()[0], 'acc')
        # изменить словарь acc
        val = copy.deepcopy(self._user_res[struct.keys()[0]])
        self._user_res[nm] = val
        self._user_res[nm]['name'] = nm
        if parent is not None:
            self._user_res[nm]['group'] = parent
        parent = nm
        # сохранить новое имя в передавамой структуре
        val = struct[struct.keys()[0]]
        del struct[struct.keys()[0]]
        struct[nm] = val
        list = struct[struct.keys()[0]]
        i = 0
        for item in list:
            if isinstance(item, str):
                # получить новое имя
                nm = self.HasItemInDict('', item, 'acc')
                # изменить словарь acc
                val = copy.deepcopy(self._user_res[item])
                self._user_res[nm] = val
                self._user_res[nm]['name'] = nm
                self._user_res[nm]['group'] = parent
                # сохранить новое имя в передавамой структуре
                struct[struct.keys()[0]][i] = nm
            elif isinstance(item, dict):
                self.Copy(item, parent)
            i += 1
        return struct
    
    def Del(self, struct):
        """
        Удаляет все значения ключей acc, заданных в struct.
        """
        try:
            del self._user_res[struct.keys()[0]]
            list = struct[struct.keys()[0]]
            for item in list:
                if isinstance(item, str):
                    del self._user_res[item]
                elif isinstance(item, dict):
                    self.Del(item)
            return 1
        except:
            return 0
            
    def CopyToClip(self, struct):
        """
        Формирует список значений ключей acc, заданых в struct.
        """
        lst = []
        s = copy.deepcopy(self._user_res[struct.keys()[0]])
        lst.insert(0, s)
        list = struct[struct.keys()[0]]
        for item in list:
            if isinstance(item, str):
                s = copy.deepcopy(self._user_res[item])
                lst.insert(0, s)
            elif isinstance(item, dict):
                lst = self.CopyToClip(item)+lst
        return lst
    
    def PasteFromClip(self, struct, lst, parent=None):
        """
        Вставляет данные из Clipboard'а.
        @param struct: Дерево.
        @param lst: Список словарей - значений соответствующих ключей.
        @param parent: Родительский.
        @return: Возвращает struct с новыми именами.
        """
        # получить новое имя
        nm = self.HasItemInDict('', struct.keys()[0], 'acc')
        # сохранить новое имя в передавамой структуре
        val = struct[struct.keys()[0]]
        del struct[struct.keys()[0]]
        struct[nm] = val
        # изменить словарь acc
        self._user_res[nm] = lst.pop()
        self._user_res[nm]['name'] = nm
        if parent is not None:
            self._user_res[nm]['group'] = parent
        parent = nm
        list = struct[struct.keys()[0]]
        i = 0
        for item in list:
            if isinstance(item, str):
                # получить новое имя
                nm = self.HasItemInDict('', item, 'acc')
                # сохранить новое имя в передавамой структуре
                struct[struct.keys()[0]][i] = nm
                # изменить словарь acc
                self._user_res[nm] = lst.pop()
                self._user_res[nm]['name'] = nm
                self._user_res[nm]['group'] = parent
            elif isinstance(item, dict):
                self.PasteFromClip(item, lst, parent)
            i += 1
        return struct
    
    def save(self):
        """
        Сохранить.
        """
        self.saveAs(self._user_res_file_name)

    def saveAs(self, ResFileName_=None):
        """
        Сохранить как...
        @param ResFileName_: Имя ресурсного файла, если None, 
            то сделать его запрос.
        @return: Функция возвращает результат выполнения операции 
            сохранения True/False.
        """
        self._user_res_file_name = ResFileName_
        if self._user_res_file_name is None:
            self._user_res_file_name = ic_dlg.icFileDlg(None, u'Create user access file',
                                                        u'User access file (*.acc)|*.acc')
        
        if self._user_res_file_name:
            # Создать путь к файлу
            ic_file.MakeDirs(ic_file.Split(self._user_res_file_name)[0])
            # Сохранить сам файл
            return ic_res.SaveResourceText(self._user_res_file_name,
                                           self._user_res)
        return False

    def load(self, ResFileName_=None):
        """
        Загрузить из ресурсного файла.
        @param ResFileName_: Имя ресурсного файла, если None, 
            то сделать его запрос.
        """
        self._user_res_file_name = ResFileName_
        if self._user_res_file_name is None:
            self._user_res_file_name = ic_dlg.icFileDlg(None, u'Create user access file',
                                                        u'User access file (*.acc)|*.acc')
        self._user_res = None
        if self._user_res_file_name and \
           os.path.exists(self._user_res_file_name):
            # Обновить ресурс?
            refresh = self._res_maker_time != ic_file.GetMakeFileTime(self._user_res_file_name)
            self._user_res = ic_res.ReadAndEvalFile(self._user_res_file_name, bRefresh=refresh)
            self._res_maker_time = ic_file.GetMakeFileTime(self._user_res_file_name)
        return self._user_res

    def getRes(self):
        """
        Определение ресурса.
        """
        if self._user_res is None:
            if self._user_res_file_name:
                if ic_file.Exists(self._user_res_file_name):
                    self._user_res = ic_res.ReadAndEvalFile(self._user_res_file_name)
                else:
                    self._user_res = {'admin': self.newDefaultUser()}
                    self._user_res['admin']['name'] = 'admin'
        return self._user_res

    def getUserRes(self, UserName_):
        """
        Ресурс пользователя по имени.
        """
        return self.getRes()[UserName_]
        
    def DictToTree(self, dict):
        """
        Преобразовать словарь из файла *.acc в словарно-списковую структуру следующего формата:
        ['Admin',{'Users':['User1','User2']},
        {'Dirs':[{'Dir1':['Dir1_1','Dir1_2']},'Dir2']}].
        Если элемент списка - строка, то это НЕ группа.
        Если элемент списка - словарь, то это группа.
        @return: Возвращает словарно-списковую структуру.
        """
        # Формируем список кортежей, каждый кортеж содержит отношение (потомок,родитель)
        # отношение формируется из имени основного ключа и значения ключа 'group'
        # соответствующего словаря
        tree = []
        rel = []
        lev = {}
        for key in dict.keys():
            if dict[key]['group'] is not None:
                rel.append((key, dict[key]['group']))
                # формируем словарь уровней элементов, формата: {'Admin':1,'Users':1,'User1':1,...}
                lev[dict[key]['group']] = 1
                lev[key] = 1
        # дополнить словарно-списковую структуру tree, ключами, которые 'остались за бортом'
        # во время выполнения предыдущего кода
        for key in dict.keys():
            if key not in lev:
                tree.append(key)
    
        # оставляем в словаре только элементы самого верхненго уровня группировки
        for key in lev.keys():
            if self.DictToTreeLevel(key, rel):
                del lev[key]
        # формируем словарно-списковую структуру
        for key in lev.keys():
            tree.append({key: self.DictToTreeList(key, rel)})
        return tree
    
    def DictToTreeLevel(self, key, list):
        """
        Вспомогательная рекурсивная функция.
        @param key: имя элемента (проверяется входимость элемента в список кортежей).
        @param list: список кортежей.
        @return: Возвращает 1,если элемент обнаружен, иначе 0
        """
        for cor in list:
            if key == cor[0]:
                return 1
        return 0
    
    def DictToTreeList(self, key, list):
        """
        Вспомогательная рекурсивная функция.
        @param key: имя элемента (проверяется входимость элемента в список кортежей).
        @param list: список кортежей.
        @return: Возвращает списочно-словарную структуру
        """
        tree = []
        flag = 0
        for cor in list:
            if key == cor[1]:
                flag = 1
                t = self.DictToTreeList(cor[0], list)
                if t == cor[0]:
                    tree.append(cor[0])
                else:
                    tree.append({cor[0]: t})
        if flag == 0:
            return key
        else:
            return tree

    def createUser(self, UserName_='new_user'):
        """
        Создание нового пользователя в структуре.
        @param UserName_: Имя пользователя.
        @return: Возвращает результат выполнения операции True/False.
        """
        if self._user_res is None:
            self._user_res = {}
            
        if UserName_ in self._user_res:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Пользователь <%s> уже существует!' % UserName_)
            return False    
        else:
            self._user_res[UserName_] = self.newDefaultUser(UserName_)
        return True
        
    def createUserGroup(self, UserGrpName_='new_user_grp'):
        """
        Создание новой группы пользователей в структуре.
        @param UserName_: Имя пользователя.
        @return: Возвращает результат выполнения операции True/False.
        """
        if self._user_res is None:
            self._user_res = {}
            
        if UserGrpName_ in self._user_res:
            ic_dlg.icMsgBox(u'ВНИМАНИЕ!',
                            u'Пользователь <%s> уже существует!' % UserGrpName_)
            return False    
        else:
            self._user_res[UserGrpName_] = self.newDefaultUserGroup(UserGrpName_)
        return True
        
    def createRes(self, ResFileName_=None):
        """
        Создать файл ресурсов прав и пользователей.
        @param ResFileName_: Имя ресурсного файла.
        @return: Функция возвращает результат выполнения операции 
            сохранения True/False.
        """
        if ResFileName_:
            self._user_res_file_name = ResFileName_
        if self._user_res_file_name:    
            if not os.path.isfile(self._user_res_file_name):
                # Создать сам ресурс
                self._user_res = self.defaultRes()
                return self.saveAs(self._user_res_file_name)
        return False

    def delUser(self, UserName_='new_user'):
        """
        Удаление пользователя из ресурса.
        @param UserName_: Имя пользователя.
        @return: Возвращает True/False.
        """
        if self._user_res is None:
            self._user_res = {}
            
        if UserName_ in self._user_res:
            # Сначала проверить исть ли наследники у указанного
            # пользователя.
            user_legacy = self.findUserLegacy(UserName_)
            if user_legacy:
                # Если есть, то не удалять его
                ic_dlg.MsgBox(u'ВНИМАНИЕ!',
                              u'У пользователя <%s> есть наследники. Сначала удалите их.' % user_legacy)
                return False
            del self._user_res[UserName_]
            return True
        return False
            
    def findUserLegacy(self, UserName_='new_user'):
        """
        Поиск имен пользователей, которые наследуют права от UserName_.
        @param UserName_: Имя пользователя.
        @return: Возвращает список имен пользователей-наследников
            или None  в случае ошибки.
        """
        if self._user_res:
            return [user[0] for user in self._user_res.items() if 'group' in user[1] and user[1]['group'] == UserName_]
        return None
        
    def isUser(self, UserName_='new_user'):
        """
        Проверка,  есть ли такой пользователь в ресурса.
        @param UserName_: Имя пользователя.
        """
        if self._user_res:
            return UserName_ in self._user_res
        return False

    def getUserNameList(self):
        """
        Список имен пользователей.
        """
        if self._user_res:
            return self._user_res.keys()
        return []        
        
    def getUserNameTypeDict(self):
        """
        Словарь {имя: тип}.
        """
        if self._user_res:
            return dict([(name, self._user_res[name]['type']) for name in self._user_res.keys()])
        return {}

    def getUsers(self):
        """
        Получить полный ресурс всех пользователей.
        """
        return self._user_res

    def getUserNameDescriptionDict(self):
        """
        Словарь {имя пользователя: описание пользователя}.
        """
        if self._user_res:
            return dict([(name, self._user_res[name].get('description', u'')) for name in self._user_res.keys()])
        return dict()
