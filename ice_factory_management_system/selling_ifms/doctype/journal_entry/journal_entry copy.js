// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Journal Entry", {
    refresh(frm) {
        get_account(frm)
    },
	payment_type(frm) {
        frappe.call({
            method: 'ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate.get_exchange_rate',
            args: {
               currency: frm.doc.currency
            },
            callback: (r) => {
                frm.set_value("input_amount", 0);
                frm.set_value("exchange_rate", r.message.exchange_rate);
                update_transfer_amount(frm)
            }
        })
    },
    transfer_type(frm) {
        get_account(frm)
    },
    bank(frm){
        frm.set_value("account_transfer_to",frm.doc.account)
    },
    input_amount(frm) {
        update_transfer_amount(frm)
    },
    entry_type(frm) {
        frm.set_value("payment_type","")
        frm.set_value("transfer_type","")
        frm.set_value("exchange_rate",1)
        frm.set_value("account_transfer_from","")
        frm.set_value("account_transfer_to","")
    }
});

function get_account(frm) {
    if (frm.doc.transfer_type == "Cash") {
        frm.set_value("bank", "")
        frappe.call({
            method: 'ice_factory_management_system.selling_ifms.doctype.journal_entry.journal_entry.get_accounts',
            callback: (r) => {
                frm.set_value("account_transfer_to", r.message.cash_transfer_account);
            }
        })
    }
}

function update_transfer_amount(frm) {
    frm.set_value("total_amount", ((frm.doc.input_amount || 0) / (frm.doc.exchange_rate || 1)));
}
