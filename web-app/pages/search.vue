<template>
    <div class="container flex flex-col items-center mt-4">
        <h2 class="text-text font-bold text-2xl m-6">Search among newspapers</h2>
        <div class="rounded-2xl w-4/5">
            <input type="text" v-model="search" placeholder="Search for a newspaper" 
                class="text-input" />
            <button @click="searchNewspaper" class="btn">Search</button>    
        </div>
    </div>
</template>
<script lang="ts" setup>
import { $apifetch } from '~/composable/fetch';

const search = ref('');

const searchNewspaper = async () => {
    try {
        const response = await $apifetch('/api/search/', {
            method: 'GET',
            query: {
                q: search.value
            }
        });
        console.log(response);
    } catch (error: any) {
        console.error(error);
    }
}

definePageMeta({
    middleware: 'auth' 
})
</script>
