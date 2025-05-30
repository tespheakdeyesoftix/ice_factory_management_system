# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class AccountCode(NestedSet):
	def validate(self):
		if self.is_new():
			self.name = self.account_code + " - " + self.account_name

		# update root type
		if not self.root_type and self.parent_account_code:
			self.root_tye = frappe.db.get_value("Account Code",self.parent_account_code,"root_type")