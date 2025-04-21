# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Outlet(Document):
	def validate(self):
		if (self.outlet_name_kh or "") == "":
			self.outlet_name_kh = self.outlet_name_en