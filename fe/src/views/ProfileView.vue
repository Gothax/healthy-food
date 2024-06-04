<template>
    <div>
       <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4 ">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_userimage" class="mb-6 rounded-full">

                <p>
                    <strong>{{ user.name }}</strong>
                    <span v-if="user.is_seller">✔️</span>
                </p>

                <template v-if="userStore.user.isAuthenticated && user.is_seller">
                        <div class="flex items-center space-x-4">
                            <div>
                                <ModalView v-if="isModalViewed" @close-modal="isModalViewed = false">
                                    <ProductForm />
                                </ModalView>
                                <button @click="isModalViewed = true" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                </template>
                

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500"> {{ user.followers_count }} followers</p>
                    <p class="text-xs text-gray-500"> {{ user.following_count }} following</p>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

                <div class="mt-6">
                    <button 
                        class="inline-block py-4 px-3 bg-blue-600 text-xs text-white rounded-lg" 
                        @click="sendFollow"
                        v-if="!isFollowing && userStore.user.id !== user.id"
                    >
                        Follow
                    </button>
                    <button 
                        class="inline-block py-4 px-3 bg-gray-600 text-xs text-white rounded-lg" 
                        @click="sendFollow"
                        v-else-if="isFollowing && userStore.user.id !== user.id"
                    >
                        Unfollow
                    </button>
                
                    <button 
                        class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                    >
                        Log out
                    </button>

                    <RouterLink 
                        class="inline-block mr-2 py-4 px-3 bg-blue-600 text-xs text-white rounded-lg" 
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                    >
                        Edit profile
                    </RouterLink>

                    <div v-if="!user.is_seller" class="mt-6">
                        <input 
                            v-model="business_number" 
                            type="text" 
                            placeholder="사업자 번호" 
                            class="inline-block py-4 px-3 bg-gray-100 text-xs text-black rounded-lg"
                        />
                        <button 
                            class="inline-block py-4 px-3 bg-green-600 text-xs text-white rounded-lg" 
                            @click="registerAsSeller"
                        >
                            Register as Seller
                        </button>
                    </div>

                </div>


            </div>
        </div>

       <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

            <div class="main-center col-span-3 grid grid-cols-3 gap-4">
                <RouterLink :to="{name:'postview', params: {id: post.id}}" 
                    class="space-y-4" 
                    v-for="post in posts" 
                    v-bind:key="post.id"
                >
                    <FeedListItem v-bind:post="post" />
                </RouterLink>
            </div>

            <div class="main-right col-span-1 space-y-4">

                <Trends />
            </div>
        </div>

        

    </div>
</template>
<style>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>
<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import FeedListItem from '../components/FeedListItem.vue'
import ModalView from '../components/ModalView.vue'
import ProductForm from '../components/ProductForm.vue'

export default {
    name: 'FeedView',

    created() {
    this.checkFollowStatus();
    },

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    components: {
        Trends,
        FeedListItem,
        ModalView,
        ProductForm,
    },

    data() {
        return {
            posts: [],
            user: {
                id: ''
            },
            body: '',
            url: null,
            isFollowing: false,
            isModalViewed: false,
            business_number: '',

        }
    },

    mounted() {
        this.getFeed()
    },

    watch: { 
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        registerAsSeller() {
            axios
                .post(`/api/seller/register/`, {
                    business_number: this.business_number
                })
                .then(response => {
                    console.log('data', response.data)
                    this.$router.go();
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
        // 사용자가 현재 페이지의 프로필을 팔로우하고 있는지 확인하는 API 호출
        checkFollowStatus() {
            axios
                .get(`/api/follow/${this.$route.params.id}/status/`)
                .then(response => {
                    this.isFollowing = response.data.isFollowing;
                })
                .catch(error => {
                    console.error('Follow status check error', error);
                });
            },

        sendFollow() {
            axios
                .post(`/api/follow/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message === 'unfollow') {
                        this.isFollowing = false;
                        this.user.followers_count -= 1
                    } else {
                        this.isFollowing = true;
                        this.user.followers_count += 1
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log('Log out')

            this.userStore.removeToken()

            this.$router.push('/login')
        }
    }
}
</script>