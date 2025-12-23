// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Order Summary"] = {
	onload: function(report) {
		if(frappe.query_report.get_filter_value('filter_based_on')=="This Month"){
			frappe.query_report.toggle_filter_display('from_fiscal_year', true);
			frappe.query_report.toggle_filter_display('start_date', true  );
			frappe.query_report.toggle_filter_display('end_date', true );
		}
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
			"fieldname":"filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year","This Month", "Date Range"],
			"default": ["This Month"],
			"reqd": 1,
			on_change: function() { 
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
				if(filter_based_on=="Fiscal Year"){
					let from_fiscal_year = frappe.query_report.get_filter_value('from_fiscal_year');
					frappe.query_report.set_filter_value("start_date", start_of_year(from_fiscal_year)); 					
					frappe.query_report.set_filter_value("end_date", end_of_year(from_fiscal_year));
					
				}else if( filter_based_on =="This Month"){
					let date = new Date()
					frappe.query_report.set_filter_value("start_date", start_of_month(date)); 					
					frappe.query_report.set_filter_value("end_date", end_of_month(date));
				}else{
					let date = new Date()
					frappe.query_report.set_filter_value("start_date", date); 					
					frappe.query_report.set_filter_value("end_date", date);
				}
				if(filter_based_on!="This Month"){ 
					frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
					frappe.query_report.toggle_filter_display('start_date', filter_based_on === 'Fiscal Year'  );
					frappe.query_report.toggle_filter_display('end_date', filter_based_on === 'Fiscal Year' );				
				}else{
					frappe.query_report.toggle_filter_display('from_fiscal_year', true);
					frappe.query_report.toggle_filter_display('start_date', true  );
					frappe.query_report.toggle_filter_display('end_date', true );
				}
			}	
		},
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			default:frappe.datetime.get_today(),
			"reqd": 1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Int",
			"default": (new Date()).getFullYear(),
			"hide_in_filter":1,
			"on_change": function (query_report) {
				let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
				if(filter_based_on=="Fiscal Year"){
					let from_fiscal_year = frappe.query_report.get_filter_value('from_fiscal_year');
					frappe.query_report.set_filter_value("start_date", start_of_year(from_fiscal_year)); 					
					frappe.query_report.set_filter_value("end_date", end_of_year(from_fiscal_year));
				}
			},
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
			"options": "\nCategory\nOutlet\nStock Location\nParty Type\nParty\nDate\n\Month\nYear\nPurchase Order Invoice",
			on_change: function() { 
			}
		},
		{
			"fieldname": "row_group",
			"label": __("Row Group By"),
			"fieldtype": "Select",
			"options": "Product Code\nProduct And Price\nCategory\nOutlet\nStock Location\nParty Type\nParty\nDate\n\Month\nYear\nPurchase Order Invoice",
			"default":"Category",
			on_change: function() { 
			},
		},
		{
			"fieldname": "column_group",
			"label": __("Column Group By"),
			"fieldtype": "Select",
			"options": "None\nDaily\nWeekly\nMonthly\nQuarterly\nHalf Yearly\nYearly",
			"default":"None",
			hide_in_filter:1,
			"on_change": function (query_report) {},
		},
		{
			"fieldname": "product_category",
			"label": __("Product Category"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Product Category', txt);
			},
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
	
};

function start_of_month(date)
{
    return new Date(date.getFullYear(), date.getMonth(), 1);
}
function end_of_month(date)
{
	let lastDate = new Date(date.getFullYear(), date.getMonth() + 1, 0); 
    return new Date(date.getFullYear(), date.getMonth(), lastDate.getDate() ) ;
}

function start_of_year(year)
{
    return new Date(year, 0, 1); // January 1st
}
function end_of_year(year)
{
    return new Date(year, 11, 31);// December 31st
}
