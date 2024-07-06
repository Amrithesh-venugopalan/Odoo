from odoo import fields, models, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    commission_amount = fields.Float(string='Commission', compute='_compute_commission_amount')

    @api.depends('order_line', 'user_id', 'team_id')
    def _compute_commission_amount(self):
        for rec in self:
            total_commission = 0
            rec.commission_amount = 0
            if rec.user_id and rec.user_id.commission_plan_id or rec.team_id and rec.team_id.commission_plan_id:
                commission_plan = rec.user_id.commission_plan_id if rec.user_id.commission_plan_id else rec.team_id.commission_plan_id
                if commission_plan.from_date <= datetime.today().now() <= commission_plan.to_date:
                    if commission_plan.type == 'product_wise':
                        commission_products = commission_plan.product_wise_rate_ids.mapped('product_id').mapped(
                            'id')
                        for order in rec.order_line:
                            if order.product_template_id.id in commission_products:
                                price = commission_plan.product_wise_rate_ids.filtered(
                                    lambda x: x.product_id.id == order.product_template_id.id)
                                total_commission += (
                                        order.price_unit * order.product_uom_qty * price.rate * 0.01)
                                rec.commission_amount = price.maximum_commission_amount if total_commission > price.maximum_commission_amount else total_commission
                    else:
                        commission_rates = commission_plan.revenue_wise_rate_ids
                        untaxed_amount = rec.amount_untaxed
                        if commission_plan.revenue_type == 'straight':
                            for index, rate in enumerate(commission_rates):
                                if rate.from_amount + 1 <= untaxed_amount <= rate.to_amount or index == len(
                                        commission_rates) - 1 and untaxed_amount >= commission_rates[-1].to_amount:
                                    total_commission += (untaxed_amount * rate.rate * 0.01)
                            rec.commission_amount = total_commission
                        else:
                            for index, rate in enumerate(commission_rates):
                                if rate.to_amount < untaxed_amount:
                                    total_commission += (rate.to_amount - rate.from_amount) * rate.rate * 0.01
                                elif rate.from_amount <= untaxed_amount <= rate.to_amount:
                                    total_commission += (untaxed_amount - rate.from_amount) * rate.rate * 0.01
                            rec.commission_amount = total_commission

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.user_id:
            self.user_id.update({
                'all_commission_ids': [(fields.Command.create({
                    'sale_order_id': self.id,
                    'user_commission_amount': self.commission_amount
                }))]
            })
        elif self.team_id:
            self.team_id.update({
                'all_team_commission_ids': [(fields.Command.create({
                    'sale_team_order_id': self.id,
                    'team_commission_amount': self.commission_amount
                }))]
            })
        return res
