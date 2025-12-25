# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from ice_factory_management_system.api.inventory import add_inventory_transaction
import json
class PurchaseOrder(Document):
	def validate(self):
		


		for p in self.purchase_products:
			p.sub_total = p.quantity * p.cost
			p.total_cost = p.sub_total

		self.update_party_name()
		self.total_quantity = sum([d.quantity for d in self.purchase_products])
		self.total_cost= sum([d.total_cost for d in self.purchase_products])
		self.balance= (self.total_cost or 0) - (self.total_payment or 0)
		if self.balance<0:
			frappe.throw(_("Payment amount cannot greater than purchase order amount"))

		


	def before_submit(self):


		self.update_account_code()
		self.validate_product_unit()

	def on_submit(self):
		self.validate_account_code()
		submit_to_GL_entry(self)
		update_stock_product(self)
 
	
	def validate_account_code(self):
		# check if product dont have assset account
		if len([d for d in self.purchase_products if not d.inventory_account])>0:
			frappe.throw(_("Account code in purchase order product is required."))
		
		if not self.payable_account:
			frappe.throw(_("Please select payable account"))
		# validate payment account
		if len([d for d in self.payments if not d.account])>0:
			frappe.throw(_("Please select account code in payment list"))

		

	def update_account_code(self):
		# *****inventory account priority ****
		# 1 Stock Location, 2 from outlet, 3 from business information
		# get from business branch
		for p in [d for d in self.purchase_products if not d.inventory_account]:
			# get from stock location
			p.inventory_account = frappe.get_cached_value("Stock Location",self.stock_location, "default_inventory_account")
			# still dont have account code check from outlet
			if not p.inventory_account and self.outlet:
				p.inventory_account = frappe.get_cached_value("Outlet",self.outlet, "inventory_account")
			# get from business branch
			if not p.inventory_account:
				p.inventory_account = frappe.get_cached_value("Business Information",None,"inventory_account")


		# validate payable account
		if (self.balance or 0) >0 and not self.payable_account:
			self.payable_account = frappe.get_cached_value("Business Information",None,"payable_account")

		# validate payment account
		for p in [d for d in self.payments if not d.account]:
			payment_type_doc = frappe.get_cached_doc("Payment Type",p.payment_type)
			p.account = next((r.account for r in payment_type_doc.payment_type_accounts if r.outlet == self.outlet), "")
			
			# if still not have account then get account code from payment type
			if not p.account:
				p.account = payment_type_doc.account

	def validate_product_unit(self):
		for p in [d for d in self.purchase_products if d.is_inventory_product ==1 and d.base_unit != d.unit]:
			sql="select name,multiplier from `tabProduct Units` where parent=%(product_code)s and unit = %(unit)s"
			data = frappe.db.sql(sql,{"product_code": p.product_code,"unit":p.unit},as_dict = 1)
			if data:
				p.multiplier = data[0].get("multiplier")
			else:
				frappe.throw("Product <strong>{}-{}</strong> does not have unit <strong>{}</strong>.".format(p.product_code,p.product_name,p.unit))


	def update_party_name(self):
		##update value of party name
		doctype = self.party_type
		name = self.party
		party_name =  frappe.get_value(doctype, name, '{}_name'.format(doctype.lower()))
		self.party_name = party_name
		if self.party_type in ["Customer","Vendor"]:
			self.phone_number = frappe.get_cached_value(self.party_type, self.party,"phone_number_1")
		else:
			self.phone_number = frappe.get_cached_value(self.party_type, self.party,"phone_number")

		##end update part name value		


@frappe.whitelist()
def get_init_purchase_cost(param):
	p = json.loads(param)

	#
	cost = 0.0
	sql = """
		select
			product as product_code,
			cost
		from `tabVendor Product Price`
		where parent = %(vendor)s
		and product in %(product_codes)s
	"""

	rows = frappe.db.sql(sql, {
		"vendor": p["doc"]["party"],
		"product_codes": tuple(p["product_codes"]),
	}, as_dict=True)

	# Build lookup map
	cost_map = {row.product_code: row.cost for row in rows}

	# 🔑 iterate over PRODUCT CODES, not SQL rows
	result = [
		{
			"product_code": code,
			"cost": float(cost_map.get(code, 0))
		}
		for code in p["product_codes"]
	]

	for r in [d for d in result if d["cost"] == 0] : 
		doc = frappe.get_doc("Product", r["product_code"])
		r["cost"] = doc.purchase_price
	return result
			
def update_stock_product(self):
	data = [
		{
			"ref_doctype":self.doctype,
			"ref_docname":self.name,
			"posting_date":self.posting_date,
			"stock_location":self.stock_location,
			"product_code":p.product_code,
			"unit":p.unit,
			"quantity": p.quantity,
			"multiplier":p.multiplier or 1,
			"is_calculate_cost": 0 if p.costing_method == "Fixed Cost" else 1,
			"cost":p.cost,
			"note": "បញ្ជូលចំនួនបន្ថែមពីបញ្ជារទិញលេខ {}".format(self.name)
		}
		for p in self.purchase_products if p.is_inventory_product == 1
	]
	add_inventory_transaction(data)
	 


def submit_to_GL_entry(self):

	from ice_factory_management_system.api.accounting import submit_general_ledger_entry
	docs = []

	for acc in set([d.inventory_account for d in self.purchase_products]):
		if not acc:
				frappe.throw(_("Account code in purchase order product is required."))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":acc,
			"amount":sum([d.total_cost for d in self.purchase_products if d.inventory_account == acc]),
			"against":self.party + " - " + self.party_name,
			"voucher_type":"Purchase Order",
			"voucher_no":self.name,
			"remark":"បញ្ជាទិញពី {0} នៅថ្ងៃទី {1}។ សរុបទឹកប្រាក់ {2}".format(
				self.party + "-" + self.party_name ,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				frappe.format(sum([d.total_cost for d in self.purchase_products if d.inventory_account == acc]),{"fieldtype":"Currency"})),
			"party_type": self.party_type,
			"party": self.party,
			"party_name": self.party_name,
		}
		docs.append(doc)

	# add payment account
	for acc in set([d.account for d in self.payments]):
		if not acc:
				frappe.throw(_("Please enter payment account code in payment list"))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":acc,
			"amount":sum([d.payment_amount for d in self.payments if d.account == acc]),
			"against":self.name,
			"voucher_type":"Purchase Order",
			"voucher_no":self.name,
			"remark":"ទូទាត់ទឹកប្រាក់បញ្ជាទិញអោយ {0}, នៅថ្ងៃទី {1}, ចំនួនទឹកប្រាក់​ {2}".format(
				self.party + "-" + self.party_name,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				frappe.format(sum([d.payment_amount for d in self.payments if d.account == acc]),{"fieldtype":"Currency"})
			),
			"party_type":self.party_type,
			"party": self.party,
			"party_name": self.party_name
		}
		docs.append(doc)
	
	
	if self.balance:
		if not self.payable_account:
			frappe.throw(_('Please select payable account'))
		doc = {
			"doctype":"GL Entry",
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":self.payable_account,
			"amount":self.balance,
			"against_voucher_type":"Purchase Order",
			"against_voucher_no": self.name,
			"voucher_type":"Purchase Order",
			"voucher_no":self.name,
			"party_type": self.party_type,
			"party":self.party,
			"party_name":self.party_name,
			"remark":"បញ្ជាទិញពី {0} នៅថ្ងៃទី {1}។ សរុបទឹកប្រាក់ {2}។ ជំពាក់ {3}".format(
				self.party + "-" + self.party_name ,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				frappe.format(sum([d.total_cost for d in self.purchase_products if d.inventory_account == acc]),{"fieldtype":"Currency"}),
																				frappe.format(self.balance or 0,{"fieldtype":"Currency"})
																				),
		}

		docs.append(doc)
	submit_general_ledger_entry(docs=docs)