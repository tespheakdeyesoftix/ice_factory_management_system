import frappe
import base64
from frappe import _
import json


@frappe.whitelist(allow_guest=True)
def get_boldreport_setting():
    settings = frappe.db.get_value("Business Information",None,["server_report_url","report_server_token"], as_dict=True)   
    return {"boldreport_url":settings.server_report_url,"boldreport_authorize":settings.report_server_token}