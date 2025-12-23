<template>
    
  
    <Splitter style="height: 95vh">
    <SplitterPanel class="flex items-center justify-center"  :size="20"> 
        <ComReportList @onSelect="onPreviewReport"/>
    </SplitterPanel>
    <SplitterPanel class="flex items-center justify-center"  :size="80"> 

        <div style="height:90vh" id="main_server_report_viewer_backend" class="flex align-items-center justify-content-center">
            <div v-if="!selectedReport">
             <div class="empty-state">
    <div class="empty-icon">
        <i class="pi pi-file" style="font-size: 3.5rem"></i>
    </div>
    <h2>សូមជ្រើសរើសរបាយកាណ៍</h2>
    <p>ជ្រើសរើសរបាយកាណ៍នៅក្នុងតារាងខាងឆ្វេងដើម្បីមើលលម្អិត</p>
</div>


            </div>
             
                 </div>

    </SplitterPanel>
</Splitter>
</template>
<script setup>
import {ref,onMounted} from 'vue';
import Button from 'primevue/button';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import ComReportList from "@/views/server-report/ComReportList.vue"
import 'primeicons/primeicons.css'
const selectedReport = ref()
const frappe = window.parent.frappe;
function onPreviewReport(p){
 
    selectedReport.value = p
    let report_params = [
        {name: 'printed_by', values: [frappe.session.user_fullname] },
        {name: 'username', values: [frappe.session.user] },
        {name: 'start_date', values: ['2025-01-01'] },
        {name: 'end_date', values: ['2025-01-31'] },
    ] 

    //get more default fitler from report doc
    if(p.default_filter_options){
       report_params = [...report_params, ...app.getServerReportDefaultFilter(JSON.parse(p.default_filter_options))]
   }

 
   
    $("#main_server_report_viewer_backend").boldReportViewer({
        reportServerUrl:app.setting.server_report_url,
        reportServiceUrl: app.setting.report_service_url,
        reportPath: selectedReport.value.report_url,
        serviceAuthorizationToken: app.setting.report_server_token,
        parameters: report_params,
        printMode:true,
        zoomFactor: 1,
        enableViewState: true,  // Enables the Save View feature
    toolbarSettings: {
        items: ej.ReportViewer.ToolbarItems.All,
        showSaveView: true,  // Shows Save View button on the toolbar
        showViewList: true,  // Enables selecting a saved view
    },
        reportLoaded: function(event) {
            
          
        }
    });
  
}

onMounted( async ()=>{
     
 })
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh; /* full screen */
    text-align: center;
    color: #6b7280;
}

.empty-icon {
    font-size: 64px;
    color: #9ca3af;
    margin-bottom: 8px;
}

.empty-state h2 {
    font-size: 20px;
    font-weight: 600;
    margin: 0px;
    color: #374151;
}

.empty-state p {
    font-size: 14px;
    margin: 0px;
}

</style>