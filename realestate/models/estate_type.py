from odoo import fields, models

class Estate_type(models.Model):
    _name = 'estate.type'
    _description = 'estate property type'
    name = fields.Char(string='Property Type', required=True)

