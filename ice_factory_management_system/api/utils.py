from builtins import str
import frappe
import base64
from frappe import _
@frappe.whitelist(allow_guest=True)
def check_api_url(property_code):
        
    doc = frappe.get_cached_doc("Business Information",None)
    if doc.property_code ==  property_code:
        
        return {
            "property_code":property_code,
            "property_name":doc.business_name_en, 
            "photo":doc.photo
    }
       
    frappe.throw(_("Property {property_code} does not exist").format(property_code=property_code))


@frappe.whitelist( allow_guest=True,methods="POST" )
def login(property,usr, pwd):
 
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.throw(_("Usename and password incorrect."))
        
    frappe.response["message"] = get_response_user_information(property)

     

def generate_keys(user):
	"""
	generate api key and api secret
 
	:param user: str
	"""
	# frappe.only_for("System Manager")
	user_details = frappe.get_doc("User", user)
	api_secret = frappe.generate_hash(length=15)
	# if api key is not set generate api key
	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	user_details.api_secret = api_secret
	user_details.save(ignore_permissions=True)

	return api_secret



@frappe.whitelist(allow_guest=True)
def check_user_login(property):
 
    if frappe.session.sid == "Guest":
        frappe.response["message"] =  frappe.session.sid
    else:
        frappe.response["message"] = get_response_user_information(property)
        
def get_response_user_information(property):
    phone_number =""
    address =""
    employee_id=""
    position=""
    user = frappe.get_doc("User", frappe.session.user)
    

    sql = "select position,name,phone_number,address from `tabEmployee` where user_id = '{}' limit 1".format(frappe.session.user)
    data = frappe.db.sql(sql, as_dict=1)
    if data:
        position = data[0].get("position")
        employee_id = data[0].get("name")
        phone_number = data[0].get("phone_number")
        address = data[0].get("address")
    api_generate = generate_keys(frappe.session.user)
    # get home_page 
    
    home_page = ""
    
    if frappe.session.user!="Administrator": 
        roles = frappe.get_roles( frappe.session.user)
        sql = "select home_page from `tabRole` where name in %(roles)s and coalesce(home_page,'')!='' limit 1"
        role_data = frappe.db.sql(sql, {"roles":roles},as_dict=1)

        if role_data:
            home_page = role_data[0].get("home_page")


    return {
            "username":user.username,
            "full_name":user.full_name,
            "role_profile":user.role_profile_name,
            "photo":user.user_image,
            "phone_number":phone_number,
            "address":address,
            "name":frappe.session.user,
            "position":position,
            "token": base64.b64encode(str("{}:{}".format(user.api_key,api_generate)).encode("utf-8")).decode('utf-8'),
            "employee_id":employee_id,
            "home_page":home_page

    }

@frappe.whitelist()
def audit_trail(transaction_date,transaction_type,doc_type,doc_name,username,description):
    doc = frappe.new_doc("User Audit Trail")
    doc.transaction_date = transaction_date
    doc.transaction_type = transaction_type
    doc.doc_type = doc_type
    doc.doc_name = doc_name
    doc.username = username
    doc.description = description
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

@frappe.whitelist()
def inventory_transaction(transaction_date,transaction_type,transaction_number,product,product_name,stock_unit,unit,stock_location,quantity,note):
    doc = frappe.new_doc("Inventory Transaction")
    doc.transaction_date = transaction_date
    doc.transaction_type = transaction_type
    doc.transaction_number = transaction_number
    doc.product = product
    doc.product_name = product_name
    doc.stock_unit = stock_unit
    doc.unit = unit
    doc.stock_location = stock_location
    doc.quantity = quantity
    doc.note = note
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

