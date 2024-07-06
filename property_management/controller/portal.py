# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route
from odoo import fields
from datetime import datetime


class PropertyManagementController(Controller):
    """Property management controller"""

    @route('/property_management', auth='user', website=True)
    def property_management_form(self, **kwargs):
        """function to render related records in the website"""
        tenant_id_log = request.env.user.partner_id.id
        rent_lease_record = request.env['property.rent.lease.management'].sudo().search(
            [('tenant_id', '=', tenant_id_log)])
        values = {
            'records': rent_lease_record
        }
        return request.render('property_management.property_management_template', values)

    @route('/show_agreement/details/<int:id>', type="http", auth="user", website=True)
    def show_agreement_details(self, id):
        """function to render the chosen property"""
        agreement_record = request.env['property.rent.lease.management'].browse(id)
        return request.render('property_management.agreement_details', {'record': agreement_record})

    @route('/property_management/create/new_customer', auth='user', website=True)
    def show_modal(self, **post):
        """function to show new customer modal"""
        request.env['res.partner'].sudo().create({'name': post['name'], 'email': post['email']})
        return request.redirect('/property_management/create')

    @route('/property_management/create', auth='user', website=True)
    def web_form_submit(self, **post):
        """function to re-render web form on submit"""
        all_tenants = request.env['res.partner'].sudo().search([])
        all_properties = request.env['property.management.properties'].sudo().search([('property_state', '=', 'draft')])
        values = {
            'tenants': all_tenants,
            'properties': all_properties,
            'from_date': str(datetime.today().date()),
        }
        return request.render('property_management.website_form_template', values)

    @route('/jsonrpc/test', type='json', auth='user', website=True)
    def json_test(self, **post):
        """function for creating new rent lease record"""
        my_time = datetime.min.time()
        new_lst = post['properties']
        request.env['property.rent.lease.management'].sudo().create({
            'agreement_type': post.get('agreement_type'),
            'tenant_id': int(post.get('tenant_id')),
            'agreement_start_date': datetime.combine(datetime.strptime(post.get('from_date'), "%Y-%m-%d"), my_time),
            'agreement_end_date': datetime.combine(datetime.strptime(post.get('to_date'), "%Y-%m-%d"), my_time),
            'property_ids': [(fields.Command.create(
                {'props_id': int(prop_id)}
            )) for prop_id in new_lst]
        })
