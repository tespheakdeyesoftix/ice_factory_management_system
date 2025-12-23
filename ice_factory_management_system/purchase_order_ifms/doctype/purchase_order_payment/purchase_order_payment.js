// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Order Payment", {

     onload(frm) {         
        frm.set_query("purchase_order", "purchase_orders", function (doc, cdt, cdn) {
            
            let purchase_order_filter = {
                    "party": doc.party || 'Not Set',
                    "outlet": doc.outlet || 'Not Set',
                    "balance": [">", 0],
                    "docstatus": 1
                };          
            if (doc.purchase_order){
                purchase_order_filter.name = doc.purchase_order
            }
            return {
                "filters": purchase_order_filter,
            };
        });

        // we run this to for read purchase order payment, write off and balance again
        updatePOPaymentAmount(frm);
    },
    posting_date(frm){
        update_allocated_payment_date(frm)
    },
	refresh(frm) {
        setOutlet(frm);
        if(!frm.is_new() && frm.doc.docstatus==0){
            if(frm.doc.exchange_rate){                
                frm.set_value("exchange_rate_virtual",1/ parseFloat(frm.doc.exchange_rate))
            }
        }
	},

    party_type(frm){
        frm.set_value("party", "");
        frm.refresh_field("party")
    },

    async party(frm) { 
        await getPartyName(frm);
        await getPartyBalance(frm);
        await get_unpaid_purchase_orders(frm)
        if ((frm.doc.input_amount || 0) > 0) {
            update_allocated_amount(frm)
        } else {
            calculate_totals(frm)
        }  
    },
    async outlet(frm) {
        await get_default_account_paid_from(frm);
        await get_default_account_payable(frm);
        await get_default_account_writeoff(frm);
        await getPartyName(frm);
        await getPartyBalance(frm);
        await get_unpaid_purchase_orders(frm)
        if ((frm.doc.input_amount || 0) > 0) {
            update_allocated_amount(frm)
        } else {
            calculate_totals(frm)
        }  
    },
    async payment_type(frm) {
        await get_default_account_paid_from(frm);

        if(frm.doc.exchange_rate){
            frm.set_value("exchange_rate_virtual",1/ parseFloat(frm.doc.exchange_rate))
        }  

        if ((frm.doc.input_amount || 0) > 0) {
            const payment_amount = frm.doc.input_amount / (parseFloat(frm.doc.exchange_rate) || 1)
            frm.set_value("payment_amount", payment_amount);
            frm.set_value("total_payment_amount_virtual", payment_amount);
            update_allocated_amount(frm)
        }
       
    },

     // this is button get purchase-order invoices by date
    async get_invoices(frm) {
        if (!frm.doc.outlet) {
            frappe.throw(__("Please select outlet"))
            return
        }
        if (!frm.doc.party) {
            frappe.throw(__("Please select Party"))
            return
        }

        if (!frm.doc.start_date) {
            frappe.throw(__("Please select start date"))
            return
        }
        if (!frm.doc.end_date) {
            frappe.throw(__("Please select end date"))
            return
        }
        await get_unpaid_purchase_orders(frm)
        calculate_totals(frm)
    },

    input_amount: function (frm) {
        if (!frm.doc.payment_type) {
            frappe.throw(__("Please select payment type"))
        }
        const payment_amount = frm.doc.input_amount / (parseFloat(frm.doc.exchange_rate) || 1)

        frm.set_value("payment_amount", payment_amount);
        frm.set_value("total_payment_amount_virtual", payment_amount);  
        if (frm._from_set_value) return;      
        update_allocated_amount(frm);
   
    },

});

///child table in purchase order payment
frappe.ui.form.on("Purchase Order Payment Invoices", {
    refresh(frm) {

    },

    pay: function (frm, cdt, cdn) {
        // when user click on button pay get sale balance update  to payment amount
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
      
        let row = locals[cdt][cdn];   
        frappe.model.set_value(cdt, cdn, "payment_amount", row.purchase_order_balance || 0);
        calculate_row_purchase_order(frm, cdt, cdn);
        calculate_totals(frm);
    },

    purchase_order: function (frm, cdt, cdn) {
        calculate_row_purchase_order(frm, cdt, cdn);
        calculate_totals(frm);
    },

    purchase_orders_add: function (frm) {
        calculate_totals(frm)
    },

    purchase_orders_remove: function (frm) {
        calculate_totals(frm)
    },


    payment_amount: function (frm, cdt, cdn) {
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
        calculate_row_purchase_order(frm, cdt, cdn);



        //input amount
        const payment_amount = frm.doc.purchase_orders.reduce((sum, s) => sum + (s.payment_amount || 0), 0);
        frm._from_set_value = true;
        frm.set_value(
            "input_amount",
            payment_amount / parseFloat(frm.doc.exchange_rate_virtual || 1)
        ).then(() => {
            frm._from_set_value = false;
            calculate_totals(frm);
        });
    },
    write_off_amount: function (frm, cdt, cdn) {
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
        calculate_row_purchase_order(frm, cdt, cdn);
        calculate_totals(frm);
    },

});

/* custom method */
///method calc row of child
function calculate_row_purchase_order(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    const payment_amount = row.payment_amount || 0;
    const write_off_amount = row.write_off_amount || 0;
    frappe.model.set_value(cdt, cdn, "balance", (row.purchase_order_balance || 0) - (payment_amount + write_off_amount));
}

///method calc total summary
function calculate_totals(frm) {
    const total_amount_to_pay = frm.doc.purchase_orders.reduce((sum, s) => sum + (s.purchase_order_balance || 0), 0);
    const payment_amount = frm.doc.purchase_orders.reduce((sum, s) => sum + (s.payment_amount || 0), 0);
    const write_off_amount = frm.doc.purchase_orders.reduce((sum, s) => sum + (s.write_off_amount || 0), 0);
    const total_invoices = frm.doc.purchase_orders.filter(r => r.purchase_order).length;
    const balance = total_amount_to_pay - (payment_amount + write_off_amount)
 
    frm.set_value("payment_amount", payment_amount);
    frm.set_value("total_invoices", total_invoices);
    frm.set_value("amount_to_pay", total_amount_to_pay);
    frm.set_value("total_amount_to_pay_virtual", total_amount_to_pay);
    frm.set_value("balance", balance);
    frm.set_value("balance_virtual", balance);
}


///method get unpaid of purchase order list
function get_unpaid_purchase_orders(frm) {
    if (!frm.doc.party) {
        frm.clear_table("purchase_orders");
        frm.refresh_field("purchase_orders");
        return;
    };
    if (!frm.doc.outlet) return;
    return new Promise((resolve, reject) => {
    frm.call({
        method: "get_unpaid_purchase_orders",
        doc: frm.doc,  
        freeze: true,
        }).then(r => {
            frm.clear_table("purchase_orders");

            (r.message || []).forEach(row => {
                let d = frm.add_child("purchase_orders");
                d.purchase_order = row.name;
                d.outlet = row.outlet;
                d.party_type = row.party_type;
                d.party = row.party;
                d.payment_date = frm.doc.posting_date;
                d.posting_date = row.posting_date;
                d.total_amount = row.total_cost;
                d.paid_amount = row.total_payment;
                d.purchase_order_balance = row.balance;
                d.balance = row.balance;
            });

            frm.refresh_field("purchase_orders");
            resolve(r.message || []);
        })
        .catch(err => {
            frm.clear_table("purchase_orders");
            frm.refresh_field("purchase_orders");
            reject(err);
        });
    });


}


///method update allocated of amount
function update_allocated_amount(frm) {
 
        let paid_amount = frm.doc.payment_amount;
        if ((frm.doc.purchase_orders || []).length > 0) {
            frm.doc.purchase_orders.forEach(r => {
                if (paid_amount < r.purchase_order_balance) {
                    r.payment_amount = paid_amount;
                }
                else {
                    r.payment_amount = r.purchase_order_balance
                }
                r.balance = r.purchase_order_balance - r.payment_amount
                paid_amount = paid_amount - r.payment_amount
            });
            frm.refresh_field("purchase_orders")
            calculate_totals(frm);
        }
  
}
///method update allocated of payment date
function update_allocated_payment_date(frm) {
    if ((frm.doc.purchase_orders || []).length > 0) {
        frm.doc.purchase_orders.forEach(r => {
            r.payment_date = frm.doc.posting_date;
        });
        frm.refresh_field("purchase_orders");
    }

}

/// method get balance of party base-on party-type
function getPartyBalance(frm) {

    let is_stop = false;
    if (!frm.doc.party) is_stop = true;
    if (!frm.doc.outlet) is_stop = true;
    if(is_stop) {
        frm.set_value("party_balance",  0);
        frm.refresh_field("party_balance")
        return;
    }
    return new Promise((resolve, reject) => {
        frm.call({
            method:"get_party_credit_balance",
            doc: frm.doc,  
            freeze: true,
        }).then(r => {
            frm.set_value("party_balance", r.message || 0);
            resolve(r.message || 0);
        })
        .catch(err => {
            frm.set_value("party_balance", 0);
            reject(err);
        });
    });

}

///method get party-name base-on party-type
function getPartyName(frm) {
   
    if (!frm.doc.party) {
        frm.set_value("party_name", "");
         frm.refresh_field("party_name")
        return;
    };

    return new Promise((resolve, reject) => {
        frm.call({
            method:"get_party_name",
            doc: frm.doc,  
            freeze: true,
        }).then(r => {
            frm.set_value("party_name", r.message || "");
            resolve(r.message || "");
        }).catch(err => {
            frm.set_value("party_name", "");
            reject(err);
        });
    });

}



///method get default acount of Account Paid From
async function get_default_account_paid_from(frm){
    if(!frm.doc.payment_type || !frm.doc.outlet){
        frm.set_value("account_paid_from", "");
        return;
    }
     let resp =  await frm.call({
        method:"get_payment_default_account",
        doc: frm.doc,  
        freeze: true,
    })
    if(resp.message){
        frm.set_value("account_paid_from", resp.message);
    } 
}

///method get default acount of Account Payable
async function get_default_account_payable(frm){
    if(!frm.doc.outlet){
        frm.set_value("account_payable", "");
        return;
    }
     let resp =  await frm.call({
        method:"get_default_account_payable",
        doc: frm.doc,  
        freeze: true,
    })
    if(resp.message){
        frm.set_value("account_payable", resp.message);
    } 
}

///method get default acount of Account Payable
async function get_default_account_writeoff(frm){
    if(!frm.doc.outlet){
        frm.set_value("write_off_account", "");
        return;
    }
     let resp =  await frm.call({
        method:"get_default_account_writeoff",
        doc: frm.doc,  
        freeze: true,
    })
    if(resp.message){
        frm.set_value("write_off_account", resp.message);
    } 
}


///method set query outlet (default outlet)
function setOutlet(frm) {
    if (frm.is_new()) {
        frm.call({
            method:"get_default_outlet",
            doc: frm.doc,  
            freeze: true
        }).then(r => {
            frm.set_value("outlet", r.message);
        });
    }
}

/// method update purchase order payment amount
function updatePOPaymentAmount(frm) {
    if (!frm.is_new() && frm.doc.docstatus == 0) {
        if (frm.doc.sales) {
            frappe.db.get_list("Purchase Order", {
                fields: ["name", "total_amount", "total_payment", "total_write_off"],
                filters: { name: ["in", frm.doc.purchase_orders.map(x => x.purchase_order)] },
                limit: frm.doc.purchase_orders.length
            }).then(data => {
                frm.doc.purchase_orders.forEach(r => {
                    const s = data.find(x => x.name == r.purchase_order);
                    if (s) {
                        r.total_amount = s.total_amount || 0;
                        r.paid_amount = s.total_payment || 0;
                        r.purchase_order_balance = r.total_amount - (r.paid_amount - (s.total_write_off || 0))
                        r.balance = r.purchase_order_balance - ((r.payment_amount || 0) + (r.write_off_amount || 0))
                    }

                });

                // check if have input amount then recalculat allocate amount
                if (frm.doc.input_amount > 0) {
                    update_allocated_amount(frm)
                } else {
                    frm.refresh_field("purchase_orders")
                    calculate_totals(frm);
                }
 
            })
        }
    }
}

