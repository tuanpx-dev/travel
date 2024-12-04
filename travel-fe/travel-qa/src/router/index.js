import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '../components/home/Home'
import ResetPassWord from '@/components/ResetPassWord'
import DetailQuestion from '../components/detailQuestion/detailQuestion'
import ListQuestion from '../components/home/ListQuestion'
import Profile from '../components/profile/Profile'
import ProfileUser from '../components/profile/ProfileUser'
import MyQuestion from '../components/profile/MyQuestion'
import MyAnswers from '../components/profile/MyAnswers'
import View from '../components/View'

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
      name: 'View',
      component: View,
      meta: {
        requiresAuth: false
      },
      children: [
        {
          path: '/home',
          name: 'Home',
          component: Home,
          children: [
            {
              path: '/',
              name: 'ListQuestion',
              component: ListQuestion,
              meta: {
                requiresAuth: false
              }
            },
            {
              path: '/detail-question',
              name: 'DetailQuestion',
              component: DetailQuestion,
              meta: {
                requiresAuth: false
              }
            }
          ]
        },
        {
          path: '/profile',
          name: 'Profile',
          component: Profile,
          meta: {
            requiresAuth: true
          },
          children: [
            {
              path: '/profile',
              name: 'ProfileUser',
              component: ProfileUser,
              meta: {
                requiresAuth: true
              }
            },
            {
              path: '/myQuestion',
              name: 'MyQuestion',
              component: MyQuestion,
              meta: {
                requiresAuth: true
              }
            },
            {
              path: '/myAnswers',
              name: 'MyAnswers',
              component: MyAnswers,
              meta: {
                requiresAuth: true
              }
            }
          ]
        }
      ]
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
