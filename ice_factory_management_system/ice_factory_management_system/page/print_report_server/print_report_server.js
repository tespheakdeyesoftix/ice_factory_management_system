frappe.pages["print-report-server"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
	});

	let print_view = new frappe.ui.form.PrintView(wrapper);

	$(wrapper).bind("show", () => {
		const route = frappe.get_route();
		const doctype = route[1];
		const docname = route.slice(2).join("/");
		if (!frappe.route_options || !frappe.route_options.frm) {
			frappe.model.with_doc(doctype, docname, () => {
				let frm = { doctype: doctype, docname: docname };
				frm.doc = frappe.get_doc(doctype, docname);
				frappe.model.with_doctype(doctype, () => {
					frm.meta = frappe.get_meta(route[1]);
					print_view.show(frm);
				});
			});
		} else {
			print_view.frm = frappe.route_options.frm.doctype
				? frappe.route_options.frm
				: frappe.route_options.frm.frm;
			frappe.route_options.frm = null;
			print_view.show(print_view.frm);
		}
	});
};

frappe.ui.form.PrintView = class {
	constructor(wrapper) {
		this.wrapper = $(wrapper);
		this.page = wrapper.page;
		this.make();
	}

	make() {
		this.print_wrapper = this.page.main.empty().html(
			`<div class="server-print-preview-wrapper"><div class="print-preview">
				hello this is print preview wrapper class
			</div>
			 
		</div>
		
		`
		);

		this.print_settings = frappe.model.get_doc(":Print Settings", "Print Settings");

		this.setup_toolbar();
		this.setup_sidebar();
		this.setup_keyboard_shortcuts();
	}

	set_title() {
		this.page.set_title(this.frm.docname);
	}

	setup_toolbar() {
		this.page.set_primary_action(__("Print"), () => this.printit(), "printer");

		this.page.add_button(__("Full Page"), () => this.render_page("/printview?"), {
			icon: "full-page",
		});

		this.page.add_button(__("PDF"), () => this.render_pdf(), { icon: "small-file" });

		this.page.add_button(__("Refresh"), () => this.refresh_print_format(), {
			icon: "refresh",
		});

		this.page.add_action_icon(
			"es-line-filetype",
			() => {
				this.go_to_form_view();
			},
			"",
			__("Form")
		);
	}

	setup_sidebar() {
		this.sidebar = this.page.sidebar.addClass("print-preview-sidebar");

		this.print_format_selector = this.add_sidebar_item({
			fieldtype: "Link",
			fieldname: "print_format",
			options: "Print Format",
			label: __("Print Format"),
			get_query: () => {
				return { filters: { doc_type: this.frm.doctype } };
			},
			change: () => this.refresh_print_format(),
		}).$input;

		this.language_selector = this.add_sidebar_item({
			fieldtype: "Link",
			fieldname: "language",
			label: __("Language"),
			options: "Language",
			change: () => {
				this.set_user_lang();
				this.preview();
			},
		}).$input;

		let description = "";
		if (!cint(this.print_settings.repeat_header_footer)) {
			description =
				"<div class='form-message yellow p-3 mt-3'>" +
				__("Footer might not be visible as {0} option is disabled</div>", [
					`<a href="/app/print-settings/Print Settings">${__(
						"Repeat Header and Footer"
					)}</a>`,
				]);
		}
		const print_view = this;
		this.letterhead_selector = this.add_sidebar_item({
			fieldtype: "Link",
			fieldname: "letterhead",
			options: "Letter Head",
			label: __("Letter Head"),
			description: description,
			change: function () {
				this.set_description(this.get_value() ? description : "");
				print_view.preview();
			},
		}).$input;
		this.sidebar_dynamic_section = $(`<div class="dynamic-settings"></div>`).appendTo(
			this.sidebar
		);
	}

	add_sidebar_item(df, is_dynamic) {
		if (df.fieldtype == "Select") {
			df.input_class = "btn btn-default btn-sm text-left";
		}

		let field = frappe.ui.form.make_control({
			df: df,
			parent: is_dynamic ? this.sidebar_dynamic_section : this.sidebar,
			render_input: 1,
		});

		if (df.default != null) {
			field.set_input(df.default);
		}

		return field;
	}


	show(frm) {
		this.frm = frm;
		this.set_title();
		this.set_breadcrumbs();

		let tasks = [
			this.set_default_print_format,
			this.set_default_print_language,

			this.preview,
		].map((fn) => fn.bind(this));


		return frappe.run_serially(tasks);
	}

	set_breadcrumbs() {
		frappe.breadcrumbs.add(this.frm.meta.module, this.frm.doctype);
	}


	add_settings_to_sidebar(settings) {
		for (let df of settings) {
			let field = this.add_sidebar_item(
				{
					...df,
					change: () => {
						const val = field.get_value();
						this.additional_settings[field.df.fieldname] = val;
						this.preview();
					},
				},
				true
			);
		}
	}



	refresh_print_format() {
		this.set_default_print_language();
		this.toggle_raw_printing();
		this.preview();
	}




	setup_keyboard_shortcuts() {
		this.wrapper.find(".print-toolbar a.btn-default").each((i, el) => {
			frappe.ui.keys.get_shortcut_group(this.frm.page).add($(el));
		});
	}

	set_default_letterhead() {
		if (this.frm.doc.letter_head) {
			this.letterhead_selector.val(this.frm.doc.letter_head);
			return;
		}

		return frappe.db
			.get_value("Letter Head", { disabled: 0, is_default: 1 }, "name")
			.then(({ message }) => this.letterhead_selector.val(message.name));
	}

	set_user_lang() {
		this.lang_code = this.language_selector.val();
	}

	set_default_print_language() {
		let print_format = this.get_print_format();
		this.lang_code =
			this.frm.doc.language || print_format.default_print_language || frappe.boot.lang;
		this.language_selector.val(this.lang_code);
	}

	toggle_raw_printing() {
		const is_raw_printing = this.is_raw_printing();
		this.wrapper.find(".btn-print-preview").toggle(!is_raw_printing);
		this.wrapper.find(".btn-download-pdf").toggle(!is_raw_printing);
	}

	preview() {
		let print_format = this.get_print_format();
		if (print_format.print_format_builder_beta) {
			this.print_wrapper.find(".print-preview-wrapper").hide();
			this.print_wrapper.find(".preview-beta-wrapper").show();
			this.preview_beta();
			return;
		}

		let $print_viewer_el = this.print_wrapper.find(".server-print-preview-wrapper")
		$print_viewer_el.show();
		$print_viewer_el.html("")
		const bold_report_setting = {
			server_report_url: "http://175.100.97.220:51269/reporting/api/site/ice-factory-management-report",
			report_service_url: "http://175.100.97.220:51269/reporting/reportservice/api/Viewer",
			report_server_token: "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBoZWFrZGV5Lm1pY3JvbmV0QGdtYWlsLmNvbSIsIm5hbWVpZCI6IjIiLCJ1bmlxdWVfbmFtZSI6IjhjNzEzMjQ1LWY0YzItNGE4Ny1hMTI5LTdhYjEyZDg5OWM4NSIsIklQIjoiMTkyLjE2OC4xMC4xIiwiaXNzdWVkX2RhdGUiOiIxNzU1Nzc0Njg5IiwibmJmIjoxNzU1Nzc0Njg5LCJleHAiOjE3NjYyNTAwMDAsImlhdCI6MTc1NTc3NDY4OSwiaXNzIjoiaHR0cDovLzE3NS4xMDAuOTcuMjIwOjUxMjY5L3JlcG9ydGluZy9zaXRlL2ljZS1mYWN0b3J5LW1hbmFnZW1lbnQtcmVwb3J0IiwiYXVkIjoiaHR0cDovLzE3NS4xMDAuOTcuMjIwOjUxMjY5L3JlcG9ydGluZy9zaXRlL2ljZS1mYWN0b3J5LW1hbmFnZW1lbnQtcmVwb3J0In0.SdmkOKdWktZAbdbkzZW-LX2uJfIvUcvE3yRc-UhPsiU",
			report_url: "/Sales/rptReceiptInvoice"
		}
		let report_params = [
			{name: 'printed_by', values: ["Admin"] },
			{name: 'username', values: ["Administrator"] },
			{name: 'id', values: ['SINV2025-0006'] },
		] 
		
		 
		$print_viewer_el.boldReportViewer({
			reportServerUrl: bold_report_setting.server_report_url,
			reportServiceUrl: bold_report_setting.report_service_url,
			reportPath: bold_report_setting.report_url,
			serviceAuthorizationToken: bold_report_setting.report_server_token,
			parameters:report_params,
			printMode: true,
			zoomFactor: 1.25,
			enableViewState: true,
			toolbarSettings: {
				items: ej.ReportViewer.ToolbarItems.All,
				showSaveView: true,
				showViewList: true,
			}
		});


	}

	preview_beta() {
		let print_format = this.get_print_format();
		const iframe = this.print_wrapper.find(".preview-beta-wrapper iframe");
		let params = new URLSearchParams({
			doctype: this.frm.doc.doctype,
			name: this.frm.doc.name,
			print_format: print_format.name,
		});
		let letterhead = this.get_letterhead();
		if (letterhead) {
			params.append("letterhead", letterhead);
		}
		iframe.prop("src", `/printpreview?${params.toString()}`);
	}

	setup_print_format_dom(out, $print_format) {
		this.print_wrapper.find(".print-format-skeleton").remove();
		let base_url = frappe.urllib.get_base_url();
		let print_css = frappe.assets.bundled_asset(
			"print.bundle.css",
			frappe.utils.is_rtl(this.lang_code)
		);
		this.$print_format_body
			.find("html")
			.attr("dir", frappe.utils.is_rtl(this.lang_code) ? "rtl" : "ltr");
		this.$print_format_body.find("html").attr("lang", this.lang_code);
		this.$print_format_body.find("head").html(
			`<style type="text/css">${out.style}</style>
			<link href="${base_url}${print_css}" rel="stylesheet">`
		);

		this.$print_format_body
			.find("body")
			.html(`<div class="print-format print-format-preview">${out.html}</div>`);

		this.show_footer();

		this.$print_format_body.find(".print-format").css({
			display: "flex",
			flexDirection: "column",
		});

		this.$print_format_body.find(".page-break").css({
			display: "flex",
			"flex-direction": "column",
			flex: "1",
		});

		setTimeout(() => {
			$print_format.height(this.$print_format_body.find(".print-format").outerHeight());
		}, 500);
	}

	hide() {
		if (this.frm.setup_done && this.frm.page.current_view_name === "print") {
			this.frm.page.set_view(
				this.frm.page.previous_view_name === "print"
					? "main"
					: this.frm.page.previous_view_name || "main"
			);
		}
	}

	go_to_form_view() {
		frappe.route_options = {
			frm: this,
		};
		frappe.set_route("Form", this.frm.doctype, this.frm.docname);
	}

	show_footer() {
		// footer is hidden by default as reqd by pdf generation
		// simple hack to show it in print preview

		this.$print_format_body.find("#footer-html").attr(
			"style",
			`
			display: block !important;
			order: 1;
			margin-top: auto;
			padding-top: var(--padding-xl)
		`
		);
	}


	render_page(method, printit = false) {
		let w = window.open(
			frappe.urllib.get_full_url(
				method +
				"doctype=" +
				encodeURIComponent(this.frm.doc.doctype) +
				"&name=" +
				encodeURIComponent(this.frm.doc.name) +
				(printit ? "&trigger_print=1" : "") +
				"&format=" +
				encodeURIComponent(this.selected_format()) +
				"&no_letterhead=" +
				(this.with_letterhead() ? "0" : "1") +
				"&letterhead=" +
				encodeURIComponent(this.get_letterhead()) +
				"&settings=" +
				encodeURIComponent(JSON.stringify(this.additional_settings)) +
				(this.lang_code ? "&_lang=" + this.lang_code : "")
			)
		);
		if (!w) {
			frappe.msgprint(__("Please enable pop-ups"));
			return;
		}
	}

	get_print_html(callback) {
		let print_format = this.get_print_format();
		if (print_format.raw_printing) {
			callback({
				html: this.get_no_preview_html(),
			});
			return;
		}
		if (this._req) {
			this._req.abort();
		}
		this._req = frappe.call({
			method: "frappe.www.printview.get_html_and_style",
			args: {
				doc: this.frm.doc,
				print_format: this.selected_format(),
				no_letterhead: !this.with_letterhead() ? 1 : 0,
				letterhead: this.get_letterhead(),
				settings: this.additional_settings,
				_lang: this.lang_code,
			},
			callback: function (r) {
				if (!r.exc) {
					callback(r.message);
				}
			},
		});
	}

	get_letterhead() {
		return this.letterhead_selector.val() || __("No Letterhead");
	}

	get_no_preview_html() {
		return `<div class="text-muted text-center" style="font-size: 1.2em;">
			${__("No Preview Available")}
		</div>`;
	}

	get_raw_commands(callback) {
		// fetches rendered raw commands from the server for the current print format.
		frappe.call({
			method: "frappe.www.printview.get_rendered_raw_commands",
			args: {
				doc: this.frm.doc,
				print_format: this.selected_format(),
				_lang: this.lang_code,
			},
			callback: function (r) {
				if (!r.exc) {
					callback(r.message);
				}
			},
		});
	}

	get_mapped_printer() {
		// returns a list of "print format: printer" mapping filtered by the current print format
		let print_format_printer_map = this.get_print_format_printer_map();
		if (print_format_printer_map[this.frm.doctype]) {
			return print_format_printer_map[this.frm.doctype].filter(
				(printer_map) => printer_map.print_format == this.selected_format()
			);
		} else {
			return [];
		}
	}

	get_print_format_printer_map() {
		// returns the whole object "print_format_printer_map" stored in the localStorage.
		try {
			return JSON.parse(localStorage.print_format_printer_map);
		} catch (e) {
			return {};
		}
	}

	set_default_print_format() {
		if (
			frappe.meta
				.get_print_formats(this.frm.doctype)
				.includes(this.print_format_selector.val()) ||
			!this.frm.meta.default_print_format
		)
			return;

		this.print_format_selector.empty();
		this.print_format_selector.val(this.frm.meta.default_print_format);
	}

	selected_format() {
		return this.print_format_selector.val() || "Standard";
	}

	is_raw_printing(format) {
		return this.get_print_format(format).raw_printing === 1;
	}

	get_print_format(format) {
		let print_format = {};
		if (!format) {
			format = this.selected_format();
		}

		if (locals["Print Format"] && locals["Print Format"][format]) {
			print_format = locals["Print Format"][format];
		}

		return print_format;
	}

	with_letterhead() {
		return cint(this.get_letterhead() !== __("No Letterhead"));
	}

	set_style(style) {
		frappe.dom.set_style(style || frappe.boot.print_css, "print-style");
	}

	printer_setting_dialog() {
		// dialog for the Printer Settings
		this.print_format_printer_map = this.get_print_format_printer_map();
		this.data = this.print_format_printer_map[this.frm.doctype] || [];
		this.printer_list = [];
		frappe.ui.form.qz_get_printer_list().then((data) => {
			this.printer_list = data;
			const dialog = new frappe.ui.Dialog({
				title: __("Printer Settings"),
				fields: [
					{
						fieldtype: "Section Break",
					},
					{
						fieldname: "printer_mapping",
						fieldtype: "Table",
						label: __("Printer Mapping"),
						in_place_edit: true,
						data: this.data,
						get_data: () => {
							return this.data;
						},
						fields: [
							{
								fieldtype: "Select",
								fieldname: "print_format",
								default: 0,
								options: frappe.meta.get_print_formats(this.frm.doctype),
								read_only: 0,
								in_list_view: 1,
								label: __("Print Format"),
							},
							{
								fieldtype: "Select",
								fieldname: "printer",
								default: 0,
								options: this.printer_list,
								read_only: 0,
								in_list_view: 1,
								label: __("Printer"),
							},
						],
					},
				],
				primary_action: () => {
					let printer_mapping = dialog.get_values()["printer_mapping"];
					if (printer_mapping && printer_mapping.length) {
						let print_format_list = printer_mapping.map((a) => a.print_format);
						let has_duplicate = print_format_list.some(
							(item, idx) => print_format_list.indexOf(item) != idx
						);
						if (has_duplicate)
							frappe.throw(
								__(
									"Cannot have multiple printers mapped to a single print format."
								)
							);
					} else {
						printer_mapping = [];
					}
					dialog.print_format_printer_map = this.get_print_format_printer_map();
					dialog.print_format_printer_map[this.frm.doctype] = printer_mapping;
					localStorage.print_format_printer_map = JSON.stringify(
						dialog.print_format_printer_map
					);
					dialog.hide();
				},
				primary_action_label: __("Save"),
			});
			dialog.show();
			if (!(this.printer_list && this.printer_list.length)) {
				frappe.throw(__("No Printer is Available."));
			}
		});
	}
};
