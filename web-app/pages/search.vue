<template>
    <div class="container flex mx-auto max-w-6xl flex-col items-center mt-4">
        <h2 class="text-text font-bold text-2xl m-6">Search among newspapers</h2>
        <div class="flex rounded-2xl w-4/5">
            <input type="text" v-model="search" placeholder="Search for a newspaper" 
                class="text-input w-full h-14" />
            <button @click="searchNewspaper" class="btn">Search</button>    
        </div>
        <div v-if="message" class="mt-5 alert" role="alert">
            <span>{{ message }}</span>
        </div>
        <div v-if="newspapers" class="mt-5 container list-none">
            <ul class="column flex-row border-2 rounded-md p-2 shadow-sm">
                <li v-for="newspaper in newspapers" class="mt-5">
                    <div class="flex flew-row border-b">
                        <a :href="newspaper.url" target="_blank" class="text-text">{{newspaper.title}}</a>
                    </div>
                    <p class="text-text" >{{ newspaper.description }}</p>
                </li>
            </ul>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { $apifetch } from '~/composable/fetch';

const search = ref('');
const message = ref('');

const newspapers = ref([] as Newspaper[]);

interface Newspaper {
    title: string;
    url: string;
    description: string;
}

const searchNewspaper = async () => {
    try {
        const response = await $apifetch('/api/search/', {
            method: 'GET',
            query: {
                q: search.value
            }
        });

        newspapers.value = response;
        console.log(newspapers.value);
        message.value = "";
    } catch (error: any) {
        // Check if the error is a string
        if (typeof error === 'string') {
            message.value = error;
            return;
        }

        // Check if the error is an object
        if (error.data && error.data.error) {
            message.value = error.data.error;
        }
    }
}

definePageMeta({
    middleware: 'auth' 
})
</script>
