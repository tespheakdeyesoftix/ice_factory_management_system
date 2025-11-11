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
 

def replace_format(string):    
    from datetime import datetime
    short_year = datetime.now().strftime("%y")
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    return string.replace('.', '').replace('YYYY', year).replace('yyyy', year).replace('YY', short_year).replace('yy', short_year).replace('MM', month).replace('#', '')

 
def submit_general_ledger_entry(docs,run_commit = True):
    def get_general_ledger_entry_record(docs):
        for d in docs:
            doc = frappe.get_doc(d)
            if doc.amount and not (doc.credit_amount or doc.debit_amount ):
                root_type = frappe.get_cached_value("Chart of Account",doc.account,"root_type")
                if root_type in ["Asset","Expenses"]:
                    if doc.amount>0:
                        doc.debit_amount = abs(doc.amount)
                    else:
                        doc.credit_amount = abs(doc.amount)
                else:
                    if doc.amount>0:
                        doc.credit_amount = abs(doc.amount)
                    else:
                        doc.debit_amount = abs(doc.amount)
            doc.name  = make_autoname("GLE.YYYY.-.#####")
            doc.docstatus = 1
            yield doc
    if run_commit:
        frappe.db.commit()

    bulk_insert("GL Entry", get_general_ledger_entry_record(docs=docs) , chunk_size=10000)
        
def cancel_general_ledger_entery(doctype,docname):
    filters = "where voucher_type='{}' and voucher_no='{}'".format(doctype,docname)
    if doctype == "Sale":
        sale_id = frappe.db.get_value(doctype, docname, 'id')
        filters = "where sale_id='{}'".format(sale_id)

    frappe.db.sql("update `tabGL Entry` set is_cancelled=1 {0}".format(filters))
    frappe.db.commit()
    
    sql = "select * from `tabGL Entry` {0}".format(filters)
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
                "party": r["party"],
                "is_cancelled":1,
            }
        docs.append(doc)
    submit_general_ledger_entry(docs)

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





