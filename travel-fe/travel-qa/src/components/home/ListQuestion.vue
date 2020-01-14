<template>
  <div class="col-md-8 col-xs-12 list-qa">
    <div class="home-header">
      <input type="search" placeholder="search by keyword"/>
      <div class="search">
        <i class="fa fa-search"></i> &nbsp;
        <p>search</p>
      </div>
    </div>
    <div class="home-menu">
      <div class="home-menu-page arrow_box">Popular</div>
      <div class="home-menu-page">New ></div>
      <div class="home-menu-page">Relation ></div>
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
      v-if="!loading"
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
.list-qa {
  padding: 0;
}

.home-header {
  margin-bottom: 30px;
  position: relative;
  padding: 0 10px;
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

.search {
  display: none;
  position: absolute;
  right: 10px;
  top: 0px;
  background-color: #CBE0FF;
  height: 42px;
  border-radius: 0 10px 10px 0;
  padding: 10px;
  text-align: center;
}

.home-menu {
  text-align: center;
  display: flex;
}

.home-menu-page {
  padding: 5px 15px;
  color: black;
  background-color: white;
  border: 1px solid #ccc;
  font-weight: 700;
}

/* panigation */
.b-pagination {
  float: right;
}

@media only screen and (max-width: 600px) {
  .home-menu {
    width: 100%;
  }

  .search {
    display: flex;
  }

  .home-menu-page {
    width: calc(100% /3);
    background-color: #CBE0FF;
    border: 1px solid #8BA9F2;
    color: #2C65E7;
  }

  .arrow_box {
    position: relative;
    background: #2761E6;
    border: 1px solid #c2e1f5;
    color: #fff;
  }
  .arrow_box:after, .arrow_box:before {
    top: 100%;
    left: 50%;
    border: solid transparent;
    content: " ";
    height: 0;
    width: 0;
    position: absolute;
    pointer-events: none;
  }

  .arrow_box:after {
    border-color: rgba(136, 183, 213, 0);
    border-top-color: #2761E6;
    border-width: 10px;
    margin-left: -10px;
  }
  .arrow_box:before {
    border-color: rgba(194, 225, 245, 0);
    border-top-color: #c2e1f5;
    border-width: 10px;
    margin-left: -10px;
  }
}
</style>
