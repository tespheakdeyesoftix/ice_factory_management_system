from frappe import _
import frappe

def get_data():
	 
	return {
		 
		"fieldname": "product_code",
		"transactions": [
			{"label":"","items": ["Sale"]},
			{"label":"","items": ["Purchase Order"]},
			{"label":"","items": ["Stock Entry"]},
			{"label":"","items": ["Stock Adjustment"]},
			{"label":"","items": ["Stock Location Products"]},
			{"label":"","items": ["Inventory Transactions"]},
			 
		],
	}