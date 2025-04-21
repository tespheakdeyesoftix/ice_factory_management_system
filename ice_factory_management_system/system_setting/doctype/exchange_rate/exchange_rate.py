# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExchangeRate(Document):
	pass

@frappe.whitelist()
def get_exchange_rate(currency):
	main_currency = frappe.get_single("Business Information").currency
	"""Get the exchange rate from the Exchange Rate doctype."""
	sql = "select currency_exchange_rate from `tabExchange Rate` where from_currency = '{0}' and to_currency = '{1}'".format(main_currency, currency)
	data = frappe.db.sql(sql, as_dict=True)
	if data:
		return data[0].currency_exchange_rate
	else:
		return 1