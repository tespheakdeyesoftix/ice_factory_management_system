import frappe
from frappe.utils import today 
from frappe import _

def execute(filters=None): 
	validate(filters)
	report_data = get_report_data(filters) 
	report_summary = None
	if filters.show_summary==1:
		report_summary =get_report_summary(report_data,filters)
	return get_columns(filters), report_data, None, None, report_summary,0

def validate(filters):
	if not filters.start_date:
		filters.start_date = today()
	if not filters.end_date:
		filters.end_date = today()
	if not filters.outlet:
		filters.outlet = frappe.db.get_list("Outlet",pluck='name')
 
def get_columns(filters):
	return [
		{"label":"Posting Date", "fieldname":"posting_date","fieldtype":"Date","align":"center","width":150},
		{"label":"Customer", "fieldname":"customer","fieldtype":"Data","align":"center","width":100},
		{"label":"Customer Name", "fieldname":"customer_name","fieldtype":"Data","align":"left","width":200},
		{"label":"Sale", "fieldname":"name","fieldtype":"Data","align":"center","width":200},
		{"label":"Total Amount", "fieldname":"total_amount","fieldtype":"Currency","align":"right","width":150},
		{"label":"Total Paid", "fieldname":"total_payment","fieldtype":"Currency","align":"right","width":150},
		{"label":"Write Off Amount", "fieldname":"write_off_amount","fieldtype":"Currency","align":"right","width":150},
		{"label":"Balance", "fieldname":"balance","fieldtype":"Currency","align":"right","width":150}
	]
 
def get_conditions(filters,group_filter=None):
	conditions = "a.sale_status = 'Closed'"
	end_date = filters.end_date
	start_date = filters.start_date
	conditions += " and a.posting_date between '{0}' and '{1}'".format(start_date,end_date)
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
		a.name,
		a.posting_date,
		a.customer,
		a.customer_name,
		a.total_amount,
		0 payment_amount,
		0 write_off_amount,
		0 balance,
		'child' type
	FROM `tabSale` AS a
	where
	{1}
	""".format(filters.end_date, get_conditions(filters,group_filter))
	data = frappe.db.sql(sql,filters, as_dict=1)
	for a in data:
		b = get_payment_and_write_off(a["name"],filters)
		a["payment_amount"] = b["payment_amount"]
		a["write_off_amount"] = b["write_off_amount"]
		a["balance"] = a["total_amount"] - b["payment_amount"] - b["write_off_amount"]
	if filters.group_by_customer == 1:
		group = list(dict.fromkeys(item["customer"] for item in data))
		grouped_list = []
		for a in group:
			for b in data:
				if a == b["customer"]:
					grouped_list.append(b)
			total_amount = sum(c["total_amount"] for c in grouped_list if c["customer"] == a)
			payment_amount = sum(c["payment_amount"] for c in grouped_list if c["customer"] == a)
			write_off_amount = sum(c["write_off_amount"] for c in grouped_list if c["customer"] == a)
			balance = sum(c["balance"] for c in grouped_list if c["customer"] == a)
			customer = [c["customer_name"] for c in grouped_list if c["customer"] == a]
			grouped_list.append({"customer":a,"customer_name":customer[0],"total_amount":total_amount,"payment_amount":payment_amount,"write_off_amount":write_off_amount,"balance":balance,"type":"parent"})
			grouped_list.append({"customer":"","total_amount":0,"payment_amount":0,"write_off_amount":0,"balance":0,"type":"breaker"})
		data = grouped_list
	return data

def get_payment_and_write_off(sale,filters):
	sql = """select 
		coalesce(sum(payment_amount),0) payment_amount,
		coalesce(sum(write_off_amount),0) write_off_amount
		from `tabSale Payment Invoices`
		where sale = '{0}' and posting_date between '{1}' and '{2}'""".format(sale,filters.start_date,filters.end_date)
	payment = frappe.db.sql(sql,as_dict=1)
	return payment[0]

def get_report_summary(data,filters):
	report_summary = [] 
	report_summary.append({"label":_("Total Amount"),"value":frappe.utils.fmt_money(sum(a["total_amount"] for a in data)),"indicator":"blue"})	
	report_summary.append({"label":_("Total Paid"),"value":frappe.utils.fmt_money(sum(a["payment_amount"] for a in data)),"indicator":"green"})	
	report_summary.append({"label":_("Write Off Amount"),"value":frappe.utils.fmt_money(sum(a["write_off_amount"] for a in data)),"indicator":"orange"})	
	report_summary.append({"label":_("Balance"),"value":frappe.utils.fmt_money(sum(a["balance"] for a in data)),"indicator":"orange"})	
	return report_summary

 