from builtins import str
import frappe
import base64
from frappe import _
import json
from frappe.model.document import bulk_insert
from frappe.model.naming import make_autoname
from frappe.translate import print_language
import os
import frappe
from frappe.utils import get_files_path
from frappe.utils.file_manager import save_file
from ice_factory_management_system.api.pdf import get_pdf
@frappe.whitelist()
def create_pdf(doctype="Sale", name="SINV2025-0111"):
    html_template = """
    <html>
    <head>
        <style>
            html { padding: 0px; margin: 0px;}
            body { font-family: Arial, sans-serif; padding: 0px; margin: 0px;}
            h1 { color: #000; }
            table { width: 100%; border-collapse: collapse; margin-top: 0px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left;font-size:12px;}
            th { background-color: #f5f5f5; }
        </style>
    </head>
    <body>
    <div style="margin-top:-20px;">
    <img src="data:image/png;base64,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"/>
        <h1>Hello, {{ name }}</h1>
        <p>Here is your custom report:</p>

        <table>
            
                <tr>
                    <td>Item</td>
                    <td>Qty</td>
                    <td>Price</td>
                </tr>
          
           
                {% for item in items %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.qty }}</td>
                    <td>{{ item.price }}</td>
                </tr>
                {% endfor %}
         
        </table>
        </div>
    </body>
    </html>
    """

    context = {
        "name": "John Doe",
        "items": [
            {"name": "បាយឆាសាចគៅចានធំ<br/> ស្ករ 50%", "qty": 2, "price": "$3.00"},
            {"name": "បាយឆាសាចគៅចានធំ<br/> ស្ករ 50%", "qty": 2, "price": "$3.00"},
            {"name": "បាយឆាសាចគៅចានធំ<br/> ស្ករ 50%", "qty": 2, "price": "$3.00"},
            # {"name": "បាយឆាសាចគៅចានធំ<br/> ស្ករ 50%", "qty": 2, "price": "$3.00"},
            # {"name": "បាយឆាសាចគៅចានធំ<br/> ស្ករ 50%", "qty": 2, "price": "$3.00"},
            # {"name": "Banana", "qty": 5, "price": "$2.50"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"},
            # {"name": "Orange", "qty": 3, "price": "$4.00"}
        ]
    }

    rendered_html = frappe.render_template(html_template, context)
    pdf = get_pdf(rendered_html,
    options={
        "margin-top": "0mm",
        "margin-bottom": "0mm",
        "margin-left": "0mm",
        "margin-right": "0mm",
        "disable-smart-shrinking": None,
        "no-outline": None,
        "header-spacing": "0",
        "footer-spacing": "0",
        "print-media-type": None,
         "page-width": "80mm",          # width of the thermal receipt
        "page-height": "297mm"
    }
    )

    # frappe.local.response.filename = "custom_report.pdf"
    # frappe.local.response.filecontent = pdf
    # frappe.local.response.type = "download"


    pdf_base64 = base64.b64encode(pdf)
    return pdf_base64.decode()



def replace_format(string):    
    from datetime import datetime
    short_year = datetime.now().strftime("%y")
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    return string.replace('.', '').replace('YYYY', year).replace('yyyy', year).replace('YY', short_year).replace('yy', short_year).replace('MM', month).replace('#', '')

@frappe.whitelist()
def reset_sale_transaction(password):
    if password == "eposadmin@855855" and frappe.session.user == "Administrator":
        frappe.db.sql("delete from `tabGL Entry`")
        frappe.db.sql("delete from `tabSale`")
        frappe.db.sql("delete from `tabSale Products`")
        frappe.db.sql("delete from `tabSale Payment`")
        frappe.db.sql("delete from `tabBulk Sale Payment`")
        frappe.db.sql("delete from `tabBulk Sale`")
        frappe.db.sql("delete from `tabClosed Selling Date`")
        frappe.db.sql("delete from `tabClosed Selling Date Data`")
        frappe.db.sql("delete from `tabClosed Selling Date Items`")
        frappe.db.sql("delete from `tabStock In`")
        frappe.db.sql("delete from `tabStock In Products`")
        frappe.db.sql("delete from `tabJournal Entry`")

        doctypes = ["GL Entry","Sale","Sale Payment","Bulk Sale Payment","Closed Selling Date","Closed Selling Date Data","Stock In","Journal Entry"]
        for d in doctypes:   
            formats = ""        
            if d == "GL Entry":
                formats = "GLE.YYYY.-.#####"
            elif d == "Closed Selling Date Data":
                formats = "CSDD.YYYY.-.#####"
            else:
                formats =  frappe.get_meta(d).get_field("naming_series").options
            if formats:
                if "#" in formats:
                    format_text = replace_format(formats)
                    sql = "update `tabSeries` set current = 0 where name='{}'".format(format_text)
                    frappe.db.sql(sql)
        return "reset"
    else:
        return "wrong password"
 
def ensure_date(posting_date,creation):
    from datetime import datetime,date,time
    a = datetime.strptime(creation, "%Y-%m-%d %H:%M:%S.%f")
    now = time(a.hour, a.minute, a.second)
    if isinstance(posting_date, str):
        return  datetime.combine(datetime.strptime(posting_date, "%Y-%m-%d").date(), now)
    elif isinstance(posting_date, datetime):
        return posting_date
    elif isinstance(posting_date, date):
        return  datetime.combine(posting_date, now)
    else:
        return datetime.now()

@frappe.whitelist() 
def get_previous_closed_date(posting_date,creation,outlet):
 
    b = frappe.db.sql("select posting_date,creation from `tabClosed Selling Date` where docstatus=1 and outlet = '{0}' order by CONCAT(posting_date,' ',DATE_FORMAT(modified, '%H:%i:%s')) desc limit 1".format(outlet),as_dict=1)
 
    if len(b or []) > 0:
        posting_date =frappe.utils.getdate(ensure_date(str(posting_date),str(creation)))
        previous_closed_date = frappe.utils.getdate(ensure_date(str(b[0]["posting_date"]),str(b[0]["creation"])))


        if previous_closed_date >= posting_date:
            frappe.throw("អ្នកមិនធ្វើប្រតិបត្តិការនេះបានទេ។ ព្រោះថ្ងៃទី {} ត្រូបានបិទបញ្ជីររួចហើយ.".format(frappe.format(previous_closed_date,{"fieldtype":"Date"})))
    

@frappe.whitelist()
def get_currency_symbol(currency):
    symbol = frappe.get_cached_value("Currency", currency, "symbol")
    return symbol
 
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


    data["currency"] = frappe.get_cached_value("System Settings", None, "currency")
    data["currency_symbol"] = frappe.get_cached_value("Currency",data.get("currency"),"symbol")
    data["second_currency_symbol"] = frappe.get_cached_value("Currency",data.get("second_currency"),"symbol")
    
    # payment type
    payment_types = frappe.db.get_list("Payment Type",["name","currency","exchange_rate"])
    data["payment_types"] = payment_types    

    # get exchange rate
    exchange_rate = 1
    exchange_rate_data =  frappe.db.sql("select currency_exchange_rate from `tabExchange Rate` where from_currency=%(from_currency)s and to_currency =  %(to_currency)s and docstatus = 1 order by creation desc  limit 1",{"from_currency":data.get("currency"),"to_currency":data.get("second_currency")},as_dict = 1)
    if exchange_rate_data:
        from decimal import Decimal
        exchange_rate = Decimal( exchange_rate_data[0].get("currency_exchange_rate",1))

    data["exchange_rate"]  = exchange_rate
    data["exchange_rate_display"]  = exchange_rate if exchange_rate>1 else 1/exchange_rate
    return data
    

@frappe.whitelist(allow_guest=True)
def check_api_url(property_code,station_name,old_station_name):
    if not station_name:
        frappe.throw(_("Please enter your device name"))
        
    doc = frappe.get_cached_doc("Business Information",None)
    if doc.property_code ==  property_code:
        
        # check station
        if station_name != old_station_name:
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
    home_page = ""
    role_profile=""
    user = frappe.get_doc("User", frappe.session.user)
    

    sql = """
        select 
           *
        from `tabEmployee` 
        where 
            user_id = '{}' 
        limit 1
    """.format(frappe.session.user)

    data = frappe.db.sql(sql, as_dict=1)
    user_info={}
    
    if data:
        position = data[0].get("position")
        employee_id = data[0].get("name")
        phone_number = data[0].get("phone_number")
        address = data[0].get("address")
        photo = data[0].get("photo")
        home_page = data[0].get("default_frontend_home_page")

        role_profile = data[0].get("role_profile")
        user_info=data[0]

        

    api_generate = generate_keys(frappe.session.user)
    # get home_page 
    

    return {
            "username":user.username,
            "full_name":user.full_name,
            "role_profile":role_profile,
            "photo":photo,
            "phone_number":phone_number,
            "address":address,
            "name":frappe.session.user,
            "position":position,
            "token": base64.b64encode(str("{}:{}".format(user.api_key,api_generate)).encode("utf-8")).decode('utf-8'),
            "employee_id":employee_id,
            "home_page":home_page,
            "user_info":user_info
           

    }

@frappe.whitelist()
def on_login(login_manager):
    pass
    # from frappe.core.doctype.session_default_settings.session_default_settings import set_session_default_values
    # sql = "select default_outlet from `tabEmployee` where user_id = %(user_id)s"
    # data = frappe.db.sql(sql,{"user_id":login_manager.user},as_dict=1)
    # default_outlet = ""
    # if data:
    #     default_outlet = data[0]["default_outlet"]
    # if not  default_outlet:
    #     outlets = frappe.get_list("Outlet")
    #     if outlets:
    #         default_outlet = outlets[0].name
 
    # if default_outlet:
    #     set_session_default_values(
    #         {"outlet":default_outlet}
    #     )


@frappe.whitelist()
def getCurrentUser():
    return   frappe.get_cached_doc("User", frappe.session.user)   

def get_default_outlet():
    sql="select default_outlet from `tabEmployee` where user_id = %(user_id)s"
    data = frappe.db.sql(sql,{"user_id":frappe.session.user},as_dict = 1)
    if data:
        return data[0].get("default_outlet")
    return frappe.get_list("Outlet",pluck='name')[0]



def money_to_word(amount=7569556,currency="KHR"):
    amount = str(amount)
    if len(amount)>6:
        first_number = int(amount[:len(amount) - 6])


        return number_to_word(int(first_number)) + "លាន" + number_to_word(int(amount[-6:] )) + " " + ("រៀល" if currency=="KHR" else "ដុល្លា")
    else:
        return number_to_word(int(amount)) + " " + ("រៀល" if currency=="KHR" else "ដុល្លា")
    
def number_to_word(amount=7569556):
    
    khmer_digit = ["","មួយ","ពីរ","បី","បួន","ប្រាំ","ប្រាំមួយ","ប្រាំពីរ","ប្រាំបី","ប្រាំបួន"]
    khmer_unit = ["","ដប់","រយ","ពាន់","ម៉ឺន","សែន","លាន"]
    tens_words = ['', 'ដប់', 'ម្ភៃ', 'សាមសិប', 'សែសិប', 'ហាសិប', 'ហុកសិប', 'ចិតសិប', 'ប៉ែតសិប', 'កៅសិប']
    khmer_number = ""
    n = len(str(amount))
    for index, w in enumerate(str(amount)):
        n= n -1
        if n == 1: # we are at 10 word
            khmer_number +=tens_words[int(w)] 
        else:
            khmer_number = khmer_number + khmer_digit[int(w)] 
            
        if w !="0" and n>1:
            khmer_number = khmer_number + khmer_unit[n]

    return khmer_number
 

def clear_cache(doc, method):
    frappe.clear_document_cache(doc.doctype,doc.name)

@frappe.whitelist()
def add_audit_trail_log(data):
    if isinstance(data, list):
        for d in data:
            d["doctype"] = "Audit Trail Log"
            d["username"] = frappe.get_cached_value("User",frappe.session.user,"full_name")
            frappe.get_doc(d).insert(ignore_permissions=True)
    else:
        data["doctype"] = "Audit Trail Log"
        data["username"] = frappe.get_cached_value("User",frappe.session.user,"full_name")
        frappe.get_doc(data).insert(ignore_permissions=True)
    frappe.db.commit()
