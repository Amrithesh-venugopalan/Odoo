# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Extends res partner model to add credit information"""
    _inherit = 'res.partner'

    customer_due_limit = fields.Float(string='Customer credit limit')
    current_credit = fields.Float(string='Current credit', readonly=True)

    def get_current_credit(self):
        """function to return current credit using orm calls"""
        return self.current_credit

    def update_current_credit(self, amount):
        """function to update current credit using orm calls"""
        self.current_credit += amount
        return self.current_credit
