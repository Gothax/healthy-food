<template>
  <div>
    <h1>Order History</h1>
    <div v-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="order-item">
        <h2>Order #{{ order.id }}</h2>
        <p>Date: {{ new Date(order.created_at).toLocaleString() }}</p>
        <p>Total: {{ order.get_total_price + 3000}}원</p>
        <div v-for="item in order.order_items" :key="item.product.id" class="order-product">
          <p>Product: {{ item.product.name }}</p>
          <p>Quantity: {{ item.quantity }}</p>
          <p>Price: {{ item.get_total_item_price }}원</p>
          <div v-if="item.review">
            <RouterLink :to="{ name: 'postview', params: { id: item.review.id } }">작성한 리뷰 보기</RouterLink>
          </div>
          <div v-else>
            <div>
              <ModalView v-if="isModalViewed[item.id]" @close-modal="isModalViewed[item.id] = false">
                <ReviewForm :product="item.product" :orderItem="item" />
              </ModalView>
              <button @click="openModal(item.id)" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300">
                리뷰 작성하기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>주문 내역이 없습니다.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ModalView from '../components/ModalView.vue';
import ReviewForm from '../components/ReviewForm.vue';

export default {
  data() {
    return {
      orders: [],
      isModalViewed: {}
    };
  },
  created() {
    this.fetchOrderHistory();
  },
  components: {
    ModalView,
    ReviewForm
  },
  methods: {
    fetchOrderHistory() {
      axios
        .get('/api/orders/history/')
        .then(response => {
          this.orders = response.data.orders;
        })
        .catch(error => {
          console.error('Error fetching order history', error);
        });
    },
    openModal(itemId) {
      this.isModalViewed[itemId] = true;
    }
  }
};
</script>

<style>
.order-item {
  border: 1px solid #ccc;
  padding: 16px;
  margin-bottom: 16px;
}
.order-product {
  margin-left: 16px;
}
</style>
