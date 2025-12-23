<template>
     <Accordion :value="0">
    <AccordionPanel :value="index" v-for="(rpt,index) in reportList?.filter(r=>!r.parent_system_report)" :key="index" >
        <AccordionHeader>{{ rpt.report_title }}</AccordionHeader>
        <AccordionContent class="acc-content">
 <Listbox v-model="selectedReport" 
 :options="reportList.filter(x=>x.parent_system_report == rpt.name)" optionLabel="report_title" class="w-full md:w-56" 
   :scrollHeight="null"
 @change="onViewReport" />
            </AccordionContent>
            </AccordionPanel>
        </Accordion>
         
    </template>
    <script setup>
    import { onMounted, ref } from 'vue';
 
import Listbox from 'primevue/listbox';

import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

 

    const reportList = ref()
    const emit= defineEmits()
    const selectedReport = ref()

    onMounted(async ()=>{
       
        const res = await app.getDocList("System Report",{
            fields:["name","report_title","report_url","parent_system_report","default_filter_options"],
            filters:[
                ["is_backend_report","=",1],["show_in_report_list","=",1],
               
            ],
            orFilters:[
                 ["Has Desktop Page","desktop_page","=",localStorage.getItem("current_page")],
                 ["Has Desktop Page","desktop_page","is","not set"]
            ],
            limit:10000,
            orderBy:{
                field:"sort_order",
                order:"asc"
            }
        })
        if(res.data){
          
            reportList.value = res.data
        }
        
    })
    
    
    function onViewReport(){
        console.log(selectedReport.value)
        emit("onSelect",selectedReport.value)
    }
    
    </script>
    <style scoped>
        .p-listbox{border: none!important; margin: 0!important;}
        .p-accordionheader{padding: 6px 10px!important;}
  
    .p-accordioncontent {
  --p-accordion-content-padding: 0 !important;
}
.p-listbox{
        --p-listbox-option-padding: 4px 8px!important;
}
 
.p-listbox .p-listbox-option {
   border-bottom: solid 1px #ebebeb !important;
}

 
    </style>