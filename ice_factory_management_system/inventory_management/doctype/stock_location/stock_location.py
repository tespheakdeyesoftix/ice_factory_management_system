# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockLocation(Document):
	def validate(self):
		if (self.stock_location_name_kh or "") == "":
			self.stock_location_name_kh = self.stock_location_name_en
