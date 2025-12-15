import frappe
from ice_factory_management_system.api.utils import get_response_user_information,get_setting
from frappe import _

@frappe.whitelist( allow_guest=True,methods="POST" )
def login(property,usr, pwd,station_name):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.throw(_("Usename and password incorrect."))
    user_info = get_response_user_information(property)
    
    frappe.response["message"] = user_info
    frappe.response["home_page"] =user_info.get("home_page")
    frappe.response["setting"] = get_setting(station_name)

def get_employee_doc():
    employee_id = frappe.db.exists("Employee",{"user_id":frappe.session.user})
    if employee_id:
        return frappe.get_cached_doc("Employee",employee_id)
        
def get_employee_outlets():
    doc = get_employee_doc()
    if doc:
        outlets = [doc.default_outlet]
        outlets = outlets + [d.outlet for d in doc.outlets if not d.outlet   in outlets ]
        return outlets
    return None