frappe.treeview_settings['Account Code'] = {
    breadcrumb: 'Account Code',
    title: 'Account Code',
    fields: [
        {
            fieldtype:'Check', 
            fieldname:'is_group', 
            label:__('Is Group'),
            reqd:true
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
    extend_toolbar: true
}
