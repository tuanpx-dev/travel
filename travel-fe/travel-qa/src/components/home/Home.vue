<template>
  <div class="container home">
    <Header/>
    <div class="row home-content">
      <div class="row home-list-qa col-md-9">
        <div class="home-sidebar col-md-4">
          <select name="" id="" class="select-region">
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="mercedes">Mercedes</option>
            <option value="audi">Audi</option>
          </select>
          <div>
            <div v-for="option in options" :key="option.value" class="home-add-option">
              <input type="checkbox">
              <p>{{ option.name }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-8 list-qa">
          <div class="home-header">
            <input type="search" placeholder="search"/>
          </div>
          <div class="home-menu">
            <button class="home-menu-page">Popular</button>
            <button class="home-menu-page new">New</button>
          </div>
          <div class="home-list" v-for="question in questions" :key="question.id">
            <Question :question="question" :page="'home'"/>
          </div>
        </div>
      </div>

      <div class="col-md-3"></div>
    </div>

    <paginate
      :page-count="totalPage"
      :click-handler="handlePage"
      :prev-text="'Prev'"
      :next-text="'Next'">
    </paginate>
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import Header from '../header/header'
import request from '../../../request/request'
import Question from './Question'
import { URL } from '../../api/URL'
import Paginate from 'vuejs-paginate'

export default {
  name: 'Home',

  components: {
    Question,
    Header,
    Paginate
  },

  data () {
    return {
      totalPage: 0,
      loading: false,
      questions: [],
      options: []
    }
  },

  created () {
    this.getQuestion()
    this.getCategory()
  },

  updated () {
    EventBus.$on('closeFormCreateASK', () => {
      this.getQuestion()
    })
  },

  methods: {
    getQuestion () {
      request({
        url: URL.QUESTIONS,
        method: 'get'
      })
        .then(res => {
          this.questions = res.data.content
          this.totalPage = this.questions.length / res.data.limit
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    getCategory () {
      request({
        url: URL.CATEGORY,
        method: 'get'
      })
        .then(res => {
          this.options = res.data
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    handlePage () {

    }
  }
}
</script>

<style lang="css" scoped>
.home-header {
  margin-bottom: 30px;
}

.home-content {
  margin-top: -40px;
}

.home-header input {
  border: 1px solid #ccc;
  border-radius: 10px;
  height: 40px;
  outline: none;
  padding: 20px;
  width: 100%;
  margin: 0 auto;
}

.home-sidebar {
  border: 1px solid gray;
  max-height: 500px;
  text-align: left;
  margin-top: 73px;
}

.select-region {
  width: 70%;
  height: 35px;
  margin-top: 30px;
  margin-bottom: 20px;
  background-color: white;
  outline: none;
}

.home-add-option {
  display: flex;
  margin: 5px;
}

.home-add-option input[type="checkbox"]{
  margin-right: 20px;
}

.list-qa {
}

.home-list {
}

.home-menu {
  text-align: left;
}

.home-menu .new{
  margin-left: -6px;
}

.home-menu-page {
  padding: 5px 15px;
  color: black;
  background-color: white;
}
</style>
