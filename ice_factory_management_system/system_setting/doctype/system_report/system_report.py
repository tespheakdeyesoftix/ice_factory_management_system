# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SystemReport(Document):
	def validate(self):
		query_permission(frappe.session.user)

@frappe.whitelist()
def query_permission(user):
	
	# frappe.get_roles()
	report_names = frappe.db.sql("""
	select 
		name from 
	`tabSystem Report`
	where 
	 	name not in (select distinct parent from `tabHas Role` where parenttype ='System Report') 
		or name in (
			select distinct parent from `tabHas Role` 
			where 
				parenttype ='System Report' and 
				role in %(role)s
	)
	 """,{
		"role":frappe.get_roles()
	 },as_dict =1)

	report_names = [d.get("name") for d in report_names]
	report_names = ", ".join(
		frappe.db.escape(r) for r in report_names
		)
	return f"`tabSystem Report`.name IN ({report_names})"
	 