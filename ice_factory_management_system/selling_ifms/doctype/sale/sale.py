# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json
class Sale(Document):
	def validate(self):
		verify_account(self)
		verify_product(self)
		update_total_amounts(self)
		verify_sale_payment(self)
		update_sale_status(self)
		if self.sale_status == "Closed" and self.update_from  == "Sale":
			submit_to_GL_entry(self)
		self.update_from = "Sale"
            
	def before_insert(self):
		self.total_payment = 0
		self.total_write_off = 0
		self.balance = self.total_amount	
		get_customer_product_price(self)	

def verify_account(self):
	default = frappe.get_doc("Business Information")
	self.default_income_account = default.income_account if (self.default_income_account or "") == "" else self.default_income_account
	self.default_receivable_account = default.receivable_account if (self.default_receivable_account or "") == "" else self.default_receivable_account
	self.default_free_account = default.free_account if (self.default_free_account or "") == "" else self.default_free_account
	

def update_total_amounts(self):
	self.total_quantity = (sum((d.quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.total_free = (sum((d.free_quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.total_sale_quantity = (sum((d.quantity or 0)-(d.free_quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)

	self.total_amount = (sum((d.price or 0)*(d.total_sale_quantity or 0) for d in self.sale_products if d.allow_sum_qty == 1) or 0)
	self.balance = self.total_amount - self.total_payment
	self.product_qty = generate_product_qty(self.sale_products)

def verify_product(self):
	error = ""
	for a in self.sale_products:
		p = frappe.db.get_value('Product', (a.get("product_code") or ""), ['allow_sum_qty'], as_dict=1)
		a.allow_sum_qty = p.allow_sum_qty
		a.total_sale_quantity = (a.quantity or 0) -((a.free_quantity or 0) + (a.return_quantity or 0))
		a.total_amount = a.price * a.total_sale_quantity
		a.sub_total = a.price * a.quantity
		a.default_income_account = self.default_income_account if (a.default_income_account or "") == "" else a.default_income_account
		a.default_receivable_account = self.default_receivable_account if (a.default_receivable_account or "") == "" else a.default_receivable_account
		a.default_free_account = self.default_free_account if (a.default_free_account or "") == "" else a.default_free_account
		if a.total_amount < 0 and (a.get("product_code") or"") != "":
			error += (_("<b>{0}</b> Product <b>{1}</b> total amount can not be small than zero").format((self.name if self.update_from  != "Sale" else ""),a.product_name))
		if error != "":
			frappe.throw(error)

def verify_sale_payment(self):
	payment = frappe.db.get_list("Sale Payment", filters={"sale": self.name,"docstatus":1}, fields=["payment_amount"], as_list=False)
	if len(payment) > 0 and (self.update_from or "Sale")  == "Sale":
		frappe.throw(_("You can not change this sale because it has payments"))
		

def update_sale_status(self):
	if self.balance == 0:
		self.status = "Paid"
	elif self.balance > 0 and self.balance < self.total_amount:
		self.status = "Partially Paid"
	else:
		self.status = "Unpaid"

def get_customer_product_price(self):
	base_product_prices = frappe.db.get_list('Product',filters={'enabled': 1},fields=['name', 'price'],as_list=0)
	customer_product_prices = frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(self.customer),as_dict=1)
	customer_free_products = frappe.db.sql("""SELECT product_code,quantity FROM `tabCustomer Free Products` WHERE parent = '{}'""".format(self.customer),as_dict=1)

	if len(base_product_prices)>0:
		for a in base_product_prices:
			for b in self.sale_products:
				if a.get("name") == b.product_code:
					b.price = a["price"]
					b.total_amount = a["price"] * b.total_sale_quantity

	if len(customer_product_prices)>0:
		for a in customer_product_prices:
			for b in self.sale_products:
				if (a.get("product_code") or "") == b.product_code:
					b.price = a.get("price")
					b.total_amount = a.get("price") *  b.total_sale_quantity

	if len(customer_free_products)>0:
		for a in customer_free_products:
			for b in self.sale_products:
				if (a.get("product_code") or "") == b.product_code:
					b.free_quantity = (a.get("quantity") or 0)
					b.total_sale_quantity = b.quantity - b.free_quantity
					b.total_amount = b.price * b.total_sale_quantity
					b.sub_total = b.price * b.quantity
	else:
		for a in self.sale_products:
			b.free_quantity = 0

def submit_to_GL_entry(self):
	from ice_factory_management_system.api.utils import submit_general_ledger_entry
	docs = []
	for acc in set([d.default_income_account for d in self.sale_products]):
		if not acc:
				frappe.throw(_("Please enter income account"))
		doc = {
			"doctype":"GL Entry",
			"posting_date":self.sale_date,
			"account":acc,
			"amount":sum([d.sub_total for d in self.sale_products if d.default_income_account == acc]),
			"against":self.customer + " - " + self.customer_name,
			"voucher_type":"Sale",
			"voucher_no":self.name,
			"type":"Income",
			"remark":"Sale To Customer {0} On {1} Total Amount {2}".format(self.customer_name,self.sale_date,frappe.format(sum([d.sub_total for d in self.sale_products if d.default_income_account == acc]),{"fieldtype":"Currency"})),
		}
		docs.append(doc)
	
	if sum([(d.free_quantity or 0) for d in self.sale_products]) > 0:
		for acc in set([d.default_free_account for d in self.sale_products]):
			if not acc:
					frappe.throw(_("Please enter income account"))
			doc = {
				"doctype":"GL Entry",
				"posting_date":self.sale_date,
				"account":acc,
				"amount":sum([(d.free_quantity*d.price) for d in self.sale_products if d.default_free_account == acc]),
				"against":self.customer + " - " + self.customer_name,
				"voucher_type":"Sale",
				"voucher_no":self.name,
				"type":"Income",
				"remark":"Free To Customer {0} On {1} Total Free {2}".format(self.customer_name,self.sale_date,frappe.format(sum([(d.free_quantity*d.price) for d in self.sale_products if d.default_free_account == acc]),{"fieldtype":"Currency"})),
			}
			docs.append(doc)
	
	if self.balance:
		if not self.default_receivable_account:
			frappe.throw(_('Please select default receivable account'))
		doc = {
			"doctype":"GL Entry",
			"posting_date":self.sale_date,
			"account":self.default_receivable_account,
			"amount":self.balance,
			"against_voucher_type":"Sale",
			"against_voucher_no": self.name,
			"voucher_type":"Sale",
			"voucher_no":self.name,
			"type":"Asset",
			"party_type": "Customer",
			"party":"{}-{}".format(self.customer,self.customer_name),
			"remark":"Sale To Customer {0} On {1} Total Amount {2}".format(self.customer_name,self.sale_date,frappe.format(self.total_amount,{"fieldtype":"Currency"})),
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
		conditions += " and sale_date >= '{}'".format(start_date)
	if end_date !="":
		conditions += " and sale_date <= '{}'".format(end_date)
	if customer != "":
		conditions += " and customer = '{}'".format(customer)
	if outlet != "":
		conditions += " and outlet = N'{}'".format(outlet)
	sql = """SELECT name sale,total_amount, balance FROM `tabSale` WHERE status <> 'Paid' {}""".format(conditions)

	sales = frappe.db.sql(sql, as_dict=1)
	return (sales or [])