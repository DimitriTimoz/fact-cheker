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
        <div v-if="newspapers.length > 0" class="mt-10 container mx-auto px-4">
            <ul class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-5">
                <li v-for="newspaper in newspapers" class="bg-white border border-gray-200 rounded-lg p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
                    <div class="flex flex-col">
                        <a :href="newspaper.url" target="_blank" class="text-xl font-semibold text-blue-600 hover:text-blue-800 truncate" :title="newspaper.title">
                            {{ newspaper.title }}
                        </a>
                        <a :href="newspaper.url" target="_blank" class="text-sm text-blue-500 hover:text-blue-700 truncate" :title="newspaper.url">
                            {{ newspaper.url }}
                        </a>
                        <p class="text-gray-600 line-clamp-3 mt-2">
                            {{ newspaper.description }}
                        </p>
                    </div>
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
