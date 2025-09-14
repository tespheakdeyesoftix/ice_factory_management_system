frappe.ui.form.on("*", {
    refresh(frm) {
        
        frm.print_doc = function () {
            printDoc(frm)
        };
        setTimeout(function(){
            hideMenus()
        },700)
    }
});


function printDoc(frm,report_name="") {
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
                <iframe src="/embed/doctype-server-report?doctype=${frm.doctype}&docname=${frm.docname}&report_name=${report_name}" 
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



function hideMenus(menus=["Email","Show Link","Copy to Clipboard","Customize","Edit DocType","Jump to field","Rename"]){
    if(frappe.session.user=="Administrator") return
      setTimeout(() => {
            // Find and hide the Email dropdown item
            menus.forEach(m=>{
  $(`.dropdown-item .menu-item-label:contains(${__(m)})`)
                .closest('li')
                .remove();
            })
          
             

        }, 500);
}