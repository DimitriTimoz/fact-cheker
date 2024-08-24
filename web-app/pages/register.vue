<template>
    <form method="post">
        <div class="container form">
            <label for="uname"><b>Email</b></label>
            <input
                v-model="user.email"
                type="email"
                class="input"
                placeholder="Enter email"
                name="uemail"
                required
            />
            <label for="psw"><b>Password</b></label>
            <input
                v-model="user.password"
                type="password"
                class="input"
                placeholder="Enter Password"
                name="psw"
                required
            />
            <button @click.prevent="register" class="btn">Register</button>
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
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user.value)
    });
};

</script>
