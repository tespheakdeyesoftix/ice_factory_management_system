# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.utils import get_currency_symbol,submit_general_ledger_entry,cancel_general_ledger_entery
class SalePayment(Document):
	def validate(self):
		if self.balance == 0:
			frappe.throw("This sale has been fully paid.")
		verify_account(self)
		update_totals(self)
		
	def before_submit(self):
		update_sale_payment(self)
	
	def before_cancel(self):
		if (self.bulk_sale_payment or "") != "" and self.cancelled_from == "Sale Payment":
			frappe.throw("You cannot cancel this sale payment because it is part of a bulk sale payment.")
		update_sale_payment(self)
	
	def on_submit(self):
		submit_to_GL_entry(self)

	def on_cancel(self):
		self.flags.ignore_links = True
		cancel_general_ledger_entery(self.doctype,self.name)

def update_totals(self):
	if self.input_amount <= 0:
		frappe.throw("Please enter a valid payment amount.")
	input_amount = self.input_amount/self.exchange_rate
	balance = self.balance - input_amount
	write_off_amount = self.write_off_amount/self.exchange_rate
	if input_amount >= self.balance and write_off_amount >= 0:
		self.input_amount = (self.balance * (self.exchange_rate or 1))
		self.write_off_amount = 0
	elif input_amount < self.balance and write_off_amount > balance:
		self.write_off_amount = balance*(self.exchange_rate or 1)
	else:
		pass
	self.payment_amount = (self.input_amount/self.exchange_rate) + (self.write_off_amount/self.exchange_rate)
	self.payment_balance = get_currency_symbol(self.currency) + " " +  "{:,}".format(((self.balance - self.payment_amount)*(self.exchange_rate or 1)))

def verify_account(self):
	if self.account_paid_from == self.account_paid_to:
		frappe.throw("Account paid from and account paid to cannot be the same.")
	default = frappe.get_doc("Business Information")
	self.account_paid_from = default.receivable_account if (self.account_paid_from or "") == "" else self.account_paid_from
	self.account_paid_to = default.cash_account if (self.account_paid_to or "") == "" else self.account_paid_to
	self.write_off_account = default.write_off_account if (self.write_off_account or "") == "" else self.write_off_account

def update_sale_payment(self):
	if self.docstatus == 1:
		sale = frappe.get_doc("Sale", self.sale)
		sale.total_payment += self.payment_amount
		sale.balance = sale.total_amount - sale.total_payment
		sale.total_write_off = self.write_off_amount/(self.exchange_rate or 1)
		sale.update_from = "Sale Payment"
		sale.save()
	else:
		sale = frappe.get_doc("Sale", self.sale)
		sale.total_payment -= self.payment_amount
		sale.balance = sale.total_amount - sale.total_payment
		sale.total_write_off = sale.total_write_off - (self.write_off_amount/(self.exchange_rate or 1))
		sale.update_from = "Sale Payment"
		sale.save()

def submit_to_GL_entry(self):
	docs = []
	doc = {
		"doctype":"GL Entry",
		"posting_date":self.posting_date,
		"account":self.account_paid_to,
		"debit_amount":self.input_amount/self.exchange_rate,
		"against":self.customer + " - " + self.customer_name,
		"voucher_type":"Sale Payment",
		"voucher_no":self.name,
		"remark": "Amount {} received from {} pay for {}".format(frappe.format((self.input_amount/self.exchange_rate),{"fieldtype":"Currency"}), (self.customer + " - " + self.customer_name),self.sale),
	}
	docs.append(doc)
	
	if self.write_off_amount > 0:
		doc = {
			"doctype":"GL Entry",
			"posting_date":self.posting_date,
			"account":self.write_off_account,
			"debit_amount":self.write_off_amount/self.exchange_rate,
			"against":self.customer + " - " + self.customer_name,
			"voucher_type":"Sale Payment",
			"voucher_no":self.name,
			"remark": "Write Off Amount {} from {}".format(frappe.format((self.write_off_amount/self.exchange_rate),{"fieldtype":"Currency"}), (self.sale)),
		}
		docs.append(doc)
        
	doc = {
		"doctype":"GL Entry",
		"posting_date":self.posting_date,
		"account":self.account_paid_from,
		"credit_amount":self.payment_amount,
		"party_type":"Customer",
		"party":self.customer,
		"amount":self.payment_amount,
		"against":self.account_paid_to,
		"against_voucher_type":"Sale",
		"against_voucher_no":self.sale,
		"voucher_type":"Sale Payment",
		"voucher_no":self.name,
		"remark": "Amount {} received from {} pay for {}".format(frappe.format(self.payment_amount,{"fieldtype":"Currency"}), (self.customer + " - " + self.customer_name),self.sale),
	}
	docs.append(doc)

	submit_general_ledger_entry(docs=docs)