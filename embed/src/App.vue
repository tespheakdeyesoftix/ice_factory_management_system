<template>
	<div>
	 
		<router-view />
	</div>
</template>


<script setup>
import {onMounted} from "vue"
	onMounted(async()=>{
 
		const res = await app.getApi("utils.get_setting");
		 app.setting = res.data;
		
		const user = await app.getApi("utils.getCurrentUser"); 
	 
		 app.user = user.data;
		
	})



</script>
