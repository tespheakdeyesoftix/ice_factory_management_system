# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.inventory import get_stock_location_prouct
from frappe import _
class BorrowProduct(Document):
	def validate(self):
		if self.is_new() or self.has_value_changed("product") or self.has_value_changed("stock_location") :
			
			product = get_stock_location_prouct(self.product, self.stock_location)
			if product:
				self.cost = product.get("cost",0)

			if (self.cost or 0)==0:
					self.cost = frappe.get_cached_value("Product",self.product,"purchase_price")
		self.quantity = self.quantity or 1
		self.total_cost = self.cost * (self.quantity  or 1)
		
	
	def before_submit(self):
		if not self.borrow_account:
			self.borrow_account = frappe.get_cached_value("Outlet",self.outlet,"borrow_account")
		if not self.borrow_account:
			self.borrow_account = frappe.get_cached_value("Business Information",None,"borrow_account")
		if not self.borrow_account:
			frappe.throw(_("Please select account code for borrow account"))
	def on_submit(self):
		pass
		# submit go inventory transaction


		# submit to gl

			