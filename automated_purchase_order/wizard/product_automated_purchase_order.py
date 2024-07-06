from odoo import models, fields, api, Command
from datetime import datetime


class ProductAutomatedPurchaseOrder(models.TransientModel):
    _name = 'product.automated.purchase.order'

    product_chosen_id = fields.Many2one('product.product', string='Chosen Product')
    product_quantity = fields.Integer(string='Quantity', default=1)
    product_price = fields.Float(string='Price', related='product_chosen_id.list_price')
    product_total_price = fields.Float(string='Total Price')
    product_vendor_id = fields.Many2one('res.partner', string='Vendor')

    @api.onchange('product_quantity')
    def _onchange_product_total_price(self):
        self.product_total_price = self.product_price * self.product_quantity

    def action_confirm_po(self):
        purchase_order = self.env['purchase.order'].search(
            [('partner_id', '=', self.product_vendor_id.id), ('state', '=', 'draft')], limit=1)
        if purchase_order:
            purchase_order.write({
                'order_line': [fields.Command.create({
                    'product_id': self.product_chosen_id.id,
                    'product_qty': self.product_quantity,
                    'price_unit': self.product_price
                })]
            })
        else:
            purchase_order = self.env['purchase.order'].create({
                'partner_id': self.product_vendor_id.id,
                'date_order': datetime.today().now(),
                'order_line': [Command.create({
                    'product_id': self.product_chosen_id.id,
                    'product_qty': self.product_quantity,
                    'price_unit': self.product_price
                })]
            })
        purchase_order.button_confirm()

