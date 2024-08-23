<template>
    <div class="container lg mx-auto center">
        <textarea class="text-text bg-transparent center border-2 w-full" 
                    placeholder="The statement..."
                    @change="check"
                    v-model="value">
        </textarea>
        <button class="btn" @click="check">Check</button>
        <div v-if="review.fetched">
            <p>Conclusion: {{ review.conclusion }}</p>
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
    fetched : false,
    conclusion: '',
    reviews: [] as string[]
})

async function check() {

    const response: ReviewResponse = await $fetch<ReviewResponse>('http://localhost:8000/check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
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
