{
    'name': "Automated Purchase Order",
    'version': '17.0.1.0.0',
    'depends': ['base','product','purchase'],
    'author': "Amrithesh",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/automated_purchase_order_wizard.xml',
        'view/inherited_product_form_view.xml'
    ],
    'installable': True,
}
