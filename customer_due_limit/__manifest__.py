# -*- coding: utf-8 -*-

{
    'name': "Customer Due Limit",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale'],
    'author': "Amrithesh",
    'description': """
    Customer Due Limit
    """,
    'data': [
        'view/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale._assets_pos': [
            'customer_due_limit/static/src/js/customer_due_limit.js'
        ],
    }
}
