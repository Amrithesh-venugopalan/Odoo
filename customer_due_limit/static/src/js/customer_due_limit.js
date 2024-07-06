/** @odoo-module */
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { onWillStart,onWillRender,onRendered,onMounted,onUnmounted,onWillUpdateProps,onWillPatch,onPatched,onWillUnmount,onWillDestroy,onError } from "@odoo/owl";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");

        onWillRender(() => {
          console.log('on will render')
        });
        onWillStart(async () => {
            console.log('on will start')
        });
        onRendered(() => {
          console.log('on rendered')
        });
        onMounted(() => {
          console.log('on mounted')
        });
        onWillUpdateProps(nextProps => {
          console.log('on will update props')
        });
        onWillPatch(() => {
          console.log('on will patch')
        });
        onPatched(() => {
          console.log('on patched')
        });
        onWillUnmount(() => {
          console.log('on will unmount')
        });
        onWillDestroy(() => {
          console.log('on will destroy')
        });
        onError(() => {
          console.log('on error')
        });
    },
    async validateOrder(isForceValidate) {
        var current_customer=this.currentOrder.get_partner()?this.currentOrder.get_partner():false
        var credit_payment_sum=this.currentOrder.paymentlines.filter((x)=>x.payment_method.type=="pay_later").reduce((sum,a)=>sum+a.amount,0)
        if (current_customer && credit_payment_sum){
            var credit_limit=current_customer.customer_due_limit
            var total_credit_given= await this.orm.call("res.partner","get_current_credit",[[current_customer.id]])
//            used orm call to get current credit limit from res partner
            if(credit_payment_sum && total_credit_given+credit_payment_sum<=credit_limit){
                await this.orm.call("res.partner","update_current_credit",[[current_customer.id]],{amount:credit_payment_sum})
//                used orm call to update current credit limit from res partner
                await super.validateOrder(...arguments);
            }
            else{
                await this.popup.add(ErrorPopup, {
                    title: _t("Warning"),
                    body: _t(`${current_customer.name} current credit ${total_credit_given} will Exceed limit ${credit_limit}`),
                });
            }
        }
        else{
            await super.validateOrder(...arguments);
        }
    },
    });