 
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
        const btn = listview.page.add_inner_button(__('Return Product'), async () => {
          const result = await  frappe.borrow_product.onBulkReturnProduct();
          if(result){
            listview.refresh();
          }

        });

        // make it primary
        $(btn).removeClass('btn-default').addClass('btn-warning');
    }
}
