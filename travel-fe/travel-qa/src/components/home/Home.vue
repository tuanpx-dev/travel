<template>
  <div class="container home">
    <div class="row home-header">
      <div class="col-md-3">
        <button class="button-ask">Ask</button>
      </div>

      <input class="col-md-6" type="search" />
    </div>
    <div class="row home-content">
      <div class="row home-list-qa col-md-9">
        <div class="home-sidebar col-md-4"></div>
        <div class="col-md-8 list-qa">
          <div class="home-menu">
            <button class="home-menu-page">Popular</button>
            <button class="home-menu-page">New</button>
          </div>
          <div class="home-list" v-for="question in questions" :key="question.id">
            <Question :question="question"/>
          </div>
        </div>
      </div>

      <div class="col-md-3"></div>
    </div>
  </div>
</template>

<script>
import request from '../../../request/request'
import Question from './Question'

export default {
  name: 'Home',

  components: {
    Question
  },

  data () {
    return {
      loading: false,
      questions: [
        {
          id: 1
        },
        {
          id: 2
        }
      ]
    }
  },

  created () {
    request({
      url: '/',
      method: 'get'
    }).then(res => {
    })
  },

  methods: {}
}
</script>

<style lang="css" scoped>
.home-header {
  margin-bottom: 30px;
}

.button-ask {
  padding: 10px 30px;
  border-radius: 20px;
  border: 1px solid #ccc;
  background-color: white;
  font-size: 24px;
  font-weight: 800;
  outline: none;
}

.home-header input {
  border: 1px solid #ccc;
  border-radius: 10px;
  height: 40px;
  outline: none;
}

.home-sidebar {
  border: 1px solid gray;
  max-height: 500px;
}

.list-qa {
  margin-top: -35px;
}

.home-list {
}

.home-menu {
  text-align: left;
}

.home-menu-page {
  padding: 5px 15px;
  color: black;
}
</style>
