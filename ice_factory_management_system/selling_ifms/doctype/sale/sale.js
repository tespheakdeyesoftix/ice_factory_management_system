// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale", {
	refresh(frm) {

	},
    customer(frm) {
        frappe.call({
            method: 'ice_factory_management_system.customer_relation.doctype.customer.customer.get_customer_product_price',
            args: {
               customer: frm.doc.customer,
               products: frm.doc.sale_products
            },
            callback: (r) => {
                frm.doc.sale_products = []
                frm.refresh_field("sale_products");
                frm.doc.sale_products = r.message;
                frm.refresh_field("sale_products");
                update_sale_total(frm)
            }
        })
    }
});

frappe.ui.form.on("Sale Products", {
    sale_products_remove(frm){
        update_sale_total(frm)
    },
    quantity(frm,cdt,cdn) {
        cal_total_product(frm,cdt,cdn);
    },
    price(frm,cdt,cdn) {
        cal_total_product(frm,cdt,cdn);
    },
    free_quantity(frm,cdt,cdn) {
        cal_total_product(frm,cdt,cdn);
    },
    product_code(frm,cdt,cdn) {
        row = locals[cdt][cdn];
        frappe.call({
            method: 'ice_factory_management_system.customer_relation.doctype.customer.customer.get_customer_product_price',
            args: {
                customer: frm.doc.customer,
                product_code: row.product_code
            },
            callback: (r) => {
                frappe.model.set_value(cdt, cdn, "price", r.message);
                update_sale_total(frm)
            }
        })
    }
});

function cal_total_product(frm,cdt,cdn,skip_update_total=0) {
    let row = locals[cdt][cdn];
    sale_quantity = row.quantity - row.free_quantity;
    let total_amount = sale_quantity * row.price;
    frappe.model.set_value(cdt, cdn, "total_sale_quantity", sale_quantity);
    frappe.model.set_value(cdt, cdn, "total_amount", total_amount);
    if (skip_update_total == 0) {
        update_sale_total(frm);
    }
}

function update_sale_total(frm) {
    let total_quantity = 0;
    let total_free_quantity = 0;
    let total_total_sale_quantity = 0;
    let total_sale_amount = 0;
    frm.doc.sale_products.forEach(a => {
        if(a.allow_sum_qty == 1){
            total_quantity += a.quantity;
            total_free_quantity += a.free_quantity;
            total_total_sale_quantity += a.total_sale_quantity;
            total_sale_amount += a.total_amount;
        }
    });
    frm.set_value("total_quantity", total_quantity);
    frm.set_value("total_free", total_free_quantity);
    frm.set_value("total_sale_quantity", total_total_sale_quantity);
    frm.set_value("total_amount", total_sale_amount);
    frm.set_value("balance", total_sale_amount);
}