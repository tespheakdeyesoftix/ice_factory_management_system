frappe.ui.form.on("*", {
    refresh(frm) {
        frm.page.remove_inner_button(__('Print'));
        frm.print_doc = function () {
            printDoc(frm)
        };
    }
});


function printDoc(frm) {
    let d = new frappe.ui.Dialog({
        title: __('Print Report') + " " + frm.doc.name,
        size: 'large', // 'small', 'large', 'extra-large'
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'iframe_html',
                label: 'Iframe'
            }
        ]
    });
    
    d.fields_dict.iframe_html.$wrapper.html(`
                <iframe src="/embed/doctype-server-report?doctype=${frm.doctype}&docname=${frm.docname}" 
                        width="100%" 
                        height="${window.innerHeight - 150}px" 
                        frameborder="0"
                        style="border-radius: 8px;">
                </iframe>
            `);

    d.show();
    d.$wrapper.find('.modal-dialog').css({
        "width": "90%",
        "max-width": "90%",

    });
}