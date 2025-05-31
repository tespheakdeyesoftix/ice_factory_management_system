frappe.treeview_settings['Account Code'] = {
    breadcrumb: 'Account Code',
    title: 'Account Code',
    get_tree_root: false,
    get_tree_nodes: 'ice_factory_management_system.selling_ifms.doctype.account_code.account_code.get_children',
    filters: [
		{
			fieldname: "outlet",
			fieldtype:"Select",
			options: [],
			label: __("Outlet")
		}
	],
    fields: [
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group'),
            reqd:true
        },
        {
			fieldname: "outlet",
			fieldtype:"Link",
			options: "Outlet",
			label: __("Outlet"),
		},
        {
            fieldtype:'Data', 
            fieldname:'account_code', 
            label:__('Account Code')
        },
        {
            fieldtype:'Data', 
            fieldname:'account_name', 
            label:__('Account Name')
        },
        {
            fieldtype:'Select', 
            fieldname:'root_type', 
            label:__('Root Type'), 
            options:"Asset\nLiabilities\nEquity\nIncome\nExpenses"
        },
        {
            fieldtype:'Select', 
            fieldname:'account_type', 
            label:__('Account Type'),
            options:"\nReceivable\nPayable\nCash\nBank\nIncome\nExpense\nTemporary"
        }
    ],
    extend_toolbar: true,
    onload(treeview) {
        frappe.db.get_list("Outlet", {
            fields: ["name"]
        }).then(outlets => {
            const outlet_filter = treeview.page.fields_dict.outlet;
            outlet_filter.df.options = outlets.map(o => o.name);
            outlet_filter.value = outlets.length > 0 ? outlets[0].name : "";
            outlet_filter.refresh();
            outlet_filter.$input.trigger("change");
            treeview.make_tree();
        });
    }
}