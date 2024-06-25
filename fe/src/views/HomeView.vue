<template>
    <!-- 메인화면 Carousel -->
    <Carousel
      :autoplay="3000"
      :wrap-around="true"
      class="carousel-container bg-gray-100"
    >
      <Slide v-for="slide in 1" :key="slide">
        <div class="carousel__item">
          <img src="@/assets/banner1.png" class="banner" />
        </div>
      </Slide>
      <Slide v-for="slide in 1" :key="slide">
        <div class="carousel__item">
          <img src="@/assets/banner2.png" class="banner" />
        </div>
      </Slide>
      <template #addons>
        <Pagination />
      </template>
    </Carousel>
  
    <HomePost />
  
    <HomeInfo />
  
    <Footer />
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import { Carousel, Navigation, Pagination, Slide } from "vue3-carousel";
  import axios from "axios";
  import "vue3-carousel/dist/carousel.css";
  import HomePost from "@/components/HomePost.vue";
  import HomeInfo from "@/components/HomeInfo.vue";
  import Footer from "@/components/Footer.vue";
  
  export default defineComponent({
    name: "HomeView",
    components: {
      Carousel,
      Slide,
      Navigation,
      Pagination,
      HomePost,
      HomeInfo,
      Footer,
    },
  });
  </script>
  
  <style scoped>
  .carousel-container {
    width: 100%;
    margin-bottom: 120px;
  }
  .banner {
    width: 1360px;
  }
  </style>
  