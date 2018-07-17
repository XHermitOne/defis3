#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import os

print('POST SCRIPT START', os.getcwd())
CMD_SCRIPT = [
    ('mergeCell', (u'Лист1', 5, 1, 1, 0)),
    ('setCellStyle', (u'Лист1', 5, 1), {'Alignment_': {'Vertical': 'Center',
                                                       'Horizontal': 'Center'},
                                        'Borders_': {'name': 'Borders',
                                                     'children': [{'Position': 'Bottom',
                                                                   'LineStyle': 'Continuous',
                                                                   'Weight': 2},
                                                                  {'Position': 'Top',
                                                                   'LineStyle': 'Continuous',
                                                                   'Weight': 2},
                                                                  {'Position': 'Left',
                                                                   'LineStyle': 'Continuous',
                                                                   'Weight': 2}]}}),
    ('mergeCell', (u'Лист1', 5, 2, 1, 0)),
    ('setCellStyle', (u'Лист1', 5, 2), {'Alignment_': {'Vertical': 'Center',
                                                       'Horizontal': 'Center'},
                                        'Borders_': {'name': 'Borders',
                                                     'children': [{'Position': 'Bottom',
                                                                   'LineStyle': 'Continuous',
                                                                   'Weight': 2},
                                                                  {'Position': 'Top',
                                                                   'LineStyle': 'Continuous',
                                                                   'Weight': 2}]}}),
]
root_parser.app.exec_cmd_script(CMD_SCRIPT)
print('POST SCRIPT OK')
