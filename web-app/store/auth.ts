import { defineStore } from "pinia";
import { $apifetch } from "~/composable/fetch";

interface UserPayloadInterface {
    email: string;
    password: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false,
    loading: false,
  }),
  actions: {
    async authenticateUser({ email, password }: UserPayloadInterface): Promise<string> {
      // useFetch from nuxt 3
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
          console.log("data", data);
          if (data.value) {
            console.log("data", data)
            this.authenticated = true;
            return "success";
          }    
      } catch (error) {
        console.log("error", error);
      }
      return "Login failed";
    },
    logUserOut() {
      this.authenticated = false;
    },
  },
});
