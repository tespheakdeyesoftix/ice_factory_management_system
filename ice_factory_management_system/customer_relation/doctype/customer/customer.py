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
def get_customer_product_price(customer="", products=[],product_code=""):
	if len(products) > 0:
		products = json.loads(products)
		base_product_prices = frappe.db.get_list('Product',filters={'enabled': 1},fields=['name', 'price'],as_list=False)
		customer_product_prices = frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(customer),as_dict=1)
		customer_free_products = frappe.db.sql("""SELECT product_code,quantity FROM `tabCustomer Free Products` WHERE parent = '{}'""".format(customer),as_dict=1)

		if len(base_product_prices)>0:
			for a in base_product_prices:
				for b in products:
					if (a.get("name") or "") != "" and (a.get("name") or "") == b.get("product_code",""):
						b["price"] = a["price"]
						b["total_amount"] = a["price"] * b["total_sale_quantity"]
						b["__unsaved"] = 1
						b["__islocal"] = 1

		if len(customer_product_prices)>0:
			for a in customer_product_prices:
				for b in products:
					if (a.get("product_code") or "") != "" and (a.get("product_code") or "") == b.get("product_code",""):
						b["price"] = a["price"]
						b["total_amount"] = a["price"] * b["total_sale_quantity"]
						b["__unsaved"] = 1
						b["__islocal"] = 1

		if len(customer_free_products)>0:
			for a in customer_free_products:
				for b in products:
					if (a.get("product_code") or "") != "" and (a.get("product_code") or "") == b.get("product_code",""):
						b["free_quantity"] = a["quantity"]
						b["total_sale_quantity"] = b["quantity"] - b["free_quantity"]
						b["total_amount"] = b["price"] * b["total_sale_quantity"]
						b["sub_total"] = b["price"] * b["quantity"]
		else:
			for a in products:
				a["free_quantity"] = 0
				
		return products
	else:
		if product_code:
			base_product_price = frappe.get_doc("Product", product_code)
			customer_product_prices = (frappe.db.sql("""SELECT product_code,price FROM `tabCustomer Product Price` WHERE parent = '{0}' and product_code = '{1}'""".format(customer,product_code),as_dict=1) or [])
			customer_free_products = (frappe.db.get_list('Customer Free Products',filters={'parent': customer,'product_code':product_code},fields=['product_code','quantity'],as_list=False) or [])
			free_quantity = 0
			if len(customer_free_products)>0:
				free_quantity = customer_free_products[0]["quantity"] or 0
			if len(customer_product_prices)>0:
				return {"price":customer_product_prices[0]["price"],"free_quantity":free_quantity}
			else:
				return {"price":base_product_price.price,"free_quantity":free_quantity}