# Copyright (c) 2024, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from ice_factory_management_system.account_ifmf.doctype.chart_of_account.chart_of_account import get_hierarchy_account_for_report_by_parent,get_timespan_report_column,get_filter_date_range

def execute(filters=None):
	get_hierarchy_account_for_report_by_parent.cache_clear()
	columns = get_report_columns(filters)
	data  = get_data(filters)
	report_data = get_report_data(filters,raw_data=data)
	report_chart = get_report_chart(columns=columns, data=data)
	report_summary = get_report_summary(data)
	return columns, report_data,None,report_chart,report_summary

def get_report_columns(filters):
	columns = []
	columns.append({
		"fieldname":"account",
		"label":_("Account"),
		"fieldtype":"Data",
		"width":350
	})
	dynamic_column_data =  get_timespan_report_column(filters=filters)
	for c in dynamic_column_data:
		columns.append({
			"fieldname":c["name"],
			"label": c["column_group"],
			"fieldtype":"Currency",
			"width":150 if len(c["column_group"])<=8 else 125,
			"align":"right",
		})
	columns.append({
		"fieldname":"total",
		"label": _("Total"),
		"fieldtype":"Currency",
		"width":150,
		"align":"right"
	})
	return columns

def get_report_data(filters,raw_data=None):
	branch = frappe.get_doc("Business Information")
	report_data=[]
	income_accounts = get_hierarchy_account_for_report_by_parent(parent=branch.income_head_account)
	expense_accounts = get_hierarchy_account_for_report_by_parent(parent=branch.expense_head_account)
	income_data = [d for d in raw_data if d["root_type"]=="Income"]
	expense_data = [d for d in raw_data if d["root_type"]=="Expenses"]
	if income_data:
		report_data = income_accounts
		report_data=report_data + [{},get_total_row(_("Total Income(Credit)"), income_data) ]
	if expense_data:
		if income_data:
			report_data.append({})
		report_data = report_data + expense_accounts
		report_data = report_data + [{},get_total_row(_("Total Expenses(Debit)"), expense_data)]
	if report_data:
		report_data=report_data+[{} , (get_grand_total_row(raw_data))]
	for d in raw_data:
		row = [x for x in report_data if "account" in x and  x["account"]==d["account"]]
		if row:
			row = row[0]
			column_name = d["column_group"]
			row[column_name] = d["amount"]
			if not "total" in row:
				row["total"] = d["amount"]
			else:
				row["total"] = row["total"] + d["amount"]
			parent_row = [d for d in   report_data if "account" in d and d["account"] == row["parent_chart_of_account"]]
			while parent_row:
				parent_row = parent_row[0]
				if column_name in parent_row:
					parent_row[column_name] =parent_row[column_name] +  d["amount"]
				else:
					parent_row[column_name] = d["amount"]
				if "total" in parent_row:
					parent_row["total"] = parent_row["total"] + d["amount"]
				else:
					parent_row["total"] = d["amount"]
				parent_row = [d for d in   report_data if "account" in d and d["account"] == parent_row["parent_chart_of_account"]]
	report_data = [
		{key: value for key, value in d.items() if value != 0 or key == 'indent'}
		for d in report_data
	]
	report_data = [d for d in report_data if not len(d.keys())==3]
	return report_data

def get_report_chart(columns, data):
	labels = [d.get("label") for d in columns if not d.get("fieldname") in ["account","total"]]
	fieldnames = [d.get("fieldname") for d in columns if not d.get("fieldname") in ["account","total"]]
	income_data, expense_data, net_profit = [], [], []
	for f in fieldnames:
		income_data.append(sum([d["amount"] for d in data if d["root_type"]=="Income" and d["column_group"] ==f] ))
		expense_data.append(sum([d["amount"] for d in data if d["root_type"]=="Expenses" and d["column_group"] ==f]))
		net_profit.append(sum([d["amount"] * (1 if d["root_type"]=="Income" else -1) for d in data if  d["column_group"] ==f]))
	if len(fieldnames)>1:
		labels = [d.get("label") for d in columns if d.get("fieldname") not in ["account"]]
		income_data.append(sum([d["amount"] for d in data if d["root_type"]=="Income"] ))
		expense_data.append(sum([d["amount"] for d in data if d["root_type"]=="Expenses" ]))
		net_profit.append(sum([d["amount"] * (1 if d["root_type"]=="Income" else -1) for d in data]))
	datasets = []
	if income_data:
		datasets.append({"name": _("Income"), "values": income_data})
	if expense_data:
		datasets.append({"name": _("Expense"), "values": expense_data})
	if net_profit:
		datasets.append({"name": _("Net Profit/Loss"), "values": net_profit})
	chart = {"data": {"labels": labels, "datasets": datasets}}
	chart["type"] = "bar"
	chart["fieldtype"] = "Currency"
	return chart

def get_report_summary(data):
	net_profit = sum([d["amount"] * (1 if d["root_type"]=="Income" else -1) for d in data])
	return [
		{"value": sum([d["amount"] for d in data if d["root_type"]=="Income"]), "label": _("Total Income"), "datatype": "Currency"},
		{"type": "separator", "value": "-"},
		{"value": sum([d["amount"] for d in data if d["root_type"]=="Expenses"]), "label": _("Total Expense"), "datatype": "Currency"},
		{"type": "separator", "value": "=", "color": "blue"},
		{
			"value": net_profit,
			"indicator": "Green" if net_profit > 0 else "Red",
			"label": _("Net Profit"),
			"datatype": "Currency",
		},
	]

def get_data(filters):
	outlet = ""
	if filters.outlet:
		outlet = "a.outlet = %(outlet)s  and "
	column_group_info= get_data_info(filters.column_group)
	filters=get_filter_date_range(filters)
	sql = """
		select 
			{0},
			c.root_type,
			a.account,
			sum(if(c.root_type='Income',a.credit_amount-a.debit_amount,a.debit_amount-a.credit_amount)) as amount
		from `tabGL Entry` a
		inner join `tabChart of Account` c on c.name = a.account

		where
			a.posting_date between %(start_date)s and %(end_date)s and
			{1}
			c.root_type in ('Income','Expenses') and 
			a.is_cancelled = 0
		group by
			account,
			c.root_type,
			{2}
	""".format(
		column_group_info["sql_expression"],
		outlet,
		column_group_info["group_by_expression"]
	)
	data = frappe.db.sql(sql,filters,as_dict=1)
	return data

def get_data_info(key):
    return [d for d in column_data_keys() if d["key"] == key][0]

def column_data_keys():
    return [
        {"key":"Yearly","sql_expression":"date_format(a.posting_date,'%%Y') as column_group", "group_by_expression":"date_format(a.posting_date,'%%Y')" },
        {"key":"Monthly","sql_expression":"date_format(a.posting_date,'%%b %%y') as column_group", "group_by_expression":"date_format(a.posting_date,'%%b %%y')" },
        {"key":"Quarterly","sql_expression":"concat(QUARTER(a.posting_date),'-', date_format(a.posting_date,'%%Y')) as column_group", "group_by_expression":"concat(QUARTER(a.posting_date),'-', date_format(a.posting_date,'%%Y'))" },
        {"key":"Half-Yearly","sql_expression":"concat(floor((month(a.posting_date)-1)/6),'-', date_format(a.posting_date,'%%Y')) as column_group", "group_by_expression":"concat(floor((month(a.posting_date)-1)/6),'-', date_format(a.posting_date,'%%Y'))" },
    ]


def get_total_row(label, data):
	row = {"account": label,"indent":0,"is_total_row":1}
	for c in set([d["column_group"] for d in data]):
		row[c] = sum([d["amount"] for d in data if d["column_group"]==c])
	row["total"] = sum([d["amount"] for d in data])
	return row

def get_grand_total_row(data):
	row = {"account": _("Grand Total"),"is_total_row":1,"indent":0}
	for c in set([d["column_group"] for d in data]):
		row[c] = sum([d["amount"] * (1 if d["root_type"]=="Income" else -1) for d in data if d["column_group"]==c])
	row["total"] = sum([d["amount"] * (1 if d["root_type"]=="Income" else -1) for d in data])
	return row


