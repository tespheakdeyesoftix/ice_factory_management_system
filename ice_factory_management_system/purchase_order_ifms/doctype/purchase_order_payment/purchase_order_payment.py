# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

from frappe import _
import frappe
from frappe.model.document import Document
from ice_factory_management_system.overrides.base_document import BaseDocument
from ice_factory_management_system.api.utils import get_default_outlet,money_to_word
from ice_factory_management_system.api.accounting import submit_general_ledger_entry,cancel_general_ledger_entery

class PurchaseOrderPayment(BaseDocument):
	
	def validate(self):
		super().validate()		 
		self.payment_amount_in_word = money_to_word(int(self.payment_amount))
		self.validate_purchase_order_payment_invoices()
		update_totals(self)
		self.validate_payment_amount()


	def before_submit(self):
		self.purchase_orders = [d for d in self.purchase_orders if (d.payment_amount or 0)>0  or (d.write_off_amount or 0)>0]
		if not self.payment_amount:
			frappe.throw(_("Please enter payment amount"))
		self.update_account_code()

	def on_submit(self):		
		self.validate_account_code()
		frappe.db.sql("call sp_update_purchase_order_information('',%(purchase_order_payment_name)s)",{"purchase_order_payment_name":self.name})
		submit_to_general_ledger_entry(self)

		# make this enqueue
		frappe.enqueue("ice_factory_management_system.purchase_order_ifms.doctype.purchase_order_payment.purchase_order_payment.add_comment_to_purchase_order_after_submit_purchase_order_payment",self=self)

	def on_cancel(self):
		self.flags.ignore_links = True
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Purchase Order Payment' and voucher_no=%(name)s",{"name":self.name})
		frappe.db.sql("call sp_update_purchase_order_information('',%(purchase_order_payment_name)s)",{"purchase_order_payment_name":self.name})

		frappe.enqueue("ice_factory_management_system.purchase_order_ifms.doctype.purchase_order_payment.purchase_order_payment.add_comment_to_purchase_order_after_cancel_purchase_order_payment",self=self)


	# custom doc event
	def validate_purchase_order_payment_invoices(self):
		for s in self.purchase_orders:
			# update payment date to purchase-order payment invoice
			s.payment_date = self.posting_date
			s.party_type = self.party_type
			s.party = self.party

			# we force to validate purchase-order amount, payment amount and write off amount from db again to
			# ensure purchase-order amount information is correct before save to db
			po_amount, po_payment,po_write_off =frappe.db.get_value("Purchase Order",s.purchase_order,["total_cost","total_payment","total_write_off"])
			s.total_amount = po_amount or 0
			s.paid_amount = po_payment or 0
			s.purchase_order_balance = s.total_amount - (s.paid_amount + (po_write_off or 0))
			s.balance = (s.purchase_order_balance or 0) - ((s.payment_amount or 0) + (s.write_off_amount or 0))
			s.payment_type = self.payment_type	
	
	def validate_payment_amount(self):
		if self.input_amount:
			if (self.input_amount / float(self.exchange_rate))>self.payment_amount:
				frappe.throw(_("សូមបែងចែកចំនួនទឹកប្រាក់តាមវិកយប័ត្រអោយបានត្រឹមត្រូវ"))
		if self.payment_amount>self.amount_to_pay:
			frappe.throw(_("Payment amount cannot greater than amount to pay"))

	def update_account_code(self):		
		if not self.account_paid_to:
			# get from outlet
			pt_doc = frappe.get_cached_doc("Payment Type",self.payment_type)
			self.account_paid_to = next((r.account for r in pt_doc.payment_type_accounts if r.outlet == self.outlet), "")
			if not self.account_paid_to:
				self.account_paid_to = pt_doc.account
	
	def validate_account_code(self):		
		if not self.account_paid_to:
			frappe.throw(_("Please select account code for Account Paid To field"))

		if not self.account_paid_from:
			frappe.throw(_("Please select account code for Account Paid From field"))

		if (self.write_off_amount or 0)	>0:
			if not self.write_off_account:
				frappe.throw(_("Please select account code for Write Off Account field"))


	##custom doc event for api
	@frappe.whitelist()
	def get_unpaid_purchase_orders(self):
		data = []
		sql = """select 
					outlet,
					party_type,
					party,
					party_name,
					name, 
					posting_date, 
					total_cost,
					total_payment,
					balance 
				from `tabPurchase Order` 
				where  1= 1
					and (name = %(purchase_order)s or %(purchase_order)s = '')  
					and balance> 0
					and docstatus = 1
					and party=%(party)s 
					and outlet = %(outlet)s  
					{}
				order by 
					posting_date,
					name
			"""
		filter = {
			"outlet":self.outlet,
			"purchase_order":self.purchase_order or '',
			"party": self.party
		}

		if self.start_date and self.end_date:
			sql = sql.format("and (posting_date between %(start_date)s and %(end_date)s)") 
			filter.update({
				"start_date":self.start_date, 
				"end_date":self.end_date
			})
		else:
			sql = sql.format("and 1=1")

		data = frappe.db.sql(sql, filter,as_dict = 1)

		return data or []
	
	@frappe.whitelist()
	def get_party_credit_balance(self):
		if not self.outlet:
			frappe.throw(_("Please select oulet"))
		sql = "select sum(balance) as balance from `tabPurchase Order` where docstatus = 1 and outlet=%(outlet)s and party=%(party)s and balance>0"
		data = frappe.db.sql(sql,{"outlet":self.outlet,"party": self.party},as_dict = 1)
		if data:
			return data[0].get("balance")
		return 0
	
	@frappe.whitelist()
	def get_default_outlet(self):
		if self.purchase_order:
			return frappe.db.get_value("Purchase Order",self.sale,"outlet")
		return get_default_outlet()
	
	@frappe.whitelist()
	def get_party_name(self):
		##update value of party name
		doctype = self.party_type
		if self.party:
			name = self.party
			party_name =  frappe.get_value(doctype, name, '{}_name'.format(doctype.lower()))
			return party_name
		return ""


#local method in doc
def update_totals(self):
	self.total_invoice = len([d   for d in self.purchase_orders if (d.payment_amount or 0)> 0 or (d.write_off_amount or 0)>0 ])
	self.payment_amount = sum([d.payment_amount or 0 for d in self.purchase_orders if (d.payment_amount or 0)> 0 ])
	self.write_off_amount = sum([d.write_off_amount or 0 for d in self.purchase_orders if (d.write_off_amount or 0)> 0 ])
	self.balance = self.amount_to_pay - (self.payment_amount + self.write_off_amount)

def submit_to_general_ledger_entry(self):
	docs = []
	for s in [d for d in self.purchase_orders if (d.payment_amount or 0) > 0 or (d.write_off_amount or 0)> 0]:
		# 1 post deduct account payable
		doc = {
			"doctype":"GL Entry",
			"reference_doctype":"Purchase Order",
			"reference_docname":s.purchase_order,
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":self.account_paid_from,
			"credit_amount":(s.payment_amount or 0) ,
			"against_voucher_type": "Purchase Order",
			"against_voucher_no": s.purchase_order,
			"voucher_type":"Purchase Order Payment",
			"voucher_no":self.name,
			"party_type":self.party_type,
			"party":self.party,
			"party_name":self.party_name,
			"transaction_type":"Payment",
			"remark": "បង់ប្រាក់ទៅ {} {} នៅថ្ងៃទី {} លេខបង្កាន់ដៃ {}".format(
				self.party_type, self.party + " - " + self.party_name,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				self.name
			)
		}
		docs.append(doc)

		# 2 post to payment type 
		if (s.payment_amount or 0)> 0:
			doc = {
				"doctype":"GL Entry",
				"reference_doctype":"Purchase Order",
				"reference_docname":s.purchase_order,
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":self.account_paid_to,
				"debit_amount":(s.payment_amount or 0) , 
				"against_voucher_type": "Purchase Order",
				"against_voucher_no": s.purchase_order,
				"voucher_type":"Purchase Order Payment",
				"voucher_no":self.name,
				"remark": "បង់ប្រាក់ទៅ {} {} នៅថ្ងៃទី {} លេខបង្កាន់ដៃ {}".format(
					self.party_type, self.party + " - " + self.party_name,
					frappe.format(self.posting_date,{"fieldtype":"Date"}),
					self.name
				)
			}
			docs.append(doc)

		# 3 write off
		if (s.write_off_amount or 0 )> 0:
			doc = {
				"doctype":"GL Entry",
				"reference_doctype":"Purchase Order",
				"reference_docname":s.purchase_order,
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":self.account_paid_from,
				"credit_amount": (s.write_off_amount or  0),
				"against_voucher_type": "Purchase Order",
				"against_voucher_no": s.purchase_order,
				"voucher_type":"Purchase Order Payment",
				"voucher_no":self.name,
				"party_type":self.party_type,
				"party":self.party,
				"party_name":self.party_name,
				"transaction_type":"Write Off",
				"remark": "កាត់ប្រាក់ចោល {} នៅថ្ងៃទី {} លេខបង្កាន់ដៃ {}".format(
					self.party + " - " + self.party_name,
					frappe.format(self.posting_date,{"fieldtype":"Date"}),
					self.name
				)
			}
			docs.append(doc)
			doc = {
				"doctype":"GL Entry",
				"reference_doctype":"Purchase Order",
				"reference_docname":s.purchase_order,
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":self.write_off_account,
				"debit_amount":(s.write_off_amount or  0),
				"against_voucher_type":"Purchase Order",
				"against_voucher_no": s.purchase_order,
				"voucher_type":"Purchase Order Payment",
				"voucher_no":self.name,
				"remark": "កាតចោល {} ពី {}".format(
					frappe.format((self.write_off_amount),{"fieldtype":"Currency"}), 
					(s.purchase_order)),
			}
			docs.append(doc)

	submit_general_ledger_entry(docs=docs)


@frappe.whitelist()
def add_comment_to_purchase_order_after_submit_purchase_order_payment(self):
	for s in self.purchase_orders:
		doc = frappe.get_doc("Purchase Order",s.purchase_order)
		comment_text = f"""
			<br/>
			<strong>បង់ប្រាក់ទៅ {self.party_type} </strong> <br/>
			បង្កាន់ដៃបង់ប្រាក់៖ <strong>{self.name}</strong><br/>
			កាលបរិច្ឆេទ៖ <strong>{frappe.format(s.posting_date,{"fieldtype":"Date"})}</strong><br/>
			ទឹកប្រាក់បង់៖ <strong>{frappe.format(s.payment_amount,{"fieldtype":"Currency"})}</strong><br/>
			ទឹកប្រាក់កាត់ចោល៖ <strong>{frappe.format(s.write_off_amount,{"fieldtype":"Currency"})}</strong>
		"""

		frappe.msgprint(comment_text)
		doc.add_comment('Info', comment_text)
		audit_trail_doc = {
			"doctype":"Audit Trail Log",
			"ref_doctype":"Purchase Order",
			"ref_doc_name":s.purchase_order,
			"outlet":self.outlet,
			"posting_date":frappe.utils.now(),
			"station":"Backend Admin",
			"audit_trail_type":"បង់ប្រាក់",
			"description": comment_text
		}
		frappe.get_doc(audit_trail_doc).insert(ignore_permissions=True,ignore_links=True)

@frappe.whitelist()
def add_comment_to_purchase_order_after_cancel_purchase_order_payment(self):
	for s in self.purchase_orders:
		doc = frappe.get_doc("Purchase Order",s.purchase_order)
		comment_text = f"""
			<br/>
			<strong style='color:red'>លុបការបង់ប្រាក់នៃ {self.party_type}</strong> <br/>
			បង្កាន់ដៃបង់ប្រាក់៖ <strong>{self.name}</strong><br/>
			កាលបរិច្ឆេទ៖ <strong>{frappe.format(s.posting_date,{"fieldtype":"Date"})}</strong><br/>
			ទឹកប្រាក់បង់៖ <strong>{frappe.format(s.payment_amount,{"fieldtype":"Currency"})}</strong><br/>
			ទឹកប្រាក់កាត់ចោល៖ <strong>{frappe.format(s.write_off_amount,{"fieldtype":"Currency"})}</strong>
		"""
		frappe.msgprint(comment_text)
		doc.add_comment('Info', comment_text)

		audit_trail_doc = {
			"doctype":"Audit Trail Log",
			"ref_doctype":"Purchase Order",
			"ref_doc_name":s.purchase_order,
			"outlet":self.outlet,
			"posting_date":frappe.utils.now(),
			"station":"Backend Admin",
			"audit_trail_type":"លុបការបង់ប្រាក់",
			"description": comment_text
		}
		frappe.get_doc(audit_trail_doc).insert(ignore_permissions=True,ignore_links=True)

