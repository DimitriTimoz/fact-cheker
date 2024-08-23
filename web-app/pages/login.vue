<template>
    <div>
      <div class="title">
        <h2>Login</h2>
      </div>
      <div class="container form">
        <label for="uname"><b>Email</b></label>
        <input
          v-model="user.email"
          type="email"
          class="input"
          placeholder="Enter Email"
          name="uname"
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
  
        <button @click.prevent="login" class="button">Login</button>
      </div>
    </div>
  </template>
  <script lang="ts" setup>
  const user = ref({
    email: '',
    password: '',
  });
  
  const login = async () => {
    // Login and check status
    const response = await $fetch('http://localhost:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user.value),
    });

    const data = await response;
  };
  </script>
  