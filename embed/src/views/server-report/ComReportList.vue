<template>
 <Accordion :value="0">
    <AccordionPanel :value="index" v-for="(rpt,index) in reportList?.filter(r=>!r.parent_system_report)" :key="index">
        <AccordionHeader>{{ rpt.report_title }}</AccordionHeader>
        <AccordionContent>
            <Menu  :model="reportList.filter(x=>x.parent_system_report == rpt.name)" >
                <template #item="{ item, props }">
        <a v-ripple class="flex items-center" style="cursor: pointer; display: block; padding-left: 10px;" @click="onViewReport(item)">
            <span class="pi pi-plus" />
            <span>{{ item.report_title }}</span>
        </a>
    </template>
            </Menu>
        </AccordionContent>
    </AccordionPanel>
     
</Accordion>
    </template>
    <script setup>
    import { onMounted, ref } from 'vue';
 
import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

import Menu from 'primevue/menu';

    const reportList = ref()
    const emit= defineEmits()
    onMounted(async ()=>{
       
        const res = await app.getDocList("System Report",{
            fields:["name","report_title","report_url","parent_system_report","default_filter_options"],
            filters:[["is_backend_report","=",1],["show_in_report_list","=",1]],
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
    
    
    function onViewReport(r){
        
        emit("onSelect",r)
    }
    
    </script>