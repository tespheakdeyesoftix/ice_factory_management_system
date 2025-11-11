# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AuditTrailLog(Document):
	def validate(self):
		self.username =frappe.get_cached_value("User",frappe.session.user,"full_name")
		self.posting_date = frappe.utils.now()

@frappe.whitelist(methods="POST")
def create_audit_trail_log(data):
	data["doctype"] = "Audit Trail Log"
	frappe.get_doc(data).insert(ignore_permissions=True)

			
