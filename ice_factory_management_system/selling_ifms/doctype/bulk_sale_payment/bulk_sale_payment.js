// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Sale Payment", {
    refresh(frm) {
        frm.set_query("sale", "sales", function () {
            return {
                filters: [
                    ["Sale", "customer", "=", frm.doc.customer],["Sale", "status", "!=", "Paid"],
                ]
            }
        });
    },
    get_sales(frm) {
        frappe.call({
            method: 'ice_factory_management_system.selling_ifms.doctype.sale.sale.get_sales',
            args: {
                customer: frm.doc.customer,
                outlet: frm.doc.outlet,
                start_date: frm.doc.start_date,
                end_date: frm.doc.end_date
            },
            callback: (r) => {
                if(r.message.length == 0){
                    frappe.msgprint(__("No Sale Found"));
                    return;
                }
                else{
                    frm.clear_table("sales");
                    r.message.forEach((r => {
                        doc = frm.add_child("sales");
                        doc.posting_date = frm.doc.posting_date;
                        doc.sale = r.sale;
                        doc.sale_amount = r.total_amount;
                        doc.amount = r.balance;
                        doc.balance = r.balance;
                        doc.payment_type = frm.doc.payment_type;
                        doc.currency = frm.doc.currency;
                        doc.exchange_rate = frm.doc.exchange_rate;
                    }))
                    frm.refresh_field('sales');
                    update_totals(frm)
                }
            }
        })
    },
	payment_type(frm) {
        frm.set_value("payment_amount", 0);
        frappe.call({
            method: 'ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate.get_exchange_rate',
            args: {
               currency: frm.doc.currency
            },
            callback: (r) => {
                frm.set_value("exchange_rate", r.message);
            }
        })
    },
    payment_amount(frm) {
        update_allocated_amount(frm);
    }
});
frappe.ui.form.on("Bulk Sale", {
    sale(frm,cdt,cdn) {
        cal_row_sale(frm,cdt,cdn);
    },
    input_amount(frm,cdt,cdn) {
        cal_row_sale(frm,cdt,cdn);
    },
    write_off_amount(frm,cdt,cdn) {
        cal_row_sale(frm,cdt,cdn);
    }
});

function cal_row_sale(frm,cdt,cdn) {
    let row = locals[cdt][cdn];
    let payment_amount = ((row.input_amount || 0) + (row.write_off_amount || 0)) / (frm.doc.exchange_rate || 1);
    frappe.model.set_value(cdt, cdn, "payment_amount", payment_amount);
    frappe.model.set_value(cdt, cdn, "balance", row.amount-payment_amount);
    update_totals(frm);
}

function update_totals(frm) {
    let total_amount = 0;
    let total_payment_amount = 0;
    let total_balance = 0;
    let total_write_off_amount = 0;
    frm.doc.sales.forEach(a => {
        total_amount += a.amount;
        total_payment_amount += a.payment_amount;
        total_balance += a.balance;
        total_write_off_amount += a.write_off_amount;
    });
    frm.set_value("total_invoices", (frm.doc.sales || []).length);
    frm.set_value("total_amount", total_amount);
    frm.set_value("total_payment_amount", total_payment_amount);
    frm.set_value("total_write_off_amount", total_write_off_amount);
    frm.set_value("total_balance", total_balance);
}

function update_allocated_amount(frm){
    paid_amount = frm.doc.payment_amount/frm.doc.exchange_rate
    if((frm.doc.sales || []).length > 0){
        frm.doc.sales.forEach(r => {
            if(paid_amount<r.amount){
                r.input_amount = paid_amount * frm.doc.exchange_rate
                r.payment_amount = paid_amount
            }
            else{
                r.input_amount = r.amount * frm.doc.exchange_rate
                r.payment_amount = r.amount
            }
            r.balance = r.amount - r.payment_amount
            paid_amount = paid_amount - r.payment_amount
        });
        frm.refresh_field("sales")
        update_totals(frm);
    }
    else{
        
    }
}