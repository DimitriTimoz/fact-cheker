<template>
    <div class="container mx-auto max-w-sm">
        <div class="center">
            <h2 class="center title text-text text-xl">Sign up</h2>
        </div>
        <form method="post">
            <div class="form flex flex-col mx-auto">
                <label for="email"><b>Email</b></label>
                <input
                    v-model="user.email"
                    type="email"
                    class="text-input"
                    placeholder="Enter email"
                    name="email"
                    required
                />
                <label for="psw"><b>Password</b></label>
                <input
                    v-model="user.password"
                    type="password"
                    class="text-input"
                    placeholder="Enter Password"
                    name="psw"
                    required
                />

                <label for="confirm-psw"><b>Confirm Password</b></label>
                <input
                    v-model="user.confirmPassword"
                    type="password"
                    class="text-input"
                    placeholder="Confirm Password"
                    name="confirm-psw"
                    required
                />
                <div class="flex justify-end">
                    <nuxt-link to="/login" class="text-text hover:scale-110 transition-all font-medium rounded-lg text-lg px-4 lg:px-5 py-2 lg:py-2.5 mr-2">Log in</nuxt-link>
                    <button @click.prevent="register" class="btn">Register</button>
                </div>
            </div>
        </form>
    </div>
</template>
<script lang="ts" setup>
interface User {
    email: string;
    password: string;
}

import { ref } from 'vue';

const user = ref({
    email: '',
    password: '',
    confirmPassword: '',
});

const register = async () => {
    $fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": useCookie('csrftoken').value || ''
        },
        body: JSON.stringify(user.value)
    });
};

</script>
