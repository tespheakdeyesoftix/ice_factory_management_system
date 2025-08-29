import frappe
from frappe.utils import today 
from frappe import _

def execute(filters=None): 
	validate(filters)
	report_data = []
	skip_total_row=False
	if filters.show_sale_transaction:
		skip_total_row=True
	report_data = get_report_data(filters) 
	report_summary = None
	if filters.show_summary==1:
		report_summary =get_report_summary(report_data,filters)
	return get_columns(filters), report_data, None, None, report_summary,skip_total_row

def validate(filters):
	if not filters.start_date:
		filters.start_date = today()
	if not filters.end_date:
		filters.end_date = today()
	if not filters.outlet:
		filters.outlet = frappe.db.get_list("Outlet",pluck='name')
 
def get_columns(filters):
	if filters.show_sale_transaction:
		return [
			{"label":"Customer", "fieldname":"row_group","fieldtype":"Data","align":"left","width":200},
			{"label":"Date", "fieldname":"posting_date","fieldtype":"Date","align":"center","width":100},
			{"label":"Total Amount", "fieldname":"total_amount","fieldtype":"Currency","align":"right","width":120},
			{"label":"Total Paid", "fieldname":"total_payment","fieldtype":"Currency","align":"right","width":120},
			{"label":"Balance", "fieldname":"balance","fieldtype":"Currency","align":"right","width":120}
		]
	else:
		return [
			{"label":"Customer", "fieldname":"row_group","fieldtype":"Data","align":"left","width":200},
			{"label":"Total Amount", "fieldname":"total_amount","fieldtype":"Currency","align":"right","width":120},
			{"label":"Total Paid", "fieldname":"total_payment","fieldtype":"Currency","align":"right","width":120},
			{"label":"Balance", "fieldname":"balance","fieldtype":"Currency","align":"right","width":120}
		]
 
def get_conditions(filters,group_filter=None):
	conditions = ""
	end_date = filters.end_date
	start_date = filters.start_date
	conditions += "a.posting_date between '{0}' and '{1}'".format(start_date,end_date)
	if filters.get("customer_group"):
		conditions += " AND a.customer_group in %(customer_group)s"
	if filters.get("customer"):
		conditions += " AND a.customer = %(customer)s"
	if filters.get("outlet"):
		conditions += " AND a.outlet in %(outlet)s"
	return conditions

def get_report_data(filters,parent_row_group=None,indent=0,group_filter=None):
	sql = """
	select
		0 as indent,
		a.customer,
		if(ifnull(a.customer,'')='','Not Set',concat(a.customer ,'-',a.customer_name)) as row_group,
		sum(a.total_amount) as total_amount,
		sum(a.total_payment) as total_payment,
		sum(a.balance) as balance
	FROM `tabSale` AS a
	where
		a.balance > 0 and 
	{1}
	group by 
		if(ifnull(a.customer,'')='', 'Not Set',concat(a.customer ,'-',a.customer_name))
	""".format(filters.end_date, get_conditions(filters,group_filter))
	data = frappe.db.sql(sql,filters, as_dict=1)
	
	if not filters.show_sale_transaction:
		return data
	else:
		report_data = []
		for  d in data:
			report_data.append(d)
			report_data = report_data + get_sale_transaction_data(filters, d.customer)
		return report_data

def get_sale_transaction_data(filters,customer):
	sql = """select
		1 as indent,
		a.name as row_group,
		a.posting_date,
		a.total_amount,
		a.total_payment,
		a.balance as balance
	FROM `tabSale` AS a
	where
		a.balance > 0 and 
		a.customer = '{1}' and
	{2}
	""".format(filters.end_date,customer, get_conditions(filters))
	data = frappe.db.sql(sql,filters, as_dict=1)
	return data


def get_report_summary(data,filters):
	report_summary = [] 
	report_summary.append({"label":_("Total Amount"),"value":frappe.utils.fmt_money(sum(a.total_amount for a in data if a.indent ==0)),"indicator":"blue"})	
	report_summary.append({"label":_("Total Paid"),"value":frappe.utils.fmt_money(sum(a.total_payment for a in data if a.indent ==0)),"indicator":"green"})	
	report_summary.append({"label":_("Balance"),"value":frappe.utils.fmt_money(sum(a.balance for a in data if a.indent ==0)),"indicator":"orange"})	
	return report_summary

 