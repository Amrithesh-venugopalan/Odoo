# -*- coding: utf-8 -*-

{
    'name': "POS Rating",
    'version': '17.0.1.0.0',
    'depends': ['base', 'product','point_of_sale'],
    'author': "Amrithesh",
    'description': """
    POS Rating
    """,
    'data': [
        'view/inherited_product_product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_rating/static/src/js/receipt_rating.js',
            'pos_rating/static/css/product_rating.css',
            'pos_rating/static/src/xml/inherited_pos_productcard_attributes.xml',
            'pos_rating/static/src/xml/inherited_pos_product_card_view.xml',
            'pos_rating/static/src/xml/inherited_pos_receipt_form.xml',
        ],
    }
}
