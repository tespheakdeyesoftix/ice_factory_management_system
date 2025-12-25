// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor", {
	onload(frm) {
       
            frm.set_query("stock_location", "product_price", function (doc, cdt, cdn) {
               
            return {
                "filters": {
                    "vendor": doc.name,
                    "enabled":1
                }
            };
        });
       
        
	},
});
