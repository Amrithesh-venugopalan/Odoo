# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route


class PropertySnippet(Controller):
    """controller for property snippet"""

    @route(['/property_management_snippet'], type="json", auth="user", website=True)
    def all_properties(self):
        """function to retrieve details of latest four properties"""
        properties = request.env['property.management.properties'].search_read(
            [], ['name', 'property_img', 'create_date'],
            order='create_date desc')
        return properties

    @route('/show_property/<int:id>', type="http", auth="user", website=True)
    def show_property_details(self, id):
        """function to render the chosen property"""
        property_record = request.env['property.management.properties'].browse(id)
        return request.render('property_management.product_details', {'record': property_record})

    @route('/property_snippet', type='http', auth='user', website=True)
    def show_property_snippet(self):
        """function to render website snippet page"""
        return request.render('property_management.property_snippet_template')
