<template>
  <div class="info">
    <div>
      <p class="info_title mt-20">못생겨도 맛과 가격은 A급!</p>
      <h1>'못난이 농사물'을 아시나요?</h1>
      <div class="info_board" style="display: flex">
        <div class="board-1 mr-5" data-aos="zoom-in" data-aos-delay="100">
          <img src="@/assets/ugly_1.jpg" />
          <div
            class="board-1-text mt-5"
            style="text-align: center; font-size: 20px"
          >
            <h1>못난이 채소</h1>
            <p class="board-text">예쁘지 않으면 어때? 맛좋고 몸에좋은걸</p>
          </div>
        </div>
        <div class="board-2 ml-5" data-aos="zoom-in" data-aos-delay="200">
          <img src="@/assets/Lettuce.jpg" />
          <div
            class="board-1-text mt-5"
            style="text-align: center; font-size: 20px"
          >
            <h1>제철 친환경 농산물</h1>
            <p class="board-text">제철 농산물만 엄선하여 보내드려요.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="info_mission">
    <div class="info_banner">
      <div class="image-overlay">
        <p>
          우리의 미션<br />
          지속가능한 식탁
        </p>
        <div class="mission-board">
          <div class="m-board" style="color: white" data-aos="flip-left">
            <div>
              <img src="@/assets/Lettuce.jpg" />
              <h2
                class="m-board1-t mt-14"
                style="
                  color: white;
                  display: flex;
                  justify-content: center;
                  font-weight: bold;
                  font-size: 18px;
                "
              >
                현재 우리가 필요한건 무엇일까?
              </h2>
            </div>
          </div>
          <div class="m-board" style="color: white" data-aos="flip-left">
            <div class="image-container">
              <div class="image-overlay">
                <img src="@/assets/Lettuce.jpg" />
                <h2
                  class="m-board1-t mt-14"
                  style="
                    color: white;
                    display: flex;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 18px;
                  "
                >
                  현재 우리가 필요한건 무엇일까?
                </h2>
              </div>
            </div>
          </div>
          <div class="m-board" style="color: white" data-aos="flip-left">
            <div>
              <img src="@/assets/Lettuce.jpg" />
              <h2
                class="m-board1-t mt-14"
                style="
                  color: white;
                  display: flex;
                  justify-content: center;
                  font-weight: bold;
                  font-size: 18px;
                "
              >
                현재 우리가 필요한건 무엇일까?
              </h2>
            </div>
          </div>
          <div class="m-board" style="color: white" data-aos="flip-left">
            <div>
              <img src="@/assets/Lettuce.jpg" />
              <h2
                class="m-board1-t mt-14"
                style="
                  color: white;
                  display: flex;
                  justify-content: center;
                  font-weight: bold;
                  font-size: 18px;
                "
              >
                현재 우리가 필요한건 무엇일까?
              </h2>
            </div>
          </div>
        </div>
      </div>
      <img src="@/assets/Crop_main.jpg" />
    </div>
  </div>

  <div class="info_btn">
    <RouterLink to="/crop" class="text-purple-700">
      <div class="home_btn">
        <p>농산물 취급 이동하기</p>
      </div>
    </RouterLink>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import "aos/dist/aos.css"; // AOS 애니메이션 스타일 추가
import AOS from "aos";
import CropView from "@/views/CropView.vue";

export default defineComponent({
  name: "HomeInfo",
  components: {
    CropView,
  },
  mounted() {
    AOS.init({
      duration: 1100,
    });
  },
});
</script>

<style scoped>
.info {
  display: flex;
  justify-content: center;
  text-align: center;
  vertical-align: auto;
  margin-top: 130px;
  height: 700px;
  background-color: #fff6ee;
}
.info_title {
  font-size: 28px;
}
.info h1 {
  font-size: 30px;
  font-weight: 600;
}
.info_board img {
  margin-top: 60px;
  width: 500px;
  height: 300px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.4);
}
.info_board .board-1 {
  transition: opacity 0.5s ease-in-out;
}
.info_board .board-2 {
  transition: opacity 1s ease-in-out;
}
.image-container {
  position: relative;
  width: 100%;
}
.image-overlay {
  position: absolute;
  top: 0px;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
}
.info_mission {
  display: block;
  justify-content: center;
  text-align: center;
  height: 700px;
  margin-bottom: 100px;
  position: relative;
}
.info_mission p {
  margin: 50px 0;
  font-size: 30px;
  font-weight: 600;
  color: white;
}
.info_mission img {
  width: 100%;
  height: 700px;
}
.m-board1 img {
  width: 200px;
  height: 100%;
}
.board-1 {
  transition: opacity 0.5s ease-in-out;
}
.board-2 {
  transition: opacity 2s ease-in-out;
}
.board-3 {
  transition: opacity 4s ease-in-out;
}
.board-4 {
  transition: opacity 5s ease-in-out;
}

.mission-board {
  display: flex;
  justify-content: center;
}
.m-board {
  justify-content: center;
  margin: 5px;
  border-radius: 8px;
  width: 250px;
  height: 380px;
  background-color: rgba(146, 146, 146, 0.6);
}
.mission-board img {
  width: 100%;
  height: 220px;
}
.board-text {
  font-size: 18px;
  margin-top: 4px;
}
.info_btn {
  display: flex;
  justify-content: center;
  align-content: center;
}
.home_btn {
  width: 400px;
  height: 60px;
  background-color: orange;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 110px;
}
.home_btn p {
  font-size: 16px;
  font-weight: bold;
  color: white;
}
</style>
