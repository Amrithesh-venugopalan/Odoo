# -*- coding: utf-8 -*-
from odoo import fields
from odoo.http import request, Controller, route


class WebsiteSaleClear(Controller):
    """controller for clearing website cart"""

    @route('/website/clear/cart', type="json", auth="user", website=True, csrf=False)
    def clear_website_cart(self, **post):
        """function to clear cart items from website"""
        sale_order_id = post.get('sale_order_id')
        website_sale_order = request.env['sale.order'].browse(sale_order_id)
        website_sale_order.update({
            'order_line': [(fields.Command.clear())]
        })
