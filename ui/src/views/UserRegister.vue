<script setup lang="ts">
import { ref } from 'vue';
import { registerUser } from "@/services/auth.ts";

const username = ref('');
const password = ref('');
const email = ref('');
const errorMessage = ref('');
const successMessage = ref('');

function handleRegister() {
  // Clear messages
  errorMessage.value = '';
  successMessage.value = '';

  // Simple validation
  if (!username.value || !password.value || !email.value) {
    errorMessage.value = 'All fields are required.';
    return;
  }

  if (!validateEmail(email.value)) {
    errorMessage.value = 'Please enter a valid email address.';
    return;
  }

  // Simulate an API call (replace with your actual API logic)
  registerUser({
    username: username.value,
    password: password.value,
    email: email.value,
  })
    .then((response) => {
      successMessage.value = 'Registration successful!';
      console.log('Registration response:', response);

      // Clear form fields after successful registration
      username.value = '';
      password.value = '';
      email.value = '';
    })
    .catch((error) => {
      errorMessage.value = 'Registration failed. Please try again.';
      console.error('Registration error:', error);
    });
}

// Utility function to validate email format
function validateEmail(email: string) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
</script>

<template>
  <div>
    <h1>Register Page</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <button type="submit">Register</button>
      </div>
    </form>

    <!-- Error Message -->
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>

    <!-- Success Message -->
    <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
  </div>
</template>

<style>
form {
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}
</style>
