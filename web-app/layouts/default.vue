<template>
    <div class="flex flex-col h-screen justify-between">
        <header class="bg-white text-gray-800 border-b border-blue-200 p-4">
            <nav class="flex flex-wrap justify-between items-center container mx-auto" aria-label="Global">
                <div class="flex items-center text-xl">
                    <img src="~/assets/logo.svg" alt="logo" class="h-10 w-10 mr-3" />
                    <nuxt-link :to="authenticated ? '/check/' : '/'" class="font-semibold text-blue-600 hover:text-blue-700 transition-colors">
                    Fact Checker
                    </nuxt-link>
                </div>
                <div class="flex items-center space-x-4">
                <template v-if="authenticated">
                    <nuxt-link to="/search" class="text-gray-700 hover:text-blue-600 transition-colors font-medium text-lg">
                        Search Engine
                    </nuxt-link>
                    <nuxt-link to="/check" class="text-gray-700 hover:text-blue-600 transition-colors font-medium text-lg">
                        Checker
                    </nuxt-link>
                    <button @click="logUserOut" class="bg-blue-600 text-white hover:bg-blue-700 transition-colors font-medium rounded-lg text-lg px-5 py-2">
                        Logout
                    </button>
                    </template>
                    <template v-else>
                    <nuxt-link to="/login" class="bg-blue-600 text-white hover:bg-blue-700 transition-colors font-medium rounded-lg text-lg px-5 py-2">
                        Login
                    </nuxt-link>
                </template>
              </div>
            </nav>
          </header>
        <main class="mainContent mb-auto">
            <slot />
        </main>
        <footer class="bg-background text-text border-t border-primary">
            <div class="flex justify-center items-center mx-auto max-w-screen-xl">
                <a href="https://github.com/DimitriTimoz" target="_blank"><p class="text-center">Dimitri Timoz © 2024</p></a>
            </div>
        </footer>
    </div>
</template>
<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '~/store/auth';

const { authenticated } = storeToRefs(useAuthStore());
const { logUserOut } = useAuthStore();
</script>