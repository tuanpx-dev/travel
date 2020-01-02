<template>
  <div>
    Comment
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import { URL } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
export default {
  name: 'Comment',
  props: [ 'question', 'page' ],
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
      request({
        url: URL.ANSWERS_QUESTION(this.question.id),
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

</style>
