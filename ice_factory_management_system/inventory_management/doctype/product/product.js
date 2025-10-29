// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
    refresh: function (frm) {

        updateIndicator(frm)
        addCustomerButtons(frm)

    },
    onload: function (frm) {
        if (frm.is_new()) {
            frm.add_child('product_outlet', {});
            frm.refresh_field('product_outlet');
        }
    },
});
function updateIndicator(frm) {
    frm.dashboard.clear_headline();
    frm.call("get_stats")
        .then(r => {
            if (r.message) {
                r.message.forEach(x => {
                    frm.dashboard.add_indicator(
                        __("{0}: {1}", [x.label, x.value]),
                        "blue"
                    );
                });
            }
        })
}
function addCustomerButtons(frm) {

    if (frm.doc.is_inventory_product==1){
         frm.add_custom_button(__("Stock Adjustment"), function () {
        onStockAdjustment(frm)
    }, __("Actions"));
    }
   
}

function onStockAdjustment(frm) {
    
    frm.call("get_stock_location_product_for_adjustment").then(result => {
        console.log(result.message)
       
        let dialog = new frappe.ui.Dialog({
            title: __("Product Quantity"),
              size: "extra-large",
            fields: [
                {
                    fieldname: 'products',
                    label: 'Products',
                    fieldtype: 'Table',
                    cannot_add_rows: true,  
                    in_place_edit: true,  
                   
                    data:result.message,
                    fields: [
                        { fieldname: 'stock_location', label: __('Stock Location') ,in_list_view: 1, fieldtype: 'Data', read_only:1 },
                        { fieldname: 'current_quantity', label: __('Old Quantity') ,in_list_view: 1, fieldtype: 'Float', read_only:1 },
                        { fieldname: 'current_cost', label: __('Old Cost') ,in_list_view: 1, fieldtype: 'Currency', read_only:1 },
                        
                        { fieldname: 'new_quantity', label: __('New Quantity'),in_list_view: 1, fieldtype: 'Float',non_negative:1 },
                        { fieldname: 'new_cost', label: __('New Cost'),in_list_view: 1, fieldtype: 'Currency', non_negative:1 },
                        { fieldname: 'note', label: __('Note'),in_list_view: 1, fieldtype: 'Data',  },

                        
                    ]
                }
            ],
            primary_action_label: 'Submit',
            primary_action(values) {
                frm.doc.stock_adjustment_data = values.products;
                frappe.dom.freeze(__("Updating stock adjustment..."));
                frm.call("update_stock_adjustment").then(result=>{

                    frappe.dom.unfreeze();
                    
                      dialog.hide();
                })
                .catch(err=>{
                  frappe.dom.unfreeze();
                })
             
            }
        });

        dialog.show();

    })

}
