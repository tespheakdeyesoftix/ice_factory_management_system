# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.accounting import submit_general_ledger_entry

class BankTransfer(Document):
	def validate(self):
		if self.amount<=0:
			frappe.throw("Transfer amount cannot be zero")
		if self.from_account == self.to_account:
			frappe.throw("Transfer account cannot be the same")

	def on_submit(self):
		glEntry(self)
	
	def on_cancel(self):
		glEntry(self)

	@frappe.whitelist()
	def get_currency_exchange_rate(self):
		main_currency = frappe.get_doc("System Settings")
		exchange_rate = frappe.db.sql("select currency_exchange_rate from `tabExchange Rate` where from_currency = '{0}' and to_currency = '{1}' order by posting_date desc limit 1".format(main_currency.currency,self.currency),as_dict=1)
		if len(exchange_rate)>0:
			return exchange_rate[0]["currency_exchange_rate"]
		else:
			return 1

def glEntry(self):
	docs = []
	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.from_account,
		"voucher_type":"Bank Transfer",
		"voucher_no":self.name,
		"remark":"Bank Transfer To {0}".format(self.to_account)
	}
	root_type = frappe.get_cached_value("Chart of Account",self.from_account,"root_type")
	if root_type in ["Asset","Expenses"] and self.docstatus == 1:
		doc["credit_amount"] = self.amount
	else:
		doc["debit_amount"] = self.amount
	docs.append(doc)

	doc = {
		"doctype":"GL Entry",
		"outlet":self.outlet,
		"posting_date":self.posting_date,
		"account":self.to_account,
		"voucher_type":"Bank Transfer",
		"voucher_no":self.name,
		"remark":"Bank Transfer from {0}".format(self.from_account)
	}
	root_type = frappe.get_cached_value("Chart of Account",self.to_account,"root_type")
	if root_type in ["Asset","Expenses"] and self.docstatus == 1:
		doc["debit_amount"] = self.amount
	else:
		doc["credit_amount"] = self.amount
	docs.append(doc)
	submit_general_ledger_entry(docs)
	if self.docstatus == 2:
		frappe.db.sql("update `tabGL Entry` set is_cancelled = 1 where voucher_type = 'Bank Transfer' and voucher_no='{}'".format(self.name))