# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils.data import strip
import json
import frappe
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