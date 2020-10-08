# -*- coding: utf-8 -*-
{
    'name': 'Synchronisation des factures et paiements',
    'version': '12.0',
    'description': " Synchronisation des factures et paiements ",
    'author': 'ANDEMA',
    'website': 'www.andemaconsulting.com',
    'depends': ['base', 'product_extend', 'account', 'sale_extend', 'fiscal_sync_link'
                  ],
    'data': [
        'security/synch_security.xml',
        'views/res_company_views.xml',
        'wizard/account_invoice_synch_views.xml',
        'wizard/account_payment_synch_views.xml',

        ],
    'demo': [],
    'test': [],
    'installable': True,
}