# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet


class ProductCategory(NestedSet):
	def validate(self):
		if (self.category_name_kh or "") == "":
			self.category_name_kh = self.category_name_en
