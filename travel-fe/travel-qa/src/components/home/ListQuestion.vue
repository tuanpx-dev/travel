<template>
  <div class="col-md-8 col-xs-12 list-qa">
    <div class="home-header">
      <input type="search" placeholder="search by keyword"/>
      <div class="search">
        <i class="fa fa-search"></i> &nbsp;
        <p>search</p>
      </div>
    </div>

    <div class="filter-home">
      <p class="title-filter-home">Filter: </p> &nbsp;&nbsp;
      <p v-for="(filter, index) in filters" :key="index" class="filter-item">{{filter}}</p>
      <p class="add-filter-home"  @click="showPopupFilter"> + </p>
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

    <modal
      name="home-filter-popup"
      width="80%"
      height="auto"
      :pivotY="0.1"
      :scrollable="true"
      :clickToClose="false">
      <div class="header-popup-filter">
        <p>Filter</p>
      </div>
      <Category />
      <div class="footer-popup-filter">
        <button class="cancel-popup" @click="closeFilter">Cancel</button>
        <button class="filter-home-action" @click="addFilterHome">Filter</button>
      </div>
    </modal>
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import request from '../../../request/request'
import Question from './Question'
import { URL } from '../../api/URL'
import Paginate from 'vuejs-paginate'
import Category from '../ask/Filter'

export default {
  name: 'ListQuestion',

  components: {
    Question,
    Paginate,
    Category
  },

  data () {
    return {
      currentPage: 1,
      totalPage: 0,
      limit: 10,
      loading: true,
      questions: [],
      filters: [],
      listFilter: []
    }
  },

  created () {
    this.getQuestion(0)
  },

  updated () {
    EventBus.$on('closeFormCreateASK', () => {
      this.getQuestion(0)
    })

    EventBus.$on('addFilter', (listFiler) => {
      this.listFilter = listFiler
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
    },

    showPopupFilter () {
      this.$modal.show('home-filter-popup')
    },

    closeFilter () {
      this.$modal.hide('home-filter-popup')
    },

    addFilterHome () {
      this.filters = this.listFilter
      this.$modal.hide('home-filter-popup')
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

.filter-home {
 display: none;
}

.add-filter-home {
  font-size: 25px;
  font-weight: 700;
  margin: 0;
}

.header-popup-filter {
  background-color: #2761E6;
  padding: 0;
  margin-bottom: 10px;
  text-align: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  padding-top: 20px;
}

.footer-popup-filter {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.cancel-popup {
  background: none;
  border: none;
  margin-right: 10px;
}

.title-filter-home {
  margin: 0;
}

.filter-home-action {
    background-color: #2761E6;
    margin-right: 10px;
    padding: 5px 20px;
    border-radius: 10px;
    border: 1px solid #2761E6;
    color: white;
}

.filter-item {
  margin: 0 10px;
  background-color: #CBE0FF;
  border-radius: 5px;
  padding: 0 5px;
}

@media only screen and (max-width: 600px) {
  .home-menu {
    width: 100%;
  }

  .home-header {
    margin-bottom: 15px;
  }

  .search {
    display: flex;
  }

  .filter-home {
    padding-left: 10px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 15px;
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
