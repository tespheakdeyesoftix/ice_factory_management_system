// let hasRendered = false; // Flag to prevent multiple runs
// function getTemplate(path) {
//     return new Promise((resolve, reject) => {
//         $.get(path)
//             .done((template) => resolve(template))
//             .fail((err) => reject(err));
//     });
// }


// async function renderMyDesktop() {
    

//     // Define context
//     const context = {
//         title: "Frappe Card",
//         description: "This card is rendered using frappe.render_template"
//     };
//     const template = await getTemplate("/assets/ice_factory_management_system/js/templates/my_desktop.html")

//     const html = frappe.render_template(template, context);
//      $('.desktop-container').html(html);

//      setTimeout(() => {
//         let awesome_bar = new frappe.search.AwesomeBar();
//         awesome_bar.setup("#my-desktop-navbar-modal-search")
//      }, 1000);
 
// }




// // Observe body attribute for page completion
// const observer = new MutationObserver((mutationsList, observer) => {
//     if (hasRendered) return; // Prevent multiple runs

//     for (let mutation of mutationsList) {
//         if (mutation.type === 'attributes' && mutation.attributeName === 'data-ajax-state') {
//             const status = document.body.getAttribute('data-ajax-state');
//             if (status === 'complete') {
//                 hasRendered = true; // Mark as rendered
//                 renderMyDesktop();

//                 observer.disconnect(); // Stop observing
//                 break;
//             }
//         }
//     }
// });

// // Start observing the body for attribute changes
// observer.observe(document.body, { attributes: true });
