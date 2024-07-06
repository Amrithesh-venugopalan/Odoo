# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    related_agreement_id = fields.Many2one('property.rent.lease.management', string='Related Agreement')

    def action_post(self):
        """function extended to display chatter message in property rent lease management model"""
        res = super(AccountMove, self).action_post()
        self.env['property.rent.lease.management'].search(
            [('id', '=', self.related_agreement_id.id)]).display_chatter_message(
            message_body=f'Invoice {self.name} validated')
        return res
