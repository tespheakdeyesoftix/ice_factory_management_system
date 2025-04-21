# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils.data import strip

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