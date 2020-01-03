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
            <button class="home-menu-page new">Relation</button>
          </div>
          <div>
            <div class="home-list">
              <Question :question="questionDetail" :page="'home'"/>

              <div v-if="!loading">
                <div v-for="answer in answers" :key="answer.id">
                  <Comment :answer="answer"/>
                </div>
              </div>

              <div v-else>
                <b-spinner class="m-5"></b-spinner>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3"></div>
    </div>
  </div>
</template>

<script>
import Header from '../header/header'
import request from '../../../request/request'
import { URL } from '../../api/URL'
import Question from '../home/Question'
import Comment from './Comment'

export default {
  name: 'Home',

  components: {
    Header,
    Question,
    Comment
  },

  data () {
    return {
      loading: true,
      questionDetail: {},
      answers: [],
      options: []
    }
  },

  created () {
    this.getDetailQuestion()
  },

  methods: {
    getDetailQuestion () {
      request({
        url: URL.DETAIL_QUESTION(this.$route.query.id),
        method: 'get'
      })
        .then(res => {
          this.questionDetail = res.data
          this.getListAnswer(this.questionDetail.id)
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    getListAnswer (id) {
      this.loading = true

      request({
        url: URL.ANSWERS_QUESTION(id),
        method: 'get'
      })
        .then(res => {
          this.loading = false
          // this.questions = res.data.content
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    handlePage (pageNumber) {
      const offset = (pageNumber - 1) * this.limit
      this.getQuestion(offset)
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

/* panigation */
.b-pagination {
  float: right;
}
</style>
