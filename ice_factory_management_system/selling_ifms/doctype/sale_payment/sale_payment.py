# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from ice_factory_management_system.api.accounting import submit_general_ledger_entry,cancel_general_ledger_entery
from ice_factory_management_system.overrides.base_document import BaseDocument
from ice_factory_management_system.api.utils import get_default_outlet,money_to_word
class SalePayment(BaseDocument):
	def validate(self):
 
		super().validate()
		self.payment_amount_in_word = money_to_word(int(self.payment_amount))
		self.validate_sale_payment_invoices()
		update_totals(self)
		self.validate_payment_amount()
		


	def before_submit(self):
		self.sales = [d for d in self.sales if (d.payment_amount or 0)>0  or (d.write_off_amount or 0)>0]
		if not self.payment_amount:
			frappe.throw(_("Please enter payment amount"))
		self.update_account_code()
	
	
	def on_submit(self):
		
		self.validate_account_code()
		frappe.db.sql("call sp_update_sale_information('',%(sale_payment_name)s)",{"sale_payment_name":self.name})
		submit_to_GL_entry(self)

		# make this enqueue
		frappe.enqueue("ice_factory_management_system.selling_ifms.doctype.sale_payment.sale_payment.add_comment_to_sale_after_submit_sale_payment",self=self)
		

		

	def on_cancel(self):
		self.flags.ignore_links = True
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Sale Payment' and voucher_no=%(name)s",{"name":self.name})
		frappe.db.sql("call sp_update_sale_information('',%(sale_payment)s)",{"sale_payment":self.name})
		frappe.enqueue("ice_factory_management_system.selling_ifms.doctype.sale_payment.sale_payment.add_comment_to_sale_after_cancel_sale_payment",self=self)
	 


	def validate_sale_payment_invoices(self):
		for s in self.sales:
			# update payment date to sale payment invoice
			s.payment_date = self.posting_date
			s.customer = self.customer
			# we force to validate sale amount, payment amount and write off amount from db again to
			# ensure sale amount information is correct before save to db
			
			sale_amount, sale_payment,sale_write_off =frappe.db.get_value("Sale",s.sale,["total_amount","total_payment","total_write_off"])
			s.total_amount = sale_amount or 0
			s.paid_amount = sale_payment or 0
			s.sale_balance = s.total_amount - (s.paid_amount + (sale_write_off or 0))
 
			s.balance = (s.sale_balance or 0) - ((s.payment_amount or 0) + (s.write_off_amount or 0))
		frappe.msgprint("dnt forget update sale balance")

	def validate_payment_amount(self):
		
		if self.input_amount:
			if (self.input_amount / float(self.exchange_rate))>self.payment_amount:
				frappe.throw(_("សូមបែងចែកចំនួនទឹកប្រាក់តាមវិកយប័ត្រអោយបានត្រឹមត្រូវ"))
		if self.payment_amount>self.amount_to_pay:
			frappe.throw(_("Payment amount cannot greater than amount to pay"))
	
	def update_account_code(self):
		if not self.enable_multiple_payment_type:
			if not self.account_paid_to:
				# get from outlet
				payment_type_doc = frappe.get_cached_doc("Payment Type",self.payment_type)
				self.account_paid_to = next((r.account for r in payment_type_doc.payment_type_accounts if r.outlet == self.outlet), "")
				if not self.account_paid_to:
					self.account_paid_to = payment_type_doc.account
		else:
			frappe.throw("payment type accoiunt for child table payment child table")
	
	def validate_account_code(self):
		if not self.enable_multiple_payment_type:
			if not self.account_paid_to:
				frappe.throw(_("Please select account code for Account Paid To field"))
		if not self.account_paid_from:
			frappe.throw(_("Please select account code for Account Paid From field"))
		if (self.write_off_amount or 0)	>0:
			if not self.write_off_account:
				frappe.throw(_("Please select account code for Write Off Account field"))

			
	# custom doc event
	@frappe.whitelist()
	def get_unpaid_sales(self):
		data = []
		if self.start_date and self.end_date:
			sql = """
				select 
					name, posting_date, total_amount,total_payment,balance 
					from `tabSale` 
					where 
						(name = %(sale)s or %(sale)s = '') and 
						balance> 0 and 
						sale_status = 'Closed' and 
						customer=%(customer)s and 
						outlet = %(outlet)s  and 
						posting_date between %(start_date)s and %(end_date)s
					order by 
						posting_date,
						name
				"""
			data = frappe.db.sql(sql,{"outlet":self.outlet,"sale":self.sale or '',"customer": self.customer,"start_date":self.start_date, "end_date":self.end_date},as_dict = 1)
		else:
			sql = """
				select 
					name, posting_date, total_amount,total_payment,balance 
					from `tabSale` 
					where 
						(name = %(sale)s or %(sale)s = '') and 
						balance> 0 and 
						sale_status = 'Closed' and 
						customer=%(customer)s and 
						outlet = %(outlet)s  
					order by 
						posting_date,
						name
				"""
			data = frappe.db.sql(sql,{"outlet":self.outlet,"sale":self.sale or '',"customer": self.customer},as_dict = 1)
		return data or []
	
	@frappe.whitelist()
	def get_customer_credit_balance(self):
		if not self.outlet:
			frappe.throw(_("Please select oulet"))
		sql = "select sum(balance) as balance from `tabSale` where outlet=%(outlet)s and customer=%(customer)s and balance>0"
		data = frappe.db.sql(sql,{"outlet":self.outlet,"customer": self.customer},as_dict = 1)
		if data:
			return data[0].get("balance")
		return 0
		
	@frappe.whitelist()
	def get_default_outlet(self):
		if self.sale:
			return frappe.db.get_value("Sale",self.sale,"outlet")
		return get_default_outlet()
	


def update_totals(self):

	self.total_sales_invoice = len([d   for d in self.sales if (d.payment_amount or 0)> 0 or (d.write_off_amount or 0)>0 ])
	self.payment_amount = sum([d.payment_amount or 0 for d in self.sales if (d.payment_amount or 0)> 0 ])
	self.write_off_amount = sum([d.write_off_amount or 0 for d in self.sales if (d.write_off_amount or 0)> 0 ])
	self.balance = self.amount_to_pay - (self.payment_amount + self.write_off_amount)


	
def verify_account(self):
	if self.account_paid_from == self.account_paid_to and ((self.account_paid_from or "") != "" and (self.account_paid_to or "") != ""):
		frappe.throw("Account paid from and account paid to cannot be the same.")
	
	payment_default = get_payment_default_account(self.outlet, self.payment_type)
	self.account_paid_to = payment_default.get("account") if (self.account_paid_to or "") == "" else self.account_paid_to

	from ice_factory_management_system.system_setting.doctype.outlet.outlet import get_default_accounts
	default = get_default_accounts(self.outlet)
	self.account_paid_from = default.get("receivable_account") if (self.account_paid_from or "") == "" else self.account_paid_from
	self.account_paid_to = default.get("cash_account") if (self.account_paid_to or "") == "" else self.account_paid_to
	self.write_off_account = default.get("write_off_account") if (self.write_off_account or "") == "" else self.write_off_account


def submit_to_GL_entry(self):
	docs = []
	
	for s in [d for d in self.sales if (d.payment_amount or 0) > 0 or (d.write_off_amount or 0)> 0]:
		# 1 post deduct account receivable
		doc = {
			"doctype":"GL Entry",
			"reference_doctype":"Sale",
			"reference_docname":s.sale,
			"outlet":self.outlet,
			"posting_date":self.posting_date,
			"account":self.account_paid_from,
			"credit_amount":(s.payment_amount or 0)  + (s.write_off_amount or  0),
			"against_voucher_type": "Sale",
			"against_voucher_no": s.sale,
			"voucher_type":"Sale Payment",
			"voucher_no":self.name,
			"party_type":"Customer",
			"party":self.customer,
			"remark": "ទទួលប្រាក់ពីអតិថិជន  {} នៅថ្ងៃទី {} លេខបង្កាន់ដៃ {}".format(
				self.customer + " - " + self.customer_name,
				frappe.format(self.posting_date,{"fieldtype":"Date"}),
				self.name
			)
		}
		docs.append(doc)

		# 2 post to payment type 
		if (s.payment_amount or 0)> 0:
			doc = {
				"doctype":"GL Entry",
				"reference_doctype":"Sale",
				"reference_docname":s.sale,
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":self.account_paid_to,
				"debit_amount":(s.payment_amount or 0) , 
				"against_voucher_type": "Sale",
				"against_voucher_no": s.sale,
				"voucher_type":"Sale Payment",
				"voucher_no":self.name,
				"party_type":"Customer",
				"party":self.customer,
				"remark": "ទទួលប្រាក់ពីអតិថិជន  {} នៅថ្ងៃទី {} លេខបង្កាន់ដៃ {}".format(
					self.customer + " - " + self.customer_name,
					frappe.format(self.posting_date,{"fieldtype":"Date"}),
					self.name
				)
			}
			docs.append(doc)

		# 3 write off
		if (s.write_off_amount or 0 )> 0:
			doc = {
				"doctype":"GL Entry",
				"reference_doctype":"Sale",
				"reference_docname":s.sale,
				"outlet":self.outlet,
				"posting_date":self.posting_date,
				"account":self.write_off_account,
				"debit_amount":(s.write_off_amount or  0),
				"against_voucher_type":"Sale",
				"against_voucher_no": s.sale,
				"voucher_type":"Sale Payment",
				"voucher_no":self.name,
				"party_type":"Customer",
				"party":self.customer,
				"remark": "កាតចោល {} from {}".format(frappe.format((self.write_off_amount),{"fieldtype":"Currency"}), (s.sale)),
			}
			docs.append(doc)

 


 
		
 
	submit_general_ledger_entry(docs=docs)

@frappe.whitelist()
def get_payment_default_account(outlet="",payment_type=""):
	from ice_factory_management_system.system_setting.doctype.exchange_rate.exchange_rate import get_exchange_rate
	payment_type = frappe.get_doc("Payment Type", payment_type)
	exchange_rate = get_exchange_rate(payment_type.currency)
	accounts = [a.account for a in payment_type.payment_type_accounts if a.outlet == outlet]
	if accounts:
		return {"account":accounts[0],"exchange_rate":exchange_rate["exchange_rate"],"symbol":exchange_rate["symbol"]}
	else:
		return {"account":"","exchange_rate":exchange_rate["exchange_rate"],"symbol":exchange_rate["symbol"]}
	
@frappe.whitelist()
def add_comment_to_sale_after_submit_sale_payment(self):
	for s in self.sales:
		doc = frappe.get_doc("Sale",s.sale)
		comment_text = f"""
			<br/>
			<strong>ទទួលប្រាក់ពីអតិថិជន</strong> <br/>
			បង្កាន់ដៃបង់ប្រាក់៖ <strong>{self.name}</strong><br/>
			កាលបរិច្ឆេទ៖ <strong>{frappe.format(s.posting_date,{"fieldtype":"Date"})}</strong><br/>
			ទឹកប្រាក់ទទួល៖ <strong>{frappe.format(s.payment_amount,{"fieldtype":"Currency"})}</strong><br/>
			ទឹកប្រាក់កាត់ចោល៖ <strong>{frappe.format(s.write_off_amount,{"fieldtype":"Currency"})}</strong>
		"""
		frappe.msgprint(comment_text)
		doc.add_comment('Info', comment_text)
	
@frappe.whitelist()
def add_comment_to_sale_after_cancel_sale_payment(self):
	for s in self.sales:
		doc = frappe.get_doc("Sale",s.sale)
		comment_text = f"""
			<br/>
			<strong style='color:red'>លុបការទទួលប្រាក់ពីអតិថិជន</strong> <br/>
			បង្កាន់ដៃបង់ប្រាក់៖ <strong>{self.name}</strong><br/>
			កាលបរិច្ឆេទ៖ <strong>{frappe.format(s.posting_date,{"fieldtype":"Date"})}</strong><br/>
			ទឹកប្រាក់ទទួល៖ <strong>{frappe.format(s.payment_amount,{"fieldtype":"Currency"})}</strong><br/>
			ទឹកប្រាក់កាត់ចោល៖ <strong>{frappe.format(s.write_off_amount,{"fieldtype":"Currency"})}</strong>
		"""
		frappe.msgprint(comment_text)
		doc.add_comment('Info', comment_text)