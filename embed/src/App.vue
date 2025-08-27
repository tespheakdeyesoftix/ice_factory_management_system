<template>
	<div >
	 <div v-if="!loading">
		<router-view />
		</div>
		<div v-else>
			Loading...
		</div>
	</div>
	
</template>


<script setup>
import {onMounted, ref} from "vue"

const loading = ref(true)
	onMounted(async()=>{
 loading.value = true
		const res = await app.getApi("utils.get_setting");
		 app.setting = res.data;
		
		const user = await app.getApi("utils.getCurrentUser"); 
	 
		 app.user = user.data;
		 loading.value = false;
		
	})



</script>
