# PyReditor - Advanced Python Regular Expresion Editor
#
# Copyright (c) 2008, 2009
# Primoz Cermelj <primoz.cermelj@gmail.com>
#
# This program is based on RegexEditor.plug-in.py plugin originated from
# Boa Constructor and is licensed under GPL.
# 
# See LICENSE.TXT for license terms.
#----------------------------------------------------------------------------

import wx
from .commons import setpath, set_png


class EditInsertMenu(wx.Menu):
    """Versatile and enhanced EDIT and/or INSERT menu that can be used for a
    RE editor, either as a classical menu within a menu bar or as a popup menu.
    """
    def __init__(self, parent, stc, path=None, hasedit=True, insertitems=None,
                 tempitems=None, acckeys=None):
        """Path is used to find images (icons) - this is app's path. acckeys
        is not used at the moment. hasedit, insertitems and tempiitems are used to
        turn on/off each of the menues/part. At
        least one has to be given/true. parent should be None if used as a popup, and
        an existing form instance for a regular menu - to bind the menu events to
        the form!
        
        This can be used as a popup menu binded to an editor (use like 
        editor.PopupMenu(self._popup)) or can be added as a submenu to an
        existing menu in the menubar.
        """
        if hasedit == False and insertitems == None and tempitems == None:
            raise Exception('At least one of {hasedit, insertitems, tempitems},'\
                            ' must be given/True')
        wx.Menu.__init__(self)
        
        self._stc = stc             # The parent (RE editor)
        self._path = setpath(path)  # main app's path
        self._hasedit = hasedit == True
        self._hasinsert = insertitems != None
        self._hastemp = tempitems != None
        self._insertitems = insertitems
        self._tempitems = tempitems
        self._parent = parent
        self.ids = {}
        
        # The submenus/menu items
        if self._hastemp:
            # "template" submenus - essentially the same as the insert ones
            # bellow
            if tempitems == {} or tempitems == None:
                id = wx.NewId()
                self.Append(id=id, text='No templates found')
                self.Enable(id, False)
            else:
                self._add_submenu_items(tempitems, separator=False)
        if self._hasinsert:
            # insert submenus
            self._add_submenu_items(insertitems, separator=self._hastemp)
        if hasedit:
            # standard "edit" items
            self._add_edit_items(separator=(self._hastemp or self._hasinsert))
            # Add some events to stc that manages (auto enabling and disabling)
            # of the standard edit items.
            self._stc.Bind(wx.EVT_UPDATE_UI, self._OnUpdateUI)
        
    def _add_submenu_items(self, submenus, separator=False):
        # Add submenu items to the menu (to self) and set the bindings as well -
        # all the callbacks will be bound to the:
        #    self._OnInsertItem callback
        # This can be used for inesrtion-like submenu items like for insertions
        # and templates used herein.
        # submenus is a dictionary (here will be either self._insertitems or
        # self._tempitems) that holds all the information needed for the menu
        # items creation, including the names for the icons, insertions, etc.
        # "insert items"
        
        # Add items' ids to self.ids
        _id = wx.NewId
        for key in submenus:
            items = submenus[key][1]
            self.ids.update({key: _id()})
            for subkey in items:
                self.ids.update({subkey: _id()})
                
        # Update self._id2name dictionary
        self._updateid2name()
        
        # Add the submenus to (self) menu
        if separator:
            self.AppendSeparator()
        for menu_name in submenus:
            menu = wx.Menu()
            item_dict = submenus[menu_name][1]
            icon_name = submenus[menu_name][0]
            for it in sorted(item_dict.keys()):
                menu.Append(self.ids[it], item_dict[it][0])
            # menu item as a submenu
            self._add_menu_item(self, id=self.ids[menu_name], text=menu_name,
                                icon=icon_name, submenu=menu)
            
        # Bindings
        # And those for the submenus
        if self._parent == None:
            obj = self._stc
        else:
            obj = self._parent
        for menu_name in submenus:
            for it in submenus[menu_name][1]:
                obj.Bind(wx.EVT_MENU, self._OnInsertItem, id=self.ids[it])
                
    def _add_menu_item(self, menu, id, text, icon=None, submenu=None):
        # Adds a menu icon to the menu. If the icon does not exist, it simply
        # ignores this.
        mitem = wx.MenuItem(menu, id=id, text=text, subMenu=submenu)
        try:
            mitem.SetBitmap(set_png(self._path, icon))
        except:
            pass
        menu.AppendItem(mitem)
    
    def _add_edit_items(self, separator=False):
        # Adds standard edit menu items to the menu. Separator can be appended
        # to the menu (self) at the beginning if requested so.
        
        _id = wx.NewId
        self.ids.update({'undo':_id(), 'redo':_id(), 'cut':_id(), 'copy':_id(),
                         'paste':_id(), 'delete':_id(), 'select_all':_id(),
                         'insert':_id()})
        
        # Update self._id2name dictionary
        self._updateid2name()
        
        # The items
        if separator:
            self.AppendSeparator()
            
        self._add_menu_item(self, id=self.ids['undo'], text='Undo', icon=r'undo.png')
        self._add_menu_item(self, id=self.ids['redo'], text='Redo', icon=r'redo.png')
        
        self.AppendSeparator()
        
        self._add_menu_item(self, id=self.ids['cut'], text='Cut', icon=r'editcut.png')
        self._add_menu_item(self, id=self.ids['copy'], text='Copy', icon=r'editcopy.png')
        self._add_menu_item(self, id=self.ids['paste'], text='Paste', icon=r'editpaste.png')
        self.Append(self.ids['delete'], 'Delete')

        self.AppendSeparator()
        
        self.Append(self.ids['select_all'], 'Select All')
        
        # Bind the standard menu items
        if self._parent == None:
            obj = self._stc
        else:
            obj = self._parent
        obj.Bind(wx.EVT_MENU, self._OnUndo, id=self.ids['undo'])
        obj.Bind(wx.EVT_MENU, self._OnRedo ,id=self.ids['redo'])
        obj.Bind(wx.EVT_MENU, self._OnCut, id=self.ids['cut'])
        obj.Bind(wx.EVT_MENU, self._OnCopy, id=self.ids['copy'])
        obj.Bind(wx.EVT_MENU, self._OnPaste, id=self.ids['paste'])
        obj.Bind(wx.EVT_MENU, self._OnDelete, id=self.ids['delete'])
        obj.Bind(wx.EVT_MENU, self._OnSelectAll, id=self.ids['select_all'])
                
    def set_editor(self, stc):
        """Sets the editor this menu corresponds (binds) to. This is to be used
        when this menu is a part of the menubar (not a popup menu), where it might
        bind to more than one editor if there is a multi-tab application. So, this
        way the callbacks will "fire" the proper editor (stc).
        """
        self._stc = stc
        
    def _OnUndo(self, event):
        self._stc.Undo()
    
    def _OnRedo(self, event):
        self._stc.Redo()

    def _OnCut(self, event):
        self._stc.Cut()
    
    def _OnCopy(self, event):
        self._stc.Copy()
    
    def _OnPaste(self, event):
        self._stc.Paste()
    
    def _OnDelete(self, event):
        self._stc.Clear()
    
    def _OnSelectAll(self, event):
        self._stc.SelectAll()
        
    def _OnInsertItem(self, event):
        # All the "insertions" (insertmenus and templates) are handled here,
        # according to the id that fired this callback.
        name = self._id2name[event.Id]
        if self._insertitems != None:
            for menu_name in self._insertitems:
                if name in self._insertitems[menu_name][1].keys():
                    embr = self._insertitems[menu_name][1][name][1]
                    text = self._insertitems[menu_name][1][name][2]
                    sel = self._insertitems[menu_name][1][name][3]
                    self._stc.insert_text(text, embr, sel)
                    return
        if self._tempitems != None:
            for menu_name in self._tempitems:
                if name in self._tempitems[menu_name][1].keys():
                    embr = self._tempitems[menu_name][1][name][1]
                    text = self._tempitems[menu_name][1][name][2]
                    sel = self._tempitems[menu_name][1][name][3]
                    self._stc.insert_text(text, embr, sel)
                    return
        
    def _OnUpdateUI(self, event):
        # The standard menu items are updated automatically
        if self._hasedit:
            if self._stc.CanUndo(): self.Enable(self.ids['undo'], True)
            else: self.Enable(self.ids['undo'], False)
            if self._stc.CanRedo(): self.Enable(self.ids['redo'], True)
            else: self.Enable(self.ids['redo'], False)
            if self._stc.CanPaste(): self.Enable(self.ids['paste'], True)
            else: self.Enable(self.ids['paste'], False)
        event.Skip()
        
    def enable(self, items, on=True):
        """Enables/disables the ids of the items given - items given as
        keys corresponding to self.ids - see get_id_names(). Standard items (cut,
        paste,...) are handled automatically.
        """
        for item in items:
            id = self.ids[item]
            self.Enable(id, on==True)
        
    def get_id_names(self):
        return self.ids.keys()
    
    def get_ids(self):
        return self.ids
    
    def _updateid2name(self):
        # Updates self._id2name dictionary, an id-to-name-mapping
        self._id2name = dict([(self.ids[key], key) for key in self.ids])
        
