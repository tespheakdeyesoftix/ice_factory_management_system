# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils.data import strip
import json
import frappe
from frappe import _ 
class Product(Document):
	def validate(self):
		if (self.product_name_kh or "") == "":
			self.product_name_kh = self.product_name

	def autoname(self):
		from frappe.model.naming import set_name_by_naming_series
		if strip(self.naming_series) !="" and strip(self.product_code) =="":
			set_name_by_naming_series(self)
			self.product_code = self.name		
		self.product_code = strip(self.product_code)
		self.name = self.product_code
	
	def on_update(self):
		product_outlets = []
		for a in self.product_outlet:
			product_outlets.append({"outlet":a.outlet})
		self.product_outlets = json.dumps(product_outlets)
		update_product_unit(self)

	@frappe.whitelist()
	def get_stats(self):
		
		sql="select stock_location as label, quantity as value  from `tabStock Location Products` where product_code=%(product_code)s"
		data = frappe.db.sql(sql,{"product_code":self.name},as_dict = 1)
		
		if data:
			data.append({
				"label":_("Total"),
				"value": sum([d.get("value") for d in data])
				 
			})
		# format number
		for d in data:
			d["value"] = frappe.format(d.get("value"),{"fieldtype":"Float"})


		data.append({
			"label":_("Stock Value"),
			"value":frappe.format(265900,{"fieldtype":"Currency"}),
			
		})
			
		return data
	
def update_product_unit(self):
	if len(self.product_units or [])>0:
		if self.has_value_changed("price") or self.has_value_changed("unit"):
			for a in self.product_units:
				if a.base_product_unit == 1:
					a.price = self.price
					a.unit = self.unit
					a.multiplier = 1
	else:
		self.append("product_units", {
                "unit":self.unit,
                "multiplier": self.multiplier,
                "price": self.price,
				"base_product_unit": 1
            })

@frappe.whitelist()
def get_product_accounts(product_code="",outlet=""):
	income_account = ""
	free_account = ""
	receivable_account = ""
	product_defaults = frappe.get_doc("Product", product_code)
	product_default = [a for a in product_defaults.product_accounts if a.outlet == outlet]
	if len(product_default) > 0:
		income_account = product_default[0].income_account
		free_account = product_default[0].free_account

	if outlet:
		outlet_default = frappe.get_doc("Outlet", outlet)
		income_account = outlet_default.income_account if (income_account or "") == "" else income_account
		free_account = outlet_default.free_account if (free_account or "") == "" else free_account

	business_default = frappe.get_doc("Business Information")
	income_account = business_default.income_account if (income_account or "") == "" else income_account
	free_account = business_default.free_account if (free_account or "") == "" else free_account

	receivable_account = business_default.receivable_account if (receivable_account or "") == "" else receivable_account

	return {"income_account":income_account,"free_account":free_account,"receivable_account":receivable_account}