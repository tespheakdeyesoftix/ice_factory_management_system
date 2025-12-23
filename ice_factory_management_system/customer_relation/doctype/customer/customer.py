# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Customer(Document):
	def validate(self):
		if (self.customer_name_kh or "") == "":
			self.customer_name_kh = self.customer_name
		self.customer_code_name = f"{self.name} - {self.customer_name}"

@frappe.whitelist()
def get_customer_product_price(customer="", products=[],product_code="",unit=""):
	if len(products) > 0:
		products = json.loads(products)
		base_product_prices = frappe.db.sql("select parent name,price,unit,multiplier from `tabProduct Units`",as_dict=1)
		customer_product_prices = frappe.db.sql("""SELECT product_code,price,unit,multiplier FROM `tabCustomer Product Price` WHERE parent = '{}'""".format(customer),as_dict=1)
		customer_free_products = frappe.db.sql("""SELECT product_code,quantity,unit,multiplier FROM `tabCustomer Free Products` WHERE parent = '{}'""".format(customer),as_dict=1)

		if len(base_product_prices)>0:
			for a in base_product_prices:
				for b in products:
					if (a.get("name") or "") != "" and ((a.get("name") or "") == b.get("product_code","")):
						if (a.get("unit","") == b.get("unit","")):
							b["price"] = a["price"]
							b["total_amount"] = b["price"] * b["total_sale_quantity"] * (a["multiplier"] or 1)
							b["multiplier"] = (a["multiplier"] or 1)
							b["sub_total"] = b["price"] * b["quantity"] * (a["multiplier"] or 1)
							b["__unsaved"] = 1
							b["__islocal"] = 1
						else:
							p = frappe.get_cached_doc("Product",b.get("product_code",""))
							m = frappe.get_cached_doc("Unit",b["unit"])
							b["price"] = p.price
							b["total_amount"] = b["price"] * b["total_sale_quantity"] *  (m.multiplier or 1)
							b["multiplier"] = (m.multiplier or 1)
							b["sub_total"] = b["price"] * b["quantity"] * (a["multiplier"] or 1)
							b["__unsaved"] = 1
							b["__islocal"] = 1
					

		if len(customer_product_prices)>0:
			for a in customer_product_prices:
				for b in products:
					if (a.get("product_code") or "") != "" and ((a.get("product_code") or "") == b.get("product_code","")) and (a.get("unit","") == b.get("unit","")):
						b["price"] = a["price"]
						b["total_amount"] = a["price"] * b["total_sale_quantity"]  * (a["multiplier"] or 1)
						b["multiplier"] = (a["multiplier"] or 1)
						b["sub_total"] = b["price"] * b["quantity"] * (a["multiplier"] or 1)
						b["__unsaved"] = 1
						b["__islocal"] = 1

		if len(customer_free_products)>0:
			for a in customer_free_products:
				for b in products:
					if (a.get("product_code") or "") != "" and (a.get("product_code") or "") == b.get("product_code",""):
						b["free_quantity"] = a["quantity"] * ((a["multiplier"] or 1) / (b["multiplier"] or 1))
						b["total_sale_quantity"] = b["quantity"] - (b["free_quantity"] * ((a["multiplier"] or 1) / (b["multiplier"] or 1)))
						b["total_amount"] = b["price"] * b["total_sale_quantity"]
						b["sub_total"] = b["price"] * b["quantity"]
		else:
			for a in products:
				a["free_quantity"] = 0
		return products
	else:
		multiplier = frappe.get_cached_doc("Unit",unit).multiplier
		if product_code:
			base_product_price = (frappe.db.sql("select parent name,price,unit,multiplier from `tabProduct Units` where parent = '{0}' and unit='{1}'".format(product_code,unit),as_dict=1) or [])
			if len(base_product_price) == 0:
				base_product_price = (frappe.db.sql("select parent name,price,unit,multiplier from `tabProduct Units` where parent = '{0}'".format(product_code),as_dict=1) or [])
			customer_product_prices = (frappe.db.sql("""SELECT product_code,price,multiplier FROM `tabCustomer Product Price` WHERE parent = '{0}' and product_code = '{1}' and unit = '{2}'""".format(customer,product_code,unit),as_dict=1) or [])
			customer_free_products = (frappe.db.sql("""SELECT product_code,quantity,unit,multiplier FROM `tabCustomer Free Products` WHERE parent = '{0}' and product_code = '{1}'""".format(customer,product_code),as_dict=1) or [])
			free_quantity = 0
			if len(customer_free_products)>0:
				free_multiplier = customer_free_products[0]["multiplier"] / multiplier
				free_quantity = (customer_free_products[0]["quantity"] or 0) * free_multiplier
			if len(customer_product_prices)>0:
				return {"price":customer_product_prices[0]["price"],"multiplier":multiplier,"free_quantity":free_quantity}
			else:
				return {"price":base_product_price[0]["price"],"multiplier":multiplier,"free_quantity":free_quantity}


@frappe.whitelist()
def get_events(start, end, filters=None):
    events = frappe.get_all(
        "Sale",
        fields=[
            "name",
            "name as subject",
            "posting_date as start",
            "posting_date as end"
        ],
        filters={
            "posting_date": ["between", [frappe.utils.getdate(start), frappe.utils.getdate(end)]]
        }
    )
    frappe.msgprint(str(events))
    return events