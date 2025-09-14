# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BlockIceProduceGrid(Document):
	def validate(self):
		self.max_produce_quantity = self.total_produce_per_day*self.row*self.column
		if not self.block_grid_name:
			self.block_grid_name = "{} {}x{}".format(self.location, self.row,self.column)
