{
    'name': "Real estate",
    'version': '1.0',
    'depends': ['base', 'web','contact'],
    'author': "Amrithesh",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
        'view/estate_property_view.xml',
        'view/estate_property_type_view.xml',
        'view/estate_property_tag_view.xml',
        'view/estate_property_offer.xml',
        'view/estate_menu_view.xml'

    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
