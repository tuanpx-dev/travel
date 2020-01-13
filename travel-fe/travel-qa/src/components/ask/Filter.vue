<template>
  <div>
    <div class="filter-category">
      <p>Category</p>
      <div v-for="category in categorys" :key="category.id" class="category-item">
        <input type="checkbox" name="" id="">
        <p>{{ category.name }}</p>
      </div>
    </div>
    <div class="filter-area">
      <p>Area</p>
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
      categorys: []
    }
  },

  created () {
    this.getListCategory()
  },

  methods: {
    getListCategory () {
      request({
        url: URL.CATEGORY,
        method: 'get'
      })
        .then(res => {
          this.categorys = res.data
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
.filter-category {
  margin-left: 10px;
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
</style>
