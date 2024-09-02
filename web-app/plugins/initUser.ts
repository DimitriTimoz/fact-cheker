import { useUserStore } from "~/store/user";

export default defineNuxtPlugin(() => {
    const authStore = useUserStore();
    authStore.load(); 
});
