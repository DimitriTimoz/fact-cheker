<template>
    
    <!-- Hero Section -->
    <section class="bg-blue-600 text-white text-center py-16">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-4xl font-bold mb-4">Verify News with Confidence</h1>
            <p class="text-lg mb-8">Our app helps you quickly and accurately fact-check news articles and prevent misinformation.</p>
            <a href="#cta" class="bg-white text-blue-600 py-2 px-4 rounded-lg font-semibold hover:bg-gray-100">Get Started</a>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-16">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-12">Features</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="feature-container">
                    <svg class="w-12 h-12 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4.5M12 16h.01"></path></svg>
                    <h3 class="text-xl font-semibold mb-2">Fast Fact-Checking</h3>
                    <p class="text-gray-600">Get instant results on the accuracy of news articles with our fast and reliable fact-checking algorithms.</p>
                </div>
                <div class="feature-container">
                    <svg class="w-12 h-12 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-1h-1v1H9v-2h3v2zm-2 0v-2H8v-1H7v-2h1V8h4v3h1v3h-1v1H8v1h1v2h2z"></path></svg>
                    <h3 class="text-xl font-semibold mb-2">Reliable Sources</h3>
                    <p class="text-gray-600">We pull data from trusted sources to ensure the information you receive is accurate and up-to-date.</p>
                </div>
                <div class="feature-container">
                    <svg class="w-12 h-12 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a2 2 0 012-2h14a2 2 0 012 2v16a2 2 0 01-2 2H5a2 2 0 01-2-2V4zm2 0v16h14V4H5zm2 4h10v2H7V8z"></path></svg>
                    <h3 class="text-xl font-semibold mb-2">User-Friendly Interface</h3>
                    <p class="text-gray-600">Our intuitive interface makes it easy for anyone to navigate and find accurate information quickly.</p>
                </div>

                <!-- AI Feature Block -->
                <div class="feature-container">
                    <div class="flex flex-col lg:flex-row items-center gap-8">
                        <svg class="w-12 h-12 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a2 2 0 012-2h14a2 2 0 012 2v16a2 2 0 01-2 2H5a2 2 0 01-2-2V4zm2 0v16h14V4H5zm2 4h10v2H7V8z"></path></svg>
                        <div class="flex-1 text-center lg:text-left">
                            <h3 class="text-2xl font-semibold mb-4">Advanced AI Technology</h3>
                            <p class="text-gray-600">Stay ahead of misinformation with our powerful AI-driven fact-checking capabilities that ensure you always have access to the truth.</p>
                        </div>
                    </div>
                </div>
                <!-- End AI Feature Block -->
            </div>
        </div>
    </section>


    <!-- Call to Action (CTA) -->
    <section id="cta" class="bg-blue-600 text-white text-center py-16">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Ready to Start Fact-Checking?</h2>
            <p class="text-lg mb-8">Join thousands of users who rely on our app to stay informed and avoid misinformation.</p>
            <nuxt-link to="/register" href="#" class="bg-white text-blue-600 py-2 px-4 rounded-lg font-semibold hover:bg-gray-100 cursor-pointer">Sign Up Now</nuxt-link>
        </div>
    </section>
</template>
<script lang="ts" setup>

</script>
