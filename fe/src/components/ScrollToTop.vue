<template>
    <div class="fixed bottom-5 right-5">
        <button @click="scrollToTop"
            class="bg-white text-gray-700 rounded-full p-2 hover:bg-gray-200 border border-white-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 6.75 12 3m0 0 3.75 3.75M12 3v18" />
            </svg>
        </button>
    </div>
</template>

<script>
export default {
    name: 'ScrollToTop',
    methods: {
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    }
}
</script>