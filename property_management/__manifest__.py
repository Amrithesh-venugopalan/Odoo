# -*- coding: utf-8 -*-

{
    'name': "Property Management",
    'version': '17.0.0.1.0',
    'depends': ['base', 'web', 'mail', 'account','sale'],
    'author': "Amrithesh",
    'category': 'Category',
    'description': """
    Property Management App
    """,

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/rent_lease_wizard.xml',
        'data/order_sequence.xml',
        'data/property_demo_data.xml',
        'data/email_template.xml',
        'data/scheduled_action_mail.xml',
        'data/payment_remainder_email_template.xml',
        'report/property_management_reports.xml',
        'report/property_management_templates.xml',
        'view/property_management_properties_view.xml',
        'view/inherited_partner_form_view.xml',
        'view/property_rent_lease_management_view.xml',
        'view/property_management_tags_view.xml',
        'view/property_management_record_template.xml',
        'view/property_management_website_form.xml',
        'view/property_management_website.xml',
        'view/property_snippet_template_view.xml',
        'view/inherited_report_invoice_document.xml',
        'view/inherited_cart_form_view.xml',
        'view/property_details_template.xml',
        'view/property_management_snippet_view.xml',
        'view/property_management_snippet_menu.xml',
        'view/property_management_website_menu.xml',
        'view/property_management_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'property_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'property_management/static/src/js/action_script.js',
            'property_management/static/src/js/action_snippet.js',
            'property_management/static/src/js/action_clear_cart.js',
            'property_management/static/src/xml/dynamic_carousel.xml',
            'property_management/static/css/property_record_template.css',
            'property_management/static/css/website_shop.css',
            'property_management/static/css/property_details_template.css',
            'property_management/static/css/properties_snippet.css',
            'property_management/static/css/property_management.css',
        ]
    },

    'application': True,
    'installable': True,
    'auto_install': False,
}
