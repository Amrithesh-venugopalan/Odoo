# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    """Extends POS session model"""
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'] += ['customer_due_limit','current_credit']
        return result
