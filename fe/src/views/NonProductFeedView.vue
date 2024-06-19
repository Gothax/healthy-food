<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4" ref="content">
		<div class="main-center col-span-3 space-y-4">

			<div v-for="post in posts" :key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
				<FeedItem :post="post" />
			</div>
		</div>
		<div class="main-right col-span-1 space-y-4">

			<Trends />
		</div>
	</div>
	
	<ScrollToTop></ScrollToTop>
</template>

<script>
import axios from 'axios';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue';
import ScrollToTop from '../components/ScrollToTop.vue';

export default {
	name: 'NonProductFeedView',

	components: {
		Trends,
		FeedItem,
		ScrollToTop,
	},

	data() {
		return {
			posts: [],
			nextPageUrl: null,
			isLoading: false,
		}
	},

	mounted() {
		this.getPost(1)
		window.addEventListener('scroll', this.handleScroll)
	},

	beforeDestroy() {
		window.removeEventListener('scroll', this.handleScroll)
	},
	
	methods: {
		getPost(page) {
			if (this.isLoading) return;
			this.isLoading = true;

			const url = this.nextPageUrl || `/api/posts/feed/?page=${page}`;
			axios
				.get(url)
				.then((response) => {
					this.posts.push(...response.data.results);
					this.nextPageUrl = response.data.next;
					this.isLoading = false;
					console.log(this.posts)
				})
				.catch((error) => {
					console.log('error', error);
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
				this.getPost();
			}
		},
	}
}

</script>