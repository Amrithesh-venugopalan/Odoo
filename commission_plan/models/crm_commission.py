# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CrmCommission(models.Model):
    _name = 'crm.commission'
    _description = 'commission plan'
    #     Field: Name, active, From date and to date,
    name = fields.Char(string="Name")
    active = fields.Boolean(string="Active", default=True)
    from_date = fields.Datetime(string='From')
    to_date = fields.Datetime(string="To")
    type = fields.Selection([('product_wise', 'Product Wise'), ('revenue_wise', 'Revenue Wise')], required=True,
                            copy=False, default='product_wise')
    revenue_type = fields.Selection([('straight', 'Straight'), ('graduated', 'Graduated')], required=True, copy=False,
                                    default="straight")
    revenue_wise_rate_ids = fields.One2many('commission.order.lines', 'commission_id', string="Commission rates")
    product_wise_rate_ids = fields.One2many('commission.product.order.lines', 'product_wise_id')

    @api.onchange('revenue_wise_rate_ids')
    def _onchange_revenue_wise_rate_ids(self):
        for i in range(len(self.revenue_wise_rate_ids)):
            self.revenue_wise_rate_ids[i].sequence = i + 1


class CommissionProductOrderLines(models.Model):
    _name = 'commission.product.order.lines'
    product_wise_id = fields.Many2one('crm.commission')
    product_id = fields.Many2one('product.template', string="Commission Product", required=True)
    product_category_id = fields.Many2one('product.category', string="Product Category", related='product_id.categ_id')
    rate = fields.Float(string='Rate-%')
    maximum_commission_amount = fields.Float(string='Maximum Commission Amount')


class CommissionOrderLines(models.Model):
    _name = 'commission.order.lines'
    commission_id = fields.Many2one('crm.commission')
    sequence = fields.Integer(string='Sequence')
    from_amount = fields.Float(string='From amount')
    to_amount = fields.Float(string='To amount')
    rate = fields.Float(string='Rate')

