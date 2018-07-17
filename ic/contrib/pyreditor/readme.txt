=========
PyReditor
=========

:Author: Primoz Cermelj
:Contact: primoz.cermelj@gmail.com
:Version: 1.1.4
:Revision: 2010

.. contents:: Table of Contents


Introduction
------------

PyReditor is a simple but quite useful Regular Expression Editor for
Python, i.e, for Python's re module. The editor has syntax
highlighting, brace matching, easy zoom in/out capability, context-menu
RE shortcuts, re templates and more.

PyReditor is a should have tool for a Python programmer.


Installation
------------

PyReditor can be used as a standalone tool or as a plugin to
Boa Constructor (open source rapid UI development environment).

To use it as a standalone application, copy everything to a
folder (e.g. create pyreditor folder somewhere), and run
pyreditor.pyw. For this to work, Python and wxPython must be
installed and will probably work on Linux too.

To run PyReditor without the need for Python and/or wxPython,
run pyreditor.exe. However, this will only work on MS Windows
(win xp/vista/7).

See also plugin-install.txt to see how to add PyReditor to
Boa Constructor's Tools menu, i.e., how to use it as Boa's
plugin.


Templates
---------

From version 1.0.0b and up, PyReditor has (optional) templates -
code snippets the user can insert. These templates are stored in
templates.cfg ascii files and can be easily modified (changed, new
templates added, deleted).