<template>
    <TransitionRoot as="template" :show="open">
      <Dialog class="relative z-10" @close="closeCart">
        <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>
  
        <div class="fixed inset-0 overflow-hidden">
          <div class="absolute inset-0 overflow-hidden">
            <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
              <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
                <DialogPanel class="pointer-events-auto w-screen max-w-md">
                  <div class="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
                    <div class="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
                      <div class="flex items-start justify-between">
                        <DialogTitle class="text-lg font-medium text-gray-900">Shopping cart</DialogTitle>
                        <div class="ml-3 flex h-7 items-center">

                        </div>
                      </div>
  
                      <div class="mt-8">
                        <div class="flow-root">
                          <ul role="list" class="-my-6 divide-y divide-gray-200">
                            <li v-for="product in products" :key="product.id" class="flex py-6">
                              <div class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
                                <img :src="product.imageSrc" class="h-full w-full object-cover object-center" />
                              </div>
  
                              <div class="ml-4 flex flex-1 flex-col">
                                <div>
                                    <div class="flex justify-between text-base font-medium text-gray-900">
                                      <h3>
                                        <a :href="product.href">{{ product.specific }}</a>
                                      </h3>
                                      <p class="ml-4">{{ product.price }}</p>
                                    </div>
                                    <p class="mt-1 text-sm text-gray-500">{{ product.name }}</p>
                                  </div>
                                  <div class="flex flex-1 items-end justify-between text-sm">
                                    <div class="flex items-center">
                                      <button @click="decreaseQuantity(product.id)" class="font-medium text-indigo-600 hover:text-indigo-500">-</button>
                                      <p class="mx-2 text-gray-500">수량 : {{ product.quantity }}</p>
                                      <button @click="increaseQuantity(product.id)" class="font-medium text-indigo-600 hover:text-indigo-500">+</button>
                                    </div>
                                    <div class="flex">
                                      <button type="button" class="font-medium text-indigo-600 hover:text-indigo-500" @click="removeProduct(product.id)">제거</button>                                  </div>
                                    </div>
                                </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
  
                    <div class="border-t border-gray-200 px-4 py-6 sm:px-6">
                      <div class="flex justify-between text-base font-medium text-gray-900">
                        <p>총 금액</p>
                        <p>{{totalPrice+3000}}원</p>
                      </div>
                      <p class="mt-0.5 text-sm text-gray-500">배송비 : 3000원</p>
                      <div class="mt-6">
                        <RouterLink to="/order" class="flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700"
                        @click.native="closeCart">                    
                        주문
                        </RouterLink>
                      </div>
                      <div class="mt-6 flex justify-center text-center text-sm text-gray-500">

                      </div>
                    </div>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </template>

  <script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
  import { XMarkIcon } from '@heroicons/vue/24/outline'
  import { RouterLink } from 'vue-router'

  const props = defineProps({
    open: Boolean
  })

  const emit = defineEmits(['close-cart']);
  const products = ref([])
  onMounted(() => {
    const cart = JSON.parse(sessionStorage.getItem('cart')) || [];
    products.value = cart;
  })
  watch(() => props.open, (newVal) => {
    if (newVal) {
      const cart = JSON.parse(sessionStorage.getItem('cart')) || [];
      products.value = cart;
    }
  });


  function removeProduct(productId) { 
      products.value = products.value.filter(product => product.id !== productId)
      sessionStorage.setItem('cart', JSON.stringify(products.value))
  }
  function increaseQuantity(productId) {
    const product = products.value.find(product => product.id === productId)
    if (product) {
      product.quantity++
      sessionStorage.setItem('cart', JSON.stringify(products.value))
    }
  }
  function decreaseQuantity(productId) {
    const product = products.value.find(product => product.id === productId)
    if (product && product.quantity > 1) {
      product.quantity--
      sessionStorage.setItem('cart', JSON.stringify(products.value))
    }
  }
  function closeCart() {
    emit('close-cart')
  }
  const totalPrice = computed(() => {
    return products.value.reduce((sum, product) => sum + product.price * product.quantity, 0)
  })
  
  </script>
