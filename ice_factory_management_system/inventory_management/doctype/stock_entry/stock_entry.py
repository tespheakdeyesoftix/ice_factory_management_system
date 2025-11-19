# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

from ice_factory_management_system.overrides.base_document import BaseDocument
from ice_factory_management_system.api.inventory import get_stock_location_prouct,add_inventory_transaction
class StockEntry(BaseDocument):
	def validate(self):
		super().validate()
		self.validate_stock_entry_products()
		self.validate_stock_entry()





	def validate_stock_entry_products(self):
		for d in self.stock_entry_products:
			# get product_cost

			slp = get_stock_location_prouct(d.product_code, d.default_stock_location or self.stock_location)
			if slp:
				d.cost = slp.cost
			d.total_cost = d.cost * d.quantity
			

	def validate_stock_entry(self):
		self.total_quantity = sum([d.quantity for d in self.stock_entry_products])
		self.total_cost = sum([d.total_cost for d in self.stock_entry_products])
	
	def on_submit(self):
		if not self.flags.ignore_submit_to_inventory:
			product_codes = [d for d in self.stock_entry_products if d.is_inventory_product ==1]
			data = [
			{
				"ref_doctype":self.doctype,
				"ref_docname":self.name,
				"posting_date":self.posting_date,
				"stock_location": p.default_stock_location or self.stock_location, #stock location index
				"product_code":p.product_code,
				"unit":p.unit,
				"quantity": p.quantity * self.multiplier,
				"is_calculate_cost":0,
			}
			for p in product_codes
			]
			add_inventory_transaction(data)
