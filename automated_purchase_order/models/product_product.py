from odoo import models

from odoo import fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_product_automated_po(self):
        return {
            'name': 'Automated Purchase Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.automated.purchase.order',
            'context': {
                'default_product_vendor_id': None if len(self.seller_ids) == 0 else self.seller_ids[
                    0].partner_id.id},
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
