# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils.data import strip
import json
import frappe
from frappe import _ 
from ice_factory_management_system.api.inventory import add_inventory_transaction
class Product(Document):
	def validate(self):
		if (self.product_name_kh or "") == "":
			self.product_name_kh = self.product_name
		if self.cost and not self.purchase_price:
			self.purchase_price =  self.cost
		if not self.cost and  self.purchase_price:
			self.cost = self.purchase_price
		

	def autoname(self):
		from frappe.model.naming import set_name_by_naming_series
		if strip(self.naming_series) !="" and strip(self.product_code) =="":
			set_name_by_naming_series(self)
			self.product_code = self.name		
		self.product_code = strip(self.product_code)
		self.name = self.product_code
	
	def on_update(self):
		product_outlets = []
		for a in self.product_outlet:
			product_outlets.append({"outlet":a.outlet})
		self.product_outlets = json.dumps(product_outlets)
		update_product_unit(self)

		# update inventory transaction
		if self.has_value_changed("is_inventory_product"):
			self.validate_product_use_in_inventory_transaction()
			

		# self.update_stock()

	def after_insert(self):
		if self.is_inventory_product==1:
			self.update_stock()

	@frappe.whitelist()
	def get_stats(self):
		
		sql="select stock_location as label,quantity, quantity as value,cost  from `tabStock Location Products` where product_code=%(product_code)s"
		data = frappe.db.sql(sql,{"product_code":self.name},as_dict = 1)
		
		if data:
			data.append({
				"label":_("Total"),
				"value": sum([d.get("value") for d in data])
				 
			})
		# format number
		for d in data:
			d["value"] = frappe.format(d.get("value"),{"fieldtype":"Float"})


		if data:
			stock_value = sum([(d.get("quantity") or  0)* (d.get("cost") or 0) for d in data ])
			 
			data.append({

				"label":_("Stock Value"),
				"value":frappe.format(stock_value or 0,{"fieldtype":"Currency"}),
				
			})
			
		return data
	
	def update_stock(self):
		

		add_inventory_transaction([
			{
			"ref_doctype":self.doctype,
			"ref_docname":self.name,
			"posting_date":frappe.utils.getdate(self.creation),
			"stock_location":self.stock_location,
			"product_code":self.name,
			"unit":self.unit,
			"quantity": self.opening_quantity,
			"multiplier":1,
			"cost":self.cost,
			"is_calculate_cost":1,
			"note": "ចំនួនដើមគ្រា"
		}
		])

	

	def validate_product_use_in_inventory_transaction(self):
		if self.is_inventory_product == 0:

			# check if product have in inventory transaction
			sql = "select name from `tabInventory Transactions` where ref_doctype<>'Product'and product_code =%(product_code)s"
			if frappe.db.sql(sql,{"product_code":self.product_code}):
				frappe.throw(_("This product has been use in inventory transaction. We can not change this to none inventory tracking product."))
			
			self.opening_quantity = 0
			self.cost = 0
			# delete opening transaction and delete product from stock lodation product
			frappe.db.sql("delete from `tabInventory Transactions` where product_code = %(product_code)s",{"product_code":self.name})
			frappe.db.sql("delete from `tabStock Location Products` where product_code = %(product_code)s",{"product_code":self.name})
	@frappe.whitelist()
	def get_stock_location_product_for_adjustment(self):
		sql = """
			select 
				a.name as stock_location,
				coalesce(b.quantity,0) as current_quantity,
				coalesce(b.quantity,0) as new_quantity,
				coalesce(b.cost,0) as current_cost,
				coalesce(b.cost,0) as new_cost
			from `tabStock Location` a
			left join `tabStock Location Products`  b on a.name = b.stock_location and b.product_code = %(product_code)s
		"""
		data = frappe.db.sql(sql, {"product_code":self.name},as_dict = 1)
		return data
	
	@frappe.whitelist()
	def update_stock_adjustment(self):
		if [d for d in self.stock_adjustment_data if d.get("new_quantity")<0]:
			frappe.throw(_("Quantity cannot less than 0"))
			
		if [d for d in self.stock_adjustment_data if d.get("new_cost")<0]:
			frappe.throw(_("Cost cannot less than 0"))

		# update quantity adjustment 
		add_inventory_transaction([
			{
				"ref_doctype":self.doctype,
				"ref_docname":self.name,
				"posting_date":frappe.utils.getdate(frappe.utils.now()),
				"stock_location":p.get("stock_location"),
				"product_code":self.name,
				"unit":self.unit,
				"quantity": (p.get("new_quantity") or 0 ) - (p.get("current_quantity") or 0),
				"multiplier":0,
				"is_calculate_cost":0,
				"cost":p.get("current_cost") or 0,
				"note": "កែប្រែចំនួនទំនិញ"
			}
			for p in self.stock_adjustment_data
			if 
			((p.get("new_quantity") or 0) != (p.get("current_quantity") or 0))  
		])
		# cost
		add_inventory_transaction([
			{
				"ref_doctype":self.doctype,
				"ref_docname":self.name,
				"posting_date":frappe.utils.getdate(frappe.utils.now()),
				"stock_location":p.get("stock_location"),
				"product_code":self.name,
				"unit":self.unit,
				"quantity": 0,
				"multiplier":1,
				"is_calculate_cost":1,
				"cost":p.get("new_cost") or 0,
				"note": "កែប្រែថ្លៃដើម"
			}
			for p in self.stock_adjustment_data
			if 
			((p.get("new_cost") or 0) != (p.get("current_cost") or 0))  
		])

		

		frappe.msgprint(_("Update stock adjustment successfully"))
 

def update_product_unit(self):
	if len(self.product_units or [])>0:
		if self.has_value_changed("price") or self.has_value_changed("unit"):
			for a in self.product_units:
				if a.base_product_unit == 1:
					a.price = self.price
					a.unit = self.unit
					a.multiplier = 1
	else:
		self.append("product_units", {
                "unit":self.unit,
                "multiplier": self.multiplier,
                "price": self.price,
				"base_product_unit": 1
            })

@frappe.whitelist()
def get_product_accounts(product_code="",outlet=""):
	income_account = ""
	free_account = ""
	receivable_account = ""
	expense_account = ""
	inventory_account = ""
	borrow_account = ""
	product_defaults = frappe.get_doc("Product", product_code)
	product_default = [a for a in product_defaults.product_accounts if a.outlet == outlet]
	if len(product_default) > 0:
		income_account = product_default[0].income_account
		free_account = product_default[0].free_account
		expense_account = product_default[0].expense_account
		borrow_account = product_default[0].borrow_account

	if outlet:
		outlet_default = frappe.get_doc("Outlet", outlet)
		income_account = outlet_default.income_account if (income_account or "") == "" else income_account
		free_account = outlet_default.free_account if (free_account or "") == "" else free_account
		inventory_account = outlet_default.inventory_account
		if not borrow_account:
			borrow_account = outlet_default.borrow_account

	business_default = frappe.get_doc("Business Information")
	income_account = business_default.income_account if (income_account or "") == "" else income_account
	free_account = business_default.free_account if (free_account or "") == "" else free_account

	receivable_account = business_default.receivable_account if (receivable_account or "") == "" else receivable_account

	return {
			"income_account":income_account,
			"free_account":free_account,
			"receivable_account":receivable_account,
			"expense_account":expense_account,
		 	"inventory_account":inventory_account,
			 "borrow_account":borrow_account
		}