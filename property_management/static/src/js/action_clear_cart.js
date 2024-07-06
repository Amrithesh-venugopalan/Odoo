/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";
import { jsonrpc } from "@web/core/network/rpc_service";

WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        'click .clear-website-order-line-btn':'_onSelectClearCartBtn',
    }),
    _onSelectClearCartBtn: async function(ev){
        var order_id=this.$el.find('#order_total').find('.monetary_field').attr('data-oe-id')
        await jsonrpc('/website/clear/cart',{'sale_order_id':parseInt(order_id)}).then((result)=>{
            window.location.reload()
        })
    }
})
