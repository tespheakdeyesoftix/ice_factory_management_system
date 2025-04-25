// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Journal Entry", {
	payment_type(frm) {
        frappe.call({
            method: 'ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate.get_exchange_rate',
            args: {
               currency: frm.doc.currency
            },
            callback: (r) => {
                frm.set_value("input_amount", 0);
                frm.set_value("exchange_rate", r.message.exchange_rate);
            }
        })
    },
    input_amount(frm) {
        update_transfer_amount(frm)
    },
});

function update_transfer_amount(frm) {
    frm.set_value("transfer_amount", ((frm.doc.input_amount || 0) / (frm.doc.exchange_rate || 1)));
}
