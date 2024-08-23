<template>
    <header class="bg-background text-text border-b border-primary">
        <nav class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl" aria-label="Global">
            <div class="flex items-center ml-2">
                <nuxt-link to="/">Home</nuxt-link>
            </div>
            <div class="flex items-center" v-if="!authenticated" >
                <nuxt-link to="/login" class="text-text  hover:primary focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2">Login</nuxt-link>
            </div>
        </nav>
    </header>
    <div class="mainContent">
        <slot />
    </div>
    <footer>
    </footer>
</template>
<style>
</style>
