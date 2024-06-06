<template>
  <!-- 메인화면 Carousel -->
  <Carousel :autoplay="3000" :wrap-around="true" class="carousel-container bg-gray-100">
    <Slide v-for="slide in 1" :key="slide">
      <div class="carousel__item">
        <img src="@/assets/banner1.png" class="banner">
      </div>
    </Slide>
    <Slide v-for="slide in 1" :key="slide">
      <div class="carousel__item">
        <img src="@/assets/banner2.png" class="banner">
      </div>
    </Slide>
    <template #addons>
      <Pagination />
    </template>
  </Carousel>

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

  <div class = "caution bg-gray-100">
    <div>
      <h1 class="mt-10">농작물 취급 안내</h1>
      <img src="@/assets/p_banner.jpg">
      </div>
      </div>
      
  <div>
    <button class="btn mt-8">농작물 취급 안내</button>
  </div>

</template>

<script>
import { defineComponent } from 'vue'
import { Carousel, Pagination, Slide } from 'vue3-carousel'

import 'vue3-carousel/dist/carousel.css'

export default defineComponent({
  name: 'Autoplay',
  components: {
    Carousel,
    Slide,
    Pagination,
  },
})
</script>

<style scoped>
 .carousel-container{
  width: 100%;
  margin-bottom : 100px;
 }
 .banner{
  width : 1360px;
 }
 .middle {
  display: flex;
  justify-content: center; /* 중앙 정렬 */
  text-align : center;
  gap : 100px;
  margin-bottom : 100px;
}
 .middle img{
  margin : auto;
  width : 100px;
  margin-bottom : 20px;
 }
 .middle h1{
  font-size : 22px;
  font-weight: 600;
 }
.caution {
  display: flex;
  justify-content: center; /* 중앙 정렬 */
  text-align : center;
  margin-bottom : 50px;
}
.caution h1{
  font-size : 28px;
  font-weight : 600;
}
.caution img{
  width:1360px;
  margin-top : 30px;
}
.btn{
  display: flex;
  justify-content: center; /* 중앙 정렬 */
  text-align : center;
  margin : auto;
  background: orangered; /* 배경을 없앱니다 */
  /* border: 2px solid orange; 테두리를 설정합니다 */
  border-radius: 8px; /* 양끝을 둥글게 만듭니다 */
  padding: 16px 20px; /* 버튼의 패딩을 설정합니다 */
  cursor: pointer; /* 마우스 커서를 포인터로 설정합니다 */
  color : white;
  font-weight: 600;
  width : 448px;
  height : 56px;
}

</style>