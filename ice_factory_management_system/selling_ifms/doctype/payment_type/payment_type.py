# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentType(Document):
	def validate(self):
		#update exchage rate
		#1 check if current = main current set exchange rate 1
		main_currency = frappe.get_cached_value("System Settings",None,"currency")

		if self.currency == main_currency:
			self.exchange_rate = 1
		else:
			sql = "select currency_exchange_rate from `tabExchange Rate` where from_currency = %(main_currency)s and to_currency = %(to_currency)s order by creation desc limit 1"
			data = frappe.db.sql(sql,{"main_currency":main_currency, "to_currency":self.currency},as_dict = 1)
		 
			if data:
				self.exchange_rate = data[0].get("currency_exchange_rate")
			else:
				frappe.throw("There is no exchange rate from {} to {}".format(main_currency,self.currency))
	def on_update(self):
	 
		if self.is_default == 1:
			frappe.db.sql("""UPDATE `tabPayment Type` SET is_default = 0 where name <> '{}'""".format(self.name), as_dict=1)
			frappe.db.commit()

			frappe.clear_document_cache('Payment Type', None)
			if self.is_default == 1:
				frappe.db.set_default("payment_type", self.name)