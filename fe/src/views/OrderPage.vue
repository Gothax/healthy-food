<template>
  <div class="order-page">
    <h1 class="text-2xl font-bold mb-4">주문하기</h1>
    <div class="order-summary">
      <div class="user-info">
        <div>
          <label for="real_name" class="block text-sm font-medium text-gray-700">이름:</label>
          <input v-model="user.real_name" :placeholder="user.real_name || '이름을 입력하세요'" id="real_name" type="text" class="input-field" />
        </div>

        <div>
          <label for="phone_number" class="block text-sm font-medium text-gray-700">전화번호:</label>
          <input v-model="user.phone_number" :placeholder="user.phone_number || '받는 분 연락처'" id="phone_number" type="text" class="input-field" />
        </div>

        <div>
          <label for="address" class="block text-sm font-medium text-gray-700">주소:</label>
          <input v-model="user.address" :placeholder="user.address || '주소'" id="address" type="text" class="input-field" />
        </div>

        <div>
          <label for="detailed_address" class="block text-sm font-medium text-gray-700">상세 주소:</label>
          <input v-model="user.detailed_address" :placeholder="user.detailed_address || '상세 주소'" id="detailed_address" type="text" class="input-field" />
        </div>
      </div>
      <div v-for="product in products" :key="product.id" class="product-item mt-4">
        <div class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
          <img :src="product.imageSrc" class="h-full w-full object-cover object-center" />
        </div>
        <p>{{ product.specific }} - {{ product.quantity }}개</p>
        <p>{{ product.price }}원</p>
      </div>
      <p class="mt-4">총 금액: {{ totalPrice + 3000 }}원 (배송비 포함)</p>
      <button @click="requestPay()" class="mt-4 bg-indigo-600 text-white px-4 py-2 rounded">결제</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'OrderPage',

  data() {
    return {
      products: JSON.parse(sessionStorage.getItem('cart')) || [],
      user: {
        real_name: '',
        phone_number: '',
        address: '',
        detailed_address: ''
      }
    }
  },

  computed: {
    totalPrice() {
      return this.products.reduce((sum, product) => sum + product.price * product.quantity, 0)
    },
    isFormValid(){
        return this.user.real_name && this.user.phone_number && this.user.address && this.user.detailed_address
    }
  },

  mounted() {
    this.fetchUserData()
    if (window.IMP) {
      window.IMP.init('imp62067428')
    }
  },

  methods: {
    requestPay() {
      if (!this.isFormValid) {
        alert('모든 필수 정보를 입력해주세요.');
        return;
      }
      const today = new Date()
      const hours = today.getHours()
      const minutes = today.getMinutes()
      const seconds = today.getSeconds()
      const milliseconds = today.getMilliseconds()
      const makeMerchantUid = hours + minutes + seconds + milliseconds

      IMP.request_pay({
        pg: 'kakaopay',
        merchant_uid: "IMP" + makeMerchantUid,
        name: this.products.length > 0 ? this.products[0].specific : '상품명',
        amount: this.totalPrice + 3000,
        buyer_email: this.user.email,
        buyer_name: this.user.real_name,
        buyer_tel: this.user.phone_number,
        buyer_addr: this.user.address,
        buyer_postcode: '123-456'
      }, function (rsp) { // callback
        if (rsp.success) {
          console.log(rsp)
          // 결제 성공 시 주문 생성
          this.createOrder()
        } else {
          console.log(rsp)
          alert('결제에 실패했습니다. 다시 시도해주세요.')
        }
      }.bind(this))
    },

    fetchUserData() {
      axios.get('/api/me/noimg/')
        .then(response => {
          this.user = response.data
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    createOrder() {
      if (this.products.length === 0) {
        alert('장바구니에 상품이 없습니다.')
        return
      }
      const order = {
        products: this.products,
        totalPrice: this.totalPrice + 3000,
        createdAt: new Date(),
        user: this.user
      }
      axios
        .post('/api/orders/create/', {
          order: order,
        })
        .then(response => {
          console.log('data', response.data)
          sessionStorage.removeItem('cart')
          this.$router.push(`/profile/${this.user.id}`)
        })
        .catch(error => {
          console.log('error', error)
        })
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.order-summary {
  border: 1px solid #e5e7eb;
  padding: 20px;
  border-radius: 8px;
}
.input-field {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}
.product-item {
  margin-top: 10px;
}
</style>