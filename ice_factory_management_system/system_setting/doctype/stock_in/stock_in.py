# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.utils import get_previous_closed_date


class StockIn(Document):
	def validate(self):
		get_previous_closed_date(self.posting_date,self.creation,self.outlet)		
		default = frappe.get_doc("Business Information")
		self.default_credit_account = default.credit_account if (self.default_credit_account or "") == "" else self.default_credit_account
		self.default_inventory_account = default.inventory_account if (self.default_inventory_account or "") == "" else self.default_inventory_account

	def on_submit(self):
		submit_to_GL_entry(self)
		self.total_amount = self.total_product_amount if self.total_product_amount > 0 else self.total_amount
	
	def before_cancel(self):
		get_previous_closed_date(self.posting_date,self.creation,self.outlet)		

def submit_to_GL_entry(self):
	from ice_factory_management_system.api.utils import submit_general_ledger_entry
	docs = []
	if not self.default_inventory_account:
			frappe.throw(_("Please select inventory account"))
	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.default_inventory_account,
		"amount":(self.total_amount + self.total_product_amount),
		"against":self.vendor + " - " + self.vendor_name,
		"voucher_type":"Stock In",
		"voucher_no":self.name,
		"remark":"",
	}
	docs.append(doc)
	
	if not self.default_credit_account:
		frappe.throw(_('Please select credit account'))
	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.default_credit_account,
		"amount":(self.total_amount+self.total_product_amount),
		"against_voucher_type":"Stock In",
		"against_voucher_no": self.name,
		"voucher_type":"Stock In",
		"voucher_no":self.name,
		"party_type": "vendor",
		"party":"{}-{}".format(self.vendor,self.vendor_name),
		"remark":""
	}
	docs.append(doc)
	submit_general_ledger_entry(docs=docs)