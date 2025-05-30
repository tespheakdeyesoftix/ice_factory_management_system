// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Closed Selling Date", {
	refresh(frm) {
        
	},
    outlet(frm) {
        frm.get_field('closed_selling_date_items').grid.cannot_add_rows = true;
        frm.fields_dict['closed_selling_date_items'].grid.wrapper.find('.grid-remove-rows').hide();
        frappe.call({
            method: 'ice_factory_management_system.selling_ifms.doctype.closed_selling_date.closed_selling_date.get_closed_date_data',
            args: {
                outlet: frm.doc.outlet
            },
            callback: (r) => {
                frm.clear_table("closed_selling_date_items");
                r.message.forEach(a => {
                    let child = frm.add_child('closed_selling_date_items');
                    child.total_name = a.total_name;
                    child.total_amount = a.total_amount;
                    frm.refresh_field('closed_selling_date_items');
                })
            }
        })
    }
});
