# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class ChartofAccount(NestedSet):
	def autoname(self):
		self.name ="{}-{}".format((self.account_code).strip(),(self.account_name).strip() )
