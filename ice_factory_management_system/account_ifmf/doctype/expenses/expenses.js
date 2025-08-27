// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Expenses", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Expense Item Child", {
    price: function(frm, cdt, cdn) {
        calculate_sub_total(frm, cdt, cdn);
    },
    quantity: function(frm, cdt, cdn) {
        calculate_sub_total(frm, cdt, cdn);
    }
});

function calculate_sub_total(frm, cdt, cdn) {
    let row = locals[cdt][cdn];  // get current child row
    let sub_total = (row.price || 0) * (row.quantity || 0);

    // update sub_total and total_amount fields
    frappe.model.set_value(cdt, cdn, 'sub_total', sub_total);
    frappe.model.set_value(cdt, cdn, 'total_amount', sub_total);
    update_summary(frm);
}

function update_summary(frm) {
    let total_quantity = 0;
    let total_amount = 0;
     

    (frm.doc.expense_items || []).forEach(row => {
        total_amount += row.total_amount || 0;
        total_quantity += row.quantity || 0;
    });

    frm.set_value('total_quantity', total_quantity);
    frm.set_value('total_amount', total_amount);

    frm.set_value('total_payment', 0);
    
     frm.set_value('balance', total_amount - (frm.doc.total_payment || 0));


}
