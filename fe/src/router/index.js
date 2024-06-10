import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import PostView from '../views/PostView.vue'
import TrendView from '../views/TrendView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import OrderPage from '../views/OrderPage.vue'
import OrderHistory from '../views/OrderHistory.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/post/:id', // 포스트 상세 페이지 경로 설정
      name: 'postview',
      component: PostView
    },
    {
      path: '/trends/:id',
      name: 'trendview',
      component: TrendView
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/order',
      name: 'OrderPage',
      component: OrderPage
    },
    {
      path: '/orderhistory',
      name: 'OrderHistory',
      component: OrderHistory
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
