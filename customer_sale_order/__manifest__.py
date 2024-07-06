# -*- coding: utf-8 -*-

{
    'name': "Customer Sale Order",
    'version': '17.0.1.0.0',
    'depends': ['base','sale','product'],
    'author': "Amrithesh",
    'description': """
    Customer Sale Order
    """,
    'data': [
        'view/inherited_res_partner_form_view.xml',
        'view/inherited_product_template_form_view.xml'
    ],
    'installable': True,
    'auto_install':False,
}
