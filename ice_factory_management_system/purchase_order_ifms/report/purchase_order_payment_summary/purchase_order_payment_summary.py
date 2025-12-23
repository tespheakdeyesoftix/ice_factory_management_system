import frappe
from frappe.utils import date_diff,today 
from frappe.utils.data import strip
import datetime
from frappe import _
def execute(filters=None): 
	if filters.filter_based_on =="Fiscal Year":
		if not filters.from_fiscal_year:
			filters.from_fiscal_year = datetime.date.today().year
		filters.start_date = '{}-01-01'.format(filters.from_fiscal_year)
		filters.end_date = '{}-12-31'.format(filters.from_fiscal_year) 
	validate(filters)
	report_data = []
	skip_total_row=False
	message=None
	if filters.get("parent_row_group"):
		report_data = get_report_group_data(filters)
		message="Enable <strong>Parent Row Group</strong> making report loading slower. Please try  to select some report filter to reduce record from database "
		skip_total_row = True
	else:
		report_data = get_report_data(filters) 
	report_chart = None
	if filters.chart_type !="None" and len(report_data)<=100:
		report_chart = get_report_chart(filters,report_data) 
	report_summary = get_report_summary(report_data,filters)
	return get_columns(filters), report_data, message, report_chart, report_summary,skip_total_row
 
def validate(filters):
	if not filters.outlet:
		filters.outlet = frappe.db.get_list("Outlet",pluck='name')
  
	if filters.start_date and filters.end_date:
		if filters.start_date > filters.end_date:
			frappe.throw("The 'Start Date' ({}) must be before the 'End Date' ({})".format(filters.start_date, filters.end_date))

	if filters.column_group=="Daily":
		n = date_diff(filters.end_date, filters.start_date)
		if n>30:
			frappe.throw("Date range cannot greater than 30 days")

	if filters.row_group and filters.parent_row_group:
		if(filters.row_group == filters.parent_row_group):
			frappe.throw("Parent row group and row group can not be the same")
 
def get_columns(filters): 
	columns = []
	columns.append({'fieldname':'row_group','label':_(filters.row_group),'fieldtype':'Data','align':'left','width':250})
	for c in get_dynamic_columns(filters):
		columns.append(c)
	return columns
 
def get_dynamic_columns(filters):
	#dynmic report file
	columns = []
	if filters.column_group =="Payment Type":
		payment_types = frappe.db.get_list("Payment Type",filters=[{"enabled":1}])
		for p in payment_types:
			if filters.row_group != "Payment Type":
				columns.append({
							"label":_(p.name),
							"fieldname":"{}".format(p.name.replace(" ", "_").replace("-","_").lower()), 
							"fieldtype":"Float",
							"align":"center",
							})
		columns.append({
       					"label":_("Total Payment"),
            			"fieldname":"total_payment", 
               			"fieldtype":"Currency",
                  		"align":"center"
                    	})
	elif filters.column_group =="Payment Type Group":
		payment_types = frappe.db.get_list("Payment Type Group",filters=[{"name":['!=', "On Account"]}])
		for p in payment_types:
			columns.append({
						"label":_(p.name),
						"fieldname":"{}".format(p.name.replace(" ", "_").replace("-","_").lower()), 
						"fieldtype":"Float",
						"align":"center",
						})
		columns.append({
						"label":_("Total Payment"),
						"fieldname":"total_payment", 
						"fieldtype":"Currency",
						"align":"center",
						})

	elif  filters.column_group in ["Daily","Monthly","Yearly","Quaterly","Half Yearly","Weekly"]:
		fields =  get_date_fields(filters)
		for f in fields:
			columns.append({
				'fieldname':f["fieldname"],
				'label': _(f["label"]),
				'fieldtype':"Float",
				'precision': None,
				'align':"center"}
			)
	return columns

def get_date_fields(filters):
	sql=""
	if filters.column_group=="Daily":
		sql = """
			select 
				concat('col_',date_format(date,'%d_%m')) as fieldname, 
				date_format(date,'%d') as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',date_format(date,'%d_%m')) , 
				date_format(date,'%d')  	
		""".format(filters.start_date, filters.end_date)
	elif filters.column_group =="Monthly":
		sql = """
			select 
				concat('col_',date_format(date,'%m_%Y')) as fieldname, 
				date_format(date,'%b %y') as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',date_format(date,'%m_%Y')) , 
				date_format(date,'%b %y')  	
		""".format(filters.start_date, filters.end_date)
	elif filters.column_group=="Weekly":
		sql = """
			select 
				concat('col_',date_format(date,'%v_%Y')) as fieldname, 
				concat('WK ',date_format(date,'%v %y')) as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',date_format(date,'%v_%Y')), 
				concat('WK ',date_format(date,'%v %y')) 
		""".format(filters.start_date, filters.end_date)
	elif filters.column_group=="Quarterly":
		sql = """
			select 
				concat('col_',QUARTER(date)) as fieldname, 
				concat('Q',QUARTER(date),' ',date_format(date,'%y')) as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',QUARTER(date)),
				concat('Q',QUARTER(date),' ',date_format(date,'%y')) 
		""".format(filters.start_date, filters.end_date)
	elif filters.column_group=="Half Yearly":
		sql = """
			select 
				concat('col_',if(month(date) between 1 and 6,'jan_jun','jul_dec'),date_format(date,'%y')) as fieldname, 
				concat(if(month(date) between 1 and 6,'Jan-Jun','Jul-Dec'),' ',date_format(date,'%y')) as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',if(month(date) between 1 and 6,'jan_jun','jul_dec'),date_format(date,'%y')), 
				concat(if(month(date) between 1 and 6,'Jan-Jun','Jul-Dec'),' ',date_format(date,'%y')) 
		""".format(filters.start_date, filters.end_date)
	elif filters.column_group=="Yearly":
		sql = """
			select 
				concat('col_',date_format(date,'%Y')) as fieldname, 
				date_format(date,'%Y') as label ,
				min(date) as start_date,
				max(date) as end_date
			from `tabDates` 
			where date between '{}' and '{}'
			group by
				concat('col_',date_format(date,'%Y')),
				date_format(date,'%Y')
		""".format(filters.start_date, filters.end_date)
	fields = frappe.db.sql(sql,as_dict=1)
	return fields
 
def get_report_field_by_payment_type(filters ):
	sqls=[]
	if filters.row_group != "Payment Type":
		payment_types = frappe.db.get_list("Payment Type")
		for p in payment_types:
			sqls.append("ifnull(sum(if(a.payment_type='{0}',a.payment_amount*a.exchange_rate,0)),0) as {1}".format(p.name,p.name.replace(" ", "_").replace("-","_").lower()))
	sqls.append("ifnull(sum(a.payment_amount*a.exchange_rate),0) as total_payment")
	return  ','.join(sqls)
 
def get_report_field_by_payment_type_group(filters):
	sqls=[]
	if filters.row_group != "Payment Type":
		payment_types = frappe.db.get_list("Payment Type Group")
		for p in payment_types:
			sqls.append("ifnull(sum(if(a.payment_type_group='{0}',a.payment_amount*a.exchange_rate,0)),0) as {1}".format(p.name,p.name.replace(" ", "_").replace("-","_").lower()))
	sqls.append("ifnull(sum(a.payment_amount*a.exchange_rate),0) as total_payment")
	return  ','.join(sqls)

def get_report_field_by_currency(filters ):
	sqls=[]
	if filters.row_group != "Payment Type":
		datas = frappe.db.get_list("Currency")
		for p in datas:
			sqls.append("ifnull(sum(if(a.currency='{0}',a.payment_amount*a.exchange_rate,0)),0) as {1}".format(p.name,p.name.replace(" ", "_").replace("-","_").lower()))
	sqls.append("ifnull(sum(a.payment_amount*a.exchange_rate),0) as total_payment")
	return  ','.join(sqls)

def get_conditions(filters,group_filter=None):
	conditions = " 1 = 1 "
	start_date = filters.start_date
	end_date = filters.end_date

	if(group_filter!=None):
		conditions += " and {} ='{}'".format(group_filter["field"],group_filter["value"].replace("'","''").replace("%","%%"))

	conditions += " AND a.posting_date between '{}' AND '{}'".format(start_date,end_date)
	if filters.outlet:
		conditions += " AND b.outlet in %(outlet)s"

	if filters.party_type:
		conditions += " AND a.party_type = %(party_type)s"
	
	if filters.party:
		conditions += " AND a.party = %(party)s" 
	
	return conditions

def get_report_data(filters,parent_row_group=None,indent=0,group_filter=None):
	row_group = [d["fieldname"] for d in get_row_groups() if d["label"]==filters.row_group][0]
	if(parent_row_group!=None):
		row_group = [d["fieldname"] for d in get_row_groups() if d["label"]==parent_row_group][0]
	sql = "select {} as row_group, {} as indent ".format(row_group, indent) + ", "
	if filters.column_group != "None":
		if filters.column_group in ["Daily","Monthly","Yearly","Quaterly","Half Yearly","Weekly"]:
			fields = get_date_fields(filters)
			for f in fields:
				sql = strip(sql)
				if sql[-1]!=",":
					sql = sql + ','
					sql = sql +	"SUM(if(a.posting_date between '{}' AND '{}',{},0)) as '{}_{}',".format(f["start_date"],f["end_date"],"a.payment_amount",f["fieldname"],f["fieldname"])
				#end for
		elif filters.column_group =="Payment Type":
			sql = sql + get_report_field_by_payment_type(filters)
		elif filters.column_group =="Payment Type Group":
			sql = sql + get_report_field_by_payment_type_group(filters)
		elif filters.column_group =="Currency":
			sql = sql + get_report_field_by_currency(filters)

	sql = sql + """ 
		FROM `tabPurchase Order Payment Invoices` AS a
		INNER JOIN `tabPurchase Order` b on b.name = a.purchase_order
		WHERE
			a.docstatus = 1 and
			{0}
		GROUP BY 
		{1} 
	""".format(get_conditions(filters,group_filter), row_group)	 

	# frappe.throw(sql)
	data = frappe.db.sql(sql,filters, as_dict=1)
	return data
 
def get_report_group_data(filters): 
	parent = get_report_data(filters, filters.parent_row_group, 0)
	data=[] 
	for p in parent:
		p["is_group"] = 1
		data.append(p)
		row_group = [d for d in get_row_groups() if d["label"]==filters.parent_row_group][0]
		children = get_report_data(filters, None, 1, group_filter={"field":row_group["fieldname"],"value":p[row_group["parent_row_group_filter_field"]]})
		for c in children:
			data.append(c)
	return data
 
def get_report_summary(data,filters):
	report_summary = []
	if filters.show_summary:
		columns = get_dynamic_columns(filters)
		for f in columns:
			value=sum(d[f["fieldname"]] for d in data if d["indent"]==0)
			report_summary.append({"label":f["label"],"value":value,"datatype":"Currency"})	
	return report_summary

def get_chart_column(data):
	columns = []
	for d in data:
		if d["indent"]==0:
			columns.append(d["row_group"])
	return columns

def get_report_chart(filters,data):
	columns = []
	dataset = []
	report_fields = get_dynamic_columns(filters)
	fields = get_chart_column(data)
	for f in fields:
		columns.append(f)
	for rf in report_fields:
		if rf["fieldname"] !="total_payment":
			dataset_values = []
			for f in fields:
				dataset_values.append(sum(d["{}".format(rf["fieldname"])] for d in data if d["indent"]==0 and d["row_group"]==f))
			dataset.append({'name':rf["label"],'values':dataset_values})
	chart = {
		'data':{
			'labels':columns,
			'datasets':dataset
		},
		"type": filters.chart_type,
		"lineOptions": {
			"regionFill": 1,
		},
		"axisOptions": {"xIsSeries": 1}
	}
	return chart

def get_row_groups():
	return [
		{
			"fieldname":"a.sale",
			"label":"Sale Invoice",
			"parent_row_group_filter_field":"row_group"
		},
  		{
			"fieldname":"a.payment_type",
			"label":"Payment Type",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"a.payment_type_group",
			"label":"Payment Type Group",
			"parent_row_group_filter_field":"row_group"
		},
   		{
			"fieldname":"if(ifnull(a.outlet,'')='','Not Set',a.outlet)",
			"label":"Outlet",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"if(ifnull(b.party,'')='','Not Set',concat(b.party,'-',b.party_name))",
			"label":"Party",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"ifnull(b.party_type,'Not Set')",
			"label":"Party Type",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"date_format(a.posting_date,'%%d/%%m/%%Y')",
			"label":"Date",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"date_format(a.posting_date,'%%m/%%Y')",
			"label":"Month",
			"parent_row_group_filter_field":"row_group"
		},
		{
			"fieldname":"date_format(a.posting_date,'%%Y')",
			"label":"Year",
			"parent_row_group_filter_field":"row_group"
		}
	]