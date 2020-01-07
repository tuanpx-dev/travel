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
import { URL } from '../../api/URL'
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
      isEditComment: false,
      comment: '',
      isSendComment: false
    }
  },

  created () {
    this.getListComment()
  },

  methods: {
    getListComment () {
      request({
        url: URL.ANSWERS_COMMENT(this.answer.id),
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

    addComment () {
      if (!this.comment) return

      this.isSendComment = true
      const data = {
        body: this.comment,
        answer_id: this.answer.id
      }

      request({
        url: URL.COMMENT,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.comment = ''
          this.getListComment()
          this.isSendComment = false
        })
        .catch((e) => {
          this.isSendComment = false

          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    editComment () {

    },

    deletecomment () {
      request({
        url: URL.DELETE_COMMENT(this.question.id),
        method: 'delete'
      })
        .then(res => {
          this.getListComment()
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
