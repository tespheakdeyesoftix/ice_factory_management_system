# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AuditTrailLog(Document):
	def validate(self):
		if not self.username:
			self.username = frappe.session.user
