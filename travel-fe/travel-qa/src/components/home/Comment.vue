<template>
  <div class="comment-answer-question">
    <div class="comment-answer">
      <input type="text" v-model="comment" placeholder="Comment" @keyup.enter="addComment">
    </div>

    <!-- <div v-for="comment in comments" :key="comment.id" class="comment-item">
      <div class="user-answer-header">
        <div class="user-answer">
          <img v-if="comment.user.img" :src="comment.user.img" alt="">
          <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
          <p>{{ comment.user.username }} &nbsp; {{comment.created_at | moment('DD/MM')}}</p>
        </div>

        <div class="coll-md-2">
          <b-dropdown v-if="page === 'detail-question' && user.id === comment.user.id">
            <template v-slot:button-content>
              <i class="fa fa-pen" style="color: #2761E6"></i>
            </template>
            <b-dropdown-item @click="isEditComment =! isEditComment">Edit</b-dropdown-item>
            <b-dropdown-item @click="deleteComment(comment.id)">Delete</b-dropdown-item>
          </b-dropdown>
        </div>
      </div>
      <p v-if="!isEditComment" class="body-comment">{{ comment.body }}</p>
      <input type="text" v-else v-model="commentText" @keyup.enter="editComment(comment.id)">
    </div> -->
    <div v-for="comment in comments" :key="comment.id">
     <CommentItem  :comment="comment" :page="page" :answer="answer"/>
    </div>
  </div>
</template>

<script>
import { URL } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
import CommentItem from './CommentItem'
import { EventBus } from '../../eventBus'

export default {
  name: 'Comment',
  props: [ 'answer', 'page' ],
  components: {
    Ask,
    CommentItem
  },

  data () {
    return {
      isEditComment: false,
      commentText: '',
      comment: '',
      comments: [],
      isSendComment: false,
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

    this.getListComment()
  },

  updated () {
    EventBus.$on('getlistcomment', () => {
      this.getListComment()
    })
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
  margin: 5px 0;
}

.comment-answer input {
  width: 95%;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 30px;
  padding-left: 10px;
  outline: none;
}

.comment-item {
  padding: 10px 10px 0 10px;
}

.body-comment {
  padding: 5px 0 0 5px;
}

.user-answer-header {
  display: flex;
  justify-content: space-between;
}
</style>
