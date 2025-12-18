frappe.ui.form.on("*", {
    refresh(frm) {
        
        frm.print_doc = function () {
            printDoc(frm)
        };
        cleanFormSidebar();
        hideMenus();
       

        render_html_template(frm);
        render_custom_sidebar(frm);
        
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

function render_html_template(frm){
    let html_fields = frm.fields.filter(f => f.df.fieldtype === 'HTML').map(x=>x.df.fieldname);
    frappe.call("ice_factory_management_system.ice_factory_management_system.doctype.html_template.html_template.get_html_template",{
        fields:html_fields,
        doc:frm.doc
    }).then(r=>{
        html_fields.forEach(f => {
            if (r.message.hasOwnProperty(f)){
                frm.fields_dict[f].$wrapper.html(r.message[f]);
            }
        });
        
    })
}

//render side bar

function render_custom_sidebar(frm){
    if(!frm.is_new()){
         
        frappe.call("ice_factory_management_system.ice_factory_management_system.doctype.html_template.html_template.get_custom_sidebar_template",{
        doc:frm.doc
    }).then(r=>{
        if(r.message){
            frm.sidebar.sidebar.append(r.message);
        }
    })
    }
    
}

//clean form sidebar
function cleanFormSidebar(){
      setTimeout(() => {
            $('.form-sidebar .sidebar-section.form-shared').remove();
            $('.form-sidebar .sidebar-section.form-assignments').remove();
            $('.form-sidebar .sidebar-section .avatar-group').parent().parent().remove();
        }, 100);
}




function hideMenus(menus=["Email","Show Link","Copy to Clipboard","Customize","Edit DocType","Jump to field","Rename","Undo","Redo"]){
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