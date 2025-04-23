# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentType(Document):
	def on_update(self):
		if self.is_default == 1:
			frappe.db.sql("""UPDATE `tabPayment Type` SET is_default = 0 where name <> '{}'""".format(self.name), as_dict=1)
			frappe.db.commit()

			frappe.clear_document_cache('Payment Type', None)
			if self.is_default == 1:
				frappe.db.set_default("payment_type", self.name)