// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Payment", {
    refresh(frm) {
        get_default_account(frm);
    },
    outlet(frm) {
        get_default_account(frm);
        get_payment_type_accounts(frm);
    },
    payment_type(frm) {
        get_payment_type_accounts(frm);
    },
    input_amount(frm) {
        update_total_amount(frm)
    },
    sale(frm) {
        set_amount_to_zero(frm);
    },
    write_off_amount(frm) {
        update_total_amount(frm)
    }
});

function set_amount_to_zero(frm) {
    frm.set_value("input_amount", 0);
    frm.set_value("total_amount", 0);
    frm.set_value("payment_balance", frm.doc.currency_symbol + " " + ((frm.doc.balance - frm.doc.total_amount)*(frm.doc.exchange_rate || 1)).toLocaleString());
}

function update_total_amount(frm) {
    if( frm.doc.input_amount == 0 && frm.doc.write_off_amount == 0) {
        frm.set_value("total_amount",0);
    }
    else{
        let total_amount = ((frm.doc.input_amount || 0) + (frm.doc.write_off_amount || 0)) / (frm.doc.exchange_rate || 1);
        frm.set_value("total_amount", total_amount);
    }   
    frm.set_value("payment_balance", frm.doc.currency_symbol + " " + ((frm.doc.balance - frm.doc.total_amount)*(frm.doc.exchange_rate || 1)).toLocaleString());
}

function get_payment_type_accounts(frm) {
    frappe.call({
            method: 'ice_factory_management_system.selling_ifms.doctype.sale_payment.sale_payment.get_payment_default_account',
            args: {
                outlet: frm.doc.outlet,
                payment_type: frm.doc.payment_type
            },
            callback: (r) => {
                if( r.message) {
                    frm.set_value("exchange_rate", r.message.exchange_rate);
                    frm.set_value("currency_symbol", r.message.symbol);
                    frm.set_value("account_paid_to", r.message.account);
                    set_amount_to_zero(frm);
                }
            }
        })
}

function get_default_account(frm){
    frappe.call({
        method: 'ice_factory_management_system.system_setting.doctype.outlet.outlet.get_default_accounts',
        args: {
            outlet: frm.doc.outlet
        },
        callback: (r) => {
            if (r.message) {
                frm.set_value("account_paid_from", r.message.receivable_account);
                frm.set_value("write_off_account", r.message.write_off_account);
            }
        }
    })
}