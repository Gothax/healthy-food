<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4" ref="content">
		<div class="main-center col-span-3 space-y-4">

			<div v-for="post in posts" :key="post.id"
				class="p-4 bg-white border border-gray-200 rounded-lg">
				<FeedItem :post="post" />
			</div>
		</div>
		<div class="main-right col-span-1 space-y-4">

			<Trends />
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue';

export default {
	name: 'NonProductFeedView',

	components: {
		Trends,
		FeedItem,
	},

	data() {
		return {
			posts: [],
		}
	},

	mounted() {
		this.getPost()
	},

	methods: {
		getPost() {
			axios
				.get(`/api/posts/feed/`)
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