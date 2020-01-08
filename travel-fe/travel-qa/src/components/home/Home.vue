<template>
  <div class="row home-content">
    <div class="home-list-qa col-md-9 col-xs-12">
      <div class="home-sidebar col-md-4 col-xs-0">
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
      <router-view/>
    </div>

    <div class="col-md-3 col-xs-0"></div>
  </div>
</template>

<script>
import Header from '../header/header'
import request from '../../../request/request'
import ListQuestion from './ListQuestion'
import Question from './Question'
import { URL } from '../../api/URL'
import Paginate from 'vuejs-paginate'

export default {
  name: 'Home',

  components: {
    Question,
    ListQuestion,
    Header,
    Paginate
  },

  data () {
    return {
      options: []
    }
  },

  created () {
    this.getCategory()
  },

  methods: {
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
    }
  }
}
</script>

<style lang="css" scoped>
.home-content {
  margin-top: -40px;
}

.home-list-qa {
  display: flex;
  padding: 0;
}

.home-sidebar {
  border: 1px solid gray;
  max-height: 500px;
  text-align: left;
  margin-top: 73px;
  margin-right: 10px;
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

/* panigation */
.b-pagination {
  float: right;
}

@media only screen and (max-width: 600px) {
  .home-sidebar  {
    display: none;
  }

  .home-content {
    margin-top: 0;
  }
}
</style>
