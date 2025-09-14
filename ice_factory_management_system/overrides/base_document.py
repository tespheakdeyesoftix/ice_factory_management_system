
import frappe
from frappe.model.document import Document
from frappe import _
from ice_factory_management_system.api.utils import get_previous_closed_date
class BaseDocument(Document):
  # this method will raise on insert,save and submit
  def validate(self):
      frappe.msgprint("base doc run on validation")
      self.validate_close_date()

  
  def before_cancel(self):
    frappe.msgprint("base doc run on cancel")
    self.validate_close_date()

  def on_trash(self):
    frappe.msgprint("base doc run on cancel")
    self.validate_close_date()


  def validate_close_date(self):
    if frappe.db.exists("Closed Selling Date Doctype",{"closed_doctype":self.doctype}):
      
      get_previous_closed_date(self.posting_date, self.creation, self.outlet)
    
    

