<template>
<div>
    <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="post.created_by.get_userimage" class="w-[40px] rounded-full">
            
            <p>
                <strong>
                    <RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink>
                </strong>
            </p>
        </div>


        <div v-if="userStore.user.id == post.created_by.id">
            <div @click="toggleOptionModal" class="cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                </svg>   
            </div>   

        <div>
          <div class="modal-wrap" v-show="showOptionModal" @click="closeModal">
            <div class="modal-container" @click.stop="">
              <div class="flex items-center space-x-2 cursor-pointer mb-3" @click="toggleFeedModify" v-if="userStore.user.id == post.created_by.id">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-black-500">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232a2.828 2.828 0 114 4L9 19 5 20l1-4 10.232-10.768z"/>
                </svg>
                <div class="text-black-500 text-xs cursor-pointer">
                  Modify post
                </div>
              </div>
              <div class="flex items-center space-x-2 cursor-pointer mt-3" @click="deletePost" v-if="userStore.user.id == post.created_by.id">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"/>
                </svg>

                <div class="text-red-500 text-xs cursor-pointer">
                  Delete post
                </div>
              </div>
            </div>
          </div>

          <!-- FeedModify 모달 -->
          <div v-if="showFeedModify" class="modal-wrap" @click="closeFeedModify">
            <div class="modal-container" @click.stop="">
              <FeedModify :post="post" @close="closeFeedModify" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    

    <swiper :navigation="true" :pagination="{ clickable: true }">
        <swiper-slide v-for="image in post.attachments" :key="image.id" class="swiper-container">
            <img :src="image.get_image" class="max-w-full mb-4 rounded-xl flex justify-center items-center" style="margin: auto;">
        </swiper-slide>
    </swiper>

    <p>{{ post.body }}</p>

    <div v-if="post.content_type === 'product'" class="mt-4">
        <p class="text-gray-700 text-sm"><strong>상품 이름:</strong> {{ post.product.name }}</p>
        <p class="text-gray-700 text-sm"><strong>상품 설명:</strong> {{ post.product.specific }}</p>
        <p class="text-gray-700 text-sm"><strong>상품 가격:</strong> {{ post.product.price }}</p>
        <input v-model.number="productQuantity" type="number" min="1" class="mt-2 px-4 py-2 border rounded" placeholder="수량">
        <button @click="saveProductToSession(post.product)" class="mt-2 px-4 py-2 bg-blue-500 text-white rounded">장바구니에 담기</button>
    </div>

    <div class="my-6 flex justify-between">
        <div class="flex space-x-6">
            <div class="flex items-center space-x-2" @click="likePost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" :fill="isLiked ? 'red' : 'none'" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                </svg>  
                
                <span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
            </div>
            
            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"></path>
                </svg> 

                <div class="text-gray-500 text-xs">{{ post.comments_count }} comments</div>
            </div>
        </div>
    </div>
    <p class="text-gray-600">{{ post.created_at_formatted }} 전</p>

</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { Swiper, SwiperSlide } from 'swiper/vue';
import ModalView from "@/components/ModalView.vue";
import FeedModify from "@/components/FeedModify.vue";

export default {
    components: {
        Swiper,
        SwiperSlide,
        ModalView,
        FeedModify,
       },
    props: {
        post: Object
    },
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },
    
    data() {
        return {
            isLiked: false,
            showOptionModal: false,
            productQuantity: 1,
            isModalViewed: false,
            showFeedModify: false,

        }
    },
    
    mounted() {
        this.checkLikeStatus(this.post.id);
    },


    methods: {
        checkLikeStatus(id) {
        axios.post(`/api/posts/${id}/likestatus/`)
            .then(response => {
                this.isLiked = response.data.isLiked;
            })
            .catch(error => {
                console.error('Liked status check error', error);
            });
        },

        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == 'like created') {
                        this.post.likes_count += 1
                        this.isLiked=true;
                    }
                    else{
                        this.post.likes_count -= 1
                        this.isLiked=false
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)

            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'The post was deleted', 'bg-emerald-500')
                    this.$router.push({ name: 'profile', params: { id: this.userStore.user.id } })
                })
                .catch(error => {
                    console.log("error", error);
                })
        },
        toggleFeedModify() {
            this.showFeedModify = !this.showFeedModify;
            this.showOptionModal = false; // 옵션 모달을 닫음
        },
        closeFeedModify() {
            this.showFeedModify = false;
        },
        toggleOptionModal() {
            this.showOptionModal = !this.showOptionModal
        },
        closeModal(event) {
            if (event.target.classList.contains('modal-wrap')) {
                this.showOptionModal = false;
            }
        },
        saveProductToSession(product) {
            let cart = JSON.parse(sessionStorage.getItem('cart')) || [];
            
            const existingProduct = cart.find(item => item.id === product.id);
            if (existingProduct) {
                existingProduct.quantity += this.productQuantity;
            } else {
                const productWithQuantity = { ...product, quantity: this.productQuantity, imageSrc: this.post.attachments[0].get_image };
                cart.push(productWithQuantity);
            }
            sessionStorage.setItem('cart', JSON.stringify(cart));
            this.toastStore.showToast(3000, '상품이 장바구니에 담겼습니다.', 'bg-blue-500');
        }

    }
    
}
</script>

<style scoped>
.modal-wrap {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000; 
}
.modal-container {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 550px;
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
  z-index: 1001; 
}
.swiper-container {
    display : flex;
    justify-content: center;
    align-content: center;
    align-items: center;
    margin : auto;
}
</style>