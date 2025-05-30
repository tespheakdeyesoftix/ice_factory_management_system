# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.document import bulk_insert
from frappe.model.naming import make_autoname
from ice_factory_management_system.api.utils import get_previous_closed_date

class ClosedSellingDate(Document):
	def on_submit(self):
		generate_closed_selling_date_data(self)
	
	def validate(self):
		get_previous_closed_date(self.posting_date,self.creation,self.outlet)
		data = get_closed_date_data(self.outlet)
		if len(data or []) > 0:
			for a in self.closed_selling_date_items:
				for b in data:
					if a.total_name == b.get("total_name"):
						a.total_amount = b.get("total_amount")

def generate_closed_selling_date_data(self):
	data = []
	previous_closed_date = ""
	p = frappe.db.sql("select CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) posting_date from `tabClosed Selling Date` where docstatus=1 and name != '{0}' and outlet = '{1}' order by CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) desc limit 1".format(self.name,self.outlet),as_dict=1)
	if len(p or []) > 0:
		previous_closed_date = "and CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) > '{0}'".format(p[0]["posting_date"])
	closed_doctypes = frappe.get_doc("Business Information").closed_doctypes
	for a in closed_doctypes:
		docs = frappe.db.sql("select name,total_amount from `tab{0}` where outlet = '{1}' {2}".format(a.closed_doctype,self.outlet,previous_closed_date),as_dict=1)
		for b in docs:
			data.append({"doctype":"Closed Selling Date Data","closed_selling_date":self.name,"closed_doctype":a.closed_doctype,"closed_docname": b["name"],"total_amount": b["total_amount"]})
	bulk_submit(docs=data)
      
def bulk_submit(docs):
    bulk_insert("Closed Selling Date Data", get_bulk_entry_record(docs=docs) , chunk_size=10000)
    frappe.db.commit()

def get_bulk_entry_record(docs):
	from datetime import datetime
	for d in docs:
		doc = frappe.get_doc(d)
		doc.closed_date = datetime.now()
		doc.name  = make_autoname("CSDD.YYYY.-.#####")
		doc.docstatus = 1
		yield doc

@frappe.whitelist()
def get_closed_date_data(outlet):
	data = []
	previous_closed_date = ""
	previous_closed_date_data = frappe.db.sql("select CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) posting_date from `tabClosed Selling Date` where docstatus=1 and outlet = '{0}' order by CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) desc limit 1".format(outlet),as_dict=1)
	if len(previous_closed_date_data or []) > 0:
		previous_closed_date = "and CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) > '{0}'".format(previous_closed_date_data[0]["posting_date"])
	closed_doctypes = frappe.get_doc("Business Information").closed_doctypes
	for a in closed_doctypes:
		note = "("+a.note+")" if (a.note or "") != "" else ""
		status = " and docstatus = 1"
		if a.closed_doctype == "Sale":
			status = " and sale_status = 'Closed'"
		elif a.closed_doctype == "Journal Entry":
			status += " and entry_type = 'Cash Transfer'"
		else:
			pass
		sql = "select '{0}',sum(total_amount) total_amount from `tab{0}` where outlet = '{1}' {2} {3}".format(a.closed_doctype,outlet,previous_closed_date,status)
		datas = frappe.db.sql(sql,as_dict=1)
		if len(datas or []) > 0:
			data.append({"total_name":a.closed_doctype+note,"total_amount": datas[0]["total_amount"]})
		else:
			data.append({"total_name":a.closed_doctype+note,"total_amount": 0})
	return data
