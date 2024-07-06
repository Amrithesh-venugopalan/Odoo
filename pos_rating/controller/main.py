# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route


class PosRatingController(Controller):
    """Pos rating controller"""

    @route('/jsonrpc/test', type='json', auth='user', website=True)
    def pos_rating_form(self, **post):
        """function to set product rating in pos"""
        try:
            current_product_rating = request.env['product.product'].browse(
                int(post['currentProductId'])).product_rating
            return current_product_rating
        except:
            print('error')
