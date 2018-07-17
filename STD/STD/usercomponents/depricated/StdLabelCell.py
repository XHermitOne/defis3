#!/usr/bin/env python
# -*- coding: utf-8 -*-
### TEMPLATE_MODULE:
"""
Представление ячеек (в зависимости от схемы) для стилизованного грида (StdDataGrid).
"""
import wx
import ic.interfaces.ictemplate as ictemplate
import ic.utils.util as util
import copy
import ic.PropertyEditor.icDefInf as icDefInf
import ic.kernel.io_prnt as io_prnt
import STD.reestr_img as reestr_img

### Описание цветовых схем
blue_scheme = {'bgrImage':reestr_img.blue2Bgr,
               'foregroundColor': (255, 255, 255),
               'backgroundColor': (164, 209, 255)}

light_blue_scheme = {'bgrImage':reestr_img.blueBgr,
               'foregroundColor': (0, 0, 0),
               'backgroundColor': (164, 209, 255)}

std_scheme = {'backgroundType':0,
              'bgrImage':None}
            
red_scheme = {'backgroundColor': (128, 0, 45),
             'foregroundColor': (255, 255, 255),
             'backgroundColor2': (232, 0, 81),
             'bgrImage':reestr_img.redBgr,
             'borderBottomColor': (136, 0, 68),
             'borderTopColor': (136, 0, 68),
             'borderLeftColor': (136, 0, 68),
             'borderRightColor': (136, 0, 68)}

green_scheme = {'backgroundColor': (56, 112, 94),
             'backgroundColor2': (95, 175, 149),
             'foregroundColor': (255, 255, 255),
             'bgrImage':reestr_img.greenBgr,
             'borderBottomColor': (44, 86, 72),
             'borderTopColor': (44, 86, 72),
             'borderLeftColor': (44, 86, 72),
             'borderRightColor': (44, 86, 72)}

gray_scheme = {'backgroundColor': (178, 178, 178),
             'backgroundColor2': (245, 245, 245),
             'foregroundColor': (0, 0, 0),
             'bgrImage':reestr_img.gray2Bgr,
             'borderBottomColor': (150, 150, 150),
             'borderTopColor': (150, 150, 150),
             'borderLeftColor': (150, 150, 150),
             'borderRightColor': (150, 150, 150)}

flat_gray_scheme = {'backgroundColor': (178, 178, 178),
             'backgroundColor2': (245, 245, 245),
             'foregroundColor': (0, 0, 0),
             'bgrImage':reestr_img.indBgrPic3,
             'borderBottomColor': (150, 150, 150),
             'borderTopColor': (150, 150, 150),
             'borderLeftColor': (150, 150, 150),
             'borderRightColor': (150, 150, 150)}

white_scheme = {'backgroundColor': (209, 228, 248),
             'backgroundColor2': (249, 252, 255),
             'foregroundColor': (50, 50, 70),
             'bgrImage':reestr_img.whiteBlueBgr,
             'borderBottomColor': (153, 189, 230),
             'borderTopColor': (153, 189, 230),
             'borderLeftColor': (153, 189, 230),
             'borderRightColor': (153, 189, 230)}

gold_scheme = {'backgroundColor': (249, 164, 6),
             'backgroundColor2': (250, 233, 78),
             'foregroundColor': (0, 0, 0),
             'bgrImage':reestr_img.lightGoldBgr,
             'borderBottomColor': (133, 107, 7),
             'borderTopColor': (181, 134, 11),
             'borderLeftColor': (181, 134, 11),
             'borderRightColor': (181, 134, 11)}

black_scheme = {'backgroundColor': (30, 30, 30),
             'backgroundColor2': (127, 127, 127),
             'bgrImage':reestr_img.blackBgr,
             'borderBottomColor': (30, 30, 30),
             'borderTopColor': (30, 30, 30),
             'borderLeftColor': (30, 30, 30),
             'borderRightColor': (30, 30, 30)}
            
lightBrown_scheme = {'backgroundColor': (223, 223, 189),
             'backgroundColor2': (247, 247, 238),
             'foregroundColor': (0, 0, 0),
             'bgrImage':reestr_img.lightBrownBgr,
             'borderBottomColor': (187, 187, 115),
             'borderTopColor': (187, 187, 115),
             'borderLeftColor': (187, 187, 115),
             'borderRightColor': (187, 187, 115)}

scheme_dict = {'RED':red_scheme,
               'BLUE':blue_scheme,
               'LIGHT_BLUE':light_blue_scheme,
               'GREEN':green_scheme,
               'GRAY':gray_scheme,
               'LIGHT_BROWN':lightBrown_scheme,
               'FLAT_GRAY':flat_gray_scheme,
               'GOLD':gold_scheme,
               'WHITE':white_scheme,
               'BLACK':black_scheme,
               'STD':std_scheme}

### Общий интерфейс компонента
ictemplate.init_component_interface(globals(), ic_class_name = 'CStdLabelCell')

ic_class_spc = {'name':'defaultPanel',
                'type':'StdLabelCell',
                'round_corner':[1,1,1,1],
                'label':'Label',
                'przn_border':[1,1,1,1],
                'foregroundColor': None,
                'backgroundColor': None,
                'borderColor': None,
                'shortHelpString':'',
                'isSort':False,
                'scheme':'BLUE',
                '__attr_types__': {0: ['name', 'type'],
                        icDefInf.EDT_TEXTLIST: ['round_corner', 'przn_border'],
                        icDefInf.EDT_NUMBER:['isSort'],
                        icDefInf.EDT_CHOICE:['scheme'],
                        icDefInf.EDT_COLOR:['foregroundColor', 'backgroundColor', 'borderColor']},
                '__lists__':{'scheme':scheme_dict.keys()},
                '__parent__':ictemplate.SPC_IC_TEMPLATE}
                
### !!!! Данный блок изменять не рекомендуется !!!!
###BEGIN SPECIAL BLOCK
#   Ресурсное описание класса
resource={'activate': 1, 'obj_module': None, 'show': 1, 'borderRightColor': (0, 66, 132), 'child': [], 'refresh': None, 'borderWidth': 1, 'borderTopColor': (0, 66, 132), 'font': {}, 'border': 0, 'alignment': (u'centred', u'middle'), 'size': (96, 20), 'moveAfterInTabOrder': u'', 'foregroundColor': (255, 255, 255), 'span': (1, 1), 'component_module': None, 'proportion': 0, 'label': u'\u041f\u043e\u043b\u0435 2', 'source': None, 'backgroundColor': (1, 84, 209), 'isSort': 1, 'type': u'HeadCell', 'res_module': None, 'description': None, 'shortHelpString': u'\u0421\u043f\u0440\u0430\u0432\u043a\u0430:\r\n\u043f\u043e \u0432\u0442\u043e\u0440\u043e\u043c\u0443 \u043f\u043e\u043b\u044e !!!', 'backgroundColor2': (0, 128, 255), '_uuid': u'8a7aee68fff59709e78a0aca1ed8a293', 'style': 0, 'bgrImage': None, 'flag': 0, 'recount': None, 'onLeftDown': None, 'cursorColor': (0, 66, 132), 'borderStyle': None, 'borderStep': 0, 'borderLeftColor': (0, 66, 132), 'name': u'LabelCell', 'borderBottomColor': (0, 66, 132), 'keyDown': None, 'alias': None, 'init_expr': u'', 'position': (10, 10), 'backgroundType': 1, 'onInit': None}

#   Версия объекта
__version__ = (1, 0, 3, 0)
###END SPECIAL BLOCK

class CStdLabelCell(ictemplate.icTemplateInterface):
    """
    Описание пользовательского компонента.

    @type component_spc: C{dictionary}
    @cvar component_spc: Спецификация компонента.
        - B{type='defaultType'}:
        - B{name='default'}:
        - B{label='Label'}: Текст заголовка.
        - B{przn_border=[1,1,1,1]}: Признак наличия бордюр [L,T,R,B].
        - B{shortHelpString=''}: Подсказка заголовка.
        - B{round_corner=(1,1,1,1)}: Задает для каждого угла (rt, lt, lb, rb)
            признак скругления.
    """
    component_spc = ic_class_spc
    
    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace = None, bCounter=False, progressDlg=None):
        """
        Конструктор интерфейса.
        """
        #   Дополняем до спецификации
        component = util.icSpcDefStruct(ic_class_spc, component)
            
        self.scheme = component['scheme']
        self.round_corner = component['round_corner']
        self.label = component['label']
        self.przn_border = component['przn_border']
        self.shortHelpString = component['shortHelpString']
        self.isSort = component['isSort']
            
        ictemplate.icTemplateInterface.__init__(self, parent, id, component, logType, evalSpace,
                                                bCounter, progressDlg)
        self._reload_resource()

        #   Устанавливаем нужную схему (по умолчанию стоит BLUE).
        self.resource['name'] = component['name']
        
        if self.scheme in scheme_dict.keys():
            sch = scheme_dict[self.scheme]
            for key, val in sch.items():
                self.resource[key] = val
                
            if self.scheme == 'STD':
                self.resource['backgroundColor'] = component['backgroundColor']
                self.resource['foregroundColor'] = component['foregroundColor']
                self.resource['borderBottomColor'] = component['borderColor']
                self.resource['borderTopColor'] = component['borderColor']
                self.resource['borderLeftColor'] = component['borderColor']
                self.resource['borderRightColor'] = component['borderColor']

    def _reload_resource(self):
        """
        Доопределяем ресурс.
        """
        self.resource['isSort'] = self.isSort
            
    def _init_template_resource(self):
        """
        Инициализация ресурса шаблона.
        """
        self._templRes = resource

    def init_component(self, context=None):
        """
        Инициализация компонента. Вызывается парсером после создания компонента.
        """
        if context:
            print('#### init_component cornenrs=', self.round_corner, self._reg_objects)
            for cell in self._reg_objects.values():
                if cell.type == 'HeadCell':
                    cell.SetRoundCorners(tuple(self.round_corner))
                    cell.SetLabel(self.label)
                    cell.shortHelpString = self.shortHelpString
                    
                    if not self.przn_border[0]:
                        cell.leftColor = None
                    if not self.przn_border[1]:
                        cell.topColor = None
                    if not self.przn_border[2]:
                        cell.rightColor = None
                    if not self.przn_border[3]:
                        cell.bottomColor = None

                    break
    
    ###BEGIN EVENT BLOCK
    ###END EVENT BLOCK
    
def test(par=0):
    """
    Тестируем класс CStdLabelCell.
    """
    
    from ic.components import ictestapp
    app = ictestapp.TestApp(par)
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)

    ################
    # Тестовый код #
    ################
        
    frame.Show(True)
    app.MainLoop()
    
if __name__ == '__main__':
    test()