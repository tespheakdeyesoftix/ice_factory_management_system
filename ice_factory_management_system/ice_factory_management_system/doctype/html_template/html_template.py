# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class HTMLTemplate(Document):
	pass

@frappe.whitelist()
def get_html_template(fields,doc):
	fields = json.loads(fields)
	doc= json.loads(doc)
	result = {}
	for f in fields:
		if frappe.db.exists("HTML Template",f):
		 
			template = frappe.get_cached_value("HTML Template", f,"template")
			if template:
				result[f] = frappe.render_template(template,{"doc":doc})
	return result

@frappe.whitelist()
def get_custom_sidebar_template(doc):
	doc= json.loads(doc)
	if frappe.db.exists("HTML Template",doc.get("doctype") +"_sidebar"):

		template_doc = frappe.get_cached_doc("HTML Template", doc.get("doctype")+"_sidebar")
		if template_doc.template:
			template = ""
			if template_doc.css:
				template = f"<style>{template_doc.css}</style>"
			template =template +  frappe.render_template(template_doc.template,{"doc":doc})
			return template
	return ""