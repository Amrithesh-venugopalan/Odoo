# -*- coding: utf-8 -*-

{
    'name': "Import Order Lines",
    'version': '17.0.1.0.0',
    'depends': ['base','sale'],
    'author': "Amrithesh",
    'category': 'Category',
    'description': """
    Import order lines
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_order_lines_wizard.xml',
        'view/inherited_sale_order_form_view.xml'
    ],
    'installable': True,
    'auto_install':False,
}
