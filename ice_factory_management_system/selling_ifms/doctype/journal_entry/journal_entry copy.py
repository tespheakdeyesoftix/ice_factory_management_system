# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.utils import submit_general_ledger_entry,cancel_general_ledger_entery,get_previous_closed_date

class JournalEntry(Document):
	def validate(self):
		update_accounts(self)
		verify_account(self)
	
	def on_submit(self):
		submit_to_GL_entry(self)
	
	def before_cancel(self):
		get_previous_closed_date(self.posting_date,self.creation,self.outlet)
		
	def on_cancel(self):
		self.flags.ignore_links = 1
		cancel_general_ledger_entery(self.doctype,self.name)
	
@frappe.whitelist()
def get_accounts():
	data = frappe.get_doc("Business Information")
	return {
		"cash_transfer_account":data.cash_transfer_account
	}

def update_accounts(self):
	if self.transfer_type == "Cash" and (self.account_transfer_to or "") == "":
		self.account_transfer_to = get_accounts().cash_transfer_account
	if self.transfer_type == "Bank" and (self.bank or "") !="" and (self.account_transfer_to or "") == "":
		bank = (frappe.get_doc("Banks", self.bank).account or "")
		self.account_transfer_to = bank
	if self.payment_type != "" and (self.account_transfer_from or "") == "":
		bank = (frappe.get_doc("Payment Type", self.payment_type).account or "")
		self.account_transfer_from = bank

def verify_account(self):
	if self.account_transfer_from == self.account_transfer_to:
		frappe.throw("Account transfer from and account transfer to cannot be the same.")
	if self.account_transfer_from == "":
		frappe.throw("Account transfer from cannot be empty.")
	if self.account_transfer_to == "":
		frappe.throw("Account transfer to cannot be empty.")
	if self.total_amount <= 0:
		frappe.throw("Amount must be greater than zero.")

def submit_to_GL_entry(self):
	docs = []
	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.account_transfer_to,
		"debit_amount":self.total_amount,
		"against":self.account_transfer_from,
		"voucher_type":"Journal Entry",
		"voucher_no":self.name,
		"remark": "Amount {} received from {} ".format(frappe.format((self.total_amount),{"fieldtype":"Currency"}), self.account_transfer_from),
	}
	docs.append(doc)
        
	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.account_transfer_from,
		"credit_amount":self.total_amount,
		"amount":self.total_amount,
		"against":self.account_transfer_to,
		"voucher_type":"Journal Entry",
		"voucher_no":self.name,
		"remark": "Amount {} transfer to {}".format(frappe.format(self.total_amount,{"fieldtype":"Currency"}),self.account_transfer_to),
	}
	docs.append(doc)
	submit_general_ledger_entry(docs=docs)