# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from ice_factory_management_system.overrides.base_document import BaseDocument


class BlockIceProduce(BaseDocument):
	def validate(self):
		self.outlet = frappe.get_cached_value("Business Information",None,"block_ice_outlet")
		super().validate()
		
		if  frappe.utils.getdate(self.posting_date) > frappe.utils.getdate(frappe.utils.now()) :
			frappe.throw("Produce date can not be greater than current date")
		if self.is_new():
			# check if current date already have produce record
			sql="select name from `tabBlock Ice Produce` where posting_date = %(posting_date)s and docstatus <> 2"
			if frappe.db.sql(sql,{"posting_date":self.posting_date},as_dict=1):
				frappe.throw("Block ice produce on {} already exist.".format(frappe.format(self.posting_date,{"fieldtype":"Date"})))
		else:
			self.total_produce_quantity = sum([d.total_produce_quantity or 0 for d in self.produce_quantity])
			self.total_defected_quantity = sum([d.defected_quantity or 0 for d in self.produce_quantity])
	
	def before_insert(self):
		
		# generate block grid data 
		if not self.amended_from:
			self.block_grid_data = []
			block_grid_data = frappe.db.sql("select name,block_grid_name,max_produce_quantity,`column`,`row`,total_produce_per_day from `tabBlock Ice Produce Grid` order by name",as_dict = 1)
			for d in block_grid_data:
				self.append("produce_quantity", {
					"block_grid_number": d.get("name"),
					"block_grid_name": d.get("block_grid_name"),
					"max_produce_quantity":d.get("max_produce_quantity"),
					"row":d.get("row"),
					"column":d.get("column"),
					"total_remaining_quantity":d.get("max_produce_quantity"),
					"total_produce_per_day":d.get("total_produce_per_day"),
					"produce_data":str( [[0] * d.get("column") for _ in range(d.get("row"))])
				})
	
	def on_update(self):
		
		for d in self.produce_quantity:
			d.total_remaining_quantity = (d.max_produce_quantity or 0)  -  (d.total_produce_quantity or 0)

		# total to parent doctype 
		self.max_produce_quantity = sum([d.max_produce_quantity or 0 for d in self.produce_quantity ])
		self.total_produce_quantity= sum([d.total_produce_quantity or 0 for d in self.produce_quantity ])
		self.total_remaining_quantity= sum([d.total_remaining_quantity or 0 for d in self.produce_quantity ])


	def before_submit(self):
		if self.total_produce_quantity<=0:
			frappe.throw("Please enter produce quantity")