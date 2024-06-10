import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import 'swiper/swiper-bundle.css';
import './assets/main.css'
import AOS from 'aos';
import 'aos/dist/aos.css';

// production 단계에서 여기
axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)
app.use(AOS.init({
    offset: 1050, // 스크롤 위치와 애니메이션의 시작 위치 조정
  }))

app.mount('#app')

