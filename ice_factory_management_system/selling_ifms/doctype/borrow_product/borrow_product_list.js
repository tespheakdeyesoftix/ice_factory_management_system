frappe.listview_settings['Borrow Product'] = {
    add_fields: ['transaction_type','return_quantity','balance'],
    has_indicator_for_draft: true,
    get_indicator(doc) {
        if(doc.docstatus==0) return [__("Draft"), "red"];
        if(doc.docstatus==1 && doc.transaction_type==="Return") return [__("Return"), "blue"];
        if(doc.docstatus==1 && doc.transaction_type==="Borrow" && doc.quantity == (doc.balance ||0)) return [__("Borrow"), "red"];
        if(doc.docstatus==1 && doc.transaction_type==="Borrow" && (doc.return_quantity ||0)>0 && (doc.balance || 0)>0) return [__("Partially Return"), "orange"];
        if(doc.docstatus==1 && doc.transaction_type==="Borrow" &&  (doc.balance || 0)==0) return [__("Returned"), "green"];

        return [__(doc.transaction_type), doc.transaction_type==="Borrow"?"blue":"green"];
    },
    formatters: {
        transaction_type(value) {
            if (!value) return '';

            let color = 'gray';

            if (value === 'Borrow') {
                color = 'orange';
            } else if (value === 'Return') {
                color = 'green';
            }

            return `
                <span class="indicator-pill ${color}">
                    ${__(value)}
                </span>
            `;
        }
    },
    onload(listview) {
        const btn = listview.page.add_inner_button(__('Return Product'), () => {
           returnProduct(listview);

        });

        // make it primary
        $(btn).removeClass('btn-default').addClass('btn-warning');
    }
}

let last_customer = null;
function returnProduct(listview){
    const d = new frappe.ui.Dialog({
        title: __('Add Return Product'),
        size:"extra-large",
        fields: [
            {
                fieldname: 'customer',
                label: __('Customer'),
                fieldtype: 'Link',
                options:"Customer",
                onchange() {  
                   const customer = d.get_value('customer');

                    // ✅ prevent double call
                    if (!customer || customer === last_customer) return;

                    last_customer = customer;
                    alert(customer)

                }
            },
            {fieldtype:"Column Break"},
            {
                fieldname: 'posting_date',
                label: __('Return Date'),
                fieldtype: 'Date',
                reqd: 1
            },
            
            {
                fieldtype:"Section Break"
            },
            returnProductTableField("customer")

            
        ],
        primary_action_label: __('Approve'),
        primary_action(values) {
            d.disable_primary_action();
            // frappe.call({
            //     method: 'your_app.api.bulk_approve',
            //     args: {
            //         names: selected.map(d => d.name),
            //         remark: values.remark
            //     },
            //     freeze: true,
            //     freeze_message: __('Approving...')
            // }).then(() => {
            //     d.hide();
            //     frappe.show_alert({
            //         message: __('Approved successfully'),
            //         indicator: 'green'
            //     });

            //     // ✅ refresh list view
            //     listview.refresh();
            // }).finally(() => {
            //     d.enable_primary_action();
            // });
        }
    })

     d.show();
}

function returnProductTableField(customer){
    return {
    fieldname: 'return_products',
    fieldtype: 'Table',
    label: __('Return Product'),
     cannot_add_rows: true,  
                    in_place_edit: true,  
    data: [
        {
            product: 'T00009',
            borrow_quantity: 10,
            returned_quantity: 0,
            remaining_quantity: 10,
            return_quantity: 0,
            balance_quantity: 10,
            note: ''
        }
    ],
    fields: [
        {
            fieldtype: 'Link',
            fieldname: 'product',
            label: __('Product'),
            options: 'Product',
            in_list_view: 1,
            read_only: 1   // 🔒 lock
        },
        {
            fieldtype: 'Float',
            fieldname: 'borrow_quantity',
            label: __('Borrow QTY'),
            in_list_view: 1,
            read_only: 1
        },
        {
            fieldtype: 'Float',
            fieldname: 'returned_quantity',
            label: __('Returned QTY'),
            in_list_view: 1,
            read_only: 1
        },
        {
            fieldtype: 'Float',
            fieldname: 'remaining_quantity',
            label: __('Remaining QTY'),
            in_list_view: 1,
            read_only: 1
        },
        {
            fieldtype: 'Float',
            fieldname: 'return_quantity',
            label: __('Return QTY'),
            in_list_view: 1
            // ✅ editable
        },
        {
            fieldtype: 'Float',
            fieldname: 'balance_quantity',
            label: __('Balance QTY'),
            in_list_view: 1,
            read_only: 1
        },
        {
            fieldtype: 'Data',
            fieldname: 'note',
            label: __('Note'),
            in_list_view: 1,
            read_only: 1
        }
    ]
}

       
}


function load_return_products(d, customer) {
    frappe.call({
        method: 'your_app.api.get_return_products',
        args: { customer },
        freeze: true,
        freeze_message: __('Loading products...')
    }).then(r => {
        if (!r.message) return;

        const table = d.fields_dict.return_products;

        // replace table data
        table.df.data = r.message;

        table.grid.refresh();
    });
}