<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">  
                    <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you looking for?">

                    <button class="inline-block py-4 px-6 bg-blue-600 text-white rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                        </svg>
                    </button>
                </form>
            </div>


            <div v-if="posts_from_products.length || posts_from_labels.length">
                <!-- 상품 -->
                <h2 class="text-xl font-bold">검색된 상품</h2>
                <RouterLink :to="{name:'postview', params: {id: post.id}}" 
                    class="space-y-4" 
                    v-for="post in posts_from_products" 
                    v-bind:key="post.id"
                >
                    <FeedListItem v-bind:post="post" />
                </RouterLink>

                <!-- 리뷰, 일반 글 -->
                <h2 class="text-xl font-bold mt-4">연관된 글</h2>
                <RouterLink :to="{name:'postview', params: {id: post.id}}" 
                    class="space-y-4" 
                    v-for="post in posts_from_labels" 
                    v-bind:key="post.id"
                >
                    <FeedListItem v-bind:post="post" />
                </RouterLink>

            </div>
            <div v-else>
                <p class="text-center text-gray-500">검색 결과가 없습니다.</p>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">

            <Trends />
        </div>
    </div>
</template>

<!-- 지금 : 검색 - user + post의 body 검색 결과
개선 : 검색 - user + post body 검색  - product
                                    - review
                                    - post 결과 -->

<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import FeedListItem from '../components/FeedListItem.vue'

export default {
    name: 'SearchView',

    components: {
        Trends,
        FeedItem,
        FeedListItem,
    },

    data() {
        return {
            query: '',

            posts_from_products: [],
            posts_from_labels: []
        }
    },

    methods: {
        submitForm() {
            if(this.query.length < 1){
                return
            }
            console.log('submitForm', this.query)

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data)

                    this.posts_from_products = response.data.posts_from_products
                    this.posts_from_labels = response.data.posts_from_labels
                })
                .catch(error => {
                    console.log('error:', error)
                })
        }
    }
}
</script>