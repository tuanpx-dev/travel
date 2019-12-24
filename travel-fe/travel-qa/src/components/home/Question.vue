<template>
  <div class="question" v-if="page === 'home'">
    <div class="question-header col-md-12">
      <p class="question-header-menu">Question about</p>
      <p class="question-header-menu">Region</p>
      <p class="question-header-menu">Category</p>
    </div>

    <div class="question-content col-md-12">
      <div class="question-user">
        <img :src="question.user.img" alt="">
        <p class="question-title">{{question.title}}</p>
      </div>
      <p class="question-des">Question details <br/>{{question.des}}</p>
      <div class="question-review">
        <p v-if="question.like"><i class="fa fa-heart" ></i> {{question.like}}</p>&nbsp; &nbsp;
        <p v-if="question.comments.length > 0"><i class="fa fa-comment" @click="showComment = !showComment"></i> {{question.comments.length}}</p>
      </div>

      <div class="question-comment" v-if="showComment" v-for="comment in question.comments" :key="comment.id">
        <div class="question-user">
          <img :src="question.user.img" alt="">
        </div>
        <div class="question-answer">
          <div class="comment-user">
            <p>{{comment.user.name}}</p> <p>{{comment.time}}</p>
          </div>
          <p>{{ comment.des }}</p>
        </div>
      </div>

      <div class="question-add-comment">
        <input type="text" placeholder="Answer this question">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Question',
  props: [ 'question', 'page' ],
  data () {
    return {
      loading: false,
      showComment: false
    }
  },

  created () {
  },

  methods: {
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
