# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.utils import submit_general_ledger_entry,cancel_general_ledger_entery

class JournalEntry(Document):
	def validate(self):
		verify_account(self)
	
	def on_submit(self):
		submit_to_GL_entry(self)
	
	def on_cancel(self):
		self.flags.ignore_links = 1
		cancel_general_ledger_entery(self.doctype,self.name)

def verify_account(self):
	if self.account_transfer_from == self.account_transfer_to:
		frappe.throw("Account transfer from and account transfer to cannot be the same.")
	if self.account_transfer_from == "":
		frappe.throw("Account transfer from cannot be empty.")
	if self.account_transfer_to == "":
		frappe.throw("Account transfer to cannot be empty.")
	if self.transfer_amount <= 0:
		frappe.throw("Amount must be greater than zero.")

def submit_to_GL_entry(self):
	docs = []
	doc = {
		"doctype":"GL Entry",
		"posting_date":self.posting_date,
		"account":self.account_transfer_to,
		"debit_amount":self.transfer_amount,
		"against":self.account_transfer_from,
		"voucher_type":"Journal Entry",
		"voucher_no":self.name,
		"remark": "Amount {} received from {} ".format(frappe.format((self.transfer_amount),{"fieldtype":"Currency"}), self.account_transfer_from),
	}
	docs.append(doc)
        
	doc = {
		"doctype":"GL Entry",
		"posting_date":self.posting_date,
		"account":self.account_transfer_from,
		"credit_amount":self.transfer_amount,
		"amount":self.transfer_amount,
		"against":self.account_transfer_to,
		"voucher_type":"Journal Entry",
		"voucher_no":self.name,
		"remark": "Amount {} transfer to {}".format(frappe.format(self.transfer_amount,{"fieldtype":"Currency"}),self.account_transfer_to),
	}
	docs.append(doc)
	submit_general_ledger_entry(docs=docs)