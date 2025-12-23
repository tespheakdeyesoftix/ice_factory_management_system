// Copyright (c) 2025, Tes Pheakdey and contributors
// For license information, please see license.txt
 
frappe.ui.form.on("Customer", {
    onload: function(frm) {
        if (frm.is_new()) {
            frm.add_child('product_prices', {});
            frm.refresh_field('product_prices');
        }else {
            
        }

        frm.set_query("product_code", "product_prices", function (doc, cdt, cdn) {
            return {
                "filters": {
                    "enabled": 1,
                    "name":["not in",doc.product_prices.map(x=>x.product_code)]
                },
            };
        });

        
    },
    refresh(frm){
    frm.dashboard.clear_headline();
       addCustomButton(frm);
       setIndicator(frm)
       renderCalender(frm)
       renderCalender(frm)
     
    
    },
     

    
    
});
function setIndicator(frm) {
    if (frm.is_new()) return;
    frappe.call({
        method: 'ice_factory_management_system.api.customer.get_customer_dashboard_data',
        args: {
            customer: frm.doc.name
        },
        callback: function (r) {
            if (!r.message) return;
            data = r.message.account_recivable
            // example: r.message.total_quantity
              frm.dashboard.add_indicator(
                __("Opening: {0}", [fmt_money(data.opening || 0)]),
                "blue"
            );

            frm.dashboard.add_indicator(
                __("Debit Amount: {0}", [fmt_money(data.debit_amount || 0)]),
                "blue"
            );

            frm.dashboard.add_indicator(
                __("Payment Amount: {0}", [fmt_money(data.payment_amount || 0)]),
                "green"
            );

            frm.dashboard.add_indicator(
                __("Write Off Amount: {0}", [fmt_money(data.write_off_amount || 0)]),
                "red"
            );
            frm.dashboard.add_indicator(
                __("Balance: {0}", [fmt_money(data.balance)]),
                "green"
            );
        }
    });
}



function addCustomButton(frm){
    frm.add_custom_button(__('Sale Invoices List'), function() {
            frappe.msgprint('view sale invoice list');

    }, __('View')); 
    
    frm.add_custom_button(__('Sale Payment List'), function() {
            frappe.msgprint('view sale invoice list');

    }, __('View')); 


    frm.add_custom_button('My Custom Action', function() {
            frappe.msgprint('Button clicked!');
        }, 'Actions'); 
}

 
function renderCalender(frm) {
    return
    if (frm._calendar_loaded) return;
    frm._calendar_loaded = true;
    frappe.require("fullcalendar.bundle.min.js", () => {
        const wrapper = frm.fields_dict.html_calendar.$wrapper;
        wrapper.empty();

        wrapper.append(`
            <div id="customer-calendar" style="min-height:600px;"></div>
        `);

        const calendarEl = document.getElementById("customer-calendar");
       const calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: "dayGridMonth",
                height: "auto",

                headerToolbar: {
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay"
                },

                 

                eventClick(info) {
                    frappe.set_route("Form", info.event.extendedProps.doctype, info.event.id);
                }
            });

            calendar.render();
    });

    // frappe.require("fullcalendar").then(() => {

    //     // Safety check
    //     if (!window.FullCalendar) {
    //         frappe.throw("FullCalendar failed to load");
    //     }

    //     const wrapper = frm.fields_dict.html_calendar.$wrapper;
    //     wrapper.empty();

    //     wrapper.append(`
    //         <div id="customer-calendar" style="min-height:600px;"></div>
    //     `);

    //     const calendarEl = document.getElementById("customer-calendar");

    //     frm.calendar = new FullCalendar.Calendar(calendarEl, {
    //         initialView: "dayGridMonth",
    //         height: 600,
    //         headerToolbar: {
    //             left: "prev,next today",
    //             center: "title",
    //             right: "dayGridMonth,timeGridWeek,timeGridDay"
    //         },
    //         events(info, success) {
    //             frappe.call({
    //                 method: "ice_factory_management_system.customer_relation.doctype.customer.customer.get_events",
    //                 args: {
    //                     start: info.startStr,
    //                     end: info.endStr,
    //                     customer: frm.doc.name
    //                 },
    //                 callback(r) {
    //                     success(r.message || []);
    //                 }
    //             });
    //         }
    //     });

    //     frm.calendar.render();
    // });
}
