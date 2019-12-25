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
  </div>
</template>

<script>
import Header from '../header/header'
// import request from '../../../request/request'
import Question from './Question'
import { QUESTIONS, OPTIONS } from '../Constant'

export default {
  name: 'Home',

  components: {
    Question,
    Header
  },

  data () {
    return {
      loading: false,
      questions: QUESTIONS,
      options: OPTIONS
    }
  },

  created () {
    // request({
    //   url: '/',
    //   method: 'get'
    // }).then(res => {
    // })
  },

  methods: {}
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
