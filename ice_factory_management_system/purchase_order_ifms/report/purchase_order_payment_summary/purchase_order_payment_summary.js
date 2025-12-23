// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt
frappe.query_reports["Purchase Order Payment Summary"] = {
	"filters": [
		{
			"fieldname": "outlet",
			"label": __("Outlet"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Outlet', txt);
			},
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year", "Date Range"],
			"default": ["Fiscal Year"],
			"reqd": 1,
			on_change: function() {
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
				frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
				frappe.query_report.toggle_filter_display('start_date', filter_based_on === 'Fiscal Year');
				frappe.query_report.toggle_filter_display('end_date', filter_based_on === 'Fiscal Year');
			},
		},
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"hidden": 1,
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"hidden": 1,
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Int",
			"on_change": function (query_report) {},
			"default": (new Date()).getFullYear(),
			hide_in_filter:1,
		},
		{
            "fieldname": "party_type",
            "label": __("Party Type"),
            "fieldtype": "Select",
            "default": "Vendor",
            "options": ["Vendor", "Employee", "Customer"],
            "on_change": function(query_report) {
                // clear previous party
                query_report.set_filter_value("party", "");
                // refresh the Dynamic Link filter
                const party_filter = query_report.get_filter("party");
                if (party_filter) {
                    party_filter.refresh(); 
                }
            }
        },
        {
            "fieldname": "party",
            "label": __("Party"),
            "fieldtype": "DynamicLink",
            "get_options": function() {
                // return current party_type value
                return frappe.query_report.get_filter_value("party_type");
            },

			"on_change": function (query_report) {},
        },
		{
			"fieldname": "parent_row_group",
			"label": __("Parent Group By"),
			"fieldtype": "Select",
			"options": "\nOutlet\nParty Type\nParty\nDate\n\Month\nYear\nPayment Type Group",
			"on_change": function (query_report) {},
			hide_in_filter:1,
		},
		{
			"fieldname": "row_group",
			"label": __("Row Group By"),
			"fieldtype": "Select",
			"options": "Outlet\nParty Type\nParty\nDate\n\Month\nYear\nPurchase Order Invoice\nPayment Type\nPayment Type Group",
			"default":"Date",
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "column_group",
			"label": __("Column Group By"),
			"fieldtype": "Select",
			"options": "Payment Type\nPayment Type Group",
			"default":"Payment Type",
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "chart_type",
			"label": __("Chart Type"),
			"fieldtype": "Select",
			"options": "None\nbar\nline\npie",
			"default":"bar",
			hide_in_filter:1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "show_summary",
			"label": __("Show Summary"),
			"fieldtype": "Check",
			default:true,
			hide_in_filter:1,
			"on_change": function (query_report) {},
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.is_group==1) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
	onload: function(report) {
		report.page.add_inner_button("Preview Report", function () {
			frappe.query_report.refresh();
		});	
	},
};

 