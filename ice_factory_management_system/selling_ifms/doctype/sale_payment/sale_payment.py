# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.selling_ifms.doctype.sale.sale import update_sale_status
from ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate import get_exchange_rate

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

	def on_submit(self):
		update_sale_payment(self)
		update_sale_status(self.sale)

def update_sale_payment(self):
	sale = frappe.get_doc("Sale", self.sale)
	sale.total_payment += self.payment_amount
	sale.balance = sale.total_amount - sale.total_payment
	sale.total_write_off = self.write_off_amount/(self.exchange_rate or 1)
	sale.save()