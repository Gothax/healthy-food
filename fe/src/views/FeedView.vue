<template>
    <div class="mx-20 mt-2 mb-6">
        <button @click="categorizeProduct('all')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'all' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">전체</button>
        <button @click="categorizeProduct('fruit')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'fruit' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">과일</button>
        <button @click="categorizeProduct('vegetable')" 
                :class="['mx-1 px-4 py-2 rounded text-white', category === 'vegetable' ? 'bg-blue-600' : 'bg-blue-500 hover:bg-blue-600']">채소</button>
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
</template>

<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import FeedListItem from '../components/FeedListItem.vue'

export default {
    name: 'FeedView',

    components: {
        Trends,
        FeedListItem,
    },

    data() {
        return {
            posts: [],
            body: '',
            category: 'all',
            nextPageUrl: null,
            isLoading: false,
            debouncedGetFeed: null,
        }
    },

    mounted() {
        this.getFeed('all')
        this.initDebouncedGetFeed()
        window.addEventListener('scroll', this.handleScroll)
    },

	beforeDestroy() {
		window.removeEventListener('scroll', this.handleScroll)
	},

    methods: {
        initDebouncedGetFeed() {
            this.debouncedGetFeed = this.debounce(this.getFeed, 100);
        },
        debounce(func, delay) {
            let timeoutId;
            return (...args) => {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                func.apply(this, args);
                }, delay);
            };
        },
        getFeed(category, page = 1) {
            if (this.isLoading) return;
            this.isLoading = true;

            let url = this.nextPageUrl || `/api/posts/?page=${page}`;
            if (category !== 'all') {
                url += `&category=${category}`;
            }

            axios
                .get(url)
                .then(response => {
                    this.posts.push(...response.data.results);
                    this.nextPageUrl = response.data.next;
                    this.isLoading = false;
                    
                    console.log('posts', this.posts)
                })
                .catch(error => {
                    console.log('error', error)
                    this.isLoading = false;
                });
        },
        handleScroll() {
            const scrollHeight = document.documentElement.scrollHeight;
            const scrollTop = document.documentElement.scrollTop;
            const clientHeight = document.documentElement.clientHeight;

            if (
                Math.ceil(scrollTop + clientHeight) >= Math.floor(scrollHeight) &&
                this.nextPageUrl &&
                !this.isLoading
            ) {
                this.debouncedGetFeed(this.category);
            }
        },
        categorizeProduct(category) {
            this.category = category
            this.posts = []
            this.nextPageUrl = null
            this.isLoading = false;
            this.getFeed(category)
        },
    }
}
</script>
