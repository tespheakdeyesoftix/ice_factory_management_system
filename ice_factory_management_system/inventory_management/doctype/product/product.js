// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
    refresh: function(frm) {
        
        frm.dashboard.clear_headline();
        frm.call("get_stats")
        .then(r => {
        if (r.message) {
            r.message.forEach(x=> {
                  frm.dashboard.add_indicator(
                    __("{0}: {1}", [x.label , x.value]),
                    "blue"
                );
            });
        }
        })
 
    },
    onload: function(frm) {
        if (frm.is_new()) {
            frm.add_child('product_outlet', {});
            frm.refresh_field('product_outlet');
        }
    },
});
