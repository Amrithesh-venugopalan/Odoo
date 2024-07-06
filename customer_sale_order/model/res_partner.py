# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartners(models.Model):
    _inherit = 'res.partner'
    customer_sale_order_ids = fields.Many2many('sale.order', string='Sale Orders', compute='_compute_sale_order')
    customer_product_sale_count = fields.Integer(compute='_compute_product_count')

    def _compute_sale_order(self):
        print('hello',self)
        # for rec in self:
        #     all_ids = self.env['sale.order'].search([('partner_id', '=', rec.id)]).mapped('id')
        #     # rec.write({'customer_sale_order_ids': all_ids})
        #     rec.customer_sale_order_ids = all_ids
        all_ids = self.env['sale.order'].search([('partner_id', '=', self[0].id)]).mapped('id')
        self.customer_sale_order_ids = all_ids

    def _compute_product_count(self):
        for rec in self:
            rec.customer_product_sale_count = 0
            all_products = []
            for record in self.env['sale.order'].search([('partner_id', '=', rec.id), ('state', '=', 'sale')]):
                product = record.order_line.mapped('product_template_id')
                all_products += product
            rec.customer_product_sale_count = len(list(set(all_products)))

    def get_sale_order_record(self):
        all_products = []
        for record in self.env['sale.order'].search([('partner_id', '=', self.id)]):
            product = record.order_line.mapped('product_template_id.id')
            all_products += product
        new_lst = list(set(all_products))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'domain': [('id', 'in', new_lst)],
            'context': "{'create': False}"
        }
