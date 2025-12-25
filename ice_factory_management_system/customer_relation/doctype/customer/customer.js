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
        window.loadCustomerCalenar = false;
        frm.dashboard.clear_headline();
        addCustomButton(frm);
        setIndicator(frm)
      
        if(window.location.hash == "#tab_customer_calendar")  {
            renderCalender(frm)
        } 
        $("#customer-tab_customer_calendar-tab").click(function(){
            renderCalender(frm)
        })
    
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


    frm.add_custom_button(__('Return Product'), async function() {
            const result = await frappe.borrow_product.onBulkReturnProduct({customer:frm.doc.name});
            if(result){
                frm.refresh();
            }
    }, 'Actions'); 
}



 
function renderCalender(frm) {
    if (!window.loadCustomerCalenar){
 frappe.require("calendar.bundle.js", () => {
            render_calendar(frm);
            window.loadCustomerCalenar = true;
        });
    }
  
   

        
}


function render_calendar(frm) {
    alert("load me")
    const wrapper = frm.fields_dict.html_calendar.$wrapper;
    wrapper.empty();

    const calEl = document.createElement('div');
    calEl.style.minHeight = '500px';
    wrapper.append(calEl);

    const today = frappe.datetime.get_today();

    const events = [
        { title: "Event 1", start: `${today}T09:00:00` },
        { title: "Event 2", start: `${today}T10:00:00` },
        { title: "Event 3", start: `${today}T11:00:00` },
        { title: "Event 4", start: `${today}T14:00:00` },
        { title: "Event 5", start: `${today}T16:00:00` }
    ];

    const calendar = new frappe.FullCalendar(calEl, {
        plugins: frappe.FullCalendar.Plugins,

        initialView: 'dayGridMonth',
        initialDate: today,

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },

        dayMaxEvents: 5,
        nowIndicator: true,
        editable: false,
        selectable: false,

        events: events,
        // events: {
        //     url: '/api/method/your_app.api.get_calendar_events',
        //     method: 'GET',
        //     failure() {
        //         frappe.msgprint(__('Failed to load calendar events'));
        //     }
        // },

         eventClick(info) {
            info.jsEvent.preventDefault();

            frappe.msgprint({
                title: __('Event Clicked'),
                message: `
                    <b>${info.event.title}</b><br>
                    Start: ${info.event.start}
                `,
                indicator: 'blue'
            });
 
        }
    });

    calendar.render();
}
