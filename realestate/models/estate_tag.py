from odoo import fields, models


class Estate_type(models.Model):
    _name = 'estate.tag'
    _description = 'estate property tag'
    name = fields.Char(string='Tag Name')
