import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import 'swiper/swiper-bundle.css';
import './assets/main.css'

// production 단계에서 여기
axios.defaults.baseURL = 'http://3.35.171.162'

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)

app.mount('#app')
