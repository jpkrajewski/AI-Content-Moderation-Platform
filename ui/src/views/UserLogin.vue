<script setup lang="ts">
import { ref } from 'vue';
import {loginUser} from "@/services/auth.ts";
import { useJwtStore } from '@/stores/jwt.ts';
import { useRouter } from 'vue-router';
const router = useRouter();



const jwtStore = useJwtStore();

function handleLogin() {
    loginUser({
        username: username.value,
        password: password.value
    })
        .then(token => {
            jwtStore.setJwt(token);
            router.push('/secure/dashboard/summary');

        })
        .catch(error => {
            console.error('Login failed:', error);
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
