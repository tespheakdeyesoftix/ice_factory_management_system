# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json
class Sale(Document):
	def validate(self):
		if not self.sale_products:
			frappe.throw(_("Please select product to your order"))

		for a in self.sale_products:
			a.total_sale_quantity = a.quantity - a.free_quantity
			a.total_amount = a.price * a.total_sale_quantity
		
		self.total_quantity = (sum((d.quantity or 0) for d in self.sale_products if a.allow_sum_qty == 1) or 0)
		self.total_free = (sum((d.free_quantity or 0) for d in self.sale_products if a.allow_sum_qty == 1) or 0)
		self.total_sale_quantity = (sum((d.total_sale_quantity or 0) for d in self.sale_products if a.allow_sum_qty == 1) or 0)

		self.total_amount = (sum((d.total_amount or 0) for d in self.sale_products if a.allow_sum_qty == 1) or 0)
		self.balance = self.total_amount - self.total_payment
            
	def before_insert(self):
		self.total_payment = 0
		self.balance = self.total_amount
		get_customer_product_price(self)
	
	def after_insert(self):
		update_sale_status(self.name)

	def on_update(self):
		if self.balance == 0:
			self.status = "Paid"
		elif (self.balance or 0) > 0 and (self.balance or 0) < (self.total_amount or o):
			self.status = "Partially Paid"
		else:
			self.status = "Unpaid"

@frappe.whitelist()
def update_sale_status(sale):
	doc = frappe.get_doc("Sale", sale)
	if doc.balance == 0:
		doc.status = "Paid"
	elif doc.balance > 0 and doc.balance < doc.total_amount:
		doc.status = "Partially Paid"
	else:
		doc.status = "Unpaid"
	doc.save()
	frappe.db.commit()

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
	return sales

def get_customer_product_price(self):
	base_product_price = frappe.db.get_list('Product',filters={'enabled': 1},fields=['name', 'price'],as_list=False)
	customer_product_price = frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(self.customer),as_dict=1)

	for a in base_product_price:
		for b in self.sale_products:
			if a["name"] == b.product_code:
				b.price = a["price"]
				b.total_amount = a["price"] * b.total_sale_quantity

	if len(customer_product_price)>0:
		for a in customer_product_price:
			for b in self.sale_products:
				if a["product_code"] == b.product_code:
					b.price = a["price"]
					b.total_amount = a["price"] *  b.total_sale_quantity