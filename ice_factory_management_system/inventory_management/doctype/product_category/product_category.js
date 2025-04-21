// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product Category", {
	refresh(frm) {
        frm.set_query("parent_product_category", function() {
            return {
                filters: [
                    ["is_group", "=", 1],
                    ["enabled", "=", 1]
                ]
            }
        });
	},
});
