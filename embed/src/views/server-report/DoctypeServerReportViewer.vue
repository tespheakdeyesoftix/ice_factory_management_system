<template>
    <div>
       <div v-if="!loading">
<Splitter style="height: 98vh" v-if="reportList.length>0">
         
                <SplitterPanel class="flex items-center justify-center" :size="20" v-if="reportList.length>1">
                    <Menu :model="reportList" style="margin: 10px;">
                        <template #item="{ item, props }">
                            <a v-ripple class="flex items-center"
                                style="cursor: pointer; display: block; padding-left: 10px;"
                                @click="onPreviewReport(item)">
                                <span class="pi pi-plus" />
                                <span>{{ item.report_title }}</span>
                            </a>
                        </template>
                    </Menu>
                </SplitterPanel>
                <SplitterPanel class="flex items-center justify-center" :size="80">
                    <div style="height:98vh" id="doctype_server_report_viewer"
                        class="flex align-items-center justify-content-center">
                        <div v-if="!selectedReport">
                            Please select a report to view your report.
                        </div>

                    </div>

                </SplitterPanel>
           
            
 
        </Splitter>
        <div v-else>
            There's no report report for this document.
        </div>
       </div>
        
        <div v-else>

            Loading...
        </div>
     
    </div>

</template>
<script setup>
import { ref, onMounted } from 'vue';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import { useRoute } from 'vue-router'
import Menu from 'primevue/menu';
const loading = ref(true)
const route = useRoute()
const reportList = ref([])
const selectedReport = ref(null)


async function getReportList() {

    const res = await app.getDocList("System Report", {
        fields: ["name", "report_title", "report_url", "parent_system_report", "default_filter_options"],
        filters: [["is_doctype_report", "=", 1], ["show_in_report_list", "=", 1], ["doctype_name", "=", route.query.doctype]],
        limit: 10000,
        orderBy: {
            field: "sort_order",
            order: "asc"
        }
    })
    if (res.data) {
        reportList.value = res.data

    }

    loading.value = false;

}
function onPreviewReport(rpt) {
selectedReport.value = rpt;

    let report_params = [
        { name: 'printed_by', values: [app.user?.full_name || "Administrator"] },
        { name: 'username', values: [app.user?.name || "Administrator"] },
        { name: 'id', values: [route.query.docname] },
        { name: 'start_date', values: ['2025-01-01'] },
        { name: 'end_date', values: ['2025-01-31'] },
    ]

    //get more default fitler from report doc
    if (rpt.default_filter_options) {
        report_params = [...report_params, ...app.getServerReportDefaultFilter(JSON.parse(rpt.default_filter_options))]
    }



    $("#doctype_server_report_viewer").boldReportViewer({
        reportServerUrl: app.setting.server_report_url,
        reportServiceUrl: app.setting.report_service_url,
        reportPath: rpt.report_url,
        serviceAuthorizationToken: app.setting.report_server_token,
        parameters: report_params,
        printMode: true,
        zoomFactor: 1.25,
        enableViewState: true,  // Enables the Save View feature
        toolbarSettings: {
            items: ej.ReportViewer.ToolbarItems.All,
            showSaveView: true,  // Shows Save View button on the toolbar
            showViewList: true,  // Enables selecting a saved view
        },
        reportLoaded: function (event) {


        }
    });

}

onMounted(async () => {
    await getReportList()
    if (reportList.value.length > 0) {
      
        if(route.query.report_name){
            const report = reportList.value.find(x=>x.name == route.query.report_name)
            if(report){
            onPreviewReport(report)    
            return;
            }
        }

            onPreviewReport(reportList.value[0])
        

    }

})
</script>
<style>
html,
body {
    margin: 0;
    padding: 0;
}
</style>