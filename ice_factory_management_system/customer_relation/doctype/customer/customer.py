# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Customer(Document):
	def validate(self):
		if (self.customer_name_kh or "") == "":
			self.customer_name_kh = self.customer_name

@frappe.whitelist()
def get_customer_product_price(customer, products=[],product_code=""):
	frappe.throw(str(products))
	if len(products) > 0:
		products = json.loads(products)
		base_product_price = frappe.db.get_list('Product',filters={'enabled': 1},fields=['name', 'price'],as_list=False)
		customer_product_price = frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(customer),as_dict=1)
		
		for a in base_product_price:
			for b in products:
				if a["name"] == b["product_code"]:
					b["price"] = a["price"]
					b["total_amount"] = a["price"] * b["total_sale_quantity"]
					b["__unsaved"] = 1
					b["__islocal"] = 1

		if len(customer_product_price)>0:
			for a in customer_product_price:
				for b in products:
					if a["product_code"] == b["product_code"]:
						b["price"] = a["price"]
						b["total_amount"] = a["price"] * b["total_sale_quantity"]
						b["__unsaved"] = 1
						b["__islocal"] = 1
		return products
	else:
		if product_code:
			base_product_price = frappe.get_doc("Product", product_code)
			customer_product_price = frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{0}' and product_code = '{1}'""".format(customer,product_code),as_dict=1)
			if len(customer_product_price)>0:
				return customer_product_price[0]["price"]
			else:
				return base_product_price.price