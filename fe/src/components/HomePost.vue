<template>
    <div class="middle">
    <div>
      <img src="@/assets/icon1.png">
      <h1>가장 소량씩, 가장 신선하게</h1>
      <p>적은 양으로 부담없이 즐겨요.</p>
    </div>
    <div>
      <img src="@/assets/icon2.png">
      <h1>친환경 채소를 가장 저렴하게!</h1>
      <p>30% OFF, 합리적인 가격으로 만나요!</p>
    </div>
    <div>
      <img src="@/assets/icon3.png">
      <h1>환경에 한 발 나은 선택</h1>
      <p>환경에 더 가까운 생산과 소비를 지지해요.</p>
     </div>
  </div>

    <div>
      <div class="r_product">
        <div>
          <h1>스토리보드</h1>
        </div>
      </div>
    </div>

    <div class="r_post">
    <Carousel v-bind="settings"  class="r_post-carousel">
      <Slide v-for="post in posts" :key="post.id">
        <div class="post-card"
          @mousedown.prevent="onMouseDown"
          @touchstart.prevent="onTouchStart"
          @click="goToPost(post.id)">
          <FeedListItem :post="post" />
          <h2>{{ post.created_by.username }}</h2>
        </div>
      </Slide>
      <template #addons>
        <Navigation />
      </template>
    </Carousel>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { Carousel, Navigation, Slide } from 'vue3-carousel';
import axios from 'axios';
import FeedListItem from '../components/FeedListItem.vue';
import 'vue3-carousel/dist/carousel.css';

export default defineComponent({
  name: 'HomePost',
  components: {
    Carousel,
    Slide,
    Navigation,
    FeedListItem,
  },
  data() {
    return {
      posts: [],
      // carousel settings
      settings: {
        itemsToShow: 4, // 한 번에 보여질 포스트 수
        snapAlign: 'center',
        infinite: true, // 무한 스크롤 활성화
      },
    };
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      axios.get('/api/posts/story')
        .then(response => {
          console.log(response.data); // API 응답 확인
          this.posts = response.data
        })
        .catch(error => {
          console.error('Error fetching posts:', error)
        })
    },
    goToPost(postId) {
      this.$router.push({ name: 'postview', params: { id: postId } })
    },
    onMouseDown(event) {
      event.stopPropagation()
    },
    onTouchStart(event) {
      event.stopPropagation()
    },
    regularPosts() {
      return this.posts.filter(post => post && post.content_type === 'post');
    },
  },
});
</script>
  
  
  <style scoped>
  .middle {
    display: flex;
    justify-content: center;
    text-align: center;
    gap: 100px;
    margin-bottom: 100px;
  }
  .middle img {
    margin: auto;
    width: 100px;
    margin-bottom: 20px;
  }
  .middle h1 {
    font-size: 22px;
    font-weight: 600;
  }
  .r_product {
    display: flex;
    justify-content: center;
    text-align: center;
    margin-bottom: 25px;
  }
  .r_product h1 {
    font-size: 28px;
    font-weight: 600;
  }
  .r_post {
    display: flex;
    justify-content: center;
    text-align: center;
    margin: auto;
  }
  .r_post-carousel {
    overflow-x: hidden;
    scroll-snap-type: x mandatory;
    height: auto;
    width: 70%;
  }
  .image-grid {
    position: relative;
  }
  .post-card {
    margin: 5px;
    border-radius: 13px;
    width: 400px;
    height: 300px;
    overflow: hidden;
    position: relative;
  }
  .post-card img {
    width: 100%;
    height: 100%;
    display: block;
    margin: auto;
    overflow: hidden;
  }
  </style>
  

  