// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt
 
frappe.ui.form.on("Customer", {
    onload: function(frm) {
        if (frm.is_new()) {
            frm.add_child('product_prices', {});
            frm.refresh_field('product_prices');
        } 

        frm.set_query("product_code", "product_prices", function (doc, cdt, cdn) {
            return {
                "filters": {
                    "enabled": 1,
                    "name":["not in",doc.product_prices.map(x=>x.product_code)]
                },
            };
        });

        
    },
    refresh(frm){
       addCustomButton(frm)
    }
});


function addCustomButton(frm){
    frm.add_custom_button(__('Sale Invoices List'), function() {
            frappe.msgprint('view sale invoice list');

    }, __('View')); 
    
    frm.add_custom_button(__('Sale Payment List'), function() {
            frappe.msgprint('view sale invoice list');

    }, __('View')); 


    frm.add_custom_button('My Custom Action', function() {
            frappe.msgprint('Button clicked!');
        }, 'Actions'); 
}