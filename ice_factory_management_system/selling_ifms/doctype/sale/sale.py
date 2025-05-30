# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json
from datetime import datetime, date
from ice_factory_management_system.api.utils import cancel_general_ledger_entery,get_previous_closed_date
class Sale(Document):
	def validate(self):
		self.validate_require_fields()
		if self.update_from == "Sale":
			get_previous_closed_date(self.posting_date,self.creation,self.outlet)
		verify_account(self)
		verify_product(self)
		update_total_amounts(self)
		verify_sale_payment(self)
		update_payment_status(self)
		verify_before_GL_submit(self)
            
	def before_insert(self):
		self.total_payment = 0
		self.total_write_off = 0
		self.balance = self.total_amount	
		get_customer_product_price(self)	

	def validate_require_fields(self):

		if self.sale_status=='Closed' and not self.customer:
			frappe.throw(_("Please select customer"))



def verify_before_GL_submit(self):
	if self.is_new():
		if self.sale_status == "Closed":
			submit_to_GL_entry(self)
	else:
		if self.update_from  == "Sale" :
			previous = self.get_doc_before_save()
			if previous.get("sale_status") == "Draft" and self.sale_status == "Closed":
				submit_to_GL_entry(self)
			elif previous.get("sale_status") == "Closed" and self.sale_status == "Closed":
				if verify_child_table(self) == 1 or self.customer != previous.customer:
					cancel_general_ledger_entery(self.doctype,self.name)
					submit_to_GL_entry(self)
			elif previous.get("sale_status") == "Closed" and (self.sale_status == "Deleted" or self.sale_status == "Draft"):
				cancel_general_ledger_entery(self.doctype,self.name)
			elif previous.get("sale_status") == "Deleted" and self.sale_status == "Closed":
				submit_to_GL_entry(self)
			else:
				pass
	self.update_from = "Sale"

def verify_child_table(self):
	msg = []
	old_doc = self.get_doc_before_save()
	if not old_doc:
		for row in self.sale_products:
			msg.append({"New row added": f"{row.product_code}"})
		return
	old_rows_map = {row.name: row for row in old_doc.sale_products}
	for row in self.sale_products:
		if row.name not in old_rows_map:
			msg.append({"New row added": f"{row.product_code}"})
		else:
			old_row = old_rows_map[row.name]
			changed_fields = []
			for field in ['product_code', 'quantity', 'price']:  # fields you want to track
				if getattr(row, field) != getattr(old_row, field):
					changed_fields.append(field)
			if changed_fields:
				msg.append({f"Row {row.idx} changed fields:":f"{', '.join(changed_fields)}"})
	current_row_names = [row.name for row in self.sale_products]
	for old_row in old_doc.sale_products:
		if old_row.name not in current_row_names:
			msg.append({"Row deleted": f"{old_row.product_code}"})
	if len(msg)>0:
		return 1
	else:
		return 0		

def verify_account(self):
	from ice_factory_management_system.system_setting.doctype.outlet.outlet import get_default_accounts
	default = get_default_accounts(self.outlet)
	self.default_income_account = default.get("income_account") if (self.default_income_account or "") == "" else self.default_income_account
	self.default_receivable_account = default.get("receivable_account") if (self.default_receivable_account or "") == "" else self.default_receivable_account
	self.default_free_account = default.get("free_account") if (self.default_free_account or "") == "" else self.default_free_account
	
def update_total_amounts(self):
	self.total_quantity = (sum((d.quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.total_free = (sum((d.free_quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.total_sale_quantity = (sum((d.quantity or 0)-(d.free_quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)

	self.total_amount = (sum((d.price or 0)*(d.total_sale_quantity or 0)*(d.multiplier or 1) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.balance = self.total_amount - self.total_payment
	self.product_qty = generate_product_qty(self.sale_products)

def verify_product(self):
	from ice_factory_management_system.inventory_management.doctype.product.product import get_product_accounts
	error = ""
	for a in self.sale_products:
		default = get_product_accounts(a.product_code,self.outlet)
		a.default_income_account = default.get("income_account") if (a.default_income_account or "") == "" else a.default_income_account
		a.default_receivable_account = default.get("receivable_account") if (a.default_receivable_account or "") == "" else a.default_receivable_account
		a.default_free_account = default.get("free_account") if (a.default_free_account or "") == "" else a.default_free_account

		p = frappe.db.get_value('Product', (a.get("product_code") or ""), ['allow_sum_qty'], as_dict=1)
		m = frappe.db.get_value("Unit",a.unit,["multiplier"],as_dict=1)
		a.allow_sum_qty = p.allow_sum_qty
		a.total_sale_quantity = (a.quantity or 0) -((a.free_quantity or 0) + (a.return_quantity or 0))
		a.total_amount = a.price * a.total_sale_quantity * m.multiplier
		a.sub_total = a.price * a.quantity * m.multiplier
		a.multiplier = m.multiplier

		if a.total_amount < 0 and (a.get("product_code") or"") != "":
			error += (_("<b>{0}</b> Product <b>{1}</b> total amount can not be small than zero").format((self.name if self.update_from  != "Sale" else ""),a.product_name))
		if error != "":
			frappe.throw(error)

def verify_sale_payment(self):
	payment = frappe.db.get_list("Sale Payment", filters={"sale": self.name,"docstatus":1}, fields=["total_amount"], as_list=False)
	if len(payment) > 0 and (self.update_from or "Sale")  == "Sale":
		frappe.throw(_("You can not change this sale because it has payments"))
		

def update_payment_status(self):
	if self.sale_status == "Deleted":
		self.status = self.sale_status
		return
	
	if self.balance == 0:
		self.status = "Paid"
	elif self.balance > 0 and self.balance < self.total_amount:
		self.status = "Partially Paid"
	else:
		self.status = "Unpaid"

def get_customer_product_price(self):
	base_product_prices = frappe.db.sql("select parent name,price,unit,multiplier from `tabProduct Units`",as_dict=1)
	customer_product_prices = frappe.db.sql("""SELECT product_code,price,unit,multiplier FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(self.customer),as_dict=1)
	customer_free_products = frappe.db.sql("""SELECT product_code,quantity,unit,multiplier FROM `tabCustomer Free Products` WHERE parent = '{}'""".format(self.customer),as_dict=1)

	if len(base_product_prices)>0:
		for a in base_product_prices:
			for b in self.sale_products:
				if (a.get("name") or "") == b.product_code:
					if (a.get("unit","") == b.unit):
						b.price = a["price"]
						b.total_amount = a["price"] * b.total_sale_quantity *  a.get("multiplier",1)
						b.multiplier = a.get("multiplier",1)
					else:
						p = frappe.get_cached_doc("Product",b.product_code)
						m = frappe.get_cached_doc("Unit",b.unit)
						b.price = p.price
						b.multiplier = m.multiplier
						b.total_amount = b.price * b.total_sale_quantity *  b.multiplier

	if len(customer_product_prices)>0:
		for a in customer_product_prices:
			for b in self.sale_products:
				if (a.get("product_code") or "") == b.product_code and (a.get("unit","") == b.unit):
					b.price = a.get("price")
					b.total_amount = a.get("price") *  b.total_sale_quantity *  a.get("multiplier",1)
					b.multiplier = a.get("multiplier",1)

	if len(customer_free_products)>0:
		for a in customer_free_products:
			for b in self.sale_products:
				if (a.get("product_code") or "") == b.product_code:
					b.free_quantity = (a.get("quantity") or 0) * (a.get("multiplier",1)/b.get("multiplier",1))
					b.total_sale_quantity = b.quantity - b.free_quantity
					b.total_amount = b.price * b.total_sale_quantity
					b.sub_total = b.price * b.quantity
	else:
		for a in self.sale_products:
			b.free_quantity = 0

def submit_to_GL_entry(self):
	import uuid
	self.id = str(uuid.uuid4().hex)
	from ice_factory_management_system.api.utils import submit_general_ledger_entry
	docs = []
	for acc in set([d.default_income_account for d in self.sale_products]):
		if not acc:
				frappe.throw(_("Please enter income account"))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":acc,
			"amount":sum([d.sub_total for d in self.sale_products if d.default_income_account == acc]),
			"against":self.customer + " - " + self.customer_name,
			"voucher_type":"Sale",
			"voucher_no":self.name,
			"type":"Income",
			"sale_id": self.id,
			"remark":"Sale To Customer {0} On {1} Total Amount {2}".format(self.customer_name,self.posting_date,frappe.format(sum([d.sub_total for d in self.sale_products if d.default_income_account == acc]),{"fieldtype":"Currency"})),
		}
		docs.append(doc)
	
	if sum([(d.free_quantity or 0) for d in self.sale_products]) > 0:
		for acc in set([d.default_free_account for d in self.sale_products]):
			if not acc:
					frappe.throw(_("Please enter income account"))
			doc = {
				"doctype":"GL Entry",
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":acc,
				"amount":sum([(d.free_quantity*d.multiplier*d.price) for d in self.sale_products if d.default_free_account == acc]),
				"against":self.customer + " - " + self.customer_name,
				"voucher_type":"Sale",
				"voucher_no":self.name,
				"type":"Income",
				"sale_id": self.id,
				"remark":"Free To Customer {0} On {1} Total Free {2}".format(self.customer_name,self.posting_date,frappe.format(sum([(d.free_quantity*d.price) for d in self.sale_products if d.default_free_account == acc]),{"fieldtype":"Currency"})),
			}
			docs.append(doc)
	
	if self.balance:
		if not self.default_receivable_account:
			frappe.throw(_('Please select default receivable account'))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":self.default_receivable_account,
			"amount":self.balance,
			"against_voucher_type":"Sale",
			"against_voucher_no": self.name,
			"voucher_type":"Sale",
			"voucher_no":self.name,
			"type":"Asset",
			"sale_id": self.id,
			"party_type": "Customer",
			"party":"{}-{}".format(self.customer,self.customer_name),
			"remark":"Sale To Customer {0} On {1} Total Amount {2}".format(self.customer_name,self.posting_date,frappe.format(self.total_amount,{"fieldtype":"Currency"})),
		}
		docs.append(doc)
	submit_general_ledger_entry(docs=docs)

@frappe.whitelist()
def generate_product_qty(sale_products):
	from collections import defaultdict
	if isinstance(sale_products, str):
		if sale_products != "":
			sale_products = json.loads(sale_products)
			group = defaultdict(lambda: {"total_sale_quantity": 0, "total_amount": 0})
			for item in sale_products:
				if (item.get("product_code") or "") != "":
					key = item.get("revenue_group")
					group[key]["total_sale_quantity"] += (item.get("total_sale_quantity") or 0)
					group[key]["total_amount"] += (item.get("total_amount") or 0)
			result = [{"revenue_group": key, "total_sale_quantity": val["total_sale_quantity"], "total_amount": val["total_amount"]}for key, val in group.items()]
			return json.dumps(result)
	else:
		if len(sale_products or []) > 0:
			group = defaultdict(lambda: {"total_sale_quantity": 0, "total_amount": 0})
			for item in sale_products:
				if (item.get("product_code") or "") != "":
					key = item.revenue_group
					group[key]["total_sale_quantity"] += item.total_sale_quantity
					group[key]["total_amount"] += item.total_amount
			result = [{"revenue_group": key, "total_sale_quantity": val["total_sale_quantity"], "total_amount": val["total_amount"]}for key, val in group.items()]
			return json.dumps(result)

@frappe.whitelist()
def get_sales(start_date="",end_date="",customer="",outlet=""):
	conditions = ""
	if start_date !="":
		conditions += " and posting_date >= '{}'".format(start_date)
	if end_date !="":
		conditions += " and posting_date <= '{}'".format(end_date)
	if customer != "":
		conditions += " and customer = '{}'".format(customer)
	if outlet != "":
		conditions += " and outlet = N'{}'".format(outlet)
	sql = """SELECT name sale,total_amount, balance FROM `tabSale` WHERE status <> 'Paid' {}""".format(conditions)

	sales = frappe.db.sql(sql, as_dict=1)
	return (sales or [])