# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PaymentTypeGroup(Document):
	def validate(self):
		if (self.payment_type_group_kh or "") == "":
			self.payment_type_group_kh = self.payment_type_group_en
