from odoo import fields, models


class Estate_offer(models.Model):
    _name = 'estate.offer'
    _description = 'estate property offer'
    _rec_name = 'price'
    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True)
    property_id = fields.Many2one('estate', string='Property', required=True)

