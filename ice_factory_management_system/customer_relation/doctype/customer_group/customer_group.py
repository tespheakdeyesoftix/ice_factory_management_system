# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CustomerGroup(Document):
	def validate(self):
		if (self.customer_group_kh or "") == "":
			self.customer_group_kh = self.customer_group_en
