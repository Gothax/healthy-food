<template>
<div>
    <nav class="py-10 px-8 border-b border-gray-200">
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
                <div class="menu-left">
                    <RouterLink :to="{ name: 'home' }" class="text-x1 bold-text">Healthy Food</RouterLink>
                </div>

                <div class="menu-center flex space-x-12">
                    <RouterLink to="/feed" class="text-purple-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                        </svg>
                    </RouterLink>

                    <RouterLink to="/nonproductfeed" class="text-purple-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"></path>
                        </svg>                              
                    </RouterLink>

                    <RouterLink to="/crop" class="text-purple-700">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"></path>
                        </svg>                              
                    </RouterLink>

                    <RouterLink to="/search">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                        </svg>                                                         
                    </RouterLink>
                </div>

                <div class="menu-right flex items-center space-x-4">
                    <div>
                        <ChatbotModal v-if="isChatModalViewed" @close-modal="isChatModalViewed = false">
                            <ChatbotView />
                        </ChatbotModal>
                        <button  @click="isChatModalViewed = true" class="p-2 rounded-full hover:bg-gray-300">
                            <svg width="50" height="30" viewBox="0 0 85 83" fill="none" xmlns="http://www.w3.org/2000/svg" class="stroke-current stroke-0 fill_white wh-7"><g clip-path="url(#icon-chTalk_svg__clip0_2433_2222)" fill="#000"><path d="M41.719 83C18.722 83 0 64.407 0 41.5S18.722 0 41.719 0c22.996 0 41.718 18.624 41.718 41.5 0 5.87-1.244 11.549-3.668 16.943l4.976 11.644a3.162 3.162 0 01-.415 3.173 3.272 3.272 0 01-2.998 1.205L69.18 72.69A41.6 41.6 0 0141.72 83zm0-76.654c-19.488 0-35.34 15.768-35.34 35.154 0 19.386 15.852 35.154 35.34 35.154 9.026 0 17.637-3.426 24.24-9.613a3.13 3.13 0 012.647-.825l8.038 1.174-3.318-7.773a3.288 3.288 0 01.064-2.634A34.518 34.518 0 0077.026 41.5c0-19.386-15.851-35.154-35.34-35.154h.033z"></path><path d="M25.038 46.671c2.871 0 5.199-2.315 5.199-5.171 0-2.856-2.328-5.172-5.2-5.172-2.87 0-5.198 2.316-5.198 5.172s2.328 5.171 5.199 5.171zM43.505 46.671c2.87 0 5.198-2.315 5.198-5.171 0-2.856-2.327-5.172-5.199-5.172-2.87 0-5.198 2.316-5.198 5.172s2.327 5.171 5.199 5.171zM59.93 46.671c2.872 0 5.2-2.315 5.2-5.171 0-2.856-2.328-5.172-5.2-5.172-2.87 0-5.199 2.316-5.199 5.172s2.328 5.171 5.2 5.171z"></path></g><defs><clipPath id="icon-chTalk_svg__clip0_2433_2222"><path fill="#fff" d="M0 0h85v83H0z"></path></clipPath></defs></svg>                             
                        </button>
                    </div> 
                        <div class="flex items-center">
                            <button @click="isCartOpen = true" class="p-2 rounded-full hover:bg-gray-300">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 6h11L17 13M9 21h6M9 21a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm6 0a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
                                </svg>
                            </button>
                            <ShoppingCart :open="isCartOpen" @close-cart="isCartOpen = false" />
                        </div>

                    <template v-if="userStore.user.isAuthenticated">
                        <div class="flex items-center space-x-4">
                            <div>
                                <ModalView v-if="isModalViewed" @close-modal="isModalViewed = false">
                                    <FeedForm />
                                </ModalView>
                                <button @click="isModalViewed = true" class="p-2 rounded-full hover:bg-gray-300">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                </button>
                            </div>
                            <RouterLink :to="{name: 'profile', params:{'id': userStore.user.id}}">
                                <img :src="userStore.user.user_image" class="w-11 rounded-full">
                            </RouterLink>
                        </div>
                    </template>

                    <template v-else>
                        <RouterLink to="/login" class="mr-4 py-4 px-6 bg-gray-600 text-white rounded-lg">Log in</RouterLink>
                        <RouterLink to="/signup" class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign up</RouterLink>
                    </template>

                </div>

            </div>
        </div>
    </nav>

    <main class="px-8 py-6 bg-gray-100">
        <RouterView />
    </main>

    <Toast />
</div>
</template>

<style>
.bold-text {
  font-weight: bold;
  font-size : 30px;
}
</style>


<script>
    import axios from 'axios'
    import Toast from '@/components/Toast.vue'
    import { useUserStore } from '@/stores/user'
    import FeedForm from '@/components/FeedForm.vue';
    import ModalView from '@/components/ModalView.vue';
    import { RouterLink } from 'vue-router';
    import { ref } from 'vue'
    import ShoppingCart from './components/ShoppingCart.vue'
    import ChatbotView from '@/views/ChatbotView.vue'
    import ChatbotModal from '@/components/ChatbotModal.vue';


    export default {
        setup() {
            const userStore = useUserStore()
            const isCartOpen = ref(false)
            const isChatModalViewed = ref(false)

            return {
                userStore,
                isCartOpen,
                isChatModalViewed

            }
        },

        data() {    
            return {
                isModalViewed: false,
            };
        },

        components: {
            Toast,
            FeedForm,
            ModalView,
            ShoppingCart,
            ChatbotView,
            ChatbotModal

        },

        beforeCreate() {
            this.userStore.initStore()

            const token = this.userStore.user.access

            if (token) {
                axios.defaults.headers.common["Authorization"] = "Bearer " + token;
            } else {
                axios.defaults.headers.common["Authorization"] = "";
            }
        }
    }
</script>