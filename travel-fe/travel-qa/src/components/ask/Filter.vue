<template>
  <div>
    <div v-if="!loading">
       <div class="filter-category">
        <p class="filter-title">Category</p>
        <div v-for="category in categorys" :key="category.id" class="category-item">
          <input type="checkbox" name="" id="">
          <p>{{ category.name }}</p>
        </div>
      </div>
      <div class="filter-area">
        <p class="filter-title">Area</p>

        <div v-for="(area, index) in areas" :key="index" class="list-option">
          <select  v-model="area.start">
            <option value="">--- Select ---</option>
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="mercedes">Mercedes</option>
            <option value="audi">Audi</option>
          </select>

          <select v-model="area.end">
            <option value="">--- Select ---</option>
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="mercedes">Mercedes</option>
            <option value="audi">Audi</option>
          </select>
        </div>

        <div class="add-area">
          <p class="area-item" @click="addArea"> + </p>
          <p>create</p>
        </div>
      </div>
    </div>

    <div v-else>
      <b-spinner class="m-5"></b-spinner>
    </div>
  </div>
</template>

<script>
import request from '../../../request/request'
import { URL } from '../../api/URL'

export default {
  name: 'Filter',

  data () {
    return {
      categorys: [],
      areas: [{ start: '', end: '' }],
      loading: true
    }
  },

  created () {
    this.getListCategory()
    this.getListArea()
  },

  methods: {
    getListCategory () {
      request({
        url: URL.CATEGORY,
        method: 'get'
      })
        .then(res => {
          this.categorys = res.data
          this.loading = false
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    getListArea () {
      request({
        url: URL.AREA,
        method: 'get'
      })
        .then(res => {
          this.areas = res.data
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    addArea () {
      this.areas.push({
        start: '',
        end: ''
      })
    }
  }
}
</script>

<style lang="css" scoped>
.filter-category {
  margin-left: 10px;
}

.filter-title {
  font-weight: 600;
  margin-bottom: 0;
}

.category-item {
  display: flex;
  margin-left: 15px;
  align-items: center;
  line-height: 0;
}

.category-item p {
  padding-top: 15px;
  margin-left: 15px;
}

.filter-area {
  margin-left: 10px;
}

.list-option {
  margin-left: 10px
}

.list-option select {
  width: 150px;
  height: 35px;
  padding-left: 5px;
  margin-bottom: 10px;
}

.add-area {
  display: flex;
  margin-left: 10px
}

.area-item {
  border: 2px solid #ccc;
  padding: 1px 7px;
  border-radius: 50%;
  margin-right: 5px;
}
</style>
