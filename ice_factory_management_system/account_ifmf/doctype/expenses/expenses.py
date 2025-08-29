# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class Expenses(Document):
	def validate(self):
		for d in self.expense_items:
			d.sub_total = (d.price or 0) * (d.quantity or 1)

		self.total_quantity = sum([d.quantity for d in self.expense_items]) 

	def before_submit(self):
		if not self.payable_account:
			# get default from global setting
			self.payable_account = frappe.get_cached_value("Business Information",None,"payable_account")
		


		# validate payment account
		if self.payments:
			for p in [d for d in self.payments if not d.account]:
				payment_type_doc = frappe.get_cached_doc("Payment Type",p.payment_type)
				if self.outlet:
					p.account = next((r.account for r in payment_type_doc.payment_type_accounts if r.outlet == self.outlet), "")

				if not p.account:
					p.account = payment_type_doc.account
					

	def on_submit(self):
		# validate account code
		if not self.payable_account:
			frappe.throw(_("Please select payable account"))
		submit_to_GL_entry(self)

def submit_to_GL_entry(self):
	from ice_factory_management_system.api.accounting import submit_general_ledger_entry
	docs = []

	for acc in set([d.account for d in self.expense_items]):
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":acc,
			"amount":sum([d.total_amount for d in self.expense_items if d.account == acc]),
			"voucher_type":"Expense",
			"voucher_no":self.name,
			"remark":"ចំណាយលើ {0} នៅថ្ងៃទី {1}។ សរុបទឹកប្រាក់ {2}".format(
				self.vendor + "-" + self.vendor_name ,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				frappe.format(sum([d.total_amount for d in self.expense_items if d.account == acc]),{"fieldtype":"Currency"})),
			"party_type":"Vendor",
			"party": self.vendor,
			"party_name": self.vendor_name,
		}
		docs.append(doc)

	# add payment account
	for acc in set([d.account for d in self.payments]):
		if not acc:
				frappe.throw(_("Please enter payment account code in payment list"))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":acc,
			"amount":sum([d.payment_amount for d in self.payments if d.account == acc]),
			"against":self.name,
			"voucher_type":"Purchase Order",
			"voucher_no":self.name,
			"remark":"ទូទាត់ទឹកប្រាក់បញ្ជាទិញអោយ {0}, នៅថ្ងៃទី {1}, ចំនួនទឹកប្រាក់​ {2}".format(
				self.vendor + "-" + self.vendor_name,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				frappe.format(sum([d.payment_amount for d in self.payments if d.account == acc]),{"fieldtype":"Currency"})
			),
			"party_type":"Vendor",
			"party": self.vendor,
			"vendor_name": self.vendor_name
		}
		docs.append(doc)
	
	
	if self.balance:
		if not self.payable_account:
			frappe.throw(_('Please select payable account'))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":self.payable_account,
			"amount":self.balance,
			"voucher_type":"Expenses",
			"voucher_no":self.name,
			"party_type": "Vendor",
			"party":self.vendor,
			"party_name":self.vendor_name,
			"remark":"ជំពាក់លើការចំណាយ {0} នៅថ្ងៃទី {1}, អ្នកផ្គត់ផ្គង់ {2}, ទឹកប្រាក់ជំពាក់ {2}".format(
				self.name,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				self.vendor + "-" + self.vendor_name ,
				frappe.format(self.balance,{"fieldtype":"Currency"})
			)
		}

		docs.append(doc)
	submit_general_ledger_entry(docs=docs)
