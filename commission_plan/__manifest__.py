# -*- coding: utf-8 -*-

{
    'name': "Commission Plan",
    'version': '17.0.1.0.0',
    'depends': ['base','crm','sale'],
    'author': "Amrithesh",
    'description': """
    Commission plan
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/commission_plan_crm_commission_view.xml',
        'views/inherited_res_users_form_view.xml',
        'views/inherited_crm_team_form_view.xml',
        'views/inherited_sale_order_form_view.xml',
        'views/commission_plan_menu.xml',
    ],
    'application': True,
}
