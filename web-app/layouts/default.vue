<template>
    <div class="flex flex-col h-screen justify-between">
        <header class="bg-background text-text border-b border-primary p-2">
            <nav class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl" aria-label="Global">
                <div class="flex items-center ml-2 text-xl">
                    <img src="~/assets/logo.svg" alt="logo" class="h-10 w-10 mr-2" />
                    <nuxt-link to="/">Fact cheker</nuxt-link>
                </div>
                <div class="flex items-center" v-if="!authenticated" >
                    <nuxt-link to="/login" class="text-text hover:scale-110 transition-all font-medium rounded-lg text-lg px-4 lg:px-5 py-2 lg:py-2.5 mr-2">Login</nuxt-link>
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
<style>
</style>
