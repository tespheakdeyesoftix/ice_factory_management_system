import frappe

def has_app_permission():
    if frappe.session.user == "Administrator":
        return True
    
    return True
@frappe.whitelist()
def desktop_icon_query_condition(user):
    return "`tabDesktop Icon`.app not in ('frappe')"


@frappe.whitelist()
def disable_frappe_desktop():
    frappe.db.sql("update `tabDesktop Icon` set standard = 0 where name in ('Productivity','Integrations')")
    frappe.db.commit()
    