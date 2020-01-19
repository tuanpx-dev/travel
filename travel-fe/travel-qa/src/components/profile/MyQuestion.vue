<template>
  <div class="my-question col-md-9">
    <div class="avartar-name mobile-profile">
      <img
        :src="user.avatar"
        alt
      />
      <p>name</p>
    </div>
    <div class="border-content-profile mobile-profile"></div>

    <div v-for="question in questions" :key="question.id">
      <Question :question="question" :page="'myquestion'"/>
      <div class="my-question-item"></div>
    </div>
  </div>
</template>

<script>
import request from '../../../request/request'
import Question from '../home/Question'
import {URL} from '../../api/URL'
export default {
  name: 'MyQuestion',
  components: {
    Question
  },
  data () {
    return {
      loading: false,
      questions: [],
      user: {}
    }
  },

  created () {
    if (!JSON.parse(localStorage.getItem('user'))) {
      this.user = {
        id: ''
      }
    } else {
      this.user = JSON.parse(localStorage.getItem('user')).data.user
    }
    request({
      url: URL.MY_QUESTION(0),
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
  border: 1px solid #ccc;
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

  .my-question-item {
    border-top: 1px solid #2761E6;
    height: 5px;
    background-color: #CBE0FF;
    margin-bottom: 5px;
  }
}
</style>
