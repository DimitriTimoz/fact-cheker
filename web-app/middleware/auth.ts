import { useAuthStore } from "~/store/auth";

export default defineNuxtRouteMiddleware((to, from) => {
    const authStore = useAuthStore();
    if (!authStore.authenticated && to.name !== 'login') {
      return navigateTo('/login'); // Redirect to login page if user is not authenticated
    }
})
