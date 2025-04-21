// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer", {
    onload: function(frm) {
        if (frm.is_new()) {
            frm.add_child('product_prices', {});
            frm.refresh_field('product_prices');
        }
    },
});
