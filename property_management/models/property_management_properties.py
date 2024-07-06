# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PropertyManagementProperties(models.Model):
    """class for managing customer properties"""

    _name = 'property.management.properties'
    _description = 'Property Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', help='name of the property')
    address_street = fields.Char(string='Street')
    address_city = fields.Char(string='City')
    description = fields.Text(string='Description')
    property_record_count = fields.Integer(compute='_compute_property_record_count')
    rent = fields.Float(string='Rent', help="property's rental cost")
    legal_amount = fields.Float(string='Legal Amount', help="property's lease cost")
    property_img = fields.Image(string='Image of property')
    built_date = fields.Date(string='Built date', help='date at which property is built')
    can_be_sold = fields.Boolean(string='Can Be Sold', help='defines whether the property can be sold or not')
    property_state = fields.Selection(string='Property State', tracking=True, required=True,
                                      selection=[('draft', 'Draft'), ('rented', 'Rented'), ('leased', 'Leased'),
                                                 ('sold', 'Sold')
                                                 ],
                                      default='draft')
    address_country_id = fields.Many2one('res.country', string='Country', required=True)
    address_state_id = fields.Many2one('res.country.state', string='State')
    property_owner_id = fields.Many2one('res.partner', string='Property Owner', copy=False)
    property_facilities_ids = fields.Many2many('property.management.tags', string='Property Facilities')
    active = fields.Boolean(string='Active', default=True)

    def _compute_property_record_count(self):
        """function to compute number of records for a property"""
        self.property_record_count = self.env['property.rent.lease.management'].search_count(
            [('property_ids.props_id', '=', self.name)]
        )

    @api.ondelete(at_uninstall=False)
    def _ondelete_properties(self):
        """function for deleting related order lines from rent lease record"""
        for rec_id in self:
            deleted_record_id = rec_id.id
            for prop_rec in self.env['property.order.lines'].search([('props_id', '=', deleted_record_id)]):
                prop_rec.unlink()
            for inv_rec in self.env['account.move.line'].search([('name', '=', rec_id.name)]):
                inv_rec.unlink()

    def get_rent_lease(self):
        """function for returning all related rent lease records"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'name',
            'view_mode': 'tree,form',
            'res_model': 'property.rent.lease.management',
            'domain': [('property_ids.props_id', '=', self.name)],
            'context': "{'create': False}"
        }
