# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt
from frappe.utils import strip_html
from frappe.utils.password import update_password 
import frappe
from frappe.model.document import Document

class Employee(Document):
	def validate(self):
		if  strip_html(self.employee_code or ""):
			self.name = strip_html(self.employee_code or "")
		self._password = ""
		if self.password:
			self._password = self.password
			self.password = ""
 
	def on_update(self):
		# check if user tick Allow Login then create user to Uer table
		if self.allow_login:
			if not self.user_id:
				user_doc  = frappe.new_doc("User")
				user_doc.first_name = self.employee_name
				user_doc.username = self.username
				user_doc.email = "{}@mail.com".format(self.username.strip().lower().replace(" ", "_"))
				user_doc.language = self.language
				if self.role_profile:
					user_doc.append("role_profiles", {  
							"role_profile": self.role_profile
					})
					module_profile = frappe.get_cached_value("Role Profile",self.role_profile,"custom_module_profile") or ""
					user_doc.module_profile = module_profile

				user_doc.insert(ignore_permissions=True)
				self.user_id = user_doc.name
				

				if self._password:
					update_password(user=user_doc.name, pwd=self.get_password("_password"), logout_all_sessions=True)
	
			else:
				# check if user change username
				# then update user name to table user
				if check_user_field_changed(self,["username","employee_name","language","_password","allow_login","role_profile"]):
					user_doc = frappe.get_doc("User",self.user_id)
					user_doc.username = self.username
					user_doc.first_name = self.employee_name
					user_doc.language = self.language
					user_doc.enabled = self.allow_login
					user_doc.set("role_profiles", [])
					
					if self.role_profile:
						
						user_doc.append("role_profiles", {  
								"role_profile": self.role_profile
						})
						module_profile = frappe.get_cached_value("Role Profile",self.role_profile,"custom_module_profile") or ""
						user_doc.module_profile = module_profile
						
					else:
						user_doc.set("roles", [])
						user_doc.module_profile = ""
					
					if self._password:
						update_password(user=user_doc.name, pwd=self.get_password("_password"), logout_all_sessions=True)
					user_doc.save(ignore_permissions=True)
		else: #Not Allow to Login
			if self.user_id:
				user_doc = frappe.get_doc("User", self.user_id) 
				user_doc.enabled = False
				user_doc.save(ignore_permissions=True)


		update_outlet_user_permission(self)

	def on_trash(self):
		if(self.user_id):
			user_doc = frappe.get_doc("User", self.user_id) 
			user_doc.delete(ignore_permissions=True)


def check_user_field_changed(self, fields):
	for f in fields:
		if self.has_value_changed(f):
			return True
	return False

def update_outlet_user_permission(self):
	frappe.db.sql("delete from `tabUser Permission` where user=%(user)s and allow = 'Outlet'",{"user":self.user_id})
	outlets = [self.default_outlet]
	outlets = outlets + [d.outlet for d in self.outlets]
	for o in outlets:
		user_permission_doc = frappe.new_doc("User Permission")
		user_permission_doc.user = self.user_id
		user_permission_doc.allow = "Outlet"
		user_permission_doc.for_value = o
		user_permission_doc.insert(ignore_permissions=True)


