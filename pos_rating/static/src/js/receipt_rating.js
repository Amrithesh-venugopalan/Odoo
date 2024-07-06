/** @odoo-module */
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
   export_for_printing() {
       const result = super.export_for_printing(...arguments);
       const data=this.orderlines
       result.orderlines.map((order,index)=>order.prodRating=data[index].product.product_rating)
       return result;
   },
});