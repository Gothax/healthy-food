<template>
  <div class="faq-container">
    <div class="faq-section" v-if="showSections || showShippingOptions">
      <button v-if="!showShippingOptions" @click="toggleShippingOptions">배송 문의</button>
      <div v-else class="sub-menu">
        <button @click="sendFAQ('일반상품 배송조회')">일반상품 배송조회</button>
        <button @click="sendFAQ('지연/누락/오배송/분실')">지연/누락/오배송/분실</button>
        <button @click="resetMenu">처음으로</button>
      </div>
    </div>

    <div class="faq-section" v-if="showSections || showLoginOptions">
      <button v-if="!showLoginOptions" @click="toggleLoginOptions">로그인 관련</button>
      <div v-else class="sub-menu">
        <button @click="sendFAQ('회원 탈퇴는 어떻게 하나요?')">회원 탈퇴는 어떻게 하나요?</button>
        <button @click="sendFAQ('비밀번호를 잊어버렸어요.')">비밀번호를 잊어버렸어요.</button>
        <button @click="resetMenu">처음으로</button>
      </div>
    </div>

    <div class="faq-section" v-if="showSections || showOrderOptions">
      <button v-if="!showOrderOptions" @click="toggleOrderOptions">주문 문의</button>
      <div v-else class="sub-menu">
        <button @click="sendFAQ('나의 주문 내역')">나의 주문 내역</button>
        <button @click="resetMenu">처음으로</button>
      </div>
    </div>

    <div class="faq-section" v-if="showSections">
      <button @click="sendFAQ('불량 문의')">불량 문의</button>
    </div>

    <div class="faq-section" v-if="showSections">
      <button @click="sendFAQ('상담원 문의')">상담원 문의</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['sendFAQMessage'],
  data() {
    return {
      showSections: true,
      showShippingOptions: false,
      showLoginOptions: false,
      showOrderOptions: false,
    };
  },
  methods: {
    resetMenu() {
      this.showSections = true;
      this.showShippingOptions = false;
      this.showLoginOptions = false;
      this.showOrderOptions = false;
    },
    toggleShippingOptions() {
      this.showSections = false;
      this.showShippingOptions = !this.showShippingOptions;
      this.showLoginOptions = false;
      this.showOrderOptions = false;
    },
    toggleLoginOptions() {
      this.showSections = false;
      this.showLoginOptions = !this.showLoginOptions;
      this.showShippingOptions = false;
      this.showOrderOptions = false;
    },
    toggleOrderOptions() {
      this.showSections = false;
      this.showOrderOptions = !this.showOrderOptions;
      this.showShippingOptions = false;
      this.showLoginOptions = false;
    },
    sendFAQ(question) {
      if (question === '불량 문의') {
        this.$emit('showEmailForm');
      } else {
        this.sendFAQMessage(question);
        this.resetMenu();
      }
    },
  },
};
</script>

<style>
.faq-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.faq-section {
  flex: 1 1 calc(33.33% - 10px);
  box-sizing: border-box;
}

.faq-section button {
  width: 100%;
  padding: 10px;
  background-color: #d6d5e1;
  border: 1px solid #040404;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.faq-section button:hover {
  background-color: #020101;
  color: white;
}

.sub-menu {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.sub-menu button {
  flex: 1 1 calc(33.33% - 10px);
}
</style>
