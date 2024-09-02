<template>
    <div v-if="userdata" class="flex justify-end" role="alert">
        <span class="bg-black text-white text-sm rounded-3xl px-3 py-2 text-center m-3" >Rate limit {{  userdata.used }}/{{ userdata.limit }}</span>
    </div>
    <div class="container lg mx-auto center max-w-screen-lg p-2">
        <h1 class="text-title font-bold text-2xl">Fact Checker</h1>
        <p> Enter a statement to find relevant reviews and references to verify it thanks to the newspapers.</p>
        <textarea class="text-text bg-transparent center w-full mt-5 p-2 outline-blue-600 border-2 border-primary rounded-lg mb-2"
                    placeholder="The statement..."
                    v-model="value">
        </textarea>
        <button v-if="!fetching" class="btn" @click="check">Check</button>
        <button v-if="!fetching" class="btn ml-2" @click="clear">Clear</button>

        <li v-for="review in review.reviews" class="mt-6 list-none">
            <div class="bg-white border border-gray-200 rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div class="flex items-center justify-between border-b border-gray-200 pb-3 mb-3">
                <div class="flex items-center">
                  <svg v-if="review.state" class="w-5 h-5 mr-2 text-green-500 flex-shrink-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                  </svg>
                  <svg v-else class="w-5 h-5 mr-2 text-red-500 flex-shrink-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
                  </svg>
                  <span class="font-semibold text-lg text-gray-800">
                    {{ review.state ? 'Vérifié' : 'Non vérifié' }}
                  </span>
                </div>
                <a :href="review.url" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm truncate max-w-xs">
                  {{ review.url }}
                </a>
              </div>
              <p class="text-gray-700 leading-relaxed">{{ review.review }}</p>
            </div>
          </li>
        
        <div v-if="review.fetched" class="mt-5 container border-2 rounded-md p-2 shadow-sm">
            <p class="text-text">{{ review.conclusion }}</p>
        </div>

        <div v-if="fetching" class="flex mx-auto justify-center fle">
            <svg class="animate-spin h-5 w-5 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing...
        </div>
          
        <div v-if="error" class="mt-5 alert" role="alert">
            <span>{{ error }}</span>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { $apifetch } from '~/composable/fetch';
import { useUserStore } from '~/store/user';

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

const fetching = ref(false);
const value = ref('');
const review = ref({
    fetched : false,
    conclusion: '',
    reviews: [] as ReviewResponse[]
})

const error = ref('');

const userStore = useUserStore()
const { updateUser } = userStore
const { userdata } = storeToRefs(userStore);

function clear() {
    value.value = '';
    review.value = {
        fetched: false,
        conclusion: '',
        reviews: []
    }
}

interface CheckError {
    error: string;
}

async function check(e: Event) {
    e.preventDefault();
    console.log("Check function triggered"); // Log the function call

    try {
        fetching.value = true;
        const response = await $apifetch('/api/check/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: value.value })
        });
        const data = await response;

        review.value = {
            fetched: true,
            conclusion: data.conclusion,
            reviews: data.reviews
        }
        error.value = '';
        updateUser();

    } catch (errorResp: any) {
        error.value = errorResp.data.error;
    }
    fetching.value = false;
}

definePageMeta({
    middleware: 'auth' 
})

</script>
