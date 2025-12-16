frappe.pages['my-order'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'My Orderss',
		single_column: true
	});
	alert(123)
	frappe.set_route('List', 'Sale');
}