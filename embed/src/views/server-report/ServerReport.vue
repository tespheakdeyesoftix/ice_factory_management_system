<template>
    
  
    <Splitter style="height: 90vh">
    <SplitterPanel class="flex items-center justify-center"  :size="20"> 
        <ComReportList @onSelect="onPreviewReport"/>
    </SplitterPanel>
    <SplitterPanel class="flex items-center justify-center"  :size="80"> 

        <div style="height:90vh" id="main_server_report_viewer_backend" class="flex align-items-center justify-content-center">
            <div v-if="!selectedReport">
             Please select a report to view your report.
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

const selectedReport = ref()

function onPreviewReport(p){
 
    selectedReport.value = p
    let report_params = [
        {name: 'printed_by', values: [app.user.full_name] },
        {name: 'username', values: [app.user.name] },
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
        zoomFactor: 1.25,
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