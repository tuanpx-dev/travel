<template>
  <div class="col-md-8 list-qa">
    <div class="home-header">
      <input type="search" placeholder="search"/>
      <div class="search">
        <i class="fa fa-search"></i> &nbsp;
        <p>search</p>
      </div>
    </div>
    <!-- <div class="home-menu">
      <button class="home-menu-page arrow_box">Popular</button>
      <button class="home-menu-page new">New ></button>
      <button class="home-menu-page new">Relation ></button>
    </div> -->
    <div v-if="!loading" >
      <div class="home-list">
        <Question :question="questionDetail" :page="'detail-question'"/>

        <!-- <div>
          <div v-for="answer in answers" :key="answer.id">
            <Comment :answer="answer"/>
          </div>
        </div> -->
      </div>
    </div>
    <div v-else>
      <b-spinner class="m-5"></b-spinner>
    </div>
  </div>
</template>

<script>
import request from '../../../request/request'
import { URL, URL_INCOGNITO } from '../../api/URL'
import Question from '../home/Question'
import { EventBus } from '../../eventBus'

export default {
  name: 'DetailQuestion',

  components: {
    Question
    // Comment
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

  updated () {
    EventBus.$on('closeFormCreateASK', () => {
      this.getDetailQuestion()
    })
  },

  methods: {
    getDetailQuestion () {
      let url = URL.DETAIL_QUESTION(this.$route.query.id)

      if (!JSON.parse(localStorage.getItem('user'))) {
        url = URL_INCOGNITO.DETAIL_QUESTION(this.$route.query.id)
      }

      request({
        url: url,
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
      let url = ''

      if (!JSON.parse(localStorage.getItem('user'))) {
        url = URL_INCOGNITO.ANSWERS_QUESTION(id)
      } else {
        url = URL.ANSWERS_QUESTION(id)
      }

      request({
        url: url,
        method: 'get'
      })
        .then(res => {
          this.loading = false
          this.answers = res.data.content
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
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

@media only screen and (max-width: 600px) {
  .home-menu {
    width: 100%;
  }

  .search {
    display: flex;
  }

  .home-list {
    margin-top: -25px;
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
