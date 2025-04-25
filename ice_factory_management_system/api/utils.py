from builtins import str
import frappe
import base64
from frappe import _
import json
from frappe.model.document import bulk_insert
from frappe.model.naming import make_autoname

def submit_general_ledger_entry(docs):
    bulk_insert("GL Entry", get_general_ledger_entry_record(docs=docs) , chunk_size=10000)
    frappe.db.commit()

def get_general_ledger_entry_record(docs):
    for d in docs:
        doc = frappe.get_doc(d)
        if doc.amount and not (doc.credit_amount or doc.debit_amount ):
            root_type = frappe.get_cached_value("Account Code",doc.account,"root_type")
            if root_type in ["Asset","Expenses"]:
                if doc.amount>0:
                    doc.debit_amount = abs(doc.amount)
                else:
                    doc.credit_amount = abs(doc.amount)
            else:
                if doc.amount>0:
                    doc.credit_amount = abs(doc.amount)
                else:
                    doc.debit_amount =abs(doc.amount)
        doc.name  = make_autoname("GLE.YYYY.-.#####")
        doc.docstatus = 1
        yield doc
        
def cancel_general_ledger_entery(doctype,docname):
    frappe.db.sql("update `tabGL Entry` set is_cancelled=1 where voucher_type='{}' and voucher_no='{}'".format(doctype,docname))
    frappe.db.commit()
    
    sql = "select * from `tabGL Entry` where voucher_type='{}' and voucher_no= '{}'".format( doctype,docname)
    data = frappe.db.sql(sql,as_dict=1)
    docs = []
    for r in data:
        doc = {
                "doctype":"GL Entry",
                "posting_date":r["posting_date"],
                "account":r["account"],
                "credit_amount":r["debit_amount"],
                "debit_amount":r["credit_amount"],
                "against":r["against"],
                "against_voucher_type":"Sale",
                "against_voucher_no": r["against_voucher_no"],
                "voucher_type":doctype,
                "voucher_no":docname,
                "remark": r["remark"],
                "party_type": r["party_type"],
                "party": r["party"]
            }
        docs.append(doc)
    submit_general_ledger_entry(docs)

@frappe.whitelist()
def get_currency_symbol(currency):
    symbol = frappe.get_cached_value("Currency", currency, "symbol")
    return symbol

@frappe.whitelist()
def get_default_account():
    data = frappe.get_doc("Business Information")
    return {
        "cash_account":data.cash_account,
        "bank_account":data.bank_account,
        "receivable_account":data.receivable_account,
        "income_account":data.income_account,
        "credit_account":data.credit_account,
        "write_off_account":data.write_off_account,
        "free_account":data.free_account,
    }
@frappe.whitelist()
def get_meta(doctype=None):
    data =  frappe.get_meta(doctype)
    return data

@frappe.whitelist(allow_guest=True)
def get_setting(station_name=""):
    data  = frappe.get_cached_doc("Business Information",None)
    data =json.loads( frappe.as_json(data))
    
    
    if station_name:
         if frappe.db.exists("Station", station_name):
            data["can_login_multi_site"]  = frappe.get_cached_value("Station",station_name,"can_login_multi_site")
            data["outlet"]  = frappe.get_cached_value("Station",station_name,"outlet")
            data["default_unit"]  = frappe.get_cached_value("Outlet",data.get("outlet"),"default_unit")
            
              
    return data
    

@frappe.whitelist(allow_guest=True)
def check_api_url(property_code,station_name,old_station_name):
    if not station_name:
        frappe.throw(_("Please enter your device name"))
        
    doc = frappe.get_cached_doc("Business Information",None)
    if doc.property_code ==  property_code:
        
        # check station
        if station_name != station_name:
            if frappe.db.exists("Station", station_name):
                if frappe.get_cached_value("Station",station_name,"is_used") ==1:
                    frappe.throw(_("This station name is already in used"))
            else:
                frappe.throw(_("This station name is not exist"))
                
            
        
        return {
            "property_code":property_code,
            "property_name":doc.business_name_en, 
            "photo":doc.photo,
            "station_name":station_name,
            "outlet":frappe.get_cached_value("Station",station_name,"outlet"),
            "can_login_multi_site":frappe.get_cached_value("Station",station_name,"can_login_multi_site")
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
    frappe.response["setting"] = get_setting()

     

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
    photo=""
    user = frappe.get_doc("User", frappe.session.user)
    

    sql = "select position,name,phone_number,address,photo from `tabEmployee` where user_id = '{}' limit 1".format(frappe.session.user)
    data = frappe.db.sql(sql, as_dict=1)
    if data:
        position = data[0].get("position")
        employee_id = data[0].get("name")
        phone_number = data[0].get("phone_number")
        address = data[0].get("address")
        photo = data[0].get("photo")
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
            "photo":photo,
            "phone_number":phone_number,
            "address":address,
            "name":frappe.session.user,
            "position":position,
            "token": base64.b64encode(str("{}:{}".format(user.api_key,api_generate)).encode("utf-8")).decode('utf-8'),
            "employee_id":employee_id,
            "home_page":home_page,
           

    }
