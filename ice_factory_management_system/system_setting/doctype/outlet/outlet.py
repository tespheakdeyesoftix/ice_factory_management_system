# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Outlet(Document):
	def validate(self):
		if (self.outlet_name_kh or "") == "":
			self.outlet_name_kh = self.outlet_name_en
	
	def before_insert(self):
		pass
		# outlets = frappe.get_all("Outlet", fields=["name"])
		# accounts = frappe.db.get_list("Account Code", fields=["*"],filters={"outlet": outlets[0].name})
		# insert_accounts(self,accounts)

def insert_accounts(self,accounts):
	for a in accounts:
		a.name = a.account_code + " - " + a.account_name + " - "+ ''.join(word[0].upper() for word in self.outlet_name_en.split() if word)
		a.parent_account_code = a.parent_account_code + " - "+ ''.join(word[0].upper() for word in self.outlet_name_en.split() if word) if a.parent_account_code else ""
		sql = """INSERT INTO `tabAccount Code` 
				(`name`, 
				`creation`, 
				`modified`, 
				`modified_by`, 
				`owner`, 
				`docstatus`, 
				`idx`, 
				`lft`, 
				`rgt`, 
				`is_group`, 
				`old_parent`, 
				`parent_account_code`, 
				`account_code`, 
				`account_name`, 
				`root_type`, 
				`account_type`, 
				`outlet`) 
				VALUES
				('{0}',NOW(),NOW(),'{1}','{2}',1,1,0,0,{3},'','{4}','{5}','{6}','{7}','{8}','{9}')
				""".format(a.name,frappe.session.user,frappe.session.user,a.is_group,a.parent_account_code,a.account_code,a.account_name,a.root_type,a.account_type,self.outlet_name_en)
		frappe.db.sql(sql)
		frappe.db.commit()

@frappe.whitelist()
def get_default_accounts(outlet=""):
	cash_account = ""
	bank_account = ""
	income_account = ""
	free_account = ""
	cash_transfer_account = ""
	receivable_account = ""
	credit_account = ""
	write_off_account = ""
	inventory_account = ""
	if outlet:
		outlet_default = frappe.get_doc("Outlet", outlet)
		cash_account = outlet_default.cash_account
		bank_account = outlet_default.bank_account
		income_account = outlet_default.income_account
		free_account = outlet_default.free_account
		cash_transfer_account = outlet_default.cash_transfer_account
		receivable_account = outlet_default.receivable_account
		credit_account = outlet_default.credit_account
		write_off_account = outlet_default.write_off_account
		inventory_account = outlet_default.inventory_account
	
	business_default = frappe.get_doc("Business Information")
	cash_account = business_default.cash_account if (cash_account or "") == "" else cash_account
	bank_account = business_default.bank_account if (bank_account or "") == "" else bank_account
	income_account = business_default.income_account if (income_account or "") == "" else income_account
	free_account = business_default.free_account if (free_account or "") == "" else free_account
	cash_transfer_account = business_default.cash_transfer_account if (cash_transfer_account or "") == "" else cash_transfer_account
	receivable_account = business_default.receivable_account if (receivable_account or "") == "" else receivable_account
	credit_account = business_default.credit_account if (credit_account or "") == "" else credit_account
	write_off_account = business_default.write_off_account if (write_off_account or "") == "" else write_off_account
	inventory_account = business_default.inventory_account if (inventory_account or "") == "" else inventory_account
	return {
		"cash_account":cash_account,
		"bank_account":bank_account,
		"income_account":income_account,
		"free_account":free_account,
		"cash_transfer_account":cash_transfer_account,
		"receivable_account":receivable_account,
		"credit_account":credit_account,
		"write_off_account":write_off_account,
		"inventory_account":inventory_account
		}
	