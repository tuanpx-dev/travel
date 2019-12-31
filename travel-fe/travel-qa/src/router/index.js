import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '../components/home/Home'
import ResetPassWord from '@/components/ResetPassWord'
import DetailQuestion from '../components/detailQuestion/DetailQuestion'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '*',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/resetpassword',
      name: 'ResetPassWord',
      component: ResetPassWord,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/detail-question',
      name: 'DetailQuestion',
      component: DetailQuestion,
      meta: {
        requiresAuth: true
      }
    }
  ],
  mode: 'history'
})

export default router

router.beforeEach((to, from, next) => {
  var user = null
  if (localStorage.getItem('user')) {
    user = JSON.parse(localStorage.getItem('user'))
  }

  if (to.meta.requiresAuth === false) {
    next()
  } else {
    if (user != null) {
      next()
    } else {
      next('/login')
    }
  }
})
