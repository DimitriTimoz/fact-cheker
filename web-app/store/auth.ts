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

const AUTHENTICATED = 'authenticated';

export const useAuthStore = defineStore('authStore', () => {
  const authenticated: Ref<boolean> = ref(false);
  const loading: Ref<boolean> = ref(false);

  load();

  async function authenticateUser({ email, password }: UserPayloadInterface): Promise<AuthResultInterface> {
    loading.value = true;
    try {
      const { data }: any = await $apifetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      authenticated.value = true;
      save();
      loading.value = false;
      return { success: true, message: "User authenticated" };

    } catch (error: any) {
      console.error(error);
      loading.value = false;
      return { success: false, message: "User not authenticated" };
    }
  }

  function logUserOut() {
    authenticated.value = false;
    save();
    // TODO: Send logout request to server
  }

  function save() {
    sessionStorage.setItem(AUTHENTICATED, JSON.stringify(authenticated.value));
  }

  function load() {
    const authData = sessionStorage.getItem(AUTHENTICATED);

    if (authData) {
      authenticated.value = JSON.parse(authData);
    }
  }

  return {
    authenticated,
    loading,
    authenticateUser,
    logUserOut
  };
});
