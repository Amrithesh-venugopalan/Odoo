# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    total_count = fields.Integer(string='Quantities Sold', compute="_compute_total_count")

    def _compute_total_count(self):
        for rec in self:
            rec.total_count = 0
            count = 0
            for sale in self.env['sale.order'].search([('state', '=', 'draft')]):
                for product in sale.order_line:
                    if product.product_template_id.id == rec.id:
                        count += product.product_uom_qty
            rec.total_count = count

    @api.onchange('list_price')
    def change_draft_sale_order_price(self):
        print('triggering')
        print(self)
        print(self._origin)
        target_id=self._origin
        for rec in self.env['sale.order'].search([('state', '=', 'draft')]):
            rec.order_line.search([('product_template_id.id','=',target_id.id)]).price_unit=self.list_price

