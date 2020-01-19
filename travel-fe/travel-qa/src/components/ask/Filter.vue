<template>
  <div>
    <div v-if="!loading">
      <div class="filter-category">
        <p class="filter-title">Category</p>
        <div v-for="category in categorys" :key="category.id" class="category-item">
          <input type="checkbox" name="" id="" @change="checkcategory(category)">
          <p>{{ category.name }}</p>
        </div>
      </div>

      <div v-if="showborder" class="border-content-ask"></div>
      <div v-else class="border-content-profile"></div>

      <div class="filter-area">
        <p class="filter-title">Area</p>

        <div v-for="(area, index) in areas" :key="index" class="list-option">
          <select  v-model="area.province_id" @change="handleArea('province', area, index)">
            <option value="">Select province</option>
            <option v-for="item in listProvince" :key="item.id" :value="item.id">{{ item.name }}</option>
          </select>

          <select v-model="area.area_id" @change="handleArea('area', area, index)" :disabled="area.listArea.length < 1">
            <option value="">Select area</option>
            <option v-for="item in area.listArea" :key="item.id" :value="item.id">{{ item.name }}</option>
          </select>

          <select v-model="area.city_id" @change="handleArea('city', area, index)" :disabled="area.listCity.length < 1">
            <option value="">Select city</option>
            <option v-for="item in area.listCity" :key="item.id" :value="item.id">{{ item.name }}</option>
          </select>

          <select v-model="area.station_id" @change="handleArea('station', area, index)" :disabled="area.listStation.length < 1">
            <option value="">Select station</option>
            <option v-for="item in area.listStation" :key="item.id" :value="item.id">{{ item.name }}</option>
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
import { EventBus } from '../../eventBus'

export default {
  name: 'Filter',
  props: ['showborder', 'filter'],
  data () {
    return {
      categorys: [],
      areas: [{
        province_id: '',
        city_id: '',
        area_id: '',
        station_id: '',

        listCity: [],
        listArea: [],
        listStation: []
      }],
      loading: true,
      listFilter: [],
      listCategory: [],

      listProvince: []
    }
  },

  created () {
    this.getListCategory()
    this.getListProvince()
    if (this.filter) {
      this.getListFilter()
    }
  },

  methods: {
    getListFilter () {
      this.areas = this.filter.areas.map((el, index) => {
        return {
          province_id: el.province.id,
          city_id: el.city.id,
          area_id: el.area.id,
          station_id: el.station.id,

          listCity: [],
          listArea: [],
          listStation: []
        }
      })

      this.areas = this.filter.areas.map((el, index) => {
        this.filterCity(index)
        this.filterArea(index)
        this.filterStation(index)
        return {
          province_id: el.province.id,
          city_id: el.city.id,
          area_id: el.area.id,
          station_id: el.station.id,

          listCity: [],
          listArea: [],
          listStation: []
        }
      })
    },

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

    getListProvince () {
      request({
        url: URL.PROVINCE,
        method: 'get'
      })
        .then(res => {
          this.listProvince = res.data
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
        province_id: '',
        city_id: '',
        area_id: '',
        station_id: '',

        listCity: [],
        listArea: [],
        listStation: []
      })
    },

    checkcategory (category) {
      if (this.listFilter.filter(el => el === category.name).length > 0) {
        this.listFilter = this.listFilter.filter(el => el !== category.name)
        this.listCategory = this.listCategory.filter(el => el !== category.id)
      } else {
        this.listFilter.push(category.name)
        this.listCategory.push(category.id)
      }

      EventBus.$emit('addFilter', this.listFilter)
      EventBus.$emit('addCategory', this.listCategory)
    },

    handleArea (key, area, index) {
      if (key === 'province') {
        this.filterCity(index)
        this.areas[index].city_id = ''
        this.areas[index].area_id = ''
        this.areas[index].station_id = ''
      }

      if (key === 'city') {
        this.filterArea(index)
        this.filterStation(index)
        this.areas[index].area_id = ''
        this.areas[index].station_id = ''
      }

      if (key === 'area') {}

      if (key === 'station') {}

      let listArea = this.areas.map(el => `${el.province_id} > ${el.station_id}`)

      EventBus.$emit('addFilter', this.listFilter.concat(listArea))
      this.$emit('addArea', this.areas)
    },

    filterCity (index) {
      let provinceId = this.areas[index].province_id
      request({
        url: URL.CITY(provinceId),
        method: 'get'
      })
        .then(res => {
          this.areas[index].listCity = res.data
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    filterArea (index) {
      let cityId = this.areas[index].city_id
      request({
        url: URL.AREA(cityId),
        method: 'get'
      })
        .then(res => {
          this.areas[index].listArea = res.data
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    filterStation (index) {
      let cityId = this.areas[index].city_id
      request({
        url: URL.STATION(cityId),
        method: 'get'
      })
        .then(res => {
          this.areas[index].listStation = res.data
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
  margin-left: 10px;
  border-bottom: 1px solid #CBE0FF;
  margin-bottom: 3px;
  margin-top: 10px;
}

.list-option select {
  width: 45%;
  max-width: 150px;
  height: 35px;
  padding-left: 5px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
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

.border-content-ask {
  border-top: 1px solid #2761E6;
  height: 5px;
  background-color: #CBE0FF;
  margin-bottom: 5px;
}

.border-content-profile {
  border-bottom: 1px solid #CBE0FF;
  margin-left: 10px;
}
</style>
