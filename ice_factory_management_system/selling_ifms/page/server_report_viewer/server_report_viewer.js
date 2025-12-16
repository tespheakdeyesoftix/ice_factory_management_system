frappe.pages['server-report-viewer'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Reports',
		single_column: true
	});
 
	$(frappe.render_template("server_report_viewer")).appendTo(page.main);
	
	 
	 
}