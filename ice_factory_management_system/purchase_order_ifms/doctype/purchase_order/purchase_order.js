// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Order", {
  onload: function (frm) {

  },
  refresh: function (frm) {
    frm.dashboard.clear_headline();
    
    if (!frm.is_new()) {
      frm.dashboard.add_indicator(
        __("Total Quantity: {0}", [format_number(frm.doc.total_quantity)]),
        "blue"
      );

      frm.dashboard.add_indicator(
        __("Total Cost: {0}", [fmt_money(frm.doc.total_cost)]),
        "blue"
      );
      frm.dashboard.add_indicator(
        __("Total Payment: {0}", [fmt_money(frm.doc.total_payment)]),
        "green"
      );

      frm.dashboard.add_indicator(
        __("Balance: {0}", [fmt_money(frm.doc.balance)]),
        "red"
      );
    }
  },
});

frappe.ui.form.on("Purchase Order Products", {
  quantity: function (frm, cdt, cdn) {
    calculate_total_cost(frm, cdt, cdn);
  },
  cost: function (frm, cdt, cdn) {
    calculate_total_cost(frm, cdt, cdn);
  },
});

frappe.ui.form.on("Purchase Order Payment Child", {
  payment_type: function (frm, cdt, cdn) {
    calculate_payment_amount(frm, cdt, cdn);
  },
  input_amount: function (frm, cdt, cdn) {
    calculate_payment_amount(frm, cdt, cdn);
  },
});

function calculate_total_cost(frm, cdt, cdn) {
  let row = locals[cdt][cdn]; // get current child row
  let total = (row.quantity || 0) * (row.cost || 0);

  frappe.model.set_value(cdt, cdn, "sub_total", total);
  frappe.model.set_value(cdt, cdn, "total_cost", total);

  update_summary(frm);
}

function update_summary(frm) {
  let total_cost = 0;
  let total_quantrity = 0;

  (frm.doc.purchase_products || []).forEach((row) => {
    total_cost += row.total_cost || 0;
    total_quantrity += row.quantity || 0;
  });

  frm.set_value("total_quantity", total_quantrity);
  frm.set_value("total_cost", total_cost);

  frm.set_value("balance", total_cost - (frm.doc.total_payment || 0));
}

function calculate_payment_amount(frm, cdt, cdn) {
  let row = locals[cdt][cdn]; // get current child row
  let payment_amount = (row.input_amount || 0) / (row.exchange_rate || 1);

  frappe.model.set_value(cdt, cdn, "payment_amount", payment_amount);

  // update total payment
  let total_payment = 0;
  (frm.doc.payments || []).forEach((row) => {
    total_payment += row.payment_amount || 0;
  });

  frm.set_value("total_payment", total_payment);
}
