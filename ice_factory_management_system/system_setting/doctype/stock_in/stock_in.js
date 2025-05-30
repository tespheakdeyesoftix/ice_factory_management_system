// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock In", {
	qty(frm) {
        update_totals(frm)
	},
    price(frm){
        update_totals(frm)   
    },
    stock_in_type(frm){
        set_value(frm)
    }
});

frappe.ui.form.on("Stock In Products",{
    qty(frm,cdt,cdn){
        update_row_total(frm,cdt,cdn)
    },
    price(frm,cdt,cdn){
        update_row_total(frm,cdt,cdn)
    }
});

function update_row_total(frm,cdt,cdn){
    row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "total_amount", row.price * row.qty);
    update_sale_total(frm)
}

function update_sale_total(frm) {
    let total_quantity = 0;
    let total_amount = 0;
    frm.doc.stock_in_products.forEach(a => {
        total_quantity += a.qty;
        total_amount += a.total_amount;
    });
    frm.set_value("total_qty", total_quantity);
    frm.set_value("total_product_amount", total_amount);
}

function update_totals(frm){
    frm.set_value("total_amount",frm.doc.qty * frm.doc.price)
}

function set_value(frm){
    if(frm.doc.stock_in_type == "Multiple Product"){
        frm.set_value("product_code","")
        frm.set_value("qty",1)
        frm.set_value("price",0)
        frm.set_value("total_amount",0)
    }
   else{
    frm.clear_table("stock_in_products")
    frm.refresh_field('stock_in_products');
    frm.set_value("total_product_amount",0)
    frm.set_value("total_qty",0)
   }
}