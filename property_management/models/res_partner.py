# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartners(models.Model):
    _inherit = 'res.partner'
    properties_owned_ids = fields.Many2many('property.management.properties', string='Properties Owned',
                                            compute="_compute_partner_properties")

    def _compute_partner_properties(self):
        """function to find and display all properties of a partner"""
        for rec in self:
            all_ids = []
            for record in self.env['property.management.properties'].search([('property_owner_id', '=', rec.id)]):
                all_ids.append(record.id)
            rec.write({'properties_owned_ids': all_ids})
