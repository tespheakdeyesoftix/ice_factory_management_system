// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Business Information", {
    refresh(frm) {
        frm.add_custom_button('Reset Transaction', () => {
            frappe.prompt(
                {
                    label: 'Enter Password',
                    fieldname: 'password',
                    fieldtype: 'Password',
                    reqd: 1
                },
                (values) => {
                    frappe.call({
                        method: 'ice_factory_management_system.api.utils.reset_sale_transaction',
                        args: {
                            password: values.password
                        },
                        callback: (r) => {
                            if (r.message == "reset") {
                                frappe.msgprint(__('Transaction has been reset.'));
                            }
                            else{
                                frappe.msgprint(__('Wrong password.'));
                            }
                        }
                    });
                },
                'Security Check'
            );
        });
    }
});
