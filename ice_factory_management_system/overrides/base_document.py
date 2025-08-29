
import frappe
from frappe.model.document import Document
from frappe import _
from ice_factory_management_system.api.utils import get_previous_closed_date
class BaseDocument(Document):
  def on_update(self):
      frappe.msgprint("check prevent edit delete record from process transaction in overrides/base_documenbt.py")
  
  def on_submit(self):
    pass

  def before_cancel(self):
    #  frappe.throw("why u canncel me")
    pass