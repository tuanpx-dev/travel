<template>
  <div class="question">
    <div class="question-header">
      <div class="col-md-10 col-xs-11 question-header">
        <p class="question-header-menu">Question about</p>
        <p class="question-header-menu">Region</p>
        <p class="question-header-menu">Category</p>
      </div>
      <div class="coll-md-2">
        <b-dropdown v-if="page === 'detail-question' && user.id === question.user.id">
          <template v-slot:button-content>
            <i class="fa fa-pen" style="color: #2761E6"></i>
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
        <p><i class="far fa-heart" @click="likeQuestion(question.like)" :class="{ 'like-item' : question.like }"></i> {{ question.total_likes }}</p>&nbsp; &nbsp;
        <p v-if="question.total_answers > 0 || answres.length > 0"><i class="fa fa-comment" @click="showAnswer"></i> {{ hideAnswer ? question.total_answers : answres.length }}</p>
      </div>

      <div class="question-add-comment">
        <input type="text" placeholder="Answer this question" v-model="answre" @keyup.enter="addAnswer" :disabled="isSendAnswer">
      </div>

      <div v-if="(question.total_answers > 0 || answres.length > 0) && !hideAnswer">
        <div v-for="answre in answres" :key="answre.id">
          <div class="question-comment">
            <div class="question-user">
              <img v-if="answre.user.img" :src="answre.user.img" alt="">
              <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
            </div>
            <div class="question-answer">

              <div class="comment-user">
                <p>{{answre.user.username}}</p> <p>{{answre.created_at | moment('DD/MM')}}</p>
              </div>

              <p>{{ answre.body }}</p>
            </div>

            <div class="coll-md-2">
              <b-dropdown v-if="page === 'detail-question' && user.id === answre.user.id">
                <template v-slot:button-content>
                  <i class="fa fa-pen" style="color: #2761E6"></i>
                </template>
                <b-dropdown-item @click="editAnswer(answre.id)">Edit</b-dropdown-item>
                <b-dropdown-item @click="deleteAnswer(answre.id)">Delete</b-dropdown-item>
              </b-dropdown>
            </div>
          </div>

          <div class="question-review">
            <p><i class="far fa-heart" @click="likeAnswer(answre)" :class="{ 'like-item' : answre.like }"></i> {{ answre.total_likes }}</p>
          </div>
          <div class="comment-section" v-if="page !== 'myAnswer'">
            <Comment :answer="answre" :page="page"/>
          </div>
        </div>
      </div>
    </div>

    <Ask
      v-if="isshowQuestion"
      :name="'edit-question'"
      @closeASK="closeASK"
      :question="question"
      :width="'90%'"
    />
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import { URL, URL_INCOGNITO } from '../../api/URL'
import request from '../../../request/request'
import Ask from '../ask/ask'
import Comment from './Comment'

export default {
  name: 'Question',
  props: [ 'question', 'page' ],
  components: {
    Ask,
    Comment
  },
  data () {
    return {
      user: {},
      isshowQuestion: false,
      loading: false,
      hideAnswer: true,
      isShowComment: false,
      answres: [],
      like: 0,
      answre: '',
      isSendAnswer: false
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

    if (this.page === 'detail-question' || this.page === 'myAnswer') {
      this.hideAnswer = false
      this.getListAnswer(this.question.id)
    }
  },

  methods: {
    viewDetail () {
      if (this.page !== 'home') return
      this.$router.push({ path: '/detail-question', query: { id: this.question.id } })
    },

    showAnswer () {
      this.getListAnswer()
      this.hideAnswer = !this.hideAnswer
    },

    getListAnswer () {
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
          this.answres = res.data.content
        })
        .catch((e) => {
          if (e.response.status === '401') {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    addAnswer () {
      if (!this.answre) return
      this.isSendAnswer = true
      const data = {
        body: this.answre,
        question_id: this.question.id
      }

      request({
        url: URL.CREATE_ANSWER,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.answre = ''
          this.hideAnswer = false
          this.getListAnswer()
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

    editAnswer (id) {

    },

    showComment (answre) {
      this.isShowComment = !this.isShowComment
      this.getListComment(answre)
    },

    getListComment (answre) {
      request({
        url: URL.ANSWERS_COMMENT(answre.id),
        method: 'get'
      })
        .then(res => {
          this.answres = res.data.content
        })
        .catch((e) => {
          if (e.response.status === '401') {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    likeAnswer (answer) {
      if (!JSON.parse(localStorage.getItem('user'))) return

      if (answer.like) return

      request({
        url: URL.LIKE_ANSWER,
        method: 'post',
        data: JSON.stringify({
          answer_id: answer.id
        })
      })
        .then(res => {
          this.getListAnswer()
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    deleteAnswer (id) {
      request({
        url: URL.DELETE_ANSWER(id),
        method: 'delete'
      })
        .then(res => {
          this.getListAnswer()
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    likeQuestion (like) {
      if (!JSON.parse(localStorage.getItem('user'))) return

      if (like) return

      const data = {
        question_id: this.question.id
      }

      request({
        url: URL.LIKE_QUESTION,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.question.like = true
          this.question.total_likes = this.question.total_likes + 1
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
          this.$router.push({ path: '/' })
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    editQuestion () {
      this.isshowQuestion = true
      setTimeout(() => {
        this.$modal.show('edit-question')
      }, 500)
    },

    closeASK () {
      this.isshowQuestion = false
      this.$modal.hide('edit-question')
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

.question-answer {
  width: 100%;
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

.question-title:hover {
  cursor: pointer;
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
  border: 1px solid #ccc;
  border-radius: 3px;
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

.like-item {
  color: #ADC3F6;
}

@media only screen and (max-width: 600px) {
  .question   {
    border: none;
  }
}
</style>
