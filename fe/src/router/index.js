import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import HomeView from '../views/HomeView.vue'
import FeedView from '../views/FeedView.vue'
import CropView from '../views/CropView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import PostView from '../views/PostView.vue'
import TrendView from '../views/TrendView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import SalesView from '../views/SalesView.vue'
import OrderPage from '../views/OrderPage.vue'
import OrderHistory from '../views/OrderHistory.vue'
import NonProductFeedView from '../views/NonProductFeedView.vue'

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
      path: '/nonproductfeed',
      name: 'nonproductfeed',
      component: NonProductFeedView
    },
    {
      path: '/crop',
      name: 'crop',
      component: CropView
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
      path: '/trends/:id',
      name: 'trendview',
      component: TrendView
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView,
      meta: {
        isAuthenticated: true,
      }
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView,
      meta: {
        isAuthenticated: true,
      }
    },
    {
      path: '/seller/sales',
      name: 'sales',
      component: SalesView,
      meta: {
        isAuthenticated: true,
        isSeller: true
      }
    },
    {
      path: '/order',
      name: 'OrderPage',
      component: OrderPage,
      beforeEnter: (to, from, next) => {
        const userStore = useUserStore()
        if (userStore.user.isAuthenticated) {
          next()
        } else {
          next('/login')
        }
      }
    },
    {
      path: '/orderhistory',
      name: 'OrderHistory',
      component: OrderHistory,
      meta: {
        isAuthenticated: true,
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  const requiresAuth = to.matched.some(record => record.meta.isAuthenticated)
  const requiresSeller = to.matched.some(record => record.meta.isSeller)

  if (requiresAuth && !userStore.user.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (requiresSeller && !userStore.user.isSeller) {
    return next({ name: 'home' })
  }

  next()
})

export default router
