# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet
import functools
import re

class AccountCode(NestedSet):
	def validate(self):
		if self.is_new():
			self.name = self.account_code + " - " + self.account_name + " - "+ ''.join(word[0].upper() for word in self.outlet.split() if word)

		# update root type
		if not self.root_type and self.parent_account_code:
			self.root_tye = frappe.db.get_value("Account Code",self.parent_account_code,"root_type")

@frappe.whitelist()
def get_children(doctype=None, parent=None, outlet=None, is_root=False):
	parent_fieldname = "parent_" + doctype.lower().replace(" ", "_")
	fields = ["name as value", "is_group as expandable"]
	filters = [["docstatus", "<", 2]]

	filters.append(['ifnull(`{0}`,"")'.format(parent_fieldname), "=", "" if is_root else parent])

	if is_root:
		filters.append(["outlet", "=", outlet])
	else:
		fields += [parent_fieldname + " as parent"]
	acc = frappe.get_list(doctype, fields=fields, filters=filters)
	sort_accounts(acc, is_root, key="value")
	return acc


def sort_accounts(accounts, is_root=False, key="name"):
	def compare_accounts(a, b):
		if re.split(r"\W+", a[key])[0].isdigit():
			# if chart of accounts is numbered, then sort by number
			return int(a[key] > b[key]) - int(a[key] < b[key])
		elif is_root:
			if a.report_type != b.report_type and a.report_type == "Balance Sheet":
				return -1
			if a.root_type != b.root_type and a.root_type == "Asset":
				return -1
			if a.root_type == "Liability" and b.root_type == "Equity":
				return -1
			if a.root_type == "Income" and b.root_type == "Expense":
				return -1
		else:
			# sort by key (number) or name
			return int(a[key] > b[key]) - int(a[key] < b[key])
		return 1

	accounts.sort(key=functools.cmp_to_key(compare_accounts))