# -*- coding: utf-8 -*-

{
    'name': 'HB Solutions product',
    'version': '11.0.1',
    'category': 'extra',
    'description': """
    """,
    'author': 'Andema',
    'website': '',
    'depends': [
        'base',
        'product','mrp','stock','sale'
    ],
    "data": [
        'data/default_code_seq.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/CoreNumber.xml',
        'views/CPU.xml',
        'views/FormFactor.xml',
        'views/Grade.xml',
        'views/GraphicCardSize.xml',
        'views/GraphicCardTechnology.xml',
        'views/HardDiskSize.xml',
        'views/HardDiskTechnology.xml',
        'views/Keyboard.xml',
        'views/Model.xml',
        'views/Maker.xml',
        'views/RamSize.xml',
        'views/RamTechnology.xml',
        'views/ScreenResolution.xml',
        'views/ScreenSize.xml',
        'views/Menu.xml',
        'report/product_templates.xml',
        'report/product_reports.xml',
    ],
    'license': 'AGPL-3',
    'demo_xml': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: