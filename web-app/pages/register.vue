<template>
    <div class="center">
        <h2 class="center">Register</h2>
    </div>
    <form method="post">
        <div class="container form flex flex-col mx-auto">
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
            <button @click.prevent="register" class="btn mt-2">Register</button>
        </div>
    </form>
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
