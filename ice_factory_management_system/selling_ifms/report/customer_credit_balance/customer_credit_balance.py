import frappe
from frappe.utils import today 
from frappe import _

def execute(filters=None): 
	validate(filters)
	#run this to update parent_product_group in table sales invoice item
	report_data = []
	skip_total_row=False
	if filters.show_sale_transaction:
		skip_total_row=True
	report_data = get_report_data(filters) 
	report_chart = None
	if filters.show_chart:
		report_chart = get_report_chart(report_data)
	report_summary = []
	if filters.show_summary:
		report_summary =get_report_summary(report_data,filters)	
	return  get_columns(filters), report_data, None, report_chart, report_summary , skip_total_row

def validate(filters):
	if not filters.end_date:
		filters.end_date = today()
 
def get_columns(filters):
	return [
		{"label":_("Customer"), "fieldname":"row_group","fieldtype":"Data","align":"left","width":200},
		{"label":_("Opening Amount"), "fieldname":"opening_amount","fieldtype":"Currency","align":"right","width":150},
		{"label":_("Current Amount"), "fieldname":"current_amount","fieldtype":"Currency","align":"right","width":150},
		{"label":_("Current Payment"), "fieldname":"current_payment","fieldtype":"Currency","align":"right","width":150},
		{"label":_("Write Off"), "fieldname":"write_off","fieldtype":"Currency","align":"right","width":150},
		{"label":_("Balance"), "fieldname":"balance","fieldtype":"Currency","align":"right","width":150}
	]

def get_conditions(filters):
	conditions = ""
	conditions += "a.posting_date between '{0}' and '{1}'".format(filters.start_date,filters.end_date)
	if filters.get("customer"):
		conditions += " AND a.party in %(customer)s"
	if filters.outlet:
		conditions += " AND a.outlet in %(outlet)s"
	return conditions

def get_customers_condition(filters):
	conditions = "1=1"
	if filters.get("customer"):
		conditions += " AND a.name in %(customer)s"
	return conditions

def get_report_data(filters):
	sql = """with sales as(select
		coalesce(a.party,'Not Set') party, 	
		(if(a.voucher_type = 'Sale',a.credit_amount-a.debit_amount, 0)) as current_amount,
		(if(a.voucher_type = 'Sale Payment' and a.transaction_type = 'Payment',a.credit_amount-a.debit_amount, 0)) as current_payment,
		(if(a.voucher_type = 'Sale Payment' and a.transaction_type = 'Write Off',a.credit_amount-a.debit_amount, 0)) as write_off
	FROM `tabGL Entry` AS a
	where
		coalesce(party,'') != '' and is_cancelled=0 and voucher_type in ('Sale','Sale Payment') and
	{0})
	select
	a.name,
	if(ifnull(a.name,'')='','Not Set',concat(a.name ,'-',coalesce(a.customer_name,'Not Set'))) as row_group,
	coalesce(sum(current_amount),0) current_amount,
	coalesce(sum(current_payment),0) current_payment,
	coalesce(sum(write_off),0) write_off
	from `tabCustomer` a
	left join sales b on b.party = a.name
	where 
	{1}
	group by 
		a.name,
		if(ifnull(a.name,'')='','Not Set',concat(a.name ,'-',coalesce(a.customer_name,'Not Set')))
	""".format(get_conditions(filters),get_customers_condition(filters))	
	data = frappe.db.sql(sql,filters, as_dict=1)
	datas=[]
	for a in data:
		a["opening_amount"] = get_opening_balance(a["name"],filters)
		a["balance"] = a["opening_amount"] + a["current_amount"] + (a["current_payment"] + a["write_off"])
		if filters.show_zero_amount:
			datas.append(a)
		else:
			if (abs(a["opening_amount"]) + abs(a["current_amount"]) + abs(a["current_payment"]) + abs(a["write_off"])) > 0:
				datas.append(a)
	return datas

def get_opening_balance(party,filters):
	conditions = ""
	if filters.outlet:
		conditions += " AND a.outlet in %(outlet)s"
	sql = """select
		sum(if(a.posting_date<'{0}',a.credit_amount-a.debit_amount, 0)) as opening_amount
	FROM `tabGL Entry` AS a
	where
		coalesce(party,'') = '{1}' {2}
	""".format(filters.start_date,party,conditions)	
	data = frappe.db.sql(sql,filters, as_dict=1)
	return data[0]['opening_amount'] or 0

def get_report_chart(data):
	chart_data = []
	chart_data.append(sum(d["current_amount"] for d in data))
	chart_data.append(sum(d["current_payment"] for d in data))
	chart_data.append(sum(d["write_off"] for d in data))
	chart =  {'data':
     			{
            		'labels':[_('Current Amount'),_("Current Payment"),_("Write Off")],
              		'datasets':[{'values':chart_data}]
                },
        		'type':'percentage'
             }
	return chart

def get_report_summary(data,filters):
	report_summary = [] 
	report_summary.append({"label":_("Opening Amount"),"value":frappe.utils.fmt_money(sum(a["opening_amount"] for a in data)),"indicator":"blue"})	
	report_summary.append({"label":_("Current Amount"),"value":frappe.utils.fmt_money(sum(a["current_amount"] for a in data)),"indicator":"blue"})	
	report_summary.append({"label":_("Current Payment"),"value":frappe.utils.fmt_money(sum(a["current_payment"] for a in data)),"indicator":"green"})	
	report_summary.append({"label":_("Write Off"),"value":frappe.utils.fmt_money(sum(a["current_payment"] for a in data)),"indicator":"green"})	
	report_summary.append({"label":_("Balance"),"value":frappe.utils.fmt_money(sum(a["balance"] for a in data)),"indicator":"orange"})	
	return report_summary

 