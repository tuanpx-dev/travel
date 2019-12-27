<template>
  <div class="question" v-if="page === 'home'">
    <div class="question-header col-md-12">
      <p class="question-header-menu">Question about</p>
      <p class="question-header-menu">Region</p>
      <p class="question-header-menu">Category</p>
    </div>

    <div class="question-content col-md-12">
      <div class="question-user">
        <img v-if='question.user.img' :src="question.user.img" alt="">
        <img v-else src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
        <p class="question-title">{{question.title}}</p>
      </div>
      <p class="question-des">Question details <br/>{{question.des}}</p>
      <div class="question-review">
        <p v-if="question.total_likes"><i class="fa fa-heart" ></i> {{question.total_likes}}</p>&nbsp; &nbsp;
        <p v-if="question.total_answers > 0"><i class="fa fa-comment" @click="showComment"></i> {{question.total_answers}}</p>
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

      <div class="question-add-comment">
        <input type="text" placeholder="Answer this question">
      </div>
    </div>
  </div>
</template>

<script>
import { URL } from '../../api/URL'
import request from '../../../request/request'
export default {
  name: 'Question',
  props: [ 'question', 'page' ],
  data () {
    return {
      loading: false,
      hideComment: true,
      comments: []
    }
  },

  methods: {
    showComment () {
      if (this.hideComment) {
        this.getListComment()
      } else {
        this.hideComment = true
      }
    },

    getListComment () {
      request({
        url: URL.ANSWERS_QUESTION(this.question.id),
        method: 'get'
      })
        .then(res => {
          this.hideComment = false
          this.comments = res.data.content
        })
        .catch((e) => {
          if (e.response.status === '401') {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    }
  }
}
</script>

<style lang="css" scoped>
.question {
  width: 100%;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  text-align: left;
}

.question-header {
  display: flex;
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
</style>
