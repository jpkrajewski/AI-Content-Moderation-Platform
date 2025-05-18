<script setup lang="ts">
import { ref } from 'vue';
import { getCurrentUser } from "@/services/auth.ts";
import { useJwtStore } from '@/stores/jwt.ts';

const data = ref(null);
const jwtStore = useJwtStore();


function onbtnclick() {
    console.log('Button clicked');
    console.log('JWT:', jwtStore.jwt);
    getCurrentUser(jwtStore.jwt)
        .then(response => {
            console.log('User information:', response);
            data.value = response; // Update the reactive `data` value
        })
        .catch(error => {
            console.error('Error fetching user information:', error);
        });
}
</script>

<template>
    <div>
        <h1>Test Page</h1>
        <p>This is a test page.</p>
    </div>
    <div>
        <h2>User Information</h2>
        <pre>{{ data }}</pre>
        <button @click="onbtnclick">Fetch User Info</button>
    </div>
</template>
