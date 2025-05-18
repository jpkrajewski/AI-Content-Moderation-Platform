import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useJwtStore = defineStore('jwt', () => {
  // Initialize the JWT token from localStorage if available
  const jwt = ref(localStorage.getItem('jwt') || '');

  // Computed property to determine if the user is logged in
  const isLoggedIn = computed(() => !!jwt.value);

  // Method to set the JWT token and persist it in localStorage
  const setJwt = (token: string) => {
    jwt.value = token;
    localStorage.setItem('jwt', token); // Save the token to localStorage
  };

  // Method to clear the JWT token and remove it from localStorage
  const clearJwt = () => {
    jwt.value = '';
    localStorage.removeItem('jwt'); // Remove the token from localStorage
  };

  return { jwt, isLoggedIn, setJwt, clearJwt };
});
