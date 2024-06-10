<template>
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
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        
    }
}
</script>
