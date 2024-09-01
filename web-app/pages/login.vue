<template>
    <div class="container mx-auto max-w-sm">
      <div class="center">
        <h2 class="auth-title">Log in</h2>
      </div>
      <form class="container form flex flex-col mx-auto">
        <label class="input-label"  for="email"><b>Email</b></label>
        <input
          v-model="user.email"
          type="email"
          class="text-input"
          placeholder="Enter Email"
          name="email"
          required
        />
  
        <label class="input-label" for="psw"><b>Password</b></label>
        <input
          v-model="user.password"
          type="password"
          class="text-input"
          placeholder="Enter Password"
          name="psw"
          required
        />
        <div class="flex justify-end">
          <nuxt-link to="/register" class="text-text hover:scale-110 transition-all font-medium rounded-lg text-lg px-4 lg:px-5 py-2 lg:py-2.5 mr-2">Register</nuxt-link>
          <button @click.prevent="login" class="btn">Log in</button>
        </div>

        <div v-if="message" class="mt-5 alert" role="alert">
          <span>{{ message }}</span>
        </div>
      </form>
    </div>
  </template>
  <script lang="ts" setup>
import { storeToRefs } from 'pinia'; 
import { useAuthStore, type AuthResultInterface } from '~/store/auth';

const { authenticateUser } = useAuthStore(); 

const { authenticated } = storeToRefs(useAuthStore()); 

  const user = ref({
    email: '',
    password: '',
  });

  const message = ref('');
  
  const login = async () => {
    // Login and check status
    const response: AuthResultInterface = await authenticateUser(user.value);
    console.log(response);
    if (response.success) {
      window.location.href = '/check';
    } else {
      message.value = response.message;
    }
  };
  </script>
  