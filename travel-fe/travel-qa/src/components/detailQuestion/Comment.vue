<template>
  <div>
    <div class="user-answer">
      <img v-if="answer.user.img" :src="answer.user.img" alt="">
      <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
      <div>
        <p>name</p>
        <p>time</p>
      </div>
    </div>

    <p>detail of the answer</p>

    <div class="question-review">
      <p><i class="fa fa-heart"></i> 1 </p>&nbsp; &nbsp;
      <p><i class="fa fa-comment"></i>1</p>
    </div>
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import { URL, URL_INCOGNITO } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
export default {
  name: 'Comment',
  props: [ 'answer', 'page' ],
  components: {
    Ask
  },
  data () {
    return {
      showPopup: false,
      loading: false,
      hideComment: true,
      comments: [],
      like: 0,
      answres: '',
      isSendAnswer: false
    }
  },

  created () {
    this.getListComment()
  },

  methods: {
    showAnswerComment () {
      this.getListComment()
      this.hideComment = !this.hideComment
    },

    getListComment () {
      let url = ''

      if (!JSON.parse(localStorage.getItem('user'))) {
        url = URL_INCOGNITO.ANSWERS_QUESTION(this.question.id)
      } else {
        url = URL.ANSWERS_QUESTION(this.question.id)
      }
      request({
        url: url,
        method: 'get'
      })
        .then(res => {
          this.comments = res.data.content
        })
        .catch((e) => {
          if (e.response.status === '401') {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    addAnswerComment () {
      if (!this.answres) return
      this.isSendAnswer = true
      const data = {
        body: this.answres,
        question_id: this.question.id
      }

      request({
        url: URL.ANSWERS,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.answres = ''
          this.hideComment = false
          this.getListComment()
          this.isSendAnswer = false
        })
        .catch((e) => {
          this.isSendAnswer = false
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    likeQuestion () {
      const data = {
        question_id: this.question.id
      }

      request({
        url: URL.LIKE_QUESTION,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          // todo
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    deleteQuestion () {
      request({
        url: URL.DELETE_QUESTION(this.question.id),
        method: 'delete'
      })
        .then(res => {
          EventBus.$emit('closeFormCreateASK')
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
.user-answer {
  display: flex;
}
</style>
