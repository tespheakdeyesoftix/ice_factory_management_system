<template>
  <div>
	<h1>Home Page</h1>
	
	<div class="card flex justify-center">
        <Button label="Verify" />
    </div>
	<Checkbox v-model="checked" binary />

  </div>
</template>

<script setup>
 import Button from "primevue/button"
 import Checkbox from 'primevue/checkbox';
</script>
