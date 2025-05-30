frappe.treeview_settings['Account Code'] = {
    breadcrumb: 'Account Code',
    title: 'Account Code',
    get_tree_root: false,
    get_tree_nodes: 'ice_factory_management_system.selling_ifms.doctype.account_code.account_code.get_children',
    filters: [
		{
			fieldname: "outlet",
			fieldtype:"Link",
			options: "Outlet",
			label: __("Outlet"),
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
}
