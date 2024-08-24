<template>
    <div class="container lg mx-auto center">
        <textarea class="text-text bg-transparent center w-full mt-5 p-2 outline-blue-500 border-2 border-primary rounded-lg mb-2"
                    placeholder="The statement..."
                    @change="check"
                    v-model="value">
        </textarea>
        <button class="btn" @click="check">Check</button>
        <button class="btn ml-2" @click="clear">Clear</button>
        <div v-if="review.fetched" class="mt-5 container">
            <p class="text-text">Conclusion: {{ review.conclusion }}</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

interface ReviewResponse {
    fetched: boolean;
    conclusion: string;
    reviews: string[];
}

const value = ref('');
const review = ref({
    fetched : true,
    conclusion: 'This is a conclusion',
    reviews: [] as string[]
})

function clear() {
    value.value = '';
    review.value = {
        fetched: false,
        conclusion: '',
        reviews: []
    }
}

async function check() {
    const csrf = useCookie('csrftoken');
    const response: ReviewResponse = await $fetch<ReviewResponse>('/api/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf.value || ''
        },

        body: JSON.stringify({ content: value.value })
    });

    const data = await response;

    review.value = {
        fetched: true,
        conclusion: data.conclusion,
        reviews: data.reviews
    }
}

</script>
