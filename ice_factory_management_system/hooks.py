app_name = "ice_factory_management_system"
app_title = "Ice Factory Management System"
app_publisher = "Tes Pheakdey"
app_description = "Manage Ice Factory"
app_email = "pheakdey.micronet@gmail.com"
app_license = "mit"
# required_apps = []

add_to_apps_screen = [
	{
		"name": "ice_factory_management_system",
		"logo": "/assets/frappe/images/frappe-framework-logo.svg",
		"title": "ICE Factory Management",
		"route": "/app",
		"has_permission": "ice_factory_management_system.api.permission.has_app_permission"
	}
]



# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = ["/assets/ice_factory_management_system/css/ice_factory_management_system.css"]
app_include_js = ["/assets/ice_factory_management_system/js/ice_factory_management_system.js"]

# include js, css files in header of web template
# web_include_css = "/assets/ice_factory_management_system/css/ice_factory_management_system.css"
# web_include_js = "/assets/ice_factory_management_system/js/ice_factory_management_system.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ice_factory_management_system/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
page_js = {"print-report-server" : "/assets/ice_factory_management_system/js/page.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {
    "doctype" : "ice_factory_management_system/public/js/sale_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ice_factory_management_system/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "ice_factory_management_system.utils.jinja_methods",
#	"filters": "ice_factory_management_system.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ice_factory_management_system.install.before_install"
# after_install = "ice_factory_management_system.install.after_install"


before_migrate =[
    
]

after_migrate = [
    "ice_factory_management_system.store_procedures.execute.execute",
    "ice_factory_management_system.api.permission.disable_frappe_desktop"
]
 

# Uninstallation
# ------------

# before_uninstall = "ice_factory_management_system.uninstall.before_uninstall"
# after_uninstall = "ice_factory_management_system.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ice_factory_management_system.utils.before_app_install"
# after_app_install = "ice_factory_management_system.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ice_factory_management_system.utils.before_app_uninstall"
# after_app_uninstall = "ice_factory_management_system.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ice_factory_management_system.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Sale": "ice_factory_management_system.selling_ifms.doctype.sale.sale.query_permission",
	
}
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Payment Type": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Chart of Account": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Stock Location": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Outlet": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Customer": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Product": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Block Ice Produce Grid": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	"Tube Ice Machine": {"on_update": "ice_factory_management_system.api.utils.clear_cache"	},
	 
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"ice_factory_management_system.tasks.all"
#	],
#	"daily": [
#		"ice_factory_management_system.tasks.daily"
#	],
#	"hourly": [
#		"ice_factory_management_system.tasks.hourly"
#	],
#	"weekly": [
#		"ice_factory_management_system.tasks.weekly"
#	],
#	"monthly": [
#		"ice_factory_management_system.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "ice_factory_management_system.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ice_factory_management_system.event.get_events"
# }
#

on_login = "ice_factory_management_system.api.utils.on_login"

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ice_factory_management_system.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ice_factory_management_system.utils.before_request"]
# after_request = ["ice_factory_management_system.utils.after_request"]

# Job Events
# ----------
# before_job = ["ice_factory_management_system.utils.before_job"]
# after_job = ["ice_factory_management_system.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ice_factory_management_system.auth.validate"
# ]

fixtures = [
	{"dt": "Custom Field"},
	{"dt": "HTML Template"},
	{"dt": "Custom HTML Block"},
	{
        "dt": "Workflow State",
        "filters": [
            ["custom_is_standard", "=", 1]
        ]
    }
	 
]


website_route_rules = [
	{'from_route': '/embed/<path:app_path>', 'to_route': 'embed'},
	{'from_route': '/block-ice', 'to_route': '/me'},

	# {"from_route": "/profile", "to_route": "me"},
	]
 
