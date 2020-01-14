<template>
  <div class="my-question col-md-9">
    <div class="avartar-name mobile-profile">
      <img
        src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35"
        alt
      />
      <p>name</p>
    </div>
    <div class="border-content-profile mobile-profile"></div>

    <div v-for="question in questions" :key="question.id">
      <Question :question="question" :page="'myAnswer'"/>
    </div>
  </div>
</template>

<script>
import request from '../../../request/request'
import Question from '../home/Question'
import {URL} from '../../api/URL'
export default {
  name: 'MyAnswer',
  components: {
    Question
  },
  data () {
    return {
      loading: false,
      questions: []
    }
  },

  created () {
    request({
      url: URL.QUESTIONS(0),
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
  }
}
</script>

<style lang="css" scoped>
.avartar-name img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.avartar-name p {
  font-size: 20px;
  padding-left: 10px;
  padding-top: 10px;
}

.mobile-profile {
  display: none;
}

.border-content-profile {
  border-top: 1px solid #2761e6;
  height: 5px;
  background-color: #cbe0ff;
  margin-bottom: 5px;
}

@media only screen and (max-width: 600px) {
  .avartar-name {
    display: flex;
    padding-left: 10px;
  }

  .mobile-profile {
    display: flex;
  }
}
</style>
