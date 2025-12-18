// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale Payment", {
    onload(frm) {
        frm.set_query("sale", "sales", function (doc, cdt, cdn) {
            
            let sale_filter = {
                    "customer": doc.customer || 'Not Set',
                    "outlet": doc.outlet || 'Not Set',
                    "balance": [">", 0],
                    "sale_status": "Closed"
                };
          
            if (doc.sale){
                sale_filter.name = doc.sale
            }
            return {
                "filters": sale_filter,
            };
        });
 
            // we run this to for read sale payment, write off and balance again
        updateSalePaymentAmount(frm);
        
    },
    refresh(frm) {
        setOutlet(frm);
        if(!frm.is_new() && frm.doc.docstatus==0){
            if(frm.doc.exchange_rate){
            
            frm.set_value("exchange_rate_virtual",1/ parseFloat(frm.doc.exchange_rate))
        }
        }
    },

    async customer(frm) {
 
await getCustomerBalance(frm)
        await get_unpaid_sales(frm)
        if ((frm.doc.input_amount || 0) > 0) {
            update_allocated_amount(frm)
        } else {
            calculate_totals(frm)
        }
         
        

    },
    async outlet(frm) {
        await getCustomerBalance(frm)
        await get_unpaid_sales(frm)
        if ((frm.doc.input_amount || 0) > 0) {
            update_allocated_amount(frm)
        } else {
            calculate_totals(frm)
        }

    },
    async payment_type(frm) {
        if ((frm.doc.input_amount || 0) > 0) {
            update_allocated_amount(frm)
        }
        if(frm.doc.exchange_rate){
            frm.set_value("exchange_rate_virtual",1/ parseFloat(frm.doc.exchange_rate))
        }
        

    },
    // this is button get Sale Invoice by Date
    async get_sales_invoice(frm) {
        if (!frm.doc.outlet) {
            frappe.throw(__("Please select outlet"))
            return
        }

        if (!frm.doc.customer) {
            frappe.throw(__("Please select customer"))
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
        await get_unpaid_sales(frm)
        calculate_totals(frm)
    },
    input_amount(frm) {
        if (!frm.doc.payment_type) {
            frappe.throw(__("Please select payment type"))
        }
        const payment_amount = frm.doc.input_amount / (frm.doc.exchange_rate || 1)
        frm.set_value("payment_amount", payment_amount);
        frm.set_value("total_payment_amount_virtual", payment_amount);

        update_allocated_amount(frm);
    },
    
});


frappe.ui.form.on("Sale Payment Invoices", {
    refresh(frm) {

    },
    sale: function (frm, cdt, cdn) {
        calculate_row_sale(frm, cdt, cdn);
        calculate_totals(frm);
    },
    sales_add: function (frm) {
        calculate_totals(frm)
    },
    sales_remove: function (frm) {
        calculate_totals(frm)

    },

    pay: function (frm, cdt, cdn) {
        // when user click on button pay get sale balance update  to payment amount
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
      
        let row = locals[cdt][cdn];
   
        frappe.model.set_value(cdt, cdn, "payment_amount", row.sale_balance || 0);
        calculate_row_sale(frm, cdt, cdn);
        calculate_totals(frm);

    },
    payment_amount: function (frm, cdt, cdn) {
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
        calculate_row_sale(frm, cdt, cdn);
        calculate_totals(frm);

    },
    write_off_amount: function (frm, cdt, cdn) {
        // if we change value in sale payment invoice child table input amount will be clear 
        // and total_payment_amount is sum from child table
        calculate_row_sale(frm, cdt, cdn);
        calculate_totals(frm);
    },
})



function getCustomerBalance(frm) {
    if (!frm.doc.customer) return;
    if (!frm.doc.outlet) return;
    return new Promise((resolve, reject) => {
        frm.call("get_customer_credit_balance")
            .then(r => {
                frm.set_value("customer_balance", r.message || 0);

                resolve(r.message || 0);
            })
            .catch(err => {
                frm.set_value("customer_balance", 0);
                reject(err);
            });
    });

}

function get_unpaid_sales(frm) {
    if (!frm.doc.customer) {
        frm.clear_table("sales");
        frm.refresh_field("sales");
        return;
    };
    if (!frm.doc.outlet) return;


    return new Promise((resolve, reject) => {
        frm.call("get_unpaid_sales")
            .then(r => {

                frm.clear_table("sales");
                // Loop and add rows
                r.message.forEach(row => {
                    let child_row = frm.add_child("sales");
                    child_row.sale = row.name;
                    child_row.posting_date = row.posting_date;
                    child_row.total_amount = row.total_amount;
                    child_row.paid_amount = row.total_payment;
                    child_row.sale_balance = row.balance;
                    child_row.balance = row.balance;

                });


                frm.refresh_field("sales");
                resolve(r.message || 0);
            })
            .catch(err => {
                frm.set_value("sales", 0);
                reject(err);
            });
    });

}

function update_allocated_amount(frm) {
    let paid_amount = frm.doc.payment_amount;

    if ((frm.doc.sales || []).length > 0) {
        frm.doc.sales.forEach(r => {
            if (paid_amount < r.sale_balance) {
                r.payment_amount = paid_amount;
            }
            else {
                r.payment_amount = r.sale_balance
            }
            r.balance = r.sale_balance - r.payment_amount
            paid_amount = paid_amount - r.payment_amount
        });
        frm.refresh_field("sales")
        calculate_totals(frm);
    }

}


function calculate_row_sale(frm, cdt, cdn) {

    let row = locals[cdt][cdn];
    const payment_amount = row.payment_amount || 0;
    const write_off_amount = row.write_off_amount || 0;
    frappe.model.set_value(cdt, cdn, "balance", (row.sale_balance || 0) - (payment_amount + write_off_amount));

}


function calculate_totals(frm) {
    const total_amount_to_pay = frm.doc.sales.reduce((sum, s) => sum + (s.sale_balance || 0), 0);
    const payment_amount = frm.doc.sales.reduce((sum, s) => sum + (s.payment_amount || 0), 0);
    const write_off_amount = frm.doc.sales.reduce((sum, s) => sum + (s.write_off_amount || 0), 0);
    const total_sales_invoice = frm.doc.sales.filter(r => r.sale).length;
    const balance = total_amount_to_pay - (payment_amount + write_off_amount)
    frm.set_value("payment_amount", payment_amount);
    frm.set_value("total_sales_invoice", total_sales_invoice);
    frm.set_value("amount_to_pay", total_amount_to_pay);
    frm.set_value("total_amount_to_pay_virtual", total_amount_to_pay);
    frm.set_value("balance", balance);
    frm.set_value("balance_virtual", balance);


}
function set_amount_to_zero(frm) {
    frm.set_value("input_amount", 0);
    frm.set_value("total_amount", 0);
    frm.set_value("payment_balance", frm.doc.currency_symbol + " " + ((frm.doc.balance - frm.doc.total_amount) * (frm.doc.exchange_rate || 1)).toLocaleString());
}

function update_total_amount(frm) {
    if (frm.doc.input_amount == 0 && frm.doc.write_off_amount == 0) {
        frm.set_value("total_amount", 0);
    }
    else {
        let total_amount = ((frm.doc.input_amount || 0) + (frm.doc.write_off_amount || 0)) / (frm.doc.exchange_rate || 1);
        frm.set_value("total_amount", total_amount);
    }
    frm.set_value("payment_balance", frm.doc.currency_symbol + " " + ((frm.doc.balance - frm.doc.total_amount) * (frm.doc.exchange_rate || 1)).toLocaleString());
}

function setOutlet(frm) {

    if (frm.is_new()) {

        frm.call("get_default_outlet").then(r => {
            frm.set_value("outlet", r.message);

        })
    }

}

function updateSalePaymentAmount(frm) {

    if (!frm.is_new() && frm.doc.docstatus == 0) {
        if (frm.doc.sales) {
            frappe.db.get_list("Sale", {
                fields: ["name", "total_amount", "total_payment", "total_write_off"],
                filters: { name: ["in", frm.doc.sales.map(x => x.sale)] },
                limit: frm.doc.sales.length
            }).then(data => {
                frm.doc.sales.forEach(r => {
                    const s = data.find(x => x.name == r.sale);
                    if (s) {
                        r.total_amount = s.total_amount || 0;
                        r.paid_amount = s.total_payment || 0;
                        r.sale_balance = r.total_amount - (r.paid_amount - (s.total_write_off || 0))
                        r.balance = r.sale_balance - ((r.payment_amount || 0) + (r.write_off_amount || 0))
                    }

                });

                // check if have input amount then recalculat allocate amount
                if (frm.doc.input_amount > 0) {
                    update_allocated_amount(frm)
                } else {
                    frm.refresh_field("sales")
                    calculate_totals(frm);
                }
 
            })
        }
    }
}