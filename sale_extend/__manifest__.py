# -*- coding: utf-8 -*-

{
    'name': 'HB Solutions product',
    'version': '13.0.1',
    'category': 'extra',
    'description': """
    """,
    'author': 'Andema',
    'website': '',
    'depends': [
        'base','product','sale_management','account_accountant','account','stock','purchase_stock','purchase','account_reports',
    ],
    "data": [
        'views/sale.xml',
        'wizard/account_validate_move_view.xml',
    ],
    'license': 'AGPL-3',
    'demo_xml': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: