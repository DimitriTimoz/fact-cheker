import { defineStore } from "pinia";
import { $apifetch } from "~/composable/fetch";

interface UserPayloadInterface {
  email: string;
  password: string;
}

export interface AuthResultInterface {
  success: boolean;
  message: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false,
    loading: false,
  }),
  actions: {
    async authenticateUser({ email, password }: UserPayloadInterface): Promise<AuthResultInterface> {
      // useFetch from nuxt 
      try {
        const { data, pending }: any = await $apifetch('/api/login/', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                password: password
              })
            });
          this.loading = pending;
          this.authenticated = true;
          this.loading = false;
          return { success: true, message: "User authenticated" };
      
      } catch (error: any) {
        console.error(error);
      }

      return { success: false, message: "User not authenticated" };
    },
    logUserOut() {
      this.authenticated = false;
    },
  },
});
