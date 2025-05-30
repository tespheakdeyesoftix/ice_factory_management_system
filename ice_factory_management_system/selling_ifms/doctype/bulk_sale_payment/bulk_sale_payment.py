# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.selling_ifms.doctype.sale.sale import get_sales
from ice_factory_management_system.api.utils import get_previous_closed_date

class BulkSalePayment(Document):
	def validate(self):
		for a in self.sales:
			input_amount = a.input_amount/self.exchange_rate
			balance = a.amount - input_amount
			write_off_amount = a.write_off_amount/self.exchange_rate
			if input_amount >= a.amount and write_off_amount >= 0:
				a.input_amount = (a.amount * (self.exchange_rate or 1))
				a.write_off_amount = 0
			elif input_amount < a.amount and write_off_amount > balance:
				a.write_off_amount = balance*(self.exchange_rate or 1)
			else:
				pass
			a.payment_amount = (a.input_amount/self.exchange_rate) + (a.write_off_amount/self.exchange_rate)
			a.balance = a.amount - a.payment_amount
			a.exchange_rate = self.exchange_rate

		payment_amount = (sum((d.input_amount or 0) + (d.write_off_amount) for d in self.sales) or 0) 
		self.total_amount = (sum((d.amount or 0) for d in self.sales) or 0)
		self.total_payment_amount = (sum((d.payment_amount or 0) for d in self.sales) or 0)
		self.total_write_off_amount = (sum((d.write_off_amount or 0)/(self.exchange_rate or 0) for d in self.sales) or 0)
		self.total_balance = (sum((d.amount or 0)-(d.payment_amount or 0) for d in self.sales) or 0)
		self.total_invoices = len(self.sales)
		if payment_amount == 0 and self.payment_amount >0:
			update_allocated_amount(self)
		elif payment_amount == 0 and self.payment_amount == 0:
			frappe.throw("Please enter payment amount")
		elif payment_amount > 0 and self.payment_amount != payment_amount:
			self.payment_amount = payment_amount
		else:
			pass
		if self.total_amount == 0:
			frappe.throw("Please select one or more sale")
	
	def before_submit(self):
		keep = []
		remove = ""
		for a in self.sales:
			if a.payment_amount >0:
				keep.append(a)
			else:
				remove += a.sale + ", "
		self.sales.clear()
		self.sales = keep

		for a in self.sales:
			if a.payment_amount > 0:
				sale_payment = frappe.new_doc("Sale Payment")
				sale_payment.outlet = self.outlet
				sale_payment.payment_type = self.payment_type
				sale_payment.sale = a.sale
				sale_payment.input_amount = a.input_amount
				sale_payment.write_off_amount = a.write_off_amount
				sale_payment.total_amount = a.payment_amount
				sale_payment.exchange_rate = self.exchange_rate
				sale_payment.bulk_sale_payment = self.name
				sale_payment.submit()
				a.sale_payment = sale_payment.name
		if remove != "":
			frappe.msgprint("Sale " + remove + " has been removed from this payment")
	
	def before_cancel(self):
		from datetime import datetime,date
		get_previous_closed_date(self.posting_date,self.creation,self.outlet)
		for a in self.sales:
			sale_payment = frappe.get_doc("Sale Payment", a.sale_payment)
			if sale_payment.docstatus == 1:
				sale_payment.cancelled_from = "Bulk Sale Payment"
				sale_payment.cancel()

def update_allocated_amount(self):
	paid_amount = self.payment_amount/self.exchange_rate
	if(len(self.sales or []) > 0):
		for r in self.sales:
			if(paid_amount<r.amount):
				r.input_amount = paid_amount * self.exchange_rate
				r.payment_amount = paid_amount
			else:
				r.input_amount = r.amount * self.exchange_rate
				r.payment_amount = r.amount
			r.balance = r.amount - r.payment_amount
			paid_amount = paid_amount - r.payment_amount