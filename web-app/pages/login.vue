<template>
    <div>
      <div class="center">
        <h2 class="center">Login</h2>
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
  
        <button @click.prevent="login" class="btn mt-2">Login</button>
      </form>
    </div>
  </template>
  <script lang="ts" setup>
  const user = ref({
    email: '',
    password: '',
  });
  
  const login = async () => {
    // Login and check status
    const response = await $fetch('/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": useCookie('csrftoken').value || ''
      },
      body: JSON.stringify(user.value),
    });

    const data = await response;
  };
  </script>
  