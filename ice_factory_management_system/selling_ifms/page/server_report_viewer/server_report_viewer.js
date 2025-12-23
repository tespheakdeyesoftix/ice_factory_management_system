frappe.pages['server-report-viewer'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Reports',
        single_column: true
    });

    // store page reference
    wrapper.page = page;
};

frappe.pages['server-report-viewer'].on_page_show = function (wrapper) {
    const page = wrapper.page;

    // clear old content
    page.main.empty();

    // re-render every time user enters this page
    $(frappe.render_template("server_report_viewer", {
        current_page: localStorage.getItem("curent_page")
    })).appendTo(page.main);

    
};
