# -*- coding: utf-8 -*-

{
    'name': "Employee Level",
    'version': '17.0.1.0.0',
    'depends': ['base','hr'],
    'author': "Amrithesh",
    'description': """
    Employee Level
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/inherited_employee_form_view.xml',
        'view/employee_level_view.xml',
        'view/employee_level_menu.xml',
    ],
    'installable': True,
    'auto_install':False,
}
