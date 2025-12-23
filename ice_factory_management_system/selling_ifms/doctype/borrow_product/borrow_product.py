# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ice_factory_management_system.api.inventory import get_stock_location_prouct,add_inventory_transaction
from frappe import _
from frappe.utils import getdate
import json
class BorrowProduct(Document):
	def validate(self):
		if not self.flags.ignore_validate_cost:#we do not run this when use use return option from doctype form detail
			if self.is_new() or self.has_value_changed("product") or self.has_value_changed("stock_location") :
				
				product = get_stock_location_prouct(self.product, self.stock_location)
				if product:
					self.cost = product.get("cost",0)

				if (self.cost or 0)==0:
						self.cost = frappe.get_cached_value("Product",self.product,"purchase_price")

		self.quantity = self.quantity or 1
		self.total_cost = self.cost * (self.quantity  or 1)
		if self.transaction_type == "Borrow":
			self.balance = self.quantity - (self.return_quantity or 0)
		else:
			#  validate return balance must be less then borrow balance
			if self.borrow_reference_name:
				if frappe.db.get_value("Borrow Product", self.borrow_reference_name,"balance") < self.quantity:
					frappe.throw(_("Return quantity can not be greater than borrow quantity")) 
				# validate if return date is < borrow data
				if  getdate(frappe.db.get_value("Borrow Product", self.borrow_reference_name,"posting_date"))>getdate(self.posting_date):
					frappe.throw(_("Return date can not be smaller than borrow date"))


		
	
	def before_submit(self):
		if not self.borrow_account:
			self.borrow_account = frappe.get_cached_value("Outlet",self.outlet,"borrow_account")
		if not self.borrow_account:
			self.borrow_account = frappe.get_cached_value("Business Information",None,"borrow_account")
		if not self.borrow_account:
			frappe.throw(_("Please select account code for borrow account"))
	def on_submit(self):
		if not self.sale_product_id:
			submit_to_inventory(self)

			# submit to gl
		update_borrow_transaction_quantity(self)
			


	def on_cancel(self):

		if self.sale_product_id:
			if not self.flags.force_cancel: #this flag has been use in sale.py when user delete sale
				frappe.throw(_("You can not Cancel this transaction, because this transaction is created from Sale."))

		submit_to_inventory(self)

		update_borrow_transaction_quantity(self)



	@frappe.whitelist()
	def on_return_product(self,data):
		# frappe.throw(data.get("posting_date"))
		doc = frappe.get_doc({
				"doctype":"Borrow Product",
				"posting_date":data.get("posting_date"),
				"transaction_type":"Return",
				"borrow_reference_name":self.name,
				"outlet":self.outlet,
				"stock_location":self.stock_location,
				"customer":self.customer,
				"product": self.product,
				"quantity":data.get("quantity"),
				"cost":self.cost,
				"reference_doctype":self.reference_doctype,
				"reference_name":self.reference_name,
				"note":data.get("note","")
			})
		doc.flags.ignore_validate_cost = True
		doc.insert()
		doc.submit()

		frappe.msgprint(_("Add return successfully"))


		

def update_borrow_transaction_quantity(self):
	if self.transaction_type =="Return" and self.borrow_reference_name:
		sql = """ 
					select max(posting_date) as last_return_date, sum(quantity) as total 
					from `tabBorrow Product` 
					where 
						borrow_reference_name=%(name)s and docstatus=1
					
				"""

		data = frappe.db.sql(sql,{"name":self.borrow_reference_name},as_dict=1)
		update_data = {
				"name":self.borrow_reference_name,
				"return_quantity": 0,
				"last_return_date" :None
			}
		 
		if data:
			
			update_data = {
				"name":self.borrow_reference_name,
				"return_quantity":data[0].get("total") or 0,
				"last_return_date" :data[0].get("last_return_date")
			}
		 
		frappe.db.sql("update `tabBorrow Product` set last_return_date = %(last_return_date)s, return_quantity = %(return_quantity)s, balance = quantity - %(return_quantity)s where name = %(name)s",update_data)


	
@frappe.whitelist()			
def submit_to_inventory(self):
	multiplier = (1 if self.docstatus == 2 else -1) * (1 if self.transaction_type=='Borrow' else -1)
	note = ""
	if self.docstatus == 1 and self.transaction_type == "Borrow":
		note = f"អថិថិជន {self.customer} - {self.customer_name} បានខ្ចី ចំនួន៖ {self.quantity}"
	elif self.docstatus == 2 and self.transaction_type == "Borrow":
		note = f"ប្រតិបត្តិការខ្ចីត្រូវបានបោះបង់"
	elif self.docstatus == 1 and self.transaction_type == "Return":
		note = f"អថិថិជន {self.customer} - {self.customer_name} បានសង ចំនួន៖ {self.quantity}"
	elif self.docstatus == 2 and self.transaction_type == "Return":
		note = f"ប្រតិបត្តិការសងទំនិញត្រូវបានបោះបង់"


	data = [
		{
			"ref_doctype":self.doctype,
			"ref_docname":self.name,
			"posting_date":self.posting_date,
			"stock_location":self.stock_location,
			"product_code":self.product,
			"unit":self.unit,
			"quantity": self.quantity*multiplier,
			"is_calculate_cost":0,
			"note":note
		}  
	]
	add_inventory_transaction(data)


@frappe.whitelist()
def get_customer_borrow_product_remaining(customer):
	
	sql="""select name, product,posting_date,product_name, quantity as borrow_quantity,
		return_quantity as returned_quantity,
		balance as remaining_quantity,
		balance as return_quantity,
		0 as balance_quantity,
		cost,
		reference_doctype,
		reference_name,
		outlet,
		stock_location

		from `tabBorrow Product`
		where
			docstatus = 1 and 
			customer = %(customer)s and 
			balance>0 and 
			transaction_type = 'Borrow'
	"""
	data = frappe.db.sql(sql,{"customer":customer},as_dict = 1)
	return data or []

@frappe.whitelist()
def update_bulk_return_product(data):
	data = json.loads(data)
	if not [x for x in data.get("return_products") if x.get("return_quantity",0)>0]:
		frappe.throw(_("Please enter return quantity"))
	for d in [x for x in data.get("return_products") if x.get("return_quantity",0)>0]:

		doc = frappe.get_doc({
				"doctype":"Borrow Product",
				"posting_date":data.get("posting_date"),
				"transaction_type":"Return",
				"borrow_reference_name":d.get("name"),
				"outlet":d.get("outlet"),
				"stock_location":d.get("stock_location"),
				"customer":data.get("customer"),
				"product": d.get("product"),
				"quantity":d.get("return_quantity"),
				"cost":d.get("cost"),
				"reference_doctype":d.get("reference_doctype"),
				"reference_name":d.get("reference_name"),
				"note":d.get("note","")
			})
		doc.flags.ignore_validate_cost = True
		doc.insert()
		doc.submit()

	frappe.msgprint(_("Add return successfully"))