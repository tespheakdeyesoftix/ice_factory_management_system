// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Borrow Product", {
    refresh(frm) {
        if (!frm.is_new()) {
            if (frm.doc.docstatus == 1 && frm.doc.transaction_type ==="Borrow" && frm.doc.balance>0) {
                frm.add_custom_button(__("Return Product"), function () {
                    returnProduct(frm)
                });
            }
            setIntro(frm)
            setIndicator(frm);
        }
    },
});

function setIntro(frm){
    if(frm.doc.transaction_type=="Return"){
        
        frm.set_intro(__(`This is a return product transaction`));
        
    }
}

function setIndicator(frm){
        if(frm.doc.transaction_type !="Borrow") return;

         frm.dashboard.add_indicator(
                __("Borrow Quantity: {0}", [frappe.format(frm.doc.quantity,{"fieldtype":"Float"})]),
                "blue"  
            );
            
            frm.dashboard.add_indicator(
                __("Return Quantity: {0}", [frappe.format(frm.doc.return_quantity,{"fieldtype":"Float"})]),
                "green"  
            );
            
            frm.dashboard.add_indicator(
                __("Balance: {0}", [frappe.format(frm.doc.balance,{"fieldtype":"Float"})]),
                "red"  
            );

            // borrow duration
            const posting_date = frappe.datetime.str_to_obj(frm.doc.posting_date);
            const today = frappe.datetime.str_to_obj(frm.doc.last_return_date ||  frappe.datetime.get_today());

            const diff_days = frappe.datetime.get_day_diff(today, posting_date);
            if (diff_days>0){
                frm.dashboard.add_indicator(
                __("Borrow Duration: {0} Day(s)", [diff_days]),
                "red"  
            );
            }
            

     
    }
            
            

function returnProduct(frm){
    let d = new frappe.ui.Dialog({
    title: __('Add new return transaction'),
    fields: [
        {
            label: __('Posting Date'),
            fieldname: 'posting_date',
            fieldtype: 'Date',
            default: frappe.datetime.nowdate()
        },
        {
            label: __('Return Quantity'),
            fieldname: 'quantity',
            fieldtype: 'Float',
            default: frm.doc.balance
        },
        {
            label: __('Note'),
            fieldname: 'note',
            fieldtype: 'Small Text'
        }

    ],
    primary_action_label: __('Return'),
    primary_action(values) {
        if (values.quantity>frm.doc.balance){
            frappe.throw(__("Return quantity can not be greater than borrow quantity"))
            return
        }
        frappe.dom.freeze(__("Saving..."));

        frm.call("on_return_product",{data:values}).then(r=>{
             d.hide();
            frm.reload_doc()
            frappe.dom.unfreeze();
           
        }).catch(err=>{
              frappe.dom.unfreeze();
        })
        
       
    }
});

d.show();

}