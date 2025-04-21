// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Payment", {
    payment_type(frm) {
        frappe.call({
            method: 'ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate.get_exchange_rate',
            args: {
               currency: frm.doc.currency
            },
            callback: (r) => {
                frm.set_value("exchange_rate", r.message);
                set_amount_to_zero(frm);
            }
        })
    },
    input_amount(frm) {
        update_payment_amount(frm)
    },
    sale(frm) {
        set_amount_to_zero(frm);
    },
    write_off_amount(frm) {
        update_payment_amount(frm)
    }
});
function set_amount_to_zero(frm) {
    frm.set_value("input_amount", 0);
    frm.set_value("payment_amount", 0);
}

function update_payment_amount(frm) {
    if( frm.doc.input_amount == 0 && frm.doc.write_off_amount == 0) {
        frm.set_value("payment_amount",0);
    }
    else{
        let payment_amount = ((frm.doc.input_amount || 0) + (frm.doc.write_off_amount || 0)) / (frm.doc.exchange_rate || 1);
        frm.set_value("payment_amount", payment_amount);
        frm.set_value("payment_balance", (frm.doc.balance - payment_amount)*(frm.doc.exchange_rate || 1));
    }   
}
