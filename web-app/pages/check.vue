<template>
    <div class="container lg mx-auto center">
        <textarea class="text-text bg-transparent center w-full mt-5 p-2 outline-blue-500 border-2 border-primary rounded-lg mb-2"
                    placeholder="The statement..."
                    v-model="value">
        </textarea>
        <button class="btn" @click="check">Check</button>
        <button class="btn ml-2" @click="clear">Clear</button>

        <li v-for="review in review.reviews" class="mt-5 container list-none">
            <ul class="column flex-row border-2 rounded-md p-2 shadow-sm">
                <div class="flex flew-row border-b">
                    <svg v-if="review.state" class="w-3.5 h-3.5 me-2 my-auto text-green-500 dark:text-green-400 flex-shrink-0 center" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                    </svg>
                    <svg v-else class="flex-shrink-0 inline w-4 h-4 me-3 text-red-600 my-auto" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
                    </svg>
                    <a :href="review.url" target="_blank" class="text-text">{{review.url}}</a>
                </div>
                <p class="text-text" >{{ review.review }}</p>
            </ul>
        </li>

        <div v-if="review.fetched" class="mt-5 container border-2 rounded-md p-2 shadow-sm">
            <p class="text-text">{{ review.conclusion }}</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { $apifetch } from '~/composable/fetch';

interface ReviewResponse {
    state: boolean;
    url: string;
    content: string;
}

interface ReviewResponse {
    fetched: boolean;
    conclusion: string;
    reviews: string[];
}

const value = ref('');
const review = ref({
    fetched : false,
    conclusion: '',
    reviews: []
})

function clear() {
    value.value = '';
    review.value = {
        fetched: false,
        conclusion: '',
        reviews: []
    }
}

async function check(e: Event) {
    e.preventDefault();
    console.log("Check function triggered"); // Log the function call

    const response = await $apifetch('/api/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: value.value })
    });

    const data = await response;

    console.log("Response data:", data); // Log the response

    review.value = {
        fetched: true,
        conclusion: data.conclusion,
        reviews: data.reviews
    }
}

definePageMeta({
    middleware: 'auth' 
})

</script>
