<template>
  <div class="comment-answer-question">
    <div class="comment-answer">
      <input type="text" v-model="comment" placeholder="Comment" @keyup.enter="addComment">
    </div>

    <div class="user-answer">
      <img v-if="answer.user.img" :src="answer.user.img" alt="">
      <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
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
    console.log(this.answer)
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
        url: URL.CREATE_COMMENT,
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
.comment-answer-question {
  margin: 5px 0;
  background-color: #F4F7FC;
  border: 1px solid #b8daff;
}

.user-answer {
  display: flex;
}

.user-answer img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.comment-answer {
  width: 100%;
  text-align: center;
  margin-top: 5px;
}

.comment-answer input {
  width: 95%;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 30px;
  padding-left: 10px;
}
</style>
