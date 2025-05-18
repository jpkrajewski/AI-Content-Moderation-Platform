<script setup lang="ts">
import { ref } from 'vue';
import {loginUser} from "@/services/auth.ts";
import { useJwtStore } from '@/stores/jwt.ts';

const jwtStore = useJwtStore();

function handleLogin() {
    // Handle login logic here
    console.log('Logging in with', { username, password });
    loginUser({
        email: username.value,
        password: password.value
    })
        .then(token => {
            console.log('Login successful:', token);
            // Handle successful login (e.g., redirect to dashboard)
            jwtStore.setJwt(token);
            console.log('Token set in store:', token);
            // Optionally, redirect to another page after login
        })
        .catch(error => {
            console.error('Login failed:', error);
            // Handle login failure (e.g., show error message)
        });


}
const username = ref('');
const password = ref('');

</script>

<template>
    <div>
        <h1>Login Page</h1>
        <form @submit.prevent="handleLogin">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>
