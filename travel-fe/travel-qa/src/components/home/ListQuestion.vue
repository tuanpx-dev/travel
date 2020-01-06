<template>
  <div class="col-md-8 col-xs-12 list-qa">
    <div class="home-header">
      <input type="search" placeholder="search"/>
    </div>
    <div class="home-menu">
      <button class="home-menu-page">Popular</button>
      <button class="home-menu-page new">New</button>
      <button class="home-menu-page new">Relation</button>
    </div>
    <div v-if="!loading">
      <div class="home-list" v-for="question in questions" :key="question.id">
        <Question :question="question" :page="'home'"/>
      </div>
    </div>

    <div v-else>
      <b-spinner class="m-5"></b-spinner>
    </div>

    <b-pagination
      v-model="currentPage"
      :total-rows="totalPage"
      :hide-goto-end-buttons="true"
      per-page="limit"
      prev-text="Prev"
      next-text="Next"
      @change="handlePage"
    ></b-pagination>
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import request from '../../../request/request'
import Question from './Question'
import { URL } from '../../api/URL'
import Paginate from 'vuejs-paginate'

export default {
  name: 'ListQuestion',

  components: {
    Question,
    Paginate
  },

  data () {
    return {
      currentPage: 1,
      totalPage: 0,
      limit: 10,
      loading: true,
      questions: []
    }
  },

  created () {
    this.getQuestion(0)
  },

  updated () {
    EventBus.$on('closeFormCreateASK', () => {
      this.getQuestion(0)
    })
  },

  methods: {
    getQuestion (offset) {
      this.loading = true
      request({
        url: URL.QUESTIONS(offset),
        method: 'get'
      })
        .then(res => {
          this.loading = false
          this.questions = res.data.content
          this.totalPage = res.data.total_length
          this.limit = res.data.limit
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
