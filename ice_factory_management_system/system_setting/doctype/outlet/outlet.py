# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Outlet(Document):
	def validate(self):
		if (self.outlet_name_kh or "") == "":
			self.outlet_name_kh = self.outlet_name_en

@frappe.whitelist()
def get_default_accounts(outlet=""):
	cash_account = ""
	bank_account = ""
	income_account = ""
	free_account = ""
	cash_transfer_account = ""
	receivable_account = ""
	credit_account = ""
	write_off_account = ""
	inventory_account = ""
	if outlet:
		outlet_default = frappe.get_doc("Outlet", outlet)
		cash_account = outlet_default.cash_account
		bank_account = outlet_default.bank_account
		income_account = outlet_default.income_account
		free_account = outlet_default.free_account
		cash_transfer_account = outlet_default.cash_transfer_account
		receivable_account = outlet_default.receivable_account
		credit_account = outlet_default.credit_account
		write_off_account = outlet_default.write_off_account
		inventory_account = outlet_default.inventory_account
	
	business_default = frappe.get_doc("Business Information")
	cash_account = business_default.cash_account if (cash_account or "") == "" else cash_account
	bank_account = business_default.bank_account if (bank_account or "") == "" else bank_account
	income_account = business_default.income_account if (income_account or "") == "" else income_account
	free_account = business_default.free_account if (free_account or "") == "" else free_account
	cash_transfer_account = business_default.cash_transfer_account if (cash_transfer_account or "") == "" else cash_transfer_account
	receivable_account = business_default.receivable_account if (receivable_account or "") == "" else receivable_account
	credit_account = business_default.credit_account if (credit_account or "") == "" else credit_account
	write_off_account = business_default.write_off_account if (write_off_account or "") == "" else write_off_account
	inventory_account = business_default.inventory_account if (inventory_account or "") == "" else inventory_account
	return {
		"cash_account":cash_account,""
		"bank_account":bank_account,
		"income_account":income_account,
		"free_account":free_account,
		"cash_transfer_account":cash_transfer_account,
		"receivable_account":receivable_account,
		"credit_account":credit_account,
		"write_off_account":write_off_account,
		"inventory_account":inventory_account
		}
	