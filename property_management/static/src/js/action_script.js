/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from '@web/legacy/js/public/public_widget';

var rentLeaseAmountInput=$('.rent_lease_amount')

function calculateRentLeaseAmount() {
    var agreementType=$(".agreement_type").val()
    var sum=0
    var find_attr=''
    if (agreementType=='rent') {
        find_attr='data-rent'
    } else if (agreementType=='lease') {
        find_attr='data-lease'
    }
    var all_records=$('[data-checked = "true"]')
    if (find_attr && all_records['length']>0){
            for (var i=0;i<all_records['length'];i++){
        sum+=parseInt(all_records[i].getAttribute(find_attr))
        }
    }
   return sum
}

publicWidget.registry.PropertyWebsiteForm=publicWidget.Widget.extend({
    selector:'.form-container',
    events:{
        'change .property-check-box': '_onSelectProperty',
        'change .agreement_type':'_onSelectAgreementType',
        'click .new-customer-btn':'_onSelectCustomerBtn',
        'click .form-btn-submit':'_onSelectFormSubmitBtn'
    },
    _onSelectProperty:function(e){
        e.target.setAttribute('data-checked',e.target.getAttribute('data-checked')=='false'?'true':'false')
        rentLeaseAmountInput.prop('value',calculateRentLeaseAmount())
    },
    _onSelectAgreementType:function(e){
        rentLeaseAmountInput.prop('value',calculateRentLeaseAmount())
    },
    _onSelectCustomerBtn:function(e){
        $('#myModal').modal('show')
    },
    _onSelectFormSubmitBtn: async function(){

        var all_properties=this.$el.find('.property-check-box')
        var input_from_date=this.$el.find('#input-from-date').val()
        var input_to_date=this.$el.find('#input-to-date').val()
        var input_tenant_id=this.$el.find('.tenant-input').val()
        var input_agreement_type=this.$el.find('.agreement_type').val()

        var all_prop_list=[]
        for (var key in all_properties){
            var element=all_properties[key]
            if (key<all_properties['length'] && element.getAttribute('data-checked')=='true'){
                all_prop_list.push(parseInt(element.getAttribute('value')))
            }
        }
        let values={
           'properties':all_prop_list,
           'agreement_type':input_agreement_type,
           'tenant_id':input_tenant_id,
           'from_date':input_from_date,
           'to_date':input_to_date,
           'from_date':input_from_date
        }
        if (all_prop_list.length>0 && input_from_date && input_to_date && input_tenant_id && input_agreement_type){

            await jsonrpc('/jsonrpc/test',values).then((result)=>{
            window.location.href = '/property_management'
        })
        }
        else{
            this.$el.find('#myDialogModal').modal('show')
        }
    }
})


