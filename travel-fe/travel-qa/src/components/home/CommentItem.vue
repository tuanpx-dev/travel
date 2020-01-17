<template>
    <div class="comment-item">
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
            <b-dropdown-item @click="actionEdit">Edit</b-dropdown-item>
            <b-dropdown-item @click="deleteComment(comment.id)">Delete</b-dropdown-item>
          </b-dropdown>
        </div>
      </div>
      <p v-if="!isEditComment" class="body-comment">{{ comment.body }}</p>
      <input class="input-edit-comment" placeholder="comment editer" type="text" v-else v-model="commentText" @keyup.enter="editComment(comment.id)">
    </div>
</template>

<script>
import { URL } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
import { EventBus } from '../../eventBus'

export default {
  name: 'CommentItem',
  props: [ 'answer', 'comment', 'page' ],
  components: {
    Ask
  },

  data () {
    return {
      isEditComment: false,
      commentText: '',
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
  },

  methods: {

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

    actionEdit () {
      if (!JSON.parse(localStorage.getItem('user'))) return

      this.isEditComment = !this.isEditComment
      this.commentText = this.comment.body
    },

    editComment (id) {
      if (!JSON.parse(localStorage.getItem('user'))) return

      if (!this.commentText) return

      this.isSendComment = true
      const data = {
        body: this.commentText,
        answer_id: this.answer.id
      }

      request({
        url: URL.EDIT_COMMENT(id),
        method: 'put',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.commentText = ''
          EventBus.$emit('getlistcomment')
          this.isSendComment = false
          this.isEditComment = false
        })
        .catch((e) => {
          this.isSendComment = false

          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    deleteComment (id) {
      if (!JSON.parse(localStorage.getItem('user'))) return

      request({
        url: URL.DELETE_COMMENT(id),
        method: 'delete'
      })
        .then(res => {
          EventBus.$emit('getlistcomment')
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

.input-edit-comment {
    width: 100%;
    height: 40px;
    border-radius: 20px;
    border: 1px solid #ccc;
    margin: 5px 0;
    outline: none;
    padding-left: 10px;
}
</style>
