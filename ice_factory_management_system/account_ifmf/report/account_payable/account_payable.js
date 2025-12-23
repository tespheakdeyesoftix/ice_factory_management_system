// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Account Payable"] = {
	onload: function(report) {
		report.page.add_inner_button("Preview Report", function () {
			frappe.query_report.refresh();
		});
		
	},
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
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"on_change": function (query_report) {},
		},
		{
            "fieldname": "party_type",
            "label": __("Party Type"),
            "fieldtype": "Select",
            "default": "Vendor",
            "options": ["Vendor", "Employee", "Customer"],
            "on_change": function(query_report) {
				let party_type = frappe.query_report.get_filter_value('party_type');
				frappe.query_report.toggle_filter_display('party', party_type === "");

                // clear previous party
                query_report.set_filter_value("party", "");
                // // refresh the Dynamic Link filter
                // const party_filter = query_report.get_filter("party");
                // if (party_filter) {
                //     party_filter.refresh(); 
                // }
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
			"fieldname": "show_chart",
			"label": __("Show Chart"),
			"fieldtype": "Check",
			"default":true,
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "show_summary",
			"label": __("Show Summary"),
			"fieldtype": "Check",
			"default":true,
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "show_zero_amount",
			"label": __("Show Zero"),
			"fieldtype": "Check",
			"default":false,
			"on_change": function (query_report) {},			
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.indent==0 && frappe.query_report.get_filter_value('show_sale_transaction')==1) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
