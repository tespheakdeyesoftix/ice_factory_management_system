// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Credit Balance"] = {
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
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Customer', txt);
			},
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
			"fieldname": "show_chart",
			"label": __("Show Chart"),
			"fieldtype": "Check",
			"default":false,
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
