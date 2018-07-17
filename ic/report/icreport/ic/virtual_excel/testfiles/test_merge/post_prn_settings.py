# -*- coding: cp866 -*-

CMD_SCRIPT=[
    ('mergeCell',(u'Лист1',5,1,1,0)),
    ('setCellStyle',(u'Лист1',5,1),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous','Weight':2},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous','Weight':2}}),
    ('mergeCell',(u'Лист1',5,2,1,0)),
    ('setCellStyle',(u'Лист1',5,2),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous','Weight':2}}),
    ('mergeCell',(u'Лист1',5,3,0,2)),
    ('setCellStyle',(u'Лист1',5,3),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('mergeCell',(u'Лист1',5,6,0,2)),
    ('setCellStyle',(u'Лист1',5,6),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('mergeCell',(u'Лист1',5,9,0,2)),
    ('setCellStyle',(u'Лист1',5,9),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('mergeCell',(u'Лист1',5,12,0,2)),
    ('setCellStyle',(u'Лист1',5,12),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('mergeCell',(u'Лист1',5,15,0,2)),
    ('setCellStyle',(u'Лист1',5,15),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('mergeCell',(u'Лист1',5,18,0,2)),
    ('setCellValue',(u'Лист1',5,18,u'Итого')),
    ('setCellStyle',(u'Лист1',5,18),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous'},'right_border':{'LineStyle':'Continuous'},'top_border':{'LineStyle':'Continuous','Weight':2},'bottom_border':{'LineStyle':'Continuous'}}),
    ('setCellStyle',(u'Лист1',5,21),{'alignment':{'Vertical':'Center','Horizontal':'Center'},'left_border':{'LineStyle':'Continuous','Weight':2}}),
]
root_parser.app.exec_cmd_script(CMD_SCRIPT)
