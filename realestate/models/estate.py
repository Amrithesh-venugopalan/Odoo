from odoo import fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Estate(models.Model):
    _name = 'estate'
    _description = 'estate properties'
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    property_type_id = fields.Many2one('estate.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.tag', string='Property Tag')
    property_offers_id = fields.One2many('estate.offer', 'property_id', string='Property Offer')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Seller', default=lambda self: self.env.user)
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Float(default=2, string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    active = fields.Boolean(string='Active', default=True)
    status = fields.Selection(string='Status', required=True,
                              selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                         ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                         ('cancelled', 'Cancelled')], default='new')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('east', 'East'), ('north', 'North'), ('south', 'South'), ('west', 'West')],
        help="Garden Orientation Type")

