# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalePayment(Document):
	def validate(self):
		if self.balance == 0:
			frappe.throw("This sale has been fully paid.")
			
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
		self.payment_balance = (self.balance - self.payment_amount)/(self.exchange_rate or 1)

	def before_submit(self):
		update_sale_payment(self)
	
	def before_cancel(self):
		if (self.bulk_sale_payment or "") != "" and self.cancelled_from == "Sale Payment":
			frappe.throw("You cannot cancel this sale payment because it is part of a bulk sale payment.")
		update_sale_payment(self)
		

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