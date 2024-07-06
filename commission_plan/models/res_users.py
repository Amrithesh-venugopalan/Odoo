# -*- coding: utf-8 -*-
from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'

    commission_plan_id = fields.Many2one('crm.commission', string="Commission Plan")
    all_commission_ids = fields.One2many('commission.amount.lines', 'commission_amount_id', string="All commission")


class CommissionAmountLines(models.Model):
    _name = 'commission.amount.lines'

    commission_amount_id = fields.Many2one('res.users')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    user_commission_amount = fields.Float(string='Amount')
