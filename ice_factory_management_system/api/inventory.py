import frappe

def add_inventory_transaction(doc):
    doc = frappe.get_doc(doc)
    doc.insert(ignore_permissions=True)

