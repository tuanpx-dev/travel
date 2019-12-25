import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '../components/home/Home'
import ResetPassWord from '@/components/ResetPassWord'

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
      path: '/home',
      name: 'Home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    }
  ],
  mode: 'history'
})

export default router

router.beforeEach((to, from, next) => {
  var user = JSON.parse(localStorage.getItem('user'))
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
