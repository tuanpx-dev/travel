<template>
  <div class="question" v-if="page === 'home'">
    <div class="question-header col-md-12">
      <div class="coll-md-10 question-header">
        <p class="question-header-menu">Question about</p>
        <p class="question-header-menu">Region</p>
        <p class="question-header-menu">Category</p>
      </div>
      <div class="coll-md-2">
        <b-dropdown v-if="this.page !== 'home'">
          <template v-slot:button-content>
            <i class="fa fa-edit"></i>
          </template>
          <b-dropdown-item @click="editQuestion">Edit</b-dropdown-item>
          <b-dropdown-item @click="deleteQuestion">Delete</b-dropdown-item>
        </b-dropdown>
      </div>
    </div>

    <div class="question-content col-md-12">
      <div class="question-user">
        <p class="question-title" @click="viewDetail">{{question.title}}</p>
      </div>
      <p class="question-des">Question details <br/>{{question.body}}</p>
      <div class="poster">
        <p class="img-poster">P</p>
        <p>{{ question.user.username }} &nbsp; Poster: {{ question.created_at | moment('DD/MM') }}</p>
      </div>
      <div class="question-review">
        <p><i class="fa fa-heart" @click="likeQuestion"></i> {{ like }}</p>&nbsp; &nbsp;
        <p v-if="comments.length > 0"><i class="fa fa-comment" @click="showComment"></i> {{ comments.length }}</p>
      </div>

      <div class="question-add-comment">
        <input type="text" placeholder="Answer this question" v-model="answres" @keyup.enter="addAnswer" :disabled="isSendAnswer">
      </div>

      <div v-if="question.total_answers > 0 && !hideComment">
        <div class="question-comment" v-for="comment in comments" :key="comment.id">
          <div class="question-user">
            <img v-if="comment.user.img" :src="comment.user.img" alt="">
            <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
          </div>
          <div class="question-answer">
            <div class="comment-user">
              <p>{{comment.user.username}}</p> <p>{{comment.created_at | moment('DD/MM')}}</p>
            </div>
            <p>{{ comment.body }}</p>
          </div>
        </div>
      </div>
    </div>

    <Ask
      v-if="showPopup"
      @closeASK="closeASK"
      :question="question"
      :name="'edit-question'"
    />
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import { URL } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
export default {
  name: 'Question',
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
    viewDetail () {
      this.$router.push({ path: '/detail-question', query: { id: this.question.id } })
    },

    showComment () {
      this.hideComment = !this.hideComment

      if (!this.hideComment) {
        this.getListComment()
      }
    },

    getListComment () {
      request({
        url: URL.ANSWERS_QUESTION(this.question.id),
        method: 'get'
      })
        .then(res => {
          this.comments = res.data.content
          console.log(this.comments.length);
          
        })
        .catch((e) => {
          if (e.response.status === '401') {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    addAnswer () {
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
    },

    editQuestion () {
      this.showPopup = true
      this.$modal.show('edit-question')
    },

    closeASK () {
      this.showPopup = false
      // this.$modal.hide('create-new-ask')
    }
  }
}
</script>

<style lang="css">
.question {
  width: 100%;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  text-align: left;
}

.question-header {
  display: flex;
  justify-content: space-between;
}

.question-header-menu {
  margin: 10px 20px 10px 0;
}

.question-content {
  /* text-align: left; */
}

.question-comment {
  display: flex;
}

.question-user {
  display: flex;
}

.question-user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.question-answer p{
  word-break: break-word;
}

.comment-user {
  display: flex;
}

.comment-user p {
  margin-right: 10px;
  padding-top: 10px;
  font-size: 16px;
}

.question-title {
  font-size: 18px;
  font-weight: bold;
}

.question-des {
  width: 100%;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 5;
}

.question-review {
  font-size: 20px;
  display: flex;
}

.question-add-comment {
  margin-bottom: 5px;
}

.question-add-comment input {
  width: 100%;
  height: 40px;
  padding-left: 10px;
}

/* poster */
.poster {
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
}

.img-poster {
  width: 22px;
  height: 22px;
  margin-right: 10px;
  border: 1px solid #ccc;
  text-align: center;
  border-radius: 50%;
}

/* edit-create-question */
.btn-secondary {
  background: none;
  border: none;
  color: gray;
}
</style>
